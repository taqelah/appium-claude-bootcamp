# 🍎 iOS Simulator Setup (macOS only — OPTIONAL)

iOS is **optional** for the bootcamp. Do this only if you're on a Mac and want to follow the
iOS examples. Everything required for the course works on Android alone.

---

## 1. Xcode

Install **Xcode** from the Mac App Store (it's large — several GB).
Then accept the license and install the command line tools:

```bash
sudo xcodebuild -license accept
xcode-select --install        # if not already installed
xcode-select -p               # should print a path like /Applications/Xcode.app/Contents/Developer
```

## 2. A simulator

Xcode bundles iOS simulators. List them:

```bash
xcrun simctl list devices
```

Boot one (example):

```bash
xcrun simctl boot "iPhone 15"
open -a Simulator
```

## 3. Appium xcuitest driver + dependencies

```bash
appium driver install xcuitest
appium driver list --installed     # should now include xcuitest
appium driver doctor xcuitest      # checks Xcode, carthage, etc.
```

The doctor may ask you to install extra tools:

```bash
brew install carthage
brew install ios-deploy        # for real devices (not needed for simulators)
```

---

## ✅ Verify

The repo's `scripts/doctor.sh` will report iOS items as **optional** — they won't fail the run.
There's no iOS smoke test in this prereq repo; we'll cover iOS live if there's interest.

Trouble? → [troubleshooting.md](troubleshooting.md)
