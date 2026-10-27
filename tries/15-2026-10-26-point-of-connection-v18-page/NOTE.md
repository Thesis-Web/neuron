# 15. Point Of Connection 18: the 17.3 page on the new v18 core (2026-10-26)

**Status: a page, not a brain.** Nothing in `tries/11` changed; its scores and its audit stand. This folder holds the page, the door it looks through, and the record of what was checked.

**The ask (owner, 10-26, verbatim):** "point of connection vesion 18 has no html ... i like the 17.3 point of connection html. but I would like the sidebars to have tabs such that they are not a continueous long scroll to get to all the different types of information. do not change the design of the v 18 ... just add the ability for the html to represent and interact with the design, basically take the 17.3 html update the side bars, and connect it to v 18 such that it works... possible? if so make it happen."

## What is here

- `NEURON-POINT-OF-CONNECTION-v18-2026-10-26.html`: the page. 17.3's stylesheet byte for byte (its lines 5 to 122), 17.3's stage (springs only, origin fixed, the space between points, spacing, axes, the atlas, the camera), and both rails rebuilt as four tabs each. 95 KB; 17.3 was 3.8 MB because it carried sql.js and the told block inside it. Nothing of a brain is inside this page.
- `serve18.py`: the door. It imports `host18.py` from `tries/11` unchanged and holds the brain in memory the way `neuron_prompt18.py` does (the file loaded by backup, the same 512 MB thread stack, the same recursion limit). It answers two things: a typed line, which it hands to `Brain.type` (an insert into the input table; the brain's triggers do the rest), and a SELECT, which it runs and returns. Anything that is not a SELECT is refused. It decides nothing, and the only way it writes into the brain is a typed line. It refuses to save onto the file it loaded.
- `tests/`: the two DevTools-protocol drivers that clicked through the page, and `CHECK-RESULTS-2026-10-26.md`, what they found.

Start it from this folder: `python3 serve18.py` (the tested brain of `tries/11`, loaded into memory, never written back), then open `http://localhost:8018/`. `python3 serve18.py some/other.db` opens another brain; a path that does not exist lays the bare core, and the brain tab's button types the four teaching lines.

## Why the brain is behind a door and not inside the page

17.3 ran its brain inside the browser on sql.js, and its own note records that past about 1,000 triggers a line "nests deeper than this browser can follow". v18's born run is 1,272 hops, each through mother, and v18's prompt needs a 512 MB thread stack for it. Running v18 inside the page would have meant writing mother again in JavaScript, which is changing v18. So the page is a window: it reads v18's tables and types into v18's input table, and v18 runs as it ran on 10-25.

## What each part reads, and from which table

| Where | What | Table |
|---|---|---|
| stage, points | every gate | `label` |
| stage, lines | arrival to gate, gate to remainder, gate to the neuron its trigger column names | every DNA table `g1, g3, ...` (read by a loop over `sqlite_master`, 75 ms in memory) |
| stage, lines | a word with a formula to the gates its teaching run touched | `formula`, `receipt` |
| step | one run's hops, in order | `receipt WHERE run = ?` |
| step, the runs of this line | every run with the same root | `run` |
| run | the run's cells; BUILD is what mother said | `sheet WHERE run = ?` |
| run | the words between a pair of BUILD gates | the run's receipt, words from `label` |
| run | fired, born, build, returns, end, output | `fire`, `born`, `build`, `secondary`, `end`, `output` |
| selected | the gate's DNA rows, its gate trigger, its definition node's rows and their return runs | `g<k>`, `sqlite_master`, `g<k+1>`, `run` |
| neurons, brain | every gate; counts; the hand-laid triggers; the formulas | `label`, `sqlite_master`, `shards`, `formula` |

## What is mine, labelled

- The door's two calls, the job queue, and the rule that a read is not "busy" while a line is not running.
- The tabs and which panel holds what.
- Which rows become lines, and the one rest length (30) for every kind. The positions are the page's; the brain holds none.
- The colours: grey hand-laid, blue born, orange with a formula, green definition nodes.
- The switch that hides the space neuron's lines (most DNA rows arrive from a space or go to one, so with it on the picture is a star around the space gate; that is what v18 holds).
- The four lines offered under Type are the lines of the v18 test (`test18.json`).
- The hop count in the readout is 0-based, as 17.3 counted ticks.

## Checked, 2026-10-26, on the hub

Chromium 156 (the Playwright build cached under `~/.cache/ms-playwright`, run headless with its missing NSS libraries extracted beside it), driven over the DevTools protocol by `tests/cdp-check-2026-10-26.js` and `-2`. The door on the tested brain `tries/11/.../brain18.db`. The numbers are in `tests/CHECK-RESULTS-2026-10-26.md`. In one line: every tab filled from the brain; stepping and play walked a run's receipt and went on into the next run; the dog gate showed its 9 DNA rows, its 32 definition rows best first, and its gate trigger as SQLite holds it; the define run showed its sheet with "ok" from mother for every BUILD cell and the words between the BUILDs; "define : cat" typed through the page ran in 2.6 s and said the Merriam-Webster line; the atlas listed 2,004 gates; a fresh brain laid the bare core (174 label rows, 87 shards, 100 triggers, no formula), took the four teaching lines in 70 s (292 label rows, 3 formulas, 900 shards, 159 triggers) and then said 2 to "BUILD SELECT 1 + 1 BUILD"; no console exception. The phone layout has no sideways scroll at 420 px.

## Not checked

- A word new to the brain, typed through the page (minutes to a quarter of an hour natively on 10-25; the page polls and shows the seconds, but I did not wait one out).
- The page opened as a file (`file://`) rather than from the door; the door sends the headers for it, untried.
- Firefox, Edge, Safari; a real phone.
- Saving from the page writes a new file through `Brain.save`; the refusal to overwrite the loaded file was checked, a save itself was not.

## What I got wrong while building it, and found

- The door first marked the brain busy for every job, reads included, so two pages reading at once made one of them give up ("the brain is running a line"). Found by the headless check, fixed: only a typed line is busy.
- Three times I killed my own shell with `pkill -f` or `pgrep -f` on a pattern that sat elsewhere in the same command line (the third time inside this note's text), the trap `LLM-HANDLER.md` §4.8 names. The door was finally started by a command with no process search in it; stop it by PID from a command of its own.
- Patches that matched on backslash-u escapes in the page script failed, because the file holds the characters themselves (the shell heredoc had already turned the escapes into characters).
