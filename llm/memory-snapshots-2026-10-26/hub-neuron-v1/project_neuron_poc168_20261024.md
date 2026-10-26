---
name: project_neuron_poc168_20261024
description: Turn 21 (2026-10-24) Point Of Connection 16.8 - bare core view, above-average strength, balanced pairs (beginning/end), origin diagnosis, modifier effects measured, SQL doc meanings proposed, call/mother facts
metadata:
  type: project
---
Owner message 22 (verbatim in turn16/OWNER-VERBATIM.txt, inside Downloads NEURON-v16.8-SOURCES-2026-10-24.tar.gz) asked about:
- modifiers by what they do;
- operators (and, or, but, is, are, as);
- a bare core brain;
- origin as the one known place, so fix what's wrong with the pulls;
- SQL meanings are known and should be populated, not guessed;
- < and > as separate points; != ; cut text vs rows;
- call / receive, and whether JS or the graph runs it.

Measured:
- **Origin.**
  - Closeness pulls are not specific: origin, like every word, got 18-44% of every action.
  - An unpaired line pushes everything: CLOCK alone moved origin +2.6 x.
  - In the map, origin = alike ancestry, beginning, genesis, inception, provenance, source; opposite end.
  - Fix F1 (count only a pull's part above the word's own average) puts the action words 12 deg from their own lines with share marks (58 before). Ratios become specific: read = READ 77%; sluggish = MOVE 26 / INEQUALITY 20 / SUBTRACT 17.
  - Beginning / end on opposite lines brings origin from 1.07 to 0.53x a typical word's distance (its pulls: beginning 39%, end 34%).
  - Cost: held-out mean on map lines worsens. Balanced start: 0.276 share marks, 0.266 sum. Six named pulls are still best at 0.102.
- **Modifiers** (turn21/out/affix21.json):
  - -ly adj->adv 66%; -ful/-less noun|verb->adj; -able verb->adj 59%; -ness adj->noun 45%; -or verb->noun 6/6; un-/in-/dis- keep class, sometimes opposite.
  - Consistency of the move (six named graph): -less 0.96, -ness 0.92, -ful 0.88, -ly 0.86, -able 0.82, -s 0.82 (random 0.01-0.17). Prefixes 0.28-0.44.
  - Map errors: reaches = re+aches, images = im+ages, probed = pro+bed.
  - Absent: -sion, -ible, 's, s', be-, con-, com-.
- **Function words:** almost no lines (but/as/of 0; "or" merged with suffix -or). AND OR NOT IS AS are told SQL words.
- **mother:** v1 mother.c runs the SQL and returns only 'ok'/'error: ...' (no rows back). The page's JS mother returns rows into secondary input; sources go inbox -> own trigger -> outbox -> pickup -> secondary input.
- **SQL doc meanings table** (SELECT read, INSERT write, ... <> and != = not equal, < > separate, substr cut, instr find, || join text, EXCEPT diff): in the 16.8 notes for the owner's OK, NOT told.

Where it lives:
- 16.8 = 16.7 + make168.py patches.
- Artifact https://claude.ai/artifact/YK3kx7RPaMjdhWpjXqiDgg.
- Downloads: NEURON-POINT-OF-CONNECTION-v16.8-2026-10-24.html (sha f5ce9b920dd8) and NEURON-v16.8-SOURCES-2026-10-24.tar.gz.

**Why / how to apply:**
- Next: if the owner OKs the SQL table, give the told rows as text.
- Real "what a word does" pulls need runs.
- Keep every version a patch of the last working page.

Related: [[project_neuron_poc167_20261024]].
