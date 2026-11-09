# tries/54 (2026-11-04, 06:45 CST): the state at the end, read live

| What | Read |
|---|---|
| the restart (06:27:59) | `bash run-on-hp.sh up` 6.2 s; nk pid 369308, door 369315; runs 19,939,072, defined 722,299, refused 1, gates 1,317,492 equal before and after (`restart-and-relabel-hp.txt`) |
| the back population (`relabel`, 06:28:08 to about 06:34) | the request's socket timed out at 120 s while the kernel ran the pass single-threaded, in disk wait (state D, 43 % CPU, 11 GB read in three minutes: the source rows read by rowid from the Wiktionary and GCIDE files); the door answered again at about 06:34; gates 1,317,492 → 1,788,888: 471,396 symbols born for the held rows; the print of the pass itself (points, texts, seconds) was lost with the socket |
| its effect (`after-relabel-and-merge-hp.txt`) | `define : abligurition` (0.226 s): suffix 10547 = 1317491 tiō, prefix ab, the etymology whole (h₂epó, abligurrītiō). `define : spend` (0.419 s): 68 etymology gates, among them h₁éǵʰ, h₁éǵʰs, péndeti, pendō, expendōbor, and also spend”, consume”, provide”, dedicate”: the first letter rule (any byte at or above 0x80) glued the closing quote to the word |
| the letter rule corrected (`test-7009-letters-2-hp.txt`) | `letter_len`: a character of another script continues a word unless it is punctuation (U+0080-00BF, U+2000-206F); on the test kernel: “ to … squander ” cut apart, ab ‧ lig ‧ u ‧ rit ‧ ion apart at the hyphenation points, naïve café h₂epó tiō whole. Built in `~/nk-c27`; not yet live (the third restart and a second pass wait on the door being free) |
| the merge (`merge-reply-hp.txt`, `merge-2-hp.txt`) | MERGE-nk.txt typed (run 19939969, 0.537 s, 0 refused): 55 pairs merged, each "shards N moved, 0 kept by the twin, node rows 0 ..." (BEGIN, DEFAULT, TEXT, TRIGGER moved one shard each); MERGE-2-nk.txt for the three left by the source condition: INSERT 81 → insert 10441 (node rows 19, memories 2), DROP 1788891 → drop 1547 (12 rows, 1 shard), DELETE 917750 → delete 22293 (13 rows, 1 shard). After: `label` reads SELECT as 17434, INSERT as 10441, TABLE 410, INTEGER 26685, GROUP 186, TEXT 450; neuron 98 born 0; a new `BUILD SELECT count ( * ) FROM ranks ; BUILD` encodes select, count, from and answers 15; `define : who` 0.186 s, the same def |
| the kernel | pid 369308 (the C27+C28 binary), ready, runs about 19,944,xxx, refused 1 |
| the Cortex | C27 with the after-relabel receipt; C28 with the twins read and the merge replies; C22 working with the trials and the check |

## The third restart and the second pass (06:53), read live (`restart-3-hp.txt`)

| What | Read |
|---|---|
| before, 06:53:40 | ready, runs 19,948,277, defined 722,323, refused 1, gates 1,788,920 |
| `bash run-on-hp.sh up` with `letter_len` | 7.376 s; nk pid 388398, door 388407; the same four counts after |
| the second `relabel` | started 06:53:50 in the background, its print kept in `hp:~/nk-c27/relabel-2.log`; the door blocked while it ran (state D) |
| the second pass, its own print (`relabel-2.log`) | points 722,320; node rows 4,849,757; texts 4,835,342; missing 14,415 (rows with no source row to re-read: the guesser's and the repaired); labels 1,788,920 → 1,790,817, 1,897 born; 232.9 s; the door answered at 06:57:43; gates 1,790,817, refused 1, heap 14 MB |
