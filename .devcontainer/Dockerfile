# Reproducible CLIENT / test-code environment for the Appium + Claude bootcamp.
#
# IMPORTANT — what this image is NOT:
#   It does NOT run the Android emulator or the Appium server. Docker Desktop on
#   macOS/Windows cannot reach an emulator (no KVM) or a USB device (no USB
#   passthrough). So the emulator + Android SDK + Appium server stay NATIVE on
#   your host (see ../prerequisites/README.md).
#
# What this image IS:
#   A consistent place to write and run your test code (Node 20 + Python 3 +
#   the Appium client libraries). It talks to the Appium server running on your
#   HOST over HTTP at host.docker.internal:4723.

FROM mcr.microsoft.com/devcontainers/javascript-node:20-bookworm

# Python 3 + pip + venv for the Appium-Python-Client labs
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-pip python3-venv \
 && rm -rf /var/lib/apt/lists/*

# Pinned Python client libraries (globally importable). The Node client
# (webdriverio) is installed per-lab-project via `npm install`, since Node
# resolves packages from the project's local node_modules, not a global install.
RUN pip3 install --no-cache-dir --break-system-packages \
      "Appium-Python-Client==4.*" "pytest==8.*"

WORKDIR /workspace
