#!/usr/bin/env python3
# g34/hp_defwords_patch.py (2026-11-02, 03:00). A keyed read for the recall's known and unknown: `defwords (gate, word, defined)`, the words
# of a point's definition rows (its sources' returns through the encoder), each once, with whether the word holds definition rows of its own
# now. Measured first: computing them in SQL over the point's returns at recall time cost who 0.165 s, bread 0.84 s, stone 2.2 s, water
# 3.7 s (each symbol a vtable lookup); the same reading in C is one pass over the returns' symbols. The recall must be milliseconds.
import sys
D = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/hp'
P = D + '/nkvt.c'; s = open(P, encoding='utf-8').read()
CODE = r'''
/* defwords (gate, word, defined): the words of a point's definition rows, each once, and whether the word holds definition rows itself now
   (the guesser's rows, source 15, do not count). Keyed by the point; the recall's known and unknown cells read it. */
static int *DWW; static unsigned char *DWD; static int DWN, DWCAP; static i64 DWGATE = -1;
static void defwords_of(Brain *b, int gate){
  if(gate == DWGATE) return; DWGATE = gate; DWN = 0; Neuron *n = neuron_of(b, gate); if(!n || !n->nnode) return;
  int wikt = label_gate(b, "wikt"); HMap seen; hmap_init(&seen, 1 << 10);
  for(int j = 0; j < n->nnode; j++){ i64 run = n->node[j].run; Run *r = run_of(b, run); if(!r || !((r->arrival >= 7 && r->arrival <= 14) || r->arrival == wikt)) continue;
    int ns; const int *sq = nk_seq(b, run, &ns);
    for(int k = 0; sq && k < ns; k++){ int x = sq[k]; if(x <= 0 || x > b->label.n) continue; unsigned char c0 = (unsigned char)b->label.sym[x][0]; if(!((c0 >= 'A' && c0 <= 'Z') || (c0 >= 'a' && c0 <= 'z'))) continue;
      if(hmap_get(&seen, x, 0)) continue; hmap_put(&seen, x, 0, 1);
      if(DWN >= DWCAP){ DWCAP = DWCAP ? DWCAP * 2 : 1024; DWW = realloc(DWW, DWCAP * sizeof(int)); DWD = realloc(DWD, DWCAP); }
      Neuron *w = neuron_of(b, x); int def = 0; if(w) for(int q = 0; q < w->nnode; q++) if(w->node[q].source != 15){ def = 1; break; }
      DWW[DWN] = x; DWD[DWN] = (unsigned char)def; DWN++; } }
  free(seen.e);
}
static void defwords_begin(Cur *c, int idx, sqlite3_value **argv){ c->idx = idx; c->started = 0; c->i = -1; if(idx == 1){ c->k1 = V(argv[0]); defwords_of(c->b, (int)c->k1); } else { DWGATE = -1; DWN = 0; } }
static int defwords_step(Cur *c){ if(c->idx != 1) return 0; c->i++; return c->i < DWN; }
static void defwords_col(Cur *c, sqlite3_context *x, int col){ switch(col){ case 0: R(x, c->k1); break; case 1: R(x, DWW[c->i]); break; case 2: R(x, DWD[c->i]); break; } }
static i64 defwords_rowid(Cur *c){ return (c->k1 << 24) | (c->i + 1); }
'''
anchor = '/* run_sheet (run, cell, state, value) */'
assert s.count(anchor) == 1; s = s.replace(anchor, CODE + anchor)
entry = '  {"replay", "CREATE TABLE x(parent INTEGER, source INTEGER, kind INTEGER)", 3, 0, {{0}}, {0}, rp_begin, rp_step, rp_col, plain_rowid, rp_update},'
assert s.count(entry) == 1
s = s.replace(entry, entry + '\n  {"defwords", "CREATE TABLE x(gate INTEGER, word INTEGER, defined INTEGER)", 3, 1, {{0}}, {1}, defwords_begin, defwords_step, defwords_col, defwords_rowid, 0},')
open(P, 'w', encoding='utf-8').write(s); print('nkvt.c: defwords table')
# RECALL-7: the ask's known and unknown from defwords
import importlib.util
S = D.rsplit('/', 1)[0]
spec = importlib.util.spec_from_file_location('m4', S + '/make_recall4.py'); m4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m4)
KU = ("INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , k.gate , 1 , coalesce ( ( SELECT group_concat ( word , ' ' ) FROM ( SELECT word FROM defwords WHERE gate = what AND defined = ( k.symbol = 'known' ) ORDER BY word ) ) , '' ) FROM label k WHERE k.symbol IN ( 'known' , 'unknown' ) AND EXISTS ( SELECT 1 FROM node WHERE gate = what )")
ASK = ('BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( above , 24 , 0 , NULL ) ; '
       'INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , cell , state , value FROM run_sheet WHERE run = ( SELECT parent FROM run WHERE id = ( SELECT max ( run ) FROM node WHERE gate = what ) ) AND cell = 24 AND state = 1 ; '
       + KU + ' ; ' + m4.INBOX + ' ; BUILD')
SPAN1 = 'BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , ( SELECT gate FROM seq WHERE run = above AND pos = ( SELECT min ( pos ) FROM seq WHERE run = above AND gate = 68 ) + 2 ) ; INSERT INTO replay ( parent , source , kind ) VALUES ( above , {run:1} , 1 ) ; BUILD'
DEFINE = SPAN1 + ' ' + m4.SPAN2 + ' ' + m4.SPAN3
BIND = 'BUILD UPDATE dna SET call = {run:2} WHERE gate = {gate:define} AND before = 1 AND trigger = 68 ; BUILD'
open(S + '/RECALL-7-nk.txt', 'w', encoding='utf-8').write('\n'.join([
    "# RECALL-7-nk.txt (2026-11-02, 03:00). RECALL-6 with known and unknown read from the kernel's defwords table (one pass over the point's",
    "# definition rows in C) instead of SQL over its returns (0.2 to 3.7 s a recall, measured). def is copied from the definition node.",
    "# 1. The ask.", ASK, "# 2. The define run.", DEFINE, "# 3. define's row calls it.", BIND, ""]))
print('RECALL-7-nk.txt written')
