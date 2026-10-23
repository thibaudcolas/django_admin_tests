"""Package the installed Django revision and a demo database for static hosting."""

import hashlib
import importlib.metadata
import json
import os
import shutil
import sqlite3
import sys
import urllib.request
from contextlib import closing
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "wasm"
BUILD = SOURCE / ".build"
DIST = SOURCE / "dist"
SITE = DIST / "django_admin_tests"
PYODIDE_VERSION = "0.29.3"
CDN = f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/"
PACKAGES = ["sqlite3", "ssl", "tzdata"]
DEPENDENCIES = ["django", "asgiref", "sqlparse", "docutils"]


def download(url, target, checksum=None):
    """Reuse versioned downloads, but never reuse a partial or corrupt file."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        print(f"Downloading {target.name}", flush=True)
        with urllib.request.urlopen(url, timeout=120) as response:
            content = response.read()
        target.write_bytes(content)
    if checksum and hashlib.sha256(target.read_bytes()).hexdigest() != checksum:
        target.unlink()
        raise SystemExit(f"Checksum mismatch: {target}; rerun to download again.")


def main():
    if sys.version_info[:2] != (3, 13):
        raise SystemExit("Build with Python 3.13 to match Pyodide 0.29.3.")
    # Editable installs only list an import hook in distribution.files, so fail
    # explicitly rather than publishing a bundle with Django missing.
    for name in DEPENDENCIES:
        distribution = importlib.metadata.distribution(name)
        direct_url = json.loads(distribution.read_text("direct_url.json") or "{}")
        if direct_url.get("dir_info", {}).get("editable"):
            raise SystemExit(f"Install {name} without -e before building.")

    shutil.rmtree(BUILD, ignore_errors=True)
    shutil.rmtree(DIST, ignore_errors=True)
    BUILD.mkdir(parents=True)
    SITE.mkdir(parents=True)
    runtime = SOURCE / ".cache" / PYODIDE_VERSION
    for filename in [
        "pyodide.js",
        "pyodide.asm.js",
        "pyodide.asm.wasm",
        "python_stdlib.zip",
        "pyodide-lock.json",
    ]:
        download(CDN + filename, runtime / filename)
    lock = json.loads((runtime / "pyodide-lock.json").read_text())
    downloaded = set()

    def package(name):
        name = name.replace("_", "-").lower()
        if name in downloaded:
            return
        entry = lock["packages"][name]
        for dependency in entry["depends"]:
            package(dependency)
        target = runtime / entry["file_name"]
        download(CDN + target.name, target, entry["sha256"])
        downloaded.add(name)

    for name in PACKAGES:
        package(name)
    download(
        "https://cdn.jsdelivr.net/npm/xhr-shim@0.1.3/src/index.min.js",
        runtime / "xhr-shim.js",
    )
    shutil.copytree(runtime, SITE / "runtime")

    state = BUILD / "seed"
    state.mkdir()
    # SQLite backup includes any committed WAL contents without modifying the
    # developer's database. Migrations and credential resets affect only the copy.
    with (
        closing(
            sqlite3.connect(f"file:{ROOT / 'db.sqlite3'}?mode=ro", uri=True)
        ) as source,
        closing(sqlite3.connect(state / "db.sqlite3")) as destination,
    ):
        source.backup(destination)
    os.environ["DJANGO_SETTINGS_MODULE"] = "demo.wasm_settings"
    os.environ["DEMO_WASM_STATE"] = str(state)
    os.environ["DEMO_WASM_STATIC"] = str(SITE / "static")
    sys.path.insert(0, str(ROOT))
    import django

    django_dist = importlib.metadata.distribution("django")
    # A wheel built from Git records the source timestamp in its version. At
    # runtime Django otherwise invokes git (unsupported by WebAssembly), and
    # locally it can accidentally report this demo repository's commit date.
    changeset = django_dist.version.partition(".dev")[2] or None
    django.utils.version.get_git_changeset = lambda: changeset
    django.__version__ = django.get_version()
    django.setup()
    from django.contrib.auth import get_user_model
    from django.contrib.sessions.models import Session
    from django.core.management import call_command
    from django.db import connections

    call_command("check")
    call_command("makemigrations", check=True, dry_run=True, verbosity=0)
    call_command("migrate", interactive=False, verbosity=0)
    user, _ = get_user_model().objects.get_or_create(username="admin")
    user.is_staff = user.is_superuser = user.is_active = True
    user.set_password("correcthorsebatterystaple")
    user.save()
    Session.objects.all().delete()
    call_command("collectstatic", interactive=False, verbosity=0)
    connections.close_all()

    with ZipFile(SITE / "app.zip", "w", ZIP_DEFLATED) as bundle:
        for file in sorted((ROOT / "demo").rglob("*")):
            relative = file.relative_to(ROOT)
            if file.is_file() and "__pycache__" not in relative.parts:
                bundle.write(file, str(relative))
        for name in DEPENDENCIES:
            distribution = importlib.metadata.distribution(name)
            for file in distribution.files:
                if (
                    ".." in file.parts
                    or "__pycache__" in file.parts
                    or file.suffix in {".pyc", ".so", ".pyd"}
                ):
                    continue
                source = distribution.locate_file(file)
                if source.is_file():
                    if str(file) == "django/utils/version.py":
                        bundle.writestr(
                            str(Path("vendor") / file),
                            source.read_text()
                            + "\n# Frozen at build time: no subprocesses in WebAssembly.\n"
                            + f"def get_git_changeset():\n    return {changeset!r}\n",
                        )
                        continue
                    # Keep packaged static files too: the styleguide discovers
                    # and reads admin SVG icons with Django's staticfile finders.
                    bundle.write(source, str(Path("vendor") / file))
        bundle.write(SOURCE / "bridge.py", "bridge.py")
        bundle.write(state / "db.sqlite3", "seed/db.sqlite3")
        bundle.write(ROOT / "LICENSE", "LICENSE")
        bundle.write(SOURCE / "LICENSE.bakerydemo", "LICENSE.bakerydemo")

    build_id = hashlib.sha256((SITE / "app.zip").read_bytes()).hexdigest()[:16]
    manifest = {
        "build": build_id,
        "pyodide": PYODIDE_VERSION,
        "packages": PACKAGES,
        "django": django.get_version(),
        "django_source": json.loads(django_dist.read_text("direct_url.json") or "{}"),
        "dependencies": {
            name: importlib.metadata.version(name) for name in DEPENDENCIES
        },
    }
    (SITE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for filename in ["index.html", "boot.js", "sw.js"]:
        content = (SOURCE / filename).read_text().replace("__BUILD_ID__", build_id)
        (SITE / filename).write_text(content)
    # GitHub Pages uses 404.html for a first visit to a deep application URL.
    shutil.copyfile(SITE / "index.html", SITE / "404.html")
    shutil.copyfile(SITE / "index.html", DIST / "index.html")
    shutil.copyfile(SITE / "index.html", DIST / "404.html")
    shutil.copyfile(SOURCE / "LICENSE.bakerydemo", SITE / "LICENSE.bakerydemo")
    (SITE / ".nojekyll").touch()
    (DIST / ".nojekyll").touch()
    # Netlify/Cloudflare branch deployments publish the outer directory.
    for filename in ["_redirects", "_headers", "asset-not-found.html"]:
        shutil.copyfile(SOURCE / filename, DIST / filename)
    print(f"Built {SITE} ({build_id}), Django {django.get_version()}")


if __name__ == "__main__":
    main()
