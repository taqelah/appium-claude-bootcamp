# Appium + Claude Bootcamp — Prerequisites (do this before Day 1)

Welcome! 👋 This **one document** gets your laptop ready for the
*AI-Assisted Mobile UI Test Automation using Claude* bootcamp
(4 Saturdays, starting **June 7, 2026**, 2–6 PM SGT).

Day 1 jumps straight into building tests, so please complete everything here **a few days early**.
Work through the steps **top to bottom** — each one shows the exact command for **your operating system**.

> ⏱️ **Time budget:** ~60–90 minutes, mostly downloads. Android Studio + the emulator image are
> several GB — start early on a good connection.
>
> 🆘 **Stuck?** Jump to [Troubleshooting](#troubleshooting) or post in the cohort channel.

---

## What you'll install

| Tool | Why | Required? |
|------|-----|-----------|
| **Node.js 20 LTS+** + npm | WebdriverIO labs + Appium server | ✅ Everyone |
| **Python 3.10+** + pip | Appium-Python-Client labs | ✅ Everyone |
| **JDK 17** (Temurin) | Android automation engine needs Java | ✅ Everyone |
| **Android Studio** → SDK + emulator + 1 AVD | The device we automate against | ✅ Everyone |
| **Appium 3.x** + `uiautomator2` driver | The automation server | ✅ Everyone |
| **Appium Inspector** | Inspect app elements visually | ✅ Everyone |
| **Xcode** + `xcuitest` driver | iOS automation | 🍎 macOS only, optional |

Install **both** client stacks (Node + WebdriverIO **and** Python) — the bootcamp uses both.

---

## Before you start

- **Pick your OS** and follow only the block labelled for it: **🍎 macOS** or **🪟 Windows**.
- **Which terminal?**
  - macOS → **Terminal** (zsh). Profile file: `~/.zshrc`.
  - Windows → **PowerShell**. For the env-var steps, use an **Administrator** PowerShell (right-click → *Run as administrator*).
- ⚠️ **After changing an environment variable (`JAVA_HOME`, `ANDROID_HOME`, PATH), open a NEW terminal** — changes don't apply to already-open windows.
- **Platforms:** Android is required for everyone and works on both OSes. iOS ([Step 8](#step-8--ios--xcode--optional-macos-only)) is optional and macOS-only.

---

## Step 1 — Node.js 20 LTS + npm

**🍎 macOS** (install [Homebrew](https://brew.sh) first if you don't have it):
```bash
brew install node@20
brew link --overwrite node@20
```

**🪟 Windows:** download the **LTS** installer (`.msi`) from <https://nodejs.org/en> and run it —
accept the defaults (this also installs npm and adds Node to your PATH). Then **open a new terminal**.

**Verify (both OSes):**
```bash
node -v   # expect v20.x or newer
npm -v
```

---

## Step 2 — Python 3.10+ + pip

**🍎 macOS:**
```bash
brew install python@3.12
```

**🪟 Windows:** download the latest **Python 3.x** installer from <https://www.python.org/downloads/windows/>
and run it. ⚠️ On the first screen, **tick "Add python.exe to PATH"** before clicking Install. Then **open a new terminal**.
> If `python` opens the Microsoft Store instead, disable the alias: **Settings → Apps → Advanced app
> settings → App execution aliases** → turn off the `python.exe` entries.

**Verify:**
```bash
python3 --version    # Windows: python --version   — expect 3.10+
pip3 --version       # Windows: pip --version
```

---

## Step 3 — JDK 17 (Temurin) + `JAVA_HOME`

**🍎 macOS:**
```bash
brew install --cask temurin@17
# Set JAVA_HOME permanently:
echo 'export JAVA_HOME="$(/usr/libexec/java_home -v 17)"' >> ~/.zshrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**🪟 Windows (Administrator PowerShell):**
```powershell
winget install EclipseAdoptium.Temurin.17.JDK
# Set JAVA_HOME — adjust the path to your actual install dir under C:\Program Files\Eclipse Adoptium\
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-17.0.x-hotspot" /M
setx PATH "$($env:PATH);%JAVA_HOME%\bin" /M
# Then open a NEW PowerShell window.
```

**Verify:**
```bash
java -version          # expect 17.x
echo $JAVA_HOME        # Windows: echo $env:JAVA_HOME
```

---

## Step 4 — Android Studio + SDK + `ANDROID_HOME`

**Install Android Studio:**

**🍎 macOS:** `brew install --cask android-studio`
**🪟 Windows:** `winget install Google.AndroidStudio`

**Then (both OSes):** open **Android Studio** once and finish the setup wizard (it downloads the SDK).
In **Settings → Languages & Frameworks → Android SDK → SDK Tools**, check:
**Android SDK Platform-Tools**, **Android SDK Command-line Tools (latest)**, **Android Emulator**.

**Set `ANDROID_HOME` + PATH:**

**🍎 macOS:**
```bash
echo 'export ANDROID_HOME="$HOME/Library/Android/sdk"' >> ~/.zshrc
echo 'export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**🪟 Windows (Administrator PowerShell):**
```powershell
setx ANDROID_HOME "$env:LOCALAPPDATA\Android\Sdk" /M
setx PATH "$($env:PATH);%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\emulator;%ANDROID_HOME%\cmdline-tools\latest\bin" /M
# Then open a NEW PowerShell window.
```

**Verify:**
```bash
adb --version
```

---

## Step 5 — Create an Android emulator (AVD)

Everyone needs **one working emulator**. We target **API 34 (Android 14)** or **API 35**. Use the GUI (easiest) or CLI.

### Option A — Android Studio GUI (recommended, both OSes)
1. Open **Android Studio** → **More Actions → Virtual Device Manager**.
2. **Create Device** → pick e.g. **Pixel 7** → **Next**.
3. Select a **system image**: **API 34** or **35**, prefer a **Google APIs** image (not "Google Play" —
   those are harder to automate). Click ⬇️ to download (a few GB) → **Next**.
4. Name it e.g. `Pixel_7_API_34` → **Finish** → press ▶️ to boot.

### Option B — Command line (both OSes)
```bash
sdkmanager --licenses
# Apple Silicon: use arm64-v8a. Intel/AMD: use x86_64.
sdkmanager "platform-tools" "emulator" "platforms;android-34" "system-images;android-34;google_apis;arm64-v8a"
echo "no" | avdmanager create avd -n Pixel_7_API_34 -k "system-images;android-34;google_apis;arm64-v8a" -d pixel_7
emulator -list-avds
emulator -avd Pixel_7_API_34
```

### ⚡ Hardware acceleration (or the emulator crawls)
- **🪟 Windows:** enable **Windows Hypervisor Platform** in *Windows Features*, or install
  [Intel HAXM](https://github.com/intel/haxm) on Intel CPUs.
- **🍎 macOS:** use an **arm64-v8a** image on Apple Silicon.

### Confirm it's alive
In a **new terminal** (leave the emulator running):
```bash
adb devices
```
You should see a line ending in `device` (not `offline`/`unauthorized`):
```
emulator-5554   device
```
> First boot takes 1–2 min. Confirm boot finished: `adb shell getprop sys.boot_completed` → `1`.

---

## Step 6 — Appium 3.x and the uiautomator2 driver

Same commands on **both OSes** (Appium is an npm package):
```bash
npm install -g appium@latest
appium -v                                  # expect 3.x
appium driver install uiautomator2
appium driver list --installed             # should list uiautomator2
appium driver doctor uiautomator2          # deep environment check — fix anything it flags
```
> macOS: if global npm install hits permission errors, set a user prefix instead of using
> sudo: `npm config set prefix ~/.npm-global` and add `~/.npm-global/bin` to PATH.

---

## Step 7 — Appium Inspector

Download the latest release for your OS from
<https://github.com/appium/appium-inspector/releases>:
- **🍎 macOS:** the `.dmg` (if blocked on first open: **System Settings → Privacy & Security → Open Anyway**).
- **🪟 Windows:** the `.exe` installer.

---

## Step 8 — iOS / Xcode  *(OPTIONAL, macOS only)*

Skip unless you're on a Mac and want to follow the iOS examples. Android alone covers the course.
```bash
# Install Xcode from the Mac App Store first, then:
sudo xcodebuild -license accept
xcode-select --install        # if not already installed
xcode-select -p               # prints a path like /Applications/Xcode.app/Contents/Developer

# Appium iOS driver:
appium driver install xcuitest
appium driver doctor xcuitest      # may ask for: brew install carthage
xcrun simctl list devices          # list available simulators
```

---

## Step 9 — Verify your setup

Run these final checks — everything above should already pass:

```bash
appium driver doctor uiautomator2   # confirms the Java + Android SDK wiring is correct
```

Then **start your emulator** (Step 5) and confirm it's connected:
```bash
adb devices                         # should list it as "device" (not offline/unauthorized)
```

Finally, walk the [checklist](#-pre-bootcamp-checklist) below — when every box is ticked, you're ready.
Anything off? See [Troubleshooting](#troubleshooting).

---

## ✅ Pre-bootcamp checklist

Tick these off before Day 1.

**Core tools (everyone)**
- [ ] Node.js 20 LTS+ — `node -v`
- [ ] npm — `npm -v`
- [ ] Python 3.10+ — `python3 --version` (Windows: `python --version`)
- [ ] pip — `pip3 --version` / `pip --version`
- [ ] JDK 17 — `java -version`
- [ ] `JAVA_HOME` set and valid
- [ ] Android Studio installed
- [ ] `ANDROID_HOME` set; `platform-tools` + `emulator` on PATH
- [ ] `adb` works — `adb --version`
- [ ] At least one AVD — `emulator -list-avds`
- [ ] Emulator boots and shows as `device` in `adb devices`

**Appium**
- [ ] Appium 3.x — `appium -v`
- [ ] `uiautomator2` driver — `appium driver list --installed`
- [ ] Appium Inspector opens
- [ ] *(macOS, optional)* `xcuitest` driver installed

**iOS (macOS only, optional)**
- [ ] Xcode installed; `xcode-select -p` returns a path
- [ ] A simulator available — `xcrun simctl list devices`

When every box is ticked, **you're ready**. 🎉

---

## Troubleshooting

**First, always try:** `appium driver doctor uiautomator2` — it diagnoses most Android/Java/SDK issues.

**`JAVA_HOME is not set` / wrong Java version**
- `java -version` must show **17.x**; `echo $JAVA_HOME` (Windows: `echo $env:JAVA_HOME`) must print a path.
- macOS: `export JAVA_HOME="$(/usr/libexec/java_home -v 17)"`. Windows: re-run the `setx JAVA_HOME` step and **open a new terminal**.

**`adb: command not found` / `ANDROID_HOME` not set**
- `ANDROID_HOME` (or `ANDROID_SDK_ROOT`) must point at your SDK and `…/platform-tools` must be on PATH.
  macOS `~/Library/Android/sdk` · Windows `%LOCALAPPDATA%\Android\Sdk`.
- After editing your profile, `source` it or open a new terminal.

**Emulator shows `offline` / `unauthorized`**
- Wait for boot (`adb shell getprop sys.boot_completed` → `1`).
- Reset adb: `adb kill-server && adb start-server && adb devices`.
- Cold Boot the AVD from Android Studio's Device Manager.

**Emulator very slow / won't start** — see the hardware-acceleration notes in [Step 5](#-hardware-acceleration-or-the-emulator-crawls).

**`appium: command not found`** — reinstall: `npm install -g appium`, reopen terminal. On macOS, if
global npm needs sudo, set `npm config set prefix ~/.npm-global` and add `~/.npm-global/bin` to PATH.

**`uiautomator2` driver not found** — `appium driver install uiautomator2`.

Still stuck? Post in the **cohort channel** with: your OS, the command you ran, the full error text,
and the output of `appium driver doctor uiautomator2`.

---

## Need help?

- Cohort channel (invite emailed after registration)
- 📧 contact@taqelah.sg

See you on Day 1! — Syam
