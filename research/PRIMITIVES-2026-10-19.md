# Primitives: the bare lists

*2026-10-19, revised. Your worksheet guesses are taken out. This file holds no formulas and no meanings, only the lists.*

---

## 1. The silicon: what the machine physically does

*[mine] These are the 20 words I picked for the blueprint (§4.3). hp2 uses these 20; hp split them into 104.*

| Word | What the machine does (blueprint §4.3) |
|---|---|
| GO | moves this run to a gate, with a given arrival |
| SPLIT | starts a branch run at a gate, carrying its subject; the main run keeps going |
| LAND | puts a finding on the parent run's scratch pad |
| WAIT | holds this run until its branch runs have landed, or a beat passes |
| END | stops this run |
| READ | reads a row or field reachable from a gate, or the brain's own size |
| WRITE | writes a row, new or overwritten |
| SPAWN | makes a new gate at a point, with its definition memory and birth memory |
| DELETE | removes a row |
| MOVE | moves a point, or moves a memory between active, persistent and long-term |
| FIND | reaches by index: the gate at a point, the gates for a label, the memory for a run signature, the memories at a time, the runs with a shape |
| ADD, SUB, MUL, DIV | the machine's arithmetic on numbers and coordinates |
| COMPARE | same, more or less, and by how much |
| CLOCK | reads the time now |
| HEAR | takes the next input from a port |
| SAY | puts words or an act out through a port |
| CALL | anything else a computer can do: fetch a URL, read or write a file, run a program |

---

## 2. The 65 primes (Wierzbicka's list; no meanings attached)

| Group | Primes |
|---|---|
| Substantives | I, YOU, SOMEONE, SOMETHING/THING, PEOPLE, BODY |
| Relational substantives | KIND, PART |
| Determiners | THIS, THE SAME, OTHER/ELSE |
| Quantifiers | ONE, TWO, SOME, ALL, MUCH/MANY, LITTLE/FEW |
| Evaluators | GOOD, BAD |
| Descriptors | BIG, SMALL |
| Mental predicates | THINK, KNOW, WANT, DON'T WANT, FEEL, SEE, HEAR |
| Speech | SAY, WORDS, TRUE |
| Actions, events, movement | DO, HAPPEN, MOVE |
| Existence, possession | BE (SOMEWHERE), THERE IS, BE (SOMEONE/SOMETHING), (IS) MINE |
| Life and death | LIVE, DIE |
| Time | WHEN/TIME, NOW, BEFORE, AFTER, A LONG TIME, A SHORT TIME, FOR SOME TIME, MOMENT |
| Space | WHERE/PLACE, HERE, ABOVE, BELOW, FAR, NEAR, SIDE, INSIDE, TOUCH |
| Logical concepts | NOT, MAYBE, CAN, BECAUSE, IF |
| Intensifier, augmentor | VERY, MORE |
| Similarity | LIKE/AS/WAY |

---

## 3. Teaching by typing: what works today (checked on both builds)

| You type | hp | hp2 |
|---|---|---|
| `what is X ?` | it looks X up in its dictionaries, not in what you said | the same |
| `yes` or `no`, right after it answers | marks that answer right or wrong; a no sends it back to memory and the dictionaries to find out why | the same |
| `X is Y` | runs "is" as its told action; nothing is stored as a meaning | judges it: yes, no or maybe |
| `sleep` | says yes to its "i want sleep" | — |

In either build, nothing you type becomes a word's meaning. Meanings come only from the builder's lay files, or from the brain compiling dictionary text.
