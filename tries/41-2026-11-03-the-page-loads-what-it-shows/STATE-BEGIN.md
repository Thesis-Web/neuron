# tries/41 (2026-11-03, 01:55): the state at the beginning of the turn

The before is tries/38's `STATE-END.md` and NOTE ("The owner's questions of 11-03", "Ideas for the page"). The owner, 2026-11-03 about
02:05: "ok inform the cortex of your plan give it your outline and get the fix done..".

| What | Read at 01:55 |
|---|---|
| the hub's door | pid 530833 (the same door since 11-02 03:56, the old `serve()`), 102 % of a core, 1.08 GB resident; busy none, queued 0; hops main 1,229,297, sixth 856,440; door job 25,918 jobs / 24,764 s (still at wall-clock rate: the owner's tab on the old page text) |
| the hub's keyed reads | runs by id list 0.06 s once the queue is passed (the first waited 46 s behind a bundle read); labels, rel rows by gate and by other, a gate's DNA table, seq by run list, the timeline by id, xyz by gate list, run_memory by run list, out_user newest, a gate's node table: 0.06 to 0.34 s each |
| the kernel's door (hp) | keyed reads: run by id list, label by gate list (201 ids fine), rel by gate / by other / by gate list, seq by run list, xyz by gate list, run_memory by run, node by gate, run_receipt by run: 0.06 to 0.27 s; refused: a gate's table by name (`"153"`: the kernel has the `dna` table keyed by gate instead), the timeline by `at >`, `id >`, `at IN`, `run IN` (no range or list on the timeline), `label WHERE gate > ?` |
| the page's own handle | `window.__poc` (ready, counts, nodes, springs, chooseRun, showNode, ...) is a global: the headless checks of tries/38 could have used it |
| the page files | hub: `page_patch8` (re-read 600 s, guarded poll); hp: the poll guard; both load the whole brain on open (label, graph, run table, out_user, counts over every table, two joins over run × seq, receipts, xyz, formulas) |
| hp `/api/info` | ready, defined 722,284, runs 19,938,171, refused 1, pending 0 |
| the Cortex | neuron C10 (keyed reads), C11 (load what it shows, stream), C12 (the wave hop) registered and working; the outline ingested at 02:10 |
