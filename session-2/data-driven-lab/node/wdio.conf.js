// Session 2 · Data-driven lab — WebdriverIO config (Mocha + Appium)
// -----------------------------------------------------------------
// Runs ONE login test over a table of credentials (data/credentials.json), generating one
// `it()` per row. A fresh app session per row (beforeEach reloadSession) keeps each case
// isolated — exactly the discipline the Parallel section relies on.
//
// Prereqs (see ../README.md): emulator booted · `appium` running · demo APK installed.

export const config = {
  runner: 'local',

  hostname: process.env.APPIUM_HOST || '127.0.0.1',
  port: Number(process.env.APPIUM_PORT) || 4723,

  specs: ['./test/specs/**/*.e2e.js'],
  maxInstances: 1,

  waitforTimeout: 20000,

  capabilities: [
    {
      platformName: 'Android',
      'appium:automationName': 'UiAutomator2',
      'appium:appPackage': 'com.taqelah.demo_app',
      'appium:appActivity': '.MainActivity',
      'appium:newCommandTimeout': 180,
    },
  ],

  logLevel: 'error',

  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: {
    ui: 'bdd',
    timeout: 120000,
  },
}
