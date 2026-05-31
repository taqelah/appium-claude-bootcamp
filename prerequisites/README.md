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
| **Node.js 20 LTS+** + npm | WebdriverIO labs + Appium server + Claude Code | ✅ Everyone |
| **Python 3.10+** + pip | Appium-Python-Client labs | ✅ Everyone |
| **JDK 17** (Temurin) | Android automation engine needs Java | ✅ Everyone |
| **Android Studio** → SDK + emulator + 1 AVD | The device we automate against | ✅ Everyone |
| **Appium 2.x+** + `uiautomator2` driver | The automation server | ✅ Everyone |
| **Appium Inspector** | Inspect app elements visually | ✅ Everyone |
| **Claude Code CLI** | Our AI pair-programmer (deep dive on Day 2) | ✅ Everyone |
| **Xcode** + `xcuitest` driver | iOS automation | 🍎 macOS only, optional |

We verify **both** client stacks (Node + WebdriverIO **and** Python) because the bootcamp uses both.

---

## Before you start

- **Pick your OS** and follow only the block labelled for it: **🍎 macOS**, **🪟 Windows**, or **🐧 Linux**.
- **Which terminal?**
  - macOS → **Terminal** (zsh). Profile file: `~/.zshrc`.
  - Windows → **PowerShell**. For the env-var steps, use an **Administrator** PowerShell (right-click → *Run as administrator*).
  - Linux → your shell (bash/zsh). Profile file: `~/.bashrc` (or `~/.zshrc`).
