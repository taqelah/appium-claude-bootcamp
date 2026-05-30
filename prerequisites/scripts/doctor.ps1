# doctor.ps1 — checks your machine is ready for the Appium + Claude bootcamp (Windows).
# Pure PowerShell: no Node/Python required, so it runs even before you install them.
#
# Usage:  powershell -ExecutionPolicy Bypass -File scripts\doctor.ps1
# Exit code: 0 if all REQUIRED checks pass, 1 otherwise.

$script:Failed = 0
$script:Warned = 0

function Pass($name, $detail) { Write-Host ("  [PASS] {0,-26} {1}" -f $name, $detail) -ForegroundColor Green }
function Fail($name, $detail) { Write-Host ("  [FAIL] {0,-26} {1}" -f $name, $detail) -ForegroundColor Red;    $script:Failed++ }
function Warn($name, $detail) { Write-Host ("  [WARN] {0,-26} {1}" -f $name, $detail) -ForegroundColor Yellow; $script:Warned++ }
function Hdr($t)              { Write-Host ""; Write-Host ("-- {0} --" -f $t) -ForegroundColor DarkGray }

function Have($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

# Pull first version-looking token (e.g. 20.11.0, 17.0.2) out of a string
function FirstVer($text) {
  if ($text -match '\d+(\.\d+){1,3}') { return $Matches[0] }
  return ''
}

Write-Host ""
Write-Host "Appium + Claude Bootcamp — environment doctor"
Write-Host "   OS: Windows"

# ---- Node + npm ----
Hdr "Node.js & npm"
if (Have node) {
  $nv = (FirstVer (node -v 2>$null))
  $major = [int]($nv.Split('.')[0])
  if ($major -ge 20)     { Pass "Node.js" "v$nv" }
  elseif ($major -ge 18) { Warn "Node.js" "v$nv found — v20 LTS+ recommended" }
  else                   { Fail "Node.js" "v$nv too old — install Node 20 LTS+" }
} else { Fail "Node.js" "not found — see docs\install-windows.md (step: Node.js)" }
if (Have npm) { Pass "npm" "v$(npm -v 2>$null)" } else { Fail "npm" "not found — comes with Node.js" }

# ---- Python + pip ----
Hdr "Python & pip"
$py = $null
if (Have python)   { $py = "python" } elseif (Have python3) { $py = "python3" }
if ($py) {
  $pv = (FirstVer (& $py --version 2>&1))
  $parts = $pv.Split('.')
  if (([int]$parts[0] -ge 3) -and ([int]$parts[1] -ge 10)) { Pass "Python" "v$pv ($py)" }
  else { Fail "Python" "v$pv too old — install Python 3.10+" }
} else { Fail "Python" "not found — install Python 3.10+ (see docs\install-windows.md)" }
if (Have pip)      { Pass "pip" (FirstVer (pip --version 2>&1)) }
elseif (Have pip3) { Pass "pip" (FirstVer (pip3 --version 2>&1)) }
else               { Fail "pip" "not found — reinstall Python with pip" }

# ---- Java / JDK ----
Hdr "Java (JDK 17)"
if (Have java) {
  $jv = (FirstVer (java -version 2>&1 | Out-String))
  $jmajor = [int]($jv.Split('.')[0])
  if ($jmajor -ge 17) { Pass "Java" "v$jv" }
  else { Fail "Java" "v$jv — JDK 17+ required (Temurin 17 recommended)" }
} else { Fail "Java" "not found — install JDK 17 (Temurin)" }
if ($env:JAVA_HOME -and (Test-Path $env:JAVA_HOME)) { Pass "JAVA_HOME" $env:JAVA_HOME }
else { Fail "JAVA_HOME" "not set or invalid — set it to your JDK (see docs)" }

# ---- Android SDK ----
Hdr "Android SDK & emulator"
$asdk = if ($env:ANDROID_HOME) { $env:ANDROID_HOME } else { $env:ANDROID_SDK_ROOT }
if ($asdk -and (Test-Path $asdk)) { Pass "ANDROID_HOME" $asdk }
else { Fail "ANDROID_HOME" "not set — set ANDROID_HOME to your SDK (see docs)" }
if (Have adb)        { Pass "adb" (FirstVer (adb --version 2>$null | Out-String)) } else { Fail "adb" "not found — add %ANDROID_HOME%\platform-tools to PATH" }
if (Have emulator)   { Pass "emulator" "present" } else { Fail "emulator" "not found — add %ANDROID_HOME%\emulator to PATH" }
if (Have avdmanager) { Pass "avdmanager" "present" } else { Warn "avdmanager" "not found — add cmdline-tools\latest\bin to PATH" }

if (Have emulator) {
  $avds = (emulator -list-avds 2>$null | Where-Object { $_ -ne "" })
  if ($avds) { Pass "AVD created" ($avds -join " ") }
  else { Fail "AVD created" "no emulator defined — see docs\android-emulator.md" }
}

if (Have adb) {
  $lines = (adb devices 2>$null) | Select-Object -Skip 1
  $online  = $lines | Where-Object { $_ -match '\sdevice$' }
  $offline = $lines | Where-Object { $_ -match '\S' -and $_ -notmatch '\sdevice$' }
  if ($online)       { Pass "device online" (($online | ForEach-Object { ($_ -split '\s')[0] }) -join " ") }
  elseif ($offline)  { Warn "device online" "device present but not ready — wait for boot" }
  else               { Warn "device online" "no emulator running — start one before the smoke test" }
}

# ---- Appium ----
Hdr "Appium"
if (Have appium) {
  $av = (FirstVer (appium -v 2>$null))
  if ([int]($av.Split('.')[0]) -ge 2) { Pass "Appium" "v$av" }
  else { Fail "Appium" "v$av — Appium 2.x+ required" }
  $drivers = (appium driver list --installed 2>&1 | Out-String)
  if ($drivers -match "uiautomator2") { Pass "uiautomator2 driver" "installed" }
  else { Fail "uiautomator2 driver" "not installed — run: appium driver install uiautomator2" }
} else { Fail "Appium" "not found — run: npm install -g appium" }

# ---- Claude Code ----
Hdr "Claude Code"
if (Have claude) { Pass "Claude Code CLI" (FirstVer (claude --version 2>$null)) }
else { Fail "Claude Code CLI" "not found — npm install -g @anthropic-ai/claude-code" }

# ---- Summary ----
Write-Host ""
if ($script:Failed -eq 0) {
  $msg = "== PASS == All required checks passed."
  if ($script:Warned -gt 0) { $msg += " ($($script:Warned) optional warning(s))" }
  Write-Host $msg -ForegroundColor Green
  Write-Host "Next: start your emulator + run 'appium', then run the smoke tests in smoke\."
  exit 0
} else {
  Write-Host "== FAIL == $($script:Failed) required check(s) failed, $($script:Warned) optional warning(s)." -ForegroundColor Red
  Write-Host "Fix the [FAIL] items above (see docs\install-windows.md and docs\troubleshooting.md), then re-run."
  Write-Host "Tip: 'appium driver doctor uiautomator2' diagnoses most Android issues."
  exit 1
}
