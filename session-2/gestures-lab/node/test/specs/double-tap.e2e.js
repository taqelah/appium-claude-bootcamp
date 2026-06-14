// Session 2 · Gestures lab — DOUBLE-TAP to zoom (WebdriverIO + Mocha)
// -------------------------------------------------------------------
// Scroll the "Double Tap to Zoom" section into view, then double-tap its image to zoom.
// The image is a child view of the section (xpath sibling index, same as the taqwright demo).
// `mobile: doubleClickGesture` fires two quick taps; pass = it runs and we stay on the screen.

import { loginAndOpenGestures, scrollToDesc } from '../helpers/gestures.js'

const IMAGE = "//*[@content-desc='Double Tap to Zoom']/../android.view.View[11]"

describe('Double-tap', () => {
  before(async () => { await loginAndOpenGestures() })

  it('double-taps the image to zoom', async () => {
    await scrollToDesc('Double Tap to Zoom')
    const image = await $(IMAGE)
    await image.waitForExist({ timeout: 20000 })

    await driver.execute('mobile: doubleClickGesture', { elementId: image.elementId })

    await expect($('~Double Tap to Zoom')).toBeDisplayed()   // still on the section
  })
})
