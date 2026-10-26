# NEURON MEANING DISCOVERY: what a word does, how to find it, how to test it

*2026-10-22. Written from a read-only pass over the Point Of Connection model (version 7), the other session's transcript, your worksheet, the hp and hp2 lay files, and a literature pass (about 60 papers checked, three research helpers, each citation marked verified or not). Nothing in the model or the brain was touched. Everything I measured today is in `Downloads/Neuron-Meaning-Data-2026-10-22/`.*

*Marking: **[V]** = read on the source itself today. **[U]** = from memory or a snippet, not verified. **[mine]** = my reading or guess. Your own words are quoted with the date.*

---

## 0. The short answer

1. **Your hypothesis has real support.** The human brain measurably runs effector-specific motor code when it reads an action word (lick, pick, kick light up the mouth, hand and leg strips of motor cortex) [V]. Brain patterns for hundreds of concepts are best explained by *what experiences and actions the thing involves*, and not by its category or by which words it co-occurs with [V]. Five earlier computer systems already defined a word as the procedure it runs (SHRDLU 1971, Woods 1968, Johnson-Laird 1977, Feldman's x-schemas, Siskind's event logic) [V].
2. **Nobody has found the roots by thinking.** Every system that tried ended with two tiers: a tiny operator set (about 10 to 20) plus an open middle layer (150 to 200 predicates, or about 180 "molecules", or a few thousand grounding words) and a residue it could not reduce [V]. The research answer to "what are the roots" is: they are **measured**, not assigned, and there is more than one valid set [V].
3. **There is a balance equation.** Six distinct tests exist in the literature for "is this candidate meaning right, a guess, or wrong", and four of them are machine-checkable in your brain today (§6). I ran one of them on real brain-mapping data: a word's measured body-channel profile is reconstructible from its parts' profiles at 0.94 agreement, against 0.68 for a random pairing, and wrong decompositions fall to 0.25 to 0.66 (§5.3). That is a numeric balance over 39,707 words, from a public dataset, that the brain can be told as a source.
4. **The worksheet is mostly wrong in the formulas and right in the shape.** Of the eight prime formulas, two pass (below = −above, near = −far as "not far"), three fail outright (die = −live, before = −now, a short time = −−now), and three are the wrong kind of thing (durations written as positions). The one root error under all of them: the worksheet's "−" does three different jobs (not, opposite end of an axis, change of state) that are three different silicon actions (§4).
5. **The model's number-one gap is confirmed and sized.** In the model's own data, the words every definition leans on are the function words (or, the, a, to, of, in, and, is, that, by, with, for), and neuroscience says those words have *no* body channel at all: their meaning is purely an operation on other words [V]. They are the operators you keep asking about, and the data says they come first.

---

## 1. What exists today (read only)

### 1.1 The Point Of Connection model (version 7, 2026-10-22 02:05)

