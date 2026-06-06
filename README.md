# Appium + Claude Bootcamp 📱🤖

**AI-Assisted Mobile UI Test Automation using Claude** — a hands-on, 4-session bootcamp
(2–6 PM SGT) that takes you from zero to writing and maintaining real mobile UI tests for
**Android and iOS** with [Appium](https://appium.io), then using **Claude** to author and
maintain them faster.

By the end you'll be able to: stand up an Appium environment, find reliable locators, write
tests in **both** WebdriverIO + Mocha (Node) and Appium-Python-Client (pytest), scale them with
reporting and CI, and direct AI tooling to generate tests for you.

## Start here

> 👉 **Before Day 1, complete [`prerequisites/README.md`](prerequisites/README.md).**
> It installs Node, Python, the JDK, Android Studio + an emulator, and Appium 3.x — several GB of
> downloads, so start a few days early. Day 1 only *verifies* your setup; it doesn't re-teach it.

## Repository structure

| Folder | What it is |
|--------|------------|
| [`prerequisites/`](prerequisites/) | One-time setup guide — do this **before** the first session |
| [`session-1/`](session-1/) | **Session 1** — Introduction & Setup: landscape, Appium architecture, your first script, and a login-flow lab |
| _(more sessions added each week)_ | |

## The 4-session arc

| Session | Theme |
|---------|-------|
| **1** | Landscape & setup — first script + locators, core commands, a login flow |
| **2** | Real, maintainable tests — Page Objects, sync/waits, gestures, data-driven |
| **3** | Scaling — reporting, CI, parallel & cloud devices, debugging flaky tests; **Claude-assisted authoring begins** 🤖 |
| **4** | More Claude-driven authoring + putting it all together |

## Tech stack

- **[Appium 3.x](https://appium.io)** with the **UiAutomator2** (Android) and **XCUITest** (iOS) drivers
- **Node** — [WebdriverIO](https://webdriver.io) + Mocha
- **Python** — [Appium-Python-Client](https://github.com/appium/python-client) + pytest
- **Android Studio** emulator (required path); **Xcode** simulator (optional, macOS-only)
- **Claude** (Claude Code, taqwright, mobile-mcp/appium-mcp) for AI-assisted test authoring

## Each session at a glance

Every session folder is self-contained with its own `README.md`, a [Marp](https://marp.app)
slide deck (`slides.md`), and runnable labs. See [`session-1/README.md`](session-1/README.md) for
the full Day 1 agenda and how to present the deck.

---

Brought to you by [Taqelah](https://taqelah.sg) 🚀
