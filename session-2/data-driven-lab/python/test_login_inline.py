"""Session 2 · Data-driven lab — source 1 of 3: INLINE data (Python / pytest).

The credential rows are a list literal right here in the test code — the simplest
"data-driven" source. Same rows, same shared runner as the CSV and JSON tests.
"""

import pytest

from conftest import run_login_case

CREDENTIALS = [
    {"case": "valid credentials", "user": "emma@demoapp.com",   "password": "10203040",  "shouldPass": True},
    {"case": "wrong password",    "user": "emma@demoapp.com",   "password": "wrongpass", "shouldPass": False},
    {"case": "unknown user",      "user": "nobody@demoapp.com", "password": "10203040",  "shouldPass": False},
    {"case": "empty fields",      "user": "",                   "password": "",          "shouldPass": False},
]


@pytest.mark.parametrize("row", CREDENTIALS, ids=[r["case"] for r in CREDENTIALS])
def test_login_inline(driver, row):
    run_login_case(driver, row)
