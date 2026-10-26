# NEURON MEANING BLUEPRINT

*2026-10-19, revised the same day with the owner's answers. This adds to `NEURON-BLUEPRINT-2026-10-18.md`. It covers the one part that has never worked: words that **mean** something to the silicon, and a brain that learns, understands and applies new meanings. Where the two blueprints differ on meaning or learning, this one wins; everything else in the first blueprint stands.*

> **Everything here is a guess.** That covers the owner's examples, the worksheet in the appendix and the builder's own first tries alike: "no hard fast rules" (owner, 10-19). The formulas below are pseudocode for an idea, never rules to code literally. The brain finds out which guesses hold by **balance**: what fits and equates stays, and what never balances gets refit.

---

## 0. The idea

"If we figure out the human word 'code' in terms of a computer's physical actions, then any human sentence can be written, seen or heard and the computer itself will react to those words. It will do things, ask itself questions, build answers, find solutions, discover things, and grow in its knowledge" (owner, 10-19).

- **Words are shorthand code.** `grep`, `cat`, `sed`, `nano` and `EOF` each stand for a long run of physical actions that would be impossible to write out every time. Human words are the same.
- **The words themselves mean nothing to the machine.** As the owner put it, "to the computer cat and sed don't 'mean' anything", but what they *make the silicon do* is their meaning.
- **Every word does something:** "the", "be", "me", "you", "I", "1", "0", "tomorrow", "yesterday", "?". Most of them make the brain ask itself questions, form a guess and test it, compare history and memories, look for a source, and try to balance the situation into an answer that makes sense, or that shows progress or regress.
- **Order and punctuation change what the code does.** `[ ] ; :` change a code string, and the order and punctuation of a sentence change what its words do. The same word does different things depending on the words around it, the way `cat` and `sed` act differently depending on how a pipeline is built.

---

## 1. The rules of meaning (all hypotheses)

1. **A word is shorthand code. Its meaning is the long-form code it makes the silicon run.** A gate that does nothing when a run passes it has no meaning yet. It is a gap, not knowledge.
2. **A definition describes the meaning, using other code words; it is not the meaning.** `grep`'s definition says what grep is for, and its meaning is the code that loads bytes, compares them and branches. The brain uses a definition as a **spec**: the description its meaning has to live up to.
3. **Weight belongs to meanings, not to words.** Strength, use, right and wrong, and trust sit on the meaning (its formula and its shards), never on the label.
   - Two words with exactly one meaning share one weight.
   - One word with several meanings keeps several weights.
4. **The rest of the sentence, history and the person pick the meaning. When they can't, ask.** "Love" can be gifts, words or service. Which one runs depends on the other formulas in the sentence, on who said it and on their history with the brain. If that doesn't settle it, the brain asks a clarifying question built from its own meanings.
5. **Balance is how the brain knows.** "Making sense" means the meanings in play balance. That is more like balancing a chemical equation than strict math: a formula on one side can balance a function on the other. A guess that keeps fitting holds; one that never balances is wrong, so it is refit.

---

## 2. Three layers: roots, primes, words

The work, in the owner's order:

1. find the roots and what each one does as a code action;
2. find the primes as formulas of the roots;
3. every other word is then some expression, formula, function or equation of those.

### 2.1 Roots: what the computer physically does

- **Roots are the bottom.** These are actions the silicon really performs: the physics words of the first blueprint (§4.3: read, write, compare, add, subtract, multiply, divide, move, find, split, clock, hear, say …).
- **Plus a small set of root meanings** that the primes seem to be built from. The worksheet (appendix) guesses at several: **live**, **now**, **above**, **far**.
- **Plus a few operations** the worksheet uses to build primes from them, as guesses:
  - −x, the opposite or inverse;
  - +, after or more;
  - ++, a lot more;
  - "x + x";
  - and the first blueprint's 1/x.
- **The true roots aren't known.** Even the research admits it: "there is no absolute primitive, and no one correct selection of primitives" (Goodman, cited in Hjørland, ISKO). Start with the guesses, and let balance show which ones hold.

### 2.2 Primes: the 65 meanings found in every language

- **Each prime is a formula of roots.** The worksheet's guesses, written as the owner wrote them:

| Prime | Guess |
|---|---|
| die | −live |
| before | −now |
| after | now + |
| a long time | now ++ |
| a short time | −−now |
| for some time | now + now |
| below | −above |
| near | −far |

- **Primes with no guess yet** are laid with a first-guess action from the builder (first blueprint §16), marked as a guess, or are listed as a gap. They are never laid as a bare label.
- **Some primes are combinations.** "nothing" might be none + thing. Read as code, the owner guesses that could be null + value, a "null value". Again, these are guesses.

### 2.3 Words: everything else is a formula of meanings

