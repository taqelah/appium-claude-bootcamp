# 🪟 Install Guide — Windows

For Windows 10/11. We'll use [winget](https://learn.microsoft.com/windows/package-manager/winget/)
(built into modern Windows). [Chocolatey](https://chocolatey.org/install) alternatives are noted.
Run commands in **PowerShell** (some need an **Administrator** PowerShell — right-click → *Run as administrator*).

When you finish, run `powershell -ExecutionPolicy Bypass -File scripts/doctor.ps1` from the repo root.

> Windows can automate **Android only** (no iOS — that needs macOS). Android is all you need for the bootcamp.

---

## 1. Node.js 20 LTS + npm

```powershell
winget install OpenJS.NodeJS.LTS
# (Chocolatey alt: choco install nodejs-lts)
```

Close and reopen PowerShell, then:

```powershell
node -v   # expect v20.x or newer
npm -v
```

## 2. Python 3.10+ + pip

```powershell
winget install Python.Python.3.12
```

Reopen PowerShell:

```powershell
python --version   # expect 3.10+
pip --version
```

> If `python` opens the Microsoft Store, turn off the alias: **Settings → Apps → Advanced app
> settings → App execution aliases** → disable the `python.exe` App Installer entries.

## 3. JDK 17 (Temurin)

```powershell
winget install EclipseAdoptium.Temurin.17.JDK
```

Set `JAVA_HOME` (Admin PowerShell), then **reopen** PowerShell:

```powershell
# Adjust the path to your actual install dir (check C:\Program Files\Eclipse Adoptium\)
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-17.0.x-hotspot" /M
# Add to PATH:
setx PATH "$($env:PATH);%JAVA_HOME%\bin" /M
```

Reopen PowerShell:

```powershell
java -version   # expect 17.x
echo $env:JAVA_HOME
```

## 4. Android Studio + SDK

```powershell
winget install Google.AndroidStudio
```

Open **Android Studio** once and complete the setup wizard (downloads the SDK).
Then **Settings → Languages & Frameworks → Android SDK → SDK Tools**: check
**Android SDK Platform-Tools**, **Android SDK Command-line Tools (latest)**, **Android Emulator**.

Set the SDK env vars (Admin PowerShell). The SDK usually lives at
`C:\Users\<you>\AppData\Local\Android\Sdk`:

```powershell
setx ANDROID_HOME "$env:LOCALAPPDATA\Android\Sdk" /M
setx PATH "$($env:PATH);%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\emulator;%ANDROID_HOME%\cmdline-tools\latest\bin" /M
```

Reopen PowerShell:

```powershell
adb --version
```

Now **create an emulator** → [android-emulator.md](android-emulator.md).

> **Tip:** Enable hardware acceleration. On Intel, install
> [Intel HAXM](https://github.com/intel/haxm) or enable **Windows Hypervisor Platform**
> (Windows Features). The emulator is very slow without it.

## 5. Appium 2.x + uiautomator2 driver

```powershell
npm install -g appium
appium -v                          # expect 2.x
appium driver install uiautomator2
appium driver list --installed     # should list uiautomator2
appium driver doctor uiautomator2  # environment check
```

## 6. Appium Inspector

Download the latest `.exe` installer from
<https://github.com/appium/appium-inspector/releases>.

## 7. Claude Code CLI

See [claude-code.md](claude-code.md).

---

## ✅ Verify

```powershell
powershell -ExecutionPolicy Bypass -File scripts/doctor.ps1
```

Then start your emulator and run the [smoke tests](../smoke/node/README.md).
Problems? → [troubleshooting.md](troubleshooting.md)
