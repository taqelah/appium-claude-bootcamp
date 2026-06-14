"""Session 2 · Gestures lab — SWIPE left & right (Python / pytest).

Swipe Card 1 LEFT (delete) and Swipe Card 5 RIGHT (favourite); both leave the list.
`mobile: swipeGesture` drives the gesture over each card element.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import desc


def test_swipe_left_and_right(gestures):
    driver = gestures
    wait = WebDriverWait(driver, 20)

    card1 = wait.until(EC.visibility_of_element_located(desc("Swipe Card 1")))
    driver.execute_script("mobile: swipeGesture", {"elementId": card1.id, "direction": "left", "percent": 0.9})

    card5 = wait.until(EC.visibility_of_element_located(desc("Swipe Card 5")))
    driver.execute_script("mobile: swipeGesture", {"elementId": card5.id, "direction": "right", "percent": 0.9})

    assert not driver.find_elements(*desc("Swipe Card 1")), "Card 1 should be deleted"
    assert not driver.find_elements(*desc("Swipe Card 5")), "Card 5 should be favourited away"
