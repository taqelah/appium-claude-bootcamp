# iOS capabilities — explained 🍎  *(optional, macOS only)*

> Skip this unless you're on a Mac with Xcode + the `xcuitest` driver installed
> (see [`../../../prerequisites/README.md` Step 8](../../../prerequisites/README.md#step-8--ios--xcode--optional-macos-only)).
> Android alone covers the course. This file is here so the iOS-curious can follow along.

The structure mirrors Android — only the **driver** and the **app identifiers** change.

```json
{
  "platformName": "iOS",
  "appium:automationName": "XCUITest",
  "appium:deviceName": "iPhone 15",
  "appium:platformVersion": "17.5",
  "appium:bundleId": "com.apple.Preferences",
  "appium:newCommandTimeout": 120
}
```

| Capability | What it means |
|------------|---------------|
| `platformName` | `iOS`. |
| `appium:automationName` | `XCUITest` — Apple's automation engine (the iOS counterpart to UiAutomator2). |
| `appium:deviceName` | The **simulator** name, exactly as in `xcrun simctl list devices` (e.g. `iPhone 15`). |
| `appium:platformVersion` | The iOS version of that simulator (e.g. `17.5`). iOS needs this; Android usually doesn't. |
| `appium:bundleId` | The app's bundle identifier. `com.apple.Preferences` is the built-in **Settings** app — the iOS analog of the Android example. |
| `appium:newCommandTimeout` | Same idea as Android: idle timeout in seconds. |

## How the first script changes for iOS

Only the **capabilities** and the **locator** differ — the five steps (connect → find → assert →
quit) and the client code stay the same. For the Settings title you'd typically locate by
**accessibility id**:

```python
from appium.options.ios import XCUITestOptions
# el = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Settings")
```

```js
// const el = await driver.$('~Settings')   // '~' = accessibility id in WebdriverIO
```

> 💡 This is the payoff of Appium: **one test, swap the capabilities, run on the other platform.**
> The element tree differs, so the *locators* differ — which is exactly what Session 2 is about.

## Other useful iOS capabilities

| Capability | Use it to… |
|------------|-----------|
| `appium:app` | Path to a built **.app** (simulator) or **.ipa** (real device) to install + launch. |
| `appium:udid` | Target a specific simulator/device. |
| `appium:noReset` / `appium:fullReset` | Same reset semantics as Android. |
