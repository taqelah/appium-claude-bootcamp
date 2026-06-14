# Session 2 — Real, Maintainable Tests  📱

> **AI-Assisted Mobile UI Test Automation using Claude** · Day 2 of 4 · ~4 hours (2–6 PM SGT)
> Goal: **take last week's login test and turn it into a clean, scalable suite** — solid
> synchronization, gestures, data-driven tests, and running them in **parallel**.

This folder is the teaching material for Session 2. It builds directly on
[`../session-1/`](../session-1/): we **refactor** the login flow you wrote in Lab 2 into
something you can actually maintain and grow.

## What's in here

| File | What it is |
|------|------------|
| [`slides.md`](slides.md) | The lecture, as a [Marp](https://marp.app) Markdown deck |
| [`slides.html`](slides.html) | The deck exported to a standalone HTML file |
| [`slides.pdf`](slides.pdf) | The deck exported to PDF |
| [`waits-lab/`](waits-lab/) | **Runnable lab** — implicit vs explicit vs fluent waits, in **Node** and **Python** |
| [`gestures-lab/`](gestures-lab/) | **Runnable lab** — scroll, swipe, drag-drop, long-press, double-tap, pinch, in **Node** and **Python** |
| [`data-driven-lab/`](data-driven-lab/) | **Runnable lab** — one login test over a credentials table, in **Node** and **Python** |
| [`parallel-lab/`](parallel-lab/) | **Runnable lab** — the login suite across **two emulators** at once, in **Node** and **Python** |

> The **waits, gestures, data-driven, and parallel labs are runnable** (Node + Python). The Page
> Object topic is walked through **in the slides** this session. The parallel lab needs **two
> emulators** booted.

## Today's agenda (~4h · 2–6 PM)

**Part 1 — Synchronization & Gestures**

| Time | Segment |
|------|---------|
| 0:00–0:15 | Welcome back, recap of Session 1, today's goal |
| 0:15–1:00 | **Synchronization** — implicit vs explicit vs fluent waits, never `sleep` |
| 1:00–2:00 | **Gestures** — `mobile:` commands vs W3C Actions, scroll-to-element, swipe, long-press |

**Part 2 — Data-Driven & Parallel**

| Time | Segment |
|------|---------|
| 2:00–2:10 | ☕ Break (after the first 2 hours) |
| 2:10–2:45 | **Data-driven testing** — pytest `parametrize`, WDIO data loops, one flow → many rows |
| 2:45–3:35 | **Parallel testing** — `maxInstances` / `pytest-xdist`, one server + session per device, unique ports |
| 3:35–3:50 | **Assignment** — automate a full search → checkout purchase flow end-to-end |
| 3:50–4:00 | Putting it together (project layout), pitfalls, homework, next-session preview |

> **Page Objects** move to **Session 3** (structuring & scaling the suite) — today stays focused on waits, gestures, data-driven, and parallel.

## Presenting the deck

The deck is plain Markdown — open `slides.md` in any editor to read it. To present as slides:

```bash
# Live preview with hot-reload (recommended for teaching)
npx @marp-team/marp-cli@latest -p -w session-2/slides.md

# Or export a standalone file to share
npx @marp-team/marp-cli@latest session-2/slides.md -o slides.html   # HTML
npx @marp-team/marp-cli@latest session-2/slides.md --pdf            # PDF
```

> 💡 The **Marp for VS Code** extension gives you a live side-by-side preview with no CLI at all.

## Running the labs

Boot an emulator, start `appium`, install the demo APK, then run either lab in Node or Python.

**[`waits-lab/`](waits-lab/README.md)** — the login flow three times (implicit / explicit / fluent waits):

```bash
cd waits-lab/node      && npm install && npm test
cd waits-lab/python    && pip install -r requirements.txt && pytest
```

**[`gestures-lab/`](gestures-lab/README.md)** — six gestures on the app's **Gesture Demo** screen
(scroll, swipe, drag-drop, long-press, double-tap, pinch), each with a real assertion:

```bash
cd gestures-lab/node   && npm install && npm test
cd gestures-lab/python && pip install -r requirements.txt && pytest
```

**[`data-driven-lab/`](data-driven-lab/README.md)** — one login test over a shared credentials
table (valid / wrong / unknown / empty), each row reported individually:

```bash
cd data-driven-lab/node   && npm install && npm test
cd data-driven-lab/python && pip install -r requirements.txt && pytest -v
```

**[`parallel-lab/`](parallel-lab/README.md)** — the login suite split across **two emulators**
(`emulator-5554` + `emulator-5556`) so it finishes in about half the time. Boot **two** emulators,
start **two Appium servers** (`appium -p 4723` and `appium -p 4724`, one per device), and install
the APK on both first:

```bash
cd parallel-lab/node   && npm install && npm test
cd parallel-lab/python && pip install -r requirements.txt && pytest -n 2 -v
```

Each lab's `README.md` has the full walkthrough and "make it yours" tweaks.

## After today

- Finish the **search → checkout** assignment, and replace any `sleep()`s in your code with **explicit condition-based waits**.
- Replace any `sleep()`s in your code with **explicit condition-based waits**.
- Add a **third row** to a data-driven test and confirm it reports as its own pass/fail.
- Try a `mobile:` gesture (`scrollGesture`, `swipeGesture`) in **Appium Inspector** before scripting it.
- Boot a **second emulator** and run your data rows in parallel (`maxInstances` / `pytest -n 2`).
- Next session: **scaling** — reporting, CI, cloud device grids, debugging flaky tests —
  and **Claude-assisted authoring begins** 🤖
