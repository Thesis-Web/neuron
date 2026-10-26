---
name: feedback_never_write_in_v1_owner_pastes
description: "Owner rule (2026-10-19): in ~/neuron/v1 Claude never writes, edits or runs anything that changes the owner's files; give SQL/code as text in chat and the owner cats or pastes it in. Read-only checks are fine; probes run on a scratchpad copy of brain.db."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7c20c611-9fe3-4487-be20-478341fdbaa9
  modified: 2026-10-21T17:50:18.145Z
---

Owner 2026-10-19, after a session wrote bottom.py and brain.db into ~/neuron/v1: "i said I will cat them in. and you I will copy paste from you... not you fucking write it.. I do not trust you. you break shit." Also, same day: "you are grounded,,, I am the interface now."

**Why:** it is the owner's own hand build; every earlier build drifted when an LLM had its hands on the files.
**How to apply:** never Write/Edit/run state-changing commands under ~/neuron/v1 (or any build the owner starts). Put code in the reply for them to paste. For live checks, copy brain.db to the scratchpad and probe the copy. Never run egg.sql against the live brain (it starts with DROP statements). See [[reference_neuron_spec_sources]] and [[project_neuron_v1_build_state_20261021]].