- Hand laid: 14 physical actions (READ, WRITE, COMPARE, ADD, SUBTRACT, MOVE, FIND, SPLIT, JOIN, CLOCK, HEAR, SAY, CALL, SPAWN), 16 physics tables with triggers, mother and source.
- Five sources attached as rows for 163 words (the 65 primes, the question words, the being and helper words, the page's own words): WordNet 3.0, Webster 1913, Moby, Merriam-Webster Collegiate and Thesaurus.
- Processes: 0. Learned meanings: 0. The page says so.
- The told prime layer (`PRIME_ROOTS` in the page) maps each prime to one or two physical actions. These are the other session's guesses, for example I → FIND, you → FIND HEAR, feel → HEAR COMPARE, touch → COMPARE HEAR, do → WRITE, live → CLOCK, die → CLOCK SUBTRACT. §5.2 checks them against measured data; several are wrong.
- The operators (`-` flip, `+` more, `++` lot, `/` part, `*` join) and hop operators (`+` continue, `-` step back, `*` test, `/` choose) are proposals with no mechanics behind `**` and `sqrt`.

**The most-needed ledger, recomputed offline from the attached source slice** (defining words that two or more sources share, counted across all 163 words, that have no meaning): or 142, the 135, a 132, to 129, of 126, in 118, and 62, an 61, is 58, that 52, by 49, with 48, for 44, one 33, from 33, at 29, on 27, be 26, something 25, not 24, place 19, it 18, have 17, which 16, are 15, time 15, all 11, part 10, what 10. And outside the 163: as 99, used 33, being 27, degree 12, out 12, into 11, than 10, come 10, person 9, another 9, act 9, action 8, form 8, number 8, state 8, point 8, word 8, put 7, means 7, cause 6, position 6, space 6.

### 1.2 The other session (v1-d0, still open, 16 hours)

I read its transcript. It is the session that built the model through seven versions. Its last state: version 7 published, the Webster root test written to `NEURON-ROOT-TEST-WEBSTER-2026-10-22.md`, the sources slice fetched, and your three limits restated in the page's terms. The "800 tries" in your message is your count of build attempts; the session's own count is seven versions of this page.

### 1.3 The two builds' root layers (hp, hp2), from their lay files [V]

- hp2 ran your worksheet formulas as arithmetic: die = −(count of awake memories), before = −clock, a long time = clock × clock, a short time = −(−clock) = the clock, near = −1. Four of eight come out as nonsense numbers, which is the first evidence that "−" cannot mean one thing.
- hp wrote actions instead: before/after = compare two times, below = one step down z, near = same place, die = END. Those are closer, and none was ever tested.
- hp2's meaning loop (gap, spec, compile, test, hold, wire) ran end to end on a dev brain for one word (dissimilar = [not something]) and never on the live brain, because the live brain parked its own runs. The loop's "test" compared a candidate's place to the word's place; it never ran the candidate on a use. That is the gap §6 fills.

---

## 2. What the human brain does with a word (the neuroscience)

All verified today unless marked.

| Finding | What it says | Source |
|---|---|---|
| Action words light up the motor strip for the body part they name (lick: mouth, pick: hand, kick: leg), in passive reading. | A word's referential meaning has a somatotopic motor correlate: the word *runs* part of the action. | Hauk, Johnsrude & Pulvermüller 2004, Neuron 41:301 [V] |
| Function words (the, of, if) build assemblies only inside the language machinery (left perisylvian), with no sensory or motor part. | Their meaning is an operation on other words, not an action on the world. Exactly `|` and `&&` versus `grep`. | Pulvermüller 1999, BBS 22:253 [V] |
| 25 sensory-motor verbs as a basis predict the brain image of a new noun at 77% (9 subjects). Verbs: see, hear, listen, taste, smell, eat, touch, rub, lift, manipulate, run, push, fill, move, ride, say, fear, open, approach, near, enter, drive, wear, break, clean. | A noun is a weighted bundle of verbs. Each verb has a brain signature. New nouns are predicted by composition. This is the closest existing object to your hypothesis. | Mitchell et al. 2008, Science 320:1191 [V] |
| 65 experiential attributes rated for 535 words (vision 15, somatic 5, audition 7, taste, smell, motor 4, spatial 7, temporal 4, causal 2, social 4, cognition, emotion 10, drive 2, attention 2). | A measured feature space for word meaning. Downloaded: `Binder2016_65_attributes_535_words.csv`. | Binder et al. 2016, Cognitive Neuropsychology 33:130 [V] |
| Experiential features (48 of Binder's) explain brain similarity best; an 8-feature sensory-motor subset still beats WordNet taxonomy and word2vec; taxonomy and co-occurrence add nothing once experience is in. | Categories are a by-product of shared experience features. Co-occurrence (what an LLM has) is not what the brain holds. | Fernandino et al. 2022, PNAS 119:e2108091119 [V] |
| 39,707 words rated on 11 channels: 6 senses (touch, hearing, smell, taste, vision, interoception) and 5 effectors (mouth, hand, foot, head, torso). | The largest measured map of "what a word does in the body". Downloaded: `Lancaster_sensorimotor_norms_39707_words.csv`. | Lynott et al. 2020, Behav Res Methods 52:1271 [V] |
| 60 nouns' brain data collapse to 3 factors: manipulation (hand), shelter (body in space), eating (mouth); 16 brain spots identify a noun. | After compression the human root set for concrete things is hand, body-in-space, mouth. | Just et al. 2010, PLoS ONE 5:e8622 [V] |
| Natural-speech meaning tiles the whole cortex; the first axis is social/emotional vs physical/perceptual. | The brain's top split is people-and-feeling vs things-and-places, not verb vs noun. | Huth et al. 2016, Nature 532:453 [V] |
| Abstract words are grounded in affect (valence) and in the mouth (speech, inner speech, asking). | Freedom bottoms out in feel + say. Talking and feeling are actions to the brain. | Kousta 2011; Vigliocco 2014; Borghi 2018 [V] |
| Reading "close the drawer" prepares the hand movement away from the body, including for abstract transfer ("Liz told you the story"). | A sentence carries a movement direction. Replication contested. | Glenberg & Kaschak 2002 [V] |
| The N400 is a mismatch signal at every word; left inferior frontal gyrus binds words into the running context in a loop with temporal memory. | The human "does this balance" has two parts: a per-word mismatch score and a combiner. | Kutas & Federmeier 2011; Hagoort 2013 [V] |
| A hub (anterior temporal lobe) holds a compressed, channel-free code; spokes hold the channel-specific codes. Lose a spoke, the concept survives; lose the hub, it dies. | Meaning needs a place that is not any one channel. In your terms: the gate, with the channels as its shards. | Lambon Ralph et al. 2017, Nat Rev Neurosci 18:42 [V] |

**What this says about roots [mine].** Every basis that worked has the same shape: perceive-by-channel (5 or 6), act-by-effector (4 or 5), move-in-space (toward, away, near, enter, open, fill), feel (valence, arousal), say, plus the language operators. Sizes that worked: 3, 8, 11, 25, 48, 65. So a machine root set in the 15 to 25 range is where the human data lands, and your 14 physical actions are the right order of magnitude. The human roots are *ports* (eye, ear, skin, mouth, hand, foot, gut) plus a few movements. The machine's ports are READ from a source, HEAR from the input, SAY to the output, CALL to the outside. See §7.

---

## 3. What the people who already wrote the formulas found (the linguistics and the AI)

| System | Its root set | Its middle layer | Its test for a formula | Status |
|---|---|---|---|---|
| **Schank, Conceptual Dependency** (1972–75) | 11 ACTs: ATRANS (change possession), PTRANS (change place), PROPEL (apply force), MOVE (move a body part), GRASP, INGEST, EXPEL, MTRANS (transfer information), MBUILD (build a thought), SPEAK, ATTEND. | roles: actor, object, recipient, direction, instrument; states as attribute(value) | Paraphrase collapse: "John gave Mary a book", "Mary took a book from John", "Mary was given a book" must reduce to one ATRANS graph; then the inferences must fall out (MARGIE 1973). | [V] |
| **Jackendoff, Conceptual Semantics; Dorr, LCS** (1983–2001) | GO, BE, STAY, CAUSE, LET, ACT, ACT_ON + fields (loc, poss, ident, perc, exist, circ, comm) + paths (to, from, toward, away_from, at, in, on). | 9,805 English verbs decomposed, GPL, downloaded: `Dorr_LCS_verbs-English_9805_verbs.lcs`. | The same GO/BE/PATH used across fields (keep = CAUSE(STAY) in place, possession and state alike): a formula is right when it survives the field change. | [V] |
| **VerbNet 3.4** | 153–162 predicates: has_location, motion, cause, contact, has_possession, transfer, path_rel, exist, perceive, ... | sub-events e1 e2 e3 with pre-state, process, post-state | Entailment: "I gave my dog a treat" = has_possession(e1, I, treat), ¬has_possession(e1, dog, treat), transfer(e2), has_possession(e3, dog, treat), ¬has_possession(e3, I, treat), cause(e2,e3). The formula must assert what is true before and after. | [V] |
| **Wierzbicka & Goddard, NSM** (1972–2024) | the 65 primes you use; formerly also IMAGINE, HAVE, UNDER, ON, WORLD, dropped. | about 180 "molecules" for English, about 25 near-universal (hands, mouth, eyes, water, fire, sky, ground, children, men, women, be born, mother, father, long, round, flat); four levels of nesting attested: mouth → water → drink. | Substitutability: the explication must replace the word in a sentence with no change of meaning; non-circularity; cross-translatability into every language. | [V] |
| **Dowty 1979** | DO, CAUSE, BECOME | — | Entailment tests: "x killed y" entails "y died" entails "y became not alive"; the "again" test separates CAUSE from BECOME. | [V, the "again" test; the kill/die wording U] |
| **Talmy, force dynamics; Johnson/Lakoff, image schemas** | Agonist vs Antagonist, tendency toward action or rest, stronger/weaker, result | CONTAINER, PATH, SOURCE-PATH-GOAL, BLOCKAGE, LINK, BALANCE, NEAR-FAR, PART-WHOLE, FULL-EMPTY, SPLITTING, MERGING ... | Stated as state + tendency + result, which is how a machine step is stated. | [V] |
| **Harnad; Vincent-Lamarre et al. 2016** | The dictionary's own structure: Kernel 5–9% of the words, Core about half of that, Minimal Grounding Set about half of the Kernel (LDOCE, Cambridge, Merriam-Webster, WordNet). | — | Grounding-set words are learned youngest, most concrete, most frequent. Many minimal sets exist, so "which roots" is a choice. | [V] |
| **Winograd SHRDLU; Woods; Johnson-Laird** | a word = a LISP procedure; "understanding grasp meant knowing how to grasp something" (Palmer 2023 on Winograd) | — | The procedure runs and the arm does it, including preconditions ("first get rid of Block2"). | [V] |
| **Feldman, Bailey 1997, x-schemas** | executing schemas (Petri nets) as verb meanings; push and shove share a schema and differ by force and velocity | — | Two-way test: label an observed action, and carry out an action on command. | [V] |
| **Siskind 2001, event logic** | SUPPORTS, CONTACTS, ATTACHED as force-dynamic primitives; verbs as changes in those over time | — | Run the definition over real video: pick-up fires when support passes from table to hand; assemble must also fire put-down and stack; six misses, no false alarms. | [V] |
| **Piantadosi, Tenenbaum & Goodman 2012** | number-word meanings as small typed programs over set primitives | — | Bayesian score: fit to the data, with a size penalty for programs that accept too much, and a simplicity prior. | [V] |
| **Executable semantic parsing** (Liang 2011, Berant 2013, Spider) | words as predicates / SQL fragments | — | The meaning-program is checked by EXECUTING it and comparing the denotation with the known answer; the lexicon is learned from (sentence, answer) pairs only. | [V] |
| **Metagol (Muggleton 2013)** | predicates learned from positive and negative examples | — | A hypothesis is accepted when it proves every positive and no negative, at the smallest clause count. | [V] |
| **DreamCoder (Ellis 2021)** | a growing library of program parts | — | Wake: programs that solve the examples; sleep: shared parts become new library functions. | [V] |

**What they converged on [mine].** Two tiers everywhere: a closed operator set of 10 to 20, and an open middle layer. Nobody got under about a dozen operators without smuggling meaning into a residual root, and the honest systems say so: Dorr's `kill` is `cause(x, go(ident, y, toward(at(y, kill+ed))))`, where `kill+ed` is a root left undecomposed. Expect a residue, and make the brain mark it as one.

---

## 4. Your worksheet, tested

Each formula was checked three ways: against what the five sources agree the word is made of (the model's own agree step, recomputed), against a counterexample (the Dowty/NSM substitution test), and against the Lancaster body profile where it applies. "−" below is the worksheet's minus.

| Prime | Worksheet | Verdict | Why | A formula that balances (guess, in primes and physics) |
|---|---|---|---|---|
| die | −live | **fails** | A stone does not live, and a stone did not die. "Not live" is a state; die is a change. Sources agree on: cease, lose, life, pass, out, become, extinct. hp2 computed it as a negative count. | die(x) = happen(x): before now live(x), after now not live(x). The NSM shape (from the published BREAK explication): "something happened to Y; because of this, after this Y was not living any more." In physics: READ state(x) at t1 = live, WRITE state(x) at t2 = not live, COMPARE t1 < t2. |
| before | −now | **fails** | after is also "not now"; one minus cannot tell them apart. The worksheet uses minus as unary here and binary for after. Before is two-place: x before y. Sources: earlier, ahead, front, preceding. | before(a, b) = COMPARE(time a, time b) → less. after(a, b) → more. hp built this. |
| after | now + | **fails as written** | Same reason, and "+" with no second operand. | see before |
| a long time | now ++ | **wrong kind** | A duration is an amount of time, not a position on the clock. hp2's reading gave clock². Sources: long, duration, period, extent. | a long time = time(amount) big. Same shape as far = distance big. |
| a short time | −−now | **fails** | Double minus returns now; hp2 got "a short time = now". | a short time = time(amount) small |
| for some time | now + now | **wrong kind** | Adds two clock readings. | for some time = time(amount) some |
| below | −above | **passes** | A sign flip on a signed vertical axis. Sources: above = higher than, over; below = lower than, under. Lancaster profiles identical (Visual 3.2 vs 3.3). But both are two-place: x above y. | above(x, y) = COMPARE(height x, height y) → more; below → less. The flip is less/more, which is what "−" on an axis means. |
| near | −far | **passes weakly** | As "not far" it is ordinary English (sources: near = not far, close, within a short distance). As arithmetic (hp2: −1) it is nonsense. | near = distance small; far = distance big. Four primes (long/short time, far/near) then share one shape: measure × size. |
| nothing (your note) | none + thing → null value | plausible | Matches VerbNet's ¬exist and Dowty. | there is not something |
| some = +one, many = some ^ ?, part = full / ? | | rough | These are points on a count scale: one < two < some < many < all; COMPARE(READ.count, a threshold). Part is a SPLIT of a whole. | |

**The one error under all of them.** The worksheet's "−" is doing three jobs: (1) **not** (invert yes/no), (2) **the opposite end of an axis** (swap less/more, or multiply a signed value by −1), and (3) **change of state** (what was true is now not true). On silicon these are three different actions: COMPARE-invert, NEGATE on a signed axis, and WRITE at t2 of a different value than READ at t1. Collapsing them is why die = −live and a short time = −−now come out wrong, and why hp2's arithmetic produced garbage while hp's hand-written actions did not. The fix is not a better guess per word; it is three operators laid separately, each with its own test.

**Second finding.** Your pairs are two-place relations, not properties: x before y, x above y, x near y. A formula with one hole cannot be right for them. The hole count is part of the meaning (NSM calls these valency frames: "someone does something to someone"; Dorr's `(* thing 1)`, `(* thing 2)`).

**Third finding.** Four primes share one shape, measure × size: a long time, a short time, far, near. The sources say this themselves (long and short appear only as modifiers of time, distance, extent). Jackendoff's thematic relations hypothesis says this is general: the same GO/BE/PATH functions serve place, possession and state. A formula that repeats across domains is the strongest kind of balance you can get, and the brain can look for it.

---

## 5. What I measured today (new numbers)

### 5.1 Open English WordNet 2025: the definitional graph (the dictionary measured as a graph)

Built from the OEWN 2025 JSON on hp (read-only copy). Single-word lemmas only; a word's definers are the words in its glosses; crude lemmatizer (plural, -ing, -ed). Result:

| Measure | Count | Share |
|---|---|---|
| Single-word lemmas | 68,828 | |
| Kernel (words left after repeatedly removing words that define nothing) | 16,434 | 23.9% |
| Core (largest strongly connected set of the kernel) | 15,387 | 22.4% |
| Greedy grounding set (words from which all 15,387 can be defined), before pruning | 4,474 | 6.5% |
| The same set after a pruning pass (time-capped, so an upper bound) | 3,359 | 4.9% |

My kernel is larger than Vincent-Lamarre's 5–9% because WordNet's glosses are long and my lemmatizer is crude, and because WordNet lists a, or, in, by, as as lemmas. The order of magnitude is the same: a few thousand grounding words define everything else.

**The most-defining words of the core, measured** (how many kernel words each one defines): a 10,091; or 10,028; in 6,233; an 3,846; by 3,780; be 3,431; as 3,096; have 2,110; on 1,668; act 1,518; used 1,512; being 1,312; one 1,288; especially 1,232; not 1,196; person 1,128; who 998; make 988; it 965; at 943; any 914; usually 900; state 833; form 820; cause 777; someone 760; other 760; manner 713; some 705; relate 694; body 642; quality 610; part 596; consist 570; time 537; small 524; place 516; people 480; action 475; another 471; group 468; out 462; two 458; can 453; through 452; between 446; more 442; produce 427; surface 406; use 401; characteristic 399; give 396; animal 385; up 381; large 379; force 378; move 375; position 375; together 372; order 368; water 363; property 363; plant 359; over 358; process 357; provide 344; characterize 342; substance 341; activity 341; degree 336; do 326; resemble 325; point 324; take 320; become 316; light 314; event 311; way 303; purpose 298; unit 297; good 297; result 294; line 290; work 290; number 289; sound 288; material 287; object 283; put 282; set 282; feeling 282; member 281; amount 278; condition 278; contain 272; system 269; capable 268; very 266; language 266; occur 265; physical 265; liquid 263; piece 260; quantity 260; area 257; power 256; shape 252; food 251; all 250; direction 244; change 244; side 242; long 240; structure 237; like 234; high 231; end 230; device 230; under 228; money 226; short 226; law 224; after 223; back 220; express 220; information 216; bring 216; metal 211; life 206; means 205.

**Read it in layers [mine], and it is the three-tier picture from §3, measured on your own source:**
- the operators: a, or, in, an, by, as, on, at, not, it, any, through, between, over, up, out, under, together, so, but, such, like;
- the primes: be, have, one, someone, other, some, body, part, time, small, place, people, two, can, more, move, do, good, very, all, side, long, after, no, like;
- the predicates (Schank/VerbNet's layer): act, make, cause, relate, consist, produce, use, give, force, position, provide, characterize, become, take, put, set, contain, occur, change, bring, express, resemble;
- the molecules (NSM's layer): person, animal, plant, water, light, food, money, surface, liquid, metal, sound, language, law, information, life, feeling, power;
- the measure words: degree, quantity, amount, number, unit, shape, form, state, quality, property, condition, process, event, activity, action, manner, way, purpose, result, direction, area, line, point, structure, system, group, member, piece, material, substance, object, device.

That last group is the one nobody's list has, and it is what definitions are actually written in. The full lists are in `wn_kernel_out.json` in the data folder.

### 5.2 The primes in the Lancaster norms (what each prime does in the human body)

Ratings 0 to 5 on 11 channels. Dominant channel and strength:

- **Pure ports:** see = Visual 5.0, Head 4.9. hear = Auditory 4.6, Head 4.7. say = Auditory 3.9, Mouth 4.0. touch = Haptic 4.9, Hand 4.9. feel = Haptic 4.7, Hand 4.5 (the body sense of feel; the emotion sense is Interoceptive 2.7).
- **Internal:** think = Interoceptive 3.5, Head 4.8. know = Interoceptive 2.7, Head 4.2. want = Interoceptive 3.4, Head 3.6. I = Interoceptive 3.9. like = Interoceptive 3.1, Head 3.8.
- **Whole-body action:** move = Foot 4.5, Hand 4.1, Torso 3.8. do = Hand 3.9, Foot 3.7, Torso 3.4. body = Torso 4.0.
- **Seen things and places:** thing, people, body, part, place, here, side, above, below, far, near, big, small, one, two, many, few all have Visual as the top channel (3.0 to 4.3) with nothing else high. Space and number are seen.
- **Time words have no body channel:** before 1.6, after 1.1, moment 1.6, time 2.3 (Interoceptive), now 2.5 (Interoceptive). Time is felt inside, weakly, and otherwise is an operator over the clock.
- **Logic and function words have no channel at all:** not 1.6, if 1.5, because 1.4, very 1.5, maybe 2.3, to 1.2, a 2.4 (the letter), at 2.1, is 1.7, plus 1.5. These are the operators. This matches Pulvermüller's finding exactly.
- **Live/die:** live = Visual 3.6, Head 3.6, Interoceptive 2.7; die = Visual 2.6, Head 2.8. Similar shape, lower everywhere: consistent with die being a change applied to live, not its negation.

**Checked against the model's told layer (`PRIME_ROOTS`) [mine].** see → READ and hear → HEAR and say → SAY are consistent. feel → HEAR COMPARE and touch → COMPARE HEAR are not: both are Haptic/Hand, that is a READ through the touch port, and the machine has no touch port, so they are gaps, not HEAR. you → FIND HEAR: you = Head 4.4, Interoceptive 3.7, the most "felt" prime after I; it is who the words are said to, which is state, so FIND state is closer. do → WRITE is too small: do is whole-body (Hand, Foot, Torso), the generic "run an action", which is CALL or a run, not a write. live → CLOCK and die → CLOCK SUBTRACT: live is a state (READ), die is a change (WRITE at t2), and neither is the clock.

### 5.3 The balance test, run on real data

Test: take a word, take a candidate decomposition into parts, average the parts' 11-channel profiles, and compare with the word's own profile (cosine). If meaning composes from parts, the composed profile should match the word's; a wrong decomposition should not.

| word | parts | agreement | random pairing |
|---|---|---|---|
| shout | say + more | 0.926 | 0.614 |
| whisper | say + small | 0.847 | 0.635 |
| kick | move + foot | 0.904 | 0.593 |
| walk | move + foot | 0.955 | 0.661 |
| grab | touch + hand | 0.993 | 0.687 |
| drink | mouth + water | 0.943 | 0.661 |
| eat | mouth + food | 0.954 | 0.654 |
| read | see + words | 0.938 | 0.851 |
| listen | hear | 0.982 | 0.617 |
| kill | do + die | 0.873 | 0.859 |
| run | move + foot + fast | 0.981 | 0.746 |
| write | hand + words | 0.972 | 0.782 |
| sing | say + music | 0.972 | 0.709 |
| push | hand + move | 0.976 | 0.722 |
| yell | say + loud | 0.969 | 0.586 |
| dance | move + body + music | 0.923 | 0.749 |
| **mean of 23** | | **0.935** | **0.681** |
| wrong: kick | say + hear | 0.246 | |
| wrong: shout | see + hand | 0.379 | |
| wrong: read | foot + mouth | 0.664 | |

So: a right decomposition scores about 0.9 and up, a random one about 0.7, a wrong one 0.25 to 0.66. The test is not the whole meaning (it cannot see time, cause or logic), but it is a real, numeric, source-grounded balance for the body part of meaning, over 39,707 words, and it is cheap: one row read per part, one average, one compare. The brain can be told this file as a source and run this on every formula it compiles. Note the weak case: kill = do + die scores 0.873 but random also scores 0.859 for kill, because kill's profile is flat (abstract). For abstract words this test has no power; §6 gives the tests that do.

---

## 6. The method: how to find a word's code, and how to grade it

This is the loop the research supports, in your terms. Every step is something the brain does to rows; the builder lays none of the meanings.

**Step 1. Spec.** The agreed defining words from two or more sources (the model's agree step, already built). Example, die: cease, lose, life, pass, out, become, extinct, not, live.

**Step 2. Candidates.** Compose candidate formulas from meanings the brain already runs, using the three operators separately: not, opposite-on-axis, become. Hole count comes from the sources' own frames ("x before y"). Where a defining word has no meaning, it is a hole with the word's name on it (Dorr's `kill+ed`: a labeled residue, not a fake meaning). Prior work's formula files (Dorr's 9,805 verbs, VerbNet's predicates, NSM's explications) are sources of candidates, never of truth: the brain reads them the way it reads a dictionary.

**Step 3. Grade each candidate with the tests below.** A candidate is:
- **pure guess** when it passes none;
- **makes sense** when it passes the cheap ones (agreement, body balance);
- **balances** when it passes execution on every known use and refuses every known counter-use;
- **wrong** the moment it fails execution or asserts a known negative.

| Test | What the brain does | Source of the method | Cost |
|---|---|---|---|
| **A. Execution against uses** | Run the formula on each use sentence from the sources as a program over the brain's state; the end state must match what the sentence says (after "gave", the recipient has it and the giver does not). | semantic parsing from denotations (Liang 2011, Berant 2013), VerbNet sub-events, SHRDLU | a run per use |
| **B. Entailment, positives and negatives** | From the formula, generate what must follow (x died → x is not alive now, x lived before) and what must not (x died → not: x is alive now). Check each against WordNet's antonym, hypernym and entailment links and against memory. Any proven negative = wrong. Smallest formula that proves all positives and no negative wins. | Dowty 1979; Metagol (Muggleton 2013) | a few reads |
| **C. Substitution** | Put the formula in place of the word in its own definition sentences and in uses; the run must reach the same end state; and two words with different meanings must not collapse to the same formula (die vs not live). | NSM substitutability; Schank's paraphrase collapse | a run per sentence |
| **D. Cross-source agreement** | The formula's parts must be in the agreed spec of two or more sources (already built: agree). Later, with other-language dictionaries, the formula must survive translation. | NSM cross-translatability; your agree step | one read |
| **E. Body balance** | The composed Lancaster profile of the parts must match the word's profile (§5.3): 0.9 and up balances, under 0.7 does not. No power on abstract words. | Lynott 2020 norms; Mitchell 2008 composition | one row per part |
| **F. Size penalty** | A formula that accepts far more situations than the uses needed is still a guess; the penalty grows with each consistent example that a tighter formula would also fit. | Xu & Tenenbaum 2007; Piantadosi 2012 | a count |

Order: A first (does it compute the right thing here), then B (does it refuse the known wrong cases), then C, then E and D as cheap confirmations, then F to keep it honest. A formula is **held** after A and B on two or more uses; **understood** after it passes an unseen use (your existing definition); **wired** only then.

**Where the negatives come from.** The brain has no teacher most of the time. The literature's answer: antonym links in WordNet (checked in OEWN 2025: the verb die's antonym is be born; the adjective live's antonym is dead), the "a positive for one word is a weak negative for its rivals" rule (Regier's mutual exclusivity), and cross-situational shrinking of "must contain" and "may contain" sets until they meet (Siskind 1996). All three are rows the brain can read.

---

## 7. The roots: what the evidence says they are

Not assigned; measured, from §2 and §5.

1. **Silicon roots** stay the 14 physical actions. The human equivalents are ports: eye → READ a visual source; ear → HEAR; skin and hand → a touch port the machine does not have (feel and touch are honest gaps); mouth → SAY; gut (interoception) → READ self and state; hand/foot/torso → MOVE and CALL (run a thing). The prime layer should be told by port, not by my guesses: each prime's dominant Lancaster channel names the port it is a READ or WRITE on.
2. **Three operators, laid separately:** not (invert yes/no), opposite-on-axis (less ↔ more, or −1 on a signed value), become (state at t2 differs from state at t1). Plus the ones the worksheet already has: more (+), a lot more (++), part (/), join (*). The hop operators you proposed (− step back, * test fork, / choose) are mechanics on the run, not meanings, and the page says so correctly.
3. **The function words are operators and come first.** The most-needed ledger and the neuroscience agree. Guesses, each to be tested, in rows: a/an = FIND any one; the = FIND the one in state; of = part-of or relation; to = path toward; from = path away; in = inside; on = touching above; at = place; by = cause or instrument; with = join; and = join; or = choose; not = invert; if = branch; because = cause link; as/like = compare same; than = compare on a measure. Pulvermüller's result says they have no body channel, so the body balance (E) does not apply to them; tests A and C do.
4. **The predicate layer** (act, make, cause, become, give, take, put, contain, change, use, move, relate) and **the measure layer** (amount, number, degree, state, form, quality, process, event) are what definitions are written in, measured. They are the next words to find after the operators, before any noun.
5. **Expect a residue.** Dorr, VerbNet and NSM all keep one. The brain should write it as a named hole (kill+ed) and count it, so the residue shrinks visibly over time instead of hiding inside a fake meaning.

---

## 8. What is blatantly wrong, in one list

- die = −live, before = −now, a short time = −−now: wrong (§4).
- One "−" for three operations: wrong (§4).
- One-hole formulas for two-place relations (before, above, near): wrong.
- Durations as clock positions: wrong kind.
- In the model's told layer: feel and touch as HEAR; do as WRITE; live and die as CLOCK: wrong against measured data (§5.2).
- hp2's literal arithmetic on the worksheet: four of eight outputs are meaningless numbers.
- hp2's meaning test (compare the candidate's place to the word's place) never runs the candidate on a use: it is a place check, not a meaning check.
- The letters-and-keyboard cipher idea (your late-September messages): the research is settled against it. The form of a word is arbitrary (Saussure; and the Lancaster and Binder data show meaning tracks experience, not spelling). You said the same on 10-22: "the relationship of those letters is actually meaningless". Letters are the encoder's business only.
- Not wrong, but open: the worksheet pairs that pass (below, near) pass only because the axis is signed. The brain must hold the axis, not just the flip.

---

## 9. Where this leaves the build order

The data gives the order; I did not choose it.

1. Lay the three operators (not, opposite-on-axis, become) as separate told actions, each with tests A and B on the eight worksheet primes. The eight then compile from the sources, and the die/before/short-time failures become visible as rows.
2. Lay the function-word operators as guesses with tests A and C. They lead the most-needed ledger at every count.
3. Tell the brain the two measured sources: the Lancaster norms (39,707 rows, 11 columns) and Binder's ratings (535 rows, 65 columns), so test E is one read per part. Both are in the data folder. Dorr's verb file (9,805 formulas) and VerbNet are candidate sources, read like a dictionary.
4. Let the brain run the loop in §6 on the primes by port (§7.1), then on the predicate and measure layers (§7.4), then on nouns. Each formula carries its grade (guess, makes sense, balances, wrong) and its residue count.
5. The point-of-connection measure stays yours: the absent list reaching empty. Add one number next to it: total residue, the count of named holes still inside held formulas.

---

## 10. Files

In `Downloads/Neuron-Meaning-Data-2026-10-22/`:
- `Lancaster_sensorimotor_norms_39707_words.csv`: Lynott et al. 2020, CC-BY, from https://osf.io/7emr6/ (the Data component).
- `Binder2016_65_attributes_535_words.csv` and `Binder2016_ReadMe.txt`: from https://www.neuro.mcw.edu/representations/word_ratings.zip.
- `Dorr_LCS_verbs-English_9805_verbs.lcs`: GPL, from https://github.com/ihmc/LCS.
- `wn_kernel_out.json`: the WordNet 2025 kernel (16,434), core (15,387), pruned grounding set (3,359) and the top-400 defining-word ranking, computed today.

Not downloaded, pointers only: VerbNet 3.4 https://github.com/cu-clear/verbnet; Mitchell 2008 https://www.cs.cmu.edu/~tom/pubs/science2008.pdf; Fernandino 2022 https://pmc.ncbi.nlm.nih.gov/articles/PMC8832989/; Vincent-Lamarre 2016 https://arxiv.org/abs/1308.2428; Piantadosi 2012 https://colala.berkeley.edu/papers/piantadosi2012bootstrapping.pdf; Siskind 2001 https://arxiv.org/abs/1106.0256; Liang 2011 https://arxiv.org/abs/1109.6841; DreamCoder https://arxiv.org/abs/2006.08381; Metagol https://github.com/metagol/metagol; NSM https://nsm-approach.net/; Schank CD https://people.cs.pitt.edu/~wiebe/courses/CS3730/Spring2013/cd.pdf; Hauk 2004 https://pages.ucsd.edu/~scoulson/Courses/200/Hauketal2004_SomatotopicActionVerbOrg.pdf; Pulvermüller 1999 BBS 22:253; Lambon Ralph 2017 doi 10.1038/nrn.2016.150; Hagoort 2013 https://pmc.ncbi.nlm.nih.gov/articles/PMC3709422/; Just 2010 PLoS ONE 5:e8622; Huth 2016 https://pmc.ncbi.nlm.nih.gov/articles/PMC4852309/; Borghi 2018 https://pmc.ncbi.nlm.nih.gov/articles/PMC6015830/.
