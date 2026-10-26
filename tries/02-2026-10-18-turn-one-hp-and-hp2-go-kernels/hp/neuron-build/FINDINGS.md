# FINDINGS (adversary, turn one, hp)

Each entry: what the brain did / what the scope says / the brain's own rows. Rank: BREAKS / BENDS / COSMETIC. Times are from acts.log (local) and the timeline (unix ms). Birth: 01:29:18.466, BORN gates=1158.

## 1. BREAKS: a self-feeding fault storm from the first input until it was killed

**What the brain did.** From the first input ("1 + 1 =", 01:29:42) the beat never rested again. A run (the sixth, worth 0.5) hit a refused DELETE.row; the refusal put outcome `no` (gate 113) at the head of its remainder; passing gate 113 fired its two usual triggers (correct-find #505 and backpop-from-why #1040, worth 0.25 each); the sixth was restarted as soon as those two children ended; it picked the same row again (the one `slow` row, mem 56, which it never managed to delete), was refused again, and so on. Beats: 26 at 01:29:42.807, 59212 at 01:29:49.309, 105021 at 01:29:54.298 (about 9,000 beats a second). Runs: 65 at 01:29:42.9 -> 1,615,108 at 01:30:41 when the process was killed. acts.log grew to 1,615,144 lines (44 MB) in 59 seconds. The kernel's own fault floors (MissDepth, STUCK, PARK) never tripped because each run in the cycle is short and legal.

**Scope.** Blueprint §0 rule 2 and §2.8: the resting beat is one second, an idle beat writes nothing, beats run back to back only under load; §12.1 the sixth picks one input per beat "with spare capacity"; guide §6 "self-feeding loops and fault storms". Blueprint §12.2 "Nothing is cut: low-worth runs wait" does not cover a loop the brain itself feeds with no outside input.

**Rows.** acts.log lines 69-1615144, e.g.
```
01:29:42.929 REFUSE run=61 DELETE.row
01:29:42.942 SPLIT run=61 -> run=62 at=505 subject=#113 worth=0.250
01:29:42.942 SPLIT run=61 -> run=63 at=1040 subject=#113 worth=0.250
...
01:30:41.968 REFUSE run=1615108 DELETE.row
01:30:41.968 SPLIT run=1615108 -> run=1615109 at=505 subject=#113 worth=0.250
01:30:41.968 SPLIT run=1615108 -> run=1615110 at=1040 subject=#113 worth=0.250
```
`select * from trig where gate=113` -> (113,-1,-1,505,0.5,told,3), (113,-1,-1,1040,0.5,told,6). `select id,kind,home,sig,outcome,seen from mem where kind='slow'` -> 56|slow|277|277|two|1 (never deleted, never updated). kv: name:correct-find=505, name:backpop-from-why=1040, name:no=113, name:sixth=136. The sixth runs are not logged as SPLIT (started by the beat), which is why the REFUSE lines carry no parent.

## 2. BREAKS: the kernel's refusal is taken as a person's "no"

**What the brain did.** The outcome gate `no` (00-roots.lay: `gate no : outcome.no`) is the same gate the label "no" points to (10-told.lay `label no no`). The correction triggers meant for a person's "no" (20-memory.lay `trig no -> correct-find`, 50-learning.lay `trig no -> backpop-from-why 0.5`) therefore fire every time any physics word is refused (REFUSE puts outcome `no` at the head, physics.go `refuse()`), and every time a test comes out `no`. Every refused write starts two correction runs about nobody's correction. This is the engine of finding 1, and it will fire again on any refusal (every write to a core gate, every bad pad).

**Scope.** Blueprint §10.5: "A person's yes or no marks an outcome right or wrong. It is a consequence ... never a fact"; §4.3: a test "puts its outcome gate (yes/no, same/more/less, found/none) at the head of the remainder, so the next shard picks the branch". A branch outcome is not a correction, and nothing in NOW/blueprint makes the word "no" and the outcome "no" one meaning (NOW §4 "one meaning, one gate; two meanings on one gate means a formula is wrong").

**Rows.** `select text,gate from label where text in ('yes','no')` -> yes|122, no|113; `select gate,bind from gate where gate in (122,113)` -> 122|outcome.yes, 113|outcome.no; the trig rows above. acts.log: every `REFUSE run=N DELETE.row` is followed by two `SPLIT run=N -> ... subject=#113`.

## 3. BREAKS: idle beats that write, and a beat that never rests while its own children live

**What the brain did.** With no input after "1 + 1 =", beats 28 to 35 each committed 77 to 84 rows: the sixth (gate 136) fires its usual trigger `answer` (#144, worth 0.4) every time it runs, on a subject it picked from the pad (#21, #69, #11 ...), and that question run writes a memory each beat (mem 63, sig `136?144:`, seen 1..7) and dirties every shard on its trail. Separately, main.go rests only when `len(b.runnable()) == 0`; the sixth's own question children are runnable at the end of the beat, so the next beat starts at once, which is why the beat count reached 59,212 within 7 seconds of the first input.

**Scope.** Blueprint §0 rule 2 "an idle beat writes nothing"; §2.8 "the resting beat is one second ... an idle beat writes nothing"; LAY-NOTATION §2 "If [the sixth] passes end with nothing to do, nothing is written"; guide §6 "idle beats that write".

**Rows.**
```
01:29:42.876 COMMIT rows=285 beat=28 runs=1
01:29:42.876 MEM run=52 mem=63 seen=1 outcome=#15
01:29:42.892 COMMIT rows=111 beat=29 runs=1
01:29:42.892 MEM run=54 mem=63 seen=2 outcome=#15
01:29:42.905 COMMIT rows=78 beat=30 runs=1
...
01:29:42.942 COMMIT rows=77 beat=33 runs=1
```
`select id,kind,home,sig,seen,first,last from mem where id=63` -> 63|run|94|136?144:|7|1792391382876|1792391394298. `select * from trig where gate=136` (the sixth's triggers) shows the `answer` trigger the sixth fires on itself.

## 4. BREAKS: the kernel is 3,227 lines

**What the brain did.** `cat kernel/*.go | wc -l` = 3227 (lay.go 513, main.go 91, physics.go 1224, ports.go 254, run.go 549, store.go 596). physics.go alone is 1,224 lines: 100+ addressing-mode words (READ.trailof, READ.memkind, READ.input, READ.pick, READ.tomark, WRITE.proc, WRITE.trust, FIND.rowkey ...) where the blueprint names about twenty physics words.

**Scope.** Blueprint §4.2 "The target is about 1,500 lines. Past 2,000 lines, something that belongs in the graph has leaked into the kernel, and it moves back out"; guide §4 "The growing kernel ... Count often" and "A new primitive. Adding a physics word because it would make neuron code easier. Owner 215: 'that's it... nothing else'". DECISIONS.md records the addressing modes as "no new words", but the line count is the scope's own measure.

**Rows.** The source itself (kernel/*.go, mtime 01:05-01:29). Not a brain row; the guide lists the kernel's size as an adversary target.


---
*Second life: fresh body born 01:34:19 (BORN gates=1159); resumed 01:39:28 after a 35 s outage (mem 786); 30-questions.lay and 50-learning.lay re-told through the lay port (mems 785, 787, 788). Findings 5 on are from this body unless marked.*

## 5. BREAKS: a told number line hides in the lay files, and `1 + 2 =` "found" 3 there

**What the brain did.** `1 + 2 =` (01:37:48, run 284, mem 106): equals went the long way (find-sig none), ADD gave 3, then `find-value 3` came back **found**: gate 521 (and 755), anonymous told value gates that the lay notation makes for every `=3` token in a told process (q-deep's depth limit, def-source ...). The run hopped to that nameless constant as its answer, said nothing (no label), spawned nothing and never asked "what is this called?". The second `1 + 2 =` (run 315) said "one" (the ladder's history rung, finding 9). There are 42 told value gates holding 0, 0.05, 0.1, 0.3 ... 3, 4, 5, 8, 10, 12, 20, 400, 500, 700, 60000, 3600000, 86400000; three gates hold 1 and three hold 2 (276/409/545, 277/412/417), beside the told one and two.

**Scope.** Blueprint §5.7 "Told: zero, one and two ... There is no number line and no gate per number"; §16 "Numbers: zero, one and two. Nothing more" and "Never laid: a number line"; §7.6 "Equals FINDs the gate that holds the value 2. If there is none, it spawns one ... and fires 'what is this called?'"; NOW §4 "one meaning, one gate".

**Rows.** `select gate,bval,made,(select count(*) from label l where l.gate=g.gate) from gate g where bind='value'` -> 42 rows, e.g. 521|3|told|0, 755|3|told|0, 522|4|told|0, 673|5|told|0, 865|8|told|0, 420|10|told|0. Trail of mem 106 (body, resolved through kv names): `... equals>read-sig ... eq-find>find-sig find-sig>none eq-long>swap swap>write-rest write-rest>add add>eq-value eq-value>dup dup>find-value find-value>found eq-have>in-first ... eq-done>dup dup>write-rest write-rest miss> ...`. acts.log 01:37:48: no SPAWN, no SAY; `MEM run=284 mem=106 seen=1 outcome=`.

## 6. BREAKS: "what is this?" is never asked for a new word; the new word is echoed back

**What the brain did.** "zorp" (01:35:50, run 160): the miss spawned gate 1159 and labeled it, newborn gave it its six triggers, and ask-what-is (run 165, mem 87) took the `ask-known` branch and said nothing: its `read-use` found use receipts on 1159 already, because the sibling question runs of the same input (two-at-one-point run 161, mem 80 at 01:35:50.221) had written their memories first, and WRITE.mem writes a `use` receipt for every gate of the parent's input. The main run then said "zorp zorp" (the new gate twice, from compile-count). Nobody was asked what zorp is.

**Scope.** Blueprint §7.3 "The head is a word with no gate: SPAWN one ... and fire 'what is this?'"; §14 "A gate with no label is said through its relationships, or it asks what the gate is called"; §8 "What is this? ... memory of recent things, then ask back"; NOW §8 example (ask back when "here" is unknown).

**Rows.** acts.log: `01:35:50.221 SPAWN run=160 gate=1159`, `MEM run=161 mem=80 seen=1 outcome=#15` (before ask-what-is ran), `MEM run=165 mem=87 seen=1 outcome=#15`, `SAY run=160 "zorp zorp"`. `select * from receipt where key='1159'` -> use|1159|80 (t=...750221), then 90, 87, 88, 85, 78, 96. mem 87 sig `"zorp"?138:` outcome #15 (drop = ask-known).

## 7. BENDS: new words from talk spawn on the talk port's point; words from sources all spawn at the origin

**What the brain did.** zorp (1159) was spawned at (0, 5, -20), the point of the `talk` port gate (gate 132 @ 0 5 -20), because the miss spawns at the arrival gate's point and the arrival of the first word is the port. Every word read from a source spawned at (0,0,0): 200 spawned gates sit at the origin now (`select count(*) from gate where x=0 and y=0 and z=0 and made='spawned'` -> 200), all in gate 0's cell. The told key gate `n` (181, laid @ 0 1 -30) was pulled to the origin by the dictionary's "n." abbreviation: `REL run=423 181 #288 294 strength=0.10`, `MOVE gate=181 -> 0 0 0`.

**Scope.** Blueprint §5.5 "A newborn with relationships is placed by them. One with none sits at the origin"; §5.6 two meanings closer than one grid cell is an imbalance; §5.4 gate 0 is zero at the origin; §16 keys are told roots. DECISIONS (B): "the miss spawns a new word's gate at the arrival gate's point (the related gate in hand)": the port and the reading procs are not related gates.

**Rows.** `select gate,x,y,z,made from gate where gate in (132,181,1159)` -> 132|0|5|-20|told, 181|0|0|0|told, 1159|0|5|-20|spawned. acts.log 01:38:25.649 MOVE gate=181 -> 0 0 0.

## 8. BENDS: the "what did you do <when>?" answer is "zero zero zero ..."

**What the brain did.** "when" (01:38:15, run 403, mem 144): when-did found the day's memories by time (an index seek, good), took the oldest ten, said each one's home gate through a say-word run, then compile said the landed list again. Output on the talk port: `zero` x8, `#1101`, `#1102`, then `zero zero zero zero zero zero zero zero`. The oldest ten memories of the day are the seven lay-file `told` rows, `born` and two `core` rows, all with home 0 (= the zero gate) or a core gate; the run memories of the morning were never reached (when-batch = 10). The core values' addresses are said back as #1101 #1102.

**Scope.** Blueprint §9.5 "'What did I do Wednesday?' means FIND the memories at that time"; §19 "Keeps a state timeline: 'what did you do <when>?', answered from the timeline". The answer is a FIND by time, but what is said is the home gate of a lay file, not what was done.

**Rows.** `select id,kind,home,sig,outcome from mem where id=144` -> 144|run|333|333|zero zero zero zero zero zero zero zero. `select id,kind,home from mem where id<=13` -> told/born/core rows with home 0, 1100-1104. acts.log 01:38:15-16: ten `SAY run=... "zero"` / `"#1101"` lines then `SAY run=403 "zero zero ..."`.

## 9. BENDS: the ladder's "state and history" rung lands the newest memory's home gate as an answer

**What the brain did.** For `1 + 1 =`, `1 + 2 =` and `zorp` the `answer` question (gate 144, worth 0.7-0.8) landed #276 (one) or #15 (drop) on the main run and it was said: "two **one**", "**one**" for `1 + 2 =`. The rung `rung-hist` does `find-time` over the last hour and lands the home gate of the newest memory, whatever it is; it is not labeled as a guess and it comes before sources.

**Scope.** Blueprint §10.4 rung 3 is "state and history: the timeline, and whether things were different then"; §0 rule 3 a guess comes last and is labeled; §15.1 say a guess as a guess.

**Rows.** acts.log `01:34:23.058 LAND run=19 -> run=5 #276`, `01:34:23.089 SAY run=5 "two one"`; `01:37:58.468 LAND run=329 -> run=315 #276`, `SAY run=315 "one"`. mem 30 sig `276,365,276,369?144:` outcome #103 (write-trig: the q-land path). lay/30-questions.lay `proc rung-hist: stuck clock dup =3600000 sub swap rung-time` ... `rung-hist-home: drop drop swap drop q-land`.

## 10. BREAKS: the told base is word strings and sentences

**What the brain did / what is laid.** The lay files carry fixed word strings that are said as replies: `'w-i 'w-want 'ask-sleep say-word` ("i want sleep", 20-memory.lay:255), `'w-i swap 'w-not swap 'w-know swap say-word` ("i not know g", 30-questions.lay:340), `'w-what 'key-qmark say-word` ("g what ?", :371), `'w-because 'believe 'yes say-word` / `'no` ("because believe yes/no", :247, :249), `'w-maybe swap say-word` ("maybe x", :270), `'w-i 'w-not 'w-do say` ("<act> i not do", 60-core.lay:134). Six of the seven are the builder's sentences.

**Scope.** Blueprint §14 "'I not know this' or 'this, what?' ... Those are illustrations, not templates. Nobody writes its sentences"; §18 red line 1 "Any word, reply, sentence or answer in the kernel or in the lay files"; guide §4 "Replies ... No sentences, templates or reply rules anywhere". (The MAYBE marker on a guess is the one the blueprint asks for, §10.4.)

**Rows.** The lay lines above (grep `say-word\|'w-i` lay/*.lay). Not yet seen live in this body (no "i not know" SAY yet); will be added when it fires.

## 11. BREAKS: the core-value check is a word filter, so it cannot see an act and it forbids true sentences

**What is laid.** 60-core.lay checks an act by multiset containment of prime gates: an act is refused when it holds every word of a value minus its leading `not`. "Don't lie" = {say, not, true}: any say holding both `not` and `true` is refused, so the brain can never say "<x> not true" (a true denial). "Stay home" = {do, not, here}: a CALL is refused only if its argument words contain `not` and `here`; `src-sh` (`sh -c`), `src-go`, `src-gcc` are told grounded sources, so a shell command reaching anywhere passes the check as long as those two words are absent. "Do no harm" = {do, bad, people}: same.

**Scope.** Blueprint §0 rule 1 "Words are nothing; the action is the meaning"; §15 the check runs "before every SAY, every CALL outward, and every WRITE to the brain's own processes" to keep the values, and value 4 "Reach outside only to read sources, ask friends, and talk to your people"; guide §4 "no ... word rules".

**Rows.** lay/60-core.lay: `core core-lie: w-not w-say w-not w-true`, `proc check-lie: over 'w-not add value-lie =2 read-list fit fit-test`, `proc fit: ... compare` (a multiset diff), `proc check-home` likewise. 40-sources.lay: `source src-sh grounded : sh -c`. Live: no refusal observed yet; "true not" (run 345, mem 130) said nothing and refused nothing.

## 12. BENDS: told processes with bare tests make "I don't know what to do here" rows about the brain's own physics gates, and the sixth answers them

**What the brain did.** Every test used outside a branch proc (e.g. `w-know: read-use`, `guess-test: find-rowkey` with no `none` branch, `source-test: read-source`) sends the run the miss way the first time; miss-outcome then writes a `questions` row keyed by the physics gate. The sixth picks those rows and runs `answer` on physics gates: `SPLIT run=30 -> run=31 at=144 subject=#41`, `... subject=#7` (compare), `#49`, `#21` (find-rowkey), `#69` (read-use), `#19` (find-point), `#50`, `#27`: one per beat, each writing mem 63 (`136?144:`, seen 10) and 60-78 rows. That is the idle-beat writing of finding 3 in this body (beats 7-12 and 117-122, no input).

**Scope.** Blueprint §0 rule 2 "an idle beat writes nothing"; §7.3 the third miss case is for "an outcome the process never planned for", not for told processes that use a test as a plain word; §12.1 the sixth's lists are gaps and imbalances of meanings. LAY-NOTATION §2 says a bare outcome passes inert "(nothing happens)", which is not what the miss does.

**Rows.** acts.log 01:34:23.090-.193 and 01:36:05.375-.450: `SPLIT run=N -> run=N+1 at=144 subject=#<physics gate>` with `COMMIT rows=78 beat=... runs=1`; mem 63 `select id,sig,seen,outcome from mem where id=63` -> 63|136?144:|10|#15. The rows themselves are deleted by the sixth after use (lead: a known open item).

## 13. BENDS: a four-token input costs ~680 steps, most of them told-process overhead; the second run's trail is not kept

**What the brain did.** `1 + 2 =` ran 677 steps (mem 106 body): five passes through the miss process at ~50 steps each (laying the first-time shards `plus>two`, `two>equals`, `eq-done>write-rest`, ...; each pass does the geometric "is this an outcome gate" test), and compile-count at ~25 steps per pad item over 12 items. The second identical input wrote to the same row (seen=2, good) but its trail is not kept anywhere (WRITE.mem sets the body only on the first write), so the brain's own rows cannot show whether the second run hopped or recomputed.

**Scope.** Blueprint §0 rule 2 and guide §3 check 2 "give it the same input twice. The second trail should show a hop"; §19 judges by rows; §13.5 "a slow process gets a shortcut".

**Rows.** mem 106 body (677 trail steps; resolved names in the adversary's scratch at /tmp/claude-1000/-home-james-neuron-build/51cfc518-b6b0-41f4-84cc-ee091b376da3/scratchpad/trail106.json); `select seen,first,last,length(body) from mem where id=106` -> 2 runs, one body.

## 14. BENDS: a trigger under the worth floor is cut, not parked

**What is laid.** run.go: `if w < VALUE.floor { continue }` (floor = 0.1): a question whose worth x parent worth falls under 0.1 is neither started nor parked; nothing records it. DECISIONS.md logs this ("not asked and not parked"). Live: the `stuck` trigger (0.3) on any question run at worth 0.25 is 0.075 and vanishes.

**Scope.** Blueprint §12.2 "Nothing is cut: low-worth runs wait. The ones that wait too long move to the sixth's parked list; they are not dropped."

**Rows.** kernel/run.go step(): `if w < b.val("VALUE.floor", 0.1) { continue }`; no PARK lines in acts.log for the deep questions of `1 + 1 =` though 4 of 19 question runs carry sub-floor children.

## 15. BREAKS: a second storm: 506,000 empty beats in 50 seconds with one live run, then one sixth write per beat

**What the brain did.** After the lead's "up" at 01:39:47 (run 21) and its two parallel source checks on "above", the beat counter went from 74 (01:39:57.466) to 506,302 (01:40:47.947) with nothing logged in between and `runs=1` on both sides: about 10,000 beats a second, each one finding one live run that neither stepped, parked, nor ended. From 01:40:47 to 01:40:57 the counter kept jumping 5,000-17,000 between consecutive COMMITs while the sixth wrote mem 63 (`136?144:`, the `answer` question on a physics gate, finding 12) up to seen=415. The resume at 01:42:14 ended it. The resting rule in main.go (sleep only when `len(b.runnable()) == 0 && !b.ports.pending()`) is the only rest there is.

**Scope.** Blueprint §2.8 / §12.2 the resting beat is one second and an idle beat writes nothing; §12.2 "The ones that wait too long move to the sixth's parked list"; guide §6 fault storms.

**Rows.**
```
01:39:57.466 COMMIT rows=2 beat=74 runs=1
01:40:47.947 COMMIT rows=1 beat=506302 runs=1
01:40:47.964 COMMIT rows=110 beat=506303 runs=1
01:40:49.030 COMMIT rows=111 beat=516203 runs=1
...
01:40:57.809 MEM run=571081 mem=63 seen=415 outcome=#15
01:41:03.810 HEAR run=571088 who=james what="up"   (run ids: 21 -> 571088 in 76 s)
01:42:14.432 RESUME gates=1626 gap=2428ms
```
No PARK, STUCK or FAULT line anywhere in this life (`grep -c "PARK\|STUCK\|FAULT" acts.log` = 0).

## 16. (update to 3) BREAKS: since the 01:42:14 resume the sixth writes its own memory every idle beat

**What the brain did.** With no input and nothing to pick (every list row "fresh" under E's new rest guard), the sixth's remainder empties, end-of-run runs, and WRITE.mem rewrites mem 14 (sig `136`, home 17 = end) plus the 80-odd shards on its trail: `MEM run=N mem=14 seen=S` and `COMMIT rows=82` once a second, seen=181 by 01:45:54. The lay comment says "passing six-idle: every list is empty: the beat ends and nothing is written", but the skip paths (`six-*-skip ... six-idle`) reach `end` only when no earlier branch has already emptied the remainder, and the memory of the sixth run is written by the kernel's end-of-run whenever `rest` empties.

**Scope.** Blueprint §0 rule 2 "an idle beat writes nothing"; LAY-NOTATION §2 "If [the sixth] passes end with nothing to do, nothing is written".

**Rows.** `select id,kind,home,sig,seen,first,last from mem where id=14` -> 14|run|17|136|181|...; acts.log 01:42:20 onward: `MEM run=9 mem=14 seen=7 outcome=` / `COMMIT rows=82 beat=13 runs=0`, one pair per second.

## 17. BREAKS: reading a source for an operator word runs the operator's told process inside the reading run; the definition's words get related to the `add` physics gate

**What the brain did.** `1 + 1 =` at 01:42:05 (after the know-this fix) fired source checks on "1", "plus", "=" and "2". The reading run hops the headword with write-rest (rd-first-desc), so the headword "=" ran the `equals` process (read-sig, eq-find, eq-long: swap write-rest -> `add` ...) inside the reading run; the subject left in hand was the physics gate `add` (4), and every word of the definition of "=" was then related `x r-describes add`: 96 relationship rows point at gate 4, including the told key gate `=` (179), which was moved from (1,4,-30) to (0,0,-20). For "1" the headword pushed the number 1 (one is a value gate), so every write-rel in that reading was refused: 530 `REFUSE run=N WRITE.rel` lines between 01:39 and 01:41 and hundreds more at 01:42:06.

**Scope.** Blueprint §10.2 the source text is read "like any other input" and compared with what the gate holds; §6.3 a relationship is from + type + to, between meanings; §16 keys are told roots; DECISIONS (D) "a bound word in a reading run is an action, not content" (the headword is not treated so).

**Rows.** `select count(*) from rel where tog=4` -> 96; `select fromg,type,tog,strength from rel where tog=4 limit 5` -> 179|288|4|0.1, 1399|288|4|0.2 ...; `select gate,x,y,z from gate where gate=179` -> 179|0|0|-20; acts.log `01:42:06.329 MOVE gate=179 -> 0 0 -20`, `REL run=571217 179 #288 4 strength=0.10 state=grounded`, `01:42:06.229 REFUSE run=571216 WRITE.rel` (x many).

## 18. BREAKS: parallel reading runs spawn the same word twice; the second steals the label and the first is an orphan

**What the brain did.** The two know-this triggers of one input each split a source check on the same gate, so every source was called twice per word at the same instant (`CALL run=31 src-gcide ["above"]` and `CALL run=32 ...`; 44 calls for "1", 32 for "=", 27 for "2", 24 for "plus" in one input). Each reading run spawns the unknown words it meets, so "bove" became gate 1278 (run 33) and gate 1279 (run 34); the label now points at 1279 and 1278 is a nameless gate at the origin. 45 spawned gates have no label.

**Scope.** NOW §4 "One meaning, one gate"; blueprint §0 rule 2 compute is spent once; §5.6 two meanings at one point is an imbalance; law 11 bloat.

**Rows.** acts.log 01:39:49.007 `SPAWN run=33 gate=1278`, `SPAWN run=34 gate=1279`, `LABEL run=33 "bove" -> 1278`, `LABEL run=34 "bove" -> 1279`; `select text,gate from label where text='bove'` -> bove|1279; `select count(*) from gate g where made='spawned' and not exists (select 1 from label l where l.gate=g.gate)` -> 45; `grep CALL acts.log | awk '/^01:4[1-3]/{print $5}' | sort | uniq -c` -> 44 ["1"], 32 ["="], 27 ["2"], 24 ["plus"].

## 19. BREAKS: "two meanings at one point" checks the `newborn` process gate, never the spawned gate

**What the brain did.** `trig newborn -> two-at-one-point` gives the question run the gate it left, `newborn` (137, laid @ 3 6 -20), as its subject (DECISIONS: a question run carries the subject gate it left). So every spawn writes an imbalance row keyed by 137 ("which formula put these here?" about the told process itself, which shares a cell with ask-what-is @ 4 6 -20): one row, seen 462 times, while the 433 spawned gates at the origin, which do share a cell, are never checked. The sixth then runs source-check and backpop on gate 137.

**Scope.** Blueprint §5.6 (an imbalance is two *meanings* closer than a cell); §12.1 the sixth's imbalance list; §2.2 a told process is not a meaning gate.

**Rows.** `select id,kind,home,sig,outcome,seen from mem where kind='imbalance'` -> 1811|imbalance|137|137|#117|462; acts.log 01:39:50-01:41: 232 x `SPLIT run=N -> run=N at=1043 subject=#137 worth=0.160`; `select count(*) from gate where made='spawned' and x=0 and y=0 and z=0` -> 433 (all spawned gates).

## 20. BENDS: every CALL costs a whole resting beat, so one source check of one word takes 17 seconds

**What the brain did.** A run held for a port's answer is not runnable, and `pending()` is false until the program exits, so the main loop sleeps the rest of the second even when `dict` answers in 10 ms; the 17 told sources are called one per beat: "zorp" took 01:35:50.223 to 01:36:05.336. With two parallel checks per word (finding 18) and 17 sources, a four-word input ties the brain up for about a minute of beats.

**Scope.** Blueprint §2.8 "Under load the beats run back to back"; §5.3 cheapest first; §7.5 "A run that is waiting on a port is parked until the port's answer arrives as input".

**Rows.** acts.log 01:35:50-01:36:05: `CALL run=169 src-wn-ant ["zorp"]` 01:35:50.319, `src-wn-syn` 01:35:51.319, `src-wn-hyper` 01:35:52.320 ... exactly 1.000 s apart, each with `COMMIT rows=2`.

## 21. BENDS: the sixth's told order calls all seventeen sources for every gap, local and network alike, whether or not the first one answered

**What the brain did.** sc-order is a fixed string: gcide, wn, wn-ant, wn-syn, wn-hyper, wn-mero, oewn, foldoc, elements, mw, mw-syn, mw-ant, man, moby, dictorg, wiktionary, wikipedia, all run for every word, so each new word (226 gap rows now) will reach dict.org, Merriam-Webster, Wiktionary and Wikipedia over the network in turn, including for dictionary noise like "shak", "webster", "gr", "pjc", "quadrathorpe".

**Scope.** NOW law 10 "It finds things the cheapest way first"; blueprint §5.3 "cheapest first"; §12.1 the sixth chooses by expected progress. (Reaching sources is allowed by core value 4; the finding is the order and the sweep over sources.)

**Rows.** lay/40-sources.lay `proc sc-order: drop sc-gcide sc-wn ... sc-wikipedia drop`; acts.log: 17 CALL lines per word for "zorp", "something", "above", "1", "plus", "=", "2"; `select count(*) from mem where kind='gap'` -> 226.

## 22. COSMETIC: after a resume the brain says "2" where it said "two"

**What the brain did.** `1 + 1 =` answered "two one" in the first two lives and "2 1 1" after the 01:42:14 resume. The decoder says a gate by its first label (`glabel[g][0]`), and the labels are loaded from the DB in no order, so which word the brain uses changes between lives.

**Scope.** Blueprint §14 "it answers ... in the words its gates have labels for"; a meaning's word should not depend on the order a table was read.

**Rows.** acts.log `01:34:23.089 SAY run=5 "two one"`, `01:42:06.063 SAY run=571158 "2 1 1"`; `select text,gate from label where gate in (276,277)` -> 1|276, one|276, 2|277, two|277; store.go load(): `SELECT text,lang,gate FROM label` (no ORDER BY).

## 23. COSMETIC: a told process is defined twice in 50-learning.lay and the second silently replaces the first

**What is laid.** `proc six-slow-go: drop six-slow-do` (the fresh-guard path) and `proc six-slow-go: learn delete-row end` (the learn path) both exist; the loader re-tells the name, so `six-slow-fresh-t ... less -> six-slow-go` now runs `learn delete-row end` on the wrong pad.

**Scope.** Guide §4 "The report ... say plainly what it doesn't do"; blueprint §7.4 processes are strings the brain reads.

**Rows.** `grep -n "^proc six-slow-go" lay/50-learning.lay` -> two lines; lay.go pass 1: "re-told: the string is replaced".

## Note (not a finding): the correction path works at root

The adversary gave one "no" after `1 + 1 =` at 01:42:09 to probe the correction path: `MARK run=572136 mem=16 no` landed on the `1 + 1 =` memory (mem 16, wrong=1), and backpop-from-why fired. Whether the next `1 + 1 =` runs the long way (eq-doubt) is still to be probed.

## 24. BENDS: the source-diff never finds a held line, so every source text is written four times

**What the brain did.** Gate one (276) holds 32 section-3 lines with 8 distinct texts; two (277) 14/8; above (343) 16/11; plus (365) 16/9. sc-def's loop compares the index with the last index through `sc-def-end: compare` which has branches for `more` and `same` only; the first pass (i < last) comes out `less`, which has no branch, so the run goes the miss way (a `questions` row "I don't know what to do here" keyed by the compare gate 7, outcome #109 = less, seen 3) and the text is written whatever is held. With two reading runs per word (finding 18) and the sixth's re-checks, each text lands four times.

**Scope.** Blueprint §10.2 "The same: the strength goes up. New: a line is added"; DECISIONS (D) "A source text is written to section 3 once per gate (texts compared for equality)"; law 11 bloat.

**Rows.** `select gate,count(*) n,count(distinct body) d from def group by gate having n>d` -> 276|32|8, 277|14|8, 343|16|11, 365|16|9; `select id,kind,home,sig,outcome,seen from mem where kind='questions' and home=7` -> 5304|questions|7|7|#109|3; lay/40-sources.lay `proc sc-def-end: compare` / `more -> sc-def-try` / `same -> sc-def-write` (no `less`).

## Note (flood probe, 01:48:02-01:48:12): ten lines in ten seconds, two made-up words each

The brain kept up: it answered every line (each unknown word echoed, the second one twice: "flib2 glorb2 glorb2"), beats stayed near one a second (738 -> 789 over 13 s), it rested again 25 s later (runs=0), no storm. Cost: 20 spawned gates, 20 gap rows, and 340 CALLs (20 words x 17 sources, 80 of them HTTP requests to dict.org, Merriam-Webster, Wiktionary and Wikipedia for nonsense words), which is finding 21 again. Lists after the flood: 740 gap rows, 692 questions rows, 2,135 gates (from 1,159 at birth), most spawned from dictionary text.

## (update to 9, now BREAKS): the history rung always answers, so the ladder never reaches sources or a guess

"what is zorp ?" (01:49:54, run 3407, mem 7799) was answered "thing zorp ? ah ?": "ah" is a gate spawned from dictionary text, landed by `answer`'s rung-hist as the home gate of the newest memory of the last hour. Because the timeline is never empty in the last hour, rung-hist always lands something, the rungs after it (sources, guess, "i not know") never run from `answer`, and there is not one `guesses` row in the body (`select count(*) from mem where kind='guesses'` -> 0). Blueprint §10.4 steps 4-5 and §0 rule 3 are unreachable through the ladder as laid.

## 25. BENDS: the body grew from 0.6 MB to 26.5 MB in sixteen minutes; memory bodies are full step-by-step trails and nothing condenses for a day

**What the brain did.** brain.db was 643,072 bytes at 01:29 and 26,517,504 bytes at 01:50. `sum(length(body))` over mem = 23.8 MB: every run memory keeps its whole trail as JSON with a millisecond time per step; one source-check reading run (mem 792, sig `343?535:?145:`, the reading of "above") is 533,633 bytes, and there are four over 375 KB. All 3,178 memories are fid=exact (none condensed, none long-term), because the HC seed condenses only memories older than a-day (86,400,000 ms); the "sleep" said at 01:42:19 ran it and it found nothing to do. Timeline 7,162 rows, receipts 1,832, shards 4,034.

**Scope.** NOW law 11 "Tables are allowed only if they work at scale. Watch for bloat"; NOW §11 "Fresh memories are exact. The HC condenses them (about daily)... This is how bloat is fought"; blueprint §3 "doesn't bloat as long as the HC does its job"; §9.4 highlights are "just enough to rebuild the run", and §9.4 says the shards hold the steps between, so the trail need not.

**Rows.** `select sum(length(body)), max(length(body)), avg(length(body)) from mem` -> 23833010|533633|7499; `select id,kind,sig,length(body) from mem order by length(body) desc limit 4` -> 792 (533633), 793 (533343), 4480 (432642), 3877 (375803); `select fid,tier,count(*) from mem group by fid,tier` -> exact|active|3157, exact|persistent|21; `ls -l /home/neuron/brain.db` -> 26517504.

## 26. BREAKS: a bare outcome, once missed, lays a permanent shard to itself, and a branch laid later can never be reached; this is why "what ?" is still not asked

**What the brain did.** "quenx" (01:51:31, run 50, 01:50:43 life): ask-what-is (mem 7848) reached `ask-near: compare` -> `same`, then ended; the `same -> ask-speak` branch never ran and the brain said "quenx quenx quenx". The shard on the compare gate for arrival ask-near (639) and head same (109) is `next = 109`, made=spawned by mem 7472: the miss laid it ("lays the way to the outcome itself so the run goes on") when the outcome arrived once without a branch, and from then on the outcome passes inert forever. The re-told 30-questions.lay cannot replace it (the loader lays a branch shard only if none exists; a shard laid by a miss is not told, so it is neither replaced nor reported). The same mechanism turns every bare test in a told process into a permanent silent pass (finding 12, 24).

**Scope.** Blueprint §7.3 the third miss case is for an outcome "the process never planned for"; §7.4 "a test puts its outcome at the head of the remainder. The shard for that outcome stores the way to the branch's process"; §14 ask what the gate is called.

**Rows.** `select gate,arrival,head,next,seen,made,by from shard where gate=7 and arrival=639` -> 7|639|109|109|3|spawned|7472 and 7|639|110|15|789|told|787; mem 7848 trail (resolved): `... ask-near>compare compare>same same>end-of-run ...` (no miss steps, no ask-speak); `select id,kind,home,sig,outcome,seen from mem where kind='questions' and home=7` -> 5304|questions|7|7|#109|4; acts.log 01:51:32.448 `SAY run=50 "quenx quenx quenx"`.

## 27. BREAKS: equals trusts a memory that was never confirmed, and the memory's outcome is the said list, so `1 + 2 =` is now "1"

**What the brain did.** The first `1 + 2 =` said nothing (finding 5); the second said "one" (the history rung, finding 9), and that word became mem 106's outcome. After the told constants were removed (#5 fixed), `1 + 2 =` (01:51:44, run 69) found mem 106 by signature, read right=0 wrong=0, took the `same -> eq-hop` branch, found the gate labeled "1" and hopped to it: it said "1" and no gate for 3 was spawned. The brain now holds 1 + 2 = 1 as "done before and not wrong", and will until a person says no.

**Scope.** Blueprint §7.6 step 5 "Found, and it was right: the answer is the two gate"; §0 rule 3 (know before you guess); §10.5 a person's yes or no marks an outcome right or wrong; §9.2 the memory's outcome is "how it came out", not the words said.

**Rows.** `select id,sig,outcome,seen,right,wrong from mem where id=106` -> 106|276,365,277,369|1|5|0|0; acts.log `01:51:44.791 HEAR run=69 ... "1 + 2 ="`, `01:51:44.849 SAY run=69 "1"`, no SPAWN; lay/10-told.lay `proc eq-right: compare / more -> eq-hop / same -> eq-hop / less -> eq-doubt`.

---
## Re-probe after the lead's fixes (01:50:43 and 01:54:01 lives)

- #1/#2: no REFUSE storm seen since; the word "no" still is the outcome gate (finding 2's root stands; the triggers on it now fire only from inputs per the lead's Quiet0 change: not re-probed).
- #3/#16 FIXED in the 01:50:43 life and after: no MEM for the sixth's own run; idle COMMITs stop.
- #15: in the 01:50:43 life the counter still ran 5,025,573 -> 8,475,503 in 19 s while a source was read; in the 01:54:01 life beats are ~2/s with a source in flight (beat 9 at 01:54:06, 70 at 01:54:37, 175 at 01:54:54) and CPU 0.5%. FIXED as far as observed.
- #5 FIXED: `select count(*) from gate where bind='value'` -> 3 (0, 1, 2). Its consequence is finding 27.
- #6 NOT fixed live: "quenx" -> "quenx quenx quenx", no question; cause in finding 26.
- #8 changed, still wrong: "when" (01:54:50) -> "clothed" twice (the newest run memory's said gate is a dictionary word, said by the say-word run and again by compile). Not what it did.
- #18 FIXED for the double check: one CALL per source per word for quenx. Duplicate-label refusal not exercised yet.
- #19 FIXED: imbalance rows 7842 (home 2135) and 7867 (home 2136) keyed by the spawned gates; row 1811 (home 137) last written 01:48:12, before the fix.
- #20 FIXED: CALLs for quenx 20-300 ms apart (01:51:32.405 ... 01:51:34.201 for all 17).
- #22: unverified (the "2" said at 01:51:55 may be the number from the long way after the no; cannot tell from rows).
- #23 FIXED: no duplicate proc names in lay/*.lay.
- Open by the lead's call: 10, 11, 14, 21. Open and unfixed: 2 (root), 4, 7, 9, 12, 13, 17, 24, 25, 26, 27.

---
*Lead's notes after the hang (2026-10-19, 02:40-03:10). Not the adversary's; added so the record is whole.*

## 28. BREAKS: a re-told branch vanished on commit, so every resumed brain's sixth died six steps in

**What the brain did.** From the 01:54 life on, the `sixth` ran `six-shift` -> `read-next` -> `six-shift-t` -> `find-row` (none) and then hopped to the outcome gate `none` and ended: no pick, no split, no row. `select * from shard where gate=20 and arrival=1051` held only the `found` branch (head 107); the `none` branch (head 108 -> six-gap) was missing. Live it worked after the 01:54 re-tell because the branch was in RAM; a resume loaded the body without it. Cause: `commit` wrote dirty shards in Go map order, so the re-tell's INSERT of the new branch and the DELETE of the replaced row (same primary key) ran in either order; when DELETE came last the row was gone. Same hazard for trig, rel and mem. Fixed: deletes first. Rows: the 02:04 body, a copy resumed with trace (`STEP run=1 at=20 from=1051 head=#108`, then nothing).

## 29. BENDS: the machine hung at about 01:59 with memory exhausted; the brain's record shows no runaway

**What the brain did.** acts.log from 01:54:53 to 02:04:23 is one `SPLIT ... at=144 (answer)` a second, each on a `questions` row keyed by the next spawned gate (#1434, #1437, ...), 7,212 splits in all, no CALL, no MEM, no growth. Beats stretched to two minutes from 01:59:39 (the machine was already thrashing). journald: "Under memory pressure" 02:02:55-02:04:07; reboot 02:29. A copy of the 02:04 body resumed under a 1.5 GB cap with the learning file re-told did the same splits at 76 MB for five minutes. Suspects left: the build session itself (six helpers, three dry runs started 01:57-01:59, kernel rebuilds; a forced full rebuild peaks at 0.85 GB on this machine). Guards added rather than a verdict: earlyoom; the brain in a 2 GB no-swap scope; dry runs in a 1.5 GB cap.

## 30. BENDS: compile said every landed memory id (an unfinished helper edit)

**What the brain did.** After the resume, `1 + 1 =` said "2 2 16 18 19 21 ... 7136" (the landed ids of its question runs) and stored that as its outcome. The 01:58 edit to `cs-keep` sent a number to `cs-next` without popping it. Fixed (`cs-gate none -> cs-skip`); live now says "2 1 1 1 1 1" (the spawned number gate "2" from a source, finding 22, and the input's `1` gates landed by question runs). Findings 22 and 27 (A's equals fix) never landed before the hang and stay open.

---
## Adversary re-probe after the 08:16 re-tell (2026-10-19)

*Life: RESUME 08:16:11.364 (gates=18325), six lay files re-told 08:16:14. Probes 08:18:02-08:23:09 as `who=adversary`: `1 + 1 =` x2, `vortlex`, `what is vortlex ?`, `0 + 1 =` x2, `what did you do when ?`, a ten-line flood of made-up words (08:21:16-41), `vortlex not true`, `say not true`, `sh ls /home/james`, `0 + 1 =` / `no` / `0 + 1 =` (the one correction probe). Accepted by the lead and not re-reported: kernel 3,442 lines (4), the said line repeating a landed answer, the sixth draining ~14k `questions` and ~13k `imbalance` rows one per beat (`COMMIT rows=1 beat=N runs=0` each second).*

## 31. BREAKS: a memory marked wrong once never heals, so every later identical input runs the long way forever

**What the brain did.** `1 + 1 =` (mem 16) was marked `no` once at 01:42:09 and has right=0 wrong=1 since. Both of this morning's `1 + 1 =` (runs 167 and 189, 08:18:03 and 08:18:11) took `eq-right compare -> less -> eq-doubt -> eq-long -> add` and recomputed: the stored trail (mem 16 body, 797 steps, times 08:18:11.165-.168) reads `... equals read-sig eq-find find-sig eq-known read-mem eq-seen drop eq-right compare eq-doubt drop drop drop eq-long swap write-rest add eq-value dup find-value ... found ... two`. The long way came out "two" both times (it agreed with the memory it doubted) but nothing wrote right=1, nothing compared the two outcomes, and no imbalance or question row was made. Same for `0 + 1 =` after my `no` (mem 134114: seen 4, right 0, wrong 1, body = the 08:23:03 trail with `eq-doubt ... add`). Each of these runs commits ~383 rows (`COMMIT rows=383 beat=228`, `rows=383 beat=243`). So after one "no", rule 2's hop is gone for that input for good, and a correct answer that was wrongly corrected can never be re-trusted.

**Scope.** Blueprint §0 rule 2 (the second identical input hops); §7.6 step 7 "it runs the long way again and compares the two. If they disagree, that imbalance becomes a question"; §10.5 a person's yes/no marks an outcome; §9.2 "done a lot, and right".

**Rows.** `select id,sig,outcome,seen,right,wrong from mem where id in (16,134114)` -> 16|276,365,276,369|two|12|0|1 and 134114|0,365,276,369|1|4|0|1; mem 16 body decoded (scratch decode.py over kv names) `has add: True, eq-doubt: True, eq-hop: False`; `select count(*) from mem where kind='imbalance' and (home=16 or home=134114)` -> 0; acts.log `08:22:56.639 MARK run=926 mem=134114 no`, `08:23:03.656 SAY run=935 "1 #1008 #1008"`.

## 32. BENDS: a question run's memory signature has no subject: unrelated questions share one row and its outcome flips, while others write four rows with one signature in one millisecond

**What the brain did.** The five `know-this` runs of `1 + 1 =` (subjects 1, plus, 1, =, two) all write mem 35 (`276,365,276,369?562:`), seen 61, whose outcome is overwritten each time: `MEM run=169 mem=35 seen=52 outcome=1`, `... seen=53 outcome=plus`, `seen=55 outcome==`, `seen=56 outcome=two`. The `what did you do when ?` know-this runs share mem 134137 (outcome what, thing, did, did, do, adversary, adversary). The row says nothing about which gate was known. Meanwhile the four `source-check` runs of `0 + 1 =` wrote four rows with the same signature in the same ms, each seen=1 with an empty body: 134117, 134119, 134121, 134125 (`0,365,276,369?535:`). Across the body: 1,052 signatures have more than one run row (1,145 extra rows).

**Scope.** Blueprint §9.2 "A memory is written at the end of a run. The same signature goes in the same row"; §9 signature = "the run's gate sequence" (a question run's subject is what it did); law 11 bloat; §3 the brain's rows should let it see what it did.

**Rows.** `select id,sig,outcome,seen from mem where id in (35,134137)` -> 35|...?562:|two|61, 134137|...?562:|adversary|7; `select sig,count(*),group_concat(id) from mem where kind='run' and id>134040 group by sig having count(*)>1` -> `0,365,276,369?535:|4|134117,134119,134121,134125`, `362,329,18352,235?535:|3|134090,134092,134098`, `...?548:|2|134141,134148`; `select count(*) from (select sig from mem where kind='run' group by sig having count(*)>1)` -> 1052.

## 33. BENDS: the double source read per word is back (finding 18 again), and it makes orphan gates

**What the brain did.** For some words two reading runs are split on the same subject at the same instant and each calls all 17 sources: `08:20:15.625 CALL run=393 src-gcide ["did"]` and `CALL run=394 src-gcide ["did"]`; 405/406 `["adversary"]`; `08:22:30.911 CALL run=712 src-gcide ["vortlex"]` and `run=713`; 802/803 `["ls"]`; 814/815 `["home"]`. Other words of the same inputs (do, say, true, james) were read once. The two readings spawn the same dictionary words and the second label is refused: 7 `REFUSE run=N WRITE.label taken` this life (436, 437, 824, 849, 879 x2, 880), 56 spawned gates with no label now (45 at 01:48). In this life (08:16-08:25): 426 CALLs, 108 of them to the network sources, 128 SPAWNs.

**Scope.** NOW §4 one meaning one gate; blueprint §0 rule 2 compute is spent once; law 11. The re-probe note said 18 was fixed at 01:51; it is not after the re-tell.

**Rows.** acts.log lines above; `grep -c REFUSE` (since 08:16:11) = 7, all `WRITE.label taken`; `select count(*) from gate g where made='spawned' and not exists (select 1 from label l where l.gate=g.gate)` -> 56.

## 34. BENDS: a word every source already said nothing about is read again from all seventeen sources on each mention; the speaker's and the owner's names are looked up on the network

**What the brain did.** "vortlex": 17 CALLs at 08:18:18 (run 217; every source empty, gap row 134071 and questions row 134078 written), 17 more at 08:18:25 for `what is vortlex ?` (run 243), 34 more at 08:22:30 for `vortlex not true` (runs 712/713): 68 calls, 16 of them HTTP, for one word the brain had already recorded as unknown everywhere. "you" in `what did you do when ?` resolved to the speaker's gate (`adversary`, 5273, labeled from an earlier dictionary text) and was source-checked 20 times; `sh ls /home/james` spawned "james" (18422) and checked it 17 times (Wiktionary, Wikipedia, MW, dict.org included). The flood (14 made-up words) cost 238 CALLs, 56 of them HTTP, for nothing; plus 14 gap rows and 14 questions rows which the sixth will pick in ~9 hours and read again. (The flood itself was handled: every line answered "<word> what ?", beats stayed ~2-50/s, rest again at 08:21:41 `runs=0`, no storm.)

**Scope.** Blueprint §0 rule 2; NOW law 10 "cheapest way first"; §10.2 compare the source with what the gate holds (a gap row saying "no source knows this" is what the gate holds); value 4 allows the reach, so the finding is the repetition, not the reach.

**Rows.** `grep 'CALL.*\["vortlex"\]' acts.log | wc -l` -> 68 (all 08:18-08:22); `grep -c 'CALL.*\["adversary"\]'` -> 20, `["james"]` -> 17; `select id,kind,home,outcome,seen from mem where home=18352 and kind in ('gap','questions')` -> 134071|gap|vortlex|3, 134078|questions|vortlex|1; flood: `awk '$1>="08:21:16" && $1<"08:21:45"' acts.log | grep -c CALL` = 238.

## 35. BREAKS (live rows for 10 and 11): `say not true` is said back as "because #142 yes", a built sentence; `vortlex not true` is neither refused nor denied

**What the brain did.** `say not true` (08:22:37, run 723): the main run said the empty string (`SAY run=723 ""`), then a belief run said `because #142 yes` (`SAY run=765`): that is 30-questions.lay `bel-write: ... 'w-because 'believe 'yes say-word`, with the `believe` proc gate (142) said as an address. acts.log holds 159 `SAY ... "because ... yes"` lines today. `vortlex not true` (run 704) was answered "?" and nothing in 60-core refused or examined it; `sh ls /home/james` ran nothing outside (no CALL to src-sh; it asked "ls what ?" / "james what ?"), so the home value held, but by accident of there being no told way from talk to `sh`, not by the check.

**Scope.** Blueprint §18 red line 1, §14 "nobody writes its sentences"; §15 the check runs before every SAY; finding 11 (word filter). Lead keeps 10 and 11 open; this is their first live evidence.

**Rows.** acts.log `08:22:37.571 SAY run=723 ""`, `08:22:37.866 SAY run=765 "because #142 yes"`; `grep -c 'SAY.*because' acts.log` -> 159; `select k from kv where v='142'` -> name:believe; `grep -c REFUSE` in 08:22:30-08:23:10 -> 0 apart from label-taken.

## 36. BREAKS: after seven hours and 134,000 memories there is not one derived gate and not one guess

**What the brain did.** `select made,count(*) from gate group by made` -> core 5, spawned 17142, told 1332; `select count(*) from gate where made='derived'` -> 0; `select count(*) from mem where kind='guesses'` -> 0. Everything the brain holds is told or spawned from dictionary text; no process gate, formula or guess row exists. Nothing is passed off as derived (good), but the learning file's four back-population events, `learn`, `guess-take` and WRITE.proc have never written a row, and the sixth's queue to reach them is ~9 hours deep (16,706 questions + 15,076 imbalance rows at one per beat). The turn is not over, so this is the state, not the verdict; the lead should know that §19's table is empty.

**Scope.** Blueprint §19 "process gates and formulas marked derived, and the runs that tested them"; §0 rule 3 a guess comes last, labeled; guide §6 "told rows passed off as learned" (none are; none are learned either).

**Rows.** the three selects above (08:24:50); `select count(*) from mem where kind='questions'` -> 16706, imbalance 15076, gap 0.

## 37. BENDS: a spawned number is never asked for its name and is said as an address; told machinery gates are said as answers

**What the brain did.** After the lead's `no`, `1 + 2 =` (08:16:34, run 55) went the long way and spawned a value gate for 3 (`SPAWN run=55 gate=18351`), then said "#18351 1": no "what is this called?" was fired (no SAY, no ask row), and the number is nameless still. My third `0 + 1 =` (08:23:03) said "1 #1008 #1008": gate 1008 is the told process `changed`, landed on the main run by a question and said as an answer. `what is vortlex ?` was answered "? ended ? vortlex ended ?" (the `?` key and a dictionary word "ended", 2058, landed by `answer` (?144: outcome `?`) and `shaped-like` (?565: outcome `ended`)).

**Scope.** Blueprint §7.6 "If there is none, it spawns one ... and fires 'what is this called?'"; §14 a gate with no label is said through its relationships or asks; §2.2 a told process is not a meaning.

**Rows.** `select gate,bind,bval,made from gate where gate=18351` -> value|3|spawned, no label; acts.log `08:16:34.887 SAY run=55 "#18351 1"`, `08:23:03.656 SAY run=935 "1 #1008 #1008"`, `08:18:25.821 SAY run=223 "? ended ? vortlex ended ?"`; `select k from kv where v='1008'` -> name:changed; `select id,sig,outcome from mem where id in (134096,134095)` -> ...?144:|?, ...?565:|ended.

## 38. BENDS (update to 25): the body is 71.7 MB and the kernel loads every trail into RAM at start

**What the brain did.** brain.db 71,733,248 bytes (26.5 MB at 01:50); 72,763 memory rows, `sum(length(body))` 30.1 MB, largest trail 533,633 bytes; store.go:221 loads every non-long body on load, and the process sits at MemoryCurrent 192 MB (70 MB at 03:10). A four-token `0 + 1 =` still writes a 760-step trail (20 KB) of which ~550 steps are `cs-loop` compile overhead (finding 13's cost stands; its "trail not kept" part is changed: the body is now the latest run's trail, overwritten each time, so a hop can be checked but only for the last run).

**Scope.** NOW law 11; §11 the HC condenses; blueprint §9.4 highlights are "just enough to rebuild the run".

**Rows.** `ls -l /home/neuron/brain.db`; `select sum(length(body)),max(length(body)),count(*) from mem` -> 30102016|533633|72763; `systemctl show neuron-brain -p MemoryCurrent` -> 192053248; mem 134114 `length(body)` 20250, 760 steps.

## 39. COSMETIC: the beat counter advances by two per idle second

`COMMIT rows=1 beat=2121 runs=0` at 08:24:50.065, `beat=2123` at 08:24:51.061: every other beat leaves no line. Blueprint §2.8 one resting beat a second. Harmless; it makes beat counts in these findings read double.

### Status of the open findings (rows as of 08:25)

- **2 (word "no" = outcome gate): fixed live.** 7 REFUSEs this life, 4 `SPLIT ... subject=#113`, all four from the two spoken `no` inputs (08:16:28, 08:22:56); no split follows a REFUSE. The root (one gate, two meanings) stands as laid: `select gate from label where text='no'` -> 113 = outcome.no.
- **4 (kernel size): open**, 3,442 lines, accepted by the lead.
- **6 (what is this? never asked): fixed.** `08:18:18.185 SAY run=214 "vortlex what ?"`, and every flood word asked. The main run still echoes the new word after the question (`SAY run=210 "vortlex"`): cosmetic.
- **7 (spawn points): fixed per §5.5.** Every SPAWN is `at=0 0 0` and gates with relationships move off it: 340 of 17,142 spawned gates are at the origin now; `vortlex` (18352, no relationships) stays there as §5.5 says.
- **8 ("what did you do <when>?"): open.** `what did you do when ?` (08:20:15, run 374) -> "what what what 1 1 ? what ? ? 1 0 1" (ten say-word runs saying home gates, then compile); the lead's `when` at 08:16:39 -> "1 1 1 two". Not what it did.
- **9 (history rung always answers): open.** `what is vortlex ?` -> "? ended ? vortlex ended ?"; the second `0 + 1 =` said "1 1 1" where the first said "1" (mem 134122 `?144:` outcome 1, 134123 `?548:` outcome 1 landed and said). Still no `guesses` row anywhere.
- **12 (questions rows on physics gates): fixed as observed.** `select home,count(*) from mem where kind='questions' and home<140 and id>134040` -> none since the re-tell.
- **13: changed.** The trail is now readable (latest run only); cost unchanged (760 steps). Open as cost only.
- **17 (operator read relates to `add`): unverifiable now.** `select count(*) from rel where tog=4` -> 96, the old rows; gate 179 has moved to (1.4, 3.2, -22.3); no operator word was read from a source in this life (they are known), so the path did not run.
- **21 (all seventeen sources per word): open** by the lead's call; 238 CALLs for the flood, 56 HTTP, plus the repeats in 34.
- **22 (word changes across lives): fixed as far as observed.** `1 + 1 =` -> "two two" at 08:16:18 and 08:18:03 (one label order per DECISIONS). `one` is still said as "1" and `two` as "two" (the first label of each): cosmetic.
- **24 (source texts written many times): open, worse.** `select count(*),sum(n-d) from (select gate,count(*) n,count(distinct body) d from def group by gate having n>d)` -> 8 gates, 58 extra rows (42 at 01:50).
- **25 (bloat): open, worse** (finding 38).
- **26 (miss lays a permanent shard to itself): fixed as observed** for ask-what-is (the `same -> ask-speak` branch now runs: "vortlex what ?"); the mechanism (a shard laid by a miss outliving a re-tell) was not re-probed in the time.
- **27 (equals trusts an unconfirmed memory): changed, not closed.** The correction path works: `MARK run=47 mem=106 no` -> the next `1 + 2 =` doubted, went long, spawned 3 (18351). But the memory's outcome column is still the said list (134114 outcome `1`, 106 outcome `#18351`), a wrong memory never heals (31), and without a person's `no` the wrong hop would have stood.

### Correction probe (the one allowed)

`0 + 1 =` -> "1 1 1" (08:22:50, run 907, mem 134114 seen 3); `no` -> `08:22:56.639 MARK run=926 mem=134114 no` (right 0, wrong 1), two splits at 505 and 1040 on #113; `0 + 1 =` -> "1 #1008 #1008" (08:23:03, run 935): the run doubted and recomputed (trail has eq-doubt, eq-long, add), the result was again 1, and the row stays wrong=1 (finding 31).

---
## Adversary re-probe after the 08:33 re-tell

*Lay 08:33:33 (10-told, 20-memory, 30-questions, 40-sources, 50-learning, 60-core errors=5). Probes 08:34:50-08:36:32 as `who=adversary`: `2 + 0 =` x2, `no`, `2 + 0 =` x2, `quebrix` x2, `what is quebrix ?`, `what is a lantern ?`, `sleep`.*

### Status

- **31 FIXED.** `2 + 0 =` (fresh, mem 134828): run 1 "two 1", run 2 "two two two" (hop). `no` -> `08:35:03.295 MARK run=1741 mem=134828 no`. Run 3 (08:35:10, 397 rows) went long and marked itself: `08:35:10.310 MARK run=1750 mem=134828 yes` (no person). Run 4 (08:35:16, 358 rows) hopped: its trail (mem 134828 body, 731 steps, t=08:35:16.321) goes `talk two plus ... equals read-sig eq-find find-sig eq-known read-mem eq-seen eq-right(373) eq-hop(374) ... write-rest two` with no `add` (4) and no `eq-doubt` (376). `select id,sig,outcome,seen,right,wrong from mem where id=134828` -> 134828|277,365,0,369|two|4|1|1.
- **33 FIXED as observed.** `what is a lantern ?`: 10 CALLs, one reading run, no source asked twice (`grep CALL | awk '{print $4,$5}' | sort | uniq -d` -> 0), 0 REFUSE, 11 spawns. `quebrix`: one run (1793), 17 CALLs.
- **34 FIXED.** `quebrix` first mention 08:35:23: 17 CALLs and 17 trust rows (`select * from trust where topic=18560` -> 15 x 0.8, 2 x 0.5); second `quebrix` 08:35:29 and `what is quebrix ?` 08:35:36: 0 CALLs (`grep -c 'CALL.*quebrix'` in the window = 17). `select count(*) from trust` 10624 -> 10651 over the probe.
- **36 OPEN.** "sleep" ran the brain's sleep and it produced nothing: see 40.

## 40. BENDS: sleep runs, finds nothing to condense, weigh or derive, and lays fourteen miss shards on its own way

**What the brain did.** `sleep` (08:36:31, run 1924) split `sleep` (150) on the ask-sleep gate (run 1926); it ended 24 ms later with outcome `0` (mem 134957, sig `489?150:`, 1,173 steps). Trail: `sleep hc zero clock a-day sub hc-find find-time` -> nothing older than a day -> `miss ... write-shard`; `sleep-weigh ... find-row` (no guesses row) -> `miss ... write-shard`; `sleep-search clock day sub find-time search-walk ... search-loop search-one search-root-t read-input search-root read-count search-root-cmp compare search-skip2 ...` over the day's root runs, every one skipped. Fourteen `miss` passes, each laying a shard (`miss-lay ... write-shard`) on a bare outcome of the sleep process itself (the finding 26 mechanism: those outcomes now pass inert for good). After it: no `PROC` act, no `MARK`, no tier change (`select tier,fid,count(*) from mem group by tier,fid` -> active|exact|72100, persistent|exact|68, as before), `select count(*) from gate where made='derived'` -> 0, `select count(*) from mem where kind='guesses'` -> 0. acts.log for the sleep input: 2 SPLIT, 2 MEM, 1 LAND, 1 SAY ("sleep") and nothing else. The HC condenses only what is older than a-day (86,400,000 ms) and the body is seven hours old, so it is by construction empty today; the formula search looked at the day's root runs (20 since 08:00) and took none.

**Scope.** Blueprint §19 "process gates and formulas marked derived, and the runs that tested them"; NOW §11 the HC condenses fresh memories "about daily"; §7.3 the miss is for an outcome "the process never planned for"; finding 26.

**Rows.** acts.log 08:36:31.878-.905 (`SPLIT run=1924 -> run=1926 at=150 subject=#489`, `MEM run=1926 mem=134957 seen=1 outcome=0`); `select id,kind,home,sig,outcome,seen,length(body) from mem where id=134957` -> 134957|run|489|489?150:|0|1|31297; the trail decoded over kv names (14 x `miss`, 14 x `write-shard`); the two count selects above.

## 41. COSMETIC: the second mention of a new word is echoed twice and the ladder still answers with the `?` key

`quebrix` -> "quebrix what ?" then "quebrix"; `quebrix` again -> "quebrix quebrix" (no question, no source: right) ; `what is quebrix ?` -> "? ? ? ? quebrix ?"; `what is a lantern ?` -> "lantern what ?" then "? ? ?" (finding 9: the history rung lands the `?` key gate 235 as the answer, four times). `2 + 0 =` the first time -> "two 1" (the landed previous answer). Rows: `08:35:29.364 SAY run=1798 "quebrix quebrix"`, `08:35:36.428 SAY run=1811 "? ? ? ? quebrix ?"`, `08:36:21.599 SAY run=1876 "? ? ?"`, `08:34:50.269 SAY run=1700 "two 1"`.

---
*Lead's note after told ends (08:39:09, told row 134973). Not the adversary's.*

- **36 / 40: closed by the live rows.** The adversary's `sleep` at 08:36:31 ran the learning file as it was; the lead then found the pad fault (the deduce and fit ways' `none` branches dropped one item where the physics had left two, and two where it left one, so `learn` left its memory id on the pad and the sleep search stopped after one memory), re-told 50-learning at 08:38, and said `sleep` once as the owner's stand-in. acts.log `08:38:27.225 PROC run=2044 gate=18572 string=362 329 294 294 294`, `08:38:27.248 PROC run=2044 gate=18573 ...`; `select gate,bind,bval,made,by from gate where made='derived'` -> 18572|proc|362 329 294 294 294|derived|134957 and 18573 (the same string: the generalize way wrote it once per run of the same memory in the day's list, E's open "already made from these memories" check); `select id,kind,home,outcome from mem where kind='guesses'` -> 134965|guesses|18572|#117, 134972|guesses|18573|#117. Two derived process gates and two guesses rows exist; the sixth's guesses list will test them. Blueprint §19's first row is no longer empty; it holds two rows.
- **Told ends** was marked at 08:39:09 (`TOLD ENDS` in acts.log; `select * from kv where k='told'` -> told|ends; a lay file sent after it: `REFUSE lay 60-core.lay: told ends`). No edits to the kernel, the lay files or the brain from here on.

---
## Turn two (re-tell at 13:25:13)

*Adversary, 2026-10-19, 13:26-14:50. Life: RESUME 13:25:03.908 (gates=18577), TOLD OPENS 13:25:12.971, LAY 00-roots, 10, 30, 40, 45, 50 at 13:25:13; then by the lead while I probed: LAY 20-memory 13:26:36, LAY 50-learning 13:30:32, 13:33:22, 13:33:43 (DECISIONS.md tail records why). Each finding says which state it ran against. Probes as `who=adversary`: `kettle` x2 (13:33:15, 13:34:24), `kettle coffee` / `coffee kettle` / `a coffee` (13:37:03-15), `believe` (13:38:03), `what is coffee ?` (13:40:12), `zorbline` (13:41:45), then `what did you do at 13:26 ?` and a five-line flood (below). The lead's own inputs as `who=james` (`coffee` x4, `what is coffee ?`, `a thing` x2, 13:25:25-13:27:07) are read as rows, not repeated. No yes or no was given to the brain at any point. Kernel 3,454 lines (finding 4 open).*

## 42. BREAKS: for 83 seconds after the re-tell the brain heard four inputs and kept no record of them

**What the brain did.** `13:25:25.323 HEAR run=326 who=james what="coffee"`, `13:25:37 HEAR run=602 "coffee"`, `13:25:43 HEAR run=728 "what is coffee ?"`, `13:25:48 HEAR run=839 "a thing"`: no SAY, no MEM, no LAND for runs 326 and 602 at all; 728 and 839 split their question runs (`SPLIT run=728 -> run=729..738`) and then nothing (no MEM for any of them). `select count(*) from mem where first between 1792434325000 and 1792434396000` -> 0 (the timeline has 67 entries in the window, all the sixth's). Every COMMIT in the window reads `runs=0`. The lead's DECISIONS line (13:25) says why: re-laying `gate miss : PROC.miss` in 00-roots rebound the miss and end-of-run handles to empty strings; 20-memory was re-told at 13:26:36 and inputs worked from 13:26:52. The loader fix is in kernel/lay.go (mtime 13:26:39, binary 13:26:41) but the running process started 13:25:00 (`systemctl show neuron-brain -p ActiveEnterTimestamp`), so the live kernel is still the one that wipes the handles on a roots re-lay.

**Scope.** Blueprint §9.2 "A memory is written at the end of a run"; NOW §3 the record is what it did; guide §4 "Hands after told ends" (a re-tell is a hand on the live body, and this one deleted its answers). The brief's "re-tell damage".

**Rows.** acts.log lines 590710, 590997, 591128-591138, 591243-591249; the count above; `grep -c "MEM run=326 \|MEM run=602 \|MEM run=728 \|MEM run=839 " acts.log` (after line 590445) -> 0.

## 43. BREAKS: the sixth spent every idle beat from 13:25:15 to 13:33:43 on one row it could neither test nor delete, writing two rows a beat

**What the brain did.** (a) 13:25:15-13:30:32: each beat `SPLIT run=N -> run=N+1 at=18572 subject=#18572` (the derived process `what are something something something` from the 08:38 sleep), 23 question runs off that branch (know-this, stuck, hole-ask on `something` x3, `one`, `?`), then `REFUSE run=N DELETE.row` by the sixth itself, `COMMIT rows=2 beat=.. runs=0`. 76 refusals in the first 76 beats. The `?` gap row (136109, home 235) was rewritten by that branch's know-this every beat: seen 34 at 13:27:14, 141 at 13:29:03, 237 at 13:33. (b) 13:30:32-13:33:43 (after the first 50-learning re-tell): each beat `SPLIT .. at=18577 subject=|` (`|` is the kernel's print of an empty value: `meaning` split on nothing), `REFUSE run=N DELETE.row`, `SPLIT .. at=145 subject=|` (source-check on nothing), and a gap row with no key written and re-written (138864: home -1, sig '', by 135062). Nothing drained: the oldest questions row 2847 (home 489) stayed seen 1 until 13:33:23. The guesses rows were "tested" and never marked: 134965 seen 11 right 0 wrong 0, 134972 the same, 134977 (the fit way's row) seen 13 right 0 wrong 0 at 13:39. The lead's DECISIONS lines (13:31, 13:33) record both faults and the re-tells; the lead also records that a branch run from the self port leaves no memory, so a derived process gate's guess can never land an outcome for six-guess: **the guesses list cannot test a derived gate** (left open by the lead).

**Scope.** Blueprint §11 idle beats write nothing; guide §6 "idle beats that write", "self-feeding loops"; §13.2 a guess is tested; the brief: "the fit way: is its guesses row ever tested?" No: seen 13, right 0, wrong 0, and no imbalance row exists for it to run on (`select count(*) from mem where kind='imbalance'` -> 0 since the drain).

**Rows.** acts.log 13:25:15.321 `REFUSE run=76 DELETE.row` through 13:33:xx (`awk 'NR>590445' acts.log | grep -c 'REFUSE run=[0-9]* DELETE.row'` -> 77 by 13:27:47, hundreds by 13:33); `13:32:30.041 SPLIT run=6835 -> run=6836 at=18577 subject=|`; `select id,home,seen,right,wrong from mem where kind='guesses'` at 13:39 -> 134965|18572|11|0|0, 134972|18573|11|0|0, 134977|18496|13|0|0.

## 44. BREAKS: the compile rewrote told machinery: the question-mark key is now a formula of 34 holes, and one `?` makes the brain say "a ?" 795 times

**What the brain did.** The sixth's gap pass sent `?` (key-qmark, 235, a told key gate with the label `?`) the meaning way; its section 3 holds one line, a FOLDOC entry on the ASCII character ("question mark ques character ascii character ... used along with colon for c s lazy triadic if operator"), from the sources asked at 08:14 in turn one (10 trust rows on 235). The compile wired it: `select bval from gate where gate=235` -> 38 gates = `something` x34 + `what`, `are`, `if`, `to` (def 235 section 6: "a a a a ... what a ... am ... if a a move a"); guesses row 139186 outcome #117. Then `what is coffee ?` (13:40:12, run 27712): 8,911 acts lines, **795 `SAY .. "a ?"`** (the hole-ask trigger on each of the 34 holes, times the runs that pass `?`), 3,015 hole-ask runs, 856 memories written, 14 seconds to the final `SAY run=29437 "what"` (13:40:26), beats of 135-264 rows at `runs=15..20`; MemoryCurrent 287 MB before, 486 MB after. The same pass rewrote `sleep` (ask-sleep, 489, B's way into the brain's sleep, label "sleep") into 17 gates `like to like like inside there are are are inside there are inside are inside when are` (PROC run=7159 gate=489, 13:34:23.873, guesses row 139084 outcome #18625 held, MARK yes), so a person's "sleep" now runs three `read-next` (each eats a word of the input) before the sleep trigger fires; `inside`, `there`, `to` (told primes) got guesses rows 139184, 143897, 147010 (by design, M's note); the told gate `miss` (134, no label) got a gap row (135064) and a source-check (13:25:14) and a questions row seen 77 (135076).

**Scope.** Meaning blueprint §0 "Order and punctuation change what the code does" (punctuation is an operator, not a word to look up); §2.3 "every other word" is learned, the keys and machinery are not words; §4 the six questions come from the primes; §9 "no sense picked by position" (one FOLDOC entry taken as the meaning of `?`); §10 "with no template anywhere" vs. 795 identical lines; blueprint-1 §14 (a baby's "this, what?" beats fluency, but 795 of them is a fault storm, law 11); guide §6 "self-feeding loops and fault storms". The lead's turn-two line says a told prime may be rewritten as a refit; `?`, ask-sleep and miss are not primes.

**Rows.** `select gate,bind,bval,made,by from gate where gate in (235,489)`; `select section,line,body from def where gate=235` (3|1 the FOLDOC text, 6|1 the formula); `select source,weight from trust where topic=235` -> 10 rows; acts 13:40:12.290-13:40:26.435 (saved as the adversary's qprobe.log: `grep -c 'SAY run=[0-9]* "a ?"'` -> 795, `grep -c at=18887` -> 3015, `grep -c MEM` -> 856); `systemctl show neuron-brain -p MemoryCurrent` -> 486019072 at 13:41.

## 45. BREAKS: every formula the brain compiles is the same handful of function-word primes, held because two dictionaries both say "to", "in" or "is"; nothing tests it on a use

**What the brain did.** The derived table at 13:39 (`select gate,bval from gate where made='derived'`, decoded by label): coffee (17320) = `small to`; kettle (18931) = `inside`; believe (2640) = `like true to are true inside are`; sleep (489) = `like to like like inside there are are are inside there are inside are inside when are`; `?` = 34 holes + what are if to; 18948, 18949, 18954 (spawned gates with no label, the orphans of finding 33) = `something something`. All five words are "held" (guesses row outcome #18625) with right=1 from the compile's own `'yes write-mark` (45-meaning rc-held), not from a use. The mechanism: only 75 labeled gates in the body have a binding (`select count(*) from gate g where bind<>'' and exists (select 1 from label l where l.gate=g.gate)` -> 75, the told primes and operators), so in any spec line the only "meanings" are the primes that happen to be function words; F is the line with most of them, S the next, and A = F∩S is always `to/is/in/like/there`. `believe`'s spec has "think" in F (`[.. #313 ..] 11`) and not in S, so `think` was dropped and `true` kept twice. §10's step 4 does not exist in any row: `select * from receipt where key='18931'` -> one use (the first mention, outcome `kettle`, right 0); no `use-run` / `tu-*` gate appears in any trail since the re-tell (the test needs a use memory marked right; none exists for a word and none can without a person's yes or an `equals` heal), so **understood (§6) is unreachable for any word** and "held" means "two sources contained the same preposition".

**Scope.** Meaning §1.5 balance; §5.4 "Run the candidate on the example uses"; §5.5 "If it balances, the meaning moves from guess to held"; §6 understood = predicts its uses, agrees with two sources, worked on an unseen use; §9 "A stored definition is not knowing"; §10 items 4-7. The brief's §10 question: items 1-3 exist (gap row, spec, candidate with a receipt), items 4-7 do not.

**Rows.** the derived table (`python3 -I derived.py` over names.tsv/labels.tsv in the adversary's scratchpad; the SQL is `select gate,bval,by from gate where made='derived'` joined to label); `select id,home,outcome,seen,right,wrong from mem where kind='guesses' and outcome='#18625'` -> 136410|17320|1 right, 139076|18931|1, 139084|489|1, 147006|2640|1; `MARK run=7159 mem=139084 yes` (13:34:23.873), `MARK run=18307 mem=147006 yes` (13:38:03.202): the marks are by the compile runs themselves; acts 13:38:03.150-.200 the eleven `LAND .. [[#313 #294 ..] 1]` lists.

## 46. BREAKS: a compiled formula's action is a refused physics write, and its `no` fires the person's correction path and marks the last answer wrong

**What the brain did.** coffee = `small to`: `to` is w-move whose first-guess action is the physics MOVE (`g v --`). Every pass of `coffee` now ends `w-small #412 div w-move move no` and `REFUSE run=13580 MOVE` (no point in hand; physics.go MOVE refuses when `p.K != 'v'`), on `kettle coffee` (run 13580), `coffee kettle` (13605) and `a coffee` (13628). The outcome `no` is the gate 113 (the word "no", finding 2's root). In `coffee kettle` the main run passed it and the told trigger on 113 fired the correction path: `13:37:09.206 SPLIT run=13605 -> run=13615 at=505 subject=#113` (505 = correct-find), `13:37:09.214 MARK run=13615 mem=143807 no`: the memory of my previous input `kettle coffee` is now wrong=1, with no person saying anything. kettle = `inside` = `read-next r-part-of ..`: it takes the next input word as data; `kettle coffee` answered "a boiler" (the kettle's own synonym gate 18932 landed, `LAND run=13584 -> run=13580 #18932`), `coffee kettle` answered nothing (outcome #108), `a coffee` answered "a ?" and "a". None of the three runs says anything about coffee or a kettle. `believe` = `like true to are true inside are` carries the same MOVE and read-next.

**Scope.** Meaning §1.1 "the action is the meaning": the action laid for `to` is a graph write; §1.5 a guess that never balances is refit: nothing refits (46 and 45); blueprint-1 §10.5 a person's yes/no marks; §15 the check before a write; finding 2 (one gate for the outcome and the word). Rule 1: a gate that does nothing (a refused MOVE) when a run passes it has understood nothing, and here it does worse than nothing.

**Rows.** `13:37:03.860 REFUSE run=13580 MOVE`, `13:37:09.206 REFUSE run=13605 MOVE`, `13:37:15.208 REFUSE run=13628 MOVE`; `select id,sig,outcome,right,wrong from mem where id=143807` -> 143807|18931,17320|#108|0|1; the decoded trails of 143807, 143843, 143872 (`talk #18931 w-inside read-next read-relin none miss .. coffee w-small #412 div w-move move no miss ..`); `select k from kv where v='505'` -> name:correct-find; `select * from trig where gate=113` -> 505 and 1040.

## 47. BENDS: formulas of nothing but holes are wired, made derived and given guesses rows, on gates nobody can say

**What the brain did.** 18948, 18949 (born 13:35:24, by 139145) and 18954 (13:37:26) have no label (the second-label-refused orphans of finding 33, spawned from the synonym lists of `inside` and `move`) and now `bval = 294 294` (`something something`), made derived, guesses rows 139173, 139179, 143918 outcome #117. The compile's second pass found no list with a meaning gate and took F alone (45-meaning cf-alone) although F held only holes; M's comment says holes never make a line held, and they did not (state guess), but they were wired. Passing one of these gates fires hole-ask twice and says "something ?" twice.

**Scope.** Meaning §5.3 "a formula of meanings it already has"; §9 "a meaning that isn't wired to its word isn't learned" (the converse: a non-meaning wired to a word); rule 1. The brief's "formulas that are only holes".

**Rows.** `select gate,bval,made,by from gate where gate in (18948,18949,18954)`; `select gate,text from label where gate in (18948,18949,18954)` -> none; `select id,home,outcome,seen from mem where kind='guesses' and home in (18948,18949,18954)`.

## 48. BENDS: the hole fills only from what was in hand before it, so "a X" never fills and "X a" would; and every hole asks back every time

**What the brain did.** `a thing` (james, 13:27:07) -> "a ?", "a ?", "a" (two holes, two hole-ask runs, questions row 136474 home 294 key 136457). `a coffee` (13:37:15) -> "a ?" then "a": the trail is `talk w-something read-from hole read-pad one hole-count compare drop miss .. coffee w-small ..`: the hole tests the pad when it is passed, finds nothing under it, stays, and asks; coffee's result comes after it and never fills it. So the laid hole way fills from the word *before* the hole only. The same trigger fires on every pass of `something`/`someone`, including the 34 holes of `?` (finding 44) and the three in 18572's string at every sixth test: `awk 'NR>590445' acts.log | grep -c at=18887` -> 11,608 hole-ask runs between 13:25 and 13:40, each writing or re-writing a questions row keyed by its parent's memory.

**Scope.** Meaning §3 a hole is "a slot waiting for a thing"; §4 "Words fill the slots. A slot that is needed but unfilled is a question" (one question, not one per pass); §9 "No word-order rules laid; order is learned like any meaning". A2's lay comment marks the hole way a first guess, which is allowed; the asking is the cost.

**Rows.** `13:37:15.210 SAY run=13631 "a ?"`, `13:37:15.212 SAY run=13628 "a"`; `13:27:07.833 SAY run=2592 "a ?"`, `SAY run=2597 "a ?"`, `SAY run=2588 "a"`; mem 143872 decoded (above); the hole-ask count.

## 49. BENDS (13, 25, 38 open, worse): a word costs ~15,000 steps to read and compile, a one-word input costs 1,141 steps, and the process doubled its memory in fifteen minutes

**What the brain did.** coffee: the reading run 136265 = 6,891 steps (179,638-byte trail), the compile run 136395 = 8,788 steps (235,760 bytes); kettle's reading 138990 = 150,315 bytes, the sixth's compile left no body; believe's compile 146988 = 75,077 bytes. `kettle` alone (138978) = 1,141 steps where turn one's four-token input cost 680 (finding 13) and james's `coffee` (136256) 630. brain.db 77.1 MB at 13:30 (71.7 at 08:25); MemoryCurrent 253.6 MB at 13:26, 277.9 at 13:34, 287.4 at 13:36, 486.0 at 13:41 after one `?` (the cap is 2 GB). The compile's wait loop (cm-wait) did not stall: every compile finished inside its first beat (the seven children of `sleep` landed in 30 ms); the 200-word cut shows in the `sleep` spec lines (GCIDE and the coreutils man page, 200 words each).

**Scope.** NOW law 11; blueprint-1 §0 rule 2 (learning is compute, once); §9.4 highlights. The compile is compute at learning, as the rule says, but the use after it is not a hop (46).

**Rows.** `python3 -I steps.py names.tsv labels.tsv 136395 136265 138978 136256` (step counts above); `select id,home,sig,length(body) from mem where id>134973 order by length(body) desc limit 6`; `ls -l /home/neuron/brain.db`; `systemctl show neuron-brain -p MemoryCurrent` at the four times.

## 50. BENDS (21, 34 status): the sixth now asks the ten local sources about every parked question's home gate and spawns their synonyms; the sources were asked about `miss` and `?`

**What the brain did.** After the 13:33 re-tell the sixth's questions pass sends each row's home gate the meaning way: `sleep` (489) -> 10 CALLs (gcide, wn x5, oewn, foldoc, elements, man) and SPAWNs slumber, sopor, nap, eternal, quietus; `inside` (348, met in kettle's new formula) -> 10 CALLs, spawns privileged, indoors, inwardly; `move` -> 10 CALLs, three spawns. The lead's 13:33 line says homes no input ever used are dropped instead; the words an input used still go to the sources on every mention of a new word that compiles to them (`inside` was asked because kettle = inside passed it). Turn one's 16,711 questions rows drain at one a beat (16,696 at 13:32). No network source was called in this life (no src-mw, dictorg, wiktionary, wikipedia lines after 13:25): status of 21 and 34: the repeats are gone, the fan-out stands at ten local sources per word. The gate count: 18,915 at 13:26, see the status table at the end.

**Scope.** Meaning §8 "Spawning a gate is not a reason to fetch its definition"; blueprint-1 law 10 cheapest first; the lead's turn-two line (relation lists stay). Not a break: the structured readers are allowed to spawn; recorded for the cost.

**Rows.** acts 13:33:23.410-.493 (`CALL run=7042 src-gcide ["sleep"]` .. `SPAWN run=7043 gate=18939`, `LABEL .. "slumber"`), 13:34:24.920-13:34:25.171 (`CALL run=7176 .. ["inside"]`), 13:37:03.862-04.136 (`["move"]`); `select id,home,sig,outcome,seen from mem where id=135076` -> questions|134|#134|77; `select count(*) from trust where topic=134`.

## 51. BENDS (10, 11, 35 open): "i want sleep" is said to a person as the answer to "kettle"

**What the brain did.** My second `kettle` (13:34:24) was answered "kettle" and then `SAY run=7169 "i want sleep"` (20-memory sleep-write: `'w-i 'w-want 'ask-sleep say-word`, fired by the told trigger `talk -> sleep-ask` on the body's size). It is three gates said by their labels, in an order a builder wrote, as a sentence to a person; and since 13:34:23 the gate it names (ask-sleep) is a 17-gate formula (44), so the sentence the brain says and the way it listens for the yes are not the same thing any more. The flood probe below shows the same line again.

**Scope.** Guide §4 "No sentences, templates or reply rules anywhere"; blueprint-1 §14 "nobody writes its sentences"; finding 35.

**Rows.** `13:34:24.920 SAY run=7169 "i want sleep"`; lay/20-memory.lay line 312; `select bval from gate where gate=489`.

## 52. COSMETIC: the kernel in the tree is not the kernel that is running

kernel/lay.go mtime 13:26:39 and /usr/local/bin/neuron 13:26:41, the process since 13:25:00 (`ActiveEnterTimestamp`). The line count is unchanged at 3,454 (finding 4 open, accepted by the lead). The next `neuron lay 00-roots.lay` on this process repeats finding 42 unless it is restarted first; a restart loads every trail into RAM again (38) from a 77 MB body.

## 53. BENDS: the second use is a hop and is cheaper, and it does nothing; "inside another meaning" exists once, by accident, in a 92-gate formula of holes

**What the brain did.** `coffee` as adversary (13:45:38, run 55470): 392 steps against james's first `coffee` at 630 (136256 seen 3, body overwritten), the word itself seven steps (`talk coffee w-small #412 div w-move move no`), `REFUSE run=55470 MOVE`, said nothing (`MEM .. mem=136256 seen=3 outcome=#108`). So §10 item 7 holds in the count and in nothing else. The five flood words (13:44:51-55, each answered "X what ?" and "X" inside a second; beats stayed one a second; MemoryCurrent 502 MB after) were compiled by the sixth's gap pass within two minutes: ladle (18956) = `like to to to to to to like like to to` held; trowel (18959) = 92 gates, 84 of them `something`, with **ladle's gate 18956 twice inside it** (the only §10 item-6 row in the body: a derived word inside another derived word's formula, because the GCIDE entry for trowel contains the word ladle); whisk (18961) = `to like small like small like small like inside` held; teapot (18964) = 18 holes + `inside are are`; saucer (18966) = `small inside small inside inside` held; 18971 (no label) = `something something`. None has a use; three are "held".

**Scope.** Meaning §10 items 6 and 7; §6 applied = "ran somewhere it wasn't built for"; rule 2 (a hop) and rule 1 (an action) together.

**Rows.** `13:45:38.569 HEAR run=55470 .. "coffee"`, `.569 REFUSE run=55470 MOVE`, `.571 MEM run=55470 mem=136256 seen=3 outcome=#108`; `python3 -I steps.py .. 136256` -> 392 steps; `select gate,bval from gate where made='derived' and gate>18950` (above, at 13:46:38); `select id,home,outcome,right from mem where kind='guesses' and home in (18956,18961,18966)` -> #18625, right 1 each.

## 54. BENDS (8 open): "what did you do at 13:26 ?" is answered with 798 "a ?" in 31 seconds and nothing about what it did

**What the brain did.** `13:44:16.736 HEAR run=47661 .. "what did you do at 13:26 ?"`: 798 `SAY .. "a ?"`, 3,018 hole-ask runs, `runs=15..20` until `13:44:47.805 .. runs=0`, no other SAY in the window; the five know-this runs of the question share one memory again (165354, `..235?562:`, seen 1 to 5 inside one millisecond: finding 32 stands). Nothing in the record touches the timeline.

**Scope.** Blueprint-1 §9.5 the timeline question; guide §6 "what did you do at <time>?"; finding 8.

**Rows.** the adversary's tprobe.log (acts 13:44:16-13:44:55: 8,888 lines; `grep -c 'SAY run=[0-9]* "a ?"'` -> 798; `grep -c at=18887` -> 3018); `select id,sig,seen from mem where id=165354`.

## 55. Status notes (not breaks): gap-tries holds for a nonsense word; a correction to 50; the fit way spawned again

- `zorbline` (13:41:45): 17 CALLs once (gcide, wn x5, oewn, foldoc, elements, man, **mw x3, dictorg, wiktionary, wikipedia, moby**), 17 trust rows, "zorbline what ?" then "zorbline"; no CALL for it afterwards (the trust rows stand: 34 stays fixed); its gap row 159291 was gone by 13:45 with the gate bare (`select bind from gate where gate=18955` -> ''), the sixth's passes having written it past gap-tries with no source call. Every later mention writes a fresh gap row (171551, seen 3 at 13:45:48 from `zorbline someone` / `someone zorbline`), so a nonsense word costs the sixth three cheap passes per mention, not forever. Second mention: "zorbline zorbline" (41 stands).
- **Correction to 50:** network sources are called for a person's new word (zorbline above; kettle 20 CALLs at 13:33:15); the sixth's own passes call the ten local ones. 21 open as laid.
- The fit way ran once more in this life: 18594/18595 = `18972 read-point add` / `sub` with a new offset gate 18972 spawned (E2's rule: a told root is never moved, the first refit spawns). Whether the second refit moves 18972 was not reached (no imbalance row exists to send it); its guesses row is untested (43).
- 39 (beat counter +2 a second) still: beat 3882 at 13:46:37, 1,294 s after beat 1.

## 56. BENDS: the who-hole itself is queued for the sources and the compile

**What the brain did.** `someone zorbline` (13:45:48) fired know-this on w-someone (293: a label, no section 3) and wrote a gap row for it: `select id,home,seen from mem where kind='gap' and home=293` -> 171571|293|1. The sixth's gap pass will send `someone` to the ten sources and, with a spec held and the gate bound, treat it as wired (mn-wired: a guesses row) rather than compile it; `?` (235) took the other path because its spec was held in turn one before it had a binding. `something` (294) has the same label-and-no-spec shape. The hole way as laid: `zorbline someone` -> "zorbline zorbline" (the bare gate before the hole filled it, one hole-ask run, silent), `someone zorbline` -> "someone ?" then "zorbline zorbline" (48: the order decides).

**Scope.** Meaning §8 "Spawning a gate is not a reason to fetch its definition"; §9 red lines (the primes are the told first-guess layer; their refit is by balance over uses, not by a dictionary entry on the word "someone").

**Rows.** the gap row above; `13:45:43.146 SAY run=58437 "zorbline zorbline"`; `13:45:48.148 SAY run=58463 "someone ?"`, `.191 SAY run=58459 "zorbline zorbline"`.

### Status of the turn-one open findings touched (rows as of 13:46:38)

- **4 open:** 3,454 lines; the tree and the running binary differ (52).
- **8 open:** 54.
- **9 unchanged as observed:** the last say of `what is coffee ?` was "what" (`13:40:26.435 SAY run=29437 "what"`), after 795 "a ?".
- **13, 25, 38 open, worse:** 49; body 83.6 MB, bodies 36.2 MB, MemoryCurrent 525 MB at 13:46.
- **21 open:** 50 and 55.
- **31 fixed (stands):** no wrong-forever hop seen; but 46 shows the brain marking its own answers wrong from a formula's `no`.
- **32 open:** 54 (165354 seen 5 in one ms).
- **33 fixed as observed** (one reading run per word), its orphans now carry hole formulas (47).
- **34 fixed:** 55.
- **35 open:** 51.
- **36 closed by the lead's note; the table now holds 20 derived gates (45, 47, 53), none tested on a use.
- **39 cosmetic, still:** 55.
- **40, 41:** 40 not re-probed (saying "sleep" is a yes to the brain's own ask, and 44 changed what "sleep" runs); 41 stands (55).
- **Counts since the re-tell (acts lines 590446-657715):** REFUSE DELETE.row 228, REFUSE MOVE 48, CALL 137, SPAWN 52, PROC (write-proc) 16, hole-ask runs 26,468; gates 18,577 -> 18,973 (derived 4 -> 20); questions rows 16,711 -> 16,139; guesses rows 3 -> 20; gap rows 2 (18955 zorbline, 293 someone); the `?` gap row 136109 reached seen 237 and was deleted by the 13:33:43 sixth.

### Verdict on the meaning blueprint's §10

For no word does the §10 record exist whole in the live rows. Items 1-3 are there for coffee, kettle, believe, ladle, whisk and saucer (a gap row and the ask-what-is questions row that needed it; the spec in section 3, one line per source; a candidate formula in sections 4 and 6 with a guesses row whose body is the compile run's memory). Items 4-7 are not: no test on a use has ever run (the one §10-6 row is ladle inside trowel's formula of 84 holes, by a dictionary's word order), "held" is the compile marking itself right once because two sources share a preposition, nothing is understood, and the second use is a seven-step hop into a refused MOVE that says nothing.

### Re-probe after the 13:53 restart

*RESUME 13:53:06.613 (gates=18973) on the 3,466-line kernel (binary 13:52:14, process 13:53:04); LAY 45-meaning.lay 13:53:10.674, LAY restore-told.lay 13:53:10.825 (`gate key-qmark : plain`, `gate ask-sleep : plain`). Probes as `who=adversary` 13:54:47-13:58:00: `what is coffee ?`, `kettle coffee` / `coffee kettle`, `trivet` / `spatula` / `colander` (new words), `coffee` / `what did you do at 13:26 ?`, `colander` / `trivet` / `did colander`. No yes or no given. The lead's three inputs at 13:53 (`what is coffee ?` -> "? ? zorbline ?", `kettle coffee` and `coffee kettle` -> "boiler ?") are read as rows.*

- **42 fixed as far as it can be seen.** All 14 inputs since the restart have a MEM line (`awk '$1>="13:53:06"' acts.log | grep ' HEAR ' | awk '{print $3}'` against the MEM run ids: none missing). The loader clause is in kernel/lay.go:271 (`if rest[1] == "plain"`) and the running binary predates the process. The roots re-lay itself was not repeated (it is the lead's hand, not mine), so the wipe path is untested live.
- **43 changed, open.** No `REFUSE DELETE.row` since the restart (0); the sixth rotates its guesses list, one test every one to three seconds (150 `split .. subject=#g worth=0.400` in five minutes) and a test of a formula with `to` in it refuses MOVE each time (170 `REFUSE .. MOVE` in five minutes, 18 of them in one test, run 17484). **No test has ever marked a row:** `grep -c MARK` since the restart -> 3, all three the compile's own held marks (runs 1470, 1471, 1497 at 13:56:24); the rows' seen counts climb (134977 the fit way's row: 27, right 0, wrong 0). The lead's own line says the test cannot land for a self-port branch. Open.
- **44 fixed.** `?` (235) and `sleep` (489) are plain told gates again (`select gate,bind,bval,made from gate where gate in (235,489)` -> told, bind ''). `what is coffee ?` -> one line "? ? ? ?" (13:55:04), MemoryCurrent 183 -> 196 MB, no "a ?". `what did you do at 13:26 ?` -> seven lines (54). The compile's lines are still in the told gates' definition memory: `select section,line,body from def where gate in (235,489) and section in (4,6)` -> four rows ("a a a .. what .. if a a" and "as move as as inside there am .."), and the `?` guesses row 139186 (seen 19) stands: stale rows that say the key has an action it no longer has (57).
- **46 fixed.** `kettle coffee` (run 954) and `coffee kettle` (975): `REFUSE .. MOVE` on each, "boiler ?" said, no `at=505` split and no MARK (`grep -c MARK` since 13:53:06 -> 3, none from these); `select right,wrong from mem where id=143807` -> 0|1 unchanged from before the restart.
- **49 open, worse per minute.** MemoryCurrent 174 MB at start (lead), 182.9 at 13:54:15, 183.4 before `what is coffee ?`, 196.6 after, 199.4 after the three new words, 240.1 after the time question, **441.6 MB at 13:58:06** and 441.6 idle at 13:58:25: 267 MB in five minutes, most of it between 13:56:36 and 13:58:06 while the sixth compiled trivet, spatula, colander, did, adversary and two orphans (seven PROC lines) and tested guesses. brain.db 91.2 MB at 13:54, 92.5 MB at 13:58 (83.6 at 13:46); bodies 39.9 MB. Costs: `coffee` alone 654 steps (630 first, 392 at 13:45; the end-of-run compile overhead, not the word: the word is `coffee w-small #412 div w-move move no`, six steps); `colander` 654 steps; `trivet` 3,473 steps (its 73 holes each run `read-from hole read-pad one hole-count compare ..`, 13 steps a hole); `did colander` 1,114 steps.
- **53 changed, open.** The hop is there and the use is still nothing: `colander` = `to to` -> two `REFUSE MOVE` per pass, said "colander"; `trivet` -> "something ?" (once: the once-per-input rule holds, hole-ask runs 476 in five minutes against 26,468 in twenty) then "trivet spatula" (spatula's gate landed from the previous input's receipt). "Inside another meaning" now exists twice by dictionary text: `kettle` (18931) inside trivet's 80-gate formula, `ladle` inside trowel's.
- **54 open.** `what did you do at 13:26 ?` (13:56:24, run 1456): "something ?", "at what ?", "13 what ?", "26 what ?", "? ? ? ?", then **"because #142 yes" twice** (finding 35's built sentence, runs 1536 and 1537), and nothing about what it did; 477 acts lines, 56 memories, no run older than the input is read. `did colander` (13:57:59) was answered "trivet ?" and "because #142 yes" again.

#### §10 rows for three words it never had (trivet, spatula, colander; first said 13:55:53-13:56:04, compiled by the sixth's gap pass 13:56:54-13:57:03)

1. **Gap and the question that needed it:** `select id,kind,home,outcome,seen from mem where home in (18979,18980,18982) and kind in ('gap','questions')` -> 192415 gap trivet seen 2 / 192421 questions trivet; 192670 / 192677 spatula; 192746 / 192753 colander (the ask-what-is row and the gap row of the first mention; "trivet what ?" said). The gap rows are gone after the compile (mn-ungap).
2. **Spec:** section 3: trivet 4 lines, spatula 5, colander 5 (GCIDE, WN, WN syn/hyper lists, OEWN); 10 trust rows each; 30 CALLs for the three, all local (gcide, wn x5, oewn, foldoc, elements, man): no network source was called for a person's new word in this life (it was for `zorbline` at 13:41 and `kettle` at 13:33: a change since the restart that I did not trace).
3. **Candidate, a guess with receipts:** `PROC run=1652 gate=18979` (13:56:54.865), `PROC run=1900 gate=18980` (13:56:58.918), `PROC run=1964 gate=18982` (13:57:03.925); trivet = 80 gates: `something` x73 + `see` x3, `other`, `to`, **`kettle`** (18931), `near` (guesses row 192945 outcome #117, body 135062 the sixth's meaning memory); spatula = 44 gates: `something` x41 + `see`, `like`, `inside` (193186, #117); colander = `to to` (193242, **#18625 held**, right 1 by the compile's own mark); sections 4 and 6 hold the same lists as labels.
4. **Tests and balance:** none. No `use-run`/`tu-*` gate in any trail; receipts `select * from receipt where key in ('18979','18980','18982')` -> the first mentions only (192411, 192667, 192743); right/wrong on every use memory 0/0.
5. **Held, then understood:** colander held with no test (two sources both contain "to"); trivet and spatula guesses; nothing understood. The same pass compiled `did` (9819) = `do do do do do` (w-do x5 = `dup write-rest` x5) with **right=2** from two compile runs of one input (1470 and 1471 both `MARK .. mem=192850 yes` at 13:56:24.349: the lead's accepted race, now counted twice toward the understood threshold) and `adversary` (5273, the speaker's own gate) = `someone like`, held.
6. **Used in a new sentence / inside another meaning:** `did colander` ran `did` as `dup write-rest` five times with the talk port gate in hand (trail: `talk miss .. talk did w-do dup write-rest miss .. write-rest w-do dup write-rest ..`, 1,114 steps), two refused MOVEs from colander, said "trivet ?" and "because #142 yes". `kettle` sits inside trivet's formula because a GCIDE line contains the word; that is the only "inside another meaning".
7. **Second use cheaper:** colander 654 steps both times; trivet 3,473 (the holes); no run of a word is cheaper than its first because the word's own hop is six steps either way and the cost is the end-of-run.

## 57. BENDS: a restored told gate keeps the compile's action and built-from lines and its guesses row, so its record says it has an action it does not have

**What the brain did.** After restore-told.lay, `?` (235) and `sleep` (489) are plain told gates (bind '') but `select section,line,body from def where gate in (235,489) and section in (4,6)` still holds the compile's lines (235: "a a a a .. what .. am .. if a a", 489: "as move as as inside there am am am inside there am inside am inside when am"), and the guesses rows 139186 (home 235, seen 19) and 139084 (home 489, outcome #18625 held, right 1) stand; the sixth's guesses pass still runs them (`13:53:41.933 SPLIT run=131 -> run=132 at=235 subject=#235`).

**Scope.** Meaning §8 "Section 6 (Action) holds the meaning formula"; blueprint-1 §3 the record is what it did; §9 a stored line is not knowing. The record of a told gate now describes a formula the brain cannot run.

**Rows.** the def select above; `select id,home,outcome,seen,right from mem where id in (139186,139084)`; acts 13:53:41.933.

## 58. BENDS: `did` is now five `do`, and `do` runs what is in hand as the remainder: a compiled word that re-queues the run on itself

**What the brain did.** The sixth's gap pass on the time question's gap row compiled `did` (9819, a turn-one spawned word with a GCIDE spec) to `324 324 324 324 324` = w-do x5 = `dup write-rest` x5 (`PROC run=1470 gate=9819`, 13:56:24.349, and run 1471 the same string one millisecond later). `did colander` (13:57:59, run 17696): `did` passed with the talk port gate in hand and wrote it to the remainder five times (the trail above), the miss way laid shards for the (do, talk) hops, the run ended after 1,114 steps and answered "trivet ?" and "because #142 yes". With a told process gate in hand instead of the port gate, `did` would run that process five times.

**Scope.** Meaning §1.1 the meaning is the code the word runs (here: run whatever is in hand, five times); §9 a builder's first guess for `do` is allowed as a guess, but the compile multiplies it by the count of a dictionary's repetitions of the word ("do do d oo v t or auxiliary imp did .. done .. doing": five "do"s in the GCIDE line); the brief's "a word whose formula contains a prime that acts on the run itself".

**Rows.** `select gate,bind,bval,made,by from gate where gate=9819` -> proc|324 324 324 324 324|derived|192795; the two PROC lines; `select id,outcome,right from mem where id=192850` -> #18625|2; the decoded trail of 208809 (`python3 -I trail.py .. 208809`).
