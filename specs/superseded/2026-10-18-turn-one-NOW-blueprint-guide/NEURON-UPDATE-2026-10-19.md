# UPDATE for the running builds (2026-10-19)

*This was added to `~/neuron-build/` after the builders started. Read it, then read the changed parts named below. Nothing that was already settled has changed; everything here is an addition.*

1. **Merriam-Webster keys are here.** They are in `~/neuron-build/keys/mw_collegiate.key` (the Collegiate Dictionary) and `mw_thesaurus.key` (the Collegiate Thesaurus), mode 600. Both were tested live on this machine. Install them where the brain can read them (blueprint §17, step 1). Each key works only for its own reference.
2. **Sources.** `NEURON-SOURCES-2026-10-19.md`, also at `/srv/sources/SOURCES.md`, lists about 60 sources the brain can connect to, tested live and sorted into grounded, grounded to a degree, and never grounded.
   - Open English WordNet 2025 is in `/srv/sources/wordnet/oewn-2025/`, alongside the installed WordNet 3.0.
   - The brain reads sources itself, through runs. Nothing is bulk-loaded.
3. **`/home/james` started at mode 700,** so the `neuron` user couldn't read anything under it. If you haven't handled that already, put the kernel binary, the lay files, the sources and the keys the brain must read outside it. `/srv/sources/` is readable by everyone.
4. **QKV is allowed on the guessing side only** (owner, 10-19). The rules are in the new paragraph at the end of blueprint §10.6 and the new "QKV in the wrong place" trap in guide §4:
   - many small sets of weights, each over a small group of data, never over the whole corpus;
   - the brain's own weights, built from its own math, changed only in sleep;
   - the output is always a labeled guess, never a truth.
5. **Research.** `NEURON-RESEARCH-2026-10-19.md` collects published work behind the owner's ideas: meaning vs definition; telling vs teaching vs learning; understanding and applying; learning as compute and use as retrieval; and QKV as guessing. It is reading for the *why*, not new instructions. Where it seems to disagree with NOW or the blueprint, NOW and the blueprint win.
