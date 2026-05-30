# Appium + Claude Bootcamp — Prerequisites

Welcome! 👋 This repo gets your laptop **ready before Day 1** of the
*AI-Assisted Mobile UI Test Automation using Claude* bootcamp
(4 Saturdays, starting **June 7, 2026**, 2–6 PM SGT).

Day 1 jumps straight into building tests. Please complete everything here **a few days early**
so we don't spend live class time on installs. If you get stuck, post in the cohort channel —
don't suffer in silence.

> **Time budget:** ~60–90 minutes, most of it downloads. Android Studio and the emulator image
> are large (multiple GB) — start early on a good connection.

---

## What you'll set up

| Tool | Why | Required? |
|------|-----|-----------|
| **Node.js 20 LTS+** + npm | WebdriverIO labs + Appium server + Claude Code | ✅ Everyone |
| **Python 3.10+** + pip | Appium-Python-Client labs | ✅ Everyone |
| **JDK 17** (Temurin) | Android automation engine needs Java | ✅ Everyone |
| **Android Studio** → SDK + emulator + 1 AVD | The device we automate against | ✅ Everyone |
| **Appium 2.x** + `uiautomator2` driver | The automation server | ✅ Everyone |
| **Appium Inspector** | Inspect app elements visually | ✅ Everyone |
| **Claude Code CLI** | Our AI pair-programmer (full setup Day 2) | ✅ Everyone |
| **Xcode** + `xcuitest` driver | iOS automation | 🍎 macOS only, optional |

We verify **both** client stacks (Node + WebdriverIO **and** Python) because the bootcamp uses both.

---

## Quick start

```bash
# 1. Clone this repo
git clone <repo-url> appium-claude-bootcamp
cd appium-claude-bootcamp

# 2. Install everything for your OS (pick one guide)
#    macOS  -> docs/install-macos.md
#    Windows-> docs/install-windows.md
#    Linux  -> docs/install-linux.md

# 3. Run the doctor to check what's installed
#    macOS / Linux:
bash scripts/doctor.sh
#    Windows (PowerShell):
#    powershell -ExecutionPolicy Bypass -File scripts/doctor.ps1

# 4. When the doctor is all-green, prove it end-to-end with the smoke tests
#    (start your emulator + `appium` first — see smoke/ READMEs)
```

---

## Step-by-step

1. **Install the toolchain** — follow the guide for your OS:
   - 🍎 [macOS](docs/install-macos.md)
   - 🪟 [Windows](docs/install-windows.md)
   - 🐧 [Linux](docs/install-linux.md)
2. **Set up an Android emulator (AVD)** — [docs/android-emulator.md](docs/android-emulator.md)
3. *(macOS, optional)* **Set up an iOS simulator** — [docs/ios-simulator.md](docs/ios-simulator.md)
4. **Install Claude Code** — [docs/claude-code.md](docs/claude-code.md)
5. **Run the doctor script** — it tells you exactly what's missing.
6. **Run the smoke tests** — proves Appium can drive your emulator:
   - [smoke/node](smoke/node/README.md) (WebdriverIO)
   - [smoke/python](smoke/python/README.md) (Appium-Python-Client)
7. **Tick off** [CHECKLIST.md](CHECKLIST.md) and you're ready. 🎉

Stuck? See [docs/troubleshooting.md](docs/troubleshooting.md).

---

## What "done" looks like

- `scripts/doctor.sh` (or `.ps1`) prints **all ✅** and exits with `PASS`.
- An Android emulator boots and shows up in `adb devices`.
- **Both** smoke tests connect, print your device's time, and exit cleanly.

---

## Need help?

- Cohort channel (invite emailed after registration)
- 📧 contact@taqelah.sg

See you on Day 1! — Syam
