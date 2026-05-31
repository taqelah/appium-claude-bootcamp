# Node smoke test (WebdriverIO)

Proves WebdriverIO can drive your Android emulator through Appium. No app/APK needed — it
connects, reads the device time and screen size, and quits.

## Run it

1. **Start an emulator** (see [Step 5 in the main guide](../../README.md#step-5--create-an-android-emulator-avd))
   and wait for the home screen. Confirm: `adb devices` shows a line ending in `device`.
2. **Start Appium** in a separate terminal and leave it running:
   ```bash
   appium
   ```
3. **Run the smoke test** here:
   ```bash
   npm install
   npm run smoke
   ```

## Expected output

```
→ Connecting to Appium at 127.0.0.1:4723 ...
  device time : 2026-06-07T13:00:00+08:00
  screen size : 1080x2400

✅ SMOKE TEST PASSED — WebdriverIO drove your emulator successfully.
```

## If it fails

- `ECONNREFUSED ... 4723` → Appium isn't running. Run `appium` (step 2).
- Session/`no devices` errors → emulator isn't booted, or run `appium driver doctor uiautomator2`.
- More help: [Troubleshooting in the main guide](../../README.md#troubleshooting)

> Override host/port if your Appium runs elsewhere:
> `APPIUM_HOST=127.0.0.1 APPIUM_PORT=4723 npm run smoke`
