# Django admin in WebAssembly

The static host serves a launcher, Python/Pyodide, the application bundle, and
collected CSS/JS. A service worker runs Django's synchronous WSGI application to
answer requests under `/django_admin_tests/`, including POSTs, redirects, query
strings, and error responses. There is no deployed Python server.

## Build and run locally

Use Python 3.13, matching Pyodide 0.29.3:

```sh
python3.13 -m venv .venv-wasm
source .venv-wasm/bin/activate
python -m pip install -r wasm/requirements.txt \
  'Django @ git+https://github.com/django/django.git@main'
python wasm/build.py
python wasm/serve.py
```

Open <http://127.0.0.1:8013/django_admin_tests/latest/english/admin/> and sign in
with **admin** / **correcthorsebatterystaple**. The first visit downloads about
30 MB before starting Django. JavaScript, WebAssembly, service workers, and
IndexedDB are required. Use HTTPS when deploying; localhost works over HTTP.

The local server uses port **8013** to keep a separate origin from
`bakerydemo-webassembly`, which uses port 8001. Service workers remain registered
after a server stops. Reusing its port can leave the bakery's root-scoped worker
intercepting this demo, causing requests to `/runtime/python_stdlib.zip` or JSON
parsing errors when a request receives an HTML error page. This demo's runtime
URLs start with `/django_admin_tests/runtime/`. Use the dedicated port rather than
clearing the bakery's storage. If overriding `--port`, choose an origin without
another application's service worker.

To preview a Django PR, install its head **without `-e`** before rebuilding:

```sh
python -m pip install --force-reinstall --no-deps \
  'Django @ git+https://github.com/django/django.git@refs/pull/19688/head'
python wasm/build.py
```

Alternatively install a local Django checkout with `python -m pip install
/path/to/django` (without `-e`). The build packages the installed distribution,
including templates, translations, admin assets, and distribution metadata.
`manifest.json` records its version, dependency versions, and Git commit when
installed from Git. Revisions must support Python 3.13 and the pinned dependencies.

The build copies `db.sqlite3` with SQLite's backup API, migrates only the copy,
clears its sessions, and resets the public admin credentials. It does not modify
the development database or install anything at browser startup. Generated files
live in `wasm/.build/` and `wasm/dist/`; downloads are cached in `wasm/.cache/`.

## Runtime behavior

- The existing English demo URLs are preserved. As with the previous CI build,
  only `latest/english` is packaged; the browser home page lists that variant.
- SQLite and the private session cookie jar persist in IndexedDB. Requests and
  filesystem flushes are serialized. Tabs on the same origin share this demo's
  login and data. Different browsers have separate copies.
- Each bundle has a separate database namespace, so a new build starts from its
  seed instead of applying schema changes to a visitor's edited database. Clear
  the site's browser storage to reset manually. Browser storage can be evicted.
- Service-worker responses cannot set browser cookies. The bridge keeps its own
  cookies, and CSRF uses Django sessions and rendered form tokens. Normal CSRF
  validation remains enabled. Auto-login middleware is disabled in this build.
- The debug toolbar is disabled, but `DEBUG=True` is intentional: Django's debug
  error pages are part of this test site. The SVG styleguide keeps working because
  the bundle also contains the admin assets used by staticfile finders.
- Development Django normally runs `git` to calculate its version. The packaged
  `get_git_changeset()` returns the installed wheel's recorded development
  timestamp instead, avoiding subprocesses and preserving the selected version.
- The source and database are downloadable demo assets with public credentials.
  This is a local playground; email stays in the console and the Spotify import
  command requires the normal Python environment. Offline startup is not provided.

After rebuilding, open `/django_admin_tests/index.html` to update the worker.
The worker checks the manifest and bundle hash so it won't silently start with
code from a different build. It reloads Python and restores state if the browser
stops the worker while idle. Dynamic responses have the header
`X-Django-Runtime: Pyodide service worker`.

## Hosting and GitHub Actions

The workflow builds on pushes, repository PRs, scheduled runs, and manual runs.
It tests the bridge before building and uploading artifacts. Browser smoke tests
are temporarily excluded from CI to keep builds fast; they remain available locally.
Publishing runs only from this repository's `main` branch, outside repository PRs:

| Target | Published directory | Deployment |
| --- | --- | --- |
| GitHub Pages project site | `wasm/dist/django_admin_tests/` | Actions Pages artifact, mounted at `/django_admin_tests/` |
| Netlify / Cloudflare Pages branch site | `wasm/dist/` | `gh-pages` or `preview-<Django PR number>` branch |

The outer distribution includes `_redirects` and `_headers` for branch hosting.
Existing files take precedence; application routes fall back to the launcher,
while missing static/runtime assets return 404. Disable host-side HTML/JS
post-processing so the supplied assets are served unchanged. GitHub Pages uses
the generated `404.html` launcher for a first visit to a deep URL. `serve.py`
simulates that behavior, including the initial HTTP 404 before the worker starts.

Serve `.wasm` as `application/wasm` and JavaScript with a JavaScript content type.
Do not apply immutable caching to `sw.js`, `boot.js`, `manifest.json`, `app.zip`,
or launcher HTML. Deploy the output together. No cross-origin isolation headers
are required. The worker is scoped to `/django_admin_tests/` and ignores requests
outside that prefix, including other GitHub Pages projects on the same origin.

Django PR numbers are validated before installation and preview branch publishing.
PR previews never replace the main GitHub Pages deployment. Building has only
read access to the repository; deployment permissions belong to separate jobs.

## Validation

```sh
python -m unittest discover -s wasm -p 'test_*.py'
python wasm/build.py
npm ci --prefix wasm
npx --prefix wasm playwright install chromium
npm test --prefix wasm
```

Activate `.venv-wasm` before these commands, or set `WASM_PYTHON` to the Python
executable for the smoke test's static server. The Chromium test starts its own
server on port 8002. It covers first-visit deep links, login, creating/deleting an
admin object, CSRF rejection, search, static assets, the SVG styleguide, logout,
and database/session recovery after a forced worker stop. Failed runs retain a
Playwright trace under `wasm/test-results/` for diagnosis.

The bridge tests cover byte-preserving multipart requests, Unicode paths, cookies,
and closing streaming responses. The existing Pa11y/Lighthouse suite still targets
the conventional development server; this smoke test validates the browser runtime.

## References

Adapted from the `bakerydemo-webassembly` WSGI bridge and worker, which in turn was
inspired by [django_webassembly](https://github.com/mattbutterfield/django_webassembly).
The adapted code's license is retained in [LICENSE.bakerydemo](LICENSE.bakerydemo)
and in the generated distribution.

- [Pyodide service workers](https://pyodide.org/en/0.29.3/usage/service-worker.html)
- [Pyodide filesystems and persistence](https://pyodide.org/en/0.29.3/usage/file-system.html)
