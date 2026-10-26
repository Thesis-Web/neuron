---
name: project_neuron_six_pulls_20261023
description: "Turn 18 (2026-10-23) Six Pulls test - owner's idea x = pull(+x) - pull(-x) on the owner's relation map; 7 graphs scored on held-back lines; no graph met the pre-set bar; named pulls + 3 diagonal pulls best (0.085); opposite = same place except the signed graph; page v16.5 + sources in Downloads"
metadata:
  node_type: memory
  type: project
  originSessionId: 7c20c611-9fe3-4487-be20-478341fdbaa9
  modified: 2026-10-24T03:23:10.170Z
---

Owner message 5 (10-23, verbatim in turn16/OWNER-VERBATIM.txt): "the sqlite is a vector graph data 3d data base.. how on earth can the gates ... not have x,y,z"; the cap "can't be correct you are putting limits on the shape of the graph"; find "a 6 pull graph that actually makes sense... an equation, formula, function, log rhythm that... points out every relationship"; +x/-x etc.; bisects (two-axis, three-axis, "4 axis"). Message 6 after a Windows crash (7:56 PM, 0x7E, dxgmms2.sys named) wiped /tmp: "rebuild what you were working on, and let's get it done."

Facts given to the owner:
- **x,y,z:** SQLite stores rows and columns only. v1's egg.sql gate tables have shard, arrival, remainder, trigger, run, pos; no x,y,z. My v16 pages also kept positions only in the page.
- **Closest earlier build:** the 10-03 build (my notes in ~/.claude/projects/-home-exnulla/memory/neuron_xyz_space.md; its files are gone from disk) stored a point as six whole numbers (x+ x- y+ y- z+ z-), with opposite = swap. The owner hypothesised on 10-17 a "fixed overlay graph of simplest expressions, gates move by relationships"; "3D not Nd".
- **Data:** the owner's relation map 2026-10-08, merged to one point per spelling: 27,606 words and 9 kinds. Lines split 70/15/15 build/choose/test. WordNet 2025 lines used only as a check.
- **Score:** rank share. A formula per kind (same, shift, flips, through origin, scale, linear) is fitted on build lines and chosen on choose lines. The score is the share of words closer to the formula's point than the real word: 0 = closest, 0.5 = chance. "Points out" = share < 0.25, hit@10 >= 0.3% and shuffled control >= 0.45. "Makes sense" bar = 7 of 9 map kinds and 3 of 5 WordNet kinds.
- **Results (test mean / map kinds pointed out / WordNet kinds pointed out):**
  - named pulls + 3 diagonal pulls 0.085 / 3 / 3
  - named pulls 0.102 / 3 / 1
  - places fitted to lines 0.116 / 6 / 3 (not a true ceiling)
  - found NMF six 0.127 / 3 / 1
  - signed eigenvectors 0.269 / 1 / 0
  - 14 actions 0.279 / 3 / 0
  - eigenvectors 0.390 / 1 / 0

  No graph met the bar.
- **Winning named pulls:** +x in WordNet, -x reach of write; +y noun, -y adjective; +z adverb share, -z reach of hear. These are class and connectedness pulls, not tense, mood or memory. Reach pulls largely overlap (median rank correlation 0.63). On x, 20,187 words are pulled both ways (the owner's "x,-x,y,z" bisect: x cancels).
- **Opposite:** "same place" is best except in the signed graph (there through origin wins 0.216, pairs across 0 on 56-73% vs 41-49% chance). Through origin elsewhere scores 0.49-0.89.
- **Diagonal pulls kept (all three-axis):** reach of modifier on +x,-y,+z; is a part on -x,-y,+z; is an affix on -x,+y,-z. They improved test 17%. There is no consistent relation to their own main axes.
- **Distance from 0,0,0 vs WordNet depth:** rank correlation 0.41 (named), 0.53 (NMF), 0.36 (fitted). General words sit nearer origin.
- **Other checks:** the 14 actions cluster (0.52x random spread). The word origin never lands at 0,0,0.
- **Wrong predictions:** found pulls beat named (reverse); diagonals < 10% (17%); actions apart (they cluster); fitted placement meets bar (6/9).

Where it lives:
- Artifact https://claude.ai/artifact/Ab1Xhb1VsJ3tXRVA4VKDHi.
- Downloads: NEURON-SIX-PULLS-v16.5-2026-10-23.html (sha 561baa7569ed) and NEURON-v16.5-SOURCES-2026-10-23.tar.gz. The archive holds turn18 scripts, EXPECT18.md, MY-NUMBERS.md, final18.json, the search jsons and the updated OWNER-VERBATIM; its README has the rebuild commands and the WordNet URL and sha.

**Why:** the owner judges the graph by whether places mean something; these are the measured answers.
**How to apply:** build on final18.json, never re-tune toward a look. The next steps the owner may pick:
- pulls from the brain's own rows;
- six numbers per gate as a view;
- the signed graph for opposites.

Related: [[project_neuron_v16_results_20261023]], [[feedback_known_failures_checklist]], [[project_neuron_owner_design_20261023]].
