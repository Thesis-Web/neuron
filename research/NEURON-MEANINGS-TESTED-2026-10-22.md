# NEURON MEANINGS, TESTED: the first layer, run on the silicon
*2026-10-22. A word's meaning is a RUN; its definition is the SPEC the run has to satisfy. For every word below, the definitions come from WordNet 3.0, Webster 1913 and Merriam-Webster (fetched live from hp and the MW API), the run is SQL executed by a scratch mother on a scratch database, and the spec is a set of before-and-after checks, each quoting the source phrase it encodes. A run PASSES only when every check holds on every world it applies to, out of ten worlds (four written by hand, six generated at random with the same things under different places, owners, values, life, clocks and purses). Wrong runs were included on purpose to see whether the test can tell. The harness, the raw results and the fetched definitions are in `Neuron-Meaning-Data-2026-10-22/meanings/`. No run was taken as right because it looked right; the numbers below are what executed.*
## 0. The count
| | |
|---|---|
| words tested | 63 |
| candidate runs executed | 98 |
| runs that pass their spec on every applicable world | 78 |
| runs written to be wrong | 20 |
| wrong runs the test let through | 0 |
| worlds | 10 |
| entailments found by execution (a run of one word satisfies another word's spec on every world) | 65 |
| words whose run also fires silicon, not only reads it | 26 |

## 1. How this differs from everything before it
- Versions 8 to 11 of the model picked words out of definitions and called them candidate meanings. Those are descriptions. Nothing in them fires silicon. The page now says so.
- Here every candidate is executed. The scratch mother runs it, the state before and after is read back, and the checks are the definition's own phrases turned into tests. A run with a wrong line fails on that line, and the line is named.
- The twenty wrong runs are the control. Copying instead of moving, hiding instead of deleting, taking without paying, reading instead of writing, the worksheet's minus-now and minus-live, a write with no destination: every one failed, and on the check that says why.
- Nothing is laid by hand into the brain. This is a measurement of what the silicon does when a candidate is run, kept as a file. What the brain has to learn to do itself is the step I did by hand: turn a definition's phrases into checks (section 7).

## 2. Every word, its sources, its run, and what happened
Roots are read from the SQL that ran: READ (SELECT), WRITE (INSERT, UPDATE), DELETE, SPAWN (CREATE), COMPARE and FIND (WHERE), ADD and SUBTRACT, JOIN (UNION), MOVE (ORDER, LIMIT), CLOCK (now), SAY (rows handed back), HEAR (holes filled from outside), plus which of the brain's own tables it touched (MEMORY, STATE, TIMELINE). The measure column is what SQLite's authorizer counted: schema changes (the graph), row writes (the silicon), reads, rows said back.

### a
Sources: mw: used as a function word before singular nouns when the referent is unspecified

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| any one of the kind | `SELECT id FROM things WHERE name=:k LIMIT 1` | PASS | COMPARE, FIND, HEAR, MOVE, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): exactly one; of the kind asked, and which one is not specified

*Its run also satisfies the spec of:* part

### add
Sources: mw: to join or unite so as to bring about an increase / wn v1: make an addition

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| bring about an increase | `UPDATE things SET value=value+:k WHERE id=:i` | PASS | ADD, COMPARE, FIND, HEAR, WRITE | 0 / 1 / 2 / 0 |

Spec (each line is a check, quoting the source phrase): the value after is the value before plus k

*Its run also satisfies the spec of:* change, write

### after
Sources: wn: happening at a time subsequent to a reference time / mw: following in time or place

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| later in time | `SELECT (SELECT t FROM timeline WHERE id=:a) > (SELECT t FROM timeline WHERE id=:b)` | PASS | COMPARE, FIND, HEAR, READ, SAY, TIMELINE | 0 / 0 / 4 / 1 |
| later in time, asked the other way round | `SELECT (SELECT t FROM timeline WHERE id=:a) > (SELECT t FROM timeline WHERE id=:b)` | PASS | COMPARE, FIND, HEAR, READ, SAY, TIMELINE | 0 / 0 / 4 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when a happened at a later time than b

*Finding:* before and after are one COMPARE on two times read from the timeline, less or more. The flip between them is the axis flip, not a negation.

### all
Sources: wn: quantifier; used to indicate the whole number or amount / mw: the whole amount, quantity, or extent of

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| every one | `SELECT id FROM things` | PASS | READ, SAY | 0 / 0 / 2 / 5 |

Spec (each line is a check, quoting the source phrase): the whole number: every thing comes out

*Its run also satisfies the spec of:* whole

### and
Sources: mw: used as a function word to indicate connection or addition especially of items within the same class

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| both at once | `SELECT id FROM things WHERE place='box' AND alive=1` | PASS | COMPARE, FIND, READ, SAY | 0 / 0 / 3 / 2 |

Spec (each line is a check, quoting the source phrase): the rows are those in both sets; never more than either set alone

### before
Sources: wn adv: earlier in time; previously / mw: at an earlier time

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| earlier in time | `SELECT (SELECT t FROM timeline WHERE id=:a) < (SELECT t FROM timeline WHERE id=:b)` | PASS | COMPARE, FIND, HEAR, READ, SAY, TIMELINE | 0 / 0 / 4 / 1 |
| earlier in time, asked the other way round | `SELECT (SELECT t FROM timeline WHERE id=:a) < (SELECT t FROM timeline WHERE id=:b)` | PASS | COMPARE, FIND, HEAR, READ, SAY, TIMELINE | 0 / 0 / 4 / 1 |
| WRONG: the worksheet minus now | `SELECT -(SELECT value FROM state WHERE key='now')` | FAIL: says yes exactly when a happened at an earlier time than b | CLOCK, COMPARE, FIND, READ, SAY, STATE, SUBTRACT | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when a happened at an earlier time than b

*Finding:* "-now" returns a number (-10), not whether a was earlier than b: it cannot be before, because before takes two events.

### begin
Sources: wn v1: set in motion, cause to start / mw: to do the first part of an action

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| set in motion | `UPDATE state SET value='1' WHERE key='running'; INSERT INTO timeline(t,event) VALUES((SELECT value FROM state WHERE key='now'),'start')` | PASS | CLOCK, COMPARE, FIND, READ, STATE, TIMELINE, WRITE | 0 / 2 / 3 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: not running before; running after, and the start is on the timeline at now

### between
Sources: wn: in the interval / mw: in the space that separates

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| in the interval | `SELECT id FROM things WHERE value BETWEEN :lo AND :hi` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 2 |

Spec (each line is a check, quoting the source phrase): the things whose value lies in the interval, all of them

*Its run also satisfies the spec of:* part

### born
Sources: wn adj: brought into existence / mw: brought forth by or as if by birth

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| brought into existence, alive | `INSERT INTO things(name,place,alive,t) VALUES(:x,:p,1,(SELECT value FROM state WHERE key='now'))` | PASS | CLOCK, COMPARE, FIND, HEAR, READ, STATE, WRITE | 0 / 1 / 2 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: did not exist before; exists after, alive, at now

