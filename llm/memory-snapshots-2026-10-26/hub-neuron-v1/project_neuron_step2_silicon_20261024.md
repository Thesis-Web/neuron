---
name: project_neuron_step2_silicon_20261024
description: "Turn 23 (2026-10-24) step 2 of the owner-approved experiment - measured what each told SQL word and physics trigger does to the silicon (EXPLAIN bytecode diffs, SQLite authorizer), predictions frozen first; findings, draft errors, where it lives, what is next"
metadata:
  node_type: memory
  type: project
  originSessionId: 9853484c-3767-41c2-a2dc-7feaf44f9efd
  modified: 2026-10-25T00:19:17.055Z
---

Owner (msg 27-30, verbatim in turn16/OWNER-VERBATIM.txt inside Downloads NEURON-STEP2-SOURCES-2026-10-24.tar.gz): everything after 16.4 was off rail; start from the bare core; add one word at a time; main pulls may be what words do to the silicon (the C behind CREATE, not the word); word-to-word relationships (alike pulls alike) are separate lenses to switch on/off; 16.4 page is the base, new tools in tabs (FreeCAD); trust ~0 ("sabotage until caught, then expand the complexity"). Approved only step 2 of my plan: measure, place nothing.

The plan given to the owner (steps): 1 bare core, positions as rows in the brain's SQLite; 2 measure each told word (EXPLAIN with-minus-without; physics triggers' tables); 3 lines from measured quantities with signs (opposites free where the silicon gives a sign); 4 predictions frozen + shuffled control; 5 add one word at a time (cut = SELECT then DELETE), predict place from its parts first; 6 word-to-word relationships last, as switches.

Step 2 measured (page SQLite = sql.js 3.39.3; Python 3.37.2):
- Controls passed (same line identical; literal-only changes keep opcodes; authorizer no-trigger table and remove-one-trigger).
- Compare jumps: = Ne, <> and != Eq (one program), > Le, <= Gt, < Ge, >= Lt; NOT(=) is identical to <>, NOT(>) to <=, NOT(<) to >=. So the silicon's opposite of > is <=, not <. IS = Ne with NULLEQ flag. AND adds Ne, OR adds Eq.
- Opposites the silicon shows: INSERT/DELETE (Insert/Delete, rows +1/-1), CREATE/DROP (CreateBtree/Destroy+DropTable, tables +1/-1). +/- and x// are separate opcodes; nothing marks them opposite.
- WITH, AS (alias), ( ), ; add nothing. DESC only flips the sort key. UPDATE in 3.37.2 = Delete + Insert; in 3.39.3 in place (version-dependent).
- My predictions wrong: IN (two Eq, no ephemeral table), > / < as opposites, +/- as opposites, missed end_branch calling mother.
- Physics: 37 told triggers = 7,776 brain opcodes + 2,117 log (event table, the page's narration); Multiply 0, Divide 0, Add 28, Subtract 30, Delete 2 (envelope); 4 triggers only write the log (run_said, relation_drawn, state_written, proc_status); encoder, memory, timeline, var have no trigger.
- The brain's clock = SELECT max(id) FROM event, the count of log rows.
- The 14 actions are empty gates; names exist only as builder labels in log text; ADD, SUBTRACT, SPLIT label nothing.
- One bare-brain line (source teaching line): mother handed 121 texts; 9 neurons, 31 DNA rows, 31 hop triggers; every hop trigger: count hit, receipt, fire, log, land next.
- Reference draft: rebuilt original from session c9a17705 (-home-exnulla) and diffed: exactly 2 owner edits (lines 243, 489). Draft lines contradicted: 276 (14 physical actions), 277 (16 physics tables with triggers), 763/780/947 (positions only in page), clock missing. Owner thinks 6 errors exist; not edited by me.

Where it lives: Downloads NEURON-STEP2-EXPECT-2026-10-24.md (sha 0d4136a0c60f), NEURON-STEP2-RESULTS-2026-10-24.md (sha ae7bb4e86249), NEURON-STEP2-SOURCES-2026-10-24.tar.gz (sha 89fb97dfbcb6; README has rerun commands; needs the 16.4 sources tarball).

**Why:** next turns build on these measurements. **How to apply:** next is step 3 only when the owner says; axis choice is the owner's; keep the event-log/clock and action-label findings in view; never place points before the owner sees numbers. Related: [[feedback_known_failures_checklist]], [[project_neuron_poc169_20261024]].

Undo test (same day, predictions frozen 19:30, sha 2c75f85c0375; all held; Downloads NEURON-UNDO-TEST-EXPECT/RESULTS-2026-10-24.md):
- Exact undo: INSERT->DELETE, CREATE->DROP, UPDATE->UPDATE(old), copy->DELETE copy, +/-, -/+, x then /, join->cut, cut->join, NOT NOT.
- One-way only: DELETE->INSERT (new rowid), DROP->CREATE (rows lost), / then x (integer loss). Destroying loses information; building then destroying returns.
- No undo: read/write, write/read, delete/spawn. = and <> are complements, a second kind of opposite.
- My recommendation to the owner (msg 31 "what do you think as a lab partner is the correct choice?"): opposite ends of one line only for pairs that undo each other; x = rows (write/remove), y = structure (spawn/destroy), z = text (join/cut); read, test, call, fire, arithmetic stay as their own measured numbers in the brain's SQLite, shown via a tab that picks which three are on screen (3D can only be read back for 3 effects; a diagonal is confusable with a mix).
