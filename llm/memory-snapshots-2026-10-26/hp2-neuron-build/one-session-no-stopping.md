---
name: one-session-no-stopping
description: Neuron turn one must be carried through to told ends in one go; never stop after a round to propose the next one
metadata:
  node_type: memory
  type: feedback
  originSessionId: 80f23f53-d360-40fd-961c-3729213563d8
  modified: 2026-10-19T12:28:25.033Z
---

On the Neuron hp2 build, after adversary round 3 the session stopped and laid out a "plan" for round 4. The owner pushed back: "this was all supposed to be in one turn... it was supposed to be done?"

**Why:** CLAUDE.md and the builder guide (§5) say all of turn one is built in one session because of drift; stopping to report a plan hands the work back to the owner and breaks that.

**How to apply:** When a round ends with work left, go straight into the next round (builders, merge, adversary, §19 re-check, told ends) and only report when turn one is done or truly blocked. Report status as progress, not as a proposal awaiting approval.
