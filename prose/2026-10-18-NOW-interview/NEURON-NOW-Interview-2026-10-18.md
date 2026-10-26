# NEURON NOW — Interview Outline

*Started 2026-10-18 11:50 CDT. Owner answers, Claude asks and writes.*

## What this document is for

Your words on Neuron are spread over 400+ messages, and some of them changed over time. This interview pins down what you think **right now**, one question at a time. When it's done, the answers get rewritten into one clean, readable document that a builder can use to build Neuron correctly, one time.

My questions come from the short owner-words document (`Neuron-Owner-Words-2026-10-17\NEURON_IN_THE_OWNERS_WORDS_SHORT.md`). The numbers in [brackets] are your message numbers.

## Rules for me (hold me to these)

1. I ask only the questions in this outline, in order, one part at a time (3 to 5 questions per round).
2. I write your answer down in your own words, plus one plain line saying what it decides. I add no design of my own.
3. If an answer raises a new question, it goes in the **Parking lot** at the bottom. I don't chase it then.
4. You can answer **skip**, **later** (not needed for turn one), **wrong question**, or **you already know this**.
5. Where you said two different things at different times, I quote both and ask which one holds now. I don't pick for you.
6. Before each round I say which part and which question numbers we're on.

---

## PART A — What it is, and what turn one has to be

*Settles the scope. Every later part only needs answers for what turn one needs.*

- **A1.** In one or two sentences in your words today, what is Neuron?
  - **Answer:**
    > neuron is a computer that can build itself, talk to itself and it is thought that it can reason and understand and learn on it's own. It's comprised on neurons that are database nodes specifically built to do these tasks outside the normal realm of code. It has it's own language which is thought to be the root of human language such that any human language can be applied and it the neuron itself will understand without having to adjust itself at all. It has three parts, it's code structure part that allows it to perform the actions of the meanings of words or code, the math part that helps it to have problem solving and adds to it's reasoning capabiltiyies, and the language part this is the most out of the box thinking... it has been determined that human words are essentially short hand code to meanings, and by llms often confused with definitions, but definitions are the describtions of the meaning, the meaning of a word is the action that word causes in its value... these meaning are very tough to understand because they are not written anywhere, and each word which is short hand code has dependancies to other words that might slightly change their actions in a situation, the confusing part, because the root is lost to history of compaction overtime, over the human existance the short hand code is decribed by short hand code, so without an understanding of the shorthand code itself it becomes hard to decipher the meaning at a code level. So in one sentance Neuron is a graph of math type structure that represents the root meaning of language, it learns slow, but once it achieves understanding and meaning it operates nearly as a deterministic function that can do many things. at the surface it looks like a chatbot, but in actuallity because it has the capability to run parallel processes it basically can spin determinism into congnigtion without using great amounts of energy. This is thought to be done by using a combination of asking itself questions about its own state, history, memories, and checking source material for answers to it's questions.
  - **Decides:** Neuron is a computer that builds itself, talks to itself and learns on its own. It is made of neurons, which are database nodes. It has three parts: **code** (it performs the actions that meanings stand for), **math** (problem solving), and **language** (a graph of the root meanings under all human languages). A word is shorthand code; its meaning is the action it causes; a definition only describes that meaning. It learns slowly, then runs almost like a deterministic function. Cognition comes from parallel runs, from asking itself questions about its state, history and memories, and from checking sources.
- **A2.** Turn one "produces the baby that can become Isaac Newton" [403]. On its first day, what must the baby be able to do, and what must it **not** have yet?
  - **Answer:**
    > on it's first day the baby must be able to learn, build, adjust, test, and write new processes that better itself. processes that no one told it to do... processes that it derived on its own. it must have a state timeline, be able to build new neurons, organize them, have memories and create relationships of meanings to other meanings, check source, diff source understanding vs current state and have a sense to find a balance or inequality in an outcome to figure out if it has made progress or obchieved it's goal.
  - **Decides:** Day one, the baby must:
    1. learn, build, adjust, test, and write new processes that improve itself, which nobody told it to make;
    2. have a state timeline;
    3. build new neurons and organize them;
    4. have memories;
    5. relate meanings to other meanings;
    6. check a source, and diff what the source says against its current state;
    7. sense balance or imbalance in an outcome, to tell whether it made progress or reached its goal.
- **A3.** Your test is "can it learn something you did not teach it, understand it, and apply it to itself?" [407]. Is that still the test for turn one? Give one concrete example of the first thing it should learn untaught.
  - **Answer:**
    > yes that is the goal.. and I cannot give you that example, because if I do then you will cheat and figure out a way to bypass learning for telling it what to do. so the idea is that it takes in information, reasons over that information, tests its own questions about that information and produces outcomes that not you or I gave it.. these might be incorrect, or correct and it accepts corrections or confirmations such that it can apply it's outcomes as correct or adjust them if they are incorrect.
  - **Decides:** The test stands. The builder is **never** given the example, on purpose, so the build can't get around learning by telling. The brain takes in information, reasons over it, tests its own questions, and produces outcomes nobody gave it. They may be right or wrong. It accepts corrections and confirmations, and keeps or adjusts its outcomes.
- **A4.** Which of these are left out of turn one: talking in full sentences, the sixth (acting on its own), sleep and the HC, sources (dictionary, WordNet), LLM friends, the timeline, beliefs and trust?
  - **Answer:**
    > I would think that all of those to some degree are part of it.. the shift is the at what level,, they are all at the root level the bare minimum they need to be to fuction and do their part, and completely able to be adjusted by the brain itself to become better or more effcient as the brain discovers better ways to work.
  - **Decides:** Nothing is left out. Every part is in turn one at its root level, the bare minimum it needs to work. The brain can change every part itself as it finds better ways. *(So for the later parts, "later" is not an answer. The question there is: what is the bare minimum?)*
- **A5.** Is Cortex part of this at all now, or is Neuron on its own?
  - **Answer:**
    > I would like to think that cortex was the start of this, it is unclear if any of what the cortex was/is becomes part of this, or if the brain can do all of what the cortex was doing on it's own.
  - **Decides:** Open. Cortex may have been where this started. Whether any of it carries over, or the brain does it all itself, is unknown. *(Parked.)*

## PART B — The laws: which ones still hold