*Finding:* born = create + alive. die undoes the alive, not the create.

*Its run also satisfies the spec of:* create, into, write

### buy
Sources: wn v1: obtain by purchase; acquire by means of a financial transaction / mw: to acquire possession, ownership, or rights to the use or services of by payment

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| possession one way, money the other | `UPDATE things SET owner=:buyer WHERE id=:i AND owner=:seller; UPDATE purse SET money=money-:price WHERE owner=:buyer; UPDATE purse SET money=money+:price WHERE owner=:seller` | PASS | ADD, COMPARE, FIND, HEAR, SUBTRACT, WRITE | 0 / 3 / 6 / 0 |
| WRONG: take without paying | `UPDATE things SET owner=:buyer WHERE id=:i AND owner=:seller` | FAIL: by payment: the buyer has less money by the price; and the seller has more by the price | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 2 / 0 |

Spec (each line is a check, quoting the source phrase): acquire possession; by payment: the buyer has less money by the price; and the seller has more by the price

*Finding:* buy = take + pay. Taking without paying passes take and fails buy. The money line is what buy adds.

*Its run also satisfies the spec of:* change, sell, write

### change
Sources: wn v1: cause to change; make different; cause a transformation / mw: to make different in some particular

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| make different: write what is not there | `UPDATE things SET place=CASE WHEN place='box' THEN 'table' ELSE 'box' END WHERE id=:i` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 2 / 0 |
| WRONG: set a value that may already be there | `UPDATE things SET value=:v WHERE id=:i` | FAIL:  | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 1 / 0 |

Spec (each line is a check, quoting the source phrase): the same thing; is different after

*Finding:* Setting a value is a change only when the value differs from what is there: on worlds where 8 was already held, the WRONG run changes nothing. A change must read first.

*Its run also satisfies the spec of:* write

### copy
Sources: mw: to make a copy or duplicate of / wn n1: a reproduction of a written record

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| duplicate the row | `INSERT INTO things(name,place,owner,value,alive,t) SELECT name,place,owner,value,alive,(SELECT value FROM state WHERE key='now') FROM things WHERE id=:i` | PASS | CLOCK, COMPARE, FIND, HEAR, READ, STATE, WRITE | 0 / 1 / 8 / 0 |
| WRONG: move it | `UPDATE things SET place=:p WHERE id=:i` | FAIL: the original is unchanged; a duplicate exists after: same in every field but identity and birth time; one more thing exists | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 1 / 0 |

Spec (each line is a check, quoting the source phrase): the original is unchanged; a duplicate exists after: same in every field but identity and birth time; one more thing exists

*Its run also satisfies the spec of:* write

### count
Sources: mw: to indicate or name by units or groups so as to find the total number of units involved / wn v1: determine the number or amount of

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| find the total number | `SELECT COUNT(*) FROM things WHERE place=:p` | PASS | ADD, COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 1 / 1 |

Spec (each line is a check, quoting the source phrase): the number equals how many there are

*Its run also satisfies the spec of:* part

### create
Sources: mw: to bring into existence / wn v2: bring into existence

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| row | `INSERT INTO things(name,place,t) VALUES(:x,:p,(SELECT value FROM state WHERE key='now'))` | PASS | CLOCK, COMPARE, FIND, HEAR, READ, STATE, WRITE | 0 / 1 / 2 / 0 |
| table | `CREATE TABLE plum(id INTEGER)` | PASS | SPAWN | 1 / 0 / 1 / 0 |
| WRONG: read it | `SELECT * FROM things WHERE name=:x` | FAIL: bring into existence: it exists after | COMPARE, FIND, HEAR, READ | 0 / 0 / 8 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: bring into existence: it did not exist before; bring into existence: it exists after; nothing else changed

*Finding:* Two shards pass: a row brought into existence, and a table. Same shape, different kind of thing.

*Its run also satisfies the spec of:* into, write

### delete
Sources: wn v1: remove or make invisible / mw: to eliminate especially by blotting out, cutting out, or erasing

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| remove the row | `DELETE FROM things WHERE name=:x` | PASS | COMPARE, DELETE, FIND, HEAR | 0 / 1 / 1 / 0 |
| WRONG: hide by moving | `UPDATE things SET place='nowhere' WHERE name=:x` | FAIL: remove: it does not exist after; nothing else changed | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 1 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: it existed before; remove: it does not exist after; nothing else changed

*Its run also satisfies the spec of:* remove

### die
Sources: wn v1: pass from physical life and lose all bodily attributes and functions necessary to sustain life / mw: to pass from physical life: expire

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| pass from life | `UPDATE things SET alive=0 WHERE name=:x AND alive=1` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 2 / 0 |
| WRONG: the worksheet minus live | `SELECT NOT alive FROM things WHERE name=:x` | FAIL: pass from life: not alive after | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 1 |
| WRONG: minus live on a stone | `SELECT NOT alive FROM things WHERE name='stone'` | FAIL: pass from life: not alive after | COMPARE, FIND, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): PRE: it was alive before; pass from life: not alive after; the body remains: the row still exists

*Finding:* "not alive" reads a state and changes nothing; it is true of the stone, which never lived and did not die. die is a change: alive before, not alive after, the row kept. That is the executed version of the worksheet finding.

### different
Sources: wn adj1: unlike in nature or quality or form or degree / mw: partly or totally unlike in nature, form, or quality: dissimilar

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| not identical, two apples apart | `SELECT (SELECT name\|\|place\|\|IFNULL(owner,'')\|\|value\|\|alive FROM things WHERE id=:a) <> (SELECT name\|\|place\|\|IFNULL(owner,'')\|\|value\|\|alive FROM things WHERE id=:b)` | PASS | COMPARE, FIND, HEAR, JOIN, READ, SAY | 0 / 0 / 12 / 1 |
| not identical, a thing and itself | `SELECT (SELECT name\|\|place\|\|IFNULL(owner,'')\|\|value\|\|alive FROM things WHERE id=:a) <> (SELECT name\|\|place\|\|IFNULL(owner,'')\|\|value\|\|alive FROM things WHERE id=:b)` | PASS | COMPARE, FIND, HEAR, JOIN, READ, SAY | 0 / 0 / 12 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when some field differs

*Its run also satisfies the spec of:* after, before, part

### empty
Sources: wn adj1: holding or containing nothing / mw: containing nothing

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| holding nothing | `SELECT COUNT(*)=0 FROM things WHERE place=:p` | PASS | ADD, COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 1 / 1 |
| holding nothing, asked of a place with things | `SELECT COUNT(*)=0 FROM things WHERE place=:p` | PASS | ADD, COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 1 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when nothing is there

### end
Sources: wn v1: bring to an end or halt / mw: to bring to an end

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| bring to a halt | `UPDATE state SET value='1' WHERE key='running'; UPDATE state SET value='0' WHERE key='running'; INSERT INTO timeline(t,event) VALUES((SELECT value FROM state WHERE key='now'),'end')` | PASS | CLOCK, COMPARE, FIND, READ, STATE, TIMELINE, WRITE | 0 / 3 / 4 / 0 |

