"""Session 2 · Data-driven lab — shared fixtures & locators.

The `driver` fixture is **function-scoped**, so pytest gives each parametrized row its own
fresh session (the demo app's data is cleared on session start) — i.e. every credential row
starts on a clean login screen. That's the test-isolation discipline the Parallel section needs.

Prereqs (see ../README.md): emulator booted · `appium` running · demo APK installed.
"""

import csv
import json
import os
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(name="credentials.json"):
    """Read the credential rows from a JSON file."""
    return json.loads((DATA_DIR / name).read_text())


def load_csv(name="credentials.csv"):
    """Read the same rows from a CSV file (stdlib csv → all strings, so coerce shouldPass)."""
    with open(DATA_DIR / name, newline="") as f:
        return [
            {
                "case": r["case"],
                "user": r["user"],
                "password": r["password"],
                "shouldPass": r["shouldPass"].strip().lower() == "true",
            }
            for r in csv.DictReader(f)
        ]

APPIUM_HOST = os.environ.get("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = os.environ.get("APPIUM_PORT", "4723")
APPIUM_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"

CAPABILITIES = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.taqelah.demo_app",
    "appium:appActivity": ".MainActivity",
    "appium:newCommandTimeout": 180,
}

USERNAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
LOGIN = (AppiumBy.ACCESSIBILITY_ID, "Login")
HOME = (AppiumBy.ACCESSIBILITY_ID, "View All")   # only on the post-login home screen


@pytest.fixture
def driver():
    options = UiAutomator2Options().load_capabilities(CAPABILITIES)
    drv = webdriver.Remote(APPIUM_URL, options=options)
    yield drv
    drv.quit()


def run_login_case(driver, row):
    """Shared login flow + assertion — same logic for the inline, CSV and JSON tests."""
    wait = WebDriverWait(driver, 20)

    username = wait.until(EC.element_to_be_clickable(USERNAME))   # waits past the splash
    username.click()
    username.send_keys(row["user"])

    password = driver.find_element(*PASSWORD)
    password.click()
    password.send_keys(row["password"])

    driver.find_element(*LOGIN).click()

    reached_home = False
    try:
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located(HOME))
        reached_home = True
    except Exception:
        reached_home = False

    assert reached_home == row["shouldPass"]
