# Data-Driven Lab — One Test, Many Inputs 🔢

Run the **same login test over a table of credentials**, fed from **three different sources** —
an **inline** array, a **CSV** file, and a **JSON** file — in both Node and Python. The login
logic is written once; only the data source changes. Each row is reported individually, so you
see exactly which input passed or failed.

> **The app:** [`taqelah/demo-app`](https://github.com/taqelah/demo-app/releases/tag/v1.0.0) —
> the same Flutter app from Session 1. A valid login reaches the home screen (**View All**);
> wrong/empty credentials stay on the login screen.

```
data-driven-lab/
├── data/
│   ├── credentials.json   the rows as JSON  { case, user, password, shouldPass }
│   └── credentials.csv    the rows as CSV   (header + one row per case)
├── node/        WebdriverIO + Mocha
│   └── test/
│       ├── cases.js                 runLoginCases() — shared login + assertion
│       ├── data.js                  loadJson() + loadCsv() loaders
│       └── specs/
│           ├── inline-data.e2e.js   rows are an array literal in the test
│           ├── csv-data.e2e.js      rows from credentials.csv
│           └── json-data.e2e.js     rows from credentials.json
└── python/      pytest
    ├── conftest.py            driver fixture + load_json()/load_csv() + run_login_case()
    ├── test_login_inline.py   rows as a list literal in the test
    ├── test_login_csv.py      rows from credentials.csv
    └── test_login_json.py     rows from credentials.json
```

**Three tests, one set of cases — only the data SOURCE differs:** inline (in the test code),
CSV, and JSON. The login logic + assertion live once (`cases.js` / `run_login_case`). The four rows:

| Case | User | Password | Expected |
|------|------|----------|----------|
| valid credentials | `emma@demoapp.com` | `10203040` | ✅ reaches home |
| wrong password | `emma@demoapp.com` | `wrongpass` | ❌ stays on login |
| unknown user | `nobody@demoapp.com` | `10203040` | ❌ stays on login |
| empty fields | _(empty)_ | _(empty)_ | ❌ stays on login |

---

## 0 · Prerequisites

```bash
node -v                            # v26+
python3 --version                  # 3.10+   (Windows: python --version)
appium -v                          # 3.x
adb devices                        # your emulator, "device" not offline
```

## 1 · Get the app onto your emulator

```bash
# download DemoApp-v1.0.0.apk from:
#   https://github.com/taqelah/demo-app/releases/tag/v1.0.0
adb install -r DemoApp-v1.0.0.apk
```

---

## 2 · How it works

- **Three data sources, one test logic.** The same 4 cases come from three places — an
  **inline** array, a **CSV** file, a **JSON** file — and run through the *same* runner
  (`cases.js` / `run_login_case`). Only the source differs.
  - **inline** — rows written directly in the spec/test (the simplest source).
  - **CSV** — Node `test/data.js → loadCsv()` (tiny comma-split parser) · Python stdlib `csv`.
  - **JSON** — Node `loadJson()` · Python stdlib `json`.
  - ⚠️ CSV values are all **strings** — coerce `"true"`/`"false"` to a boolean.
- **One case per row.** Node `rows.forEach(row => it(...))`; Python `@pytest.mark.parametrize`.
  Each row (per source) shows up as its own pass/fail line.
- **Test isolation — fresh login per row.** A failed attempt must not leak into the next case:
  - **Node** — `beforeEach(() => browser.reloadSession())` relaunches the app per `it()`.
  - **Python** — the function-scoped `driver` fixture opens a new session per parametrized row.
  - This is the same isolation discipline the **Parallel** topic depends on.

---

## 3 · Start the emulator + Appium server

```bash
emulator -avd Pixel_10_Pro_XL      # boot your AVD (use YOUR name); leave running
appium                             # in its own terminal — http://127.0.0.1:4723
```

## 4 · Run the lab

```bash
# 🟢 Node (WebdriverIO + Mocha) — one it() per row
cd node
npm install        # first time only
npm test

# 🐍 Python (pytest) — one case per row
cd python
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```

---

## 5 · Expected result ✅

**12 cases** pass per stack — the 4 rows × 3 sources (inline, CSV, JSON). The bad rows
**assert that login fails** (`reachedHome == shouldPass`), so the run is green:

```
# Node (WebdriverIO + Mocha) — 3 specs
 ✓ [inline] valid / wrong / unknown / empty
 ✓ [CSV]    valid / wrong / unknown / empty
 ✓ [JSON]   valid / wrong / unknown / empty
12 passing

# Python — 3 test files
test_login_inline[…]  PASSED   ×4
test_login_csv[…]     PASSED   ×4
test_login_json[…]    PASSED   ×4
==== 12 passed ====
```

---

## 6 · Make it yours

- ➕ Add a row to `data/credentials.json` **or** `data/credentials.csv` (e.g. a different bad
  password) — re-run; a new case appears automatically in **both** stacks, for that source.
- 🧪 Flip a `shouldPass` to the wrong value and watch **only that row** go red — that's the
  point of per-row reporting.
- 🐌 Comment out the `reloadSession` / function-scoped reset and watch later rows misbehave
  (the previous login leaks in) — that's why isolation matters.

---

## 🆘 Troubleshooting

| Symptom | Fix |
|---------|-----|
| Every row "reaches home" | Sessions aren't resetting — keep `reloadSession` (Node) / the function-scoped fixture (Python). |
| Valid row fails | The login screen may still be on the **splash** — the test waits, but on a slow machine raise the timeout. |
| `ECONNREFUSED 127.0.0.1:4723` | Start `appium` in another terminal. |
| Node `reloadSession` slow | Expected — it relaunches the app per row for isolation; 4 rows ≈ a minute. |

A fresh session per row is deliberate; it's what makes data-driven tests trustworthy (and
ready to run in **parallel**).
