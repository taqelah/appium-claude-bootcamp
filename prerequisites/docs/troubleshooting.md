# 🛠️ Troubleshooting

The fastest first step is almost always:

```bash
appium driver doctor uiautomator2
```

It diagnoses Java, Android SDK, and environment problems specifically for Android automation.
Below are the issues we see most often.

---

## `JAVA_HOME is not set` / wrong Java version

- Confirm: `java -version` shows **17.x** and `echo $JAVA_HOME` (macOS/Linux) or
  `echo $env:JAVA_HOME` (Windows) prints a path.
- macOS: `export JAVA_HOME="$(/usr/libexec/java_home -v 17)"`
- Windows: re-run the `setx JAVA_HOME ...` step, then **open a new terminal** (env changes don't
  apply to already-open shells).
- If you have multiple JDKs, make sure 17 is the one on `PATH`.

## `adb: command not found` / `ANDROID_HOME` not set

- `ANDROID_HOME` (or `ANDROID_SDK_ROOT`) must point at your SDK, and
  `$ANDROID_HOME/platform-tools` must be on `PATH`.
  - macOS: `~/Library/Android/sdk`
  - Windows: `%LOCALAPPDATA%\Android\Sdk`
  - Linux: `~/Android/Sdk`
- After editing your profile, run `source ~/.zshrc` / `source ~/.bashrc` or **open a new terminal**.

## Emulator shows `offline` or `unauthorized` in `adb devices`

- Wait — first boot can take 1–2 minutes. Check: `adb shell getprop sys.boot_completed` → `1`.
- Reset the adb connection:
  ```bash
  adb kill-server && adb start-server && adb devices
  ```
- Cold boot the AVD from Android Studio's Device Manager (▾ menu → **Cold Boot Now**).

## Emulator is extremely slow or won't start

- **Hardware acceleration** is the usual culprit:
  - Windows (Intel): enable **Windows Hypervisor Platform** in *Windows Features*, or install Intel HAXM.
  - Linux: ensure **KVM** is enabled and your user is in the `kvm` group.
  - Apple Silicon: use an **arm64-v8a** system image (not x86_64).
- Give the AVD more RAM in its advanced settings, and close other heavy apps.

## `appium: command not found`

- Reinstall globally: `npm install -g appium`, then reopen the terminal.
- If `npm -g` fails with permission errors on macOS/Linux, set a user prefix:
  `npm config set prefix ~/.npm-global` and add `~/.npm-global/bin` to `PATH`.

## `uiautomator2` driver not found

```bash
appium driver install uiautomator2
appium driver list --installed
```

## Smoke test: `ECONNREFUSED 127.0.0.1:4723`

The Appium server isn't running. Open a terminal and run:

```bash
appium
```

Leave it running, then run the smoke test in a **second** terminal.

## Smoke test: session creation fails / no devices

- Make sure the **emulator is booted** (`adb devices` shows `device`).
- Make sure `appium` is running (previous item).
- Re-run `appium driver doctor uiautomator2`.

## Python: `ModuleNotFoundError: appium` or `selenium`

You likely installed into the wrong interpreter. Use a virtual environment:

```bash
cd smoke/python
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## `claude: command not found`

- Reinstall: `npm install -g @anthropic-ai/claude-code`, reopen terminal.
- Confirm npm's global bin is on `PATH` (`npm bin -g` shows the dir).

---

Still stuck? Post in the **cohort channel** with:
1. Your OS, 2. the command you ran, 3. the full error text, 4. `appium driver doctor uiautomator2` output.
We'll get you sorted before Day 1.
