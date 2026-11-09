# tries/63 (2026-11-06, 14:46 to 15:05 CST): the judge's brain in sql, on the test kernel

| What | Read |
|---|---|
| why the brain's shapes cannot be read from another process | seq, label, run, neuron, dna, hit are virtual tables (USING nk) served from brain.map by the kernel; main.db holds only the index cx; the kernel opens main with journal OFF and no busy timeout, so an outside reader's locks could fail its writes |
| why the judge sits in the attached cx db | the kernel holds 10 attached dbs (sixth, 8 sources, cx); the system sqlite allows 10 (MAX_ATTACHED=10) |
| the mechanism | a row into cx.judge_ask fires a trigger that hands each rule (a row of sql in cx.judge_rule) to mother(sql, run, name, n); the mother runs it on the kernel's connection, where seq and label answer by key; cells and the verdict come back as rows; the edge is one sql line over the door (judge-door.sh, bash /dev/tcp) |
| C1 done | claim 2190607 on audit C3: 28 neurons, its expected 23, 7 shared, 17 out of line; equals the python side by side line; the test kernel refused 0; completes 0.94 by receipt |
| C2 done | cells for 8 random judged claims in 5.9 s: values (digit islands starting a word; c28 a name), held by older prints, new to the project, same_as, content shared; completes 1.00 by receipt |
| the judge's own memory | judge_gate: per project and for all lines, the lines each neuron appears in and its first run, every neuron counted, built in 5.8 s from 2672 lines; the front door's gate index skips small words, so it could not be used |
| C3 working | on the 36 marked runs (guess excluded): the judge brain agrees with the mark 8, the python 27 (trained on these marks; 9 of its verdicts by haiku); with a print 6 of 14 against 12 of 14; without a print 2 of 22 against 15 of 22 (the judge brain says unsettled: no print can check the values); progresses 0.67 by receipt |
| left | C3.1 the next proof blind (fresh lines, the owner marks); C3.2 known faults (one-digit values as evidence, partial holds called progresses, the commonness line, no sources); C4 live beside the python; C5 the owner's word |
| commits | hp2 cb2bfec (judge/*.sql, judge-door.sh); nothing laid on the live cx.db yet |
