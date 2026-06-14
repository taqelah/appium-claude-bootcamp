// Session 2 · Gestures lab — WebdriverIO config (Mocha + Appium)
// ----------------------------------------------------------------
// Target app: taqelah/demo-app v1.0.0 (Flutter). Each spec logs in (helpers/login.js),
// lands on the scrollable home, then performs ONE gesture group with Android `mobile:`
// gesture commands (scrollGesture, swipeGesture, dragGesture, pinch*, longClickGesture,
// doubleClickGesture) — driven by coordinates computed from the screen size.
//
// Prereqs (see ../README.md):
//   1. An Android emulator is booted   →  `adb devices` shows it as "device"
//   2. The Appium server is running     →  run `appium` in another terminal (port 4723)
//   3. The demo app is installed         →  `adb install DemoApp-v1.0.0.apk`
//
// Run:   npm install   &&   npm test

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
    timeout: 90000,
  },
}
