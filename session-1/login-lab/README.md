# Lab 2 — Automate a Login Flow 🔐

Take everything from Part 2 — **locators**, **core commands** (`tap` / `sendKeys` / `getText`),
and **waits** — and drive a real **login** end-to-end: type a username + password, tap **Login**,
and assert you landed on the home screen.

> **The app:** [`taqelah/demo-app`](https://github.com/taqelah/demo-app/releases/tag/v1.0.0) — a small
> **Flutter** e-commerce demo built for automation practice.
> Because it's Flutter, the UI has **no `resource-id`s**, so we locate the text fields by
> **UiAutomator class + instance** and the buttons by **accessibility id** — exactly the
> "prefer accessibility / when there's no id" lesson from the lecture.

```
login-lab/
├── node/        WebdriverIO + Mocha   (wdio.conf.js, test/specs/login.e2e.js, package.json)
├── python/      pytest version        (test_login.py, requirements.txt)
└── locators/    the locators, explained + how to confirm them in Appium Inspector (README.md)
```

---

## 0 · Prerequisites

Same stack as Lab 1. Sanity check:

```bash
node -v                            # v26+
python3 --version                  # 3.10+   (Windows: python --version)
appium -v                          # 3.x
adb devices                        # your emulator, "device" not offline
```

---

## 1 · Get the app onto your emulator

Download the APK from the release and install it:

```bash
# download DemoApp-v1.0.0.apk from:
#   https://github.com/taqelah/demo-app/releases/tag/v1.0.0
adb install -r DemoApp-v1.0.0.apk
```

> 💡 Prefer zero manual steps? Skip `adb install` and let Appium fetch it — set
> `'appium:app'` to the release URL in `wdio.conf.js` / `test_login.py` (commented example included).

**Demo credentials** (also shown on the app's login screen):

| | |
|---|---|
| Username | `emma@demoapp.com` |
| Password | `10203040` |

---

## 2 · The locators

Already wired in (see [`locators/README.md`](locators/README.md) to confirm them yourself in Inspector):

| Element | Strategy | Value |
|---------|----------|-------|
| Username field | UiAutomator | `new UiSelector().className("android.widget.EditText").instance(0)` |
| Password field | UiAutomator | `new UiSelector().className("android.widget.EditText").instance(1)` |
| Login button | accessibility id | `Login` |
| Post-login element | accessibility id | `View All` *(asserted, not tapped)* |

---

## 3 · Start the emulator + Appium server

```bash
emulator -avd Pixel_7_API_34       # boot your AVD (use YOUR name); leave running
appium                             # in its own terminal — http://127.0.0.1:4723
```

---

## 4 · Run the test

```bash
# 🟢 Node (WebdriverIO + Mocha)
cd node
npm install        # first time only
npm test           # runs: wdio run ./wdio.conf.js

# 🐍 Python (pytest)
cd python
pip install -r requirements.txt    # first time only
pytest
```

> 🐳 **Devcontainer users:** the scripts already read `APPIUM_HOST` / `APPIUM_PORT`
> (pre-set to `host.docker.internal:4723`) — no code change needed.

---

## 5 · Expected result ✅

The emulator types the credentials, taps **Login**, lands on the home screen, and the **View All**
button is asserted visible:

```
# Node (WebdriverIO + Mocha)
"spec" Reporter:
 ✓ Login flow logs in with valid credentials
1 passing (5.0s)

# Python
==== 1 passed in 8.1s ====
```

🎉 **That's a real, multi-step UI test** — find, tap, type, wait, assert — in two languages.

---

## 🍎 iOS reference (optional macOS track)

The release also ships an iOS build, `DemoApp-v1.0.0-ios.app.zip`. To run the same flow on a
**simulator** (macOS + Xcode only):

- `appium:automationName`: **`XCUITest`**, `appium:platformName`: `iOS`
- `appium:bundleId`: `com.taqelah.demoApp` (or `appium:app`: path to the unzipped `.app`)
- Same visible labels (`Username` / `Password` / `Login`) and credentials. On iOS, prefer
  **`-ios predicate string`** / **`-ios class chain`** over xpath (see the locator slides).

---

## 🆘 Troubleshooting

| Symptom | Fix |
|---------|-----|
| `no such element` for a field | The login screen may still be on the **splash** — the test waits, but if it's slow, increase the wait. Confirm the EditText instances in Appium Inspector. |
| Typed text doesn't appear | The field needs focus — the test `click()`s it before typing; keep that order for Flutter inputs. |
| Test passes before login finishes | Assert on **`View All`** (home screen) with a wait, never `sleep`. |
| `ECONNREFUSED 127.0.0.1:4723` | The Appium server isn't running — start `appium` in another terminal. |
| Session won't start / app not found | `adb devices` must show your emulator as **`device`**, and the app must be installed (`adb install DemoApp-v1.0.0.apk`). |

More fixes in [`../first-script/README.md`](../first-script/README.md#-troubleshooting) and the
prerequisites Troubleshooting section.
