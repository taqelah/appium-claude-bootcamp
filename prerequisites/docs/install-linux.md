# 🐧 Install Guide — Linux

Tested on Ubuntu/Debian 22.04+. For Fedora/Arch, swap `apt` for `dnf`/`pacman`.
When you finish, run `bash scripts/doctor.sh` from the repo root.

> Linux can automate **Android only** (no iOS — that needs macOS). Android is all you need.
>
> **Emulator + virtualization:** the Android emulator needs KVM. Confirm with
> `egrep -c '(vmx|svm)' /proc/cpuinfo` (should be > 0) and that your user is in the `kvm` group:
> `sudo adduser $USER kvm` (log out/in afterwards). On a cloud VM, enable nested virtualization
> or use a physical device instead.

---

## 1. Node.js 20 LTS + npm

Use [nodesource](https://github.com/nodesource/distributions) for a current LTS:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v   # expect v20.x+
npm -v
```

## 2. Python 3.10+ + pip

```bash
sudo apt install -y python3 python3-pip python3-venv
python3 --version   # expect 3.10+
pip3 --version
```

## 3. JDK 17

```bash
sudo apt install -y openjdk-17-jdk
java -version   # expect 17.x
```

Set `JAVA_HOME` in `~/.bashrc` (or `~/.zshrc`):

```bash
echo 'export JAVA_HOME="$(dirname $(dirname $(readlink -f $(which java))))"' >> ~/.bashrc
echo 'export PATH="$JAVA_HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
echo $JAVA_HOME
```

## 4. Android SDK + emulator

Easiest path: install **Android Studio** via snap, run it once to fetch the SDK:

```bash
sudo snap install android-studio --classic
```

(Or download command-line tools only from <https://developer.android.com/studio#command-tools>
and unzip into `~/Android/Sdk/cmdline-tools/latest`.)

Set env vars in `~/.bashrc`:

```bash
echo 'export ANDROID_HOME="$HOME/Android/Sdk"' >> ~/.bashrc
echo 'export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
adb --version
```

Now **create an emulator** → [android-emulator.md](android-emulator.md).

## 5. Appium 2.x + uiautomator2 driver

```bash
npm install -g appium
appium -v                          # expect 2.x
appium driver install uiautomator2
appium driver list --installed     # should list uiautomator2
appium driver doctor uiautomator2  # environment check
```

> If global npm install needs sudo, prefer fixing npm prefix to a user dir instead:
> `npm config set prefix ~/.npm-global` and add `~/.npm-global/bin` to PATH.

## 6. Appium Inspector

Download the latest `.AppImage` from
<https://github.com/appium/appium-inspector/releases>, then:

```bash
chmod +x Appium-Inspector-*.AppImage
./Appium-Inspector-*.AppImage
```

## 7. Claude Code CLI

See [claude-code.md](claude-code.md).

---

## ✅ Verify

```bash
bash scripts/doctor.sh
```

Then start your emulator and run the [smoke tests](../smoke/node/README.md).
Problems? → [troubleshooting.md](troubleshooting.md)
