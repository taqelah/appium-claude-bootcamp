// Session 2 · Parallel lab — WebdriverIO config (Mocha + Appium)
// ----------------------------------------------------------------
// Runs the login suite across TWO emulators at the same time:
//   • maxInstances lets both sessions run concurrently.
//   • Each capability is pinned to its own device (`appium:udid`) and its own
//     UiAutomator2 port (`appium:systemPort`) so the two sessions never collide.
//   • Each capability also points at its OWN Appium server (`port` 4723 / 4724) —
//     WDIO reads `port`/`hostname` per capability (falling back to the top-level
//     values). One server per device is the recommended setup: a wedged or crashed
//     session only takes down its own server, logs stay per-device, and the two
//     sessions don't share one Node process.
//   • Per-capability `specs` SHARD the suite — device A runs group-a, device B
//     runs group-b — so the total wall-clock is ~half of running them one
//     after another on a single device.
//
// Prereqs (see ../README.md): TWO emulators booted (emulator-5554 + emulator-5556) ·
// TWO Appium servers running (`appium -p 4723` and `appium -p 4724`) ·
// demo APK installed on BOTH.

const ANDROID = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  'appium:appPackage': 'com.taqelah.demo_app',
  'appium:appActivity': '.MainActivity',
  'appium:newCommandTimeout': 180,
}

export const config = {
  runner: 'local',

  hostname: process.env.APPIUM_HOST || '127.0.0.1',
  port: Number(process.env.APPIUM_PORT) || 4723,

  maxInstances: 2,                 // up to 2 sessions at the same time

  waitforTimeout: 20000,

  capabilities: [
    {
      // Device A — its own Appium server on :4723, runs group-a.e2e.js
      hostname: process.env.APPIUM_HOST || '127.0.0.1',
      port: 4723,
      ...ANDROID,
      'appium:udid': 'emulator-5554',
      'appium:systemPort': 8200,
      specs: ['./test/specs/group-a.e2e.js'],
    },
    {
      // Device B — its own Appium server on :4724, runs group-b.e2e.js
      hostname: process.env.APPIUM_HOST || '127.0.0.1',
      port: 4724,
      ...ANDROID,
      'appium:udid': 'emulator-5556',
      'appium:systemPort': 8201,
      specs: ['./test/specs/group-b.e2e.js'],
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
