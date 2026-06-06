"""Session 1 · Lab 2 — automate a login flow (Python / Appium-Python-Client + pytest).

App: taqelah/demo-app (Flutter). The fixture handles capabilities + connect + quit.
The test does the Part 2 steps:  FIND -> tap -> send_keys -> tap -> ASSERT, with an EXPLICIT wait.

📝 It's a Flutter app, so there are NO resource-ids. We locate the two text fields by
   UiAutomator class + instance, and the buttons by accessibility id. (We tap each field
   before typing — Flutter inputs need focus first.)

Prereqs (see ../README.md):
    1. An Android emulator is booted   ->  `adb devices` shows it as "device"
    2. The Appium server is running    ->  run `appium` in another terminal (port 4723)
    3. The demo app is installed        ->  `adb install DemoApp-v1.0.0.apk`

Run:   pip install -r requirements.txt   &&   pytest
"""

import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# host.docker.internal when running inside the devcontainer; localhost otherwise.
APPIUM_HOST = os.environ.get("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = os.environ.get("APPIUM_PORT", "4723")
APPIUM_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"

# 1 — CAPABILITIES: launch the taqelah demo-app (install it first — see ../README.md).
CAPABILITIES = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.taqelah.demo_app",
    "appium:appActivity": ".MainActivity",
    "appium:newCommandTimeout": 120,
}

# Flutter app → no resource-ids. Fields by UiAutomator class+instance; buttons by accessibility id.
USERNAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
LOGIN_BTN = (AppiumBy.ACCESSIBILITY_ID, "Login")
SUCCESS = (AppiumBy.ACCESSIBILITY_ID, "View All")  # only on the home screen — assert, don't tap

USER = "emma@demoapp.com"
PASS = "10203040"


@pytest.fixture
def driver():
    """Connect, and always quit afterwards (even if the test fails)."""
    options = UiAutomator2Options().load_capabilities(CAPABILITIES)
    drv = webdriver.Remote(APPIUM_URL, options=options)
    yield drv
    drv.quit()


def test_login_succeeds(driver):
    wait = WebDriverWait(driver, 15)  # EXPLICIT wait — also covers the splash screen

    # FIND + TYPE (tap to focus first — Flutter inputs need it).
    username = wait.until(EC.presence_of_element_located(USERNAME))
    username.click()
    username.send_keys(USER)

    password = driver.find_element(*PASSWORD)
    password.click()
    password.send_keys(PASS)

    # TAP — submit.
    driver.find_element(*LOGIN_BTN).click()

    # ASSERT — "View All" only appears on the home screen, so it proves login succeeded.
    view_all = wait.until(EC.visibility_of_element_located(SUCCESS))
    assert view_all.is_displayed(), "Expected 'View All' on the home screen after login"
