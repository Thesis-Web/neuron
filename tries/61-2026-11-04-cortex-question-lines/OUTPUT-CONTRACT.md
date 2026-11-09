# tries/61: the output contract, before the build

## Works and must not change (live read now)
- cortex questions cortex --ask prints 29 open questions, each with what the sources hold (name, file:line, the line) and what no source holds, and the closing count (0 of 29).
- cortex questions <project> prints the open questions only; the answered ones are skipped (open_questions).
- The index holds no sentence text for ingest, part, verdict or receipt rows (C17, C27); a source db row is read by its pointer, the text re-cut at read (C54).

## Wrong by the newest prose
- C51.1 (the remainder of cortex C51, typed 11-04 16:xx): the lines found are printed only on the turn that closes a question; the next --ask prints nothing for it; a print of the lines found for an answered question is owed.
- The answered field of a closed question stores the found lines as text (t[:100] per line, 300 chars in all): text in the index, against C17/C27 and C54 (the pointer is kept, the text re-cut from the source row at read).

## New work, with the expected live output
- C51.1: a closed question keeps pointers to the lines found (source, row id or run, path, line), no text; `cortex questions <project> --answered` prints every question the sources answered with its lines re-read from the source db (or replayed from the run's gates for a typed source): source, file:line, the line. `--ask` ends with the count of answered questions and names the verb.
- Expected: on the test brain (CORTEX_PORT=7010) a question closed by the sources prints under --answered with at least one line found naming its source and file:line; the question's cx row holds pointers and no line text; on the live front door the same verb prints the answered questions of cortex (0 today, or the ones that close).
