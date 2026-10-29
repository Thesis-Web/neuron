# 20. The full sources: WordNet 3.1, GCIDE 0.54, Moby Thesaurus in place of the 172-word slice (2026-10-29)

**Status: done on the live v6 brain behind the 8056 door this morning, at the owner's word ("wordnet 3.1, gcide, and moby are a go"); the owner's rule: a define is trusted with two sources, better three.**

The slice (sat172.json, fetched 10-22) held 130 to 344 headwords per source, so most words came back with known and unknown empty. The three free, complete dictionaries were downloaded, laid as source brains in the shape make_sources.py laid the slice (me, corpus, inbox, outbox, the work and carry triggers), and their rows were put into the live source files wn.db, gcide.db and moby.db in place of the slice rows, keeping each file, its gate (7, 8, 11) and its triggers, so the door's attachments stayed as they were. mw, mwt, map, sqldoc, measured and guess are untouched.

| Source | Downloaded from | sha256 (first 16) | Lines laid | Headwords | Shape of a line |
|---|---|---|---|---|---|
| wn | wordnetcode.princeton.edu/wn3.1.dict.tar.gz (16.4 MB) | 3f7d8be8ef6ecc71 | 139,118 | 83,253 | one line per synset: the gloss, then [syn: {lemma}, {lemma}] as dict.org prints it; a row for every single-word lemma, lowercased |
| gcide | ftp.gnu.org/gnu/gcide/gcide-0.54.tar.xz (14.8 MB) | 22416f6f36175b16 | 179,888 | 110,568 | one line per definition (the def element), tags stripped; a row for each headword of the entry, lowercased |
| moby | gutenberg.org/files/3202/files/mthesaur.txt (24.9 MB) | 7c9742b1ed94435a | 2,520,254 | 30,259 | one line "like X" per synonym of a root, as the slice shaped the thesaurus lines and as define's relationship rule reads them |

What is mine, labelled: GCIDE's quotations, etymologies and pronunciations are left out (the owner's 10-22 measurement: they inflate the counts; they are not the description of the action). In GCIDE's prefix lists (Un-, Re-), where a thousand headwords sit under one entry, only the prefix takes the definitions. WordNet's multi-word lemmas get no row of their own (the brain asks with one symbol). Lowercasing the headword: the brain's symbols are case-sensitive, so define : WHO finds nothing.

Measured on a copy of the live brain after the load: `define : ask` 17.9 s, 419 runs, 20,925 hits, 139 born, 111 returns (wn 7, gcide 8, moby 96), known 24 symbols, unknown 217. With the slice a define took 4.7 to 9.7 s. Moby's size is the cost: a root averages 83 synonyms, do has 397, say 436, set 1,151, each a return run.

Files: `build_sources.py` (lays the three from the downloads), `load_live.py` (puts a built corpus into a live source file in chunks), `sources/` (the three as built). The downloads themselves are not archived; the URLs and checksums above fetch them again.

Also this morning, before the load: ATTACH tested through mother on SQLite 3.37.2, on a scratch database: it runs typed at the prompt, inside a trigger, and as a hop row the brain writes; the attachment lives on the connection and is gone after the door restarts. The Wiktionary extract (kaikki.org, 3.4 GB, 1,499,161 entries) is downloaded to the session scratchpad and not yet laid as a source; it would be a ninth source and needs the attach lines and a new ask, which are the owner's to type.
