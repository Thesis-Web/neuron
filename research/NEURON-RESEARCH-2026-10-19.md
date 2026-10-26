# NEURON RESEARCH

*2026-10-19. Published work behind the owner's ideas, gathered so the builders understand the **why**. These are not new instructions: where anything here seems to differ from NOW or the blueprint, NOW and the blueprint win. Every citation was checked on 10-19 against Crossref, arXiv or the publisher's page; the few that could only be partly checked are marked.*

---

## 1. Meaning is not the definition

The owner: "words by themselves are meaningless; it's the code that the word or words make happen." A definition describes the meaning; the meaning is the action.

- **The dictionary-go-round.** Harnad, S. (1990). "The symbol grounding problem." *Physica D* 42: 335–346. https://doi.org/10.1016/0167-2789(90)90087-6
  - You can't get meaning from a dictionary alone, because every word is defined by more words.
  - At least some words have to be tied directly to something outside the words: sensing or acting.
  - This is the owner's "shorthand code described by shorthand code, and the root was lost".
- **How few words need grounding.** Vincent-Lamarre, P., Massé, A.B., Lopes, M., Lord, M., Marcotte, O., & Harnad, S. (2016). "The Latent Structure of Dictionaries." *Topics in Cognitive Science* 8(3): 625–659. https://doi.org/10.1111/tops.12211
  - The authors treated a dictionary as a graph of which words define which.
  - Repeatedly removing words that define nothing else leaves a **Kernel** of about 10% of the words.
  - The smallest set that can define all the rest, the **MinSet**, is about **1%**, and there are many possible MinSets.
  - Grounding one MinSet in action is in principle enough: every other word can then be built by definition.
  - This is the research version of "the root primitives and the primes".
- **Meaning as a procedure.**
  - Woods, W.A. (1968). "Procedural semantics for a question-answering machine." *AFIPS Fall Joint Computer Conference*. https://doi.org/10.1145/1476589.1476653
  - Woods, W.A. (1981). "Procedural semantics as a theory of meaning." In *Elements of Discourse Understanding*, Cambridge UP. https://philarchive.org/rec/WOOPSA
  - Johnson-Laird, P.N. (1977). "Procedural semantics." *Cognition* 5(3): 189–214. https://doi.org/10.1016/0010-0277(77)90001-4
  - All three argue that the meaning of an expression is the procedure it runs. That is close to "a word is shorthand code".
- **The warning against it.** Fodor, J.A. (1978). "Tom Swift and his procedural grandmother." *Cognition* 6: 229–247. https://doi.org/10.1016/0010-0277(78)90015-X
  - Turning words into machine procedures is just more translation unless those procedures reach the world.
  - For Neuron, the actions must bottom out in real physics (the physics gates, sources, the machine). They can't stop at other words.
- **Use.** Wittgenstein, L. (1953). *Philosophical Investigations*, §43: "for a large class of cases … the meaning of a word is its use in the language."
- **Form is not meaning.** Bender, E.M., & Koller, A. (2020). "Climbing towards NLU: On Meaning, Form, and Understanding in the Age of Data." *ACL 2020*, 5185–5198. https://doi.org/10.18653/v1/2020.acl-main.463
  - A system trained only on word forms can't learn meaning.
  - This is the gap between an LLM and what Neuron is trying to be.
- **The brain stores word meaning as action.**
  - Pulvermüller, F. (2005). "Brain mechanisms linking language and action." *Nature Reviews Neuroscience* 6: 576–582. https://doi.org/10.1038/nrn1706
    - Action words switch on the motor areas for the body part they name: lick (the mouth), pick (the hand), kick (the leg).
  - Glenberg, A.M., & Kaschak, M.P. (2002). "Grounding language in action." *Psychonomic Bulletin & Review* 9(3): 558–565. https://doi.org/10.3758/BF03196313
    - People understand "close the drawer" faster when their answering movement goes the same way.
    - Understanding a sentence runs the action it describes.
