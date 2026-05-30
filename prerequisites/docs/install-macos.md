# 🍎 Install Guide — macOS

For macOS 13+ on Apple Silicon or Intel. We'll use [Homebrew](https://brew.sh) where possible.
Copy-paste each block. When you finish, run `bash scripts/doctor.sh` from the repo root.

> macOS users can automate **both Android and iOS**. iOS is optional for the bootcamp — do it if
> you have time. Android is required.

---

## 1. Homebrew

If you don't have it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then follow the on-screen instructions to add `brew` to your PATH (Apple Silicon puts it in
`/opt/homebrew/bin`).

## 2. Node.js 20 LTS + npm

```bash
brew install node@20
brew link --overwrite node@20
node -v   # expect v20.x or newer
npm -v
```

## 3. Python 3.10+ + pip

macOS ships Python, but install a clean one:

```bash
brew install python@3.12
python3 --version   # expect 3.10+
pip3 --version
```

## 4. JDK 17 (Temurin)

```bash
brew install --cask temurin@17
```

Set `JAVA_HOME` in your shell profile (`~/.zshrc` for the default zsh):

```bash
echo 'export JAVA_HOME="$(/usr/libexec/java_home -v 17)"' >> ~/.zshrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
java -version   # expect 17.x
echo $JAVA_HOME
```

## 5. Android Studio + SDK

```bash
brew install --cask android-studio
```

Open **Android Studio** once and complete the setup wizard (it downloads the SDK).
Then in **Settings → Languages & Frameworks → Android SDK → SDK Tools**, make sure these are checked:
**Android SDK Platform-Tools**, **Android SDK Command-line Tools (latest)**, **Android Emulator**.

Add the SDK to your shell profile:

```bash
echo 'export ANDROID_HOME="$HOME/Library/Android/sdk"' >> ~/.zshrc
echo 'export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
adb --version
```

Now **create an emulator** → follow [android-emulator.md](android-emulator.md).

## 6. Appium 2.x + uiautomator2 driver

```bash
npm install -g appium
appium -v                                  # expect 2.x
appium driver install uiautomator2
appium driver list --installed             # should list uiautomator2
```

Run the built-in environment check:

```bash
appium driver doctor uiautomator2
```

## 7. Appium Inspector

Download the latest `.dmg` from
<https://github.com/appium/appium-inspector/releases> and drag it to Applications.
(On first launch, if macOS blocks it: **System Settings → Privacy & Security → Open Anyway**.)

## 8. Claude Code CLI

See [claude-code.md](claude-code.md).

## 9. (Optional) iOS / Xcode

For iOS automation, see [ios-simulator.md](ios-simulator.md).

---

## ✅ Verify

```bash
bash scripts/doctor.sh
```

Then start your emulator and run the [smoke tests](../smoke/node/README.md).
Problems? → [troubleshooting.md](troubleshooting.md)