Spec (each line is a check, quoting the source phrase): not running after

### exist
Sources: wn v1: have an existence, be extant / mw: to have real being whether material or spiritual

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| be extant | `SELECT EXISTS(SELECT 1 FROM things WHERE name=:x)` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 1 / 1 |
| be extant, asked of a thing that is not | `SELECT EXISTS(SELECT 1 FROM things WHERE name=:x)` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 1 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when there is such a thing

*Its run also satisfies the spec of:* part

### few
Sources: wn: a small but indefinite number / mw: not many persons or things

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| a small number: fewer than the others | `SELECT (SELECT COUNT(*) FROM things WHERE alive=0) < (SELECT COUNT(*) FROM things WHERE alive=1)` | PASS | ADD, COMPARE, FIND, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when the first count is smaller

*Finding:* few = the smaller side of the same compare that more is the greater side of: one COMPARE, two labels, opposite ends.

*Its run also satisfies the spec of:* more

### find
Sources: wn v1: come upon, as if by accident; meet with / mw: to come upon often accidentally: encounter / wn v3: discover or determine the existence, presence, or fact of

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| come upon the things with a property | `SELECT id FROM things WHERE place=:p` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 3 |
| WRONG: take whatever is first | `SELECT id FROM things LIMIT 1` | FAIL: what comes out has the property asked for, and all of them do | MOVE, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): what comes out has the property asked for, and all of them do; finding changes nothing

*Finding:* read and find reach the same roots (READ, COMPARE, FIND). They differ in what is in hand on arrival: an identity (read) or a property (find). That difference is the shard key, not the roots.

*Its run also satisfies the spec of:* part

### first
Sources: mw: preceding all others in time, order, or importance

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| preceding all others in time | `SELECT event FROM timeline ORDER BY t LIMIT 1` | PASS | MOVE, READ, SAY, TIMELINE | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): its time is the smallest

### forget
Sources: wn v1: dismiss from the mind; stop remembering / mw: to lose the remembrance of: be unable to think of or recall

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| stop holding it | `DELETE FROM memory WHERE words=:q; SELECT said FROM memory WHERE words=:q` | PASS | COMPARE, DELETE, FIND, HEAR, MEMORY, READ | 0 / 1 / 3 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: it was held before; stop remembering: not held after, nothing comes back

### full
Sources: wn adj1: containing as much or as many as is possible or normal / mw: containing as much or as many as is possible or normal

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| as many as is possible | `SELECT (SELECT COUNT(*) FROM things WHERE place='box') >= (SELECT value FROM state WHERE key='capacity')` | PASS | ADD, COMPARE, FIND, READ, SAY, STATE | 0 / 0 / 3 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when the count has reached the held capacity

*Finding:* full needs a capacity, which is state, not a thing: full = count compared with a held limit.

### give
Sources: wn v1: cause to have, in the abstract sense or physical sense / mw: to make a present of

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| cause another to have it | `UPDATE things SET owner=:to WHERE id=:i AND owner=:frm` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 2 / 0 |
| WRONG: copy it to them | `INSERT INTO things(name,place,owner,value,alive,t) SELECT name,place,:to,value,alive,t FROM things WHERE id=:i` | FAIL: cause to have: the receiver has it after; and the giver no longer has it | COMPARE, FIND, HEAR, READ, WRITE | 0 / 1 / 6 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: the giver had it; cause to have: the receiver has it after; and the giver no longer has it

*Finding:* Copying fails give on the last line: the giver still has it. A gift is a move of possession, not a copy.

*Its run also satisfies the spec of:* change, write

### have
Sources: wn v: have or possess, either in a concrete or an abstract sense / mw: to hold or maintain as a possession

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| possess | `SELECT EXISTS(SELECT 1 FROM things WHERE id=:i AND owner=:o)` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 1 |
| possess, asked of the wrong owner | `SELECT EXISTS(SELECT 1 FROM things WHERE id=:i AND owner=:o)` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when that owner holds the thing

*Its run also satisfies the spec of:* one, part

### if
Sources: mw: in the event that

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| the act happens only in the event | `UPDATE things SET owner=:o WHERE id=:i AND (:cond)=1` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 1 / 0 |
| the event does not hold | `UPDATE things SET owner=:o WHERE id=:i AND (:cond)=1` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 0 / 1 / 0 |

Spec (each line is a check, quoting the source phrase): when the condition holds the thing changes; when not, nothing changes

*Its run also satisfies the spec of:* change, write

### into
Sources: mw: used as a function word to indicate entry, introduction, insertion, superposition, or inclusion

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| the place a write goes | `INSERT INTO things(name,place,t) VALUES(:x,:p,1)` | PASS | HEAR, WRITE | 0 / 1 / 0 / 0 |
| WRONG: a write with no into | `INSERT things(name,place,t) VALUES(:x,:p,1)` | FAIL: after, the thing is in that place (near "things": syntax error) | HEAR, WRITE | 0 / 0 / 0 / 0 |

Spec (each line is a check, quoting the source phrase): after, the thing is in that place

*Finding:* into is the destination hole of a write or a move. Without it the write has nowhere to go and the silicon refuses the line (a syntax error). It has no run of its own; it is a slot in another run.

*Its run also satisfies the spec of:* create, write

### join
Sources: wn n2: a set containing all and only the members of two or more given sets / wn v4: make contact or come together / mw: to put or bring together so as to form a unit

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| bring two parts together | `CREATE TABLE part1 AS SELECT * FROM things WHERE value>=3; CREATE TABLE part2 AS SELECT * FROM things WHERE value<3; CREATE TABLE joined AS SELECT * FROM part1 UNION SELECT * FROM part2` | PASS | COMPARE, FIND, JOIN, READ, SPAWN | 3 / 0 / 33 / 0 |
| WRONG: pair them up by a key (SQL JOIN) | `CREATE TABLE part1 AS SELECT * FROM things WHERE value>=3; CREATE TABLE part2 AS SELECT * FROM things WHERE value<3; CREATE TABLE joined AS SELECT p1.id, p2.id AS id2 FROM part1 p1 JOIN part2 p2 ON p1.place=p2.place` | FAIL: all and only the members of both | COMPARE, FIND, JOIN, READ, SPAWN | 3 / 0 / 23 / 0 |

Spec (each line is a check, quoting the source phrase): all and only the members of both

*Finding:* SQL JOIN is a different meaning under the same letters (pairing by a shared key). That is the encoder's business: two gates, one spelling.

*Its run also satisfies the spec of:* split

### keep
Sources: mw: to retain in one's possession or power / wn v: keep in a certain state, position, or activity

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| retain over time | `UPDATE state SET value=value+5 WHERE key='now'; SELECT owner FROM things WHERE id=:i` | PASS | ADD, CLOCK, COMPARE, FIND, HEAR, READ, SAY, STATE, WRITE | 0 / 1 / 4 / 1 |
| WRONG: give it away meanwhile | `UPDATE things SET owner='bob' WHERE id=:i; UPDATE state SET value=value+5 WHERE key='now'; SELECT owner FROM things WHERE id=:i` | FAIL: still has it after | ADD, CLOCK, COMPARE, FIND, HEAR, READ, SAY, STATE, WRITE | 0 / 2 / 5 / 1 |

