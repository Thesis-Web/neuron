# audits: outside reads of a build against the spec

Each one names the build, the scope it was read against, and the rows or lines that show each finding. None of them built or changed anything.

| File | Of what | Against what | Headline | Date |
|---|---|---|---|---|
| `AUDIT-HP-2026-10-19.md` | The hp (Fable) turn-one build, copies taken 07:28 | NOW, the blueprint, the guide, the update | "It does not learn. In 5½ hours of running alone it found no formula and made no guess... The core values can be bypassed." Blockers B1 to B5, majors M1 to M16, §19 scorecard. | 10-19 |
| `AUDIT-HP2-2026-10-19.md` | The hp2 (Opus) turn-one build, copies taken 07:28 | same | "The brain collects instead of learning... 78% of the graph into one small column... Told never ended a second time, and the REPORT says it did." Blockers B1 to B7, majors M1 to M17. | 10-19 |
| `NEURON-17.3-FORENSIC-AUDIT-2026-10-25.md` | Point Of Connection 17.3 (the told block, the host, the page) | The reference draft and the owner's typed words with timestamps | 17 chain rows plus 2 cross-cutting: what 17.3 does (file:line), what the spec says, why wrong, the fix in his terms, the trap that made me build it that way; a fix order; where v18 stands. The owner's question answered: births are string templates inside a hand-laid trigger, run by a host mother that logs nothing when called that way. | 10-25 |
| `NEURON-17.3-TRACE-EVIDENCE-2026-10-25.md` | The same | The page JS, the told block and host15.py traced with line cites | Evidence file for the forensic audit. | 10-25 |
| `NEURON-v1-CHAIN-EVIDENCE-2026-10-25.md` | The v1 egg (`tries/03`) | Replay-verified chain through egg.sql | Evidence file: what v1's five neurons do, hop by hop. | 10-25 |
| `NEURON-VERSIONS-AUDIT-2026-10-25.md` and `NEURON-VERSIONS-EVIDENCE-2026-10-25/` | Every version from 16.2 to the new v18 | Four tests in the owner's words (one table per neuron; run assembles the SQL and mother pastes it; mother decides nothing; only table-making, hop and trigger hand-laid) | "None of them did it correct end to end." Where to step back to: v1's shape plus v18's two fixes. The RESULTS file of v18 overclaims on 14 points. Seven evidence files, one per group of versions. | 10-25 |
| `NEURON-SPEC-VS-BUILD-2-COMPARISON-2026-10-25.md` | Build sheet 2 (`tries/13`) | The owner's words with the time he typed or spoke them | For each of 21 chain steps: specified / inferred / invented / contradicts? / unknown. 11 rows contradict his words; one cause under most of them (a trigger that writes; replies as runs). Traps 81 to 87 logged. Written after the owner pasted an audit saying: "The architecture converted open questions into fixed implementation rules, then used successful execution to validate those rules." | 10-25 (written after midnight, 10-26) |

Also an audit, kept where it was pasted: the independent 16.2 audit of 2026-10-01, in `prose/2026-10-17-by-topic/NEURON_OWNER_WORDS_BY_TOPIC.md`, Appendix A, paste A15.

The adversaries' own findings during the turn-one builds (FINDINGS.md 1 to 58 on hp, ADVERSARY-FINDINGS.md rounds 1 to 5 on hp2) are inside `tries/02`.
