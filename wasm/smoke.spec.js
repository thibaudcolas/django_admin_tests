const { test, expect } = require('@playwright/test');

const BASE = '/django_admin_tests/';
const ADMIN = `${BASE}latest/english/admin/`;

test('boots a deep link, edits through Django, and persists across worker restarts', async ({ page, context, request, browser }) => {
  // There is only a static server: an HTTP client gets the launcher, not Django.
  const launcher = await request.get(ADMIN);
  expect(launcher.status()).toBe(404);
  expect(await launcher.text()).toContain('Starting Django admin tests');
  const missingAsset = await request.get(`${BASE}static/missing.css`);
  expect(missingAsset.status()).toBe(404);
  expect(await missingAsset.text()).not.toContain('Starting Django admin tests');

  await page.goto(ADMIN);
  await expect(page.getByLabel('Username:')).toBeVisible({ timeout: 120000 });
  await page.getByLabel('Username:').fill('admin');
  await page.getByLabel('Password:', { exact: true }).fill('correcthorsebatterystaple');
  await page.getByRole('button', { name: 'Log in', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Log out', exact: true })).toBeVisible();

  // Actual POST, redirect and session cookies, not a captured HTML form.
  const groupName = 'Browser persistence smoke test';
  await page.goto(`${ADMIN}auth/group/add/`);
  await page.getByLabel('Name:', { exact: true }).fill(groupName);
  await page.getByRole('button', { name: 'Save', exact: true }).click();
  await expect(page.locator('#result_list').getByRole('link', { name: groupName, exact: true })).toBeVisible();
  const changeURL = await page.locator('#result_list').getByRole('link', { name: groupName, exact: true }).getAttribute('href');

  // Invalid CSRF is still rejected. The service worker doesn't bypass middleware.
  const csrfStatus = await page.evaluate(async (url) => {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: 'name=Must+not+be+saved',
    });
    return response.status;
  }, `${ADMIN}auth/group/add/`);
  expect(csrfStatus).toBe(403);

  const cdp = await context.newCDPSession(page);
  await cdp.send('ServiceWorker.enable');
  await cdp.send('ServiceWorker.stopAllWorkers');
  await cdp.detach();
  const restored = await page.reload();
  expect(restored.headers()['x-django-runtime']).toBe('Pyodide service worker');
  await expect(page.getByRole('button', { name: 'Log out', exact: true })).toBeVisible();
  await expect(page.locator('#result_list').getByRole('link', { name: groupName, exact: true })).toBeVisible();

  // Dynamic query strings and static resources work after the cold restart.
  await page.goto(`${ADMIN}auth/group/?q=NoSuchGroupForSmokeTest`);
  await expect(page.locator('#result_list').getByRole('link', { name: groupName, exact: true })).toHaveCount(0);
  expect(await page.evaluate(async (url) => {
    const response = await fetch(url);
    return [response.status, response.headers.get('Content-Type')];
  }, `${BASE}static/admin/css/base.css`)).toEqual([200, 'text/css']);

  // The demo's SVG styleguide reads files inside the Python package.
  const styleguide = await page.goto(`${ADMIN}styleguide/`);
  expect(styleguide.status()).toBe(200);
  await expect(page.locator('svg').first()).toBeVisible();

  // Delete through the confirmation form as well.
  await page.goto(new URL(changeURL, `http://127.0.0.1:8002${ADMIN}auth/group/`).href);
  await page.locator('.deletelink').click();
  await page.getByRole('button', { name: /Yes, I’m sure/ }).click();
  await expect(page.locator('#result_list').getByRole('link', { name: groupName, exact: true })).toHaveCount(0);

  await page.getByRole('button', { name: 'Log out', exact: true }).click();
  await page.goto(ADMIN);
  await expect(page.getByLabel('Username:')).toBeVisible();

  // A separate browser context gets its own seed and session.
  const isolated = await browser.newContext();
  try {
    const otherPage = await isolated.newPage();
    await otherPage.goto(`http://127.0.0.1:8002${ADMIN}`);
    await expect(otherPage.getByLabel('Username:')).toBeVisible({ timeout: 120000 });
  } finally {
    await isolated.close();
  }
});
