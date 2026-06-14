# Waits Lab — Implicit vs Explicit ⏳

Feel the difference between the two ways Appium **synchronizes** with an app. You'll drive the
**same login flow** twice — once with a single global **implicit** wait, once with per-step
**explicit** waits — and see why explicit is the tool you reach for.

> **The app:** [`taqelah/demo-app`](https://github.com/taqelah/demo-app/releases/tag/v1.0.0) — the
> same small **Flutter** e-commerce demo from Session 1. It shows a **splash screen** before the
> login form, so the first field takes a moment to appear. That delay is exactly what waits are for.

```
waits-lab/
├── node/        WebdriverIO + Mocha
│   └── test/specs/
│       ├── implicit.e2e.js     one global implicit timeout; plain finds retry past the splash
│       ├── explicit.e2e.js     per-step waitForDisplayed / waitForEnabled / waitUntil
│       └── fluent.e2e.js       explicit + a custom poll interval ({ interval: 500 })
└── python/      pytest
    ├── test_implicit_wait.py   driver.implicitly_wait(10); no WebDriverWait, no sleep
    ├── test_explicit_wait.py   implicitly_wait(0) + WebDriverWait + expected_conditions
    └── test_fluent_wait.py     WebDriverWait + poll_frequency + ignored_exceptions
```

---

## 0 · Prerequisites

Same stack as the Session 1 labs. Sanity check:

```bash
node -v                            # v26+
python3 --version                  # 3.10+   (Windows: python --version)
appium -v                          # 3.x
adb devices                        # your emulator, "device" not offline
```

---

## 1 · Get the app onto your emulator

```bash
# download DemoApp-v1.0.0.apk from:
#   https://github.com/taqelah/demo-app/releases/tag/v1.0.0
adb install -r DemoApp-v1.0.0.apk
```

**Demo credentials** (also shown on the app's login screen):

| | |
|---|---|
| Username | `emma@demoapp.com` |
| Password | `10203040` |

---

## 2 · The three waits, side by side

| | Implicit | Explicit | Fluent |
|---|----------|----------|--------|
| **Set** | once, globally | per step | per step (explicit + tuned) |
| **Waits for** | element to **exist** (presence) | a **specific condition** (displayed, enabled, custom…) | same — with a custom **poll interval** + **ignored exceptions** |
| **Python** | `driver.implicitly_wait(10)` | `WebDriverWait(driver, 15).until(EC…)` | `WebDriverWait(driver, 20, poll_frequency=0.5, ignored_exceptions=[…])` |
| **Node (WDIO)** | `driver.setTimeout({ implicit: 10000 })` | `await $(L).waitForDisplayed()` · `waitForEnabled()` | `await $(L).waitForDisplayed({ timeout, interval })` |
| **Verdict** | handy safety net | the default tool ✅ — precise, self-documenting | explicit, fine-tuned for chatty/stale cases |

> ❌ **Never `sleep(3)`** — too short → flaky, too long → slow. Wait for a **condition**, not a clock.

---

## 3 · Start the emulator + Appium server

```bash
emulator -avd Pixel_7_API_34       # boot your AVD (use YOUR name); leave running
appium                             # in its own terminal — http://127.0.0.1:4723
```

---

## 4 · Run the lab

```bash
# 🟢 Node (WebdriverIO + Mocha) — runs ALL THREE specs
cd node
npm install        # first time only
npm test           # runs: wdio run ./wdio.conf.js

# 🐍 Python (pytest) — runs ALL THREE tests
cd python
pip install -r requirements.txt    # first time only
pytest
```

> 🐳 **Devcontainer users:** the scripts already read `APPIUM_HOST` / `APPIUM_PORT`
> (pre-set to `host.docker.internal:4723`) — no code change needed.

> 🎯 Want just one? `pytest test_fluent_wait.py` · or in Node use
> `npx wdio run ./wdio.conf.js --spec ./test/specs/fluent.e2e.js`.

---

## 5 · Expected result ✅

All three styles log in past the splash and land on the home screen (`View All` asserted):

```
# Node (WebdriverIO + Mocha)
"spec" Reporter:
 ✓ Implicit wait finds the login fields past the splash with no explicit waits
 ✓ Explicit wait waits for a specific condition at each step
 ✓ Fluent wait waits with a custom poll interval at each step
3 passing

# Python
==== 3 passed ====
```

---

## 6 · Make it yours (see the difference)

- 🧪 In `test_implicit_wait.py`, change `implicitly_wait(10)` to `implicitly_wait(1)` — too short
  for the splash, so the find fails. **That's the lesson:** an implicit wait is a fixed global guess.
- 🧪 In `test_explicit_wait.py`, swap `element_to_be_clickable` for `presence_of_element_located`
  on the username field and watch it try to type before the field is ready — **conditions matter**.
- 🧪 In `test_fluent_wait.py`, raise `poll_frequency` to `2.0` (or Node `interval: 2000`) — the test
  still passes but reacts more slowly; lower it and it re-checks more often. That's the **fluent knob**.
- 🧪 Add a deliberate `time.sleep(5)` and notice the test gets **slower for no benefit** — then delete it.

---

## 🍎 iOS reference (optional macOS track)

Same flow on a **simulator** (macOS + Xcode only): `appium:automationName` **`XCUITest`**,
`appium:platformName` `iOS`, `appium:bundleId` `com.taqelah.demoApp`. The wait APIs are identical —
`implicitly_wait` / `WebDriverWait` (Python) and `setTimeout` / `waitFor*` (Node) are
**driver-agnostic**, so only the capabilities change.

---

## 🆘 Troubleshooting

| Symptom | Fix |
|---------|-----|
| `no such element` on the username field | The **splash** is still showing — increase the wait (implicit timeout, or the `WebDriverWait` ceiling). Confirm the `EditText` instances in Appium Inspector. |
| Implicit test fails but explicit passes | Your implicit timeout is **shorter than the splash**. Raise `implicitly_wait(...)`. |
| `waitForClickable is only available for desktop and mobile browsers` | It's browser-only — in a **native** app use `waitForDisplayed` / `waitForEnabled` instead. |
| Typed text doesn't appear | The field needs focus — both tests `click()` before typing; keep that order for Flutter inputs. |
| `ECONNREFUSED 127.0.0.1:4723` | The Appium server isn't running — start `appium` in another terminal. |
| Session won't start / app not found | `adb devices` must show your emulator as **`device`**, and the app must be installed (`adb install DemoApp-v1.0.0.apk`). |

More fixes in [`../../session-1/login-lab/README.md`](../../session-1/login-lab/README.md#-troubleshooting).
