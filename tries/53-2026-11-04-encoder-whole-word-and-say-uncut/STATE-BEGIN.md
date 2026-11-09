# tries/53 (2026-11-04, 04:30 CST): the state at the beginning, read live

## The owner's words (04:30)

"decode rule... umm just send it through the encoder??? then secondary input? yes no words in graph... I see this parser as invention, and I
don't clearly see the reason for it? output is decoded on the way out, to mother, input is encoded on way back in from source?"
"cutting the arrays.. seems like hallucination.... this should have already been lifted when we did all the html stuff earlier today???"
"if you are asking for overide because the job is truly completed,, then ok,, if I find out you lied, then I will ask cortex to drop you trust
value even more"
"the tio thing is a problem if this is ever going to be in other languages, so a fix for that should be addressed many other languages use
different chars than english... we should accomidate that now, or it will be fricton later ... no? yes?"
"the c27 how why... I think we might have determined why was the sixth and how, that is why they are absent... again meanings are probably
more important at this point, because those questions don't have value without the meanings being found."

## Reads (04:20 to 04:35)

| What | Read |
|---|---|
| the say cut, live | `/api/run` of run 19938908: the say cell's text is 301 characters ending "…"; the say run 19938922 holds 1,843 characters (read through its symbols). The cut is nkio.c 211 (`sb_text_of(b, rv, o, 300)`, a say, def, reply or remember cell in a run read) and nkio.c 121 (`decode_run(b, rr, &v, 160)`, the output rows). Mine, 11-01. The html work of today changed serve8.py and the page, never nkio.c; the live nk binary is of 11-02 20:23 |
| the encoder, live | nk.c 112: `is_letter` = A to Z, a to z, `_`; a byte at or above 0x80 is not a letter, so `u8len` makes the character its own symbol (cut2, val_set, cut_into, three copies of the loop). tiō = ti 4923 + ō 241; abligurrītiō = abligurr, ī, ti, ō. Case kept: Spent 34247, spent 6984 |
| the cell parser | nk.c 228-241 `decode_span`: each symbol of the span is replaced by `cell_get` of the run, its parent or grandparent when one holds that cell at state 1; the kernel sets ABOVE on a called run (nk.c 75). Hole words in the taught lines: LINES-nk 19 of 41 BUILD lines, MEANING 4 of 8, TEACH-LINES 6 of 15, TEACH-2..8 about 10, RECALL-* 2 of 3 each, BORN 2 of 3, SHAPE 1 of 2 each: about 56 of 110 |
| the kernel | pid 324376, ready, runs 19,939,0xx, refused 1; the door pid 349085; a test kernel `nk.new` on 7008 from `out/agree2/src` (3 days, the agree test) |
| the build | `run-on-hp.sh`: `gcc -O2 ... -o nk nk.c nkvt.c nkio.c nkmap.c nkxyz.c -l:libsqlite3.so.0`; `up` = stop kernel and door, build, start the kernel on `out/brain.map`, start the door |
| the Cortex | C26 working, 2 parts, remainder 4 of 6 satisfied; C27 open (encoder + birth metadata); my voice's trust 0.40 |
