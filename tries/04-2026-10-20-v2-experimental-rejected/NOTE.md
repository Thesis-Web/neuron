# 04. v2 experimental (2026-10-20): rejected

**Status: rejected the day it was delivered.** Its tarball says so itself: `BUILD-STATUS.md`, "NOT_DEMONSTRATED".

**What it was** (versions audit, row 5). C + SQL. 44 fixed tables; `dna(gate, arrival, head, …, program)`; "A fixed set of tables stores many logical neurons" (its ARCHITECTURE.md); 0 triggers. `kernel.c step()` picks DNA `ORDER BY specificity DESC`, concatenates atom texts and executes. `table NAME` fills a told template hole and the next step pastes `CREATE TABLE "u_NAME"`. 51 told SQL programs emitted by Python at build time. An unknown word creates no gate.

**Scores.** One table per neuron: no. Run → mother: half. Mother exec-only: half (a small executor, but it picks DNA by specificity and forks runs). Only hop and trigger hand-laid: no (the thinking is 51 Python-emitted SQL programs).

**The owner's verdict,** in the handoff written the same day (`../../specs/superseded/2026-10-20-builder-handoff/`, §0): "It reduced **the means of development** rather than **the initial amount of acquired knowledge**. It delivered an affine-function learner with fixed commands, structured lessons, limited construction, and manually supplied geometry. It checked that substitute and called the remaining developmental machinery a 'gap.' The owner rejected it because that gap was most of the assignment." And §7.3: "Failed V2: do not relabel it as the baby."

**Files.** `neuron-v2-experimental-2026-10-20.tar.gz` (sources/, src/kernel.c, schema.sql, seed.sql, tools/, install.sh, Makefile, say, talk, BUILD-STATUS.md, evidence/) and its `.sha256`.
