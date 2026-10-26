# Neuron v19

Built by Claude in one turn on 2026-10-15, in the folder the owner gave it ("I gave you v-19 you get one turn").

**What it shows.** A word is only a pointer to a neuron, and the neuron's meaning is what it does: its code. Each operation is taught once in its long form. After a long run, the brain lays the shortcut. Once it has three memories of an operation, the brain finds that operation's formula by balancing its own memories, and from then on the word points to the formula. In the owner's words: the "word" is nothing more than a pointer to the formula shortcut, which is the "meaning" or "action".

## Run it

| Command | What it does |
| --- | --- |
| `./demo` | Grows a brain from nothing and walks it through plus, minus, times and equals |
| `./say 2 + 3` | Types a line to the brain. Use `x` for times, or quote the line so the shell leaves `*` alone |
| `./look` | Reads the brain: what each word points to now, every memory and how each time ran, the last long path |
| `./grow` | Starts over. The old `brain.db` is kept under a dated name, never deleted |
| `./teach.sh teach/<file>` | Runs one teaching file |

To type into `brain.db` by hand, first run `.load ./kernel/eval` and `PRAGMA recursive_triggers = ON;` from this folder. The scripts do this for you.

## What was laid by hand, once

- **The bones** (`bones.sql`): the tables and three triggers.
- **Neuron 1**, the one that makes neurons (`code/new.sql`). It is the only neuron laid before time.
- **The teaching files** (`teach/`). Each operation's long form, taught once:
  - plus: one place up, as many times as the second value counts
  - minus: one place down
  - times: rounds of steps up from zero
- **The other taught pieces:** stop (`.` and `?`), equals (balance), study, relate, the inverse relation, the eight shapes study may try, and the pattern a found formula is written into. Every neuron here was born the brain's way, by hitting neuron 1.

## What the brain made itself

- **Zero:** the first run, at moment 1, born at place 0. Every other number is born at its place when a run needs it. After the demo, 20 numbers exist, not thousands.
- **Every shard:** the shortcut after each long run, plus its back-populated partner. After `2 + 3`, the shard for `5 - 3` already exists, so subtraction of that pair was never counted.
- **Every memory.** The same truth again is the same row with one more time. Each time it happens, a receipt records which meaning ran, the number of hops, and every place a long run stood on.
- **The formulas.** Study tried each shape against all of an operation's memories. It adopted the only shape that balanced all of at least three memories: A+B for plus, A−B for minus, A×B for times. The long form stays as the earlier version in the `meaning` table. After that, `1234 + 4321` answers 5555 in one hop, with no counting.

## The physics: the only things that are not neurons

1. **excite:** a step lands, a new moment starts, and the neuron's code runs. A neuron with no code is a value, so it is held.
2. **arrive:** a value arrives while an operation waits for one, so the operation fires with both values.
3. **point:** a typed token goes to the neuron of its word, or to the neuron at its number's place. If no neuron lives at that place, neuron 1 is hit with the place. Anything else becomes a need.

None of them decides anything about meaning. Only `point` names a neuron: neuron 1, which makes neurons.

## What the brain says

Only what its runs produced:
- a value
- a balance (`5 = 5` or `4 ≠ 5`)
- `?` and what it still needs (`? zork`, or `? +` when plus is missing a value)

No sentence is written in advance anywhere.

## Honest limits

- **Study chooses; it does not invent.** It picks among eight shapes the teacher gave (A+B, A−B, B−A, A×B, A×A, B×B, A, B) by balancing them against its own memories. Inventing new shapes is the open part.
- **The long forms were written by the teacher (Claude), once.** For numbers the long form is known: counting. For words, finding the long form is the open invention (see the paper "What Neuron Has to Invent").
- **"One place up" is arithmetic on a number's place.** A number's place is the number [329].
- **Reading order only:** `2 + 3 x 4` is 20.
- **The `say` script splits what you type into tokens,** outside the brain. That is the encoder.
- **Truth shifts are untested.** A memory ending when a different answer arrives is built (`code/remember.sql`), but nothing in the demo exercises it, because every run is deterministic.
- **Not built:** divide, definitions (the brain does not yet ask for them [329]), the sixth, the hc, and any words beyond the operators.

## Files

| File | What it is |
| --- | --- |
| `bones.sql` | Tables, the three triggers, neuron 1, the first run |
| `code/*.sql` | Each neuron's meaning, as code. Long forms are built from need2 + shortcut + walk_* + remember + receipt_long + lay + hold + study_hit. The formula pattern is need2 + formula + remember + receipt_formula + hold |
| `teach/1_base.sql`, `2_minus.sql`, `3_times.sql` | What the teacher lays, in order |
| `kernel/eval.c` | SQLite's own `eval.c` with one flag (`SQLITE_DIRECTONLY`) removed, so a trigger can run a neuron's code. Built to `kernel/eval.so` |
| `say`, `look`, `grow`, `teach.sh`, `demo` | The shell around it |
