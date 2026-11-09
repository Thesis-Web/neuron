# tries/59 (2026-11-04, 19:2x to 20:15 CST CST): meaning discovery, the owner's contract (paste 9) and directive (paste 10)

The owner's words are in OWNER-WORDS.md; the contract in CONTRACT-cortex-paste9.md (the Cortex owner source neuron-contract-meaning-discovery, 117 sentences) and the directive in DIRECTIVE-builder-paste10.md (neuron-directive-discover-meaning, 121 sentences); the ten expected outputs are neuron C30 to C39 in the Cortex. The selection method, the hypotheses and what each run changed are in CRITERIA.md. Every print is in this folder (phase-a-hp.txt, phase-a2-hp.txt, candidates-hp.txt, derive-run-1-hp.txt, derive-run-2-hp.txt, derive-run-3-hp.txt, testc-find2-hp.txt, testc-run-hp.txt, testc-run-2-hp.txt, retained-and-regression-hp.txt). The live kernel on hp was never typed into or stopped (19,948,495 runs before and after); everything ran on the test brain `~/nk-roots` (port 7009, door 8059), refreshed from the live stored brain at 20:1x (refresh.sh).

## What was built: one derivation run, DERIVE-nk.txt (derive_gen.py)
A line file of three lines: the evidence table `derived`; the derivation run bound to `derive : X`; its bind. The run names no word. For X it reads X's first WordNet verb sense (the first node row from source 7 whose text starts with verb, by node id), takes the words of that gloss in order that are believed points (a belief row with correct > 0, the brain's own record of a confirmed action), and lays on X the shard (heard, :) with the first such point's confirmed call as the call and the second's as the spawn; a belief row 0/0 marks it a guess; every word used is a row of `derived` with the sense run; no believed word: an `unresolved` row and no shard. Each sense shard of X (C21, keyed by an example's context) takes the same from its own sense's gloss when it holds no call yet. The expected for each candidate is written before the line by the same stated rule from the brain's node rows (derive_apply.py), never from the derivation's output.

## What the brain did (run 2, H1a, the refreshed test brain; run 3, four words never run; Test C)
| candidate (the list's order) | the brain's derivation | the line typed and what ran |
|---|---|---|
| catalogue | make → 929 | catalogue : who ran 929 (create's run) under the line |
| docket, pulsate, accommodate, affect, abandon, attest, backpedal | unresolved, no shard | X : who landed on the hop shard 17, nothing ran |
| plan | make, design, form → 929, 929 | plan : who ran 929 as call and 929 as spawn |
| adapt | make → 929 | adapt : who ran 929 |
| apologise | explain, make → 19938846, 929 | apologise : who ran define's run (which replayed its sheet run 19938193) and create's run |
| black (never run before) | make, become → 929, 950 | black : who ran 929 and 950 |
| bribe (never run before) | make, exchange → 929, 950 | bribe : who ran 929 and 950 |
| assume, six sense shards from define | (gods, human) → form 929; (I, his), (we, that), (We, that) → true 19937779; (will, the) → form 929; (President, office) → none | The gods assume human form ran 929; I assume his car was late ran 19937779; they assume nothing landed on no sense shard and ran nothing |

All thirteen agree with the expected written first. The compositions are crude (the gloss's believed words in order, two at most) and some are wrong as meanings (black : who runs create then change); they are the brain's, from its rows, with the evidence kept.

## Found on the way
- Run 1 (H1) counted or, and, as, by, on as grounded: the define cascade lays a spawn row at (define, :) on words of definitions. H1a reads belief instead.
- WordNet's senses are in node id order on the brain and in another order in the source file; the first sense is arbitrary where no context selects one (the (heard, :) shard); the sense shards select by context.
- A keyed dna read by (gate, before, trigger) lays the shard when absent (abdicate: a SELECT laid shard 20049858). The kernel bridge, mine; the derivation reads by gate only.
- A correlated subquery in a FROM clause (per sense shard) is not SQLite: the per-sense statements were re-formed as correlated scalars.
- A repeated line is a memory hop and writes no say of its own: meaning : print read 'ok' on the test brain because the live brain had typed it; meaning : catalog, never typed, is in retained-and-regression-hp.txt.
- The 21 roots of tries/58 are on no refreshed test brain now; H1a excludes them (no belief rows); the directive keeps them a test artifact.

## Not done, said plainly
EO-09 (reproducibility): the rule changed between the two runs on the same words (H1 then H1a), so the same rule on the same starting state twice was not run. The sixth asking when no shard matches: the unresolved rows are laid, nothing asks. The teacher's judgement of the laid guesses (correct : N / incorrect : N) is the owner's. Nothing on the live brain.

## The auditor's reading (the owner, 20:5x) and what it changes
"some of those candidates are operationally wrong despite executing successfully. For example, deriving an operation for black that calls create and change does not establish the meaning of black." Right. The contract (section 5) ends in validation and a retained meaning; the six shards are guesses at belief 0/0 and none is validated, so EO-01 is partial and EO-04 is not met. Why H1a produced black: it takes every believed word of the gloss as an operation to perform, and the only operations the brain has confirmed are the 25 programs on its own tables (create a neuron, change a dna column, print rows, define, correct, step), so make became create and become became change. The gloss "make or become black" has its meaning in black, the state something is given; make and become are the operator. The same sense row holds the evidence that says so and H1a does not read: the frames (Somebody ----s something: an object receives the state), the hypernym (color, discolor: a colour attribute changes), the derivationally related form (black the adjective, the property). The operation that would establish it, give a point the attribute black (a relationship row or a state cell), is not among the brain's confirmed operations. This is Phase E's material, not a reason to tune the rule to black.
