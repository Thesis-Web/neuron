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
cortex questions <project> [n]    # the open meaning questions: words of judged claims that no receipt, owner line or reference holds; the owner answers them (mark, accept, reject, or a source)
cortex remainder <project>        # the contract's parts left not satisfied, typed on their checkpoints, and NEXT WORK: the first part that does not say it waits on the kernel or the owner; `cortex remainder <project> <n> : <part left>` adds one, `... <n> <k> satisfied : <by what>` closes one
cortex verdicts <project> [n]     # every judged line of the project (or of checkpoint n), newest first: run, verdict, p, judge, when, part, mark, sentence; the run is what mark, accept and reject take
cortex at <project> <when> [word]  # C38 (11-04): the state of the project at a time of the graph's own (last tuesday, yesterday, 11-03): checkpoints as they stood (the formula snapshot), lines typed by voice, verdicts, questions, parts accepted then and since retired; with a word, the lines that held it with time, verdict and part state (the owner: last tuesday what was the state of neuron; walkers were ruled out)
cortex sources                    # C36 (11-04): every source with band, domains, lines, origin; and the routes (a project routes to domains; agreement n of m counts the routed sources)
cortex handbacks <project>        # C45 (11-04): the flaws headless workers handed back, parked on the owner; `cortex decide <project> <k> accept|reject|checkpoint [: <text> || <expected>]` unparks one
cortex states --backfill          # C42: seed the state history once; `cortex at` then reads each checkpoint's state changes to the minute
```

Projects: `cortex` (the Cortex itself), `neuron` (the owner's brain: the kernel nk on hp and the hub on 8056; see /neuron), `probe` (the blink test). Run the formula before choosing a step: complete the remainder first unless it is gated on something not mine (the owner, 11-02: "check with cortex as to what parts of the outlines are complete that it holds, then you can decide if this is the next step, or completing previous state is more important first").

## 2b. The workflow (C43 to C45, the owner 11-04 05:0x: front door is me through you, the back door is the headless)

```
cortex plan <project> <repo path> [--model m]   # the repo's own words (readme, docs) typed as the owner source <project>-repo; one design worker writes the outline; typed open; the liaison reads it (cortex status <project>) before any build
cortex build <project> [--box min] [--turns k] [--model m]   # the scheduler: hydrate the NEXT checkpoint, one headless worker turn on the hydration alone (claude -p in the repo), ingest, judge, move, again; a worker's NEEDED: line grows the next hydration (cortex need), a FLAW: line or no progress after two turns parks the checkpoint as a hand-back and the loop moves to the next unblocked one; a schedule line per turn
cortex check <project> <n> : <command>   # C47 (the owner 11-04: hold the line, demand it done correctly, not just done): the cortex's own check of a checkpoint, run by the scheduler in the repo after every turn, its print a receipt the worker never touched; `check ok` lets a close stand, `check wrong` reopens a checkpoint the worker's claims closed and tells the next worker why (a need); `cortex check <project> <n>` runs it now. Write the check with numbers of its own (random inputs, the tests file's sha) so special cases and edited tests fail it; keep each checkpoint's check to that checkpoint's cases (a check that tests a later checkpoint's case hands back a true flaw)
```

What the sample build taught (11-04 06:xx), now rules: a worker must restate the expected output in its own words with the values it observed after piping the print (a paraphrase never closes; the hydration says so); a backticked number is a value; a worker's `NEEDED:` is typed on the checkpoint and carried by the next hydration until the liaison clears it (`cortex need <project> <n> --clear`), or workers echo it; the hydration tells the next worker WHY THE LAST TURN DID NOT CLOSE the checkpoint (refusals by the print, the number and the cause; feedback, not state); a hand-back on no progress after two turns is usually a judge or hydration fault to read before deciding; a FLAW from a worker is often real (the plan's own expected can be wrong) and `cortex decide <project> <k> accept : <text> || <expected>` re-types it.

The capture judges only candidates for state (C40): a sentence with an observation, the expected mark, or two words shared with the expected or the accepted parts; the rest are typed for the record, never judged, never asked; drift, hallucination and invention never enter a hydration (LAST MOVES only). The hydration (C41) gives enough: the open checkpoint whole with the prints its expected names, its parts, remainder, questions, what the last workers said it lacked, the receipts rule and the ending lines; done checkpoints one line each.

## 2c. 11-04 15:xx to 16:xx (C48 to C52): the cascade kernel, the test system, the lesson, the why

The live Cortex kernel is hp's cascade kernel since 11-04 15:47 (hp2 commit 24e2ce8; the g35 binary kept as `nk/nk.g35-2026-11-02`): a word is one symbol in any script, returns re-cut, the output never cut, `relabel` back population, a hand laid symbol merges into its defined twin, the places history with the door verbs `restep` and `moved`. `cortex status` prints a `kernel:` line saying which kernel answers the port. The test system: the same kernel on port 7010 over a copy of the live brain (`~/cortex/brain-test`, `~/cortex/nk-new`); `CORTEX_PORT=7010 cortex <verb>` runs any verb against it.

```
cortex self start|stop|refresh                 # the test kernel on 7010; refresh = the live brain copied again (the live kernel stops for the copy, about 90 s)
cortex why <project> [--plan]                  # C49: the verdicts of the project the record itself proves wrong (a true line convicted, a false line accepted, a close the check undid, asked and convicted at once, a number held by a print called out), each with the cells and the rule; --plan registers the cortex's own plan on the project cortex-self (a clone of the front door at ~/cortex/work/self) with a check per fault; then cortex self refresh and cortex build cortex-self --box 20 --turns 4; a fix the check proves is carried to the live front door by the liaison with git
cortex source <name> reference --path <folder> [--glob a,b] : <what>   # C50: a code base's docs and code typed with the file path and line of every sentence; the verdict prints `code ground (C50): <source> <file>:<line> holds <pair>`; cortex sources shows the path
cortex questions <project> --ask               # C51: every open question's words looked up in the sources; a question whose every word a source holds closes naming the source (and file:line when it has paths); the rest wait on the owner
cortex lesson <project> <track folder> [--ladder 1,2,3,4,5,6 | --pick slug,slug]   # C52: a public teaching track (exercism python or go, cloned at ~/cortex/work/lessons/) as an outline in difficulty order: the lesson's own instructions in the repo folder, the tests passing as the expected, the answer key (the tests' shas and the exemplar) held in ~/cortex/work/keys/<project>/ outside the repo and checked by work/checks/lesson.py after every turn; the track's teaching docs typed as the source <project>-lesson with paths; then cortex build <project>
```

## 2d. 11-04 17:xx (C53 to C55, the owner 16:4x: the sixth as the second police officer; sources as mini source dbs behind the mother; the question family)

```
cortex second <project> <run>            # C53: the sixth's second opinion on a verdict: 1 the guessing (the brain's own define of the words with no ground), 2 the project record (the pairs it holds, the nearest shape: the expected or a part), 3 the sources (the dbs, with file and line); a ruling (the judge stands when a machine print was read; data held by a source or the record for half the pairs moves an off-rail verdict to unsettled by the sixth) and the shape the brain holds, for the llm to restate; typed on the sixth prompt
cortex dispute <project> <run> : <why>   # C53: the llm's side; a worker writes `DISPUTE: run <run> <why>` in its answer and the scheduler asks the sixth; the hydration carries the ruling (and the run numbers of the refusals)
cortex source <name> reference --db [--path <folder> [--glob a,b] | --from-brain | -] : <what>   # C54: a source into cx.db, the one attached source db (sqlite allows ten attachments: the sixth, eight kernel sources, cx; the guesser's slot, out since 10-31); every sentence a corpus row with path and line, keyed by word and pair in the index (sword, spair); nothing typed into the brain; the source's own symbol src_<name> and its gate in cx.me
cortex ask-source <name|all> <word or "a b"> [--run R]   # C54: the request in cx.inbox (the work trigger answers by word or by pair into cx.outbox, the carry trigger hands each return to mother): the returns are return runs under R with the source's gate as arrival and the src row as about; the brain keeps the pointer, the text is re-cut from the source row at read
cortex sources --migrate [--box min]     # C54: every reference source typed as lines moved into cx.db (the typed runs stay as history; the owner sources stay as lines, the designer's record); the ground, the questions and the code ground read the db
cortex ask <project> <question>          # C55: why did (run N | C n), how did (C n | run N), when did (C n), when is <day>, what next, what is <word>: the question word routes to the record (the verdict row, cortex why, the sixth's record, the schedule lines, the parts, the state history, cortex at, the remainder, define and the source dbs) and names its reads
```

The kernel on hp2 starts with `nk/start-nk.sh` and the source list in `nk/sources/LIST`; `cortex self refresh` carries cx.db to the test kernel. The kernel's own `define` still asks only the eight kernel sources (its dna names them); the Cortex asks cx.db itself through the same inbox.

## 2e. 11-04 20:xx (C57 and the project teach: the neuron builds its own replacements; the owner 18:4x: all may stay until the replacement is built correct, better until neuron builds it on its own, you have to teach it)

```
cortex teach dupe|pairs|known [--n k] [--project p]   # a lesson the brain takes: its own answer (the kernel's same_as on the whole line typed again; the returns under the run when it asks the source db per pair through cx.inbox; its know cell) beside the front door's answer on k random inputs; equal k of k, differ, not replayable by the encoder; the lesson line typed on the project teach
cortex retire <function> : <the owner words>        # the owner's word only: from then the front door reads the brain's answer alone (dupe: the kernel's same_as decides a repeat); cortex status prints held by the neuron
```

Laws of 11-04 18:2x to 18:4x (typed as owner lines on cortex and neuron): code never enters the brain as words (the hard block in `source`; a code base is a source db); code that does a brain function outside the brain takes the owner's permission, and all of it may stay until the neuron holds the function itself, proven side by side and retired on the owner's word; nothing is retired or killed before its replacement is proven; the builder must use the Cortex (stay in the home folder so the capture lands; report the friction). The guessing brain is cortex C56 (design, not built); the brain writing a function from a lesson's words is teach C6 (waits on the kernel's meaning work).

## 2f. 11-04 21:xx: the lesson plan (the project lesson-senses; the owner: a real doc that teaches a human, the teacher lectures, the judge holds a key the teacher never saw, problems marked, teach another way, a test, a quiz with edge cases)

```
cortex senses plan|lecture|problems|reteach|test|quiz [--n k]   # the learner is the test brain (CORTEX_LEARNER, 7010); the key is wordnet's own example sentences in wn.db, read by the judge only to mark; the record on the live cortex (lessonmark rows, the lecture/problems/test lines)
```

The brain's side (lesson-senses C2) is the hp builder's sense work (RECALL-12 and what it rests on); on the Cortex copy it is not yet in place (sense rows yes, sense shards no, landings on the space gate); handed to the neuron builder through the neuron project 11-04 21:5x. Do not debug their lines; ask through the Cortex.

## 2f. 11-09 (project rail; the owner 00:48: ok do it .. claude exec on the backside builds the tests and audits, so you are not checking your own work)

Only an audited cortex check closes a checkpoint. A completes verdict, the parts together, an accept, the judgment by graph and the state verb now record "met" and leave the checkpoint working; the hydration says MET, NOT CLOSED. You never write a check and never close a checkpoint yourself.

```
cortex author <p> <n> [--model m]     # a claude exec turn on a copy of the work writes the check: a library program (hp2:~/cortex/work/checks/lib, stored once) plus variables, citations from the source db; or answers no check (handed back: not yet a checkpoint)
cortex audit-check <p> <n>            # the check on the real work twice (fresh inputs: its inputs: line must differ), then on broken copies a codex exec turn made without seeing it, and on the work absent (empty folder / no brain on the port / empty report / target at nothing); every one caught or refused
cortex prove <p> [n] [--done] [--box min]   # write + audit + run: kept, closed, reopened (check wrong), handed back (no check, refused, author and auditor disagree)
cortex look <word> [<word>] [--source s]    # source db rows by word or pair, with path and line (read only): what an author cites
CORTEX_PORT=7010 cortex jev <p ...> [--n k] # rail C6: our own jev in the judge brain (judge/judge-jev.sql, rules 5 and 6 on the test kernel) beside the python judge; decides nothing
```

Checks of the cortex's own work run `CORTEX_PORT=7010 python3 cortex.py ...` against the test brain (stale since its last refresh; its source db was empty on 11-09). Docs sources added 11-09 (rail C5): python-3.13-library, sqlite-3.46, hp2-man, gnu-bash, gnu-coreutils.

## 3. Register the work before building

```
cortex checkpoint <project> <n> : <what is built> '||' <the live output that proves it>
cortex state <project> <n> working
```

A new checkpoint on a frozen outline needs the owner's words asking for it; quote them in the checkpoint text.

## 4. Return the outputs, once live output exists

```
<command> | cortex receipt <project> <n> <command>   # the machine's own print, piped in: the checkpoint's ground for values (never retyped by a model)
cortex ingest <project> <one sentence of observed live output, with its numbers>
cortex judge <project> <n> <run>     # the verdict: the shape read from the brain by run (echo = dupe, a new value supersedes and retires, a value out of line completes, nothing shared = drift), then the learned weights over the cells, then claude -p haiku as the fallback; a judgment cell's completes never moves the state
cortex accept <project> <n> <run>    # the owner's word only: that sentence is a part of C n's state; without a run, C n is done
cortex reject <project> <n> <run>    # the owner's word only: that sentence is not a part, whatever the judge said; it sticks
cortex ingest <project> --voice owner <text>   # the voice of a hand ingest (owner, hand, a session); the capture sets it by itself
cortex voices --rebuild           # every voice's counts recomputed from the newest verdict of each judged run (after a re-judge: a re-judge tallies twice until this runs)
cortex mark <project> <run> <kind>   # the labeled set (completes progresses regresses supersedes drift invention hallucination dupe noise unsettled); the owner is the checker
cortex learn                         # build time: the (project, gate) key for new lines, then the judge's weights from the marks, leave-one-out accuracy printed
cortex learn --pairs [--box s]       # build time: the (source or project, word pair) key for every line (C23): a claim's pairs held by which sources; a pair held by no source is a question
cortex formula <project>
```

An ingest is a context whole checked line by line: tool calls, paths, code and markup are noise and dropped; a repeat ticks and is never typed twice; a sentence that names what was observed (digits, backticks, printed, returned, output) carries the observation mark. A `completes` verdict of 0.7 or more moves the checkpoint to done and makes the sentence a part; `progresses` adds a part; a `dupe` ticks; a degression is rejected. C39 (the owner, 11-04 04:3x: the judge has to judge more than one sentence): an expected that names several outputs is done when its standing parts together cover 0.7 of its gates, each part speaking to the expected (0.3) and grounded by a receipt, the shape or the owner, never by a model; the formula prints `parts together cover x`. Write the expected as the sentences that will be typed. C33b, C33c, C33d: only a print older than the claim judges it; the verdict names a newer print that holds the number; a claim typed again after that print is a repeat judged at its newest tick, so pipe first and type the sentence again. A session's own text goes in by itself: the Stop hook on the hub (`~/.claude/settings.json`) pipes a hook line (cwd, the turn's final message from `last_assistant_message`, session, event) and the transcript tail to `cortex capture`; a SessionEnd hook does the same when the session ends (11-03 C20). The capture types the session's newest twelve Bash tool results as receipts of the project's checkpoint before its sentences, so the session's own prints judge its claims (C21); when every checkpoint is done it judges against the newest one for the record only, no parts, no state. `cortex status` prints the last capture per project; a stale time is a failed capture. cwd `~` = cortex, `~/neuron*` = neuron, anything else is not captured.

The judge after 11-03 C22 to C28: a receipt judges only a claim about its print (names its command, cites its values, or states the expected); a flag argument or a backticked command is not a value; a cortex print of its own verdicts grounds no part. The pair ground (C23): a claim's adjacent word pairs held by which sources, the project's own ingests as memory never ground; agreement k of m sources (C24) = sources holding at least half the pairs; sources confirm a claim (a near-identical line) or disagree (the same line with another value or a negation), three disagreeing and none confirming = hallucination by sources (C28); a claim differing from an owner line only by a value or a negation is a question naming that line (C26). Trust per voice (C25): `cortex status` prints each voice's claims, confirmed, false (by receipt, shape or sources only), guesses (a labeled guess never counts against), trust. The designer (C37, the owner 11-04): on cortex and neuron the owner's line counts as a reference (alone 0.60 or the owner's banded trust); three sources disagreeing with the designer is a question, never a false. A time in a claim (C38): a weekday, yesterday, today or a date names a window; the project's record in it grounds the claim's words (`timeline: last tuesday holds k of m words in n lines`); a day with no record asks.

Sources (11-03, C16): `cortex source <name> owner|reference [--domain a,b] : <what it is, where from, as of>` registers one (C36: its domains; `cortex source <name> --domain a,b` sets them later); `cortex source <name> -` types its sentences from stdin (build time). A claim's words are checked per gate against the receipts, the owner's words, the references and the brain's own projects; two or more words with no ground become a question, never a guess. Every part in the hydration carries its ground.

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
| the kernel and its brain | `hp2:~/cortex/nk` (hp's cascade kernel since 11-04, C48; the g35 binary beside it), brain file `hp2:~/cortex/brain/brain.map` with `.main.db`, `.sixth.db`, `.xyz` beside it; user services `cortex-nk.service`, `cortex-page.service` (the page on hp2:8058) |
| the sources | `hp2:~/cortex/nk/sources` (wn, gcide, mwt, moby, map, sqldoc, measured, wikt; the guesser is out) |
| jev (optional) | key files `hp2:~/.config/cortex/typesafe.key` or `gateway.key`; none needed since 11-02 ~21:00 (the subscription judge) |
| the owner's Cortex words | Win Downloads `CORTEX-OWNER-WORDS-2026-11-02.md` (574 messages, 09-01 to 11-02) |
| the memory note | `project_cortex_build_hp2_20261102.md` in the memory folder |
