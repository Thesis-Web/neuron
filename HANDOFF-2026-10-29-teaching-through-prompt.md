# Handoff, 2026-10-29: teaching through the prompt. Words, not code.

For the owner and for any model session that opens this archive after tonight. Read `LLM-HANDLER.md` first, then this. The owner's last words of the night: "for now teaching through prompt... verbage not code."

## Where things stand

The live build is v6 in `tries/19-2026-10-29-v6-space-shards-tools-and-page`. It is v5 with one change to the physics and a page in 17.3's look. The change: a word's DNA row is now keyed by the nearest symbols that are not the space, so a word's contexts are rows in its own table and the space neuron holds one row; in v5 the space held 1,955 rows and that was the cheat the owner named. The brain in that folder holds exactly the 60 tool lines of `brain/LINES-v6.txt`, typed in order, and nothing else: the born runs and their binds, the standing questions, the ask, the define run, the sixth's observing line, why, correct and incorrect, and the eleven tools. Nothing of the owner's list has been typed. The chain of every choice is `CHAIN-v6-2026-10-29.md`, the record of each line is `LEDGER-v6-2026-10-29.md`, and the page's checks are in `tests/`.

The page is `page/NEURON-POINT-OF-CONNECTION-v6-2026-10-29.html` behind `page/serve6.py`. It carries 17.3's stylesheet byte for byte and 17.3's drawing: sphere points, names that keep their size, springs with a pull and a direction per kind, the space between points, one fixed point (heard, where every typed line arrives), run lines through the points, a flash to where the run goes on and, in orange, to the run a shard calls. It replays the brain's history from the receipt table, so play from the start shows the neurons appearing as the lines bear them. What came out is the typed line's data sheet, every cell read back through the encoder; an answer from mother with rows is printed as a table. No button types lines. The two files of lines are listed under Type and a click only fills the prompt.

## The standing order for the next stretch

Teaching happens at the prompt, by typing lines. The brain lays the rows. No new program, no new egg, no change to the page or the door unless the owner asks for one by name. When the owner asks why something happened, the answer is a trace through the brain's own rows, said in words: which gate, which shard, which run, which cell. When a line does not do what was wanted, the fix is a line the owner types, not an edit to a file. A model session in this stretch writes prose, lists lines to type, and reads tables back; it does not open an editor.

## How to start

Copy the folder to a Linux path first; on the Windows drive a line is about ten times slower. In the page folder, start the door with python3 and serve6.py, then open localhost on port 8056. Or, in the brain folder, raise the stack limit (ulimit -s unlimited) and start bottom6.py for the two prompts at the terminal; a line that begins with "6>" goes to the sixth. The page's start over lays both eggs and the source brains again and types nothing. Two older doors may still be up from earlier sessions: 8018 is the tries/15 page on v18, 8055 is the v5 page. Stop a door by its process number from a command of its own; never search for its name in the same command line.

## How a line is taught

Every formula is taught the long way, in three lines, and the owner has watched this shape since v5. First the formula itself, a line of BUILD spans. Typed at the top it answers an error about the column above, because at the top there is no run above it; that is right, and the shard is laid. Second, the key line once, such as print dna : who, which lays the key word's shard: arrived from heard, going on to the colon. Third, the bind: a BUILD UPDATE of the key word's table setting call to the run number the formula line started, where before is 1 and trigger is 68. From then on the key line fires the formula. The run number comes from What came out; the page fills it in when a line of the lists is clicked.

The colon matters. Under v6's key a word's shard is one only if the same symbol follows it, so every key is the key word, a colon, the value: define : who, print dna : who, change trigger : who from 68 to 121. The two lines the brains pass each other follow the same shape: seen : N from main to the sixth, why : N cell from the sixth to main.

Inside a BUILD span some words are holes: a symbol that names a cell already filled on the sheet of this run, its parent or its grandparent is replaced by that cell's value before mother sees the text. me and above are always holes; what, reply, def, say, know, remember, shape, known, unknown, from and to become holes once a span has written them. A span that needs one of those words as a plain word cannot have it.

## What to type first

The owner's own list, in `FIRST-RUNS-v6-2026-10-29.txt`, begins with the thirteen define lines: the, as, a, find, in, are, can, who, what, when, where, how, why. After each, What came out shows what was asked, the definition run it points at, how many symbols of the line already had a definition, the memory it remembered, the formula it used, and the known and unknown symbols of the definition. The unknown list is the next work: the symbols that keep returning unknown across the core words are the compounds to define next. Then the SQL words, whose action the docs and the measured source answer. Then the guesses: a symbol no source holds leaves a cell empty, the sixth asks why, the guessing brain answers with a confidence, and the owner says correct : N or incorrect : N with the run number the guess was asked by. Then the definition cells: change define : who class, with a value of the owner's choosing, and print sheet : N to see it. Then the DNA columns through change trigger, change call, change spawn. Then a new neuron. Then one new key taught the long way, as the shape of the formulaic layer; the file holds an example of the three lines.

## The tools, in words

print dna : X prints X's DNA table. print memory : X prints the memory rows that ended on X's shards. print node : X prints X's definition node, each return read back through the encoder. print sheet : N prints run N's data sheet with the cell names. print table : name prints any table by its name; a large table such as land is a very long answer. create neuron : X bears X by calling the born run and reads its two tables back. change trigger, call or spawn : X from A to B rewrites that column of X's rows where it is A; A and B may be a symbol or a number. change define : X cell value writes a cell on the data sheet of X's newest define run. change meaning : X from A to B rewrites the meaning cell of that sheet where it is A. Every change answers how many rows changed.

## Open, and the owner's to decide

Whether the space should ever carry more than one shard. The words seen and why. The rule for reading a source line into relationships, which takes only like and opposite and splits a multi-word synonym into its words. What a definition's cells are made of beyond their names, and whether they should live on the node table rather than the define run's sheet. The names of the keys. Which point the page should hold fixed. Whether a tool's answer should also become a memory of the symbol it was about. The layers themselves: core, root, prime, compound, complex, formulaic.

## Traps met this night, for the next session

A tool bound to a key word fires when the run reaches the key word, before the run has reached the value; create neuron had to call the born run itself for that reason. The guessing brain's corpus holds only the words of source returns, so a symbol with no source line gets no guess until a later line brings more returns, and the sixth then re-asks; that is the retry loop working, not a fault. After the door restarts, the run numbers behind the lines file are matched by text against the lines already typed. The page loads the whole receipt table once for the history; past some tens of thousands of hits that read will grow. The archive's handler and this file are the record; the model's own summaries are not grounding.
