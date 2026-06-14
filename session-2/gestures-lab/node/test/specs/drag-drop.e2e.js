// Session 2 · Gestures lab — DRAG & DROP (WebdriverIO + Mocha)
// ------------------------------------------------------------
// The "Drag & Drop Reorder" list reorders on drag. We drag "Drag Item 1" onto "Drag Item 4";
// afterwards Drag Item 4 sits at position 3 — its content-desc contains both "3" and
// "Drag Item 4". `mobile: dragGesture` presses-holds the source, moves to the target, drops.

import { loginAndOpenGestures, byDescContains, centre } from '../helpers/gestures.js'

const ITEM1 = byDescContains('Drag Item 1')
const ITEM4 = byDescContains('Drag Item 4')
const REORDERED = "//*[contains(@content-desc, '3') and contains(@content-desc, 'Drag Item 4')]"

describe('Drag & drop', () => {
  before(async () => { await loginAndOpenGestures() })

  it('drags Item 1 onto Item 4 and the list reorders', async () => {
    const src = await $(ITEM1)
    await src.waitForDisplayed({ timeout: 20000 })
    const target = await $(ITEM4)
    const drop = await centre(target)

    await driver.execute('mobile: dragGesture', {
      elementId: src.elementId,
      endX: drop.x, endY: drop.y,
      speed: 1200,
    })

    await expect($(REORDERED)).toBeDisplayed()    // Drag Item 4 moved to position 3
  })
})
