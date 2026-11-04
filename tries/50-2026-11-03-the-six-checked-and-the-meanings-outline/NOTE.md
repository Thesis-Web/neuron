# tries/50 (2026-11-03, 20:10 to 21:15): the six checked, the kernel door's open set by key, the meanings outline

The owner, 20:10 (in full in `STATE-BEGIN.md`): "I hate signing off on things that are potentially built wrong, so double and triple check
c9,c10,c11,c12,c15,c16"; then the meanings: "make the outline for how we find them as the meaning points compound"; C13 unknown to the
owner; `define : who` prints the World Health Organization; the function words' definitions must be on point.

## The six, each against its expected output, by live output

| C | Expected (the Cortex) | Live output this turn | Verdict |
|---|---|---|---|
| 9 | a headless run of hp:8058/full reports visible points, springs, xyz entries, memory nodes for a clicked point, a screenshot | `cdp_c9.js` at 20:38: ready 6 s, 1,465 visible points, 3,540 rel lines of 20 kinds, 350 xyz entries, 1 memory node, screenshot; at 21:05 after the door's restart: ready 3 s, 1,463 points, 3,527 lines, 348 xyz, 1 memory node | met |
| 10 | the doors answer by key and by clock, never whole; a page read of the newest line under a second on the hub with the cascade running | keyed reads: kernel 1.5 to 19 ms (17:49), hub 19 to 279 ms (20:35) with the cascade hopping. **Not met before this turn:** the kernel page's open made four reads (input twice, out_user, the counts, the told list) that the door answered by building the whole-brain bundle (`bundle K` in C: a walk of every neuron's shards and the whole rel table; 1.34 s at K=1, 1.88 s at K=2000; 37 to 43 MB of JSON; the door at 551 to 662 MB), rebuilt on a read whenever older than 600 s | met after the door fix below |
| 11 | the page loads what it shows; with 80 points drawn the door serves no whole-brain read; the hub door process under a tenth of a core and 300 MB; a typed line shows its called and spawned runs beside the main run | the open replayed its history (90,861 hits) from the bundle's receipts: a whole-brain read at every open older than 10 min. Fixed below: the open set by key. The hub measure cannot be read as written: the hub's door process is the router too (103 % of a core, 1.2 GB with the cascade). The called run beside the main run: C12's receipt | met on the kernel after the fix; the hub measure is unmeasurable as written |
| 12 | `cold water freezes` steps its main run and its called run 19938168 together, the HUD naming both, the step count the longest run not the sum | `cdp_onehop.js` at 20:39: presses 1 to 3 show "2 runs alive this hop", the readout "hop 0 of 252 ... hop 2 of 252 in run 19938168" (the called run's 252, not 255) | met |
| 15 | thirty seconds of silence, no request; a line typed through the door arrives on the stream within the same second; the hub the same after the owner's restart | `cdp_stream.js` 30 s at 20:39 and 21:05: 0 requests, stream live. The typed line at 20:41: typed at 20:41:36.937, returned at .966, the stream told runs 19938186 at .964 (27 ms). The hub waits on the owner's restart. Remainder: the hub page polls `/api/job` every 2 s while a typed line runs (the kernel door answers a line in one response, so no poll there) | met on the kernel |
| 16 | the called run under the newest line drawn with its hops coloured by kind, the legend counting; the same on the hub; screenshots in tries 44 | `cdp_colors.js` at 20:40: the called run coloured state and time, the legend 4 after press 4 and 8 after press 8; the hub's screenshot of 17:xx shows only a typed line (white): no run with kinds under the hub's newest line | met on the kernel; the hub shows only the line kind |

My typed line for C15: one repeat of `cold water freezes` (run 19938182, 5 runs, 257 hits, 0.007 s). Nothing else typed.

## The door fix (g38, live on hp:8058 at 21:06, `serve8-g38-live.py`; the file before it `serve8-before-g38.py`)

The page's open set is read by key: `newest main K` (the typed and told lines), `run main ROOT` per line (its tree and hops), `run_memory
WHERE run IN (...)` per line; the history holds the receipts of the runs that hold their own (`same_as` 0, the bundle's `r->nrc` rule: a
run that repeats an earlier one borrows and lays none); a line's out rows are its root's sheet cells (the owner, 10-26: output to the user
comes from the same memory table); the counts from `stats` and one count of the rel table at the door's start; refreshed only when the
kernel's run count grew (`newest main 50`, the lines not yet seen), never on a clock; `bundle()` only for the old whole page's `/api/graph`.
Tested on 8059 against the live kernel in five steps (`door8059-open-set*.txt`): the first laid the repeats' borrowed receipts (1,184,249
rows), the second every run's (3,945,352), the third the roots' only (69,159, the 34 early sub-runs with their own receipts lost), the
fifth the bundle's rule: 88,561 rows over 2,273 runs against the bundle's 88,860 over 2,278 (the 5 runs only in the bundle are repeats),
1,353 gates against 1,355, and the told read moved above the bundle (it was the one read still building it). Live: the open set in 28.8 s at
the door's start (2,298 lines, 9,420 memory rows), the page ready in 3 s with 1,463 points, the door at 54 to 82 MB, `bundle_held` false
after the page's open. The owner's kernel tab needs a reload (the history's ids count from 1 again).

## C13

Mine: registered from the owner's 03:20 words on the floating graph ("the page springs run live by the brain formula rows, a kind toggled
off removes its pull..."); its page-springs half was rolled back on the owner's 03:55 words ("every run the same shape... that is wrong",
`page_patch10b`); what remains of it is C14 (the brain's own tension). The owner's call: reject it, or re-type it as C14's page half.

## The meanings outline, registered in the owner's words (C19 to C23, open)

C19 the known meanings inventoried from the brain's own rows (the kernel, gates 1 to 3000: 12 points hold 26 DNA rows with a call or
spawn: heard, born, define, meaning, why, correct, incorrect, print, create, change, step, type; the tool points write, alter, describe sit
above 3000; the egg lays 86 symbols; the SQL marks' actions are the measured source's rows). C20 the function words' definitions on point:
`define : who` traced: 40 node rows (gcide 23, wn 2, wikt 16); the newest define run 1324's def cell holds the first return, run 1332 from
WordNet, "noun 1: a United Nations agency to coordinate international health activities [syn: World Health Organization, WHO, W.H.O.]";
the encoder folds WHO, Who and who into gate 120 (the owner's open item of 10-26: digits inside words and case) and the def cell takes the
first return (the compile of several definitions, open). C21 a definition's uses as DNA shards (`how` holds 0 rows and 222 rel rows).
C22 combining the known meanings by the brain's own trial (tries/36 extended). C23 a wrong meaning fixed by back population. The
mechanisms are left as the owner's calls in each text. The prose on neuron code: `prose/2026-10-17-by-topic/NEURON_OWNER_WORDS_BY_TOPIC.md`
§14 (2026-09-29 to 10-17).

## Also

- Headless Chromium on the hub needs `LD_LIBRARY_PATH=/home/exnulla/.cache/boxstead-build-tools/browser-libs/extracted/usr/lib/x86_64-linux-gnu`; without it every check printed "no chrome".
- The Cortex's receipt judge: a sentence in the receipt's printed order passes ("ms 19.5 rows 10"); the same numbers in another order, a
  JSON line, or a sentence of timestamps is dropped or judged hallucination; hand trust went 0.61 → 0.57 on those misses this turn.
