# Gestures Lab — Scroll, Swipe, Drag, Pinch, Long-press & Double-tap 👆

Drive **six real gestures** against the demo app's **Gesture Demo** screen, with assertions
that prove each one worked. Every test logs in, opens the nav drawer, taps **Gestures**, then
performs its gesture using Appium's Android **`mobile:` gesture commands** (UiAutomator2).

> **The app:** [`taqelah/demo-app`](https://github.com/taqelah/demo-app/releases/tag/v1.0.0) —
> the same Flutter app from Session 1. Its **Gestures** screen (nav drawer → *Gestures*) has
> dedicated widgets: swipe-to-dismiss cards, a drag-to-reorder list, a long-press menu, and
> double-tap / pinch zoom areas.

```
gestures-lab/
├── node/        WebdriverIO + Mocha
│   └── test/
│       ├── helpers/gestures.js   login → drawer → Gestures; scroll helpers
│       └── specs/
│           ├── scroll.e2e.js          scroll down (UiScrollable) + up (scrollGesture)
│           ├── swipe.e2e.js           swipeGesture left/right → cards leave the list
│           ├── drag-drop.e2e.js       dragGesture Item 1 → Item 4 → list reorders
│           ├── long-press.e2e.js      longClickGesture → "Copy" menu appears
│           ├── double-tap.e2e.js      doubleClickGesture on the zoom image
│           └── pinch.e2e.js           pinchOpenGesture / pinchCloseGesture
└── python/      pytest
    ├── conftest.py          `gestures` fixture (login → Gestures) + scroll/centre helpers
    └── test_scroll.py · test_swipe.py · test_drag_drop.py
        test_long_press.py · test_double_tap.py · test_pinch.py
```

---

## 0 · Prerequisites

```bash
node -v                            # v26+
python3 --version                  # 3.10+   (Windows: python --version)
appium -v                          # 3.x
adb devices                        # your emulator, "device" not offline
```

## 1 · Get the app onto your emulator

```bash
# download DemoApp-v1.0.0.apk from:
#   https://github.com/taqelah/demo-app/releases/tag/v1.0.0
adb install -r DemoApp-v1.0.0.apk
```

Credentials: `emma@demoapp.com` / `10203040`.

---

## 2 · The six gestures & how they're driven

| Gesture | Appium `mobile:` command | What the test asserts |
|---------|--------------------------|-----------------------|
| **Scroll** up/down | `mobile: scrollGesture` + `UiScrollable.scrollIntoView` | bottom widget, then top widget, become visible |
| **Swipe** left/right | `mobile: swipeGesture` `{ elementId, direction, percent }` | swiped cards leave the list (**hidden**) |
| **Drag & drop** | `mobile: dragGesture` `{ elementId, endX, endY }` | list **reorders** (Item 4 → position 3) |
| **Long-press** | `mobile: longClickGesture` `{ elementId, duration }` | the **Copy** context menu appears |
| **Double-tap** | `mobile: doubleClickGesture` `{ elementId }` | fires on the zoom image; screen intact |
| **Pinch** in/out | `mobile: pinchOpenGesture` / `pinchCloseGesture` `{ elementId, percent }` | both run; screen intact |

> 💡 **Coordinates from size:** scrolls compute a right-edge band from `getWindowSize()` so the
> flick clears the cards' own gesture areas — the "compute from width/height" rule in action.

---

## 3 · Start the emulator + Appium server

```bash
emulator -avd Pixel_10_Pro_XL      # boot your AVD (use YOUR name); leave running
appium                             # in its own terminal — http://127.0.0.1:4723
```

## 4 · Run the lab

```bash
# 🟢 Node (WebdriverIO + Mocha) — runs all 6 specs
cd node
npm install        # first time only
npm test

# 🐍 Python (pytest) — runs all 6 tests
cd python
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

> 🎯 One gesture only? `pytest test_swipe.py` · or in Node
> `npx wdio run ./wdio.conf.js --spec ./test/specs/swipe.e2e.js`.

---

## 5 · Expected result ✅

```
# Node (WebdriverIO + Mocha)
 ✓ Scroll — up & down
 ✓ Swipe — left & right
 ✓ Drag & drop
 ✓ Long-press
 ✓ Double-tap
 ✓ Pinch — in & out
6 passing

# Python
==== 6 passed ====
```

---

## 🆘 Troubleshooting

| Symptom | Fix |
|---------|-----|
| `~Gestures` not found after login | Open the **nav drawer** first (`~Open navigation menu`); the Gestures item lives there. |
| Scroll never reaches Double-Tap / Pinch | Scrolling **down** past the swipe cards needs `UiScrollable.scrollIntoView` (raw swipes get eaten by the cards). Scrolling **up** uses `scrollGesture` on the right edge. |
| `mobile: …Gesture` "unknown command" | You're not on the **UiAutomator2** driver, or Appium 2/3 isn't current — `appium -v`, reinstall the driver. |
| Swipe/drag asserts fail | The app must be the **v1.0.0** build (its Gesture Demo screen has these widgets). |
| `ECONNREFUSED 127.0.0.1:4723` | Start `appium` in another terminal. |

Locators & flow mirror the taqwright Android demo; here they're written directly against
Appium so you can see exactly which `mobile:` command each gesture maps to.
