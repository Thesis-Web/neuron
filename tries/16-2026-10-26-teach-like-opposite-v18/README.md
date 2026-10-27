# Two formulas taught to v18 at the prompt (2026-10-26): like and opposite
Not a change to v18 (tries/11 is untouched). `like18.json` holds four lines in the shape of `sheet18.json`: the teaching line for
`like`, its bind, the teaching line for `opposite`, its bind. Type them at the prompt (`python3 neuron_prompt18.py <brain.db>` in
tries/11, or the type tab of the Point Of Connection 18 page) in that order; then `like : store`, `opposite : go`.

What a line like these is, in v18's own terms (gen18.py, the hand-laid triggers):
- `word = BUILD ... BUILD` is a teaching line (input_teach): the text after ` = ` runs through the neurons as a run of kind teach,
  every token without a gate is born first, and at its end (end_teach) a formula row points the word's gate at that run.
- `BUILD ... BUILD` pairs are what mother runs; `var name` is a hole filled from the run's data sheet (this run's cell, else its
  parent's, else its root's). A formula run starts with the cells run, after (the text after the word that fired it) and subject.
- `like : -> like` is a bind (input_bind, bind_go): the DNA row in like's table for "arrived from heard, a space next" gets its
  trigger column pointed at like, so a line that starts "like :" fires like's formula with after = " : <the rest>".
- The formula then writes its own cells (what, dna, def), asks a source by inserting into its inbox (mother brings the answer
  back as runs, and end_return writes a cell named after the source holding each return run), records those runs in the
  word's definition node, and writes the cell say, which end_line prints.

`tests/` holds the two scripts as run against a door (serve18.py, tries/15) on port 8019 on a copy of brain18.db in memory, and
`CHECK-like-2026-10-26.md` what they said. Nothing was saved to a file; the owner's brain is not changed by this folder.
