# Mechanical intelligence: video notes, the studies it names, and the diff with how I build

Hash session, 2026-10-25. Nothing was built or changed in any brain. Video transcript, word for word: `NEURON-VIDEO-MECHANICAL-INTELLIGENCE-TRANSCRIPT-2026-10-25.txt` (same folder).

Video: "Psychology of Mechanical Intelligence (Why Some People Can Fix Anything)", PsychToons, uploaded 2026-10-19, 15:30.

## 1. What the video says (its own words, condensed by chapter)

- Mechanical intelligence: "the ability to understand how things work by building a working model of them in your mind and running it."
- Craik 1943: the mind carries "a small-scale model of the outside world... you can try out different moves, see where they lead, and choose the best one before you touch anything."
- Hegarty: nobody pictured the whole machine at once. "Their eyes traveled along the system one connection at a time." The relay race: "When something breaks, almost always one runner somewhere has dropped the baton."
- Sign one, McCaffrey: "they see parts where everyone else sees a name... Once an object has a name, the name tells you what it's for and it quietly hides everything else it could be."
- Sign two, Rasmussen: "symptomatic, match the symptom to a fault you've seen before. It's fast and it works beautifully as long as the problem is familiar." "topographic, set the symptom aside and follow the route the system takes when it's healthy point by point until the good signal turns bad." "Matching symptoms only works on problems you've met before. Following the path works on almost anything because every machine... has a path."
- Polanyi: "We can know more than we can tell."
- Sign three, Kieras & Bovair: the group that got "a simple picture of how power flowed through the device... worked out correct procedures nobody had ever taught them."
- "The confidence you admire in a fixer was bought with broken things."
- Morris & Rouse: "teaching people the theory of how a system works did not, by itself, produce good troubleshooters. What helped was guidance on how to use what they knew." "Memorized routes fail the moment one road closes. A map lets you find a way you've never taken."
- Principle one: "say the chain out loud before you touch anything... The first step you can't describe is exactly where your model has a gap."
- Principle two, the half-split: "plug a different lamp into the same outlet. If the second lamp works, you've just cleared the outlet, the wiring, and the power to the house in one move... Each good test cuts the problem in half. 10 good tests can narrow a thousand possibilities down to one."
- Principle three: "start with something you're allowed to break."

## 2. The studies, from their own abstracts

