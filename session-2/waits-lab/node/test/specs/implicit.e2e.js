// Session 2 · Waits lab — IMPLICIT wait (WebdriverIO + Mocha)
// -----------------------------------------------------------
// App: taqelah/demo-app (Flutter). It shows a SPLASH before the login form, so the first
// field isn't there the instant the app launches.
//
// THE IDEA: set ONE global implicit timeout, then find elements with PLAIN `$()` lookups.
// Each find auto-RETRIES for up to that timeout before failing — so the splash delay is
// absorbed without a single explicit wait and without `sleep`.
//
// `$` and `expect` are globals injected by the WebdriverIO test-runner.

const USERNAME = 'android=new UiSelector().className("android.widget.EditText").instance(0)'
const PASSWORD = 'android=new UiSelector().className("android.widget.EditText").instance(1)'
const LOGIN_BTN = '~Login'
const SUCCESS = '~View All'   // only on the post-login home screen

const USER = 'emma@demoapp.com'
const PASS = '10203040'

describe('Implicit wait', () => {
  before(async () => {
    // ⏳ IMPLICIT WAIT — set ONCE. Every element lookup now polls for up to 10s
    //    before throwing "no such element". This is the blunt, global safety net.
    await driver.setTimeout({ implicit: 100000 })
  })

  it('finds the login fields past the splash with no explicit waits', async () => {
    // Plain finds — no waitForDisplayed, no sleep. The implicit wait retries through
    // the splash until the username field exists.
    const username = $(USERNAME)
    await username.click()
    await username.setValue(USER)

    const password = $(PASSWORD)
    await password.click()
    await password.setValue(PASS)

    await $(LOGIN_BTN).click()

    // Still a plain find — implicit wait covers the screen transition too.
    await expect($(SUCCESS)).toBeExisting()
  })
})
