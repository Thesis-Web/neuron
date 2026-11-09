# tries/53 (2026-11-04, 04:50 CST): the state at the end, read live

| What | Read |
|---|---|
| the patched binary | `hp:~/nk-c27/nk`, built 04:44 from copies of the live sources with two changes: nk.c 112 `is_letter` gains `c >= 0x80`; nkio.c 121 and 211 lose the 160 and 300 limits (1 << 30). The run's own text fields (400, 120, 100) kept |
| the test, on port 7009, in `~/nk-c27` with its own fresh brain file (`test-7009-hp.txt`) | 86 symbols laid; `type main the word abligurrītiō stands here with tiō and h₂epó` → run 1, born 13; `label`: abligurrītiō gate 89 (length 12), tiō gate 93 (3), h₂epó gate 95 (5); ti and ō: no gate. A 454-character line → run 2; its me cell read back with text length 454, no cut mark; the root text field 408 bytes (the 400 limit kept on purpose). The test kernel was left running by my first stop line (a pgrep pattern that matched the shell itself, the tries/50 trap) and stopped at 04:52 by its exact pid 355497; the live kernel never touched |
| the live kernel and door | untouched: nk pid 324376 (the binary of 11-02 20:23), serve8.py pid 349085, `/api/info` ready. The patches are laid in `~/nk/nk.c` and `~/nk/nkio.c` with `nk.c.before-c27` and `nkio.c.before-c27` beside them; `bash run-on-hp.sh up` (stop, build, start the kernel and the door) is the owner's word |
| the hub | untouched |
| the Cortex | C26 done (accepted on the owner's word of 04:30, quoted); C27 working with the test receipt and three sentences; C28 open (the cell parser retired, outlined with its cost, not built); the owner's words of 04:30 typed in the owner voice |

## The restart, on the owner's word ("you can do the restart", 05:00), read live (`restart-hp.txt`, `after-restart-hp.txt`)

| What | Read |
|---|---|
| before, 05:03:15 | ready, runs 19,939,022, defined 722,299, refused 1, gates 1,317,489; nk pid 324376 (binary of 11-02 20:23), serve8.py pid 349085 |
| `bash run-on-hp.sh up`, 05:03:17 | stop, build, start: 6.114 s real; "nk: 1317489 symbols laid in each brain, listening on 127.0.0.1:7007"; the door up |
| after, 05:03:23 to 05:03:54 | nk pid 355944 (binary of 11-04 05:03), serve8.py pid 355951; ready, runs 19,939,022 then 19,939,067 a second later (the sixth's cascade on), defined 722,299, refused 1, gates 1,317,489 then 1,317,492: the brain came back as it stopped |
| `define : spend` (run 19939023) | 0.207 s, 0 refused; the say cell run 19939037, text length 1,796, no cut mark (before the restart a say was read back at 301) |
| a line with abligurrītiō, tiō and h₂epó (run 19939039) | 3 born, 0 refused; label: abligurrītiō gate 1317490 (length 12), tiō 1317491 (3), h₂epó 1317492 (5); the old pieces ti 4923 and ō 241 stay as gates; the line's symbols: the, word, abligurrītiō, stands, here, with, tiō, and, h₂epó, with the spaces |
| the door's open set | rebuilt at the start: 721 roots, 84,861 receipts (it was 2,367 and 102,967 in the old door process; the set is the door's cache of the newest lines) |
| the owner's tab | needs a reload (the door's ids count from 1 again) |
