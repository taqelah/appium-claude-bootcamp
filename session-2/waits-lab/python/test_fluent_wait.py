"""Session 2 · Waits lab — FLUENT wait (Python / Appium-Python-Client + pytest).

App: taqelah/demo-app (Flutter), same SPLASH-then-login flow as the other tests.

THE IDEA: a fluent wait is an EXPLICIT wait with two knobs turned —
    • poll_frequency  — how often to re-check, and
    • ignored_exceptions — transient errors to swallow while polling.
In Python, `WebDriverWait` *is* the fluent wait — it already takes both. (Selenium folds
Java's separate FluentWait into WebDriverWait.)

Prereqs (see ../README.md):
    1. An Android emulator is booted   ->  `adb devices` shows it as "device"
    2. The Appium server is running    ->  run `appium` in another terminal (port 4723)
    3. The demo app is installed        ->  `adb install DemoApp-v1.0.0.apk`

Run:   pip install -r requirements.txt   &&   pytest test_fluent_wait.py
"""

import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)

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

    # Turn the implicit wait OFF — fluent is explicit-style, just tuned.
    drv.implicitly_wait(0)

    yield drv
    drv.quit()


def fluent_wait(driver):
    """A FLUENT wait: explicit + a custom poll interval + transient exceptions to ignore."""
    return WebDriverWait(
        driver,
        timeout=20,                 # ceiling
        poll_frequency=0.5,         # re-check every 0.5s
        ignored_exceptions=[        # don't fail on these mid-transition — keep polling
            StaleElementReferenceException,
            NoSuchElementException,
        ],
    )


def test_login_with_fluent_wait(driver):
    wait = fluent_wait(driver)

    username = wait.until(EC.element_to_be_clickable(USERNAME))
    username.click()
    username.send_keys(USER)

    password = wait.until(EC.element_to_be_clickable(PASSWORD))
    password.click()
    password.send_keys(PASS)

    wait.until(EC.element_to_be_clickable(LOGIN_BTN)).click()

    view_all = wait.until(EC.visibility_of_element_located(SUCCESS))
    assert view_all.is_displayed(), "Expected 'View All' on the home screen after login"
