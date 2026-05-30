# 📱 Android Emulator (AVD) Setup

Everyone needs **one working Android emulator**. You can do this with the Android Studio GUI
(easiest) or the command line. Either works for the doctor + smoke tests.

We target **API 34 (Android 14)** or **API 35 (Android 15)** — pick whichever the Device Manager
offers you.

---

## Option A — Android Studio GUI (recommended)

1. Open **Android Studio**.
2. **More Actions → Virtual Device Manager** (or **Device Manager** icon in a project).
3. Click **Create Device**.
4. Pick a phone, e.g. **Pixel 7**. → **Next**
5. Select a **system image**: choose **API 34** or **35**. Click the ⬇️ to download it (a few GB),
   then **Next**.
6. Name it something simple like `Pixel_7_API_34`. → **Finish**.
7. Press ▶️ to boot it. Wait until you see the Android home screen.

> **Recommended image:** a **Google APIs** image (not "Google Play"). Play-enabled images are
> harder to automate because they're production-signed.

---

## Option B — Command line

```bash
# 1. Accept licenses
sdkmanager --licenses

# 2. Install platform-tools, emulator, and a system image (x86_64 on Intel; arm64-v8a on Apple Silicon)
sdkmanager "platform-tools" "emulator" "platforms;android-34" "system-images;android-34;google_apis;arm64-v8a"
#   On Intel/AMD use:  "system-images;android-34;google_apis;x86_64"

# 3. Create the AVD
echo "no" | avdmanager create avd -n Pixel_7_API_34 -k "system-images;android-34;google_apis;arm64-v8a" -d pixel_7

# 4. List and launch
emulator -list-avds
emulator -avd Pixel_7_API_34
```

---

## Confirm it's alive

In a **new terminal** (leave the emulator running):

```bash
adb devices
```

You should see something like:

```
List of devices attached
emulator-5554   device
```

✅ If it says `device` (not `offline` or `unauthorized`), you're good.
The doctor script checks for this automatically.

> **Boot tip:** an emulator can take 1–2 minutes on first boot. Wait for the full home screen
> before running tests. To confirm boot completed:
> `adb shell getprop sys.boot_completed` → returns `1`.

Trouble? → [troubleshooting.md](troubleshooting.md)
