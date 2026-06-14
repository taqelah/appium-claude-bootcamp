"""Session 2 · Waits lab — IMPLICIT wait (Python / Appium-Python-Client + pytest).

App: taqelah/demo-app (Flutter). It shows a SPLASH before the login form, so the first
field isn't there the instant the app launches.

THE IDEA: set ONE global implicit wait, then use PLAIN `find_element` calls. Each find
auto-RETRIES for up to that timeout before raising NoSuchElement — so the splash delay is
absorbed without any WebDriverWait and without `sleep`.

Prereqs (see ../README.md):
    1. An Android emulator is booted   ->  `adb devices` shows it as "device"
    2. The Appium server is running    ->  run `appium` in another terminal (port 4723)
    3. The demo app is installed        ->  `adb install DemoApp-v1.0.0.apk`

Run:   pip install -r requirements.txt   &&   pytest test_implicit_wait.py
"""

import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

APPIUM_HOST = os.environ.get("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = os.environ.get("APPIUM_PORT", "4723")
APPIUM_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"

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
SUCCESS = (AppiumBy.ACCESSIBILITY_ID, "View All")  # only on the home screen

USER = "emma@demoapp.com"
PASS = "10203040"


@pytest.fixture
def driver():
    options = UiAutomator2Options().load_capabilities(CAPABILITIES)
    drv = webdriver.Remote(APPIUM_URL, options=options)

    # ⏳ IMPLICIT WAIT — set ONCE. Every find_element now polls for up to 10s before
    #    raising NoSuchElement. This is the blunt, global safety net.
    drv.implicitly_wait(10)

    yield drv
    drv.quit()


def test_login_with_implicit_wait(driver):
    # Plain finds — no WebDriverWait, no sleep. The implicit wait retries through the
    # splash until the username field exists.
    username = driver.find_element(*USERNAME)
    username.click()
    username.send_keys(USER)

    password = driver.find_element(*PASSWORD)
    password.click()
    password.send_keys(PASS)

    driver.find_element(*LOGIN_BTN).click()

    # Still a plain find — the implicit wait covers the screen transition too.
    view_all = driver.find_element(*SUCCESS)
    assert view_all.is_displayed(), "Expected 'View All' on the home screen after login"