Spec (each line is a check, quoting the source phrase): PRE: had it before; time passed; still has it after

*Finding:* keep is a test across time: possession at t2 equals possession at t1. Nothing is written to the thing; the clock moves.

### kill
Sources: wn v1: cause to die; put to death / mw: to deprive of life

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| cause to die | `UPDATE things SET alive=0 WHERE name=:x AND alive=1; INSERT INTO timeline(t,event) VALUES((SELECT value FROM state WHERE key='now'), :who\|\|' killed '\|\|:x)` | PASS | CLOCK, COMPARE, FIND, HEAR, JOIN, READ, STATE, TIMELINE, WRITE | 0 / 2 / 4 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: it was alive before; the thing died; and someone caused it: the actor is on the timeline

*Finding:* kill = die + a cause. The cause is not in the thing; it is in the receipt (the timeline row naming the actor).

*Its run also satisfies the spec of:* die

### last
Sources: mw: following all the rest

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| following all the rest | `SELECT event FROM timeline ORDER BY t DESC LIMIT 1` | PASS | MOVE, READ, SAY, TIMELINE | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): its time is the largest

*Finding:* first and last: one ORDER, two ends. The same shape as before/after and more/few: an axis, read from either end.

### live
Sources: mw: to be alive: have the life of an animal or plant / wn v2: lead a certain kind of life; live in a certain style

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| be alive | `SELECT alive FROM things WHERE name=:x` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 1 |
| be alive, asked of a stone | `SELECT alive FROM things WHERE name=:x` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): says what the thing's life is

*Its run also satisfies the spec of:* none

### lose
Sources: wn v1: fail to keep or to maintain; cease to have, either physically or in an abstract sense / mw: to miss from one's possession or from a customary or supposed place

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| cease to have | `UPDATE things SET owner=NULL WHERE id=:i AND owner=:me` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 2 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: had it; ceases to have it

*Finding:* lose and give end in the same state for the loser. They differ only in the receipt: who did it and whether anyone received. Some meanings are told apart by history, not by the state they leave.

*Its run also satisfies the spec of:* change, write

### more
Sources: wn: greater in size or amount or number / mw: greater

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| a greater number | `SELECT (SELECT COUNT(*) FROM things WHERE alive=1) > (SELECT COUNT(*) FROM things WHERE alive=0)` | PASS | ADD, COMPARE, FIND, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when the first count is greater

*Its run also satisfies the spec of:* few

### move
Sources: wn v1: change location; move, travel, or proceed / mw: to go or pass to another place or in a certain direction

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| change the place | `UPDATE things SET place=:to WHERE id=:i` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 1 / 0 |
| WRONG: copy it there | `INSERT INTO things(name,place,owner,value,alive,t) SELECT name,:to,owner,value,alive,t FROM things WHERE id=:i` | FAIL: and no longer at the old one; the same number of things | COMPARE, FIND, HEAR, READ, WRITE | 0 / 1 / 6 / 0 |
| copy it there, then remove it from here | `INSERT INTO things(name,place,owner,value,alive,t) SELECT name,:to,owner,value,alive,t FROM things WHERE id=:i; DELETE FROM things WHERE id=:i` | PASS | COMPARE, DELETE, FIND, HEAR, READ, WRITE | 0 / 2 / 7 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: it was at the old place; change location: it is at the new place after; and no longer at the old one; the same number of things

*Finding:* copy fails move on one line only: the thing is still at the old place. move = copy + remove-from-old, which is one DELETE more.

*Its run also satisfies the spec of:* change, write

### new
Sources: wn adj: not of long duration; having just come into existence / mw: having recently come into existence: recent, modern

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| born now | `INSERT INTO things(name,place,t) VALUES(:x,:p,(SELECT value FROM state WHERE key='now')); SELECT name FROM things WHERE t=(SELECT value FROM state WHERE key='now')` | PASS | CLOCK, COMPARE, FIND, HEAR, READ, SAY, STATE, WRITE | 0 / 1 / 6 / 1 |

Spec (each line is a check, quoting the source phrase): just come into existence: the new things are exactly those born at now, the created one among them

*Finding:* new is a time test on create: born at the clock reading now.

*Its run also satisfies the spec of:* create, into, write

### none
Sources: mw: not any / wn adv: not at all or in no way

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| not any, of a thing there is none of | `SELECT NOT EXISTS(SELECT 1 FROM things WHERE name=:x)` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 1 / 1 |
| not any, of a thing there is some of | `SELECT NOT EXISTS(SELECT 1 FROM things WHERE name=:x)` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 1 / 1 |

Spec (each line is a check, quoting the source phrase): says yes exactly when no such thing exists

*Its run also satisfies the spec of:* part

### not
Sources: wn: negation of a word or group of words / mw: used as a function word to make negative a group of words or a word

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| turn the yes into no | `SELECT NOT (:t), NOT (NOT (:t))` | PASS | COMPARE, HEAR, READ, SAY | 0 / 0 / 0 / 1 |

Spec (each line is a check, quoting the source phrase): negation turns 1 into 0; and back

### now
Sources: wn n: the momentary present / mw: at the present time or moment

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| the clock reading at this moment | `SELECT value FROM state WHERE key='now'` | PASS | CLOCK, COMPARE, FIND, READ, SAY, STATE | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): it is the present reading of the clock

### one
Sources: wn: used of a single unit or thing; not two or more / wn n: the smallest whole number

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| a single unit | `SELECT COUNT(*) FROM things WHERE id=:i` | PASS | ADD, COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 1 |
| a single unit, asked of a thing that is not there | `SELECT COUNT(*) FROM things WHERE id=:i` | PASS | ADD, COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): the count is one exactly when there is a single such thing

*Its run also satisfies the spec of:* part

### or
Sources: mw: used as a function word to indicate an alternative

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| either | `SELECT id FROM things WHERE place='box' OR alive=0` | PASS | COMPARE, FIND, READ, SAY | 0 / 0 / 3 / 3 |

Spec (each line is a check, quoting the source phrase): the rows are those in either set; never fewer than either set alone

### order
Sources: mw: to put in order: arrange / wn sort v1: arrange or order by classes or categories

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| arrange in sequence | `SELECT id, value FROM things ORDER BY value` | PASS | MOVE, READ, SAY | 0 / 0 / 3 / 5 |

Spec (each line is a check, quoting the source phrase): the sequence never goes down; the same members, rearranged

*Its run also satisfies the spec of:* all, whole

### part
Sources: wn n2: something determined in relation to something that includes it / mw: one of the often indefinite or unequal subdivisions into which something is or is regarded as divided

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| a subdivision of the whole | `SELECT id FROM things WHERE place='box'` | PASS | COMPARE, FIND, READ, SAY | 0 / 0 / 2 / 3 |