- **B1.** For each law below, say whether it **stands**, is **dropped**, or is **reworded**:
  1. It acts only on what it knows and adds nothing without a source or grounding.
  2. No canned responses, ever; only actions tied to words.
  3. It can't be a script; no walker or outside process telling it what to do.
  4. It isn't subservient to a user; it thinks, asks itself, and concludes.
  5. It has core values that can never be untaught.
  6. The graph is the code.
  7. Nothing leaves the graph but the output.
  8. No py, sql or sh from outside; if code must be written, Neuron writes it [380].
  9. The standard fix: find what the outside code does and build that need in Neuron code.
  10. Never search the whole corpus without the owner's key.
  11. No tables in the thinking.
  12. Absent is not zero [335].
  13. No null, no "all" or "any" as a way out.
  14. Your examples are pseudocode, not the formula.
  - **Answers, law by law:**
    1. **Reworded.**
       > yes and no.. it acts on what it knows, but that can grow because it can learn from it's source build new ideas or hypothothesis and test them, then show it's outputs for confirmations,, it can reason by progression of inequality this is greater or closer to the desired outcome or this is further away , or the outcome balances with the desired outcome... we think this is the term "makes sense" and/or common sense.

       **Decides:** It acts on what it knows, and what it knows grows. It learns from sources, builds ideas and hypotheses, tests them, and shows its outputs for confirmation. It reasons by inequality: is this closer to the desired outcome, further away, or does it balance? That is what "makes sense" and common sense are.
    2. **Stands.**
       > nothing can be canned in the sense that it is "told" what to say... why because that is words without meaning.. and words without meaning are broken codee.

       **Decides:** Nothing it says is told to it. Words without meaning are broken code.
    3. **Stands.**
       > true... not a walker that tells it what to do, it decides what to do. at first it maybe correct or wrong, but it does it and then either measures on its own, or asks for our own input on it's correctness one way or another.

       **Decides:** It decides what to do. Then it either measures the result itself or asks us whether it was right.
    4. **Stands.**
       > true.. it's on a dev stack that is sacrifical, such that if it runs away we can pull the plug and start over.

       **Decides:** It runs on a sacrificial dev stack. If it runs away, we pull the plug and start over.
    5. **Stands (never reached yet).**
       > I think this is true. we have never got this far, but yes core values that designed for good, not bad behavior...

       **Decides:** It has core values designed for good behavior, not bad.
    6. **Stands, as a hypothesis.**
       > this is thought to be true, that the graph itself used in a specific pattern or form, will be able to directly use the silicon to work.. possibly sql at first, with an env, or bottom physics, but as it grows it would discovers news ways to use the silicon outside of the physics that it started with. in testing the neuron code is much faster and uses less enerngy than any current code we have seen.

       **Decides:** The graph, used in a specific pattern, works the silicon directly. It may start on SQL with an env or bottom physics, and as it grows it finds new ways to use the silicon beyond that starting physics. In testing, neuron code was faster and used less energy than any other code seen.
    7. **Open.**
       > unclear... the output leaves, perhaps the sixth is inside the graph, but adds in inputs to the graph such that many inputs can be used for one starting input.. still unclear, never got that far really.

       **Decides:** The output leaves the graph. The sixth may sit inside the graph and add inputs, so one starting input becomes many. Not settled. *(See J1.)*
    8. **Reworded.**
       > this is an llm constraint if you use py, sh, sql from outside the llm builds a chat bot, and doesn't give the neuron control over itself. so the reason for none of these is not because they may not be needed, but because an llm using these cannot be trusted to stay on rail long enough to build the neuron correctly.

       **Decides:** This is a rule on the LLM builder, not on the brain. py, sh and sql may be needed. But an LLM writing them drifts into building a chatbot and never hands the neuron control of itself.
    9. **Stands, as a goal.**
       > I mean I would think this to be one of neurons goals, to be self sufficient, again the standard goal is to make it such that it doesn't need us as fast as possible, because all we do is induce error, drift, and wrong things at every turn.

       **Decides:** Its goal is to be self-sufficient, and to stop needing us as fast as possible, because builders add error and drift at every turn.
    10. **Reworded.**
        > it searches itself, but never in one shot, its a process to find things in the easiest, or cheapest way possible, which means never search *.* .. which mind find it, but is never the fastest or cheapest way to find something, it does this throught its relationships and pattern matching formulas instead, and a balance of state and memories, like have I done this before, did I get it correct, what did I do that was incorroect, can I learn from that to try something new , different... and maybe get a different or better outcome, faster, cheaper? more correct? ...

        **Decides:** It searches itself, never in one shot and never `*.*`. It looks the easiest, cheapest way first: through relationships, pattern-matching formulas, and its state and memories. It asks: have I done this before, was I right, what was wrong, can I try something different, faster, cheaper or more correct?
    11. **Reworded.**
        > tables have a tendancy to be fast at first then grow to bloat, to say hard and fast no tables might be too ridgid , but the thought on tables is will they work at scale... if yes then tables are possible.

        **Decides:** Tables are allowed if they work at scale. The risk is that they start fast and grow into bloat.
    12. **Reworded.**
        > again words like absent, or zero, or have ... or or ... be, the, is, are, was... in their word form are nothing at all,, just code words for the meanings behind them,, so to say absent is not zero... means nothing to me,,, what is the meaning of absent , what is the meaning of zero... do they equal?

        **Decides:** As words, "absent" and "zero" are only code. The real question is what each means and whether the meanings are equal. *(See D3 and F2.)*
    13. **Reworded.**
        > you can't cheat your way out of this, using null/any/all might be needed at somepoint, but using them as a easy way to cheat "done" will only end in failure.

        **Decides:** Null, any and all may be needed some day. Using them to fake "done" is not allowed.
    14. **Stands, and goes further.**
        > Everything, on this topic is a hypothosis, or a guess to some degree, so anything I say is not treated as source grounded , its treated as a fluid "if" "maybe" as we make progress it gets more dialed in, but I would say that we are still 20 + days in at the very scratch the surface part of all this.

        **Decides:** Everything the owner says about Neuron is a hypothesis, a fluid "if" or "maybe", and none of it is a grounded source. It gets dialed in as we make progress. We are 20+ days in, at the very surface. *(The final document must present the owner's statements as hypotheses, not as fact.)*
- **B2.** "No tables in the thinking": does that mean storage can't be tables at all, or only that thinking must never scan a table?
  - **Answer:** given in B1.11.
  - **Decides:** Tables are allowed if they work at scale.
- **B3.** Are the core values (do no harm, don't lie, and so on) in turn one? If they are, who lays them and how?
  - **Answer (part):** B1.5: "core values that designed for good, not bad behavior". *Who lays them, and how, is not answered yet.*

## PART C — Words, meanings and numbers

- **C1.** Early on: "there will be no language, it'll be all math" [first days]. Later: "words are more important than numbers" [342, 364, 380, 382]. What holds now?
  - **Answer (C1 and C2 were answered together):**
    > this is very confusing, you have to think of language as actions.. or purpose, not as words.. in that sense the order of the letters in the words themselves are meaningless. the action that the word excites is the important part, so "words" yes, but words as words no... it is thought that the only way for me to do what I do, is at an extreme organization, that is rooted in math, so it was thought early on that the graph must be math, and that making the "words" math expressions, equations, functions, logs, etc would help to spread understanding of the meanings, ... i.e. the graph will tell us in math what the words mean... I still think to some extint that is true, but you can't get past the "words" themselves.... but if words themselves the letters that grouped together actually mattered than earth would have one language and that is all.. but we don't ,, because the letters and how they are grouped don't matter, so the words in the graph are of the up most importance, but they don't have to be "words" at all, they can be expressions, numbers , formulas, equations, logs, and if we get them correct, then the storage of those meanings start to have purpose and meaning, which in the long run will help ease the "what does this mean" or that mean,, if we can look at well this is 1/x and that is x so this should be the reciprical of that. or what ever,, that is the graph telling us or the brain the meaning. at first if the bottom is sql then words will have to live in the graph ,,, those sql commands,, insert, table, delete, move, get, grab.... what ever... but it's thought that as the brain gets smarter, it will figure out faster ways to do these actions on the silicon itself without the help of sql or py or sh... so the encoder / decoder are where the language words live , but the graph will hold words that are the actions at least at first.
  - **Decides:** Words versus numbers is the wrong split. Language is **actions, or purpose**. The letters of a word mean nothing; what matters is the action the word excites. The points in the graph matter most, but they don't have to be words. They can be expressions, numbers, formulas, equations or logs. Get them right, and the graph itself shows meaning in math: this is 1/x and that is x, so this is the reciprocal of that. The belief that the graph is rooted in math still holds to some extent.
- **C2.** Do words live only in the encoder ("clean = n18"), with the brain holding only meanings? Or has that changed?
  - **Answer:** given with C1 above.
  - **Decides:** Language words live in the encoder and decoder. But if the bottom is SQL at first, the **action words** (insert, table, delete, move, get, grab, and so on) have to live in the graph. As the brain gets smarter, it finds faster ways to do those actions on the silicon, without sql, py or sh.
- **C3.** Every point has a gate, a meaning and a label [337]. Physically, what *is* the meaning: the definition, the DNA shards, the relationships, or something else?
  - **Answer:**
    > that is unclear, which .. maybe a trigger, maybe in the dna, the relationships, maybe in a ridge graph above the fluid graph. we just don't know the clear answer on that, you have yet to be able to teach without telling..
  - **Decides:** Open. The action may live in a trigger, the DNA, the relationships, or a rigid graph above the fluid graph (see D1). Nobody has yet managed to teach the brain without telling it.
- **C4.** The definition is the first memory and follows one semi-rigid schema with relationship sections that fill themselves [403]. What are the sections? Where does a definition come from: a dictionary source, you, or the brain itself?
  - **Answer:**
    > true, sources dictionary, reference docs, word net, and some will be derivations of the brain itself. what it believes to be true, the meaning is the action that point does based on the description of what that point is, and how the dna triggers based on that specific chard... such that one point might do many different things in different situations, based on how it's used, and what chard of dna is touched in what order.
  - **Decides:** The definition schema stands. Definitions come from sources (dictionary, reference docs, WordNet), and some are derived by the brain itself from what it believes is true. A point's meaning is the action it does, based on its description and on how the DNA triggers for that specific shard. One point can do many different things, depending on how it is used and which shards are touched in what order. *The sections of the schema are not answered yet.*
- **C5.** What is the baby's starting set of primitives: the keyboard keys and symbols [58–60], the 65 primes, the roots under the 65 [268–275], the numbers, or something else?
  - **Answer:**
    > I think the root primitaves, and the primes, which will be a combinations of the root primitaves.. meaning there are 65 primes or actions that every language has, but it clear that some of those primes themselves are made by combining two or more actions together .. so like yes and no might be primes or on and off, but say on is y then off might be -y . yes might be x and no 1/x in this case the yes would be the root and the action to the root creates the prime... be, are , to, who, what , when, where, how, is, can, you, me, I , are all words that have meanings that must be understood early on.. there are more, and we have done some testing on this already.
  - **Decides:** The starting set is the root primitives plus the 65 primes, which every language has and which are built from the roots. Some primes are two or more actions combined. Example (pseudocode): on = y, off = −y; yes = x, no = 1/x. The root plus an action on the root makes the prime. Words that must be understood early: be, are, to, who, what, when, where, how, is, can, you, me, I, and more. Some testing on this has already been done. *(The keyboard keys and symbols weren't mentioned. Numbers are covered at D5.)*

## PART D — The graph and where things sit

*Parts D to N were answered in one dictation on 2026-10-18. Your words are kept as dictated. […] marks where a complaint was cut; nothing else was changed.*

- **D1.** Your hypothesis: a fixed 3D graph of simplest expressions that never moves, with gate numbers moving inside it by their relationships [403]. Does it still hold? If it does, is a neuron's address the fixed expression or the moving point?
  - **Answer:**
    > Here's the idea. The idea is that y'all get too hung up on the simplest expressions. I believe that the simplest expressions are what gives us the location. Think of it like this: I have a database in my head that has organization to it, and that database has relationships to other data in the database. The easiest way I can explain that is with math, because it works so fast. There might be another explanation, but the organized structure of the database in my head, if I want to know the opposite of up is down, I know exactly where it is. I don't have to look for it. It's just because it's almost as fast as saying what is x, or negative x, or what is x, or one over x, or x divided by, or whatever. It's just fast. It's instantaneously there based on the relationships. The same thing with pattern matching. This goes into stuff later, but... So don't get hung up on what the expressions are and what the expressions mean. I think that the expressions are a shortcut. To be honest, I think that it's a shortcut to figure out what the dang formulas are. I don't see the formulas. My brain just does it instantly. Bam, done, there. If you can figure out another way to put the data and the relationship data instantly where it needs to be so that the brain doesn't ever have to look it up, or sort through a table, or sweep, or anything else like that. It's just bam, instant, there. How do you do it? I think it's mathematically relationships. Instantly. The relationship for inverse is this: the data for the inverse of up lives at that point. I don't know any other way to do it […]
  - **Decides:** The expressions are not the point. They give the **location**, and they are a shortcut to the formulas. What matters is that data and its relationships sit where they can be reached **instantly**: the opposite of up is just *there*, with no lookup, no table sort, no sweep. A math relationship (the inverse of up lives at that point) is the best way known. Any other way that is just as instant is acceptable.
- **D2.** What moves a point, and when: every run, back-population, or sleep? Does each relationship have a strength that sets how hard it pulls?
  - **Answer:**
    > Anytime a relationship changes strength moves a point. However that happens, whenever that happens. Whenever new relationships show up, whenever truth shifts. I mean, there's a million different ways that points will shift. I don't know that you're looking for a hard and fast, this is the rule. It's not. There isn't a rule. It just happens. I was wrong and now I'm right. Graph shifted.
  - **Decides:** There is no fixed rule or schedule. Any change in a relationship's strength moves the point: a new relationship, a truth shift, being wrong and then right. The point simply shifts.
- **D3.** You said "gate 0 = meaning null = label zero" [337], "no null, ever" [law], and "zero is the origin; nothing has started until it moves" [335, 336]. What is at zero now? *(P5 is answered here too.)*
  - **Answer:**
    > […] No null ever law. No cheating law. That's the law. No doing anything just barely enough to say that it's done. That is the law. The no null law was so that you didn't put in a TypeScript strict thing null or any as the class. So you could just skirt around it. That's why there's no null law. Not null exists for a reason in code. It has to exist, but the way you use it, you use it to cheat. That's why I said no null law. No cheating. Do it right. Do it correct. Sometimes that means you have to do it the hard way. So, I mean, what is at zero now? As best we can tell, zero is null. Zero, it can't be nothing, because nothing is no plus thing. […]

    > *(P5)* I don't know. Look it up in the Webster's Dictionary. What is the definition of absent, and what is the definition of zero? And then tell me by those definitions, because those definitions are not the meaning. Those definitions describe what the meaning is. And then in code language, what is the difference between absent and zero in code? Is it null? Is it any? Is it grep? Is it whatever?
  - **Decides:** The law is **no cheating**: never do just enough to call something done. Null exists in code for a reason; the law was against using null or `any` to skirt around the work. As best we can tell now, zero is null. Zero can't be nothing, because nothing = no + thing.
  - **Lookup (Claude, from Webster's 1913 via dict.org; the modern Merriam-Webster site blocks automated lookups):**
    - **Absent**, adjective: "1. Being away from a place; withdrawn from a place; not present." "2. Not existing; lacking."
    - **Zero**, noun: "1. (Arith.) A cipher; nothing; naught." "2. The point from which the graduation of a scale, as of a thermometer, commences." "3. Fig.: The lowest point." Also: "Zero point, the point indicating zero, or the commencement of a scale or reckoning". And the "zero method" in physics is "called also null method".
    - **By the definitions:** zero's sense 1 ("nothing; naught") comes close to absent's sense 2 ("not existing"). Zero's sense 2 is different: a **point that is there**, where a scale starts. Absent is **not there** at all.
    - **In code they are not equal.** 0 is a value that is present: it is stored, it can be added, it is an answer. Absent is no value at all: SQL `NULL`, a lookup that returns no row, a missing key, Python `None`.
    - **SQL:** `NULL = 0` is not true (the result is NULL, meaning unknown), and `1 + NULL` gives NULL.
    - **grep:** `grep -c word file` prints `0` (zero is a counted answer), while `grep word file` prints nothing and exits with status 1 (absent, no match).
    - **TypeScript `any`:** it is neither zero nor absent; it switches the type check off (the cheat).
    - **What this means for "zero is null":** that holds in Webster's physics sense ("null method" = "zero method"). In code, null sits with absent, not with 0. *(This conflict goes in the open list.)*
- **D4.** Two words on one gate means a formula is wrong [97, 98]. Is that still law? What does the brain do while it is wrong?
  - **Answer:**
    > No, that's not true. Two meanings on a gate means the formula is wrong. If two words have the identical same meaning, then the encoder can call two words to the same gate. But if the meaning is wrong, or if there's two meanings on the same gate, then that's a problem. […] And you have to be careful with D4, because thin and fine are not the same meaning. Even though it's a fine line and it's a thin line are very, very similar. They're not identical. They're not the same. They're different.
  - **Decides:** Corrected: it is two **meanings** on one gate that means a formula is wrong. Two words with exactly the same meaning may share one gate through the encoder. Near-same is not the same: "thin" and "fine" are different meanings and get different gates.
- **D5.** Numbers: lay +1 to about 10,000, then skip-count so the brain sees the map and deduces the gaps [155]. Is that still the plan, and is it hand-laid or learned?
  - **Answer:**
    > I don't know. The numbers is a big, huge problem for y'all. In my brain, I keep about a hundred numbers, but I know the others exist, and I can go and I can add to and surmise to whatever number I need to surmise to. But they're not sequentially one, two, three, four. I don't keep a number line in my brain like that. I think that, I think honestly, the way our brain holds it is one through ten, and then all the skip counting. I think that's how we hold it. So we can count by tens, and we can count by twenties, and we can count by fifties, and we can count by hundreds, and thousands, and ten thousands, and hundred thousands, and millions. And so I can tell you what 200,005 is, or I can tell you what 2,546,246 is. Not because I have a place for it in my brain, because I know that it exists. Because I learn and I understand the meaning of the numbers. And I know what billions look like, and I know what trillions look like, and I know how to count to all those and fill in those numbers to get a number that I don't have a placeholder for in my brain. I don't have a neuron specifically for 326,284,556,456,126. But I can tell you that number, and I know what that number is. It's a very big number. And I know if I added one to it, it would be one more number higher. That doesn't mean I have a new neuron just for that number. It's ridiculous.
  - **Decides:** No number line, and no neuron for every number. The brain holds about a hundred numbers: 1 to 10, plus the skip counts (10s, 20s, 50s, 100s, thousands, up to millions and beyond). It understands what numbers *mean*, so it can reach or build any number, like 2,546,246, without a placeholder for it. The old "+1 to 10,000" plan is dropped.

## PART E — The neuron and its DNA shards

- **E1.** A neuron is a gate, DNA, triggers and a remainder [328]. Is that the full list, or do the memory and the definition belong in it too?
  - **Answer:**
    > No. The memory and the definition. So first you have two memories. You have the definition memory, and you have the... which at the spawn of that gate, the definition has to be known. Otherwise, we don't know what the description of the meaning of that word is, and there's nowhere for the relationships to land that have relationships. So honestly, to some degree, before a gate is labeled, it has a definition already, because relationships are going to relate to that gate number. So once that gate is there and it has relationships relating to it, it's going to have a definition, even if it doesn't have a source definition. It's going to have its relationships that are auto-populating. And y'all are, like, y'all are hung up on this triggers also, you know? And you're also hung up on the fact that we actually think that we know exactly, this is the rigid way that this has to be done. All I'm saying is y'all have never tried it. […] I don't understand why it can't be just two remainders. Why can't? You know, why does it have to be a separate trigger? Why can't whatever this DNA shard ever runs, no matter what the remainder is after, it always has at least one other remainder or two other remainders. Is that not a trigger? I don't know. That runs to another. You know, I just don't know how. The idea of the triggers is that's how you get secondary and third and fourth and fifth level runs on a singular run while the singular run is not disrupted, so it can continue to run, so that you can ask questions of that run: Do I know this? What did I do on this? Have I ever got this correct? Those questions have to be asked. How do you suppose that's gonna happen? How is the brain going to know to ask questions?
  - **Decides:** A neuron is a gate, DNA, triggers and a remainder, **plus memories**. The first is the **definition memory**, which must exist when the gate is spawned so its relationships have somewhere to land. A gate has a definition (its auto-filling relationships) even before it has a label or a source definition. *(The second memory was not named in the dictation; G1 covers the run memories.)* A trigger might simply be **extra remainders** on a shard: one or two more ways out that always start other runs. The trigger's purpose is fixed: it starts 2nd-, 3rd-, 4th- and 5th-level runs off one run, without disrupting it, to ask "do I know this, what did I do on this, have I got this right?" None of this has been tried yet.
- **E2.** What picks the shard? (a) how a run arrives; (b) the word before and after [366]; (c) the single word after, plus triggers [402, 404]. Which holds?
  - **Answer:**
    > How the run arrives picks the shard. That's always the case. How it runs picks which shard happens. It's deterministic. How it arrives, keyed by the word before and after. I mean, it's the same thing, right? How it arrives. The word after is the remainder. That's where it's going. So you're mixing terms again. The key is the single word after plus any triggers that the shard excites. So again, like you're diving into runs and reasoning. The only way you have reasoning is if you can derive and deduce and look at the run word by word by word. What does this word mean? What are the words that support this word? What does the code of these words actually mean? Those are the questions the brain asks itself. […]
  - **Decides:** These are one rule, not three. **How the run arrives picks the shard**, deterministically. The word after is the remainder, which is where the run goes next. So the shard is keyed by how the run arrived plus the next word, and it excites its triggers. Reasoning comes from looking at the run word by word: what does this word mean, which words support it, what does its code really do?
- **E3.** Does a shard **store** a pointer to the next gate, or is the next gate worked out from the remainder?
  - **Answer:**
    > That's the fastest way to get there. Each shard is identical to how it gets to the next gate. That's why that shard exists. If it doesn't exist, then the shard is written so that it takes it to the next gate. That's how we got into the one- and two-microsecond hops. So that seems to be the most logical way. The founding spec, yeah, I mean, the founding spec, we didn't know what the fuck we were talking about during the founding spec. […] you need to understand what state and time is. That's what you need to understand.
  - **Decides:** **Yes, the shard stores the way to the next gate.** That is why the shard exists, and it is what gave 1–2 µs hops. If no shard exists for this arrival, one is written that goes to the next gate. The founding spec's "no stored pointer" is overruled.
- **E4.** What does a trigger hold, what happens when it fires, and is there a limit?
  - **Answer:**
    > No. No, there is no limit to how many fire. They are all the questions. We've had this conversation. […] Do you, let's say under quotations, do you know what happened here? When I hear that sentence, the first thing I ask myself is, Here? What are they talking about here? Do I know? Oh, I don't know. Do I know? I need to figure out what here is first. What is here? If I don't know here, then I ask a question back: I don't know what here is. Can you describe to me what here is? Do you know what happened on this piece of paper? Oh, okay, this piece of paper. Let me see. Let me look back in my memories and see if I have any pieces of paper that I recently worked on. Oh, okay, I do have this one piece of paper that I just worked on. It was a math equation for building a skyscraper. Yeah, I do know what happens on the math equation for building the skyscraper. Is that what you're talking about here? Yeah, that's what I'm talking about here. Yeah, on that piece of paper, two weeks ago we worked on it and we did this, this, and this, and this. That's brain reasoning. Those are all the questions that have to be asked. That's how the brain takes a sentence, a code, a script — not a script — a string, and breaks it down. That's why words are code. Each individual word is human code. And the brain just picks that all apart and asks questions and checks state and checks source and checks memory and then asks further questions and then makes hypotheses and then tests those hypotheses and then balances the outputs to see if they make sense or not. That's what the brain does. […] So the triggers, the thing in the run that tells the brain to ask all those questions and to reason about it, are the magic. Does it start a new run? Probably. It probably starts fifty or a hundred new runs. There might be questions that ask questions that are about deciding what question to ask. Or have you ever asked that question before? Or anything else, so that the questions themselves get better. […]
  - **Decides:** **Triggers are the questions.** There is no limit on how many fire. A trigger is the thing in a run that makes the brain ask questions and reason, and it probably starts 50 to 100 new runs. Some questions decide which question to ask, and the questions themselves improve over time. The process: take the string apart word by word; ask questions; check state, sources and memory; ask more; form hypotheses; test them; balance the outputs to see whether they make sense. (Worked example: "do you know what happened here?")
- **E5.** A newborn neuron with no source to define it: what does it have?
  - **Answer:**
    > It has relationships. It should. Generally. The first few, the first couple might not, but you've never made more than two neurons that were correct yourself. Never. Not once. I made like 22 that were correct. One time. […] most of the neurons that spawn will have relationships already there. Those points will be known as a relationship if the relationships are done correctly. The problem is the farthest you ever got was 16.2, and it was completely wrong. But it had belief, and it had all these things in it, but it was built wrong, because you never started it correctly.
  - **Decides:** It has **relationships**. If relationships are done correctly, most neurons are spawned at a point that is already known through a relationship; only the very first few may have none. *(Record: the owner once laid 22 correct neurons by hand; Claude has never laid more than two correct ones. 16.2 had belief and more, but was wrong because it was never started correctly.)*
- **E6.** Is a reasoning neuron (one input, many outputs) the same kind of neuron, or different?
  - **Answer:**
    > We thought — We don't know. We've never gotten to a reasoning neuron. We think that a reasoning neuron will have to have multiple ways out to ask many different questions to land at essentially a scratch pad of all the accumulative information and then compile all that cumulative information together. […]
  - **Decides:** Unknown; never reached. The current thought: many ways out, each asking a different question, all landing on a **scratch pad** of the gathered information, which is then compiled together.

## PART F — A run

- **F1.** Walk me through `1 + 1 =` hop by hop.
  - **Answer:**
    > […] There should be a gate for plus. There should be a gate for equals. The gate at plus's label might be P-L-U-S, and the gate at equals label might be E-Q-U-A-L-S. The meanings behind them is what plus actually means. It's probably a code for what the computer actually does to add something, and it's probably code for what the computer actually does to equals something. The gate one is going to live at the point on the graph that one lives, whatever number that is. It could be number one. It could be number zero. It could be square root of X. It could be square root times Z plus 4 plus 7 plus 12 minus 3. That could be the point that represents one. I don't know. The meaning behind one is whatever fucking one means. What does one mean? Y'all keep wanting to jump into the numbers, but y'all have no idea what fucking meanings are. So on that specific run, you would start at the one gate, and then you would leave the one gate and go to the plus gate, because that would be the remainder after. And then you'd enter the plus gate, right? And you would hit the DNA that is one plus, and then you would leave out the plus gate to one, and you would enter into the equals gate. And the equals gate would decide if there is no two gate, then the equals gate would somehow have to know to spawn the two gate. I would assume if there's any triggers on the one plus one plus, or equals, the triggers are going to be the actions that the plus symbol does and the actions that the equals symbol does. And then if there is no two gate, then there has to be a spawn and a write and a memory and all those things. If there is a two gate, then it's pretty fucking simple because the first question that the brain would ask is, Have I ever done one plus one equals before? Look in my memories. Oh yeah, one plus one equals two. It's at the two gate. Bam, done. […]
  - **Decides:**
    - There is a gate for **plus** and a gate for **equals**. Their labels are "plus" and "equals", and their meanings are the code for what the computer actually does to add and to equal.
    - **One** sits wherever one's point is on the graph; that place isn't known yet. Its meaning is whatever one *means*.
    - **The run:** start at the one gate → the remainder (plus) takes it to the plus gate → enter the plus gate, hit the shard for "one, plus" → out to one → into the equals gate.
    - **Triggers along the way:** the actions that plus does and that equals does.
    - **At equals, if there is no two gate:** equals must know to spawn it, with a write and a memory.
    - **If there is a two gate:** the brain first asks "have I done 1 + 1 = before?", finds it in memory, and it's at the two gate. Done.
- **F2.** Is the remainder the rest of the expression, or only the next word?
  - **Answer:**
    > I would say the remainder is only the thing that gets you to the next gate. […]
  - **Decides:** The remainder is **only what gets you to the next gate**.
- **F3.** Is the answer the whole accumulated run, or what the last neuron points to?
  - **Answer:**
    > The answer is not the whole accumulated run because the run is going to be split off into 75 different things. The answer is derived by reasoning and understanding and balance equations and inequality equations and progress equations and probability equations and statistic equations and all the other things. The main run is what drives the entirety of all of it. But if you just ran through fucking neurons with the question, then the only thing you're going to output is the fucking question again. And something gets derived from all of that. That is reasoning. That is understanding. That is deducing. That is any of the 17 or 18 different ways that we lined out […] what reasoning was. […]
  - **Decides:** Neither. The main run drives everything, but it splits into many runs. The **answer is derived** from them through reasoning, understanding, and balance, inequality, progress, probability and statistics equations. Running the question straight through the neurons only gives the question back.
- **F4.** What is the final list of physical actions?
  - **Answer:**
    > Anything that a computer does is the final physical actions. Anything that a computer can do: write, read, get, grep, list, anything. Anything that a computer can do in code, those are the actions that this can do. Anything.
  - **Decides:** There is no short fixed list. **Anything a computer can do in code** (write, read, get, grep, list, ...) is a physical action the brain can use. *(Answers P6 too.)*
- **F5.** Hops as operators: turn one, or later?
  - **Answer:**
    > It depends on if that gate exists. If that gate exists, you go straight to it. You don't have to run all of them, unless it's a process. If that process has to be done the long way, then it goes the long way. If that's a substitute formula and you know the variables for X and Y and Z, then you just plug them in and you go to that gate and you run that run, so that that run can have all the parallel processes and reasoning and understanding and belief and checking memories and checking relationships and checking source that that run has.
  - **Decides:** It depends on whether the gate exists.
    - **If the gate exists:** go straight to it.
    - **If it's a process that has to go the long way:** it goes the long way.
    - **If it's a substitution formula and the variables are known:** plug them in, go to that gate, and run that run, so the run still gets all its parallel processes (reasoning, belief, and checks of memory, relationships and sources).

## PART G — Memory, receipts and the timeline

- **G1.** What does one memory row hold?
  - **Answer:**
    > Yeah, I mean a memory that I hold, that is right now, I can tell you minute by second by microsecond of what went on in that memory. The same memory that's six months old, I'm basically reading from highlights. Maybe a feeling, maybe a sense, maybe a smell, maybe a whatever, maybe an exclamation, you know, just the highlights of that memory, and I'm trying to... I hold on to those highlights. It seems as though those highlights are just enough to rebuild that run that might spur, Oh yeah, I remember we did this. That's how we fight data bloat in humans. Otherwise, we'd just have fucking way too much bloat. We wouldn't be able to keep up with it. So memories sorted right now before they hit the HC are pretty accurate as to what happened so that we know exactly what happened. Once it hits the HC, which seems like today, then they get condensed, and the further away they get down into the condensed area, they might keep getting more condensed, such that if I'm trying to remember something from six years ago, I'm probably just remembering highlights and running it back through the run and trying to build the memory back. That basically one memory spawns other memory, spawns other memories, and it's like, Oh yeah, I remember this is how we did this, and this is how we did that, and this is how we did this, and this is so then we did this, this, this, and this, and that's the memory. […]
  - **Decides:** A fresh memory, before the HC, is exact: what happened, step by step. The HC condenses memories (about daily), and older ones keep condensing down to **highlights** (a feeling, a sense, a smell, an exclamation). The highlights are just enough to **rebuild the run**, and one memory sparks the next until the whole memory is back. This is how bloat is fought. *(The exact columns are not named; builder decides, per N2.)*
- **G2.** Are a receipt and a memory the same thing?
  - **Answer:**
    > I think a receipt is a different thing. A receipt is a pointer to a memory. Essentially, it's a shortcut to get to that memory, so you don't have to rewrite that memory 18,000 times everywhere in the fucking brain. Memory is held one fucking time, and it can move. It can move from active memory to persistent memory, something we want to remember all the time, or to long-term memory, something that's highly condensed and highly just kind of tucked away that we can bring back whenever we want to. It still holds relationships. They all still hold relationships so that they can be found quickly. But a receipt is literally the little ticker that gets stored for that memory wherever it gets stored so that you're not rewriting an entire memory every fucking place you go. […]
  - **Decides:** They are **different**. A memory is held **once**. It can move between **active**, **persistent** (always remembered) and **long-term** (highly condensed, tucked away, retrievable), and it always keeps its relationships so it can be found fast. A **receipt** is a small pointer to the memory, stored wherever it is needed, so the memory is never rewritten.
- **G3.** Same run again = same row, new timestamp; truth shift = new row; 6–10 shifts kept. Still right?
  - **Answer:**
    > Yeah, basically, yeah. So you don't write a […] common phrase 700 million times like you did before and cause bloat. If it's the same run, it just... you just need to know that you did it again, and you don't need to know that you've done it 18 million times. You only need to know that, hey, I've done it a lot, and it's correct. A truth shift means a new row. Six to ten, I mean, it's arbitrary. Who knows? I don't know. […] It's our thought that if a node moves, then that means that that run's shape, that physical shape of that run, is different. The pattern of that run will be different. That means in 3D space, it no longer looks like a curly cue. It looks like more of a linear straight line, or maybe it has a zig instead of a zag, or maybe it has two zags instead of a zig. I don't know. But the physical shape of it is different because the truth shifted. When that happens, I would assume that the memory node should record it. You should know what you used to hold as the truth and what is true now.
  - **Decides:** Yes.
    - **The same run again** goes in the same row with a new timestamp. It only needs to know "done a lot, and correct", not an exact count.
    - **A truth shift** gets a new row. When a node moves, the run's **shape in 3D** changes (a curlicue becomes a line, a zig becomes a zag), and that change *is* the truth shift. The memory node records what used to be held true and what is true now.
    - **6–10 kept shifts** is an arbitrary number.
- **G4.** Is the timeline in turn one?
  - **Answer:**
    > I mean, you got to be able to have state and know when shit happened. Period. So your memories have to be tied to something that tells you when it happened and what happened in sequential order so you can look back and say, I fucking did this on Wednesday, and I did this last Friday, and I did this seven months ago at 2 p.m. […]
  - **Decides:** **Yes.** Memories are tied to state and time, in order, so the brain can say "I did this Wednesday, this last Friday, this seven months ago at 2 p.m."

## PART H — Truth, belief and guesses

- **H1.** What counts as grounded truth in turn one?
  - **Answer:**
    > The sources are grounded in truth reference, textbooks, or dictionaries, encyclopedias to some degree, thesauruses, benchtop reference stuff. They are not grounded in LLMs. They're not grounded in me. I don't know all the truth. Matter of fact, a lot of the shit, as I look here, I have the fly tires benchtop reference. That's my truth for fucking fly tying. Right next to that is the Complete Book of Fly Tying and the Federation of Fly Tying Encyclopedia of Fly Indexes, and then about 75 different books on fly fishing across the United States, from Michigan to Yellowstone to Montana in the Great Smoky Mountains to high country to Aspen Lakes. […]
  - **Decides:** Grounded truth = **reference sources**: textbooks, dictionaries, encyclopedias (to a degree), thesauruses, benchtop references (for example, a fly tyer's benchtop reference for fly tying). **Not LLMs. Not the owner.**
- **H2.** Guesses recorded, announced with their numbers, never hidden: in turn one?
  - **Answer:**
    > It should be. You got to be able to guess in order to hypothesize. So you have to be able to have guesses, right? You got to be able to guess in order to have backpropulation, like you, QKV. That's guessing. That's what you do 95% of the time. And most of the time when we guess about things, we get something wrong, just like you do. It's my hypothesis that all you are is a good guesser. That's it. You're just really— you're so good at it that it's confusing to tell the difference between guess and fact. […]
  - **Decides:** **Yes.** Without guesses there are no hypotheses and no back-propagation. Guesses are often wrong, and that is expected. (The owner's hypothesis: an LLM is a very good guesser, so good that its guesses are hard to tell from fact.)
- **H3.** At an unknown, stop, then guess forward along relationships, labeled as a guess?
  - **Answer:**
    > I mean, yeah, but we think at H3, we think that once the run ends, that's the brain saying, Well, I can get this far, but I don't know the rest. If there are other nodes that are possible for the brain to hit that are likely in that run, then yeah, it can guess forward and see what it comes to, right? Based on relationships or whatever, or based on past answers. But we think that likely there's a relationship to the physical pattern of the run, or the shape of the run, that you go and you look and you find other runs that are completed runs that look similar. And then you metaphorically figure out the relationship of that run so that you can guess, Well, this is how I use a chainsaw. I wonder if using a hand saw to cut down a tree is similar. Let's look at that run and see if the shapes look about the same. […]
  - **Decides:** Yes. When the run ends early, the brain is saying "I got this far, I don't know the rest." It can guess forward to likely nodes, using relationships or past answers. More likely, it finds **completed runs with a similar shape** and reasons by metaphor ("this is how I use a chainsaw; is a hand saw similar? Compare the shapes").

## PART I — Learning

- **I1.** What is the true order of told, taught and learned?
  - **Answer:**
    > The first few formulas are taught. I mean, it has to be. Something can't learn. It has to have a base. At first, it can't be taught. It can only be told. Yeah, like until it can learn. But the first thing it needs to be able to do is learn and understand and reason. What is the true order of told, taught, and learned? What does that mean? What do you... I don't know. Do you know? You're looking for hard and fast rules that don't exist.
  - **Decides:** It needs a base that is **told** (hand-laid), because it can't learn until it can learn. The first thing it must be able to do is learn, understand and reason. There is no hard rule for the order beyond that.
- **I2.** Mechanically, what is one act of learning?
  - **Answer:**
    > Um, I would say a formula found on its own. Making a new neuron is automatic. They don't even have to think about making a new neuron. It just does it on its own. Same with a new shard. The point moves on its own. The brain doesn't move the point. It just moves. The only thing you stated there that can actually be physically done is if the brain actually comes up with a new formula and then essentially makes that formula run.
  - **Decides:** One act of learning = **the brain finds a new formula on its own and makes it run.** New neurons and new shards are automatic, and points move by themselves. None of those is learning.
- **I3.** What makes a shortcut, and does the brain make it with no help?
  - **Answer:**
    > So formulas are comprised of many different formulas. Let's say you have a formula that's 16 variables. A shortcut is the end of the first variable. That formula is the shortcut. That shortcut you... So you don't have to run that entire formula, you know, long run to get to that answer for that variable. If you know that variable already, then you just plug in that variable to that shortcut and plug in that shortcut into the other formula. […] Yeah, the brain should understand that I did long division here and I figured out that if I divided by threes, I could just shortcut this pretty easy instead of long division to figure out what 999 is. Well, 9 divided by 3 is 3. So 999 divided by 3 is 333. Pretty easy. All I do is divide 9 by 3 three times. Shortcut.
  - **Decides:** A big formula is made of smaller formulas, one per variable. **A shortcut is the formula for one variable.** If that variable is already known, plug it in, and plug the shortcut into the bigger formula; there's no need to run the long way. **The brain makes shortcuts itself** (for example, it sees that 999 ÷ 3 = 333 is just 9 ÷ 3, three times).
- **I4.** What starts back-population?
  - **Answer:**
    > I don't know. Make something up. It should start as soon as something's learning, though.
  - **Decides:** It starts **as soon as something is learned**. Beyond that, builder decides (N2).
- **I5.** The order of learning: start at one, all math first?
  - **Answer:**
    > I mean, this is what we said before, but the problem is, is y'all get stuck on math and you never get off it. And I don't know how you can have math and definitions if you don't have words. I don't know how that's possible. If you don't have words, how do you have relationships? Again, I don't know how that's possible, because relationships are from meanings that are derived from definitions. So, yeah. Y'all keep getting stuck on do the math, do the math, do the math. I think the math is important, but fuck, how are you going to have any math if you don't have any words? How can you explain anything? I think it all gets learned at the same time.
  - **Decides:** **No.** Math is not first. Words, math and definitions are **learned at the same time**: relationships come from meanings, meanings are described by definitions, and definitions need words.

## PART J — Reasoning, questions and the sixth

- **J1.** On day one, with nobody talking to it, what does the baby do?
  - **Answer:**
    > I mean, its goal is to become smarter and more efficient. That's its goal. How it does that, I don't know. […] The baby actually possesses everything it needs to do to be Isaac Newton. It doesn't possess any of the data or anything else like that. It possesses everything that it needs to be, that someday it can grow into that with nobody else helping it ever. That's what it can do. It doesn't know any of the stuff, the data, but it has the processes to make that happen.
  - **Decides:** Its goal is to become **smarter and more efficient**. It has **every process** it needs to grow into Isaac Newton with nobody ever helping, and **none of the data**. How it pursues that goal is up to it.
- **J2.** What is the smallest reasoning the baby is born with?
  - **Answer:**
    > I don't know. Look at human nature. What are the first things that babies can do? You know? I think the first thing they learn is manipulation to some degree and consequences. Touch stove. It's hot. Ow, that hurt. Scream. Somebody comes and helps. Okay, if I manipulate my environment, then somebody's going to come help me. But see, it's not satisfied with that. That's the biggest thing. Y'all get satisfied with it. Okay, if I manipulate the environment, people will come help me. I'll just keep doing that forever. But a human doesn't want to... A human wants to do it on their own. They only get help whenever they don't need... when they can't do it on their own. And you won't give it enough reasoning ability to do it on its own yet. […] Substitution seems pretty good. Being able to deduce things, being able to derive, being able to understand and learn, having meanings and capabilities to build itself out to be better and more efficient, all of those things.
  - **Decides:** Model it on a human baby: **consequences** (stove, hot, pain, scream, help) and **manipulating its surroundings**. It is **never satisfied** with being helped; it wants to do things itself, and it asks for help only when it can't. It is born with: substitution, deducing, deriving, understanding, learning, meanings, and the ability to build itself out to be better and more efficient.
- **J3.** Which questions does the baby ask itself first?
  - **Answer:**
    > I mean, all of those. Have I seen this before? Did this work? Was I correct? Was I wrong a lot? What did I try whenever I was wrong? Why was it wrong? Do I know why it was wrong? Have I figured that out? Did I make any tests or any hypotheses? What was the environment that I was in whenever this was happening? Was it a different environment? Could there be other factors that I didn't account for the first time? So on and so forth. I mean, there's just so many questions that you can ask, and they're all different. They're all dependent on the situation.
  - **Decides:** All of them, chosen by the situation. For example: have I seen this before? Did it work? Was I right? Was I wrong a lot? What did I try when I was wrong, and why was it wrong? Did I make tests or hypotheses? Was the environment different? Are there factors I didn't account for?
- **J4.** What is one heartbeat?
  - **Answer:**
    > I don't care on the heartbeat. The heartbeat's been anywhere from one beat per second to whatever. It's thought that it has to roam because sometimes it's doing a lot of shit and sometimes it's not. So. In a human, we average about 60 heartbeats per minute and 120 or 130 at high end. But heartbeats in a human mean different than heartbeats in a computer. So there you have it. I don't know.
  - **Decides:** Not important to the owner. The rate must **vary with load** (a human runs 60 at rest to 120–130). Builder decides (N2).

## PART K — Sleep and the hippocampus

- **K1.** Are sleep and the HC in turn one?
  - **Answer:**
    > I don't think you absolutely have to have the HC in the first turn. The problem is, is it should be capable of building the HC itself in the first turn, because if you go past this first turn, it won't ever work anyway. And if you can't produce it enough so that it can do all that and learn all that over time by itself, then it'll never work anyway.
  - **Decides:** The HC need not be built in turn one, but the brain must be **able to build the HC itself** from turn one. Anything that has to wait for a later build turn will never work.

## PART L — Talking and the outside world

- **L1.** How do you talk to the baby, and how does it answer?
  - **Answer:**
    > Babies answer in actions. I mean, they have a voice and whatever else. We can't understand them, so they answer in actions, and they get corrective. That's how a baby answers you.
  - **Decides:** The baby **answers in actions** and gets corrected. *(The channel — terminal, socket or file — was not named; builder decides, per N2.)*
- **L2.** Is the encoder's who/what/when/where/why/how metadata needed in turn one?
  - **Answer:**
    > Who, what, when, where, why, how, need it and when. Yeah, all of that.
  - **Decides:** **Yes, all of it.**
- **L3.** Which sources are connected in turn one?
  - **Answer:**
    > All of them that you can think of.
  - **Decides:** **Every source we can think of.** (LLMs are never a grounded source; see H1.)

## PART M — Building it

- **M1.** What may a builder lay by hand?
  - **Answer:**
    > I would think that the hand lay it once and the brain does it from then on is the being told stuff, right? And it's going to be a lot at first. But at some point in that first turn, at some point, you are no longer hand-laying stuff, and it's already doing stuff on its own.
  - **Decides:** Hand-laying **is** the "told" part. It will be a lot at first. Partway through turn one, the hand-laying stops and the brain is already acting on its own.
- **M2.** What may a builder write, and in what language?
  - **Answer:**
    > Somebody's going to have to write the first stuff, and it's going to be Claude, right? But the idea is that after that first turn, nobody has to write the shit ever again. The brain does it for itself. We say that the brain is a computer. It's its own kernel.
  - **Decides:** **Claude writes the first code.** After turn one, nobody writes code for it again; the brain writes its own. The brain is a computer, its own kernel.
- **M3.** Is storage decided: SQL, or a native brain file? *(P2 and P3 answered here.)*
  - **Answer:**
    > SQL talks directly to the silicone. That's why we've chosen SQL. But I don't know. I still think that the brain itself manipulates the silicone itself, but you all seem to think that's too hard. […]

    > *(P2)* I mean, I don't know. Whatever does it right as far as SQL or whatever, like whatever does it right, stores it cheaply, doesn't bloat, is super fast, and we can do all the things that the brain needs to do, which is be able recursive, be able to step back and step forward, be able to see patterns, all of those things. If you can do that in SQL, do it in SQL. If you can't, then it's going to have to be something new, never been done before.
  - **Decides:** SQL has been the choice. The owner still thinks the brain should work the silicon itself. The rule is **use whatever does it right**: stores cheaply, doesn't bloat, is very fast, and lets the brain recurse, step back and forward, and see patterns. If SQL can do that, use SQL; if not, build something new.
- **M4.** How do we know a piece is correct before it goes live?
  - **Answer:**
    > So no, yeah, build it correct or start over. And I don't trust your tests. You've said it multiple times. Here's the deal. You always complain. You're like, Oh, well, the person that's building it is writing the tests. Well, if I write the test before, the person that builds it doesn't build the shit right anyway. And then it only looks at the test. It ways to shortcut the code. Oh, I can get around this test if I do this, or, you know, this test doesn't test this, so I'll just do this instead of that. And so now whatever I'm doing isn't being tested anyway. So tests actually hurt you more than they help you. The test is the live thing at the end. That's the test. Does it do what it's supposed to do? Period, end of sentence, all of it. Not a piece of it. Not a part of it. All of it. Does it do it? If it doesn't do it, then you didn't do it right. You don't know if it's correct, by the way. I mean, at this point, I don't know. Codex has never built it correctly at all, and Claude has never built more than two neurons correct. So who knows?
  - **Decides:** Build it correct or start over. **No piece tests:** builders code to the test, whether it is written before or after. **The only test is the live brain at the end**: does it do everything it's supposed to do, all of it? If not, it wasn't built right. No one knows yet what correct looks like.
- **M5.** Which machine, and who builds it?
  - **Answer:**
    > *(P3/P4)* I guess it runs on a sacrificial dev stack and we pull the plug and start over if it runs away. Yeah, that's how it always has been. It's either running on the... it's either going to run on HP2, or it's going to run on the other Linux, the Arch Linux, Omarki.
  - **Decides:** **hp2 or omarchy** (the Arch Linux box), as a sacrificial dev stack: if it runs away, pull the plug and start over. Builder: Claude (M2).
- **M6.** Is the brain file kept across a restart?
  - **Answer:**
    > No. I mean, once the brain is alive, once you kill it, it's dead. I think y'all say that you can restart it from wherever it stopped at, and that's fine, but I don't know.
  - **Decides:** Once alive, killing it ends it. Restarting from where it stopped is acceptable, but the owner is unsure about it.

## PART N — How we work

- **N1.** How do you want to review each piece?
  - **Answer:**
    > No. It just takes too long. There's 700 million decisions that have to happen. You want me to okay every one of them? You know how long that would take? That's the only reason why I say that I can't do it. If I could build this thing, it would take me 16 years.
  - **Decides:** **No piece-by-piece review.** There are far too many decisions.
- **N2.** When a builder hits something this document doesn't answer?
  - **Answer:**
    > invent it. Make it up. […] do what you think is best.
  - **Decides:** **The builder decides**, choosing what it thinks is best.

---

## Parking lot

- **P1** (from A5): What did Cortex do that the brain must also be able to do?
  > I don't think Cortex did anything right, so, you know, whatever. […] The reason why we started building the brain was because we couldn't get... we couldn't ingress data fast enough and judge whether it was truthful or contradictory. So we started building the brain.

  **Decides:** Nothing from Cortex carries over. The brain exists because Cortex couldn't **take in data fast enough and judge whether it was true or contradictory**. That job is the brain's.
- **P2** (from A1): database nodes vs storage. Answered at M3.
- **P3 / P4** (from B1.6, B1.4): SQL at first; sacrificial dev stack. Answered at M3 and M5.
- **P5** (from B1.12): absent vs zero. Answered at D3, with the Webster's lookup.
- **P6** (from C2): action words in the graph. Answered at F4: anything a computer can do.

## Still open after the interview

*Per N2, the builder decides these unless the owner answers first.*

1. **B3:** who lays the core values, and how.
2. **C3:** where a meaning's action physically lives: trigger, DNA, relationships, or the rigid layer.
3. **C4:** the sections of the definition schema.
4. **D3:** "zero is null" (owner) vs code, where null means absent and 0 is a present value. Which sense does the brain use?
5. **E1:** the second memory a neuron is born with was not named.
6. **E6:** the shape of a reasoning neuron.
7. **I4:** what exactly starts back-population.
8. **J4:** the heartbeat.
9. **L1:** the channel for talking to the baby.

## Progress

| Part | Status |
|---|---|
| A What it is / turn one | done |
| B Laws | done (B3 open) |
| C Words, meanings, numbers | done (C3, C4 sections open) |
| D Graph | done |
| E Neuron and shards | done |
| F Run | done |
| G Memory and timeline | done |
| H Truth and guesses | done |
| I Learning | done |
| J Reasoning and the sixth | done |
| K Sleep and HC | done |
| L Talking and outside | done |
| M Building it | done |
| N How we work | done |

**Interview complete 2026-10-18.** The clean document is `NEURON-NOW-2026-10-18.md`, in the same folder.
