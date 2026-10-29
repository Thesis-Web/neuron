# 19. v6: the space-shard fix, the tools at the prompt, and the page in 17.3's look (2026-10-29)

**Status: a build, from v5 (tries/18) after the owner's words of 10-28 evening; not owner-read yet.** The brain here holds the 60 tool lines of `brain/LINES-v6.txt` and nothing else; the lines that educate it (`FIRST-RUNS-v6-2026-10-29.txt`) are the owner's to type. Every choice that is mine is in `CHAIN-v6-2026-10-29.md`, five columns per step.

**What the owner asked (10-28 evening, in full in the chain):** the page like 17.3 (the neurons acting, the relationships pulling, the run lines firing), the output readout made plain; the neuron with 1,000+ DNA rows of written SQL named as a cheat, each row to be a DNA row in the neuron with the label of that word; the button that typed a file of lines named as a cheat; the tools print, create neuron and change at the prompt; define : X to output the known and unknown meanings of a definition; the relationship autopopulate corrected and 17.3's relationship kinds back; a list of prompt runs that educate the brain, which the owner types.

## What changed from v5

| What | v5 | v6 | Where |
|---|---|---|---|
| A word's shard | keyed by the symbol just before and just after: the space, for every word. The space neuron held 1,955 rows, the word neurons one each. | keyed by the nearest symbol that is not the space on either side: a word's context is a row in its own table. The space holds one row. After the 60 lines: the space 1 row; the comma 86, the close bracket 58, the full stop 57, the equals sign 53; define 3 rows (heard → :, with the call; ' → '; change → :). | `brain/gen_egg6.py` (KB, KX) |
| The lines the brains pass | `seen N`, `why N cell` | `seen : N`, `why : N cell` (the key word's shard is one whatever N is) | `gen_egg6.py` (memory_go), `LINES-v6.txt` line 15 |
| define's relationships | kind = the first symbol of a source line, so "a" and "the" became kinds | kind = the kind word of the line (like, opposite); other = each word after it; 29 rows of kind like after define : as on the copy | `LINES-v6.txt` line 10, span 2 |
| define's output | what, def, know, remember, shape | plus known and unknown: the symbols of the returns with and without a definition of their own | line 10, span 3 |
| Tools | none | print dna / memory / node / sheet / table, create neuron, change trigger / call / spawn / define / meaning: each taught the long way, used once, bound (lines 28 to 60) | `LINES-v6.txt` |
| The page | its own stylesheet and a point cloud; every gate drawn at once; a text dump for the output; a button that typed 48 lines | 17.3's stylesheet byte for byte and 17.3's stage; the brain's history replayed hit by hit from the receipt table (points appear as lines bear them); the output as data sheets read back through the encoder; the lines files listed to click into the prompt, one at a time | `page/` |
| The door | typed a file of lines on request | serves the lines files with their {run:k} and {gate:x} read from the brains; the graph read carries memory counts and the calls' first gates; no call types a file | `page/serve6.py` |
| The bottom | | reads known/unknown back as symbols; matches a lines file against the lines already typed so {run:k} resolves after a restart | `brain/bottom6.py` |

## What is here

| File | What it is |
|---|---|
| `CHAIN-v6-2026-10-29.md` | The chain: the owner's words, then every change in five columns. Read first. |
| `brain/gen_egg6.py` → `brain/egg6.sql`, `brain/egg6-sixth.sql` | The hand-laid core, from v5's with the two changes above (marked v6 in the file). 294 statements, 80 hand-laid neurons, 12 triggers. |
| `brain/mother.c`, `brain/mother.so` | Mother, unchanged from v5. |
| `brain/bottom6.py` | The env handler and the prompts, from v5's. |
| `brain/LINES-v6.txt` | The 60 lines typed, in order, each with its grounding: the born runs and binds, the standing questions, the ask, the define run, the sixth's lines, why, correct and incorrect (1 to 27, from v5 with the v6 binds); the tools (28 to 60). |
| `brain/brain.db`, `brain/sixth.db` | The two brains after the 60 lines, laid on a Linux path from these files. |
| `LEDGER-v6-2026-10-29.md` | After each of the 60 lines: the run it started, runs, hits, born, refused, seconds, what landed in the out mailboxes. Written by the bottom from the brain's tables. |
| `FIRST-RUNS-v6-2026-10-29.txt` | The list of prompt runs for the owner: the thirteen define lines, the tools on what they made, the recurring unknowns, the SQL words, the guesses, the definition cells, the DNA columns, a new neuron, one key taught the long way. The page lists it. |
| `sources/` | The eight source brains and the guessing brain, laid from the archived slice as in v5 (`make_sources.py` unchanged). |
| `page/serve6.py`, `page/NEURON-POINT-OF-CONNECTION-v6-2026-10-29.html`, `page/src/` | The door and the page; `src/` holds the page in parts (17.3's stylesheet as the tries/15 page carries it, the body, the script in three parts) and `assemble.py` that writes the page from them. |
| `tests/` | The headless Chromium drivers (`cdp-check-v6.js`, `cdp-history-v6.js`), what they printed (`CHECK-RESULTS-2026-10-29.md`), the screenshots at 3,787 × 1,918 and 1,900 × 1,000, and the ledger of the tools used on a copy of the brain after their binds (`LEDGER-TOOLS-USED-ON-A-COPY-2026-10-29.md`, the lines in `TOOL-LINES-USED-ON-A-COPY-2026-10-29.txt`), and the ledger of the first pass of the 60 lines before the create neuron fix. |

## Run it

```
cd .../19-2026-10-29-v6-space-shards-tools-and-page/page
python3 serve6.py                    # then open http://localhost:8056/
cd ../brain; ulimit -s unlimited; python3 bottom6.py      # the two prompts at the terminal; "6> " for the sixth; Ctrl-D leaves
```
On the Windows drive (drvfs) a line takes about ten times longer than on ext4: copy the folder to a Linux path to work fast (the door and the bottom find the brains beside them). To lay fresh brains: `sqlite3 brain.db ".read egg6.sql"`, `sqlite3 sixth.db ".read egg6-sixth.sql"`, `python3 ../sources/make_sources.py ../sources/sat172.json ../sources wn=7,gcide=8,mw=9,mwt=10,moby=11,map=12,sqldoc=13,measured=14,guess=15`, or the page's start over. The 60 tool lines: `python3 bottom6.py --lines LINES-v6.txt --ledger ../LEDGER.md` (85 s on ext4), or click them into the prompt one at a time from the page.

## What the ledger shows (`LEDGER-v6-2026-10-29.md`, 60 lines, 85 s on ext4)

0 rows refused by SQLite in either brain; the five teaching lines and the nine tool formulas reply `error: no such column: above` the first time (typed at the top there is no run above them: the long way), then their binds reply ok. The space neuron: 1 row. define's table: 3 rows, the (heard, :) one carrying the call. The sixth: `why : 370 24` and `why : 390 24` for the two `define : :` lines; the guessing brain's `Health 0.50 0.50` fills the cell at line 20 and `incorrect : 390` lowers its belief to 0.25. One run without an end: the "ok" reply to the first born line, before born was bound (chicken and egg, as v5). The counts at the end are in the ledger's last rows and under the page's brains tab.

The tools, used on a copy after their binds (`tests/LEDGER-TOOLS-USED-ON-A-COPY-2026-10-29.md`): `print dna : who` says who's 5 rows as a table; `print memory : who` its 4 memory rows; `print node : who` its 2 returns read back; `print sheet : N` a sheet with cell names; `create neuron : canis` says the two tables of canis; `change define : who class noun` says 1 and the cell appears on the define run's sheet; `change meaning : who from noun to verb` says 0 before a meaning cell exists and 1 after `change define : who meaning noun`; `change trigger : who from 68 to 68` says 0; `define : the` 4.7 s, `define : as` 9.7 s (279 runs, 114 born, 29 rel rows of kind like); `define : who` again from memory, known = who as the.

## The page, checked (`tests/CHECK-RESULTS-2026-10-29.md`, 2026-10-29, headless Chromium 1248 over the DevTools protocol at 3,787 × 1,918 and 1,900 × 1,000)

Opens on the door; 265 gates, 1,332 shards; 352 points drawn, 1,763 springs (dna before 764, dna trigger 747, dna call 9, definition 69, answered 4, memory 84, alike 58, opposite 28); 111 lines listed under Type (60 tools, 51 first runs); stepping and play walk the run and go on into the next; the run tab shows the sheet read back and the BUILD pairs with mother's answers; who selected shows its 5 DNA rows with names and its 2 definition rows; `define : the` typed through the page ran in 9.6 s and its card shows what = the, def from Webster, known = the, unknown = 52 symbols; `print dna : the` ran in 2.75 s and its say cell is printed as a table; the brains tab, the atlas (302 gates); no console exception. The history: from the start 125 points (the 80 hand-laid, the sources, the dim words of the map) and 46 springs; after 18 s of play at 120 hits a second, run 46 of the born line, 149 points, 255 springs; the middle of the history, 311 points; back to now, 395. Screenshots: `tests/v6-*.png`, `tests/h*.png`.

## What is mine, labelled

The shard key's (NULL, NULL) for the space and the walk kept by position; the ":" in seen and why; the rule for reading a source line into rel rows; known and unknown as cells of gate lists; the three-span shape of every tool and the key word before ":"; the definition as the define run's sheet; create neuron calling the born run; the page's fixed point (heard), rest lengths, colours, the replay from the receipt table, the memory lines drawn dimmer; the door's calls; the order and example values of FIRST-RUNS. Each is in the chain's third column with what your words leave open beside it.

## Not checked

A define line typed through the page for a word new to every source (the sixth's why, the guess, correct/incorrect through the page: checked only at the terminal on the copy); the page on the Windows drive; Firefox, Edge, Safari; a phone; a history of more than 70,000 hits in the browser (it loads the whole receipt table once, 1.5 MB at 61,000 rows).

## Changed after the owner's first look (10-29, late)

The owner: "when I run a run on the v6 brain I don't see the run fire, just the neurons move... on 17.3 and 16.4 you actually see the run fire from neuron to neuron". 17.3 started play by itself the moment a line finished, from its first new tick; v6 set the history to the line's first hit and waited for the play button. Now, after a typed line, the page plays that line's run from its first hit at the speed, from the choices offered, that takes about twenty seconds (never faster than 600 hits a second); while it plays, the run tab's reads wait for the pause. The page only; the brain is untouched.
