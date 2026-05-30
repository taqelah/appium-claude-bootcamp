// smoke.mjs — Prerequisite smoke test (Node.js + WebdriverIO).
//
// Proves the full chain works: WebdriverIO -> Appium server -> uiautomator2 -> your emulator.
// It opens a session with NO app, reads the device time, then quits. No APK needed.
//
// Before running:
//   1. Start an Android emulator (see docs/android-emulator.md) and wait for the home screen.
//   2. In a separate terminal, run:  appium
//   3. Here:  npm install && npm run smoke
//
// Expected: "SMOKE TEST PASSED" and your device's time.

import { remote } from 'webdriverio';

const capabilities = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  // No app/appPackage: we just connect to whatever is on the emulator.
  'appium:newCommandTimeout': 120,
};

const wdOpts = {
  hostname: process.env.APPIUM_HOST || '127.0.0.1',
  port: Number(process.env.APPIUM_PORT || 4723),
  path: '/',
  logLevel: 'error',
  capabilities,
};

let driver;
try {
  console.log('→ Connecting to Appium at %s:%d ...', wdOpts.hostname, wdOpts.port);
  driver = await remote(wdOpts);

  const time = await driver.getDeviceTime();
  const { width, height } = await driver.getWindowSize();

  console.log('  device time : %s', time);
  console.log('  screen size : %dx%d', width, height);
  console.log('\n✅ SMOKE TEST PASSED — WebdriverIO drove your emulator successfully.');
} catch (err) {
  console.error('\n❌ SMOKE TEST FAILED:', err.message || err);
  console.error('\nChecklist:');
  console.error('  • Is an emulator running?   adb devices   (should show "device")');
  console.error('  • Is Appium running?        appium        (in another terminal)');
  console.error('  • Driver installed?         appium driver list --installed');
  console.error('  • Deep diagnostics:         appium driver doctor uiautomator2');
  process.exitCode = 1;
} finally {
  if (driver) {
    await driver.deleteSession().catch(() => {});
  }
}
