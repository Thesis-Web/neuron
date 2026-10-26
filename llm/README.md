# llm: the model-side record

`memory-snapshots-2026-10-26/` holds copies, taken on 2026-10-26, of the memory files that Claude Code sessions kept on each machine. The live copies were left where they were (`~/.claude/projects/<project>/memory/`) because the sessions read them from there; these are the archive's record of what the model side believed, and when.

| Folder | From | What |
|---|---|---|
| `hub-neuron-v1/` | hub, project `~/neuron/v1` | 33 files, 10-21 to 10-26: the 90-item known-failures checklist (`feedback_known_failures_checklist.md`, read at the start of every Neuron turn), the rules the owner gave (never write in his build; new model beside the old; smoke-test pages; speak in brain terms; check every step against the draft's laws), one project memory per turn from the 10-22 physics results through build sheet 2, and the reference notes (where the specs live, the pages built, the brain on hp, headless Chromium). |
| `hub-neuron-v3/` | hub, project `~/neuron/v3` | The v3 night's one memory: "I built the runtime outside the brain again and called it learning". |
| `hub-neuron/` | hub, project `~/neuron` | One September memory about the unattended loop's record-keeping. |
| `hp-neuron-build/` | hp, project `~/neuron-build` | The hp lead's memory of turn one and turn two: paths, told ends, the guards, the hang. |
| `hp2-neuron-build/` | hp2, project `~/neuron-build` | The hp2 lead's one memory: one session, no stopping. |

The condensed version of all of this, with the owner's words, is `../LLM-HANDLER.md` at the root.

A note on what these are: the project memories were written by the sessions as they worked, before the audits. Where a project memory says a thing "works" or "was verified", read the audit of that build first (`../audits/`). The checklist is the exception: it was written at each catch, usually in the owner's words, and the 10-25 audits confirmed it item by item.
