"""Session 2 · Waits lab — EXPLICIT wait (Python / Appium-Python-Client + pytest).

App: taqelah/demo-app (Flutter), same SPLASH-then-login flow as the implicit test.

THE IDEA: turn the implicit wait OFF, then wait for a SPECIFIC condition at each step with
WebDriverWait + expected_conditions (EC). An explicit wait returns the INSTANT the condition
is true — never longer than it has to — and names exactly what it's waiting for.

    EC.element_to_be_clickable     -> field is visible AND enabled (ready to tap/type)
    EC.visibility_of_element_located -> element is on screen
    (see the slides for the full toolbox: presence / visibility / clickable / invisibility / text_*)

Prereqs (see ../README.md):
    1. An Android emulator is booted   ->  `adb devices` shows it as "device"
    2. The Appium server is running    ->  run `appium` in another terminal (port 4723)
    3. The demo app is installed        ->  `adb install DemoApp-v1.0.0.apk`

Run:   pip install -r requirements.txt   &&   pytest test_explicit_wait.py
"""

import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    # Turn the implicit wait OFF so the explicit waits below are the ONLY thing syncing us.
    drv.implicitly_wait(0)

    yield drv
    drv.quit()


def test_login_with_explicit_wait(driver):
    wait = WebDriverWait(driver, 15)  # one reusable waiter, 15s ceiling

    # WAIT FOR CLICKABLE — the username field only becomes clickable after the splash.
    username = wait.until(EC.element_to_be_clickable(USERNAME))
    username.click()
    username.send_keys(USER)

    password = wait.until(EC.element_to_be_clickable(PASSWORD))
    password.click()
    password.send_keys(PASS)

    wait.until(EC.element_to_be_clickable(LOGIN_BTN)).click()

    # WAIT FOR VISIBILITY — "View All" only appears on the home screen, so it proves login worked.
    view_all = wait.until(EC.visibility_of_element_located(SUCCESS))
    assert view_all.is_displayed(), "Expected 'View All' on the home screen after login"
