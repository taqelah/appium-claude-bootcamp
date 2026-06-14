"""Session 2 · Data-driven lab — source 2 of 3: CSV file (Python / pytest).

Same cases as the inline test, but the rows are read from ../data/credentials.csv.
"""

import pytest

from conftest import run_login_case, load_csv

CREDENTIALS = load_csv()   # data/credentials.csv


@pytest.mark.parametrize("row", CREDENTIALS, ids=[r["case"] for r in CREDENTIALS])
def test_login_csv(driver, row):
    run_login_case(driver, row)
