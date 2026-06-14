// Session 2 · Gestures lab — LONG-PRESS (WebdriverIO + Mocha)
// -----------------------------------------------------------
// Press-and-hold the "Long press me for options" card to open its context menu, then assert
// the "Copy" option appears. `mobile: longClickGesture` holds for `duration` ms.

import { loginAndOpenGestures, scrollToDesc } from '../helpers/gestures.js'

describe('Long-press', () => {
  before(async () => { await loginAndOpenGestures() })

  it('long-presses the card and opens the context menu', async () => {
    const card = await scrollToDesc('Long press me for options')
    await card.waitForDisplayed({ timeout: 20000 })

    await driver.execute('mobile: longClickGesture', { elementId: card.elementId, duration: 1200 })

    await expect($('~Copy')).toBeDisplayed()      // context menu opened
  })
})
