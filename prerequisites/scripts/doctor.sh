#!/usr/bin/env bash
#
# doctor.sh — checks your machine is ready for the Appium + Claude bootcamp.
# Pure bash: no Node/Python required, so it runs even before you've installed them.
#
# Usage:  bash scripts/doctor.sh
# Exit code: 0 if all REQUIRED checks pass, 1 otherwise.

# Don't use `set -e` — we want to run every check and summarise at the end.

# ---- pretty output ----------------------------------------------------------
if [ -t 1 ]; then
  GREEN=$'\033[0;32m'; RED=$'\033[0;31m'; YELLOW=$'\033[0;33m'; DIM=$'\033[2m'; RESET=$'\033[0m'
else
  GREEN=''; RED=''; YELLOW=''; DIM=''; RESET=''
fi

FAILED=0          # number of required checks that failed
WARNED=0          # number of optional checks that failed

OS="$(uname -s)"
IS_MAC=false
[ "$OS" = "Darwin" ] && IS_MAC=true

pass() { printf "  ${GREEN}✅ %-26s${RESET} %s\n" "$1" "${DIM}$2${RESET}"; }
fail() { printf "  ${RED}❌ %-26s${RESET} %s\n" "$1" "$2"; FAILED=$((FAILED+1)); }
warn() { printf "  ${YELLOW}⚠️  %-25s${RESET} %s\n" "$1" "$2"; WARNED=$((WARNED+1)); }
hdr()  { printf "\n${DIM}── %s ──${RESET}\n" "$1"; }

have() { command -v "$1" >/dev/null 2>&1; }

# Extract first version-looking token (e.g. 20.11.0, 17.0.2) from stdin
firstver() { grep -Eo '[0-9]+(\.[0-9]+){1,3}' | head -n1; }

echo
echo "🔎 Appium + Claude Bootcamp — environment doctor"
echo "   OS: $OS"

# ---- Node + npm -------------------------------------------------------------
hdr "Node.js & npm"
if have node; then
  NODE_V="$(node -v 2>/dev/null | tr -d 'v')"
  NODE_MAJOR="${NODE_V%%.*}"
  if [ "${NODE_MAJOR:-0}" -ge 20 ] 2>/dev/null; then
    pass "Node.js" "v$NODE_V"
  elif [ "${NODE_MAJOR:-0}" -ge 18 ] 2>/dev/null; then
    warn "Node.js" "v$NODE_V found — v20 LTS+ recommended"
  else
    fail "Node.js" "v$NODE_V too old — install Node 20 LTS+"
  fi
else
  fail "Node.js" "not found — see docs/install-*.md (step: Node.js)"
fi
if have npm; then pass "npm" "v$(npm -v 2>/dev/null)"; else fail "npm" "not found — comes with Node.js"; fi

# ---- Python + pip -----------------------------------------------------------
hdr "Python & pip"
PY=""
if have python3; then PY=python3; elif have python; then PY=python; fi
if [ -n "$PY" ]; then
  PY_V="$($PY --version 2>&1 | firstver)"
  PY_MAJOR="${PY_V%%.*}"; PY_MINOR="$(echo "$PY_V" | cut -d. -f2)"
  if [ "${PY_MAJOR:-0}" -ge 3 ] && [ "${PY_MINOR:-0}" -ge 10 ] 2>/dev/null; then
    pass "Python" "v$PY_V ($PY)"
  else
    fail "Python" "v$PY_V too old — install Python 3.10+"
  fi
else
  fail "Python" "not found — install Python 3.10+ (see docs/install-*.md)"
fi
if have pip3; then pass "pip" "$(pip3 --version 2>&1 | firstver)"; \
elif have pip; then pass "pip" "$(pip --version 2>&1 | firstver)"; \
else fail "pip" "not found — install python3-pip"; fi

# ---- Java / JDK -------------------------------------------------------------
hdr "Java (JDK 17)"
if have java; then
  JAVA_V="$(java -version 2>&1 | firstver)"
  JAVA_MAJOR="${JAVA_V%%.*}"
  if [ "${JAVA_MAJOR:-0}" -ge 17 ] 2>/dev/null; then
    pass "Java" "v$JAVA_V"
  else
    fail "Java" "v$JAVA_V — JDK 17+ required (Temurin 17 recommended)"
  fi
else
  fail "Java" "not found — install JDK 17 (Temurin)"
fi
if [ -n "$JAVA_HOME" ] && [ -d "$JAVA_HOME" ]; then
  pass "JAVA_HOME" "$JAVA_HOME"
else
  fail "JAVA_HOME" "not set or invalid — export it to your JDK (see docs)"
