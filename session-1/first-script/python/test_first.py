"""Session 1 — your first Appium test (Python / Appium-Python-Client + pytest).

Prereqs (see ../README.md):
    1. An Android emulator is booted   ->  `adb devices` shows it as "device"
    2. The Appium server is running    ->  run `appium` in another terminal (port 4723)

Run:   pip install -r requirements.txt   &&   pytest

What it does — the five steps every Appium test shares:
    1. capabilities  2. connect  3. find  4. assert  5. quit
"""

import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

# host.docker.internal when running inside the devcontainer; localhost otherwise.
APPIUM_HOST = os.environ.get("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = os.environ.get("APPIUM_PORT", "4723")
APPIUM_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"

# 1 — CAPABILITIES: the "order form" telling the server what to automate.
#     We open the always-present Android Settings app, so there's no APK to install.
#     (Full explanation: ../caps/android.md)
CAPABILITIES = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.android.settings",
    "appium:appActivity": ".Settings",
    "appium:newCommandTimeout": 120,
}


@pytest.fixture
def driver():
    """2 — CONNECT: start a session, and always QUIT it afterwards (step 5)."""
    options = UiAutomator2Options().load_capabilities(CAPABILITIES)
    drv = webdriver.Remote(APPIUM_URL, options=options)
    drv.implicitly_wait(10)  # wait up to 10s for elements to appear
    yield drv
    drv.quit()  # 5 — QUIT (runs even if the test fails)


def test_settings_opens(driver):
    # 3 — FIND: locate the Settings home screen by its container's resource-id.
    #     resource-id is the most stable locator — unlike the title text, it doesn't
    #     change across Android versions or device languages.
    home = driver.find_element(AppiumBy.ID, "com.android.settings:id/homepage_container")

    # 4 — ASSERT: the screen we expected is actually showing.
    assert home.is_displayed(), "Expected the Settings home screen to be visible"
