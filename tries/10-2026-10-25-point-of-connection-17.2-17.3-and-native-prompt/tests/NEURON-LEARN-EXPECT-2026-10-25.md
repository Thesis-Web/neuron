# learn : X, the first word done the owner's way. Predictions frozen before the run (the builder's, not the owner's)
2026-10-25. Built in a copy (told block 17.2 = 17.1 plus the changes below); ~/neuron/v1 is not touched. Results in a separate file.

## The owner's design (msgs 35-37, 41), in his words
- "learn : dog --- brain learns and build the run, data sheet, meaning of dog"; "define : car .. if car is not a neuron go to source and find and build car from the source process to build a new neuron".
- The answer comes back "as a run to that brain... return from "define : join" from source wordnet ... /build "the definition" <-- as gates... those modifiers lets the brain know that it's information it requested and has been return.. such that it can populate the data sheet for the primary run".

## Told changes (17.2), checked against the builder laws first
1. A source's kept definition row runs as a line headed by modifier gates:
   "return from <the primary line> from <source> /build <the definition's words>"   (the form is my reading of the owner's pseudo code)
   The primary line is the line that brought the word ("learn : store"). The source is named by its own told gate (wn, gcide, ...),
   not by the word "source", because "source" has a formula and would fire the asks again.
2. When such a return run ends, its own trigger:
   - writes the word's definition memory: a memory row for the return run (its gates, its receipt), marked "definition from <source>";
     the source is read from the run's own receipt (the one source gate it passed), no new column;
   - fills the primary run's data sheet: a cell in the primary run named "<source> <word>" whose value is that memory row's id
     (a pointer, not text).
   Law check: 1 inside the brain (triggers); 2 new physics, the owner's call (it cannot be built from formulas: a trigger is needed
   to act when a return run ends); 4 the header words are the owner's modifiers, not a reply; 5 every definition comes from a
   source; 8 this file comes first; 13 the hop is not changed.
3. Source data: dog was in no stand-in source. Its WordNet, Webster 1913 (GCIDE) and Moby thesaurus entries are fetched from
   dict.org into those stand-ins, one row per sense, in the stand-ins' own row format (not told; a source's corpus).

## Predictions
L1. "learn : store": store is born and asked of all 8 sources. wn, gcide, mw, mwt, moby and map answer (17 rows held: 2, 1, 2, 6, 3, 3);
    sqldoc and measured answer nothing. The first 8 kept definition rows (in arrival order: wn 2, gcide 1, mw 2, mwt 3) run as
    return runs, each starting "return from learn : store from <source> /build". 8 memory rows marked "definition from <source>";
    8 cells in the primary run's data sheet pointing at them; moby and map's rows are held but never run (the told LIMIT 8).
L2. The primary run says no answer (no taught word replies): its output is the line back with "?" on the words with no meaning.
L3. "learn : dog" after the fetch: the same, with the sources that hold dog (wn, gcide, moby): at most 8 return runs and memories.
L4. Controls: (a) a word no source holds ("learn : zork") makes no return run, no definition memory and no cell; gaps say what
    came back empty; (b) with 17.1's told block (no change 1 and 2), "learn : store" makes defrow runs without the header, and no
    definition memory and no data-sheet cell.
L5. Nothing in the return runs fires the define or place formulas (they are not taught in this brain); the told source formula
    does not fire inside a return run (the header avoids the word "source").
