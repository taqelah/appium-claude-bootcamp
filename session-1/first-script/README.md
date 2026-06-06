# Lab — Your First Appium Script 🧪

Run a tiny, **guaranteed-green** Appium test against your Android emulator — in **both**
WebdriverIO + Mocha (Node) and Appium-Python-Client (Python). It automates the built-in **Settings**
app, so there's no APK to download.

> Every test you'll write does the same **five steps**:
> **1. capabilities → 2. connect → 3. find → 4. assert → 5. quit.**
> Today you just watch them work.

```
first-script/
├── node/        WebdriverIO + Mocha   (wdio.conf.js, test/specs/first.e2e.js, package.json)
├── python/      pytest version        (test_first.py, requirements.txt)
└── caps/        the capabilities, explained (android.md, ios.md)
```

---

## 0 · Prerequisites (one-time)

You should have finished [`../../prerequisites/README.md`](../../prerequisites/README.md). Sanity check:

```bash
node -v                            # v26+
python3 --version                  # 3.10+   (Windows: python --version)
appium -v                          # 3.x
appium driver doctor uiautomator2  # all green
```

---

## 1 · Start the emulator

```bash
emulator -list-avds                # find your AVD name
emulator -avd Pixel_7_API_34       # boot it (use YOUR name)
```

In another terminal, confirm it's ready (leave the emulator running):

```bash
adb devices                        # emulator-5554   device   ← must say "device"
adb shell getprop sys.boot_completed   # → 1 when fully booted
```

---

## 2 · Start the Appium server

In its **own** terminal (leave it running for the whole lab):

```bash
appium                             # listens on http://127.0.0.1:4723
```

You'll see `Appium REST http interface listener started on http://0.0.0.0:4723`.

---

## 3 · Run the test

Open a **third** terminal. Pick either stack — or do both!

### 🟢 Node (WebdriverIO + Mocha)

```bash
cd node
npm install        # first time only — pulls the WebdriverIO test-runner + Mocha
npm test           # runs: wdio run ./wdio.conf.js
```

### 🐍 Python (pytest)

```bash
cd python
pip install -r requirements.txt    # first time only
pytest
```

> 🐳 **Devcontainer users:** the client code runs in the container; the emulator + `appium` stay on
> your **host**. The scripts already read `APPIUM_HOST` / `APPIUM_PORT` (pre-set to
> `host.docker.internal:4723`), so no code change is needed. See
> [`../../.devcontainer/README.md`](../../.devcontainer/README.md).

---

## 4 · Expected result ✅

- The **emulator** opens the **Settings** app for a moment, then the session closes.
- Your terminal shows a **pass**:

```
# Node (WebdriverIO + Mocha)
"spec" Reporter:
 ✓ Android Settings opens and shows the Settings title
1 passing (3.4s)

# Python
==== 1 passed in 6.42s ====
```

🎉 **That's a passing mobile UI test.** Same five steps, two languages, one Appium server.

---

## 5 · Make it yours (homework)

1. Open **[`caps/android.md`](caps/android.md)** and read what each capability does.
2. Change `appPackage` / `appActivity` to open a **different** app (e.g. the Calculator — example in
   that file) and rerun.
3. Open **Appium Inspector** on the Settings app and find the **Settings** title yourself — note its
   `xpath` / `id` / `accessibility id`. (Locators are Session 2.)

---

## 🆘 Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ECONNREFUSED 127.0.0.1:4723` | The Appium server isn't running. Start `appium` in another terminal (Step 2). |
| `Could not find a connected Android device` / session won't start | `adb devices` must list your emulator as **`device`** (not `offline`/`unauthorized`). Wait for boot; `adb kill-server && adb start-server`. |
| `appium: command not found` | Reopen your terminal. Reinstall: `npm install -g appium`. (macOS perms: `npm config set prefix ~/.npm-global` + add to PATH.) |
| `The 'uiautomator2' driver is not installed` | `appium driver install uiautomator2`. |
| Settings opens but the **assert fails** | Your AVD's locale/version may label the title differently. Open Appium Inspector, read the **actual** title text, and update the locator. |
| Node `npm install` errors | Ensure Node 26+ (`node -v`); delete `node_modules` and retry. |
| Python `ModuleNotFoundError: appium` | You installed into the wrong environment. Re-run `pip install -r requirements.txt` in the interpreter `pytest` uses (consider a `venv`). |

Still stuck? First run `appium driver doctor uiautomator2`, then post in the **cohort channel** with
your OS, the command, and the **full** error text. More fixes in
[`../../prerequisites/README.md#troubleshooting`](../../prerequisites/README.md#troubleshooting).