- ⚠️ **After changing an environment variable (`JAVA_HOME`, `ANDROID_HOME`, PATH), open a NEW terminal** — changes don't apply to already-open windows.
- **Platforms:** Android is required for everyone and works on all three OSes. iOS ([Step 9](#step-9--ios--xcode--optional-macos-only)) is optional and macOS-only.

---

## Step 1 — Node.js 20 LTS + npm

**🍎 macOS** (install [Homebrew](https://brew.sh) first if you don't have it):
```bash
brew install node@20
brew link --overwrite node@20
```

**🪟 Windows:** download the **LTS** installer (`.msi`) from <https://nodejs.org/en> and run it —
accept the defaults (this also installs npm and adds Node to your PATH). Then **open a new terminal**.

**🐧 Linux (Debian/Ubuntu):**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

**Verify (all OSes):**
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

**🪟 Windows (PowerShell):**
```powershell
winget install Python.Python.3.12
```
> If `python` opens the Microsoft Store, disable the alias: **Settings → Apps → Advanced app
> settings → App execution aliases** → turn off the `python.exe` entries.

**🐧 Linux (Debian/Ubuntu):**
```bash
sudo apt install -y python3 python3-pip python3-venv
```

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

**🐧 Linux (Debian/Ubuntu):**
```bash
sudo apt install -y openjdk-17-jdk
echo 'export JAVA_HOME="$(dirname $(dirname $(readlink -f $(which java))))"' >> ~/.bashrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
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
**🐧 Linux:** `sudo snap install android-studio --classic`

**Then (all OSes):** open **Android Studio** once and finish the setup wizard (it downloads the SDK).
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

**🐧 Linux:**
```bash
echo 'export ANDROID_HOME="$HOME/Android/Sdk"' >> ~/.bashrc
echo 'export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Verify:**
```bash
adb --version
```

---

## Step 5 — Create an Android emulator (AVD)

Everyone needs **one working emulator**. We target **API 34 (Android 14)** or **API 35**. Use the GUI (easiest) or CLI.

### Option A — Android Studio GUI (recommended, all OSes)
1. Open **Android Studio** → **More Actions → Virtual Device Manager**.
2. **Create Device** → pick e.g. **Pixel 7** → **Next**.
3. Select a **system image**: **API 34** or **35**, prefer a **Google APIs** image (not "Google Play" —
   those are harder to automate). Click ⬇️ to download (a few GB) → **Next**.
4. Name it e.g. `Pixel_7_API_34` → **Finish** → press ▶️ to boot.

### Option B — Command line (all OSes)
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
- **🐧 Linux:** needs **KVM**. Check: `egrep -c '(vmx|svm)' /proc/cpuinfo` (>0), then
  `sudo adduser $USER kvm` and log out/in.
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

## Step 6 — Appium 2.x+ and the uiautomator2 driver

Same commands on **all OSes** (Appium is an npm package):
```bash
npm install -g appium
appium -v                                  # expect 2.x or 3.x
appium driver install uiautomator2
appium driver list --installed             # should list uiautomator2
appium driver doctor uiautomator2          # deep environment check — fix anything it flags
```
> Linux/macOS: if global npm install hits permission errors, set a user prefix instead of using
> sudo: `npm config set prefix ~/.npm-global` and add `~/.npm-global/bin` to PATH.

---

## Step 7 — Appium Inspector

Download the latest release for your OS from
<https://github.com/appium/appium-inspector/releases>:
- **🍎 macOS:** the `.dmg` (if blocked on first open: **System Settings → Privacy & Security → Open Anyway**).
- **🪟 Windows:** the `.exe` installer.
- **🐧 Linux:** the `.AppImage` → `chmod +x Appium-Inspector-*.AppImage && ./Appium-Inspector-*.AppImage`.

---

## Step 8 — Claude Code CLI

Our AI pair-programmer. **Install + sign in now**; we do the deep dive on **Day 2**. A free tier or
small amount of API credit is enough.

**Install (all OSes, via npm):**
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```
> Alternatives without npm — macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash` ·
> Windows: `irm https://claude.ai/install.ps1 | iex`. Docs: <https://docs.claude.com/en/docs/claude-code>

**Sign in** — run `claude` once and follow the prompt. Authenticate with either a **Claude account**
(Pro/Max) **or** an **Anthropic API key** — either is fine.

**Sanity check** — inside the session, type `what is 2 + 2?`. If it answers, you're connected. `/exit` to quit.

---

## Step 9 — iOS / Xcode  *(OPTIONAL, macOS only)*

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

## Step 10 — Verify your setup (doctor script)

The doctor checks every tool/version and prints a ✅/❌ table. It needs **no emulator or Appium running**.

**🍎 macOS / 🐧 Linux:**
```bash
bash scripts/doctor.sh
```

**🪟 Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\doctor.ps1
```

Keep fixing ❌ items (see [Troubleshooting](#troubleshooting)) and re-running until it prints **PASS**.

---

## Step 11 — Prove it works (smoke tests)

This is the real "my machine is ready" moment: a tiny test opens an Appium session on your emulator,
reads the device time, and quits. No app/APK needed. Run **both** stacks.

**Terminal A** — start your emulator (Step 5), then start the Appium server and leave it running:
```bash
appium
```

**Terminal B** — Node (WebdriverIO):
```bash
cd smoke/node
npm install
npm run smoke
```
Expected: `✅ SMOKE TEST PASSED — WebdriverIO drove your emulator successfully.`

**Terminal B** — Python (Appium-Python-Client):
```bash
cd smoke/python
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q -s
```
Expected: `SMOKE TEST PASSED - Appium-Python-Client drove your emulator successfully.` + `1 passed`.

> Override host/port if your Appium runs elsewhere — set `APPIUM_HOST` / `APPIUM_PORT` before the
> run command (defaults `127.0.0.1` / `4723`).

---

## ✅ Pre-bootcamp checklist

Tick these off — the doctor script (Step 10) covers most automatically.

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
- [ ] Appium 2.x+ — `appium -v`
- [ ] `uiautomator2` driver — `appium driver list --installed`
- [ ] Appium Inspector opens
- [ ] *(macOS, optional)* `xcuitest` driver installed

**Claude Code**
- [ ] `claude --version` works
- [ ] Logged in / authenticated

**Smoke tests (the real proof)**
- [ ] Node smoke passes — `cd smoke/node && npm install && npm run smoke`
- [ ] Python smoke passes — `cd smoke/python && pytest -q -s`

**iOS (macOS only, optional)**
- [ ] Xcode installed; `xcode-select -p` returns a path
- [ ] A simulator available — `xcrun simctl list devices`

When the doctor is all-green and both smoke tests pass, **you're ready**. 🎉

---

## Troubleshooting

**First, always try:** `appium driver doctor uiautomator2` — it diagnoses most Android/Java/SDK issues.

**`JAVA_HOME is not set` / wrong Java version**
- `java -version` must show **17.x**; `echo $JAVA_HOME` (Windows: `echo $env:JAVA_HOME`) must print a path.
- macOS: `export JAVA_HOME="$(/usr/libexec/java_home -v 17)"`. Windows: re-run the `setx JAVA_HOME` step and **open a new terminal**.

**`adb: command not found` / `ANDROID_HOME` not set**
- `ANDROID_HOME` (or `ANDROID_SDK_ROOT`) must point at your SDK and `…/platform-tools` must be on PATH.
  macOS `~/Library/Android/sdk` · Windows `%LOCALAPPDATA%\Android\Sdk` · Linux `~/Android/Sdk`.
- After editing your profile, `source` it or open a new terminal.

**Emulator shows `offline` / `unauthorized`**
- Wait for boot (`adb shell getprop sys.boot_completed` → `1`).
- Reset adb: `adb kill-server && adb start-server && adb devices`.
- Cold Boot the AVD from Android Studio's Device Manager.

**Emulator very slow / won't start** — see the hardware-acceleration notes in [Step 5](#-hardware-acceleration-or-the-emulator-crawls).

**`appium: command not found`** — reinstall: `npm install -g appium`, reopen terminal. If global npm
needs sudo on macOS/Linux, set `npm config set prefix ~/.npm-global` and add `~/.npm-global/bin` to PATH.

**`uiautomator2` driver not found** — `appium driver install uiautomator2`.

**Smoke test: `ECONNREFUSED 127.0.0.1:4723`** — the Appium server isn't running. Run `appium` in a
separate terminal (Step 11, Terminal A), then re-run the test.

**Smoke test: session fails / no devices** — make sure the emulator is booted (`adb devices` → `device`)
and `appium` is running; then `appium driver doctor uiautomator2`.

**Python: `ModuleNotFoundError: appium` / `selenium`** — you installed into the wrong interpreter.
Use the virtual environment: activate `.venv` and re-run `pip install -r requirements.txt`.

**`claude: command not found`** — reinstall `npm install -g @anthropic-ai/claude-code`, reopen terminal;
confirm npm's global bin (`npm bin -g`) is on PATH.

Still stuck? Post in the **cohort channel** with: your OS, the command you ran, the full error text,
and the output of `appium driver doctor uiautomator2`.

---

## Need help?

- Cohort channel (invite emailed after registration)
- 📧 contact@taqelah.sg

See you on Day 1! — Syam
