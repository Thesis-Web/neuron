# The roots and their compositions, given again by the owner on 2026-11-04 (pasted whole, as handed; the owner: "I will give you this AGAIN")

## 1. Start with the root actions
| Domain | Root | What it physically does |
|---|---|---|
| Graph | READ | Obtain the value of an addressed point or shard |
| Graph | FIND | Locate an address satisfying a condition |
| Graph | WRITE | Change or create stored information |
| Graph | MOVE | Change a position or traverse to another point |
| Graph | COPY | Reproduce specified information |
| Graph | LINK | Establish a relationship between points |
| Graph | SPLIT | Separate a structure into components |
| Graph | JOIN | Combine structures according to a relationship |
| SQL | SELECT | Return rows satisfying a query |
| SQL | INSERT | Add a row to a table |
| SQL | UPDATE | Modify an existing row |
| SQL | DELETE | Remove a row |
| Memory | STORE | Persist information for future use |
| Memory | RECALL | Recover previously stored information |
| Timeline | STAMP | Associate an occurrence with a time |
| Timeline | APPEND | Add an occurrence to chronological history |
| State | COMPARE | Determine equality, difference or ordering |
| State | SET | Establish a new state |
| State | MEASURE | Obtain a quantity or difference |
| Sources | FETCH | Acquire external information |
| Execution | RUN | Perform a specified operation |

Notice that READ, SELECT, and RECALL all obtain information, but the target substrate and operational contract are different. This is important for your DNA shards. The same general action can require different implementations depending on what it acts upon.

## 2. First generation
READ + FIND = SEARCH · READ + MOVE + MATCH = SCAN · FIND + READ = LOOKUP · FIND + READ + COPY = RETRIEVE · READ + COMPARE = EXAMINE · READ + SPLIT = PARSE · READ + LINK = ASSOCIATE · READ + MEASURE = QUANTIFY · WRITE + STAMP = RECORD · COPY + STORE = PRESERVE. The order matters: FIND → READ is LOOKUP; READ → TEST → MOVE → REPEAT is a sequential SCAN. The + is shorthand; a complete formula must also specify ordering, input/output dependencies, conditions and termination.

## 3. Second generation
RETRIEVE + STORE = MEMORIZE · RECALL + TIME + COMPARE = REMEMBER · SEARCH + MATCH + LINK = IDENTIFY · EXAMINE + COMPARE + RECORD = ASSESS · FIND + TIMELINE + READ = TRACE · RECALL + COMPARE = RECOGNIZE · READ + COMPARE + DIFFERENCE = DISTINGUISH · TRACE + COMPARE + IDENTIFY = INVESTIGATE · EXAMINE + TIME + REPEAT = MONITOR · IDENTIFY + LINK + STORE = CLASSIFY.

## 4. Third generation
EXAMINE + COMPARE + ASSESS = EVALUATE · RECALL + EXAMINE + COMPARE = ANALYZE · ANALYZE + TRACE + IDENTIFY = DIAGNOSE · RECALL + COMPARE + PROJECT = PREDICT · PREDICT + UNCERTAINTY + PROPOSE = HYPOTHESIZE · HYPOTHESIZE + TEST + MEASURE = EXPERIMENT · EXPERIMENT + COMPARE + ASSESS = VALIDATE · VALIDATE + SOURCE + PROVENANCE = VERIFY · VERIFY + COMPARE + SELECT = DECIDE · DIAGNOSE + DECIDE + UPDATE = CORRECT. Predicting does not establish correctness; hypothesizing makes the uncertainty explicit; verification requires independent evidence.

## 5. Fourth generation
OBSERVE + REMEMBER + COMPARE = EXPERIENCE · EXPERIENCE + VALIDATE + STORE = LEARN · LEARN + GENERALIZE + TEST = ABSTRACT · ANALYZE + RECALL + DERIVE = DEDUCE · LEARN + COMPARE + CORRECT = ADAPT · TRACE + DIAGNOSE + CORRECT = REPAIR · EVALUATE + DECIDE + EXECUTE = ACT · ACT + MONITOR + CORRECT = REGULATE · VERIFY + DECIDE + REGULATE = GOVERN · LEARN + ACT + VERIFY + ADAPT = IMPROVE. PROJECT, TEST, GENERALIZE and EXECUTE are left visible as primitives not derived here. LEARN must involve a change that influences future behavior.

## 6. One additive chain
L0 READ + FIND + MOVE + COMPARE · L1 SCAN + LOOKUP · L2 RECALL + TRACE + EXAMINE · L3 ANALYZE + ASSESS · L4 PREDICT + TEST + VERIFY · L5 DECIDE + ACT + MONITOR · L6 GOVERN.

## 7. Inside a DNA shard
VERIFY is not one indivisible function; its selected shard composes smaller actions depending on what is verified (a code change: READ the modification, RECALL the spec, RETRIEVE the prior state, TRACE the error history, FETCH the evidence, COMPARE, TEST, MEASURE, DECIDE, RECORD). The word is the compact symbol; the selected DNA shard is its contextual executable meaning; a shard needs inputs, guards, outputs, side effects and failure conditions.

## 8, 9. The direction and the experiment
C = B ∘ A, typed composition: inputs, transformation, outputs, conditions, evidence. Test first whether Neuron can derive the composition itself: teach only READ, FIND, MOVE, COMPARE and RETURN with their input/output contracts; expose Neuron to examples of SCAN without hand-authoring it; can it discover that a scan repeatedly reads, compares and advances until a match or termination, retain that formula, and apply it to a new graph structure. The success condition is not whether Neuron can explain what scan means. It is whether Neuron can actually scan.
