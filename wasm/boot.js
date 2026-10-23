const BASE = '/django_admin_tests/';
const statusElement = document.querySelector('#status');

async function start() {
  if (!('serviceWorker' in navigator)) {
    throw new Error('Use HTTPS or localhost in a browser with service workers.');
  }
  // The root launcher on Netlify is outside the worker's scope.
  if (!location.pathname.startsWith(BASE)) {
    location.replace(BASE + location.search + location.hash);
    return;
  }
  navigator.serviceWorker.addEventListener('message', ({ data }) => {
    if (data?.type === 'progress') statusElement.textContent = data.message;
  });
  const registration = await navigator.serviceWorker.register(`${BASE}sw.js`, {
    scope: BASE,
    updateViaCache: 'none',
  });
  await registration.update();
  const worker = registration.installing || registration.waiting || registration.active;
  await new Promise((resolve, reject) => {
    function check() {
      if (worker.state === 'activated' || worker.state === 'redundant') {
        worker.removeEventListener('statechange', check);
        if (worker.state === 'activated') resolve();
        else reject(new Error('Service worker installation failed.'));
      }
    }
    worker.addEventListener('statechange', check);
    check();
  });
  await new Promise((resolve, reject) => {
    const channel = new MessageChannel();
    const timeout = setTimeout(() => {
      channel.port1.close();
      reject(new Error('Startup timed out. Please try again.'));
    }, 180000);
    channel.port1.onmessage = ({ data }) => {
      clearTimeout(timeout);
      channel.port1.close();
      if (data.type === 'ready') resolve();
      else reject(new Error(data.message));
    };
    worker.postMessage({ type: 'start' }, [channel.port2]);
  });
  if (!navigator.serviceWorker.controller) {
    await new Promise((resolve) => {
      function check() {
        if (navigator.serviceWorker.controller) {
          navigator.serviceWorker.removeEventListener('controllerchange', check);
          resolve();
        }
      }
      navigator.serviceWorker.addEventListener('controllerchange', check);
      check();
    });
  }
  const target = [BASE + 'index.html', BASE + '404.html'].includes(location.pathname)
    ? BASE + location.search + location.hash
    : location.href;
  location.replace(target);
}

start().catch((error) => {
  statusElement.textContent = `Could not start the demo: ${error.message}`;
  document.querySelector('#retry').hidden = false;
  console.error(error);
});
