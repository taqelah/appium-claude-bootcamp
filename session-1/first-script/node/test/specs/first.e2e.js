// Session 1 — your first Appium test (WebdriverIO + Mocha)
// --------------------------------------------------------
// The test-runner already did the heavy lifting from wdio.conf.js:
//   1. capabilities   2. connect (session started)   5. quit (session closed)
// So a spec only has to do the two interesting steps:
//   3. find   4. assert
//
// `$` and `expect` are globals injected by the WebdriverIO test-runner —
// no imports needed.

describe('Android Settings', () => {
  it('opens and shows the Settings home screen', async () => {
    // 3 — FIND: locate the Settings home screen by its container's resource-id.
    //     resource-id is the most stable locator — unlike the title text, it doesn't
    //     change across Android versions or device languages.
    const home = $('//*[@resource-id="com.android.settings:id/homepage_container"]')

    // 4 — ASSERT: the screen we expected is actually showing.
    //     expect-webdriverio auto-waits, so no manual waitForDisplayed needed.
    await expect(home).toBeDisplayed()
  })
})
