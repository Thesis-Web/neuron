---
name: cortex
description: "Hydrate from the Cortex on hp2 (the owner's persistent cognitive memory for LLM sessions: state, time, grounding, hydration): read a project's status, hydration and input output formula from the brain on hp2, do the checkpoint marked NEXT, and return the live outputs to the Cortex as ingests. Use when the owner types /cortex or says hydrate from cortex. Nothing of the Cortex lives on the hub; every verb runs on hp2 over ssh."
---

# /cortex: hydrate from the Cortex, return outputs to it

The owner, 2026-11-02: "a persistant cognitive memory for llms, an organized database that could maintain state, time and grounding, and hydration". The Cortex is one nk brain on hp2 that holds every project's scope, outline (checkpoints, each with the live output that proves it), ingests and verdicts as typed lines. The hydration is the lean text a one-turn worker gets; the blink is that the worker gets nothing else. Its handler is `hp2:~/cortex/CORTEX-HANDLER.md`, FROZEN 2026-11-02 ~21:10 CST: it changes only with the owner's approval; progress goes into the brain, not into the file.

## 1. Reach it

The hub's one line (`~/.bashrc`): `alias cortex='ssh hp2 /home/james/.local/bin/cortex'`. In a tool call use the full form:

```
ssh hp2 /home/james/.local/bin/cortex <verb> ...
```

Law (owner 2026-10-13): never a Cortex file on the hub. This skill is a pointer like the alias; it holds no Cortex code or data.

## 2. Hydrate: read, change nothing

```
cortex status                     # the brain (gates, runs, refused, clock), the judge, the freeze shas, every project's checkpoints and last verdicts
cortex hydrate <project>          # the worker's whole prompt: DO NOW (the checkpoint marked NEXT), EXPECTED OUTPUT, the laws, all checkpoints, last verdicts
cortex hydrate <project> --at n   # the same for checkpoint n, with ACCEPTED SO FAR
cortex formula <project>          # the owner's input output formula over the brain: BEFORE, AFTER, PROGRESSION, CONTRACT satisfied | remainder (see /temporal)
```

Projects: `cortex` (the Cortex itself), `neuron` (the owner's brain: the kernel nk on hp and the hub on 8056; see /neuron), `probe` (the blink test). Run the formula before choosing a step: complete the remainder first unless it is gated on something not mine (the owner, 11-02: "check with cortex as to what parts of the outlines are complete that it holds, then you can decide if this is the next step, or completing previous state is more important first").

## 3. Register the work before building

```
cortex checkpoint <project> <n> : <what is built> '||' <the live output that proves it>
cortex state <project> <n> working
```

A new checkpoint on a frozen outline needs the owner's words asking for it; quote them in the checkpoint text.

## 4. Return the outputs, once live output exists

```
cortex ingest <project> <one sentence of observed live output, with its numbers>
cortex judge <project> <n> <run>     # the verdict: the shape read from the brain by run (echo = dupe, a new value supersedes and retires, a value out of line completes, nothing shared = drift), then the learned weights over the cells, then claude -p haiku as the fallback; a judgment cell's completes never moves the state
cortex accept <project> <n> <run>    # the owner's word only: that sentence is a part of C n's state; without a run, C n is done
cortex reject <project> <n> <run>    # the owner's word only: that sentence is not a part, whatever the judge said; it sticks
cortex mark <project> <run> <kind>   # the labeled set (completes progresses regresses supersedes drift invention hallucination dupe noise unsettled); the owner is the checker
cortex learn                         # build time: the (project, gate) key for new lines, then the judge's weights from the marks, leave-one-out accuracy printed
cortex formula <project>
```

An ingest is a context whole checked line by line: tool calls, paths, code and markup are noise and dropped; a repeat ticks and is never typed twice; a sentence that names what was observed (digits, backticks, printed, returned, output) carries the observation mark. A `completes` verdict of 0.7 or more moves the checkpoint to done and makes the sentence a part; `progresses` adds a part; a `dupe` ticks; a degression is rejected. A session's own text goes in by itself: the Stop hook on the hub (`~/.claude/settings.json`) pipes the transcript tail to `cortex capture --cwd` (cwd `~` = cortex, `~/neuron*` = neuron, anything else is not captured).

## 5. The grammar: every record is one typed line, a run with a clock

`cortex project <name> : <scope>` · `cortex checkpoint <name> <n> : <text>` · `cortex expected <name> <n> : <live output>` · `cortex state <name> <n> : open|working|done` · `cortex ingest <name> : <sentence>` · `cortex verdict <name> <n> <run> : <kind> <p> <judge>` · `cortex freeze : <sha256>`. The index is `main.cx` (kind, name, n → the newest run); `cortex q <sql>` is the keyed read, and the kernel refuses a scan of its own tables.

## 6. The laws that bind a worker (the handler's §2, the owner's)

- Report only what was observed as live output; name the command and its output; never invent a result, a term or a file; stay inside the scope; when the expected output is not met say so and why. End a worker answer with `EXPECTED: met` or `EXPECTED: not met` and the live output.
- Fast and light: no walker, timer, sweep, corpus query or log table. Stubs are illegal. Tests and summaries are never trusted; only live output is.
- The hp kernel's live state is never touched by the Cortex; the Cortex brain is the copy on hp2 (`nk` on 127.0.0.1:7007, `NK_MAP=~/cortex/brain/brain.map`). Nothing of Cortex lands on the hub.
- Learning (defining and placing a project's words) is build time and may be slow; use (ingest, judge, hydrate) is runtime and must be fast.
- The words are the owner's: project, scope, checkpoint, expected output, ingest, classification, judge, verdict, confidence, hydration, blink, drift, hallucination, invention, rail, edge, router.

## 7. Where things are

| What | Where |
|---|---|
| the handler (frozen, read-only, sha in the brain) | `hp2:~/cortex/CORTEX-HANDLER.md`; copy in Win Downloads `CORTEX-HANDLER.md` |
| the front door | `hp2:~/cortex/cortex.py` (stdlib python) behind `hp2:~/.local/bin/cortex`; repo `hp2:~/cortex` (git) |
| the kernel and its brain | `hp2:~/cortex/nk` (a copy of hp's source and line files), brain file `hp2:~/cortex/brain/brain.map` with `.main.db`, `.sixth.db`, `.xyz` beside it; user services `cortex-nk.service`, `cortex-page.service` (the page on hp2:8058) |
| the sources | `hp2:~/cortex/nk/sources` (wn, gcide, mwt, moby, map, sqldoc, measured, wikt; the guesser is out) |
| jev (optional) | key files `hp2:~/.config/cortex/typesafe.key` or `gateway.key`; none needed since 11-02 ~21:00 (the subscription judge) |
| the owner's Cortex words | Win Downloads `CORTEX-OWNER-WORDS-2026-11-02.md` (574 messages, 09-01 to 11-02) |
| the memory note | `project_cortex_build_hp2_20261102.md` in the memory folder |
