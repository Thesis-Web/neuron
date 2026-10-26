---
name: project_neuron_poc167_20261024
description: Turn 20 (2026-10-24) Point Of Connection 16.7 = 16.4 + pull layout; owner's opposite pairs, new actions, share-mark formula (owner's way), measured physics actions; held-out results; where it lives
metadata:
  type: project
---
Owner messages 10-21 (verbatim in turn16/OWNER-VERBATIM.txt inside Downloads NEURON-v16.7-SOURCES-2026-10-24.tar.gz):
- **Shared lines:** "can a line pull two relationships?"
- **Missing pulls:** state/time/memory; perspectives who/what/when/where/how/why; delete/erase as a 15th action; diff; DIVIDE MULTIPLY EQUAL INEQUALITY COPY CUT; call/send.
- **Opposite pairs:** pairs go on opposite lines: hear/say, split/join, subtract/add, read/write, find/move?, compare/diff?, delete/spawn?, clock/?, tense past/present/future.
- **Confusion:** "I don't understand near:"; are the percentages invented?
- **Restore:** 16.6 lacked the prompt and premade runs ("add them back").
- **Share marks:** each line pulls the word toward the mark at its share.
- **Proposal:** 15 SQL actions + 15 memory/state/timeline actions; "what is the action when nouns reflect on memories first?"; relationship names unclear.

Facts:
- **16.7 is the 16.4 page patched** (poc/make167.py). The 16.4 sources were first rebuilt byte-identical (sha 2c3095c05033).
- **Layout switch "place points by":**
  - pulls: sum (default);
  - pulls: toward share marks, place = sum share^2 x direction;
  - springs (16.4).
- **Points:** brain points in the map are placed by pulls. Others sit where their brain lines balance (average of the points they are tied to). 29 have nothing (13 SQL words the map lacks, the 6 sources, the SQL prompt, var, what, how, where, this, that, without, definition, thesaurus, retry). Origin is told at 0,0,0; its own pulls would put it at 3.0, -0.8, 4.4.
- **Browser test:** prompt, 15 premade runs and a typed line all work; page places match Python exactly.
- **Data:**
  - who/what/when/where/how have ZERO lines in the owner's map (why 2, perspective 2); WordNet lacks what/when/where/how.
  - Map opposite lines: subtract/add, divide/multiply, past/future, find/lose, move/stay, delete/add, erase/write, send/receive, copy/original, cut/join, equal/different, differ/agree.
  - "near X" pulls (closeness) are nearly the same for every word: 78% of words have no pull above 10% of their total.
- **Held-out mean rank share:**
  - owner's pairs layout 0.193;
  - relationships + actions 0.162;
  - 14 actions 0.196;
  - six named pulls (16.5) 0.102, still best.
- **Pair sides** (words closer to one end on that end's side): past/present 99%, delete/spawn 78%, inequality/equal 78%, read/write 72%, hear/say 72%, copy/cut 71%, add/subtract 65%, move/find 61%, split/join 51%, call/send 42%, divide/multiply 21%.
- **Share-mark formula** (sampled, rescaled): pairs 0.428, B 0.182, C 0.183, D 0.135, against the sum 0.181/0.152/0.174/0.090. It needs per-word shares that differ; closeness pulls are flat.
- **Physics measured** (v16 told block, 110 triggers):
  - SQL side: = 656, SELECT 536, || 407, INSERT 183, trim 109, NOT EXISTS 87, coalesce 77, instr 74, substr 57, max 56, UPDATE 38, > 33, - 31, + 30, <> 21, ORDER BY 21; x and / never used.
  - Memory side: memory read 15 / written 2 / changed 2, memwrong 1, timeline 2/2, formula read 18, var written 13, encoder read 81, DNA rows laid 75, receipt read 17, gap 8.
- **Told SQL words** include = * < > DELETE UPDATE, not / <> != EXCEPT. DELETE, DIFF (NOT EXISTS) and UPDATE are done by the physics but are not named among the 14 actions: the owner's call.

Where it lives:
- Artifact https://claude.ai/artifact/14L3pxNSuJ81ZzBiLEvSgD.
- Downloads: NEURON-POINT-OF-CONNECTION-v16.7-2026-10-24.html (sha 8190718b9159) and NEURON-v16.7-SOURCES-2026-10-24.tar.gz (README: rebuild).

**Why:** next turns build on 16.7.
**How to apply:**
- Every new version is a patch of 16.7, never a page without the brain.
- The open question is real per-word "what it does" pulls from the brain's runs; the owner may name 15 SQL + 15 memory actions.

Related: [[project_neuron_thirty_pulls_20261024]], [[feedback_known_failures_checklist]].
