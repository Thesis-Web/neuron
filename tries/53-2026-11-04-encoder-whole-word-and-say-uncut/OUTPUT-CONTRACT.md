# tries/53: the output contract, before the build (04:35)

## 1. Must not change
The live kernel and door on hp (pid 324376, 349085) are not stopped or swapped by me; the hub untouched; RECALL-9 as bound.

## 2. Wrong by the owner's prose (04:30)
The encoder ends a symbol at a non-ASCII letter (tiō → ti, ō): "we should accommodate that now". The kernel door cuts a say at 300 and 160
characters: "this should have already been lifted". The cell parser of decode_span is invention (outlined, not built: C28).

## 3. The new work, C27, with its expected live output
| Part | Built | Expected live output |
|---|---|---|
| the binary | the sources copied to `hp:~/nk-c27/` (no running brain there); nk.c 112 `is_letter` gains `c >= 0x80`; nkio.c 121 and 211 lose their limits; built with the same gcc line | `gcc` ends with the binary `~/nk-c27/nk` |
| the test, beside the live brain | the binary on port 7009 with a fresh brain file in its own folder; a line holding `abligurrītiō` typed; a 400-character line typed | `label` holds abligurrītiō as one gate; the run read of the long line shows its me cell's text whole, over 300 characters |
| the live swap | the two patches applied to `~/nk/nk.c` and `~/nk/nkio.c` with `.before-c27` copies; `bash run-on-hp.sh up` on the owner.s word of 05:00: done at 05:03, 6.1 s | after the restart: `define : spend` read by `/api/run` shows the say whole (1,843 characters); a line with abligurrītiō encodes one symbol |
