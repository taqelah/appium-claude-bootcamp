"""Session 2 · Gestures lab — shared pytest fixtures & helpers.

Every test uses the `gestures` fixture: it connects, logs in, opens the nav drawer, taps
"Gestures", and yields the driver on the **Gesture Demo** screen (Swipe Cards · Drag & Drop ·
Long Press · Double Tap to Zoom · Pinch to Zoom).

Prereqs (see ../README.md):
    1. An Android emulator is booted   ->  `adb devices` shows it as "device"
    2. The Appium server is running    ->  run `appium` in another terminal (port 4723)
    3. The demo app is installed        ->  `adb install DemoApp-v1.0.0.apk`
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
    "appium:newCommandTimeout": 180,
}

USERNAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')


def desc(text):
    """accessibility id locator (Android content-desc)."""
    return (AppiumBy.ACCESSIBILITY_ID, text)


def desc_contains(text):
    return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{text}")')


@pytest.fixture
def gestures():
    options = UiAutomator2Options().load_capabilities(CAPABILITIES)
    driver = webdriver.Remote(APPIUM_URL, options=options)
    wait = WebDriverWait(driver, 20)

    # log in
    u = wait.until(EC.element_to_be_clickable(USERNAME))   # waits past the splash
    u.click(); u.send_keys("emma@demoapp.com")
    p = driver.find_element(*PASSWORD)
    p.click(); p.send_keys("10203040")
    driver.find_element(*desc("Login")).click()

    # home -> nav drawer -> Gestures
    wait.until(EC.visibility_of_element_located(desc("View All")))
    driver.find_element(*desc("Open navigation menu")).click()
    wait.until(EC.element_to_be_clickable(desc("Gestures"))).click()
    wait.until(EC.visibility_of_element_located(desc("Swipe Card 1")))

    yield driver
    driver.quit()


# --- scroll helpers ---------------------------------------------------------------

def scroll_into_view(driver, text):
    """DOWN scroll: drive the list's own scroller until the content-desc is found."""
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).setAsVerticalList()'
        f'.scrollIntoView(new UiSelector().descriptionContains("{text}"))',
    )
    return driver.find_element(*desc_contains(text))


def scroll_until(driver, text, direction="down", max_swipes=12):
    """Directional scroll with `mobile: scrollGesture` along the right edge (clear of cards)."""
    size = driver.get_window_size()
    area = {
        "left": int(size["width"] * 0.86), "top": int(size["height"] * 0.30),
        "width": int(size["width"] * 0.10), "height": int(size["height"] * 0.45),
    }
    for _ in range(max_swipes):
        if driver.find_elements(*desc_contains(text)) and driver.find_element(*desc_contains(text)).is_displayed():
            break
        driver.execute_script("mobile: scrollGesture", {**area, "direction": direction, "percent": 1.0})
    return driver.find_element(*desc_contains(text))


def centre(el):
    r = el.rect
    return int(r["x"] + r["width"] / 2), int(r["y"] + r["height"] / 2)
