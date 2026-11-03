# tries/39 (2026-11-02, 22:11 to 22:35 CST): the `/cortex` skill, gate 0's contract, gates 1 to 3 proven on a scratch kernel on hp2, the outputs returned to the Cortex

The owner, 22:11, after a `/clear`: "hydrate from /cortex <-- which should be a skill by now.. make that happen... about /neuron you have outline tasks to complete... and return outputs to the cortex..."; ~22:25: "also a little late but /temporal also."

`STATE-BEGIN.md`, `OUTPUT-CONTRACT.md`, `STATE-END.md`, `DIFF.md` are the input output formula for this turn. Everything below is read from the running brains and the Cortex.

## Hydrated from the Cortex (hp2)

`cortex status`, `cortex hydrate cortex`, `cortex formula cortex`: 14 of 14 done, frozen, remainder 0. `cortex hydrate neuron`, `cortex formula neuron`: 2 of 7 done, remainder C1 (working, NEXT: gate 0), C2 to C4 (the build chain's gates 1 to 3, typed into the Cortex on 11-02 as "the 10-31 review's proposal, not owner-ratified"), C7 (the sixth asks meaning questions itself). The hub had resumed hopping by itself after tries/37's finding (the page's reads stopped, the queue drained); nothing of mine changed it.

## The `/cortex` skill

`~/.claude/skills/cortex/SKILL.md` (copy `llm/skills/cortex-SKILL.md`), the same shape as `/neuron` and `/temporal`: reach (the one alias, every verb over ssh), hydrate (status, hydrate, formula), register (checkpoint, state), return (ingest, judge, accept as the owner's word only), the grammar, the laws that bind a worker, where things are. It is a pointer like the alias; no Cortex code or data on the hub (the law of 10-13). The harness listed it the moment the file existed and `/cortex` loaded it in this session. Registered in the Cortex as C14 with the owner's words quoted (the handler file stays frozen; the outline lives in the brain) and closed by the judge: completes 0.80 by graph.

## Gate 0 (C1): the contract before the tests

`GATE-0-CONTRACT.md` (22:24): the authority order frozen (the owner's words, the reference draft, the thesis; builds are evidence), the prohibited substitutions, the versions (`VERSIONS.txt`: the archive at 8aec227 with the kernel sources as they run in tries/28's working tree, their six shas, the binary built from them on hp2, the 22 line files with shas, the nine source files with sizes, SQLite 3.46.1, Linux 6.12), the test-machine footprint (hp2, `~/cortex/gates`, port 7009, its own map file), and fifteen tests with predicted traces and negative controls. Closed by the judge: completes 1.00.

## The scratch kernel on hp2

The kernel sources were copied byte for byte from the archive (the same shas on hp2), built with the archive's build line (`sqlite3.h` from the Cortex kernel folder), and a fresh egg was educated with the Cortex's `educate.sh` turned into `educate-gates.sh` (port 7009, `~/cortex/gates/brain/brain.map`, a copy of the sources so no running brain shares a folder, and no `pkill`): 22 files in 14 s, refused 0. From the moment its sixth was laid the brain ran its own define cascade (runs 18,177 at the end of education, 260,025 seven minutes later), as the Cortex brain and hp's do; the tests ran beside it. The Cortex kernel on 7007 kept its pid (1355161) throughout; hp and the hub were not typed into.

## The tests (`gates-test.py`, `gates-test-2.py`; raw output in `GATES-LIVE-OUTPUT.txt`, `GATES-LIVE-OUTPUT-2.txt`)

Gate 1, the substrate: the same line typed three times (runs 260026, 260052, 283789: born 3, 0, 0; the third keyed `same_as` to the second); the keyed read of water → gate 2802 twice and an unknown symbol → no row; a keyless count → the error `no query solution` and the keyed read answers after it; a missing table → `no such table: main.nosuchtable`; an unknown request → `unknown request` and `stats` answers after it; a nonsense line accepted with born 3; the brain's own REBIND form typed (`BUILD UPDATE dna SET call = 0 …`) read back as none and the restore read back 15607, the other two rows of define unchanged.

Gate 2, one actual neuron: the define neuron holds three function rows keyed (before, trigger): (heard, `:`) shard 118 call 15607, (the sixth, `:`) shard 471 call 19937222 ticked 27,135 times by the brain's own defines, (heard, unknown) shard 494; my `define : stone` and `define : rock` hit 118 (times 3 → 5 → 7 → 9 across the turn), `describe : stone` hit no row of its own; the `:` neuron has no rows and every line crossed it on the hop shard 16. The unknown `glorpfx`: born as gate 34042, its define left the `def` cell open (state 0), nodes 0, a memory row at run 261098 (that define cost 5.2 s and 17,724 runs: the brain's own asking around an unknown, left as observed). The disable: with (heard, `:`)'s call set to 0, `define : rock` made 257 hits and returned no def; restored, 2,228 hits and the def from wn (run 260677).

Gate 3, the run sheet: run 260083 (`define : stone`) is its own root, arrival heard, kind 0, ended; its sheet holds exactly me, know, remember, shape, what, def, known, unknown at state 1; def = 260091, a return run with parent 260083, kind 3, cell def (24), about stone (9492), source wn row 41964; stone's 524 node rows name return runs of the same parent and cell (wikt's among them); the run is in `complete` once; after 23,000 further runs of the brain's own the sheet reads back the same. The scratch kernel stopped with SIGTERM in 3.1 s ("the brain is in its file"), started again in 0.5 s; the run, its sheet and its receipts read back the same; `define : stone` recalled def run 260091 in 0.03 s with 23 runs against 536 the first time.

Four predicted traces failed as written and are listed in `DIFF.md` with their readings; the tests were not changed, three checks were added with their predictions written first (1.1b, 3.1b, 3.3b), all met.

## Returned to the Cortex

Twelve ingests this turn (two for the skill, one for gate 0, three per gate), nine verdicts, ten parts; the gates' first sentences were judged `progresses 0.50 by graph` (their words were the brain's, the expected outputs' words the chain's), the closing `EXPECTED: met` sentences with the live output were judged `completes 1.00 by graph` with the mark met, and the judge moved C2, C3, C4 to done. No `accept` was typed: that is the owner's word. `cortex formula neuron` at 22:32: 6 of 9 satisfied; remainder C7 (open), C8 and C9 (the hp builder session's, registered this evening from its own screen).

## What is mine, marked

The mapping of the chain's words to the brain's rows (arrival = the symbol before; shard = the dna row keyed (before, trigger); a recorded miss = the def cell open and nodes 0; "resumes" = a cell filled by its own return) is mine and is marked [mine] in the contract. The gates C1 to C4 are the 10-25 chain's, not owner-ratified; the owner's 22:11 words were read as the order to complete them as the Cortex holds them.

## Not done

C7: the sixth asks meaning questions itself, belief from evidence, formulas from state, triads when proven: the owner's design step on the live brains (hp and the hub), not started from this screen. The scratch brain on hp2 is stopped; its file stays in `~/cortex/gates/brain` (469 MB on disk) for a restart or deletion at the owner's word.

## Files

`STATE-BEGIN.md`, `OUTPUT-CONTRACT.md`, `GATE-0-CONTRACT.md`, `VERSIONS.txt`, `GATES-LIVE-OUTPUT.txt`, `GATES-LIVE-OUTPUT-2.txt`, `STATE-END.md`, `DIFF.md`; the hands: `educate-gates.sh`, `versions.sh`, `gates-test.py`, `gates-test-2.py` (they type and read; they decide nothing). The skill: `llm/skills/cortex-SKILL.md`.
