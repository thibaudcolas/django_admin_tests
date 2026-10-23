const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: '.',
  testMatch: 'smoke.spec.js',
  timeout: 180000,
  expect: { timeout: 30000 },
  workers: 1,
  use: {
    baseURL: 'http://127.0.0.1:8002',
    actionTimeout: 30000,
    navigationTimeout: 120000,
    trace: 'retain-on-failure',
  },
  webServer: {
    command: `${process.env.WASM_PYTHON || 'python3'} serve.py --port 8002`,
    url: 'http://127.0.0.1:8002/django_admin_tests/index.html',
    reuseExistingServer: false,
  },
});
