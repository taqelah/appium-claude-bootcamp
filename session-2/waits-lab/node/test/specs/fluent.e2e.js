// Session 2 · Waits lab — FLUENT wait (WebdriverIO + Mocha)
// ---------------------------------------------------------
// App: taqelah/demo-app (Flutter), same SPLASH-then-login flow as the other specs.
//
// THE IDEA: a fluent wait is an EXPLICIT wait with two knobs turned —
//   • a custom POLL INTERVAL (how often to re-check), and
//   • ignoring TRANSIENT errors while polling.
// In WebdriverIO those knobs live right on every `waitFor*` / `waitUntil`:
//   { timeout, interval, timeoutMsg }   ← `interval` is the poll frequency.
// (WDIO's retry already swallows transient "not found" errors for you.)
//
// `$`, `browser` and `expect` are globals injected by the WebdriverIO test-runner.

const USERNAME = 'android=new UiSelector().className("android.widget.EditText").instance(0)'
const PASSWORD = 'android=new UiSelector().className("android.widget.EditText").instance(1)'
const LOGIN_BTN = '~Login'
const SUCCESS = '~View All'   // only on the post-login home screen

const USER = 'emma@demoapp.com'
const PASS = '10203040'

// Fluent knobs reused on every wait below.
const FLUENT = { timeout: 20000, interval: 500 }   // 20s ceiling, poll every 0.5s

describe('Fluent wait', () => {
  before(async () => {
    // Turn OFF the implicit wait — fluent is explicit-style, just tuned.
    await driver.setTimeout({ implicit: 0 })
  })

  it('waits with a custom poll interval at each step', async () => {
    const username = $(USERNAME)
    await username.waitForDisplayed(FLUENT)   // poll every 500ms up to 20s
    await username.click()
    await username.setValue(USER)

    const password = $(PASSWORD)
    await password.waitForDisplayed(FLUENT)
    await password.click()
    await password.setValue(PASS)

    const loginBtn = $(LOGIN_BTN)
    await loginBtn.waitForEnabled(FLUENT)
    await loginBtn.click()

    // CUSTOM CONDITION with the same fluent knobs — poll every 500ms until home loads.
    await browser.waitUntil(
      async () => await $(SUCCESS).isDisplayed(),
      { ...FLUENT, timeoutMsg: 'Expected the home screen (View All) after login' },
    )

    await expect($(SUCCESS)).toBeDisplayed()
  })
})