fi

# ---- Android SDK ------------------------------------------------------------
hdr "Android SDK & emulator"
ASDK="${ANDROID_HOME:-$ANDROID_SDK_ROOT}"
if [ -n "$ASDK" ] && [ -d "$ASDK" ]; then
  pass "ANDROID_HOME" "$ASDK"
else
  fail "ANDROID_HOME" "not set — export ANDROID_HOME to your SDK (see docs)"
fi
if have adb; then pass "adb" "$(adb --version 2>/dev/null | firstver)"; \
else fail "adb" "not found — add \$ANDROID_HOME/platform-tools to PATH"; fi
if have emulator; then pass "emulator" "present"; \
else fail "emulator" "not found — add \$ANDROID_HOME/emulator to PATH"; fi
if have avdmanager; then pass "avdmanager" "present"; \
else warn "avdmanager" "not found — add cmdline-tools/latest/bin to PATH"; fi

# AVD present?
if have emulator; then
  AVDS="$(emulator -list-avds 2>/dev/null | grep -v '^$' || true)"
  if [ -n "$AVDS" ]; then
    pass "AVD created" "$(echo "$AVDS" | tr '\n' ' ')"
  else
    fail "AVD created" "no emulator defined — see docs/android-emulator.md"
  fi
fi

# Running device?
if have adb; then
  DEV="$(adb devices 2>/dev/null | awk 'NR>1 && $2=="device"{print $1}')"
  OFFLINE="$(adb devices 2>/dev/null | awk 'NR>1 && $2!="device" && $1!=""{print $1}')"
  if [ -n "$DEV" ]; then
    pass "device online" "$(echo "$DEV" | tr '\n' ' ')"
  elif [ -n "$OFFLINE" ]; then
    warn "device online" "device present but not ready ($(echo "$OFFLINE" | tr '\n' ' ')) — wait for boot"
  else
    warn "device online" "no emulator running — start one before the smoke test"
  fi
fi

# ---- Appium -----------------------------------------------------------------
hdr "Appium"
if have appium; then
  AP_V="$(appium -v 2>/dev/null | firstver)"
  AP_MAJOR="${AP_V%%.*}"
  if [ "${AP_MAJOR:-0}" -ge 2 ] 2>/dev/null; then
    pass "Appium" "v$AP_V"
  else
    fail "Appium" "v$AP_V — Appium 2.x+ required"
  fi
  DRIVERS="$(appium driver list --installed 2>&1)"
  if echo "$DRIVERS" | grep -q "uiautomator2"; then
    pass "uiautomator2 driver" "installed"
  else
    fail "uiautomator2 driver" "not installed — run: appium driver install uiautomator2"
  fi
  if $IS_MAC; then
    if echo "$DRIVERS" | grep -q "xcuitest"; then
      pass "xcuitest driver" "installed (iOS, optional)"
    else
      warn "xcuitest driver" "not installed (optional, iOS only) — appium driver install xcuitest"
    fi
  fi
else
  fail "Appium" "not found — run: npm install -g appium"
fi

# ---- Claude Code ------------------------------------------------------------
hdr "Claude Code"
if have claude; then
  pass "Claude Code CLI" "$(claude --version 2>/dev/null | firstver)"
else
  fail "Claude Code CLI" "not found — npm install -g @anthropic-ai/claude-code"
fi

# ---- iOS (macOS optional) ---------------------------------------------------
if $IS_MAC; then
  hdr "iOS (optional, macOS)"
  if have xcode-select && xcode-select -p >/dev/null 2>&1; then
    pass "Xcode tools" "$(xcode-select -p)"
  else
    warn "Xcode tools" "not installed (optional) — see docs/ios-simulator.md"
  fi
fi

# ---- Summary ----------------------------------------------------------------
echo
if [ "$FAILED" -eq 0 ]; then
  printf "${GREEN}══ PASS ══${RESET} All required checks passed."
  [ "$WARNED" -gt 0 ] && printf "  (${YELLOW}%d optional warning(s)${RESET})" "$WARNED"
  echo
  echo "Next: start your emulator + run \`appium\`, then run the smoke tests in smoke/."
  exit 0
else
  printf "${RED}══ FAIL ══${RESET} %d required check(s) failed" "$FAILED"
  [ "$WARNED" -gt 0 ] && printf ", %d optional warning(s)" "$WARNED"
  echo "."
  echo "Fix the ❌ items above (see docs/install-*.md and docs/troubleshooting.md), then re-run."
  echo "Tip: \`appium driver doctor uiautomator2\` diagnoses most Android issues."
  exit 1
fi
