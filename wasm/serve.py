"""Serve the built files with a GitHub Pages-style 404 launcher fallback."""

import argparse
import io
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

DIST = Path(__file__).resolve().parent / "dist"
BASE = "/django_admin_tests/"


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def send_head(self):
        path = urlsplit(self.path).path
        if (
            path.startswith(BASE)
            and not path.startswith((BASE + "static/", BASE + "runtime/"))
            and not Path(self.translate_path(path)).exists()
        ):
            content = (DIST / "django_admin_tests/404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            return io.BytesIO(content)
        return super().send_head()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    # Keep a separate origin from bakerydemo-webassembly (port 8001): its
    # root-scoped service worker can otherwise intercept this demo's launcher.
    parser.add_argument("--port", type=int, default=8013)
    args = parser.parse_args()
    if not (DIST / "django_admin_tests/manifest.json").exists():
        parser.error("Run python wasm/build.py first.")
    server = ThreadingHTTPServer(
        ("127.0.0.1", args.port), partial(Handler, directory=str(DIST))
    )
    print(f"Open http://127.0.0.1:{args.port}{BASE}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
