"""Prerequisite smoke test (Python + Appium-Python-Client).

Proves the full chain works: Appium-Python-Client -> Appium server -> uiautomator2 -> emulator.
It opens a session with NO app, reads the device time, then quits. No APK needed.

Before running:
    1. Start an Android emulator (see docs/android-emulator.md); wait for the home screen.
    2. In a separate terminal, run:  appium
    3. Here:
         python3 -m venv .venv
         source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
         pip install -r requirements.txt
         pytest -q

Expected: the test passes and prints your device's time.
"""

import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

APPIUM_HOST = os.environ.get("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = os.environ.get("APPIUM_PORT", "4723")
APPIUM_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"


@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    # No app/app_package: we just connect to whatever is on the emulator.
    options.new_command_timeout = 120

    print(f"\n-> Connecting to Appium at {APPIUM_URL} ...")
    try:
        drv = webdriver.Remote(APPIUM_URL, options=options)
    except Exception as err:  # noqa: BLE001 - we want a friendly message
        pytest.fail(
            f"Could not start an Appium session: {err}\n"
            "Checklist:\n"
            "  - Is an emulator running?   adb devices  (should show 'device')\n"
            "  - Is Appium running?        appium       (in another terminal)\n"
            "  - Driver installed?         appium driver list --installed\n"
            "  - Deep diagnostics:         appium driver doctor uiautomator2"
        )
    yield drv
    drv.quit()


def test_session_can_drive_emulator(driver):
    """A session can be created and basic device queries succeed."""
    device_time = driver.get_device_time()
    size = driver.get_window_size()

    print(f"   device time : {device_time}")
    print(f"   screen size : {size['width']}x{size['height']}")

    assert device_time, "expected a non-empty device time"
    assert size["width"] > 0 and size["height"] > 0
    print("\nSMOKE TEST PASSED - Appium-Python-Client drove your emulator successfully.")
