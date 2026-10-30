# tries/29 (2026-10-30): copy P, the twin of the live brain, stopped at the owner's word

Copy P was a copy of the live v7 brain taken at 00:58 on 2026-10-30 for the hop tests of tries/27, served on the hub's port 8057 by its own serve7 door (door and router in one process, as 8056). Its cascade ran beside the live one until 16:05, when the owner said to stop it ("fine to stop this and move the historical data to the d:/neuron into tries"). It was never the owner's brain; 8056 is.

## What is here

`brain/brain.db` (2.1 GB) and `brain/sixth.db` (287 MB), P's two brains as they stood when stopped; `sources/` the small source files with P's own state (the guesser, the map, the slices); `page/` the door and page it served (the page with the space-between slider at 500 and the door with the history read capped, both written to its folder on disk before it was stopped); `FIRST-RUNS-v6-2026-10-29.txt`. The big dictionaries (WordNet, GCIDE, Moby, the lean Wiktionary) are not copied: they are the same files as the live brain's and as `D:\Neuron-sources\built`. The two brain files are in this folder on D: but kept out of git (`.gitignore`): 2.4 GB of history in the repository would weigh on every clone.

## P against the live brain, measured before it was stopped (tries/28 twins.py, twins2.py, twins3.py)

- Same physics: every trigger in main and in the sixth hashed identical on both brains. Same first 147 typed lines. P then received six more lines, all mine, during the twin tests: `define : only`, `define : across`, `define : word` three times, `define : enough`, `print dna : who`, `define unknown : 1`.
- Their sixths chose the same first 3,605 unknowns to define, in the same order; then they parted for good. Of about 55,000 chosen by each, 24,944 were shared; shared words sat a median of 10,162 places apart in the two orders. P took `mother` at place 3,606; the live brain took it at 6,526 and had 50 of its symbols known by then.
- So the design is deterministic: two brains from the same place with the same lines choose alike until an input differs. What differs after that is path: history (the shared counts, remember, the guesser's belief) decides the order, and the order decides how much a brain knows when it meets a word.
- Both were starving. The mailbox is a stack (the row written last runs first) and the self-feeding sixth pushes faster than the router pops, so the oldest defines never started. At 15:40 the live brain had sent 56,486 defines of which 1,392 had begun and 761 had a definition; P had sent 47,849 of which 3,357 had begun and 1,555 had a definition. The mailbox rows (78,607 and 60,007) are mostly first landings of define runs that each unfold into hundreds of hops.

## State when stopped

P: 207,007 runs, 62,470 gates, 362,783 shards, 19,325 relationship rows, 47,181 unknowns spawned, 147,476 memories, 219 guesses, 9.5 M hops run by its router. Live at the same hour: 242,028 runs, 71,652 gates, 427,194 shards, 33,046 relationship rows.
