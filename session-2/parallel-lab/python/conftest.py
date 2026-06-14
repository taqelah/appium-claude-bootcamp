"""Session 2 · Parallel lab — per-worker device assignment for pytest-xdist.

Run with `pytest -n 2`: xdist spins up two workers (gw0, gw1) and splits the parametrized
rows between them. Keyed on the worker id, the `driver` fixture pins each worker to its OWN
emulator (`appium:udid`), its OWN UiAutomator2 port (`appium:systemPort`), and its OWN Appium
server (port 4723 / 4724) — so the two sessions run fully independent. One server per device
is the recommended setup: a wedged/crashed session only takes down its own server, logs stay
per-device, and the sessions don't share one process. Run plain `pytest` (no -n) and it falls
back to the first device/server.

Prereqs (see ../README.md): TWO emulators booted (emulator-5554 + emulator-5556) ·
TWO Appium servers running (`appium -p 4723` and `appium -p 4724`) · demo APK on BOTH.
"""

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


APPIUM_HOST = os.environ.get("APPIUM_HOST", "127.0.0.1")

# One entry per parallel worker — each worker gets its OWN device, driver port, AND its own
# Appium server. Add more entries here (new udid + systemPort + appium_port) to scale up.
DEVICES = [
    {"udid": "emulator-5554", "systemPort": 8200, "appium_port": 4723},
    {"udid": "emulator-5556", "systemPort": 8201, "appium_port": 4724},
]

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


def _worker_index(request):
    """Map the xdist worker id (gw0, gw1, …) to a 0-based index; 'master' (no -n) → 0."""
    worker_id = getattr(request.config, "workerinput", {}).get("workerid", "gw0")
    digits = "".join(ch for ch in worker_id if ch.isdigit())
    return int(digits) if digits else 0


@pytest.fixture
def driver(request):
    # Pick this worker's device + ports + Appium server so parallel sessions don't clash.
    device = DEVICES[_worker_index(request) % len(DEVICES)]
    url = f"http://{APPIUM_HOST}:{device['appium_port']}"   # this worker's own server
    caps = {
        **CAPABILITIES,
        "appium:udid": device["udid"],
        "appium:systemPort": device["systemPort"],
    }
    options = UiAutomator2Options().load_capabilities(caps)
    drv = webdriver.Remote(url, options=options)
    yield drv
    drv.quit()


def run_login_case(driver, row):
    """Shared login flow + assertion — the same logic every row runs."""
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
