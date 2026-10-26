---
name: neuron-loop-pass-shape
description: "How an unattended Neuron loop pass actually lands its record (mailbox, not MCP close_out) and that the predecessor's pinned next_action note can be stale"
metadata:
  node_type: memory
  type: project
  originSessionId: ba19371f-f992-48b3-bfdb-9b656338b054
  modified: 2026-09-23T13:19:35.078Z
---

On an automatic Neuron pass (2026-09-23 onward), the experiment record goes into book `neuron` through `records/expNN/` + `mailbox_drop.sh neuron`, then a full-text readback with `hpcli.sh book-index neuron --chapters 1 --cap-ctok 60000` compared against chapter.md/page.md. The Cortex MCP `close_out` is not used for Neuron records: it would write to the shared front door's own book, and WAKE.md keeps Neuron's book separate. The controller writes its own short "loop ... iteration" transport chapter from `.loop_out/result.json`.

**Why:** the controller's "NOTE FROM YOUR PREDECESSOR" carried a next_action one experiment behind (it named question 5 while exp33/chapter 45 had already done it); PLAN.md, START_HERE.md and the newest experiment directory are the truth.

**How to apply:** at wake, trust PLAN.md progress + `git log` + `ls exp*/` over the pinned note; write `.loop_out/result.json` early with READY; deliver via the mailbox and verify readback before refreshing START_HERE/PLAN; commit with explicit `git add` of own files only. See [[neuron-project-state]].