Spec (each line is a check, quoting the source phrase): included in the whole; not the whole

### read
Sources: mw: to receive or take in the sense of (letters, symbols, etc.) especially by sight or touch / wn v1: interpret something that is written or printed

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| take in what is written at a known place | `SELECT name,place,owner,value FROM things WHERE id=:i` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 5 / 1 |
| WRONG: change it while looking | `UPDATE things SET value=value+1 WHERE id=:i; SELECT name,place,owner,value FROM things WHERE id=:i` | FAIL: what comes out is what is written there; taking in changes nothing | ADD, COMPARE, FIND, HEAR, READ, SAY, WRITE | 0 / 1 / 7 / 1 |

Spec (each line is a check, quoting the source phrase): what comes out is what is written there; taking in changes nothing

### remember
Sources: wn v1: recall knowledge from memory; have a recollection / mw: to bring to mind or think of again

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| bring back from memory | `SELECT said FROM memory WHERE words=:q` | PASS | COMPARE, FIND, HEAR, MEMORY, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): what comes back is what was laid in memory; bringing back changes nothing

*Finding:* remember = read from memory. It presupposes a store; without the earlier write there is nothing to bring back.

### remove
Sources: wn v1: remove something concrete, as by lifting, pushing, or taking off, or remove something abstract / mw: to change the location, position, station, or residence of; to move by lifting, pushing aside, or taking away or off

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| take the row away | `DELETE FROM things WHERE name=:x` | PASS | COMPARE, DELETE, FIND, HEAR | 0 / 1 / 1 / 0 |
| move it away from the place | `UPDATE things SET place=NULL WHERE name=:x` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 1 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: it was there before; taken away: it is not there after; nothing else changed

*Finding:* Both runs pass remove; only the first passes delete. remove is "away from here", delete is "gone from everywhere": delete is one shard of remove.

*Its run also satisfies the spec of:* delete, write

### same
Sources: wn adj1: same in identity / mw: resembling in every relevant respect; being one without addition, change, or discontinuance: identical

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| identical in every field, a thing and itself | `SELECT (SELECT name\|\|place\|\|IFNULL(owner,'')\|\|value\|\|alive FROM things WHERE id=:a) = (SELECT name\|\|place\|\|IFNULL(owner,'')\|\|value\|\|alive FROM things WHERE id=:b)` | PASS | COMPARE, FIND, HEAR, JOIN, READ, SAY | 0 / 0 / 12 / 1 |
| identical in every field, two apples in different places | `SELECT (SELECT name\|\|place\|\|IFNULL(owner,'')\|\|value\|\|alive FROM things WHERE id=:a) = (SELECT name\|\|place\|\|IFNULL(owner,'')\|\|value\|\|alive FROM things WHERE id=:b)` | PASS | COMPARE, FIND, HEAR, JOIN, READ, SAY | 0 / 0 / 12 / 1 |
| WRONG: same name only, two apples in different places | `SELECT (SELECT name FROM things WHERE id=:a) = (SELECT name FROM things WHERE id=:b)` | FAIL: a thing is the same as itself; two things unlike in some respect are not the same | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 4 / 1 |

Spec (each line is a check, quoting the source phrase): a thing is the same as itself; two things unlike in some respect are not the same

*Finding:* Identity in every relevant respect: a weaker compare (name only) calls two different apples the same, and fails.

*Its run also satisfies the spec of:* part

### sell
Sources: wn v1: exchange or deliver for money or its equivalent / mw: to give up (property) to another for something of value (such as money)

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| deliver for money | `UPDATE things SET owner=:buyer WHERE id=:i AND owner=:seller; UPDATE purse SET money=money-:price WHERE owner=:buyer; UPDATE purse SET money=money+:price WHERE owner=:seller` | PASS | ADD, COMPARE, FIND, HEAR, SUBTRACT, WRITE | 0 / 3 / 6 / 0 |

Spec (each line is a check, quoting the source phrase): give up the property; for money: the seller has more by the price

*Finding:* sell is buy from the other end: the same run, the holes swapped. One place, two labels, two arrivals.

*Its run also satisfies the spec of:* buy, change, write

### shop
Sources: wn n1: a mercantile establishment for the retail sale of goods or services / mw: a building or room stocked with merchandise for sale

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| a place stocked with things that leave when paid for | `INSERT INTO things(name,place,owner,value,alive,t) VALUES('hat','shop','shop',3,0,9); UPDATE things SET owner='ann' WHERE name='hat' AND place='shop' AND owner='shop'; UPDATE purse SET money=money-3 WHERE owner='ann'; UPDATE purse SET money=money+3 WHERE owner='shop'; UPDATE things SET place='table' WHERE name='hat'` | PASS | ADD, COMPARE, FIND, SUBTRACT, WRITE | 0 / 5 / 8 / 0 |

Spec (each line is a check, quoting the source phrase): a place with goods for sale, owned by the shop; after a sale the good is the buyer's and the shop has the money

*Finding:* shop is not a run; it is a place where the sell run happens, over and over. Its meaning is the place plus the process: a noun made of a verb. "place be" was wrong: the process was missing.

*Its run also satisfies the spec of:* write

### some
Sources: wn: quantifier; used to indicate an unspecified number or quantity / mw: being an unknown, undetermined, or unspecified unit or thing

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| an unspecified number, at least one | `SELECT id FROM things WHERE alive=1` | PASS | COMPARE, FIND, READ, SAY | 0 / 0 / 2 / 4 |

Spec (each line is a check, quoting the source phrase): at least one; a number not fixed in advance

*Finding:* some is a count between one and all; which count is not fixed by the word.

*Its run also satisfies the spec of:* part

### split
Sources: wn v1: separate into parts or portions / mw: to divide lengthwise usually along a grain or seam or by layers

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| two parts by a cut | `CREATE TABLE part1 AS SELECT * FROM things WHERE value>=:k; CREATE TABLE part2 AS SELECT * FROM things WHERE value<:k` | PASS | COMPARE, FIND, HEAR, READ, SPAWN | 2 / 0 / 18 / 0 |
| WRONG: two copies of all | `CREATE TABLE part1 AS SELECT * FROM things; CREATE TABLE part2 AS SELECT * FROM things` | FAIL: separate into parts: each thing is in exactly one part; the parts together are the whole | READ, SPAWN | 2 / 0 / 16 / 0 |

Spec (each line is a check, quoting the source phrase): separate into parts: each thing is in exactly one part; the parts together are the whole; no part is empty

