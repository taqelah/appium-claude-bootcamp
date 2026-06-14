// Session 2 · Gestures lab — PINCH in & out (WebdriverIO + Mocha)
// ---------------------------------------------------------------
// Scroll the "Pinch to Zoom" section into view, then zoom IN with two-finger spread
// (pinchOpen) and back OUT (pinchClose) on its image. `percent` is how far the fingers move.
// Pass = both gestures run and we stay on the screen.

import { loginAndOpenGestures, scrollToDesc } from '../helpers/gestures.js'

const IMAGE = "//*[@content-desc='Pinch to Zoom']/../android.view.View[15]"

describe('Pinch — in & out', () => {
  before(async () => { await loginAndOpenGestures() })

  it('pinches open (zoom in) then closed (zoom out)', async () => {
    await scrollToDesc('Pinch to Zoom')
    const image = await $(IMAGE)
    await image.waitForExist({ timeout: 20000 })
    const id = image.elementId

    await driver.execute('mobile: pinchOpenGesture', { elementId: id, percent: 0.75 })   // zoom in
    await driver.execute('mobile: pinchOpenGesture', { elementId: id, percent: 0.75 })
    await driver.execute('mobile: pinchCloseGesture', { elementId: id, percent: 0.75 })  // zoom out
    await driver.execute('mobile: pinchCloseGesture', { elementId: id, percent: 0.75 })

    await expect($('~Pinch to Zoom')).toBeDisplayed()   // still on the section
  })
})
