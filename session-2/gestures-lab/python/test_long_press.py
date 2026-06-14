"""Session 2 · Gestures lab — LONG-PRESS (Python / pytest).

Press-and-hold "Long press me for options" to open its context menu, then assert "Copy"
appears. `mobile: longClickGesture` holds for `duration` ms.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import scroll_into_view, desc


def test_long_press_opens_menu(gestures):
    driver = gestures
    wait = WebDriverWait(driver, 20)

    card = scroll_into_view(driver, "Long press me for options")
    driver.execute_script("mobile: longClickGesture", {"elementId": card.id, "duration": 1200})

    assert wait.until(EC.visibility_of_element_located(desc("Copy"))).is_displayed()