- **The primes.**
  - Wierzbicka, A. (1996). *Semantics: Primes and Universals*. Oxford UP. https://doi.org/10.1093/oso/9780198700029.001.0001
  - Goddard, C., & Wierzbicka, A. (2014). *Words and Meanings*. Oxford UP. https://doi.org/10.1093/acprof:oso/9780199668434.001.0001
  - Every word can be explained in a small set of meanings found in every language.
  - Early lists had 63 primes; the current list has 65.
  - The primes can't be defined. That is why they need actions (blueprint §16).

## 2. Told, taught, learned

The owner: the base is **told**, because "it can't learn until it can learn"; teaching must not turn into giving answers; **learning** is the brain finding the formula itself.

- **Told becomes learned by compiling.** Anderson, J.R. (1982). "Acquisition of cognitive skill." *Psychological Review* 89(4): 369–406. https://doi.org/10.1037/0033-295X.89.4.369
  - Told knowledge starts as facts that have to be interpreted, slowly.
  - Practice compiles those facts into procedures that run directly.
  - Told → learned → cheap.
- **Instrumental vs relational.** Skemp, R.R. (1976). "Relational understanding and instrumental understanding." *Mathematics Teaching* 77: 20–26. (No DOI; https://www.jstor.org/stable/41182357)
  - Instrumental understanding is "rules without reasons": a told procedure.
  - Relational understanding is knowing what to do *and why*: having the formula.
- **When telling works.** Schwartz, D.L., & Bransford, J.D. (1998). "A Time for Telling." *Cognition and Instruction* 16(4): 475–522. https://doi.org/10.1207/s1532690xci1604_4
  - Students who first explored contrasting cases on their own learned more from a later lecture, and applied it further, than students who were told first.
  - Telling works after the learner has built a place for it to land.
- **Struggle first.**
  - Kapur, M. (2008). "Productive Failure." *Cognition and Instruction* 26(3): 379–424. https://doi.org/10.1080/07370000802212669
  - Sinha, T., & Kapur, M. (2021). "When Problem Solving Followed by Instruction Works." *Review of Educational Research* 91: 761–798. https://doi.org/10.3102/00346543211019105
  - Trying, and failing, before being shown improves later learning and transfer.
  - Across 53 studies the effect is moderate (g = 0.36).
- **Discovery needs something to steer it.**
  - Kirschner, P.A., Sweller, J., & Clark, R.E. (2006). "Why Minimal Guidance During Instruction Does Not Work." *Educational Psychologist* 41(2): 75–86. https://doi.org/10.1207/s15326985ep4102_1
  - Alfieri, L., et al. (2011). "Does discovery-based instruction enhance learning?" *Journal of Educational Psychology* 103(1): 1–18. https://doi.org/10.1037/a0021017
  - Across 164 studies:
    - discovery with no help did **worse** than being told (d = −0.38);
    - discovery with feedback, worked examples or prompts did **better** than other methods (d = +0.30).
  - For Neuron this is the stove and the parent: the baby finds things itself, but consequences, and a parent's yes or no, steer it.
- **Producing beats receiving.**
  - Chi, M.T.H., & Wylie, R. (2014). "The ICAP Framework." *Educational Psychologist* 49(4): 219–243. https://doi.org/10.1080/00461520.2014.965823
    - Learning ranks interactive > constructive > active > passive.
    - Being told is passive.
  - Slamecka, N.J., & Graf, P. (1978). "The generation effect." *Journal of Experimental Psychology: Human Learning and Memory* 4(6): 592–604. https://doi.org/10.1037/0278-7393.4.6.592
    - What you produce yourself is remembered better than what you read.

## 3. Learning, understanding, applying

- **The levels.** Anderson, L.W., & Krathwohl, D.R. (eds.) (2001). *A Taxonomy for Learning, Teaching, and Assessing* (the revised Bloom's taxonomy). Longman. Overview: Krathwohl (2002), *Theory Into Practice* 41(4): 212–218. https://doi.org/10.1207/s15430421tip4104_2
  - The thinking levels are remember, understand, apply, analyze, evaluate, create.
  - It also separates **factual** from **procedural** knowledge, which matches definition vs action.
- **Applying is transfer.**
  - Perkins, D.N., & Salomon, G. (1992). "Transfer of learning." *International Encyclopedia of Education*, 2nd ed. (Sources disagree on the volume.) https://openlab.citytech.cuny.edu/fywpd/files/2020/01/transferoflearning.pdf
    - Transfer means learning in one setting changes what you do in another. It runs from near transfer to far.
  - Barnett, S.M., & Ceci, S.J. (2002). "When and where do we apply what we learn? A taxonomy for far transfer." *Psychological Bulletin* 128(4): 612–637. https://doi.org/10.1037/0033-2909.128.4.612
    - A grid of how far "far" is: across subject, place, time, purpose, social setting and format.
    - The owner's test ("apply it to itself") is far transfer.
- **Intelligence as how cheaply it learns.** Chollet, F. (2019). "On the Measure of Intelligence." arXiv:1911.01547. https://arxiv.org/abs/1911.01547
  - Intelligence is how efficiently a system picks up a skill it was never given. It is not how many skills it holds.
- **What learning machines need.** Lake, B.M., Ullman, T.D., Tenenbaum, J.B., & Gershman, S.J. (2017). "Building machines that learn and think like people." *Behavioral and Brain Sciences* 40, e253. https://doi.org/10.1017/S0140525X16001837
  - Causal models, building wholes from reusable parts, and learning how to learn.

## 4. Learning is compute; using is retrieval (energy)

The owner: "learn as compute and use of that as mainly a runtime is a huge energy save." Blueprint §0, rule 2.

- **Automatic means remembered.** Logan, G.D. (1988). "Toward an instance theory of automatization." *Psychological Review* 95(4): 492–527. https://doi.org/10.1037/0033-295X.95.4.492
  - Skill becomes automatic when it rests on "single-step direct-access retrieval of past solutions from memory".
  - Beginners compute; with practice, memory wins the race.
  - This is the strongest citation for rule 2.
- **Memoization.** Michie, D. (1968). "'Memo' functions and machine learning." *Nature* 218: 19–22. https://doi.org/10.1038/218019a0
  - A function keeps a table of the answers it has already worked out.
- **Chunking.** Laird, J.E., Rosenbloom, P.S., & Newell, A. (1986). "Chunking in Soar." *Machine Learning* 1(1): 11–46. https://doi.org/10.1007/BF00116249
  - Each solved problem is saved as a new rule, so next time it is recalled instead of solved again.
- **Sleep, and the HC.** McClelland, J.L., McNaughton, B.L., & O'Reilly, R.C. (1995). "Why there are complementary learning systems in the hippocampus and neocortex." *Psychological Review* 102(3): 419–457. https://doi.org/10.1037/0033-295X.102.3.419
  - The hippocampus learns fast.
  - The neocortex learns slowly, by replaying memories mixed together, so new learning doesn't overwrite old.
- **Finding formulas in sleep.** Ellis, K., et al. (2021). "DreamCoder: Bootstrapping inductive program synthesis with wake-sleep library learning." *PLDI '21*, 835–850. https://doi.org/10.1145/3453483.3454080
  - Awake, it solves problems by searching for programs.
  - Asleep, it pulls the shared parts of its solutions into new reusable functions.
  - **Learning means adding a function; using one afterwards is cheap.**
  - The difference from Neuron: in the blueprint, a formula found asleep stays a guess until it is tested awake.
- **Finding the shared formula.** Plotkin, G.D. (1970). "A note on inductive generalization." *Machine Intelligence 5*, 153–163. (Checked through secondary sources only.)
  - The mechanical way to get the most specific pattern that covers several examples. This is blueprint §13's "generalize".
- **The brain runs sparse.** Attwell, D., & Laughlin, S.B. (2001). "An energy budget for signaling in the grey matter of the brain." *Journal of Cerebral Blood Flow & Metabolism* 21(10): 1133–1145. https://doi.org/10.1097/00004647-200110000-00001
  - Signaling costs so much energy that the most efficient codes have 15% or fewer neurons active at once.

## 5. QKV belongs on the guessing side

The owner: "QKV can be part of this, but only in the guessing side, applied to small portions of the corpus; probably lots of weights, but over small groups of data." Blueprint §10.6.

- **Attention is weighted recall.**
  - Vaswani, A., et al. (2017). "Attention Is All You Need." *NeurIPS*. https://arxiv.org/abs/1706.03762
    - A query weighs each stored value by how well the query matches that value's key.
  - Ramsauer, H., et al. (2021). "Hopfield Networks is All You Need." *ICLR*. https://arxiv.org/abs/2008.02217
    - Attention turns out to be the update rule of an associative memory: it recalls the closest stored pattern.
  - Geva, M., Schuster, R., Berant, J., & Levy, O. (2021). "Transformer Feed-Forward Layers Are Key-Value Memories." *EMNLP*. https://doi.org/10.18653/v1/2021.emnlp-main.446
    - Even the non-attention layers act as key-value lookups.
  - Taken together, QKV is a fast, approximate way to recall what is most similar. That is a guess, which is why it belongs on the guessing side.
- **Weights used on small slices.** Fedus, W., Zoph, B., & Shazeer, N. (2022). "Switch Transformers." *JMLR* 23(120): 1–39. https://jmlr.org/papers/v23/21-0998.html
  - These models "select different parameters for each incoming example".
  - There are a huge number of weights, but each input uses only a small slice: the owner's "lots of weights, small groups".
- **Find the small group cheaply first, then weigh it.**
  - Khandelwal, U., et al. (2020). "Generalization through Memorization: Nearest Neighbor Language Models." *ICLR*. https://arxiv.org/abs/1911.00172
  - Wu, Y., et al. (2022). "Memorizing Transformers." *ICLR*. https://arxiv.org/abs/2203.08913
  - Lewis, P., et al. (2020). "Retrieval-Augmented Generation." *NeurIPS*. https://arxiv.org/abs/2005.11401
  - In all three, a lookup first picks a small set, and only that set gets weighed. The store can be swapped without retraining.
  - In Neuron, the graph's own reach finds the small group: neighbours, similar shapes, one topic. Only then may QKV weigh it.
- **Fast guess, slow reason.** Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
  - System 1 is fast and automatic; System 2 is slow and effortful.
  - Some of the priming studies in the book have since failed to replicate.

## 6. What this means for the builds

These are pointers, not changes. Each one matches something NOW or the blueprint already says.

1. **Ground a small root in action, and build everything else by definition** (Harnad; Vincent-Lamarre et al.). This is the primes laid with actions (blueprint §16), and why a prime without an action is a gap, not a word.
2. **Actions must reach the world, not just other words** (Fodor). This is the physics gates and the sources.
3. **Discovery needs consequences and a parent's yes or no to steer it** (Alfieri; Kirschner). But never answers given to it (Schwartz & Bransford; Kapur).
4. **Memory first; compute only when nothing is remembered; every solved run becomes a recall** (Logan; Michie; Soar; Anderson). This is blueprint §0, rule 2, and §7.6.
5. **Sleep consolidates and finds shared formulas** (McClelland et al.; DreamCoder). This is blueprint §9.6 and §13. What sleep finds stays a guess until it is tested awake.
6. **QKV only weighs a small group that the graph has already found** (Ramsauer; Switch; kNN-LM; RAG). It runs only after the knowns, and it produces a labeled guess (blueprint §10.6).
7. **Judge by far transfer, and by how cheaply it learned** (Barnett & Ceci; Chollet). That is the owner's test.

*Not used:* a 1975 Woods paper on procedural semantics (none could be confirmed; the 1968 and 1981 papers are cited instead).
