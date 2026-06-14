"""Session 2 · Data-driven lab — source 3 of 3: JSON file (Python / pytest).

Same cases as the inline test, but the rows are read from ../data/credentials.json.
"""

import pytest

from conftest import run_login_case, load_json

CREDENTIALS = load_json()   # data/credentials.json


@pytest.mark.parametrize("row", CREDENTIALS, ids=[r["case"] for r in CREDENTIALS])
def test_login_json(driver, row):
    run_login_case(driver, row)
