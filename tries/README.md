# tries: every build, in order

One folder per build or group of builds, numbered by date. Each has a `NOTE.md` with: what it was, who built it, the owner's verdict in his words, the audit's verdict, what was right and carried forward, what was wrong, where its tests and audits are, and what was dropped as a duplicate when it was archived.

Version numbers were reused across three different lines, which is why the folders are numbered by date and not by version:

- The September line and Cortex: neuron-v1 to v4 (September), then neuron-v16.2 (to 10-13).
- The hand builds of October: old v18 and v19 (10-15, SQLite rows), then `~/neuron/v1` (10-19, the egg), `v2` (10-20, experimental), `v3` (10-26, deleted).
- The Point Of Connection pages: v11 to v17.3 (10-21 to 10-25), then the "new v18 core" (10-25), then build sheets 1 and 2 (10-25).

| # | Dates | Folder | One line |
|---|---|---|---|
| 00 | 09-16 to 10-13 | `00-2026-09-16-to-10-13-september-seed-and-cortex-16.2` | Python wrote the rows and walked them; the code is gone; what was recovered. |
| 01 | 10-15 to 10-16 | `01-2026-10-15-old-v18-and-v19-sqlite-rows` | Neurons as rows, one hop trigger, the first `/build` paste to mother; v19 was drift. |
| 02 | 10-18 to 10-19 | `02-2026-10-18-turn-one-hp-and-hp2-go-kernels` | Two Go kernels with lay files and live brains; both audited; both failed all four tests. |
| 03 | 10-19 | `03-2026-10-19-v1-egg-most-correct-so-far` | The owner's hand build: one table and one trigger per neuron, a 14-line mother, BUILD hands the words to SQL. The shape to step back to. |
| 04 | 10-20 | `04-2026-10-20-v2-experimental-rejected` | C + SQL with 44 fixed tables; rejected the same day. |
| 05 | 10-21 | `05-2026-10-21-drawings-no-brain` | One Space, Organized Kaos, the run and build-order diagrams. |
| 06 | 10-22 | `06-2026-10-22-point-of-connection-v11-to-v14` | Drawings v11 to v13; v14 the first real SQLite under JS neurons. |
| 07 | 10-23 | `07-2026-10-23-point-of-connection-v15-to-16.4` | Neurons as tables with per-row triggers; the told block is born; 16.4 is the draft's companion. |
| 08 | 10-23 to 10-24 | `08-2026-10-23-six-pulls-16.5-and-thirty-pulls-16.6-no-brain` | Placement experiments on the relation map; no brain in the pages. |
| 09 | 10-24 | `09-2026-10-24-point-of-connection-16.7-to-17.1` | 16.4's block byte for byte under new layouts; 17.1 the first brain-held positions; the silicon measured. |
| 10 | 10-25 | `10-2026-10-25-point-of-connection-17.2-17.3-and-native-prompt` | The command words as my SQL; audited row by row; a native prompt beside the page. |
| 11 | 10-25 | `11-2026-10-25-new-v18-core` | The only build where a word's birth is a run the brain ran; still templates, text and my choices. |
| 12 | 10-25 | `12-2026-10-25-build-sheet-1-egg2` | An instruction manual for the owner to paste in; rebutted at 00:41. |
| 13 | 10-25 | `13-2026-10-25-build-sheet-2-egg3` | Rebuilt to the rebuttal; 11 of 21 steps contradict his words; the last standing code. |
| 14 | 10-26 | `14-2026-10-26-v3-deleted` | A C runtime outside the brain, deleted the same night; a note and one leftover file. |
| 15 | 10-26 | `15-2026-10-26-point-of-connection-v18-page` | Not a build: the 17.3 page with tabbed rails on the new v18 core (11), which is unchanged; a local door (serve18.py) types lines into it and reads its tables. |
| 16 | 10-26 | `16-2026-10-26-teach-like-opposite-v18` | Not a build: two formulas, like and opposite, taught to 11's brain at the prompt (four lines in the shape of sheet18.json) and checked on a copy in memory; 11 is unchanged and nothing was saved. |
| 17 | 10-28 | `17-2026-10-28-define-who-full-run-drawing` | Not a build: the whole run of `define : who` from a fresh brain drawn in D2, v4 after his three corrections: every neuron its own table with numeric rows in his sketch's five columns, the long born run hit by hit, the decide formula run and the new formula neuron born for it, the born runs by the formula path, born inline and step back as two cases, the sixth's questions and the guessing brain's confidence-to-belief table, neurons gaining shards, tools compounding, definition vs meaning with the measured SQL actions, the circle of the first meanings from the real slice, the three forms of a run, the inspection row, three columns wide, his words in tool pins; the walk beside it; the 23 whiteboards checked; ten open items left to him. |

The four tests every build is scored on (versions audit, 10-25): (1) a neuron is its own table with DNA rows; (2) a run assembles the SQL and mother pastes it, births included; (3) mother decides nothing and works no data; (4) only the table-making neurons, the hop and the trigger are hand-laid; nothing outside the brain thinks. The scores are in `../CHANGE-OF-STATE.md` §2.
