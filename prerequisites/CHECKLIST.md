# ✅ Pre-Bootcamp Checklist

Complete this **before Day 1 (June 7, 2026)**. Run the doctor script
(`bash scripts/doctor.sh` or `scripts/doctor.ps1`) — it checks most of this automatically.

## Core tools (everyone)

- [ ] **Node.js 20 LTS+** installed — `node -v`
- [ ] **npm** works — `npm -v`
- [ ] **Python 3.10+** installed — `python3 --version` (Windows: `python --version`)
- [ ] **pip** works — `pip --version` / `pip3 --version`
- [ ] **JDK 17** installed — `java -version`
- [ ] **`JAVA_HOME`** is set and points at the JDK
- [ ] **Android Studio** installed
- [ ] **`ANDROID_HOME`** (or `ANDROID_SDK_ROOT`) set, and `platform-tools` + `emulator` on `PATH`
- [ ] **`adb`** works — `adb --version`
- [ ] At least **one AVD created** — `emulator -list-avds` shows it
- [ ] Emulator **boots** and appears in `adb devices` as `device` (not `offline`)

## Appium

- [ ] **Appium 2.x** installed globally — `appium -v`
- [ ] **`uiautomator2`** driver installed — `appium driver list --installed`
- [ ] *(macOS, optional)* **`xcuitest`** driver installed
- [ ] **Appium Inspector** downloaded and opens

## Claude Code

- [ ] **Claude Code CLI** installed — `claude --version`
- [ ] Logged in / authenticated (we finish setup together on Day 2)

## Smoke tests (the real proof)

> Start your emulator, run `appium` in a separate terminal, then:

- [ ] **Node smoke** passes — `cd smoke/node && npm install && npm run smoke`
- [ ] **Python smoke** passes — `cd smoke/python && pytest -q`

## iOS (macOS only, optional)

- [ ] **Xcode** installed from the App Store
- [ ] **Command line tools** — `xcode-select -p` returns a path
- [ ] At least one **iOS Simulator** available — `xcrun simctl list devices`

---

When the doctor is all-green and both smoke tests pass, **you're ready**. 🎉
Trouble? → [docs/troubleshooting.md](docs/troubleshooting.md) or the cohort channel.