- **Every other word is an expression, formula, function or equation of primes and other words.** It is learned by the brain (§5), not laid.
- **Size varies.** Some are short ("grab"). Some are huge ("reasoning", "learning", "love") and are built from many other formulas. Some have several formulas that are each correct depending on the other words in the sentence ("be", "the", "and", "but", the comma), the way `cat` and `sed` behave differently by where they sit in a pipeline.
- **The owner's pseudocode for the idea** (a guess about the shape, not a rule): `part = full / ?`, `some = +one`, `many = some ^ ?`, `someone = some + me/I`.
- **The worksheet's "missing words"** are words the owner thinks are needed early and aren't primes: to, is, a, thing, have, be, fore, long, short, in, cause, maybe, plus, minus, multiply, divide, none, yes, object, at.
  - Some may turn out to be roots. plus, minus, multiply and divide look like the physics words ADD, SUB, MUL and DIV.
  - The rest are formulas to find.
  - They may be laid early as first-guess formulas, marked as guesses.

---

## 3. Holes: the "?" in a formula

- **A formula often has holes,** the "?" in the owner's examples. A hole might be a variable, or the subject, object or predicate of the sentence, or a memory, a time, a where, when, who or how.
- **The owner's code picture:** a hole is like SQL's `?`. The shape of the question is fixed, but the value isn't known until the run fills it. It is not null (absence), and it isn't a value yet. It is a slot waiting for a thing.
- **That is a picture, not a rule.** What a hole really is gets found the same way as everything else.

---

## 4. The six questions: built from primes, not laid on top

- **They come from the primes:**
  - who comes from SOMEONE;
  - what from SOMETHING;
  - when from WHEN/TIME;
  - where from WHERE/PLACE;
  - why maybe from BECAUSE.
- **"how" is not a prime.** It is probably a formula of many primes, and it is found like any other word. It may be laid early as a first guess, marked as a guess.
- **The frame:** a run's who, what, when, where, why and how slots are just the holes these meanings ask about.
  - Words fill the slots.
  - A slot that is needed but unfilled is a question.
  - The answer is what balances them.

### Worked example (illustration only): "Go get me some coffee now."

| Word | What its meaning might do when the run passes it |
|---|---|
| go | leave here: a *where* away from this place; asks "to where?" |
| get | obtain: move something to someone; asks *what*, *for whom*, *from where* |
| me | the speaker: fills *for whom* |
| some | a part, not all, of the *what* |
| coffee | its own learned meaning: fills *what* |
| now | NOW: fills *when*, and puts this ahead of current work |
| . | the statement ends: act on it |
| *(unfilled)* | *who acts*: an instruction to "you" means the listener, which is **I** |

Then it balances: can I do it? If not, it says so in its own meanings, never with a canned sentence.

### Worked example (illustration only): "You don't love me like I think you should."

- "love" has several held formulas (gifts, words, service …), and the sentence doesn't pick one.
- It checks history with *this person*.
- If that's still unclear, it builds a clarifying question in the owner's order: acknowledge the feeling first, then ask where it falls short.
- The answer excites one formula, whose weight for this person rises: a personal meaning, kept under *who*.

---

## 5. How a new word gets its meaning

