// Session 1 · Lab 2 — automate a login flow (WebdriverIO + Mocha)
// ---------------------------------------------------------------
// App: taqelah/demo-app (Flutter). The runner already handled capabilities +
// connect + quit (wdio.conf.js). Here you do the Part 2 steps:
//   FIND → tap → sendKeys (setValue) → tap → ASSERT
//
// `$` and `expect` are globals injected by the WebdriverIO test-runner.
//
// 📝 It's a Flutter app, so there are NO `resource-id`s to use. We locate the two
//    text fields by UiAutomator class + instance, and the buttons by accessibility id.
//    (We tap each field before typing — Flutter inputs need focus first.)

const USERNAME = 'android=new UiSelector().className("android.widget.EditText").instance(0)'
const PASSWORD = 'android=new UiSelector().className("android.widget.EditText").instance(1)'
const LOGIN_BTN = '~Login'
const SUCCESS = '~View All'   // only on the post-login home screen — we ASSERT on it, not tap it

const USER = 'emma@demoapp.com'
const PASS = '10203040'

describe('Login flow', () => {
  it('logs in with valid credentials', async () => {
    // FIND + TYPE — tap to focus, then type (auto-waits past the splash screen).
    const username = $(USERNAME)
    await username.click()
    await username.setValue(USER)

    const password = $(PASSWORD)
    await password.click()
    await password.setValue(PASS)

    // TAP — submit the form.
    await $(LOGIN_BTN).click()

    // ASSERT — "View All" only appears on the home screen, so its presence proves login worked.
    await expect($(SUCCESS)).toBeDisplayed()
  })
})
