# Python smoke test (Appium-Python-Client)

Proves Appium-Python-Client can drive your Android emulator through Appium. No app/APK needed —
it connects, reads the device time and screen size, asserts they're valid, and quits.

## Run it

1. **Start an emulator** (see [Step 5 in the main guide](../../README.md#step-5--create-an-android-emulator-avd))
   and wait for the home screen. Confirm: `adb devices` shows a line ending in `device`.
2. **Start Appium** in a separate terminal and leave it running:
   ```bash
   appium
   ```
3. **Run the smoke test** here (use a virtual environment):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pytest -q -s
   ```
   (`-s` shows the printed device time.)

## Expected output

```
-> Connecting to Appium at 127.0.0.1:4723 ...
   device time : 2026-06-07T13:00:00+08:00
   screen size : 1080x2400

SMOKE TEST PASSED - Appium-Python-Client drove your emulator successfully.
1 passed in 6.2s
```

## If it fails

- `ConnectionRefusedError` / cannot connect → Appium isn't running. Run `appium` (step 2).
- Session/`no devices` errors → emulator isn't booted, or run `appium driver doctor uiautomator2`.
- `ModuleNotFoundError: appium` → activate the venv and re-run `pip install -r requirements.txt`.
- More help: [Troubleshooting in the main guide](../../README.md#troubleshooting)

> Override host/port if your Appium runs elsewhere:
> `APPIUM_HOST=127.0.0.1 APPIUM_PORT=4723 pytest -q -s`
