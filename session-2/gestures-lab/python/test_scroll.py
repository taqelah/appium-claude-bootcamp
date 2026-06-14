"""Session 2 · Gestures lab — SCROLL up & down (Python / pytest).

On the Gesture Demo screen, scroll DOWN to a bottom widget, then UP to the top. Two tools:
  • DOWN — UiScrollable.scrollIntoView drives the list's own scroller until found.
  • UP   — `mobile: scrollGesture` flicks along the right edge (clear of the cards).
"""

from conftest import scroll_into_view, scroll_until, desc_contains


def test_scroll_down_then_up(gestures):
    driver = gestures

    # SCROLL DOWN until "Pinch to Zoom" (near the bottom) is on screen.
    pinch = scroll_into_view(driver, "Pinch to Zoom")
    assert pinch.is_displayed()

    # SCROLL UP until "Swipe Card 1" (the top) is on screen again.
    top = scroll_until(driver, "Swipe Card 1", direction="up")
    assert top.is_displayed()
