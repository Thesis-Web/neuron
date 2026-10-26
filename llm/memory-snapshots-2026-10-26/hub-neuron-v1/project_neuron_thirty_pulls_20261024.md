---
name: project_neuron_thirty_pulls_20261024
description: Turn 19 (2026-10-24) Thirty Pulls - owner's model: every word starts at 0,0,0 and is pulled along 30 lines (6 axes, 12 two-axis, 8 three-axis, 4 quads); place = sum strength x direction; held-out results; SQLite computes the places; page v16.6 + sources in Downloads
metadata:
  type: project
---
Owner messages 7-9 (verbatim in turn16/OWNER-VERBATIM.txt, inside Downloads NEURON-v16.6-SOURCES-2026-10-24.tar.gz):
- "the neurons all start at origin and are pulled away by their relationships further away the stronger the pull in that direction"
- 30 pulls on 6 axes + 12 bisects + 8 triangular + 4 quads, "relationships, actions, tense, defintions, suffix, prefix"
- all pull lines visible but "very faint... just barely"
- "change each pull by substitution"; "a ratio of the various pulls to the neuron" = meaning
- "radiations" = neurons with only 1-2 relationships
- "the only word with zero pull is origin... the sum of their pull cancels"
- "if something has no pull ... how is it even a point on the graph"
- my line "SQLite ... has no built-in 3D" contradicted ~30 days of saying it can do 3D vector graphs

Answers and facts:
- **SQLite and 3D.** SQLite can hold and compute the 3D graph. In a scratch db, a view over pull(word, slot, strength) and dir(slot, ux, uy, uz) gave the numpy places exactly (diff 0.0) for 27,333 words in 0.2 s. R*Tree 3D index: 1 ms near-queries. sql.js 3.39.3 (the brain pages' engine) computes the same view (3.5 s) but has no rtree module. My "no built-in 3D" was misleading: what is missing is position columns in our brain's tables, not SQLite ability.
- **Quads.** In 3D +z and -z cancel inside a quad, so the 4 quads lie on the 4 flat bisects. There are 26 distinct directions; the 30 slots are kept, with quads labelled further out on the shared lines.
- **Held-out mean rank share (0 best, 0.5 chance):**
  - best 30 found (greedy over 106 pulls) 0.111 (sampled choose score 0.068: overfit)
  - relationships + actions (16 relationship pulls + 14 actions) 0.162: 0 words at 0,0,0, 149 with 2 or fewer pulls
  - fourteen actions on their own lines 0.196 (six of them on the axes in v16.5: 0.279)
  - six named pulls (v16.5) 0.102, still best
  - same pulls shuffled 0.432
- **Ratios are nearly flat with reach pulls.** Sluggish is about 10% alike lines + 7% MOVE + 7% opposite lines...; MOVE is its largest action pull in both action starts.
- **Origin** never at 0,0,0 (57-64% of words sit nearer).
- **Map lines.** 10,197 of 27,606 words (37%) have only 1-2 lines and 5,875 have one kind of line: the owner's "relationships not filled out".
- **Why v16.5 had words at 0,0,0:** scored pulls used 70% of lines (1,783 words had all lines held back). Here every word's pulls come from all lines; 0,0,0 only when no pull in use touches it (best-30: 273; actions: 169 island words; relationships + actions: 0).

Where it lives:
- Artifact https://claude.ai/artifact/4Lfoq3EkHJ4wCRW4dr4uuk.
- Downloads: NEURON-THIRTY-PULLS-v16.6-2026-10-24.html (sha 978c69a38e6d) and NEURON-v16.6-SOURCES-2026-10-24.tar.gz (README has rebuild commands; needs the v16.5 tarball's turn18).
- Page defaults: guide lines at opacity 0.14; it opens on relationships + actions.

**Why:** the owner's next step is substituting pulls by hand on this page.
**How to apply:**
- Keep scores held-out.
- Don't present the sampled choose score as a result.
- When the owner wants it in the brain, offer pull rows + a place view (give the SQL as text; owner pastes).

Related: [[project_neuron_six_pulls_20261023]], [[feedback_known_failures_checklist]].
