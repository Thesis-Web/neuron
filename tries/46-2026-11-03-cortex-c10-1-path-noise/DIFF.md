# DIFF: 16:54 -> 16:58 CST

| row | before | after | progress or degression |
|---|---|---|---|
| a quoted sentence with two slash tokens | dropped as path | kept; a path token needs a word character beside its slash; two paths make noise only when fewer than four words stand beside them | progress |
| bold, headings, bullets | leaked into kept sentences ("**contract.** satisfied" became a part at 15:14) | stripped before the split; "contract." falls as too few words, the sentence is kept | progress |
| a label like c10.1 or c18 in a sentence | read as a value, failed the receipt (twice today) | a value starts its token | progress |
| the receipt cap | 40 lines dropped the summary line of a 42-line print | 80 lines | progress |
| C18 | working, its proof pending | done by receipt 0.923; the 15:14 Stop hook judged 20 sentences against it | progress |
| the judge on my own sentences at 15:14 | | 3 true lines called hallucination by receipt (numbers in no receipt, common words shared); 4 report sentences made parts of C18 through receipts of the Cortex's own prints | findings, typed as C16.6 and C18.2; no fix yet |
| remainder parts | 14, 13 left | 15, 12 left; NEXT WORK C10.2 | progress |
| cost | | filter test 52 ms; receipts 147 to 964 ms; one haiku call 6.1 s; load 0.27 | no degression |

No degression. Nothing rolled back.

## CONTRACT, balanced

| expected | SATISFIED by | REMAINDER |
|---|---|---|
| markup off before the split | run 403233 "satisfied: the root disk has 393g free as df printed." | |
| the path rule | runs 403228 and 403238 kept; two path lines dropped | |
| the receipt keeps 80 lines; C18 re-judged | C18 completes 0.923 by receipt, done | |
| the remainder part closed by the Cortex's record | `remainder cortex 10 1 satisfied` citing the receipt runs; NEXT WORK moved to C10.2 | |
| | | C16.6 the receipt rule over-fires on common words; C18.2 circular receipts of the Cortex's own prints; C17.3 a command-argument digit still a value; the four chatter parts on C18 (the owner's reject) |
