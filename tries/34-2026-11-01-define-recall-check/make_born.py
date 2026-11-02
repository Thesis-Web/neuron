#!/usr/bin/env python3
# g34/make_born.py (2026-11-01, 19:00). The build step of a new point, as the owner's prose has it: "once a meaning point or gate is built, the
# dna table is built and populated with its first row which is ALWAYS the define row ... this first define dna row spawns the definition of
# that new gate immediately"; "any unknowns have to be sent back through the encoder for gate assignment and build step all while not losing
# the main run". Today the born run (run 1, called by the born row) only inserts the neuron row: a new point's DNA table stays empty and
# nothing defines it unless a define line names it. Three lines:
#  1. The define-at-birth run: the define run's spans (RECALL-5) with the point taken from the sheet (what, set by the born run) instead of
#     the line's text; it replays the ask (the standing question, the sources), lays the relationship rows, fills known/unknown.
#  2. The born run: the neuron row; the point's first DNA row, the define row (before define 156, after ':' 68) whose spawn is run 1; what =
#     newgate on its own sheet; the spawn of run 1 under itself (a spawn runs beside the main run, not in it).
#  3. The born row (gate 16, shard 6) calls run 2 instead of run 1.
import importlib.util
S = '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34'
spec = importlib.util.spec_from_file_location('m4', S + '/make_recall4.py'); m4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m4)
ASK_RUN = 19936943   # RECALL-5's ask, live
SPAN1 = 'BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 23 , 1 , what ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( above , %d , 1 ) ; BUILD' % ASK_RUN
DEFINE_AT_BIRTH = SPAN1 + ' ' + m4.SPAN2 + ' ' + m4.SPAN3
BORN = 'BUILD INSERT INTO neuron ( gate ) VALUES ( newgate ) ; INSERT INTO dna ( gate , shard , before , trigger , call , spawn , times ) VALUES ( newgate , NULL , 156 , 68 , NULL , {run:1} , 0 ) ; INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( me , 23 , 1 , newgate ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( me , {run:1} , 2 ) ; BUILD'
BIND = 'BUILD UPDATE dna SET call = {run:2} WHERE gate = 16 AND shard = 6 ; BUILD'
open(S + '/BORN-nk.txt', 'w', encoding='utf-8').write('\n'.join([
    "# BORN-nk.txt (2026-11-01, 19:00). The build step of a new point: its neuron row, its first DNA row (the define row, define before, ':' after,",
    "# spawning its definition), and the definition spawned at once beside the main run. The owner: 'the dna table is built and populated with its",
    "# first row which is ALWAYS the define row ... this first define dna row spawns the definition of that new gate immediately'.",
    "# 1. The define-at-birth run: the define's spans with the point taken from the sheet (what, set by the born run).",
    DEFINE_AT_BIRTH,
    "# 2. The born run: neuron row, the define row with its spawn, what = newgate, the spawn.",
    BORN,
    "# 3. The born row calls it.",
    BIND, ""]))
print('BORN-nk.txt written: define-at-birth %d chars' % len(DEFINE_AT_BIRTH))
