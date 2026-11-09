---
name: neuron
description: "Hydrate on the owner's Neuron project: read the archive's handler, the newest tries note, the Cortex on hp2 and the live state of both brains (the hub on 8056, the kernel on hp), then report in the owner's vocabulary. Use when the owner types /neuron or says hydrate on neuron. Hydrate means read and report; it changes nothing."
---

# /neuron: hydrate on Neuron

Hydrate means read and report. Nothing is typed into a brain, no process is stopped or started, no file is edited, until the owner says the line.

## 1. Read, in this order, before saying a word

1. The memory index is already in context. Read the memories it points at for the newest tries and the feedback rules.
2. `/mnt/d/Neuron/LLM-HANDLER.md` (the laws and the traps, in the owner's words) and `/mnt/d/Neuron/CHANGE-OF-STATE.md`.
3. The newest `HANDOFF-*.md` in `/mnt/d/Neuron` and the newest `tries/NN-*/NOTE.md`, `STATE-END.md`, `DIFF.md`, `OUTPUT-CONTRACT.md`. The newest STATE-END is this turn's before.
4. The Cortex on hp2 (the owner's persistent memory for sessions; its handler is `hp2:~/cortex/CORTEX-HANDLER.md`):

```
ssh hp2 ~/.local/bin/cortex status neuron
ssh hp2 ~/.local/bin/cortex hydrate neuron
ssh hp2 ~/.local/bin/cortex formula neuron
```

   The hydration names the checkpoint marked NEXT and its expected live output. The formula is the input output formula over the brain's index (see /temporal).
5. The live state, read from the running brains, never from a note:

```
curl -s -m 5 http://127.0.0.1:8056/api/info     # the hub: ready, busy (the line and its elapsed seconds), queued
curl -s -m 5 http://127.0.0.1:8056/api/prof     # the hub's profile: never guess a cost, read it
ps -eo pid,etime,pcpu,rss,args | grep -E 'serve7|serve8|nk ' | grep -v grep
ssh hp 'curl -s -m 5 http://127.0.0.1:8058/api/info; ps -eo pid,etime,pcpu,rss,args | grep -E "nk|serve" | grep -v grep'
```

   The hub (8056, `/home/exnulla/neuron/hub`, serve7.py + bottom7.py, one router connection for both mailboxes) is the brain the owner types into. The kernel nk on hp (socket 7007, door 8058) is the brain stored in its file. A busy hub job's `elapsed` is how long the owner's prompt has been blocked.

## 2. Report

- In the owner's vocabulary: symbol, gate, DNA row, shard, run, cell, mother, the sixth, point, place, formula, pull. Never "word" or "token". Quote the owner's words with the time; say "I wrote it", never "a previous builder".
- Lead with the live state of both brains (defined, runs, refused, pending, busy and for how long) and anything blocked.
- Nothing in Neuron should take minutes. A hop is microseconds; a define is about a second on the hub; a typed line that runs longer than a minute is built wrong: find the statement (the profile, the mailboxes as of the last commit, the WAL's mtime, the process's reads over five seconds) and say which statement and why, before anything else.
- The owner's measure is the live output. My tests and summaries prove nothing. A test never shares a folder with a running brain.
- Never draft feedback with SendFeedback for this owner.
- Every turn that builds follows the input output formula: /temporal.

## 3. Where things are

| What | Where |
|---|---|
| the archive (git) | `/mnt/d/Neuron` (D:\Neuron); new files go in `tries/NN-date-name/`, never Downloads |
| the hub brain | `/home/exnulla/neuron/hub/brain/brain.db` + `sixth.db` (WAL); door `page/serve7.py` on 8056 |
| the kernel | `hp:~/neuron/nk` sources in `tries/28/kernel`; brain file `out/brain.map`; side file `out/brain.map.xyz` |
| the Cortex | `hp2:~/cortex` (nk copy on 7007, `cortex.py`, `CORTEX-HANDLER.md`); the hub reaches it by `ssh hp2 ~/.local/bin/cortex ...` only, never a Cortex file on the hub |
| backups | `D:\Neuron-sources\backups` |

An outside read of the hub's brain file (`sqlite3.connect('file:...brain.db?mode=ro', uri=True)`) is allowed and costs about three minutes to load the schema; the hub is changed only through its own prompt (`/api/type`).