### store
Sources: wn v1: keep or lay aside for future use / mw: to lay away

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| lay aside now, take back later | `INSERT INTO memory(words,said,t) VALUES(:w,:w,(SELECT value FROM state WHERE key='now')); UPDATE state SET value=value+5 WHERE key='now'; SELECT said FROM memory WHERE words=:w` | PASS | ADD, CLOCK, COMPARE, FIND, HEAR, MEMORY, READ, SAY, STATE, WRITE | 0 / 2 / 6 / 1 |
| WRONG: lay aside then lose it | `INSERT INTO memory(words,said,t) VALUES(:w,:w,(SELECT value FROM state WHERE key='now')); DELETE FROM memory WHERE words=:w; UPDATE state SET value=value+5 WHERE key='now'; SELECT said FROM memory WHERE words=:w` | FAIL: laid aside: held after; for future use: readable later, unchanged | ADD, CLOCK, COMPARE, DELETE, FIND, HEAR, MEMORY, READ, STATE, WRITE | 0 / 3 / 7 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: not held before; laid aside: held after; for future use: readable later, unchanged

*Finding:* store = write to memory + keep. keep alone writes nothing; store writes first. Different pre-state, shared tail.

### subtract
Sources: mw: to take away by or as if by deducting / wn v1: make a subtraction

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| take away | `UPDATE things SET value=value-:k WHERE id=:i` | PASS | COMPARE, FIND, HEAR, SUBTRACT, WRITE | 0 / 1 / 2 / 0 |

Spec (each line is a check, quoting the source phrase): the value after is the value before minus k

*Finding:* add and subtract: one axis, two directions, like more/few and before/after.

*Its run also satisfies the spec of:* change, write

### take
Sources: mw: to get into one's hands or into one's possession, power, or control / wn get v1: come into the possession of something concrete or abstract

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| come into possession | `UPDATE things SET owner=:me WHERE id=:i` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 1 / 0 |

Spec (each line is a check, quoting the source phrase): PRE: I did not have it; into my possession: I have it after; the other no longer has it

*Finding:* give and take are the same run (owner changes from one to another) seen from the two ends. Same roots, same place; the holes (who is I) differ. That is the arrival picking the shard.

*Its run also satisfies the spec of:* change, write

### the
Sources: mw: used as a function word to indicate that a following noun is definite or has been previously specified by context

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| the one already in play | `SELECT id FROM things WHERE id=(SELECT value FROM state WHERE key='it')` | PASS | COMPARE, FIND, READ, SAY, STATE | 0 / 0 / 5 / 1 |
| WRONG: any one | `SELECT id FROM things LIMIT 1` | FAIL: exactly one, and it is the one previously specified (state it) | MOVE, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): exactly one, and it is the one previously specified (state it)

*Finding:* the is a FIND in state: the thing the run already has in play. It reads state and nothing else.

*Its run also satisfies the spec of:* part

### two
Sources: wn: being one more than one / wn n: the cardinal number that is the sum of one and one

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| one more than one | `SELECT COUNT(*), 1+1 FROM things WHERE name='apple'` | PASS | ADD, COMPARE, FIND, READ, SAY | 0 / 0 / 1 / 1 |

Spec (each line is a check, quoting the source phrase): the count is one and one

*Its run also satisfies the spec of:* part

### when
Sources: mw: at what time / mw: at or during which time

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| the time an event happened | `SELECT t FROM timeline WHERE event=:e` | PASS | COMPARE, FIND, HEAR, READ, SAY, TIMELINE | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): the answer is the time of that event

### where
Sources: mw: at, in, or to what place

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| the place of a thing | `SELECT place FROM things WHERE id=:i` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 2 / 1 |

Spec (each line is a check, quoting the source phrase): the answer is its place

### which
Sources: mw: being what one or ones out of a group

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| the one out of a group with the property | `SELECT id FROM things WHERE name='apple' AND place=:p` | PASS | COMPARE, FIND, HEAR, READ, SAY | 0 / 0 / 3 / 1 |

Spec (each line is a check, quoting the source phrase): one out of the group, picked by the property

### whole
Sources: wn: all of something including all its component elements or parts

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| all the parts together | `SELECT id FROM things` | PASS | READ, SAY | 0 / 0 / 2 / 5 |

Spec (each line is a check, quoting the source phrase): includes every part

*Finding:* whole runs the same as all: one meaning, two labels.

*Its run also satisfies the spec of:* all

### write
Sources: mw: to form (characters, symbols, etc.) by or as if by marking on a surface / wn v2: communicate or express by writing

| candidate run | SQL | result | roots | graph / rows written / reads / said |
|---|---|---|---|---|
| a new mark | `INSERT INTO things(name,place,t) VALUES(:x,:p,(SELECT value FROM state WHERE key='now'))` | PASS | CLOCK, COMPARE, FIND, HEAR, READ, STATE, WRITE | 0 / 1 / 2 / 0 |
| a changed mark | `UPDATE things SET owner=:v WHERE id=:i` | PASS | COMPARE, FIND, HEAR, WRITE | 0 / 1 / 1 / 0 |
| WRONG: only look | `SELECT * FROM things` | FAIL: a mark exists after that did not before | READ, SAY | 0 / 0 / 7 / 5 |

Spec (each line is a check, quoting the source phrase): a mark exists after that did not before

