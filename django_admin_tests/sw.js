/* global importScripts, loadPyodide */
// Adapted from bakerydemo-webassembly; see LICENSE.bakerydemo.
const BASE = '/django_admin_tests/';
// Import at evaluation time so a terminated worker can start again.
importScripts(`${BASE}runtime/xhr-shim.js`);
self.XMLHttpRequest = self.XMLHttpRequestShim;
importScripts(`${BASE}runtime/pyodide.js`, `${BASE}runtime/pyodide.asm.js`);

const BUILD = 'beebe4f17879f23d';
let runtime;
let queue = Promise.resolve();

function syncFilesystem(pyodide, populate) {
  return new Promise((resolve, reject) => {
    pyodide.FS.syncfs(populate, (error) => (error ? reject(error) : resolve()));
  });
}

async function progress(message) {
  const clients = await self.clients.matchAll({ includeUncontrolled: true });
  clients.forEach((client) =>
    client.postMessage({ type: 'progress', message }),
  );
}

async function initialize() {
  await progress('Loading Python and WebAssembly libraries…');
  const pyodide = await loadPyodide({ indexURL: `${BASE}runtime/` });
  const manifestResponse = await fetch(`${BASE}manifest.json`, { cache: 'no-store' });
  if (!manifestResponse.ok) throw new Error('Could not download the build manifest.');
  const manifest = await manifestResponse.json();
  if (manifest.build !== BUILD) {
    throw new Error(
      `The demo has been rebuilt. Open ${BASE}index.html to load the new version.`,
    );
  }
  await pyodide.loadPackage(manifest.packages);
  await progress('Unpacking Django and the demo…');
  const response = await fetch(`${BASE}app.zip?build=${BUILD}`, { cache: 'no-store' });
  if (!response.ok) throw new Error('Could not download the Django bundle.');
  const archive = await response.arrayBuffer();
  const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', archive));
  const archiveBuild = Array.from(digest, (byte) =>
    byte.toString(16).padStart(2, '0'),
  )
    .join('')
    .slice(0, 16);
  if (archiveBuild !== BUILD)
    throw new Error(
      `The demo bundle changed while loading. Open ${BASE}index.html and try again.`,
    );
  pyodide.unpackArchive(archive, 'zip', {
    extractDir: '/app',
  });
  // Separate database per build: schema upgrades never overwrite an older demo.
  const statePath = `/state/${BUILD}`;
  pyodide.FS.mkdirTree(statePath);
  pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, statePath);
  pyodide.FS.symlink(statePath, '/persist');
  await syncFilesystem(pyodide, true);
  await progress('Opening the fixture database…');
  pyodide.runPython(`
import os, sys, shutil
from pathlib import Path
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.wasm_settings'
# All WSGI calls are synchronous and serialized by the JavaScript queue.
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
sys.path[:0] = ['/app', '/app/vendor']
os.chdir('/app')
if not Path('/persist/db.sqlite3').exists():
    shutil.copytree('/app/seed', '/persist', dirs_exist_ok=True)
import bridge
`);
  await syncFilesystem(pyodide, false);
  await progress('Ready');
  return { pyodide, handle: pyodide.globals.get('bridge').handle_request };
}

function ready() {
  if (!runtime) {
    runtime = initialize().catch((error) => {
      runtime = null;
      throw error;
    });
  }
  return runtime;
}

// The filesystem and SQLite connection belong to one interpreter. Include the
// persistence flush in the queue so concurrent fetches cannot race a syncfs.
function serial(operation) {
  const result = queue.then(operation);
  queue = result.catch(() => {});
  return result;
}

async function djangoResponse(request) {
  const { pyodide, handle } = await ready();
  const body = new Uint8Array(await request.arrayBuffer());
  const metadata = JSON.stringify({
    url: request.url,
    method: request.method,
    headers: Array.from(request.headers.entries()),
    referrer: request.referrer,
  });
  const result = handle(metadata, body);
  let data;
  try {
    data = result.toJs({ dict_converter: Object.fromEntries });
  } finally {
    result.destroy();
  }
  await syncFilesystem(pyodide, false);
  const headers = new Headers(data.headers);
  headers.set('X-Django-Runtime', 'Pyodide service worker');
  headers.set('Cache-Control', 'no-store');
  // Response bodies must be null for these statuses and for HEAD requests.
  const noBody =
    request.method === 'HEAD' || [204, 205, 304].includes(data.status);
  return new Response(noBody ? null : data.body, {
    status: data.status,
    headers,
  });
}

self.addEventListener('install', (event) =>
  event.waitUntil(self.skipWaiting()),
);
self.addEventListener('activate', (event) =>
  event.waitUntil(self.clients.claim()),
);

self.addEventListener('message', (event) => {
  if (event.data?.type === 'start') {
    event.waitUntil(
      serial(async () => {
        try {
          await ready();
          event.ports[0].postMessage({ type: 'ready' });
        } catch (error) {
          console.error(error);
          event.ports[0].postMessage({ type: 'error', message: String(error) });
        }
      }),
    );
  }
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  // Static files, runtime downloads, the launcher, and third-party requests
  // belong to the static host. Only application requests enter Django.
  if (
    url.origin !== self.location.origin ||
    !url.pathname.startsWith(BASE) ||
    url.pathname.startsWith(`${BASE}static/`) ||
    url.pathname.startsWith(`${BASE}runtime/`) ||
    [
      'index.html',
      '404.html',
      'boot.js',
      'sw.js',
      'app.zip',
      'manifest.json',
    ].some((path) => url.pathname === BASE + path)
  )
    return;
  event.respondWith(
    serial(() => djangoResponse(event.request)).catch((error) => {
      console.error(error);
      return new Response(
        `The browser demo could not handle this request.\n\n${error}\n\nOpen ${BASE}index.html to restart.`,
        {
          status: 503,
          headers: { 'Content-Type': 'text/plain; charset=utf-8' },
        },
      );
    }),
  );
});
