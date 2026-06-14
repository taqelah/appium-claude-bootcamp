// Shared helpers for the gestures lab.
// Every spec logs in, opens the nav drawer, and taps "Gestures" to reach the Gesture Demo
// screen (Swipe Cards · Drag & Drop · Long Press · Double Tap to Zoom · Pinch to Zoom).

const USERNAME = 'android=new UiSelector().className("android.widget.EditText").instance(0)'
const PASSWORD = 'android=new UiSelector().className("android.widget.EditText").instance(1)'

// Open the Gesture Demo screen from a fresh launch.
export async function loginAndOpenGestures(user = 'emma@demoapp.com', pass = '10203040') {
  const u = $(USERNAME)
  await u.waitForDisplayed({ timeout: 20000 })   // also waits past the splash
  await u.click(); await u.setValue(user)
  const p = $(PASSWORD)
  await p.click(); await p.setValue(pass)
  await $('~Login').click()

  await $('~View All').waitForDisplayed({ timeout: 20000 })   // home loaded
  await $('~Open navigation menu').click()
  await $('~Gestures').waitForDisplayed({ timeout: 20000 })
  await $('~Gestures').click()
  await $('~Swipe Card 1').waitForDisplayed({ timeout: 20000 })   // on the Gesture Demo screen
}

// Reliable vertical scroll: UiAutomator's UiScrollable scrolls the list natively until the
// element with the given content-desc is on screen (the interactive cards intercept raw
// swipe gestures, so we drive the scroller directly).
export function byDescContains(desc) {
  return `android=new UiSelector().descriptionContains(${JSON.stringify(desc)})`
}

export async function scrollToDesc(desc) {
  const sel =
    'android=new UiScrollable(new UiSelector().scrollable(true)).setAsVerticalList()' +
    `.scrollIntoView(new UiSelector().descriptionContains(${JSON.stringify(desc)}))`
  await $(sel)                       // scrolls FORWARD (down) until found
  return $(byDescContains(desc))
}

// Directional scroll with `mobile: scrollGesture`: flick along the right edge (clear of the
// cards' own gesture areas) in `direction` until the target content-desc is on screen.
export async function scrollUntil(desc, direction = 'down', maxSwipes = 12) {
  const { width, height } = await driver.getWindowSize()
  const area = {
    left: Math.round(width * 0.86), top: Math.round(height * 0.30),
    width: Math.round(width * 0.10), height: Math.round(height * 0.45),
  }
  const sel = byDescContains(desc)
  for (let i = 0; i < maxSwipes; i++) {
    if (await $(sel).isDisplayed().catch(() => false)) break
    await driver.execute('mobile: scrollGesture', { ...area, direction, percent: 1.0 })
  }
  return $(sel)
}

// Centre point of an element, for gestures that take an end coordinate (drag).
export async function centre(el) {
  const { x, y } = await el.getLocation()
  const { width, height } = await el.getSize()
  return { x: Math.round(x + width / 2), y: Math.round(y + height / 2) }
}
