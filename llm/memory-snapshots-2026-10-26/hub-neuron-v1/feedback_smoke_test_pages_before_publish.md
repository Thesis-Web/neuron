---
name: feedback_smoke_test_pages_before_publish
description: Run the page script under a fake DOM (scratchpad smoke.js pattern) before every artifact publish; a syntax check is not enough, a shadowed variable broke a whole published page on 2026-10-22
metadata:
  type: feedback
---

Before publishing any Neuron page, run its script in node with a fake DOM and a stubbed three.js (type lines, step every tick, click presets, run the measure) and require SMOKE OK. `node --check` passes code that throws on the first render.

**Why:** On 2026-10-22 version 13 of Point Of Connection shipped with a `var sgn` inside a callback that shadowed the outer polarity map; every render threw and the owner found the page "completely broken, cannot input the text". A second crash hid behind a blanket rename. Both were caught in two minutes by the harness, after the owner had already lost trust in the version.

**How to apply:** keep a smoke.js beside the page build (fake `document.getElementById` elements with listeners, `THREE` stubs with Vector3 math, `window.addEventListener`, `matchMedia`, `requestAnimationFrame`); run it after every build and before every Artifact publish; fix until it prints SMOKE OK. Related: [[reference_neuron_pages_20261021]], [[feedback_never_write_in_v1_owner_pastes]].
