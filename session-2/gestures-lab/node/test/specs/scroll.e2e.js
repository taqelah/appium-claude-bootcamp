// Session 2 · Gestures lab — SCROLL up & down (WebdriverIO + Mocha)
// -----------------------------------------------------------------
// On the Gesture Demo screen, scroll DOWN to bring a bottom widget into view, then UP to the
// top. Two scroll tools, both useful:
//   • DOWN — `UiScrollable.scrollIntoView` drives the list's own scroller until found.
//   • UP   — `mobile: scrollGesture` flicks along the right edge (clear of the cards).

import { loginAndOpenGestures, scrollToDesc, scrollUntil } from '../helpers/gestures.js'

describe('Scroll — up & down', () => {
  before(async () => { await loginAndOpenGestures() })

  it('scrolls DOWN to the last section, then UP to the first', async () => {
    // SCROLL DOWN until "Pinch to Zoom" (near the bottom) is on screen.
    const pinch = await scrollToDesc('Pinch to Zoom')
    await expect(pinch).toBeDisplayed()

    // SCROLL UP until "Swipe Card 1" (the top) is on screen again.
    const top = await scrollUntil('Swipe Card 1', 'up')
    await expect(top).toBeDisplayed()
  })
})
