// Session 2 · Waits lab — implicit vs explicit waits · WebdriverIO config (Mocha + Appium)
// -----------------------------------------------------------------------------------------
// Same target app as Session 1 Lab 2: taqelah/demo-app v1.0.0 (a Flutter app). It shows a
// SPLASH screen before the login form — so the very first element takes a moment to appear.
// That delay is exactly what waits are for. Two specs explore the two styles:
//
//   test/specs/implicit.e2e.js  →  ONE global implicit timeout; plain finds retry past splash
//   test/specs/explicit.e2e.js  →  per-step explicit conditions (waitForClickable / waitUntil)
//
// Prereqs (see ../README.md):
//   1. An Android emulator is booted   →  `adb devices` shows it as "device"
//   2. The Appium server is running     →  run `appium` in another terminal (port 4723)
//   3. The demo app is installed         →  `adb install DemoApp-v1.0.0.apk`
//
// Run:   npm install   &&   npm test

export const config = {
  runner: 'local',

  // WHERE the running Appium server is. (Devcontainer sets host.docker.internal.)
  hostname: process.env.APPIUM_HOST || '127.0.0.1',
  port: Number(process.env.APPIUM_PORT) || 4723,

  // WHICH test files to run — both wait specs.
  specs: ['./test/specs/**/*.e2e.js'],
  maxInstances: 1,

  // Default timeout for WebdriverIO's auto-wait + every `waitFor*` command (ms).
  // The explicit spec overrides this per call to show explicit control.
  waitforTimeout: 15000,

  // CAPABILITIES: launch the taqelah demo-app (install it first — see ../README.md).
  capabilities: [
    {
      platformName: 'Android',
      'appium:automationName': 'UiAutomator2',
      'appium:appPackage': 'com.taqelah.demo_app',
      'appium:appActivity': '.MainActivity',
      'appium:newCommandTimeout': 120,
    },
  ],

  logLevel: 'error',

  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: {
    ui: 'bdd',
    timeout: 60000,
  },
}
