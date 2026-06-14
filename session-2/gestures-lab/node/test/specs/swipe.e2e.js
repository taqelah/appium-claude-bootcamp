// Session 2 · Gestures lab — SWIPE left & right (WebdriverIO + Mocha)
// -------------------------------------------------------------------
// The "Swipe Cards" are dismissible: swipe a card LEFT to delete, RIGHT to favourite —
// either way it leaves the list. We swipe Card 1 left and Card 5 right, then assert both
// are gone (hidden). `mobile: swipeGesture` drives the gesture over each card element.

import { loginAndOpenGestures } from '../helpers/gestures.js'

const CARD1 = '~Swipe Card 1'
const CARD5 = '~Swipe Card 5'

describe('Swipe — left & right', () => {
  before(async () => { await loginAndOpenGestures() })

  it('swipes Card 1 left and Card 5 right; both leave the list', async () => {
    const card1 = await $(CARD1)
    await card1.waitForDisplayed({ timeout: 20000 })
    await driver.execute('mobile: swipeGesture', { elementId: card1.elementId, direction: 'left', percent: 0.9 })

    const card5 = await $(CARD5)
    await card5.waitForDisplayed({ timeout: 20000 })
    await driver.execute('mobile: swipeGesture', { elementId: card5.elementId, direction: 'right', percent: 0.9 })

    await expect($(CARD1)).not.toBeDisplayed()    // deleted
    await expect($(CARD5)).not.toBeDisplayed()    // favourited away
  })
})
