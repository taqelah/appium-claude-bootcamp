"""Session 2 · Gestures lab — DOUBLE-TAP to zoom (Python / pytest).

Scroll "Double Tap to Zoom" into view, then double-tap its image (a child view of the
section). `mobile: doubleClickGesture` fires two quick taps; pass = it runs and we stay put.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import scroll_into_view, desc

IMAGE = (AppiumBy.XPATH, "//*[@content-desc='Double Tap to Zoom']/../android.view.View[11]")


def test_double_tap_zoom(gestures):
    driver = gestures
    wait = WebDriverWait(driver, 20)

    scroll_into_view(driver, "Double Tap to Zoom")
    image = wait.until(EC.presence_of_element_located(IMAGE))

    driver.execute_script("mobile: doubleClickGesture", {"elementId": image.id})

    assert driver.find_element(*desc("Double Tap to Zoom")).is_displayed()
