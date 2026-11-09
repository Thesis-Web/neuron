# tries/52 (2026-11-04, 03:00 to 03:40 CST): the definition schema and the say by who is speaking, live on the kernel

The owner, 03:10: "I approve c26 .. register the outline with cortex, provide an expected output to the cortex, build it and check it live.
do not break the html serve.. proceed". 03:25: "walkers are not desired, nor sweeps, so more precise ways to determine relationships would be
better if we can... relationship tables might be small now, but later they might be hundreds deep and walks of whole tables might take a
lot of time???"

## What was built, as the brain's own lines (`RECALL-9-nk.txt`, typed by `recall9_apply.py`, 0 refused)

The define run laid again (run 19938846): RECALL-8's three spans as the kernel holds them in run 19938199, read back symbol by symbol, then
five spans. define's rows (heard, :) and (the sixth, :) call it.

- Span 4, the field cells, one statement: class 441, tense 6332, etymology 204, prefix 5516, suffix 10547, as gate lists on the typed line's
  sheet (the brain holds numbers; the page's door reads known and unknown back as words, these it shows as numbers: "made for machine to
  machine, that is fine"). The point's rows are its node rows (keyed by gate) and the returns under the line (keyed by parent). A `[` opens a
  field; only a field whose first symbol is part, forms, conjugated, plural or etymology is read further (one keyed read per `[`); its name is
  the symbols up to its `:`, its content runs to the next `]`. class = the first `part of speech` field of each row plus the first symbol of a
  WordNet or Wiktionary sense row (verb 1:, noun 2:); tense = the `forms`, `conjugated form` and `plural` fields, a symbol that names a
  sub-field (tags:, type:) left out; etymology = the field whose name is the one symbol 204; prefix = a symbol of the etymology followed by `-`
  and a non-letter (ab-, ex-) or by ` +` (GCIDE's "ab + ligurire"); suffix = a symbol after `-` preceded by a non-letter (-tiō, *-s). Ordered
  dictionaries first (the `ranks` rows of tries/51), then run, then position. '' at state 1 when nothing, so the sixth asks no why.
- Span 5, the relationship cells: like 138, opposite 139, similar 530 from `rel` both ways (gate = what by its key; other = what by its index),
  ordered by the run that laid them.
- Spans 6 to 8, the say, as the tools of 10-28: say declared; one statement; say = reply. The statement reads the eight cells and known and
  unknown back from the sheet by cell number, splits the gate lists, and shapes the text by the typed line's arrival: 5 (the sixth) → one
  json object, the values gates, the keys the cells' own labels; otherwise (1, heard) → arrays of words through the encoder, like, similar,
  opposite first, then class, tense, prefix, suffix, etymology, then the definition's first 200 characters.

Every read is keyed: node (gate), run (parent; id), seq (run; run, pos), label (gate; symbol), ranks (cell, source), rel (gate, kind, other;
other), run_sheet (run; run, cell). No table is read whole (the owner, 03:25).

## Checked live (the prints beside: `apply-hp.txt`, `define-after-hp.txt`, `sixth-path-2-hp.txt`, `check-reads-*.txt`)

| line | arrival | class | tense | prefix | suffix | like | say |
|---|---|---|---|---|---|---|---|
| define : spend (a recall, 146 rows) | 1 | verb v t i noun | Spent Spending spends present singular third person spending participle spent past plural | ex pend | s | 181 words | `spend \| like: know, run, of, to, ...` |
| define : abligurition (a recall) | 1 | n noun | | ab | ti | | `abligurition \| like: \| similar: \| opposite: \| class: n, noun \| tense: \| prefix: ab \| suffix: ti \| etymology: L, abligurito, ... spend, in, luxurious, indulgence, ...` |
| define : acersecomic (never held; wikt) | 1 | noun | acersecomics plural | | | | `... \| class: noun \| tense: acersecomics, plural \| ... \| etymology: From, Latin, acersecomes \| def: noun 1: (rare) A person who does not cut their hair.` |
| define : acersecomes (sent by the sixth) | 5 | | | | | | `{"what":1317489,"def":null,"class":[],...,"known":[],"unknown":[]}` |

The door on 8058 (pid 349085) and the hub were not edited or restarted; `/api/info` ready before and after; the page's output rows carry the
new cells.

## What is mine, labelled

The SQL of the five spans; the five field names read (the labels of tries/22, the sources' own names); the prefix and suffix rules (the
hyphen; GCIDE's plus); the order of the arrays and the 200-character cut of the definition in the human say; the json keys as the cells'
labels; reading arrival 5 as "an llm asks" and arrival 1 as "a human asks" (the owner's words name llms and humans; the brain's rows name the
sixth and heard). The owner's: the cells, the two shapes, "relationships, similar, alike are key", no walker and no sweep.

## Found on the way

- nk.c `decode_span` replaces a symbol that names a cell of the run, its parent or grandparent by that cell's value when a span is decoded.
  So inside a span a cell is named by its number, never by its word, except above, what and reply; and GLOB stands where LIKE would be
  (like is cell 138). RECALL-8's known/unknown span writes `'known'` and `'unknown'` bare: on a recall those decode to the gate lists; its
  EXISTS test fails on a recall anyway, so nothing is lost.
- A join on `s.pos = ( SELECT min ( pos ) FROM seq WHERE run = pr.r )` ran the subquery per symbol: 4.66 s of the first form's 4.9 s on `a`.
  RECALL-8's idiom (`ORDER BY pos LIMIT 1` in the select list) is one scan per row. The whole span 4 is now 0.016 to 0.255 s as a read.
- The encoder holds `tiō` as `ti` and `ō`, `Spent` (34247) and `spent` (6984) as different gates; GCIDE's `v. t.` gives the class symbols v and t.
  The cells hold what the sources and the encoder give; mapping n → noun or v → verb is a relationship for the brain to learn, not mine to type.
- The define run's own text birthed three symbols (instr, json_object, json_group_array), each defined by the birth rule as any new symbol is.
- My check tool's read `run WHERE arrival = 5` (to find the newest define from the sixth) walked the list of runs arrived from the sixth twice
  and paged 5 GB of the map file in (RssFile 6.47 GB, heap 67 MB unchanged). A walk of my tool, not a span of the brain; the owner's 03:25
  words apply to it. The brain's own spans read by key.
- The like rows of `the` and `a` (read in `check-reads-hp.txt`) hold noise laid by earlier defines (mother, main, guess, reply, ...): not this
  turn's, the compare of tries/51 saw it; the owner's C25 is where the laying of relationship rows is deepened.

## Remainder, the owner's

The accept lines (`cortex accept neuron 26 <run>`); whether the human say should cut long arrays (spend's 181 like words) and how; the hub
(unchanged: the same five spans as lines through its prompt would be its own turn); C25 (the define laying the returns' words as relationship
rows, so like/similar/opposite fill for a word like abligurition); C24 (Oxford); the C14 patches; the hub door restart.