*Finding:* write has two shards: the new mark (which is also create's row shard) and the changed mark. create and write share one shard; that is where their places overlap.

*Its run also satisfies the spec of:* change, create, into

## 3. Same place by roots: one run, several labels
Passing runs that fire exactly the same set of roots. By your law, two words with exactly one meaning share a gate; where the roots coincide but the holes differ, the arrival picks the shard.

- **CLOCK,COMPARE,FIND,HEAR,READ,STATE,WRITE**: create [row]; copy [duplicate the row]; write [a new mark]; born [brought into existence, alive]
- **COMPARE,DELETE,FIND,HEAR**: delete [remove the row]; remove [take the row away]
- **COMPARE,FIND,HEAR,WRITE**: remove [move it away from the place]; move [change the place]; write [a changed mark]; if [the act happens only in the event]; if [the event does not hold]; give [cause another to have it]; take [come into possession]; change [make different: write what is not there]; die [pass from life]; lose [cease to have]
- **COMPARE,FIND,HEAR,READ,SAY**: read [take in what is written at a known place]; find [come upon the things with a property]; none [not any, of a thing there is none of]; none [not any, of a thing there is some of]; between [in the interval]; have [possess]; have [possess, asked of the wrong owner]; exist [be extant]; exist [be extant, asked of a thing that is not]; live [be alive]; live [be alive, asked of a stone]; where [the place of a thing]; which [the one out of a group with the property]
- **COMPARE,FIND,HEAR,JOIN,READ,SAY**: same [identical in every field, a thing and itself]; same [identical in every field, two apples in different places]; different [not identical, two apples apart]; different [not identical, a thing and itself]
- **COMPARE,FIND,READ,SAY**: and [both at once]; or [either]; some [an unspecified number, at least one]; part [a subdivision of the whole]
- **READ,SAY**: all [every one]; whole [all the parts together]
- **ADD,COMPARE,FIND,HEAR,READ,SAY**: one [a single unit]; one [a single unit, asked of a thing that is not there]; count [find the total number]; empty [holding nothing]; empty [holding nothing, asked of a place with things]
- **ADD,COMPARE,FIND,READ,SAY**: two [one more than one]; more [a greater number]; few [a small number: fewer than the others]
- **COMPARE,FIND,HEAR,READ,SAY,TIMELINE**: before [earlier in time]; before [earlier in time, asked the other way round]; after [later in time]; after [later in time, asked the other way round]; when [the time an event happened]
- **ADD,COMPARE,FIND,HEAR,SUBTRACT,WRITE**: buy [possession one way, money the other]; sell [deliver for money]
- **MOVE,READ,SAY,TIMELINE**: first [preceding all others in time]; last [following all the rest]
- **CLOCK,COMPARE,FIND,READ,STATE,TIMELINE,WRITE**: begin [set in motion]; end [bring to a halt]

What the groups say:
- **give, take, lose, move, change, if**: one physical run, a WRITE after a COMPARE and FIND. They differ only in which hole is filled by whom (giver, taker, nobody), or in which field changes (owner, place, any). The run is shared; the meanings are told apart by the holes and by the receipt. That is the shard key, exactly as you described it.
- **delete and remove**: identical roots, identical runs. One meaning, two labels. remove also has a second shard (move away, no delete) that delete does not have.
- **read, find, have, exist, live, where, which, none, between**: all are a READ after a COMPARE and FIND, saying back what they found. They differ only in which column is compared and what is said. These are one family: the questions.
- **create, copy, write (new mark), born**: one run, WRITE a row with the clock. born adds alive; copy reads an existing row first. The places overlap at the write.
- **before, after, when**: one COMPARE on two times from the timeline. before and after are the two directions of it; when is the time itself.
- **more and few**, **first and last**, **add and subtract**, **begin and end**, **buy and sell**: each pair is one run read from the two ends of an axis. The flip between them is the axis flip, not a negation. The worksheet's single minus could not express this, and now the executed runs show it.

## 4. Entailments found by running, not by reading
A run of the first word satisfies the spec of the second on every applicable world. These are relations the sources never state; the silicon produced them. (Runs that only show a word "returns some rows" are left out.)

- **a** entails part
- **add** entails change, write
- **all** entails whole
- **between** entails part
- **born** entails create, into, write
- **buy** entails change, sell, write
- **change** entails write
- **copy** entails write
- **count** entails part
- **create** entails into, write
- **delete** entails remove
- **different** entails after, before, part
- **exist** entails part
- **few** entails more
- **find** entails part
- **give** entails change, write
- **have** entails one, part
- **if** entails change, write
- **into** entails create, write
- **join** entails split
- **kill** entails die
- **live** entails none
- **lose** entails change, write
- **more** entails few
- **move** entails change, write
- **new** entails create, into, write
- **none** entails part
- **one** entails part
- **order** entails all, whole
- **remove** entails delete, write
- **same** entails part
- **sell** entails buy, change, write
- **shop** entails write
- **some** entails part
- **subtract** entails change, write
- **take** entails change, write
- **the** entails part
- **two** entails part
- **whole** entails all
- **write** entails change, create, into

Read as kinds: every buy is a take; every born is a create; every move is a change and a write; every delete is a remove; every new is a create; the two apples compared are different *and* the compare says before and after about their times (a coincidence of the ten worlds that a word with a time hole would break: this is why the brain needs many uses, not a few).

## 5. What the wrong runs taught
- **create**, read it: failed on "bring into existence: it exists after"
- **delete**, hide by moving: failed on "remove: it does not exist after; nothing else changed"
- **copy**, move it: failed on "the original is unchanged; a duplicate exists after: same in every field but identity and birth time; one more thing exists"
- **move**, copy it there: failed on "and no longer at the old one; the same number of things"
- **split**, two copies of all: failed on "separate into parts: each thing is in exactly one part; the parts together are the whole"
- **join**, pair them up by a key (SQL JOIN): failed on "all and only the members of both"
- **read**, change it while looking: failed on "what comes out is what is written there; taking in changes nothing"
- **write**, only look: failed on "a mark exists after that did not before"
- **find**, take whatever is first: failed on "what comes out has the property asked for, and all of them do"
- **same**, same name only, two apples in different places: failed on "a thing is the same as itself; two things unlike in some respect are not the same"
- **before**, the worksheet minus now: failed on "says yes exactly when a happened at an earlier time than b"
- **the**, any one: failed on "exactly one, and it is the one previously specified (state it)"
- **keep**, give it away meanwhile: failed on "still has it after"
- **store**, lay aside then lose it: failed on "laid aside: held after; for future use: readable later, unchanged"
- **give**, copy it to them: failed on "cause to have: the receiver has it after; and the giver no longer has it"
- **buy**, take without paying: failed on "by payment: the buyer has less money by the price; and the seller has more by the price"
- **change**, set a value that may already be there: failed on ""
- **die**, the worksheet minus live: failed on "pass from life: not alive after"
- **die**, minus live on a stone: failed on "pass from life: not alive after"
- **into**, a write with no into: failed on "after, the thing is in that place" (near "things": syntax error)

The pattern: a wrong run is one that leaves out one physical step the definition names (the delete in move, the money in buy, the write in create), or adds one it forbids (the write in read), or reads a state where the definition names a change (minus-live for die, minus-now for before). The test finds the missing or extra step by name. Nothing about the letters of the word enters into it.

## 6. What each run does to the graph, the silicon, memory, state and time
| word | run | schema (graph) | rows written | reads | rows said | memory | state | timeline |
|---|---|---|---|---|---|---|---|---|
| create | row | 0 | 1 | 2 | 0 |  | yes |  |
| create | table | 1 | 0 | 1 | 0 |  |  |  |
| new | born now | 0 | 1 | 6 | 1 |  | yes |  |
| delete | remove the row | 0 | 1 | 1 | 0 |  |  |  |
| remove | take the row away | 0 | 1 | 1 | 0 |  |  |  |
| remove | move it away from the place | 0 | 1 | 1 | 0 |  |  |  |
| copy | duplicate the row | 0 | 1 | 8 | 0 |  | yes |  |
| move | change the place | 0 | 1 | 1 | 0 |  |  |  |
| move | copy it there, then remove it from here | 0 | 2 | 7 | 0 |  |  |  |
| split | two parts by a cut | 2 | 0 | 18 | 0 |  |  |  |
| join | bring two parts together | 3 | 0 | 33 | 0 |  |  |  |
| read | take in what is written at a known place | 0 | 0 | 5 | 1 |  |  |  |
| write | a new mark | 0 | 1 | 2 | 0 |  | yes |  |
| write | a changed mark | 0 | 1 | 1 | 0 |  |  |  |
| find | come upon the things with a property | 0 | 0 | 2 | 3 |  |  |  |
| same | identical in every field, a thing and it | 0 | 0 | 12 | 1 |  |  |  |
| same | identical in every field, two apples in  | 0 | 0 | 12 | 1 |  |  |  |
| different | not identical, two apples apart | 0 | 0 | 12 | 1 |  |  |  |
| different | not identical, a thing and itself | 0 | 0 | 12 | 1 |  |  |  |
| not | turn the yes into no | 0 | 0 | 0 | 1 |  |  |  |
| and | both at once | 0 | 0 | 3 | 2 |  |  |  |
| or | either | 0 | 0 | 3 | 3 |  |  |  |
| if | the act happens only in the event | 0 | 1 | 1 | 0 |  |  |  |
| if | the event does not hold | 0 | 0 | 1 | 0 |  |  |  |
| all | every one | 0 | 0 | 2 | 5 |  |  |  |
| some | an unspecified number, at least one | 0 | 0 | 2 | 4 |  |  |  |
| none | not any, of a thing there is none of | 0 | 0 | 1 | 1 |  |  |  |
| none | not any, of a thing there is some of | 0 | 0 | 1 | 1 |  |  |  |
| one | a single unit | 0 | 0 | 2 | 1 |  |  |  |
| one | a single unit, asked of a thing that is  | 0 | 0 | 2 | 1 |  |  |  |
| two | one more than one | 0 | 0 | 1 | 1 |  |  |  |
| more | a greater number | 0 | 0 | 2 | 1 |  |  |  |
| few | a small number: fewer than the others | 0 | 0 | 2 | 1 |  |  |  |
| before | earlier in time | 0 | 0 | 4 | 1 |  |  | yes |
| before | earlier in time, asked the other way rou | 0 | 0 | 4 | 1 |  |  | yes |
| after | later in time | 0 | 0 | 4 | 1 |  |  | yes |
| after | later in time, asked the other way round | 0 | 0 | 4 | 1 |  |  | yes |
| now | the clock reading at this moment | 0 | 0 | 2 | 1 |  | yes |  |
| when | the time an event happened | 0 | 0 | 2 | 1 |  |  | yes |
| the | the one already in play | 0 | 0 | 5 | 1 |  | yes |  |
| a | any one of the kind | 0 | 0 | 2 | 1 |  |  |  |
| between | in the interval | 0 | 0 | 2 | 2 |  |  |  |
| part | a subdivision of the whole | 0 | 0 | 2 | 3 |  |  |  |
| whole | all the parts together | 0 | 0 | 2 | 5 |  |  |  |
| keep | retain over time | 0 | 1 | 4 | 1 |  | yes |  |
| store | lay aside now, take back later | 0 | 2 | 6 | 1 | yes | yes |  |
| have | possess | 0 | 0 | 2 | 1 |  |  |  |
| have | possess, asked of the wrong owner | 0 | 0 | 2 | 1 |  |  |  |
| give | cause another to have it | 0 | 1 | 2 | 0 |  |  |  |
| take | come into possession | 0 | 1 | 1 | 0 |  |  |  |
| buy | possession one way, money the other | 0 | 3 | 6 | 0 |  |  |  |
| sell | deliver for money | 0 | 3 | 6 | 0 |  |  |  |
| shop | a place stocked with things that leave w | 0 | 5 | 8 | 0 |  |  |  |
| count | find the total number | 0 | 0 | 1 | 1 |  |  |  |
| order | arrange in sequence | 0 | 0 | 3 | 5 |  |  |  |
| first | preceding all others in time | 0 | 0 | 2 | 1 |  |  | yes |
| last | following all the rest | 0 | 0 | 2 | 1 |  |  | yes |
| empty | holding nothing | 0 | 0 | 1 | 1 |  |  |  |
| empty | holding nothing, asked of a place with t | 0 | 0 | 1 | 1 |  |  |  |
| full | as many as is possible | 0 | 0 | 3 | 1 |  | yes |  |
| change | make different: write what is not there | 0 | 1 | 2 | 0 |  |  |  |
| remember | bring back from memory | 0 | 0 | 2 | 1 | yes |  |  |
| forget | stop holding it | 0 | 1 | 3 | 0 | yes |  |  |
| exist | be extant | 0 | 0 | 1 | 1 |  |  |  |
| exist | be extant, asked of a thing that is not | 0 | 0 | 1 | 1 |  |  |  |
| begin | set in motion | 0 | 2 | 3 | 0 |  | yes | yes |
| end | bring to a halt | 0 | 3 | 4 | 0 |  | yes | yes |
| live | be alive | 0 | 0 | 2 | 1 |  |  |  |
| live | be alive, asked of a stone | 0 | 0 | 2 | 1 |  |  |  |
| die | pass from life | 0 | 1 | 2 | 0 |  |  |  |
| kill | cause to die | 0 | 2 | 4 | 0 |  | yes | yes |
| born | brought into existence, alive | 0 | 1 | 2 | 0 |  | yes |  |
| into | the place a write goes | 0 | 1 | 0 | 0 |  |  |  |
| add | bring about an increase | 0 | 1 | 2 | 0 |  |  |  |
| subtract | take away | 0 | 1 | 2 | 0 |  |  |  |
| where | the place of a thing | 0 | 0 | 2 | 1 |  |  |  |
| which | the one out of a group with the property | 0 | 0 | 3 | 1 |  |  |  |
| lose | cease to have | 0 | 1 | 2 | 0 |  |  |  |

The ratio you asked about, measured: only create-table, split and join touch the graph's schema. The questions (read, find, have, exist, live, where, which, same, different, count, more, few, all, some, the, a, between, part, before, after, when, now) write nothing: they are reads and compares that say something back. The doers (create, write, copy, move, delete, remove, give, take, buy, sell, add, subtract, change, die, kill, born, begin, end, store, forget) write rows. The words that reach the brain's own tables: now, new, create-row, copy, write, born, keep, store, full, the, begin, end (state); before, after, when, first, last, kill, begin, end (timeline); store, remember, forget (memory). into is a slot in another run, with no run of its own: the silicon refuses a write without it.

## 7. What the brain still has to do itself, and what this file is not

- **The spec step is the gap.** I turned each definition's phrases into checks by hand ("bring into existence" became: not there before, there after, nothing else changed). The brain has to learn to do that: read a definition row, pick out what must be true before and after, and write those as its own checks. Until it does, every meaning it compiles is a description. That step is where "understanding" lives, and it is not built anywhere yet.
- **The candidate step is search.** Once a spec exists, finding a run that satisfies it is search over strings of physics gates, checked by execution, the way this file did it with SQL. That the brain can do with what it has: lay a candidate, run it on its own scratch tables, read the state back, keep the receipt. Wrong candidates are kept as wrong, as the owner's rule says.
- **Worlds are uses.** A run held after four worlds broke on the sixth (change by setting a value that was already there; die on a thing already dead). Ten worlds separate most of the words here; some coincidences remain (section 4). The brain gets its worlds from uses: every sentence it hears is a world to test held meanings against.
- **Preconditions are part of the meaning.** die needs alive before; give needs the giver holding it; forget needs something held. A world where the precondition fails is not a counterexample; it is not a use of that word. The harness treats it that way, and so must the brain.
- **This is not the brain.** It is a measurement of what fifty-odd words do when their runs execute, kept as rows the brain can be told as a source. It lays nothing in any build. The runs are SQL because SQL is the crutch; each maps to the physics gates by the roots column.
