---
name: reference_headless_browser_wsl
description: How to look at an artifact page in a real headless Chromium (software WebGL) on this WSL box without root - playwright-core from ~/boxstead plus two library packages unpacked into the scratchpad
metadata:
  type: reference
---

Headless Chromium works here without sudo:
- playwright-core 1.64.0: `require('/home/exnulla/boxstead/node_modules/playwright-core')`; browsers are cached in ~/.cache/ms-playwright (chromium_headless_shell-1248).
- It lacks libnspr4/libnss3: `apt-get download libnspr4 libnss3` (no root), `dpkg-deb -x <deb> <dir>`, then `LD_LIBRARY_PATH=<dir>/usr/lib/x86_64-linux-gnu:<dir>/usr/lib/x86_64-linux-gnu/nss`.
- Launch args for three.js pages: `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`. Route only file: and cdnjs requests.
- Test rail scroll stability with page.evaluate-dispatched events, not page.fill/click (those move focus and scroll the rail themselves).
Windows chrome.exe/msedge.exe exist under /mnt/c but are not used. Related: [[feedback_smoke_test_pages_before_publish]].
The unpacked libs live in the session scratchpad and vanish when /tmp is wiped (reboot 10-23): re-run `apt-get download libnspr4 libnss3` + `dpkg-deb -x` into <scratchpad>/libs/root (takes seconds).
