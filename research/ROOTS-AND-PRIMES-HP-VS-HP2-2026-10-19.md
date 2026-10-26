# Roots and primes: hp (Fable) vs hp2 (Opus)

*Read 2026-10-19, 14:00–14:20, straight from each build's told files:*
- **hp:** `lay/00-roots.lay` and `lay/10-told.lay`, plus label rows from hp's live brain.
- **hp2:** `lay/00-roots.lay`, `lay/28-roots.lay`, `lay/30-primes.lay` and `lay/10-types.lay`.

*Each meaning below is the builder's code turned into plain words. Nothing here is my opinion of what the word should mean.*

**Words used below:**
- **"In hand"** means the thing the run is holding right now (the top of its pad).
- **"Compare"** means the kernel's COMPARE, which answers same, more or less.
- **"GAP"** means the builder laid the word with no action, for the brain to fill.

---

## Layer 0: physics, what the silicon does

| | hp | hp2 |
|---|---|---|
| Origin | gate 0 = zero, at (0,0,0), value 0 | same |
| Axes | x, y and z axis gates | same |
| Physics gates | **104**. The 20 physics words, with READ split into 51 kinds (READ.at, READ.bind … READ.worth), WRITE into 17, FIND into 8, DELETE into 6 and MOVE into 2. Plus stack helpers: DUP, DROP, SWAP, OVER, ROT. | **20**: GO, SPLIT, LAND, WAIT, END, READ, WRITE, SPAWN, DELETE, MOVE, FIND, ADD, SUB, MUL, DIV, COMPARE, CLOCK, HEAR, SAY, CALL. **Plus 61 "nouns"** that READ, WRITE, FIND and DELETE act on (ITEM, LAST, KIND, WHO, WHAT, WHERE, WHY, POINT, VALUE, LABEL, SECTION, PROC, SHARD, BODY, TIME, TRUST, …). |
| Yes / No | the outcome gates `yes` and `no` | YES at (2,0,0) and NO at (0.5,0,0). This is your "yes = x, no = 1/x" taken literally, with x = 2. |
| Settings the brain can change | budget 2000, beat 1000 ms, park after 30, slice 16, split worth 0.8, … | BEAT 1000, BUDGET 3000, STUCK 4000, PARK 400, CELL 0.02, SLICE 64, … |

---

## Layer 1: the roots (your worksheet: live, now, above, far, and the operations −, +, ++, x+x, 1/x)

### hp2: its own roots file (`28-roots.lay`), every row marked GUESS

| Root | What hp2's code does |
|---|---|
| **−x** (r-neg) | A number or point is multiplied by −1. A gate goes to its opposite (`not`). |
| **x +** (r-more) | A number gets +1. A point is grown ×1.1. |
| **x ++** (r-lot) | x × x. |
| **x + x** (r-twice) | x + x. |
| **1/x** (r-inv) | The inverse. For a point, p/\|p\|². |
| **live** | How many of its memories are awake right now (a count). |
| **now** | The clock (seconds). |
| **above** | The y-axis point (0,1,0). |
| **far** | The x-axis point times itself, which is the number 1. |

hp2 also has a "refit by balance" process for these. Each time someone says yes or no about a use, it adds up right against wrong. When wrong outweighs right, it reopens the root as a gap.

### hp: no separate roots file

hp's roots are among its primes (`10-told.lay`), told as actions. Your worksheet is laid only as "derived-from" links marked guess (die ← live, before ← now, …). Those links are recorded; they are not run.

hp's root-level operations:

| Operation | What hp's code does |
|---|---|
| plus / minus / times / divided | holds ADD / SUB / MUL / DIV for the next value |
| opposite | 1/x (inversion) |
| contradicts | −x |
| kind-of | one step up z |
| part-of | one step along x |
| like | × 0.9 |
| cause | two steps later in y |
| before / after | one step back / on in y |
| used-for | × 2 |
| describes | × 0.5 |
| supports | × 1.5 |
| derived-from | one step along x and z |

---

## Layer 2a: the worksheet primes (the ones you wrote as formulas of roots)

