// Session 2 · Waits lab — EXPLICIT wait (WebdriverIO + Mocha)
// -----------------------------------------------------------
// App: taqelah/demo-app (Flutter), same SPLASH-then-login flow as the implicit spec.
//
// THE IDEA: turn the global implicit wait OFF, then wait for a SPECIFIC condition at each
// step. An explicit wait returns the INSTANT the condition is true — never longer than it
// has to — and says exactly what it's waiting for (displayed, enabled, custom).
//
// ⚠️ NOTE: in a NATIVE app session, use `waitForDisplayed` / `waitForEnabled` / `waitForExist`.
//    `waitForClickable` (and `isClickable`) are browser-only — they throw in native context.
//
// `$`, `browser` and `expect` are globals injected by the WebdriverIO test-runner.

const USERNAME = 'android=new UiSelector().className("android.widget.EditText").instance(0)'
const PASSWORD = 'android=new UiSelector().className("android.widget.EditText").instance(1)'
const LOGIN_BTN = '~Login'
const SUCCESS = '~View All'   // only on the post-login home screen

const USER = 'emma@demoapp.com'
const PASS = '10203040'

describe('Explicit wait', () => {
  before(async () => {
    // Turn OFF the implicit wait so the explicit waits below are the only thing syncing us.
    await driver.setTimeout({ implicit: 0 })
  })

  it('waits for a specific condition at each step', async () => {
    // WAIT FOR DISPLAYED — the username field only appears after the splash.
    const username = $(USERNAME)
    await username.waitForDisplayed({ timeout: 15000 })
    await username.click()
    await username.setValue(USER)

    // WAIT FOR DISPLAYED — the password field.
    const password = $(PASSWORD)
    await password.waitForDisplayed({ timeout: 15000 })
    await password.click()
    await password.setValue(PASS)

    // WAIT FOR ENABLED — the Login button must be enabled before we tap it.
    const loginBtn = $(LOGIN_BTN)
    await loginBtn.waitForEnabled({ timeout: 15000 })
    await loginBtn.click()

    // CUSTOM CONDITION — wait until "View All" (home screen) is displayed. `waitUntil`
    // takes any boolean-returning function, so you can wait for *anything*.
    await browser.waitUntil(
      async () => await $(SUCCESS).isDisplayed(),
      { timeout: 15000, timeoutMsg: 'Expected the home screen (View All) after login' },
    )

    await expect($(SUCCESS)).toBeDisplayed()
  })
})
