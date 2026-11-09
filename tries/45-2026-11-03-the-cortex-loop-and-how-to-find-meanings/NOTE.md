# tries/45 (2026-11-03, 17:40 to 18:50): the Cortex loop, and how to find meanings

The owner, 17:35 (in full in `STATE-BEGIN.md`): the colour question ("on the reload of nk I see white, orange and sand lines, I don't see
any of the others? are they not happening, did I miss them?"), the turn ("once points are defined and have relationships, we should be
moving into finding meanings for each dna shard... mathematical... adding, subtracting, dividing, rooting, exponentially expressing them to
form formulas for other meanings... state and time"), and the task for two hours ("complete what the cortex says is next, update the cortex
on how to find meanings, add sources if needed... sources are not your summaries, they are from reference books... if you complete a step,
just go back to cortex and get another").

## The colours: what the kernel's runs hold (`survey_kinds.py` on hp, the newest 40 typed lines)

365 runs: 40 typed lines (white); 84 called runs whose text is `BUILD INSERT OR REPLACE INTO run_sheet ...` (state and time, amber); 231
called runs whose text is a return with no statement (`ok`, a source's returned text: orange). Ten returns quoted a statement inside their
text (the SQLite docs and the measured source: "The second form of the INSERT statement contains a SELECT statement", "INSERT INTO t
VALUES (4, 'w')") and were coloured as reads and writes, the sand lines the owner saw: `page_patch13.py` colours a branch run only when
BUILD or a statement word is in its first two hops (hop 0 of a called run is its arrival gate, found when the first form of the test
coloured the sheet write orange). So the owner missed nothing: writing a memory, binding a formula, laying a meaning row and a birth are
done by the kernel in C at a run's end, never as hops a receipt walks; on the hub the triggers do the same inside a hop. Those colours will
appear only when such a statement is built between BUILD gates of a line, as the tool lines of the first runs did.

## The loop (the Cortex's DO NOW, then each working checkpoint)

| C | Receipt piped | Sentence judged |
|---|---|---|
| 9 | `cdp_c9.js` (patch13 adds `xyzHeld`, `memNodes`, `relLines` to the handle): ready 9 s, 1,465 visible points, 3,540 springs as lines of 20 kinds, 350 xyz entries for 1,364 loaded gates, 1 memory node for the chosen line and after a click, screenshot in tries/38 | progresses 1.00 by receipt, part added |
| 10 | `keyed_reads.py` on both doors: kernel 1.5 to 19.1 ms a read; the hub (the old door) 30 to 207 ms | progresses 1.00 by receipt (the second sentence, in the receipt's words) |
| 11, 15 | `cdp_stream.js` 20 s of silence: stream live, 0 requests | hallucination by receipt, twice each, though the numbers are in the receipt; left for the owner's mark |
| 12 | `cdp_onehop.js` from `cold water freezes`: 2 runs alive this hop over four presses | hallucination by receipt, twice; the same |
| 16 | `cdp_colors.js`: state and time 8 after the corrected test (the first receipt of 18:1x shows the fault: branch 8) | hallucination by receipt, twice; the same |

The receipt judge: a sentence in my own words with the right numbers was judged hallucination (coverage 0.06); C10 re-typed in the
receipt's printed words passed; C11, C12, C15, C16 re-typed the same way did not. I do not know its rule well enough to say why, and I
did not mark my own sentences (the owner is the checker). This is reported, not hidden.

## C17: finding meanings for each DNA shard (registered, open, the owner's words quoted)

Sources registered (`cortex source`): `owner-meanings-11-03` (owner, six sentences of the 17:35 words); `mikolov-2013-linguistic-regularities`
(reference: six sentences of the abstract, text extracted from the ACL Anthology pdf: "King - Man + Woman results in a vector very close
to Queen"); `mikolov-2013-efficient-estimation` (reference: four sentences of the arXiv abstract); `harris-1954-distributional-structure`
(reference: the encyclopedia's statement of the hypothesis with the citation; the paper itself not read, said so). The plan typed under C17
as six "plan, not built" sentences: a known point is one whose definition and relationship rows came from the sources and whose place is
where they hold it; a shard's meaning is the action its run performs, so an unknown meaning is a formula row not laid; a formula is composed
from known points by the owner's operations over places and pulls and laid as formula rows the brain fires (the shape of tries/35's pull
rows); the reference for adding and subtracting is the vector offset; dividing, rooting and exponentiating have no reference in the Cortex
yet and are the owner's design to state; the sixth tests a composed formula against the sources and marks belief (tries/36), a proven
formula lays its triad (C7), every trial recorded in state and time; a proven meaning becomes a point or group of points with relationship
rows for later formulas. Two questions typed for the owner: what "silicon" names; which points count as known at the start. No formula
was typed into either brain.

## Ready, not live: the two kernel pieces the Cortex says wait on the owner (compiled in a separate folder, never run)

- **C14, the brain's own tension** (`nkxyz_c14_patch.py`, `nkxyz-c14.diff`, 27 lines): at a landing that moved a point, the points its
  relationship rows name, both ways, each take one step by their own pulls (which now see the moved point), at most `NK_TENSION_MAX` of
  them (64), each step a receipt of the timeline of its own (key1 = -other, key2 = pos), so `restep` replays it as it replays every step.
  One round, no decay: the strength per shard and a second round are the owner's formula design.
- **The kernel's own tell** (`nkio_tell_patch.py`, `nkio-tell.diff`, 33 lines): a client that sends the line `tell` is kept open; whenever
  the timeline or the run count grew (after a request, after pending work was pumped) the kernel writes one line `{"clock","runs","tl"}`
  to it without blocking; a client that does not read is dropped. The door's stream thread would hold that client. No timer.
- Both applied to copies in `hp:~/nk-build-test-c14/` and compiled there with the kernel's own build line (`nk.c nkvt.c nkio.c nkmap.c
  nkxyz.c`) into `nk-test` (146,656 bytes, 17:54 by hp's clock); the live kernel (pid 324376, up 21 h) and its brain untouched. To go
  live on the owner's word: apply the two patches to `~/nk`, rebuild, restart the kernel on its file (2 s), restart the door with a tell
  thread (not written yet: the door side is a few lines that connect, send `tell`, read lines and call `tell('kernel')`).

## Also

- The kernel door built the whole-brain bundle on every `/api/q` (585 MB at 17:39); gated behind the bundle's own read prefixes, 22 MB after
  400 keyed reads. A `pkill` pattern that matched the ssh shell killed the door once at 17:45; restarted within the minute.
- The hub survey (newest 40 lines, 356 runs): 40 typed lines, 4 sheet writes (state and time), 312 triggered runs with no statement text
  at all; the same picture as the kernel's.