| Prime | Your worksheet | hp | hp2 |
|---|---|---|---|
| die | −live | this run stops (END) | −(count of awake memories): a negative number |
| before | −now | compare two times: first is earlier → yes | −(clock): a negative number |
| after | now + | compare two times: first is later → yes | clock + 1 |
| a long time | now ++ | now + 30 days | clock × clock |
| a short time | −−now | now − 1 minute | −(−clock) = the clock, so "a short time" equals "now" |
| for some time | now + now | WAIT (hold until its branches land or a beat passes) | clock + clock |
| below | −above | what sits one step down z | −(0,1,0) = (0,−1,0) |
| near | −far | compare: same place → yes | −(1) = −1 |

hp read your formulas as ideas and wrote its own actions. hp2 ran them as written, as arithmetic on the numbers. Several come out broken: a short time = now, a long time = now², near = −1.

---

## Layer 2b: all 65 primes

| Prime (labels) | hp | hp2 |
|---|---|---|
| **I** (i, me) | the brain's own size in hand (gates, memories, active) | in the brain's own runs: takes stock of itself and is the actor; in a person's words, "I" is that person |
| **YOU** | who sent this input | the one the words are said to |
| **SOMEONE** | a who-hole: a gate in hand fills it, else the hole stays | a hole for a who |
| **SOMETHING** (hp: also thing, a; hp2: also thing) | a what-hole | a hole for a thing |
| **PEOPLE** | two who-holes in one list (someone + someone) | GAP |
| **BODY** | where the thing physically is (its point) | GAP |
| **KIND** | reaches its kinds (one step up z) | its strongest kind-of line; unknown → a gap |
| **PART** | reaches what it is part of (one step along x) | what it is part of; unknown → a gap |
| **THIS** | the run's subject, taken again | the run's subject; else what the brain last handed this person; else a hole |
| **THE SAME** | compare two things | compare two → yes / no |
| **OTHER** (else) | its opposite (1/x) | not the thing in hand: set it aside, leave a hole |
| **ONE / TWO** | the numbers 1 and 2 | the numbers 1 and 2 |
| **SOME** | count what's in hand; more than zero → yes | one of the list in hand (its first) |
| **ALL** | everything on the pad gathered into one list | GAP |
| **MUCH / MANY** | the count of what's in hand | GAP |
| **LITTLE / FEW** | only the first item in hand | GAP |
| **GOOD** | the thing matches the run's want → yes | it is what the run wants → yes / no; no want yet: hold |
| **BAD** | off the want either way → yes | it is what the run doesn't want → yes / no |
| **BIG** | × 2 | × 1.1 |
| **SMALL** | ÷ 2 | × 0.9 |
| **THINK** | start a question run (the ladder) on it | start the thing's own question, and wait for it |
| **KNOW** | find the memories it was used in | read its definition memory; none → no, and a gap |
| **WANT** | it becomes the run's want | it becomes the run's want |
| **DON'T WANT** (hp2: also avoid) | its opposite becomes the want (no word: the encoder splits "don't") | keep it as what the run steers away from |
| **FEEL** | weigh it against the want, if there is one | GAP |
| **SEE** | what the run was given (the input) | GAP |
| **HEAR** | take the answer to this run's last call | the text in hand is heard as input |
| **SAY** | say it (after the core check) | its word in hand; no word → ask its name |
| **WORDS** (word) | its word (label) | text → the gates its words point to; none → a hole |
| **TRUE** | how grounded its source is (2, 1 or 0) | how it came to be held: told, sourced or derived |
| **DO** | run it, and keep it as the subject | run it as a branch, and wait for what it lands |
| **HAPPEN** | the memories between this input's time and now | GAP |
| **MOVE** (hp: also **to**) | MOVE: the gate goes to the point in hand | MOVE: the gate goes to the point in hand |
| **THERE IS** (hp: there; hp2: exists) | is there a gate for this word (found / none) | is there a gate for the word, point or value → the gate and yes, or no |
| **BE** (be, is, are, am) | reaches what it is the same as (same place) | of two gates, is the first a kind of the second; weighs every held line, and a close call is said as "maybe" |
| **BE SOMEWHERE** | its place, and what's there | GAP |
| **MINE** (my) | who sent this input (the same code as YOU) | did the brain make this itself → yes / no |
| **LIVE** | how many runs are running now | root: count of awake memories |
| **DIE** | this run stops | −live |
| **WHEN / TIME** | the time of this input | the time of the memory in hand; else a hole for a time |
| **NOW** | the clock | root: the clock |
| **BEFORE** | see layer 2a | see layer 2a |
| **AFTER** | see layer 2a | see layer 2a |
| **A LONG TIME** | see layer 2a | see layer 2a |
| **A SHORT TIME** | see layer 2a | see layer 2a |
| **FOR SOME TIME** | see layer 2a | see layer 2a |
| **MOMENT** | one beat (1 second) | GAP |
| **WHERE / PLACE** | its point | its point; else a hole for a place |
| **HERE** | the run's own where | the run's own where |
| **ABOVE** (hp: also up) | what sits one step up z | root: the y-axis point |
| **BELOW** (hp: also down) | what sits one step down z | −above |
| **FAR** | compare two: apart → yes | root: 1 |
| **NEAR** | compare two: same place → yes | −far |
| **SIDE** | what sits one step along x | GAP |
| **INSIDE** (hp: also **in**) | the gates that are part of it | GAP |
| **TOUCH** | same place → yes (the same test as near) | within one grid cell → yes / no |
| **NOT** | yes flips to no; anything else → its opposite | flips: a gate to its opposite (a stored opposite-line, else the opposite's formula); a number or point is negated |
| **MAYBE** | puts the guess state next to the thing | the run is guessing from here on (its rows are written as guesses) |
| **CAN** | does it have a way (process) → found / none | does it have a process → yes / no |
| **BECAUSE** | how it was made, and the memory that made it | back to the cause: its birth memory |
| **IF** | the outcome goes to the head, and the next hop picks the branch | a no (or a zero) ends the run here; anything else carries on |
| **VERY** | x × x | doubles the degree |
| **MORE** | compare: first is more → yes | compare → yes / no; with one value: +1 |
| **LIKE** (as; hp2: also way) | reaches what's like it (× 0.9) | are the two alike? a stored like-line first, else like's formula on the first one's point, compared with the second's → yes / no |
| *who* (not a prime) | someone + ? | someone + ? |
| *what* (not a prime) | something + ? | something + ? |
| *why* (not a prime) | because + ? | (not laid as a formula) |
| *how* (not a prime) | like + ? | what, of the kind like (a hole for a way, and the question) |

**Count:**
- **hp:** all 65 have an action. Every row is plain told code; only the eight worksheet links are marked guess.
- **hp2:** 53 have an action and 12 are GAP (people, body, all, much, little, feel, see, happen, be somewhere, moment, side, inside). Every row is marked GUESS.

---

## Layer 2c: your MISSING WORDS list

| Word | hp | hp2 (each a candidate guess, not wired; the meaning loop is meant to test it) |
|---|---|---|
| to | told: the same gate as **move** | near + where (toward a place) |
| a | told: the same gate as **something** / thing | one (the count is kept) |
| is / be | told: the **be** gate | the **be** prime |
| thing | told: **something** | **something** |
| have | only a plain gate it spawned while reading, no meaning | a hole for a thing, of the kind mine |
| fore | plain gate, no meaning | before |
| long | plain gate, no meaning | far + big |
| short | plain gate, no meaning | −long |
| in | told: the same gate as **inside** | inside (itself a GAP) |
| cause | plain gate, no meaning | because |
| maybe | the **maybe** prime | the **maybe** prime |
| plus / minus | told operators: ADD / SUB, held for the next value | operators: ADD / SUB |
| multiply / divide | plain gates, no meaning (the operators are "times" and "divided") | pointed at the operators times / divided (MUL / DIV) |
| none | plain gate, no meaning | the NONE outcome, held as a thing |
| yes | the outcome **yes** | YES (x = 2) |
| object | plain gate, no meaning | a hole for a thing, of the kind body |
| at | plain gate, no meaning | where |

---

## The same word in each brain

| Word | hp | hp2 |
|---|---|---|
| small | ÷ 2 | × 0.9 |
| big | × 2 | × 1.1 |
| far | "are these two apart?" → yes / no | the number 1 |
| die | stop this run | a negative count |
| before | "is this time earlier?" → yes / no | a negative timestamp |
| a short time | one minute ago | the same as now |
| be / is | "what is it the same as?" | "is the first a kind of the second?" |
| to | move | toward a place |
| a | a what-hole | one |

**Who wrote all of the above:** in both builds, every meaning in this file was written by the LLM builder. The brain made none of them.
