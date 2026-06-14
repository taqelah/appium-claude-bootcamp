"""Session 2 · Gestures lab — PINCH in & out (Python / pytest).

Scroll "Pinch to Zoom" into view, then zoom IN (pinchOpen) and OUT (pinchClose) on its image.
`percent` is how far the two fingers travel. Pass = both gestures run and we stay put.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import scroll_into_view, desc

IMAGE = (AppiumBy.XPATH, "//*[@content-desc='Pinch to Zoom']/../android.view.View[15]")


def test_pinch_in_and_out(gestures):
    driver = gestures
    wait = WebDriverWait(driver, 20)

    scroll_into_view(driver, "Pinch to Zoom")
    image = wait.until(EC.presence_of_element_located(IMAGE))

    driver.execute_script("mobile: pinchOpenGesture", {"elementId": image.id, "percent": 0.75})   # zoom in
    driver.execute_script("mobile: pinchOpenGesture", {"elementId": image.id, "percent": 0.75})
    driver.execute_script("mobile: pinchCloseGesture", {"elementId": image.id, "percent": 0.75})  # zoom out
    driver.execute_script("mobile: pinchCloseGesture", {"elementId": image.id, "percent": 0.75})

    assert driver.find_element(*desc("Pinch to Zoom")).is_displayed()