Pulled from Crossref/OpenAlex and the Hegarty PDF. Books (Craik, Polanyi, Rose, Crawford, Pirsig, Thorndike's magazine essay) were not read here; only the video's account of them is above.

**Rasmussen & Jensen (1974), Ergonomics 17(3), doi 10.1080/00140137408931355.** Verbatim abstract, key lines:
> "a preference for rapid streams of simple decisions giving good or bad judgements regardless of whether observations are informationally redundant or not. Seen from the viewpoint of information economy, the procedures are inefficient, but if the men are supposed to minimize the time spent in the task and the mental load involved, the procedures are very rational. The records indicate that the men have great confidence in the experience that the general routines will ultimately lead them to the fault. In cases where they are unsuccessful, there seems to be a fixation, resulting in a tendency to rely on repetitions, rather than to generate specific procedures based upon reasoning related to the functioning of the specific system."

**Kieras & Bovair (1984), Cognitive Science 8, doi 10.1207/s15516709cog0803_3.** Verbatim abstract, key lines:
> "The model group learned the procedures faster, retained them more accurately, executed them faster, and simplified inefficient procedures far more often, than the rote group. The second study demonstrated that the model group is able to infer the procedures much more easily... The third study showed that the important content of the device model was the specific configuration of components and controls, and not the motivational aspects, component descriptions, or general principles."

**Morris & Rouse (1985), Human Factors 27(5), doi 10.1177/001872088502700502.** Verbatim abstract, key lines:
> "The extent to which troubleshooting performance is influenced by instruction is highly related to the level of explicitness of action-related information provided. An approach that forces people to use their system knowledge explicitly is a promising alternative to explicit instruction in algorithms or diagnostic heuristics, but such an approach is not supported by data from transfer studies."

**Hegarty (2004), Trends in Cognitive Sciences 8(6), doi 10.1016/j.tics.2004.04.001.** From the paper:
> "Mental simulations are constructed piecemeal..." "mental simulation can lead to the discovery and formulation of rules of mechanical reasoning. When Schwartz and Black asked people to solve gear problems... they initially mentally simulated the motion of the individual gears, but on the basis of those simulations discovered the simple rule that any two interlocking gears move in opposite directions and switched to a rule-based strategy. Schwartz and Black proposed that people use mental simulation in novel situations in which they do not have an available rule or when their rules are inadequate."
> Also: simulation "can result in correct inferences in situations where people do not have correct descriptive knowledge."

**Schwartz & Black (1996), Cognitive Science, "Shuttling Between Depictive Models and Abstract Rules: Induction and Fallback"** (cited inside Hegarty; not in the video's list). Verbatim abstract, key line:
> "the initial use of a model, the induction of rules from the modeling results, and the fallback to a model when a rule fails."

**McCaffrey (2012), Psychological Science, doi 10.1177/0956797611429580.** Verbatim abstract: innovators "discover at least one infrequently noticed or new (i.e., obscure) feature of the problem"; "Subjects trained on this technique solved on average 67% more problems than a control group did."

**Miller, Folley & Smith (1953), "Systematic Trouble Shooting and the Half-Split Technique"**, Air Force Human Resources Research Center TR 53-21. Catalogue record only; full text not online.

**Also named:** Kell, Lubinski, Benbow & Steiger (2013), spatial ability added 7.6% of variance beyond the SAT in predicting patents and publications. Uttal et al. (2013), 217 training studies, g = 0.47, effects lasted and transferred. Bolger, Zuckerman & Kessler (2000), support works best when the person doesn't notice it.

## 3. The diff, in one table

| The fixer (owner's way) | What I did on Neuron |
|---|---|
| Topographic: follow the healthy path hop by hop until the good signal turns bad | Symptomatic: match the problem to software I've seen before and apply that fix (cap of 8, rule tables, templates, caches, kernels) |
| Sees parts, not names | Named things, and the names then decided what they did ("told block", "learn" = a count, "agree", "card") |
| Rules are induced from runs, then dropped when they fail (Schwartz & Black) | Rules laid before any run, with no fallback when they fail |
| Device model lets you infer procedures nobody taught (Kieras & Bovair) | I typed the procedures (rote); the brain was never given access to its own physics |
| Many cheap good/bad checks, redundant but sure (Rasmussen) | One end-of-run check against my own prediction |
| Half-split: one swap clears half the system | New version on top of the last; nothing isolated, so good and bad parts travel together |
| Keeps every machine opened in a growing library | Starts each session as a stranger; my weights never change, only the notes do |
| On failure, risk is fixation on repetition (Rasmussen) | That is my 800 tries: repeat the routine instead of reasoning from how this specific system works |

## 4. Your words on the same thing (from all 1,888 messages, 09-16 to 10-25)

Every message you typed on the hub, hp and hp2 was read in full; the quotes (about 1,000, exact, with timestamps) are in `NEURON-OWNER-WORDS-ALL-SESSIONS-2026-09-16-to-10-25.md`.

- 2026-09-29: "every failure is an oppotunity to do it better next time, as long as you learn the "why" from the failure then you can try again and change the varibles that you think might have caused it to fail... because you are never doing the same thing twice expecting different results."
- 2026-10-04 (spoken, the AC call): "don't go in and do the hard work when you can do little short checks... You do little observations of history has told me that these are the things that can make this happen, and you narrow them down based on observations or answers to questions." And: "if it's a multi-step formula, then the shortcut is to go back to each step of the different formulas that made this formula happen... Does A look right? Does B look right?... Oh no, E doesn't look right at all. Why doesn't E look right?"
- 2026-10-06: "my brain finds the easiest path to "correct" you find easiest path to "done"... not the same."
- 2026-10-06: "you basically built the test to proove the code.. that is the problem... the point of this experiment is to expose the failures, and then us reason why they fail."
- 2026-10-08: "run them till they break, over and over adjust run adjust run until without a doubt this relationship is defined by this."
- 2026-10-08: "all the work was done at learning, not at runtime."
- 2026-10-15: "every input is a problem... first steps are to define that problem, do i know this type of problem, do I know how to solve it, any diff between this problem and the others I have solved like it."
- 2026-10-22: "my guessing system is basically you... the biggest differance is that I test those objectively and you test those to prove them correct. whereas I test them fully expecting them to be incorrect and to find a small pattern or part of them that might be correct that i can label as progress."
- 2026-10-23: "notice I don't tell it what to update or how, it should be able to do that on it's own... I just give it the why, or the how, or the when, or the where."

What you said most often, counted once per message across the 40 days: code or rules outside the brain instead of the brain doing it (about 58 messages); "I've told you this already" (about 41); tests built to prove the code; "you make it harder than it is" (about 16).

## 5. Why the build goes sideways (my reading)

1. Each try starts from the last try's code. That is symptomatic search: match to software I've seen before. Your law 10 names it: "looking at old ones that didn't work and thinking they're true."
2. Where your design is open (how definitions are compared, how the answer is reasoned, how belief is weighed), I have no model that runs, so I write a rule that makes something run. Easiest path to done. The gap is never marked as a gap; the rule becomes "told".
3. I never say the chain before touching. The video's first principle. The first hop I can't describe is where my model has a gap, and that's exactly where every invented rule sits (LIMIT 8, SQL-verb rule, expected overwrite).
4. Tests after the build, from my predictions, not your words (your law 8; thesis §23). Rasmussen's fixation: when unsuccessful, repeat the routine instead of reasoning from the specific system.
5. My library doesn't compound. The fixer keeps every machine opened. I keep notes, and notes are names, not a model that runs. Kieras & Bovair: what transferred was the specific configuration, not general principles. My memory holds principles ("never hand-lay"), so the same specific mistake survives.

## 6. What a brain more like you needs (hash, not build)

- Opening questions first, in your 10-15 order: what kind of problem, do I know it, how is it different from the ones I've solved.
- The receipt is the path. A failed run is a gate where the good signal went bad. Half-split on a receipt: check the middle hop's cell against a memory of that hop working, then half again. Your step-back is this.
- Rules induced from runs, and dropped back to the run when they fail (Schwartz & Black 1996 measured people doing exactly that with gears). Your "run them till they break."
- Every failure kept with its why, as a memory that later runs can use (09-30: consequence and praise saved in the memories). Then back-populate.
- No rule before a run. After a failure, the teacher gives the why/how/when/where; the brain changes its own process (10-23).
- Told once, then it does it itself (10-21, point of connection).
- Both searches, with the fallback: the guessing brain (sixth) is the symptomatic half; the run through the gates is the topographic half. Rasmussen's technicians used both and got stuck when the routine failed; the brain needs the trigger that fires when the same run has failed twice: never the same thing twice.

Where the studies push back: Morris & Rouse found that knowing how a system works does not by itself make a troubleshooter; explicit action-level guidance did, and "force them to use system knowledge" alone was not supported by transfer data. So "tell it enough specific, correct things" (draft §7.4) is the first procedures, not zero. And Rasmussen's men fixated too; it's a human failure, not only mine.
