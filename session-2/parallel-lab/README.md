# Parallel Lab — Two Devices, Half the Time ⚡

Run the login suite across **two emulators at the same time**. The four credential cases from the
[data-driven lab](../data-driven-lab/) are **split across two devices** — so the whole suite
finishes in roughly **half the wall-clock** of running them one after another. Same login logic,
same per-row isolation; the only new idea is **one session per device — each with its own Appium server and ports**.

> **The app:** [`taqelah/demo-app`](https://github.com/taqelah/demo-app/releases/tag/v1.0.0) —
> the same Flutter app from Session 1. A valid login reaches the home screen (**View All**);
> wrong/empty credentials stay on the login screen.

```
parallel-lab/
├── data/
│   └── credentials.json   the 4 rows  { case, user, password, shouldPass }
├── node/        WebdriverIO + Mocha  (shards specs across capabilities)
│   ├── wdio.conf.js        maxInstances 2 · 2 caps, each with its own port + udid + systemPort + specs
│   └── test/
│       ├── cases.js                 runLoginCases() — shared login + assertion
│       ├── data.js                  loadJson() loader
│       └── specs/
│           ├── group-a.e2e.js       first half of the rows  → emulator-5554
│           └── group-b.e2e.js       second half of the rows → emulator-5556
└── python/      pytest + pytest-xdist  (distributes rows across workers)
    ├── conftest.py            worker_id-keyed driver fixture + run_login_case()
    └── test_login_parallel.py one parametrized test over all 4 rows
```

**The four rows** (split A | B across the two devices):

| Case | User | Password | Expected | Device |
|------|------|----------|----------|--------|
| valid credentials | `emma@demoapp.com` | `10203040` | ✅ reaches home | A (5554) |
| wrong password | `emma@demoapp.com` | `wrongpass` | ❌ stays on login | A (5554) |
| unknown user | `nobody@demoapp.com` | `10203040` | ❌ stays on login | B (5556) |
| empty fields | _(empty)_ | _(empty)_ | ❌ stays on login | B (5556) |

> Node shards by **spec file** (each device runs one of `group-a`/`group-b`). Python lets
> **xdist** distribute the rows across workers automatically — only the device/ports differ.

---

## 0 · Prerequisites

```bash
node -v                            # v26+
python3 --version                  # 3.10+   (Windows: python --version)
appium -v                          # 3.x
adb devices                        # should list BOTH emulators, "device" not offline
```

## 1 · Boot TWO emulators

Parallel needs two devices. Open two terminals and boot two instances — they auto-number
`emulator-5554` and `emulator-5556` (you can use the same AVD twice):

```bash
emulator -avd Pixel_10_Pro_XL                 # terminal 1 → emulator-5554
emulator -avd Pixel_10_Pro_XL                 # terminal 2 → emulator-5556
adb devices                                   # confirm BOTH show up
```

> Different ports/UDIDs? Update `udid` in `node/wdio.conf.js` and `DEVICES` in `python/conftest.py`.

## 2 · Install the app on BOTH emulators

```bash
# download DemoApp-v1.0.0.apk from:
#   https://github.com/taqelah/demo-app/releases/tag/v1.0.0
adb -s emulator-5554 install -r DemoApp-v1.0.0.apk
adb -s emulator-5556 install -r DemoApp-v1.0.0.apk
```

## 3 · Start TWO Appium servers — one per device

```bash
appium -p 4723 --log appium-5554.log     # terminal 3 → serves emulator-5554
appium -p 4724 --log appium-5556.log     # terminal 4 → serves emulator-5556
```

**Why one server per device (not one shared server)?** A single Appium server *can* hold both
sessions, but each native session is heavy (UiAutomator2 instrumentation) and shares that
server's one Node process and log stream. Giving each device its own server means:

- **Fault isolation** — if one session hangs or its server crashes, the other device keeps running.
- **No contention** — sessions don't compete for one event loop or one set of internal state.
- **Cleaner logs** — one log file per device makes a flaky device easy to debug.
- **Scales the same way** — cloud device grids run a server (or container) per device, so the
  habit transfers directly (Session 3).

The server port is separate from the **driver** ports: each session is *also* kept apart by its
own `udid` + `systemPort` (Android) / `wdaLocalPort` (iOS).

---

## 4 · How it works

- **One Appium server per device.** Device A → `:4723`, device B → `:4724` (see §3 for why).
  Node sets `port` per capability; Python builds the server URL per worker from `DEVICES`.
- **One session per device.** Each parallel test drives its own emulator — `appium:udid` pins
  the device, `appium:systemPort` gives that UiAutomator2 session its own port so the two
  don't collide. (iOS would use `appium:wdaLocalPort` + a per-sim `derivedDataPath`.)
- **Node — shard by spec.** `maxInstances: 2` runs both capabilities at once; each capability
  lists its own `specs` (`group-a` → 5554, `group-b` → 5556), so the suite is split, not duplicated.
- **Python — distribute by worker.** `pytest -n 2` starts two xdist workers (`gw0`, `gw1`); the
  `driver` fixture reads the `worker_id` and hands each worker a device from the `DEVICES` table.
  xdist spreads the parametrized rows across the workers automatically.
- **Isolation is the precondition.** Each row still logs in fresh (Node `reloadSession`, Python
  function-scoped fixture). Parallel only works because the cases share no state and no order.

---

## 5 · Run the lab

```bash
# 🟢 Node (WebdriverIO + Mocha) — shards specs across the two devices
cd node
npm install        # first time only
npm test

# 🐍 Python (pytest + xdist) — distributes rows across two workers
cd python
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -n 2 -v
```

Watch **both** emulator screens — they log in at the same time.

---

## 6 · Expected result ✅

All 4 cases pass, spread across the two devices. The bad rows **assert that login fails**
(`reachedHome == shouldPass`), so the run is green:

```
# Node (WebdriverIO) — 2 specs on 2 devices, concurrently
 ✓ [device A] valid credentials / wrong password
 ✓ [device B] unknown user / empty fields
4 passing

# Python (pytest -n 2) — rows distributed across gw0/gw1
test_login[valid credentials]  PASSED
test_login[wrong password]     PASSED
test_login[unknown user]       PASSED
test_login[empty fields]       PASSED
==== 4 passed ====
```

Compare the wall-clock to a serial run (`pytest` with no `-n`, or `maxInstances: 1`) — two
devices finish in about half the time.

---

## 7 · Make it yours

- ➕ Add a **third emulator** (`emulator-5558`) + a **third Appium server** (`appium -p 4725`):
  add a capability in `wdio.conf.js` (new `port`/`udid`/`systemPort`/`specs`) and a third entry
  in `DEVICES` — then `pytest -n 3`.
- 🐌 Set `maxInstances: 1` (Node) or drop `-n` (Python) to feel the serial baseline, then
  re-enable parallel and watch the time drop.
- 🔀 Move a row between `group-a` and `group-b` (Node) and watch which device runs it.

---

## 🆘 Troubleshooting

| Symptom | Fix |
|---------|-----|
| Only one device runs | Check `adb devices` lists **both**; the `udid`s in config must match the actual serials. |
| `system port ... is occupied` | Each session needs a **unique** `systemPort` (8200 vs 8201) — don't reuse one. |
| Python: all rows on one device | You ran plain `pytest` — add `-n 2` so xdist starts two workers. |
| `ECONNREFUSED 127.0.0.1:4723` (or `:4724`) | Start **both** Appium servers — `appium -p 4723` and `appium -p 4724`. |
| A device hangs on the splash | Slow machine — raise the waits, or run the two emulators on a box with more RAM. |

Parallel is just isolated tests + one session per device on its own ports. Scale the same idea to
a **cloud device grid** in Session 3.
