# What the headless check found, 2026-10-26 (hub, Chromium 156 headless, DevTools protocol)

The door: `python3 serve18.py` on `tries/11/NEURON-v18-CORE-2026-10-25/brain18.db` (Python 3.10.12, SQLite 3.37.2), port 8018. The drivers: `cdp-check-2026-10-26.js`, then `cdp-check-2-2026-10-26.js` after two CSS fixes. Each line below is what the driver printed, trimmed.

## The door alone (curl, before the page)
- `/api/info` ready 2 s after start; `/api/q` `SELECT n FROM shards` gave 4665; `DELETE FROM label` refused ("only a SELECT is read through this door").
- `/api/dna?since=0`: 4,665 DNA rows and 61 definition rows over 2,004 tables in 0.075 s.
- `BUILD SELECT 1 + 1 BUILD` said `2` in 0.02 s; `define : dog` said the Webster 1913 line (as RESULTS-v18.md T5/T6).
- `/api/save` onto the loaded file refused.

## The page on the tested brain
- ready: true; counts {shards 4665, tables 2019, views 1002, triggers 1015, indexes 5, receipts 1181219, sheet 10258, hop 0, bindq 1, label 2004, input 998, run 997}; 2,004 nodes, 4,612 springs.
- opened on the newest line's root, run 995 (`define : Canis`, 5 hops).
- tabs: clicking step and neurons hid type and showed step and neurons.
- two hops forward: t 2, "hop 2 of 4 · run 995 · : (gate 279) · shard 913 · arrived from ␣, remainder ␣".
- play for 4 s: went on into run 996 (formula define, 694 hops), t 22.
- neurons, find "dog": 20 shown; click gate 293: the selected tab opened; "dog gate 293 · born by the born run · born row 60, in run 65 (formula define) of the line "define : dog" · its definition node is gate 294"; 9 DNA rows (904 ∅ ∅ → dog.definition 294; then ␣ → ␣, ", }, ;, ., -, ,; 3980 ␣ → end); definition node g294: 32 rows, best first: gcide 5.482 run 173 "(Zool.) A quadruped of the genus {Canis}…", gcide 4.441 run 325, wn 3.911 run 68; gate trigger: `CREATE TRIGGER gate_293 INSTEAD OF INSERT ON land_293 BEGIN SELECT motherp(…`.
- run 65 (formula define, parent 64, root 64, 694 hops, receipt rows 78047 to 973909): cells run 65, after " : dog", subject null, what dog, BUILD ok (×6), dna g293, def g294, first 173, say "(Zool.) A quadruped…"; between the BUILDs: `INSERT INTO sheet ( run , name , value ) SELECT var run , 'what' , trim ( ltrim ( trim ( value ) , ':' ) ) FROM sheet WHERE run = var run AND name = 'after'` → mother said ok, and the next pairs; fire 61 fires born subject 60, fire 62 fires source subject 293, born 60 "dog" then looked up in the sources, build 120 at receipt row 78133, …
- typed `define : cat` through the page: done in 2.6 s, said "any of a family (Felidae) of carnivorous usually solitary and nocturnal mammals (such as the domestic cat, lion, tiger, leopard, jaguar, cougar, wildcat, lynx, and cheetah)"; counts after: receipts 1181918, sheet 10273, input 1000, run 999; the page chose run 998 (694 hops).
- lines list: the teaching lines show "a teaching run: a formula row points at run 1 / 2 / 53"; `define : -> define` shows "a bind: no run; it went to bindq and set a trigger column".
- brain tab: hop_go's SQL read from sqlite_master; formulas born → run 1 (1,272 hops), source → run 2 (1,020), define → run 53 (694).
- atlas: 2,004 gates (1 origin, 84 handlaid, 914 born, 3 formula, 1,002 definition); 2,004 rows; detail for bandog (gate 1113): 2 DNA rows, gate_1113's SQL; after the fix the header has all ten columns and the table is 1,174 px wide in a 900 px box (it scrolls sideways, as 17.3's did).
- console: no exception in either run.
- at 420 px wide: document scrollWidth 420 (no sideways scroll).

## A fresh brain (`python3 serve18.py <new path> 8019`)
- the bare core: 174 label rows, 0 formulas, 87 shards, 100 triggers (RESULTS-v18.md T1: 87 neurons, 100 triggers).
- `/api/sheet`: born 0.5 s, source 57.4 s, define 12.3 s, bind 0.0 s; 70.2 s in all; after: 292 label rows, 3 formulas, 900 shards, 159 triggers, 78,034 receipt rows.
- `BUILD SELECT 1 + 1 BUILD` said `2` in 0.007 s.
- no file was written: the brain is saved only on request.

## What the counts say about the hand-laid block
87 words at gates 1 to 173 and none of them has a born row. Of them the page counts 84 as hand-laid, 2 as "with a formula" (born and source: source is a column name in the born line, so it is a hand-laid token) and 1 as origin. define (gate 273) was born by typing.

## The evening look, after the owner's two screenshots (`tests/cdp-check-3-2026-10-26.js`)
The owner's screenshot of the page was 3,787 px wide with the rails stacked under the stage and every letter five times its size. Rendered headless at 757 × 384 CSS px with a device scale of 5 (Chrome's 500% zoom on a 3,787 px window) the page matched that screenshot; at 3,787 × 1,918 at scale 1 the grid was three columns (290 px, stage, 410 px). The stacking is 17.3's own rule at 900 px. So that picture was the browser's zoom for localhost, not the page.

The start graph, measured through `__poc.positions()` on the tested brain:
- 2,004 points, a solid ball: radius from origin r50 88, r95 114, max 126 drawing units; centroid at 0.5, 0.8, −3.8; one point at origin.
- the DNA rows give 8,251 lines (3,655 arrival, 3,594 remainder, 1,002 trigger); 5,580 of them touch the space neuron (gate 11), 1,528 the comma; only 4 join two words with neither a space nor a punctuation mark at an end. The trigger lines each point at a different definition node.
- with the space neuron's lines on: 4,612 springs; off: 2,680.
- before the fix, at 3,787 px wide 4 s after opening, the view sat inside the ball (lines to every edge). After the fix (the view follows the radius until it holds still; the space neuron's lines start off): at 3 s and at 12 s r95 115 and the ball inside the view with dark space around it; at 1,900 px the same. No console exception.
