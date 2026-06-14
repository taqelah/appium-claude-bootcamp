"""Session 2 · Gestures lab — DRAG & DROP (Python / pytest).

Drag "Drag Item 1" onto "Drag Item 4"; afterwards Drag Item 4 sits at position 3 (its
content-desc contains both "3" and "Drag Item 4"). `mobile: dragGesture` press-holds the
source, moves to the target, and drops.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import desc_contains, centre

REORDERED = (AppiumBy.XPATH, "//*[contains(@content-desc, '3') and contains(@content-desc, 'Drag Item 4')]")


def test_drag_and_drop(gestures):
    driver = gestures
    wait = WebDriverWait(driver, 20)

    src = wait.until(EC.visibility_of_element_located(desc_contains("Drag Item 1")))
    target = driver.find_element(*desc_contains("Drag Item 4"))
    end_x, end_y = centre(target)

    driver.execute_script("mobile: dragGesture", {
        "elementId": src.id, "endX": end_x, "endY": end_y, "speed": 1200,
    })

    assert wait.until(EC.visibility_of_element_located(REORDERED)).is_displayed()
