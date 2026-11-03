# C10.1: the path rule and the markup leak, 2026-11-03 16:54 to 16:58 CST

Hydrated first. The Cortex said DO NOW C18 with one part left (the capture proof), and NEXT WORK C10.1. The 15:14 Stop hook had already proven C18.1: it judged 20 sentences of my previous message against C18. That batch also showed, live, both faults of C10.1 and two new ones.

## Done (hp2 commits ac358dc, 086163e; patch-c10-1.py and patch-c17-2.py here)
- Emphasis, heading and bullet marks come off before the sentence split.
- A path token has a word character beside its slash, so a bare `/` or `-h` is not a path; a line is a path line when it starts with one, or when two or more paths leave fewer than four words beside them.
- A receipt keeps up to 80 lines of a print (the 40-line cap dropped the summary line my C18 sentence cited).
- A value starts its token: c10.1, c18, run401 are labels, not values.

## Live
```
the command df -h / was run and its printed line shows avail 393g for / at 16:58.   -> kept
**contract.** satisfied: the root disk has 393g free as df printed.                  -> "contract." dropped (too few words); "satisfied: ..." kept
cat /home/james/a.txt /tmp/b.txt                                                     -> dropped (path)
/home/james/cortex/nk/nk 7007 egg-symbols.txt sources wn gcide                       -> dropped (path)
- the file at /home/james/cortex/cortex.py and /tmp/x.py were compared and found equal -> kept
filter: 6 sentences, kept 3, dupe 0, restated 0, noise 3, 52 ms
```
C18: completes 0.923 by receipt, done. Cortex 19 of 19. `cortex remainder cortex`: 15 parts, 12 left, NEXT WORK C10.2.

## Found while using it (typed into the brain as remainder parts)
- C16.6: three true sentences of mine were called hallucination by receipt because their numbers were in no receipt and they shared common words with broad receipts. A receipt should judge only a claim that names its command.
- C18.2: receipts of the Cortex's own prints are circular ground: four of my report sentences became parts of C18 through them. The owner's `reject cortex 18 <run>` is the word on those.
- C17.3: a digit that is a command argument in a sentence (`--at 1`) still reads as a value.
