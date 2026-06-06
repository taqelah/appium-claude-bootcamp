// Session 1 · Lab 2 — login flow · WebdriverIO test-runner config (Mocha + Appium)
// ---------------------------------------------------------------------------------
// Same shape as first-script/node/wdio.conf.js — the runner does capabilities +
// connect + quit; your spec (test/specs/login.e2e.js) does find → type → tap → assert.
//
// Target app: taqelah/demo-app v1.0.0 (a Flutter app). Install it first (see ../README.md).
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

  // WHICH test files to run.
  specs: ['./test/specs/**/*.e2e.js'],
  maxInstances: 1,

  // 1 — CAPABILITIES: launch the taqelah demo-app (install it first — see ../README.md).
  //     It's a Flutter app, so we launch its single activity by package + activity.
  //     Alternative: install on the fly with the release URL —
  //       'appium:app': 'https://github.com/taqelah/demo-app/releases/download/v1.0.0/DemoApp-v1.0.0.apk',
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