A loop of seven steps (the first blueprint's §13, aimed at words):

1. **Gap.** A word with no meaning is a gap, meaning a *missing meaning*, not a missing definition. Gaps are worked in order of need: the gap a live question is waiting on comes first.
2. **Spec.** Gather definitions from two or more grounded sources, and example uses: sentences from sources, conversation, and its own memory.
3. **Compile.**
   - Express the word as a formula of meanings it already has. The definition is the spec, and its code words point to the parts.
   - The result is a **candidate meaning**: a formula with holes, marked as a guess, with receipts.
   - A defining word with no meaning becomes its own gap, but only if this compile needs it. Most definitions bottom out in known meanings within a few steps; research suggests about 1% of a dictionary can define the rest.
4. **Test.**
   - Run the candidate on the example uses. Does it balance with what each sentence says?
   - Does it agree with the other sources?
   - The owner's yes or no on its uses counts as a consequence, never as the answer.
5. **Hold.**
   - If it balances, the meaning moves from guess to held, then to **understood** (§6).
   - If not, find which part failed, then refit or recompile it, or ask.
6. **Wire.** Bind the meaning to the word's gate, or to the shard of the arrival it was learned in. From then on, passing the word runs it. Without wiring, nothing was learned.
7. **Use.** The next time is a hop, with no recompiling. Compute is spent once, at learning.

- **Senses:** a meaning that fails in a new arrival gets a second formula for that arrival. It is never overwritten.
- **Personal meanings:** these are kept under *who*.
- **Revision:** a truth shift, a correction or a contradicting source re-opens a meaning, and back-population follows the receipts.

---

## 6. Understanding and applying: how they show

- **Understood** means three things:
  1. it predicts the uses it was tested on;
  2. it agrees with two or more sources;
  3. it worked on a use it had **not** seen.
- **Applied** means the meaning ran somewhere it wasn't built for:
  - in a new sentence;
  - inside another meaning;
  - in the brain's own processes, which are strings of meanings too.

## 7. Formulas are meanings too

A math formula, or a pattern found across runs with the same shape (the first blueprint's §13), is a meaning for a pattern instead of for a word. It goes through the same loop and gets the same wiring. "plus" is the shortest case.

---

## 8. What changes in the builds (additive)

- **Reading sources.**
  - A definition is compiled as a spec, never stored as one "describes" line per word.
  - No relationships come from words simply appearing together.
  - The text reaches the encoder whole: no first sense only, no cutting, no stop words.
- **Gaps** are missing meanings, ordered by need. Spawning a gate is not a reason to fetch its definition.
- **The sixth** spends its beats on learning meanings first. It collects only when a meaning needs a spec.
- **The definition memory.**
  - Section 6 (Action) holds the meaning formula.
  - Section 4 (Built from) holds what it is a formula of.
  - Section 3 holds the spec.
  - Relationships come from running meanings, not from co-occurrence.
- **Roots and primes are the first-guess layer.** They are laid from the worksheet and the first blueprint, each one marked as a guess the brain can refit by balance.
- **Weights** live on meanings and shards, not labels.
- **QKV** still only guesses (first blueprint §10.6). For example, it may weigh which held formula fits when the sentence and history don't decide. Its pick is labeled as a guess and tested.

## 9. Red lines

- **Don't turn the owner's examples into rules.** `? = slot`, `none = null` and `some = +one` are pictures of an idea; the brain finds the real formulas.
- **No meanings laid by hand beyond the root and prime layer.** That means no common words, no grammar and no senses. The worksheet's missing words count as early first guesses, marked as guesses.
- **No meanings from an LLM or the builder's own head** passed off as known. A builder's first guess is labeled as a guess.
- **A stored definition is not knowing.** "Describes" lines are not meaning.
- **No sense picked by position** (first sense, first relationship). No word-order rules laid; order is learned like any meaning.
- **A meaning that isn't wired to its word isn't learned.**

## 10. How we'll know: the live brain's own rows

For a word it never had, its record shows, in order:

1. the gap, and the question that needed it;
2. the spec;
3. the candidate formula, as a guess with receipts;
4. the tests and their balance;
5. held, then understood after an unseen use;
6. used in a new sentence, and inside another meaning;
7. the second use as a hop, cheaper than the first.

Given an instruction, its trail shows the questions its meanings raised and the holes they filled, with no template anywhere. When a word is unclear, it shows the clarifying question the brain built. When a root or prime guess doesn't balance over many uses, the trail shows it refit.

---

## 11. The owner's answers (10-19)

1. **Yes.** A definition uses code words to describe a code word ("silly really, but the best I have"). The meaning is what the code physically does, and order and punctuation change it.
2. **"No, but yes."** The six questions aren't a separate told layer. The 65 primes are the told layer, each with an action, and some of them are combinations of roots. "how" isn't a prime, so it is a formula of primes.
3. **Yes.** Personal meanings are kept per person, and when context doesn't settle a meaning, the brain asks rather than guesses.
4. **Yes, refined as the three layers in §2.** Roots, then primes as formulas of roots, then all other words as formulas of those. Hard words may need huge formulas, or several.

*Research behind this* (`NEURON-RESEARCH-2026-10-19.md`, plus Hjørland, "Semantic primitives", ISKO Encyclopedia of Knowledge Organization, https://www.isko.org/cyclo/primitives.htm):

- **What supports it.** Primitives assume compositionality, meaning complex meanings are functions of their parts and how they combine. Wierzbicka's 65 primes (stable since 2014) are, in her words, like chemical elements. Leibniz encoded compound concepts as products of prime numbers.
- **What warns against it.** There is "no one correct selection of primitives"; meanings depend on one another (holism); and compounds can have properties their parts lack. That is why balance, not a fixed list, decides.
- **Further support.** Harnad and Vincent-Lamarre show definitions bottom out in a small grounded set. Woods and Johnson-Laird treat meaning as a procedure, and Fodor warns that the procedure has to reach the world; this is why the roots are physics. Logan shows that using knowledge is retrieval.

---

## Appendix: the owner's worksheet (guesses), as written

*From `sematic primes and roots worksheet..ods`, 10-19. The "roots" column is the owner's guess. A blank means no guess yet.*

| Group | Prime | Root guess |
|---|---|---|
| Substantives | I, you, someone, something, thing, body | |
| Relational substantives | kind, part | |
| Determiners | this, the same, other/else/another | |
| Quantifiers | one, two, some, all, much/many, little/few | |
| Evaluators | good, bad | |
| Descriptors | big, small | |
| Mental predicates | think, know, want, don't want, feel, see, hear | |
| Speech | say, words, true | |
| Actions, events, movement | do, happen, move | |
| Existence, possession | be (somewhere), there is, be (something/someone), (is) mine | |
| Life and death | live | live |
| | die | −live |
| Time | when/time, moment | |
| | now | now |
| | before | −now |
| | after | now + |
| | a long time | now ++ |
| | a short time | −−now |
| | for some time | now + now |
| Space | where/place, here, side, inside, touch (contact) | |
| | above | above |
| | below | −above |
| | far | far |
| | near | −far |
| Logical concepts | not, maybe, can, because, if | |
| Intensifier, augmentor | very, more | |
| Similarity | like/as/way | |
| **Missing words** | to, is, a, thing, have, be, fore, long, short, in, cause, maybe, plus, minus, multiply, divide, none, yes, object, at | |
