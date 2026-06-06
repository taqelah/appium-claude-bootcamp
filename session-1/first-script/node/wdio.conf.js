// Session 1 — WebdriverIO test-runner config (Mocha + Appium)
// -----------------------------------------------------------
// This file holds steps 1 (capabilities) + 2 (connect) + 5 (quit) of every
// Appium test — the test-runner creates and tears down the session for you.
// Your spec (test/specs/*.e2e.js) only does step 3 (find) + step 4 (assert).
//
// Prereqs (see ../README.md):
//   1. An Android emulator is booted   →  `adb devices` shows it as "device"
//   2. The Appium server is running     →  run `appium` in another terminal (port 4723)
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

  // 1 — CAPABILITIES: the "order form" telling the server what to automate.
  //     We open the always-present Android Settings app, so there's no APK to install.
  //     (Full explanation: ../caps/android.md)
  capabilities: [
    {
      platformName: 'Android',
      'appium:automationName': 'UiAutomator2',
      'appium:appPackage': 'com.android.settings',
      'appium:appActivity': '.Settings',
      'appium:newCommandTimeout': 120,
    },
  ],

  logLevel: 'error',

  // Mocha gives us describe()/it() and runs the spec; the runner connects + quits.
  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: {
    ui: 'bdd',
    timeout: 60000,
  },
}
