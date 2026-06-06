# Session 1 — Introduction & Setup  📱

> **AI-Assisted Mobile UI Test Automation using Claude** · Day 1 of 4 · ~4 hours (2–6 PM SGT)
> Goal: **everyone leaves with a green first Appium test** — then writes a real **login flow** using
> locators, core commands, and waits.

This folder is the teaching material for Session 1. It assumes you finished
[`../prerequisites/README.md`](../prerequisites/README.md) a few days early — Session 1 **recaps and
verifies** your setup rather than re-teaching the installs.

## What's in here

| File | What it is |
|------|------------|
| [`slides.md`](slides.md) | The lecture, as a [Marp](https://marp.app) Markdown deck |
| [`speaker-notes.md`](speaker-notes.md) | Per-slide talking points, timings, Q&A prompts (for the instructor) |
| [`first-script/`](first-script/) | **Lab 1** — your first Appium script in **Node** and **Python** |
| [`login-lab/`](login-lab/) | **Lab 2** — automate a login flow (locators + commands + waits) |

## Today's agenda (~4h · 2–6 PM)

**Part 1 — Foundations & First Test**

| Time | Segment |
|------|---------|
| 0:00–0:10 | Welcome, the 4-Sunday arc, instructor intro |
| 0:10–0:35 | Mobile testing landscape — iOS vs Android, native vs hybrid vs web |
| 0:35–1:05 | Why Appium? Architecture, history, capabilities, driver model |
| 1:05–1:30 | Environment recap + live verification + Appium Inspector demo |
| 1:30–2:00 | **Lab 1:** run your first Appium script (Node + Python) |

**Part 2 — Locators, Commands & a Real Flow**

| Time | Segment |
|------|---------|
| 2:00–2:10 | ☕ Break (after the first 2 hours) |
| 2:10–2:45 | Capabilities recap + **locator strategies** (accessibility id, id, xpath, class name) |
| 2:45–3:15 | **Core commands** — tap, sendKeys, getText + **waits** (implicit vs explicit) |
| 3:15–3:55 | **Lab 2:** automate a login flow (find locators in Inspector → script it) |
| 3:55–4:00 | Wrap-up, pitfalls, homework, next-session preview |

## Presenting the deck

The deck is plain Markdown — open `slides.md` in any editor to read it. To present as slides:

```bash
# Live preview with hot-reload (recommended for teaching)
npx @marp-team/marp-cli@latest -p -w session-1/slides.md

# Or export a standalone file to share
npx @marp-team/marp-cli@latest session-1/slides.md -o slides.html   # HTML
npx @marp-team/marp-cli@latest session-1/slides.md --pdf            # PDF
```

> 💡 The **Marp for VS Code** extension gives you a live side-by-side preview with no CLI at all.

## Running the labs

- **Lab 1** — [`first-script/README.md`](first-script/README.md): from "emulator booted" to a passing
  test in both stacks (uses the built-in Settings app).
- **Lab 2** — [`login-lab/README.md`](login-lab/README.md): automate a login flow on **your** app,
  with locators you find in Appium Inspector.

## After today

- Finish **both labs** on your own machine if we ran short on time.
- Open **Appium Inspector**, connect to your emulator, and explore three different apps' element
  trees — you'll need this skill every week.
- In the login lab, swap each locator (accessibility id → id → xpath) and feel which is most stable.
- Next session: **Page Objects, sync/waits patterns, gestures, and data-driven** maintainable tests.
