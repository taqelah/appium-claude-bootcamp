"""Session 2 · Parallel lab — one login test over the credential rows.

Run with `pytest -n 2`: xdist distributes these parametrized rows across two workers, and
conftest pins each worker to its own emulator. Watch both devices log in at the same time.
Run plain `pytest` and all rows run on one device (the serial baseline).
"""

import pytest

from conftest import run_login_case, load_json

CREDENTIALS = load_json()   # ../data/credentials.json


@pytest.mark.parametrize("row", CREDENTIALS, ids=[r["case"] for r in CREDENTIALS])
def test_login(driver, row):
    run_login_case(driver, row)
