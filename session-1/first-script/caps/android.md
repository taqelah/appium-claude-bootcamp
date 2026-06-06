# Android capabilities — explained 🤖

The **capabilities** are the JSON "order form" your test sends to the Appium server when it starts a
session. They tell the server *what* to automate and *how*. Same object in Node and Python.

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:appPackage": "com.android.settings",
  "appium:appActivity": ".Settings",
  "appium:newCommandTimeout": 120
}
```

| Capability | What it means |
|------------|---------------|
| `platformName` | The OS family — `Android`. One of the two standard, non-prefixed W3C caps. |
| `appium:automationName` | The **driver** that does the work. `UiAutomator2` is the modern Android engine you installed in prerequisites. |
| `appium:appPackage` | The app's package id. `com.android.settings` is the built-in Settings app — **on every emulator**, nothing to install. |
| `appium:appActivity` | The screen (Activity) to launch. `.Settings` is the Settings home screen. |
| `appium:newCommandTimeout` | Seconds the server waits for your next command before auto-ending the session. 120 gives you breathing room while teaching. |

> 📝 **Why the `appium:` prefix?** Under the W3C WebDriver standard, only a few capability names are
> "standard" (like `platformName`). Everything vendor-specific must be prefixed — hence `appium:…`.

## Other useful Android capabilities (you'll meet these later)

| Capability | Use it to… |
|------------|-----------|
| `appium:app` | Install + launch an **APK** by path/URL (instead of `appPackage`/`appActivity`). |
| `appium:deviceName` | A human label, e.g. `Pixel_7_API_34` (informational for the emulator). |
| `appium:udid` | Target a **specific** device when several are connected (`adb devices`). |
| `appium:noReset` | `true` = don't clear app data/state between sessions. |
| `appium:fullReset` | `true` = uninstall + reinstall for a clean slate. |

## Try it yourself (homework)

Open a **different** built-in app by swapping two lines — e.g. the Calculator:

```json
"appium:appPackage": "com.google.android.calculator",
"appium:appActivity": "com.android.calculator2.Calculator"
```

> Not sure of an app's package/activity? With the app open on the emulator, run:
> `adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'`
