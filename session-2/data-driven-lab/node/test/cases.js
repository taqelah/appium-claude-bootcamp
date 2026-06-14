// Shared login-case runner for the data-driven lab.
// Each source (inline / CSV / JSON) calls runLoginCases() with the SAME rows shape:
//   { case, user, password, shouldPass }
// so the login logic and assertion live in one place — only the data source changes.

const USERNAME = 'android=new UiSelector().className("android.widget.EditText").instance(0)'
const PASSWORD = 'android=new UiSelector().className("android.widget.EditText").instance(1)'
const LOGIN = '~Login'
const HOME = '~View All'   // only on the post-login home screen

export function runLoginCases(source, rows) {
  describe(`Data-driven login — from ${source}`, () => {
    beforeEach(async () => {
      await browser.reloadSession()   // fresh app per row → each case is isolated
    })

    rows.forEach(({ case: name, user, password, shouldPass }) => {
      it(`[${source}] ${name} → ${shouldPass ? 'reaches home' : 'stays on login'}`, async () => {
        const username = $(USERNAME)
        await username.waitForDisplayed({ timeout: 20000 })   // waits past the splash
        await username.click()
        await username.setValue(user)

        const pwd = $(PASSWORD)
        await pwd.click()
        await pwd.setValue(password)

        await $(LOGIN).click()

        // Home is reached only on a valid login; for bad rows it never appears.
        let reachedHome = false
        try {
          reachedHome = await $(HOME).waitForDisplayed({ timeout: 6000 })
        } catch {
          reachedHome = false
        }

        expect(reachedHome).toBe(shouldPass)
      })
    })
  })
}
