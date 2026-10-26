---
name: project_neuron_poc169_20261024
description: Turn 22 (2026-10-24) Point Of Connection 16.9 - why write sat off its line (closeness crossed opposite lines), two-sided closeness, stacked-at-origin causes, order re-search overfit, held-out trade-off, the pasted anchor-experiment advice
metadata:
  type: project
---
Owner messages 23-26 (verbatim in turn16/OWNER-VERBATIM.txt, inside Downloads NEURON-v16.9-SOURCES-2026-10-24.tar.gz):
- "the word write is not pulled anywhere near the pull line write"; update not near write;
- "things are not being pulled ... in the correct directions ... or the axis order is mixed up";
- "still a bunch of words stacked on origin";
- a pasted reply from another model (26 rays; behavior-based dimensions; operational anchors such as SELECT INSERT CREATE DELETE; frozen predictions; scrambled controls; transfer test): "maybe this might help us???"

Measured:
- **Why write sat off its line.** Closeness spread through opposite lines, so each action word was close to its own opposite, whose line cancelled half its pull. In 16.8, add sat 74 deg off its line.
- **Fixes compared** (share marks):

  | Closeness | at 0,0,0 | angle (median) | add | held-out |
  |---|---|---|---|---|
  | skip opposite lines | 292 | 8 | 2 | sampled 0.285 |
  | two-sided (opposite lines flip the side), re-ordered | 152 | 15 | 17 | 0.329 (sum 0.321) |
  | 16.8 | 153 | 12 | 74 | 0.276 |

  The re-searched order's sampled 0.269 did not hold on held-out: it overfit, as in #51.
- **The trade-off:** action words on their lines vs the map's own alike/is/has lines.
- **Stacked at origin:** 152 island words (166 in small components never joined to the main body); 140 more only when opposite lines are skipped.
- **Origin** with correct pulls sits out along "beginning" (its map meaning). Its center must be told.
- **update** has no line, and its map lines (modernize, refresh) don't tie it to write.

Where it lives:
- 16.9 = 16.8 + make169.py (closeness switch).
- Artifact https://claude.ai/artifact/FFMoNrSYyPM5c246xny4nM.
- Downloads: NEURON-POINT-OF-CONNECTION-v16.9-2026-10-24.html (sha d61c484293aa) and NEURON-v16.9-SOURCES-2026-10-24.tar.gz.

**How to apply:**
- The next step proposed to the owner is the anchor experiment: measured behavior profiles of the brain's own told words from the physics, predictions frozen, pulls from behavior, scrambled controls, transfer test.
- Don't keep tuning closeness on map words.

Related: [[project_neuron_poc168_20261024]].
