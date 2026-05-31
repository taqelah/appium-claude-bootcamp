# Optional: containerized test/client environment

This is an **optional** convenience. It gives everyone an identical Node + Python + Appium-client
setup for **writing and running test code**, without fiddling with language versions. It is **not**
a replacement for the native setup in [../prerequisites/README.md](../prerequisites/README.md).

## Why the emulator stays on your host

Docker Desktop on **macOS/Windows runs inside a Linux VM that can't reach a device**:

- **No emulator** — the Android emulator needs KVM hardware acceleration, which isn't passed
  through to containers on Mac/Windows.
- **No USB phone** — Docker Desktop on Mac/Windows has no USB passthrough either.

So the **emulator + Android SDK + Appium server run natively on your host**. The container only
holds the **test code + client libraries**, and reaches the host's Appium server over HTTP.

```
┌─────────────────── your host (macOS / Windows) ───────────────────┐
│  Android emulator  ◄──adb──  Appium server (port 4723)            │
│                                        ▲                          │
│                                        │ HTTP                     │
│   ┌──────────── Docker container ──────┼──────────────────────┐   │
│   │  your test code (Node / Python)  ──┘                       │   │
│   │  WebdriverIO · Appium-Python-Client                        │   │
│   │  reaches the server at host.docker.internal:4723           │   │
│   └────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

## Use it

**Prerequisites on your host first:** complete [../prerequisites/README.md](../prerequisites/README.md)
through Step 6 (JDK, Android Studio + emulator, Appium 3 + uiautomator2). The container does not
remove those — it can't.

1. Install **Docker Desktop** and the VS Code **Dev Containers** extension.
2. Open this repository in VS Code → Command Palette → **Dev Containers: Reopen in Container**.
   First build takes a few minutes; afterwards it's instant.
3. On your **host**, start the emulator and the Appium server:
   ```bash
   # host terminal
   appium                      # leave running; listens on 4723
   ```
4. Inside the container, write/run your tests. They connect to the host Appium server using the
   pre-set env vars `APPIUM_HOST=host.docker.internal` and `APPIUM_PORT=4723`.
   - **Python:** `Appium-Python-Client` + `pytest` are already installed.
   - **Node:** run `npm install webdriverio` in your lab project (Node resolves packages locally).

## Sharing a prebuilt image (optional)

By default each attendee builds the image locally on first "Reopen in Container" — nothing to host.
If you'd rather distribute a **prebuilt** image so there's no build wait:

```bash
# build + push once (maintainer)
docker build -t ghcr.io/taqelah/appium-bootcamp-client:latest .devcontainer
docker push ghcr.io/taqelah/appium-bootcamp-client:latest
```

Then swap the `build` block in [devcontainer.json](devcontainer.json) for:

```jsonc
"image": "ghcr.io/taqelah/appium-bootcamp-client:latest",
```

Attendees then just `docker pull` it (handled automatically on Reopen in Container).

## What's inside

- **Node 20** (base image) — for WebdriverIO labs
- **Python 3** + **Appium-Python-Client** + **pytest** — for the Python labs
- VS Code extensions: ESLint, Python
- `APPIUM_HOST` / `APPIUM_PORT` pre-set to reach the host Appium server
