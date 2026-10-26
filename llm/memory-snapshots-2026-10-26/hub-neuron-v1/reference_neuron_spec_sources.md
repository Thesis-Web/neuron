---
name: reference_neuron_spec_sources
description: "Where the owner's Neuron specs live (as of 2026-10-21), newest first: the 10-20 builder handoff §0 (owner's own words), the 10-19/20 v1 build session transcript, NEURON-NOW + meaning blueprint, the 10-16 laws, the 09-28 sketch"
metadata:
  node_type: memory
  type: reference
  originSessionId: 7c20c611-9fe3-4487-be20-478341fdbaa9
  modified: 2026-10-21T17:50:33.868Z
---

Read in this order before judging any Neuron build (also `Downloads/NEURON-REFERENCE-DRAFT-1-2026-10-23.md`, the owner-edited reference; the owner reads it for errors):
0. The owner's own words of 2026-10-22/24, verbatim: turn16/OWNER-VERBATIM.txt and turn16/GROUNDING.md inside `/mnt/c/Users/AdLibitumVita/Downloads/NEURON-v18-SOURCES-2026-10-25.tar.gz` (folder t24/owner/: OWNER-VERBATIM.txt messages 1-51 and V1-BUILD-OWNER-WORDS-2026-10-19.txt; the v17.3 tarball folder t23/ has messages 1-43 + the owner's 2 edits to the reference draft; the v16.9 tarball has messages 5-26; the v16.4 tarball has up to message 4; extract to a new folder). Owner 10-23: "you have a .md file that has my prose in it. this is used for grounding not your summeries." Ground every step in these quotes, never in a compaction summary.
1. `/mnt/c/Users/AdLibitumVita/Downloads/NEURON_BUILDER_HANDOFF_2026-10-20.md` §0: the owner's own words in caps/first person (v1 "most correct so far"; "the run that lays the code to talk back to SQL is the most correct"; "the tables are built wrong because you deemed an engineering change"; only the bottom may be outside code; hand-lay only the neurons that make the table, hop and trigger; then runs for timeline, memory, dna, read/write/move/copy). §7.1 lists the prior v1 audit findings.
2. The v1 build session: `/home/exnulla/.claude/projects/-home-exnulla/3f3e6b89-45cd-492b-9c58-18f53257ace9.jsonl`, owner messages from 2026-10-19 20:55 UTC to 10-20 01:22 UTC (hand build of ~/neuron/v1; the last message rejects read/hear/born-first and positional walking: "goes to gate create, space remainder, to gate space ... if shard exists hits the shard, if not writes it"). Extract at scratchpad `sessions/3f3e_users.txt` (session-local).
3. `NEURON-NOW-2026-10-18.md` (18 sections; §6 neuron, §7 shards/hop, §11 memory) and `NEURON-MEANING-BLUEPRINT-2026-10-19.md`, same Downloads folder. `NEURON-BLUEPRINT-2026-10-18.md` and the builder guide are prior interpretations the owner partly overturned (kernel lock was wrong).
4. 10-16 laws in `/home/exnulla/.claude/projects/-home-exnulla/memory/`: 366 (hop neuron to neuron through the input's gates, shard keyed before+after, triggers are the magic), 367 (the key IS the remainder = next gate; never a position column), 380 (Claude never writes brain code; told, not taught).
5. Owner prose 343-362 and the v18 files: `/home/exnulla/neuron/v18-saved/` (v6/ bones, physics, formulas; final/; `other.txt`, `own.txt`). Owner: v18 "was the most correct we ever had"; bones.sql and physics.sql are "the cheat" (shared tables).
6. Sketch: `/home/exnulla/neuron/v18-saved/sketch/neuron_node_open_box.png` (shard table: selector/trigger | shard id | next gate | action; "selected shard determines next gate and passes remaining expression onward"; terminal resolve spawns memory; receipt trail).

The full owner memory index is `/home/exnulla/.claude/projects/-home-exnulla/memory/MEMORY.md`. Related: [[project_neuron_v1_build_state_20261021]], [[feedback_never_write_in_v1_owner_pastes]].
