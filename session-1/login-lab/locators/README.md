# The login locators — and how to confirm them 🔍

This lab targets [`taqelah/demo-app`](https://github.com/taqelah/demo-app) — a **Flutter** app.
Flutter renders its own canvas, so the Android view tree has **no `resource-id`s**. That's a great
real-world lesson: when there's no id, you fall back to **UiAutomator class+instance** and
**accessibility id** (the visible labels Flutter exposes).

## The four locators (already wired into the lab)

| Element | Strategy | Value |
|---------|----------|-------|
| Username / email field | UiAutomator (`ANDROID_UIAUTOMATOR`) | `new UiSelector().className("android.widget.EditText").instance(0)` |
| Password field | UiAutomator | `new UiSelector().className("android.widget.EditText").instance(1)` |
| Login button | accessibility id (`content-desc`) | `Login` |
| Post-login element | accessibility id | `View All` *(home screen — we assert it, not tap it)* |

> The two text fields share the same class (`android.widget.EditText`), so we tell them apart by
> **`.instance(0)`** (first = username) and **`.instance(1)`** (second = password).

## Confirm them yourself in Appium Inspector

1. Start the Appium server: `appium` (listens on **4723**).
2. Open **Appium Inspector** → server `127.0.0.1`, port `4723`, **Remote Path** `/`.
3. Paste the demo-app capabilities → **Start Session**:
   ```json
   {
     "platformName": "Android",
     "appium:automationName": "UiAutomator2",
     "appium:appPackage": "com.taqelah.demo_app",
     "appium:appActivity": ".MainActivity"
   }
   ```
4. Wait past the splash, then click each field/button and read its attributes on the right —
   note there's **no resource-id**, only the class and the `content-desc` (accessibility id).

## How each locator looks in code

| Strategy | Platform | WebdriverIO (`$(...)`) | Python (`AppiumBy`) |
|----------|----------|------------------------|---------------------|
| accessibility id | both | `$('~Login')` | `(AppiumBy.ACCESSIBILITY_ID, "Login")` |
| id (resource-id) | both | `$('id=com.example:id/username')` | `(AppiumBy.ID, "com.example:id/username")` |
| class name | both | `$('android.widget.Button')` | `(AppiumBy.CLASS_NAME, "android.widget.Button")` |
| xpath | both | `$('//android.widget.EditText[@text="Email"]')` | `(AppiumBy.XPATH, '//android.widget.EditText[@text="Email"]')` |
| UiAutomator (`UiSelector`) | 🤖 Android | `$('android=new UiSelector().className("android.widget.EditText").instance(0)')` | `(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')` |
| -ios predicate string | 🍎 iOS | `$("-ios predicate string:type == 'XCUIElementTypeButton' AND name == 'login'")` | `(AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeButton' AND name == 'login'")` |
| -ios class chain | 🍎 iOS | ``$('-ios class chain:**/XCUIElementTypeButton[`name == "login"`]')`` | ``(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "login"`]')`` |

> This lab runs on **Android** (uiautomator2). The iOS rows are reference for the optional iOS track.
