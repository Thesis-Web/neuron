#!/usr/bin/env python3
# g34/hp_rels_patch.py (2026-11-01, 18:50). A `rels N` request for the kernel: the back-population of the relationship rows of points already
# defined, from their own definition rows, N points a call so the kernel answers between calls. The owner: "as part of the build step
# relationships are populated so that the meanings have push and pull to the graph"; "it does require or can require back population of
# existing dna shard triggers". The same reading as the define run's second span (RECALL-5): WordNet's and Wiktionary's bracketed markers,
# the marker mapped onto the catalog's word by the brain's own table main.relmap (marker, kind), every single-symbol target a rel row.
# The SQL form of this cost 3 to 32 s a point on old returns (measured); in C over the same symbols it is microseconds a return.
import sys
D = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/hp'
P = D + '/nkio.c'; s = open(P, encoding='utf-8').read()
CODE = r'''
/* rels N: the relationship rows of the next N defined points, laid from their definition rows (WordNet's and Wiktionary's bracketed markers,
   mapped by main.relmap), for points that hold no relationship row beyond like/opposite/capitalized yet. A cursor keeps the place between calls. */
static int RELS_G = 1;
static void do_rels(Brain *b, int npoints, SB *o){
  double t0 = now_s(); int wikt = label_gate(b, "wikt"), like = label_gate(b, "like"), opp = label_gate(b, "opposite"), capd = label_gate(b, "capitalized");
  enum { LB = 143, RB = 147, LC = 173, RC = 177, COLON = 68, SEMI = 45, COMMA = 38 };
  char *mk[128]; int mkind[128]; int nmk = 0;
  { sqlite3_stmt *m = 0; sqlite3_prepare_v2(DB, "SELECT marker, kind FROM main.relmap", -1, &m, 0);
    while(m && sqlite3_step(m) == SQLITE_ROW && nmk < 128){ const char *a = (const char*)sqlite3_column_text(m, 0), *k = (const char*)sqlite3_column_text(m, 1); int kg = k ? label_gate(b, k) : 0; if(a && kg){ mk[nmk] = strdup(a); mkind[nmk] = kg; nmk++; } }
    if(m) sqlite3_finalize(m); }
  if(!nmk){ sb_str(o, "{\"error\":\"main.relmap holds no marker the encoder knows\"}"); return; }
  static sqlite3_stmt *HAS, *INS; if(!HAS) sqlite3_prepare_v2(DB, "SELECT 1 FROM main.rel WHERE gate = ? AND kind NOT IN (?, ?, ?) LIMIT 1", -1, &HAS, 0);
  if(!INS) sqlite3_prepare_v2(DB, "INSERT OR IGNORE INTO main.rel (gate, kind, other, run) VALUES (?, ?, ?, ?)", -1, &INS, 0);
  i64 points = 0, skipped = 0, returns = 0, rows = 0; int g = RELS_G; char marker[256];
  for(; g <= b->label.n && points < npoints; g++){ Neuron *n = neuron_of(b, g); if(!n || !n->nnode) continue; points++;
    sqlite3_reset(HAS); sqlite3_bind_int(HAS, 1, g); sqlite3_bind_int(HAS, 2, like); sqlite3_bind_int(HAS, 3, opp); sqlite3_bind_int(HAS, 4, capd);
    if(sqlite3_step(HAS) == SQLITE_ROW){ skipped++; continue; }
    for(int j = 0; j < n->nnode; j++){ i64 run = n->node[j].run; Run *r = run_of(b, run); if(!r || !(r->arrival == 7 || r->arrival == wikt)) continue;
      int ns; const int *sq = nk_seq(b, run, &ns); if(!sq || ns < 4) continue; returns++;
      for(int i = 0; i < ns; i++){ if(sq[i] != LB) continue;
        int c = -1, e = -1; for(int k = i + 1; k < ns; k++){ if(sq[k] == COLON || sq[k] == RB){ c = k; break; } } if(c < 0 || sq[c] != COLON) continue;
        for(int k = c + 1; k < ns; k++){ if(sq[k] == RB){ e = k; break; } if(sq[k] == LB) break; } if(e < 0) continue;
        int ml = 0; marker[0] = 0; for(int k = i + 1; k < c; k++){ if(sq[k] == SPACE || sq[k] <= 0 || sq[k] > b->label.n) continue; const char *w = b->label.sym[sq[k]]; int wl = (int)strlen(w); if(ml + wl + 2 >= (int)sizeof marker) break; if(ml) marker[ml++] = ' '; memcpy(marker + ml, w, wl); ml += wl; marker[ml] = 0; }
        int kind = 0; for(int k = 0; k < nmk; k++) if(strcmp(mk[k], marker) == 0){ kind = mkind[k]; break; } if(!kind) continue;
        for(int t = c + 1; t < e; t++){ int x = sq[t]; if(x <= 0 || x > b->label.n || x == r->about) continue; unsigned char c0 = (unsigned char)b->label.sym[x][0]; if(!((c0 >= 'A' && c0 <= 'Z') || (c0 >= 'a' && c0 <= 'z'))) continue;
          int pv = t - 1; while(pv > i && sq[pv] == SPACE) pv--; int nx = t + 1; while(nx < e && sq[nx] == SPACE) nx++;
          int pg = sq[pv], ng = sq[nx]; if(!(pg == LC || pg == COLON || pg == SEMI || pg == COMMA)) continue; if(!(ng == RC || ng == SEMI || ng == RB || ng == COMMA)) continue;
          sqlite3_reset(INS); sqlite3_bind_int(INS, 1, r->about); sqlite3_bind_int(INS, 2, kind); sqlite3_bind_int(INS, 3, x); sqlite3_bind_int64(INS, 4, run); if(sqlite3_step(INS) == SQLITE_DONE) rows += sqlite3_changes(DB); } } } }
  RELS_G = g; for(int k = 0; k < nmk; k++) free(mk[k]);
  sb_fmt(o, "{\"brain\":\"%s\",\"from_gate\":%d,\"next_gate\":%d,\"gates\":%d,\"done\":%s,\"points\":%lld,\"already_had\":%lld,\"returns_read\":%lld,\"rows_laid\":%lld,\"markers\":%d,\"seconds\":%.1f}", b->name, RELS_G - (int)(g - RELS_G), g, b->label.n, g > b->label.n ? "true" : "false", (long long)points, (long long)skipped, (long long)returns, (long long)rows, nmk, now_s() - t0);
}
'''
anchor = 'static void do_bundle(Brain *b, int K, SB *o){'
assert s.count(anchor) == 1; s = s.replace(anchor, CODE + anchor)
old_h = '  if(strcmp(req, "hop") == 0){'
assert s.count(old_h) == 1
s = s.replace(old_h, '  if(strncmp(req, "rels", 4) == 0){ int n = atoi(req + 4); do_rels(&MAINB, n > 0 ? n : 20000, o); return; }\n' + old_h)
open(P, 'w', encoding='utf-8').write(s); print('nkio.c: do_rels + the rels request')
# the brain's own marker map, typed as a line: main.relmap (marker, kind)
MAP = [('syn', 'like'), ('synonyms', 'like'), ('ant', 'opposite'), ('antonym', 'opposite'), ('antonyms', 'opposite'),
       ('hypernym', 'is'), ('instance hypernym', 'is'), ('hypernyms', 'is'),
       ('hyponym', 'includes'), ('instance hyponym', 'includes'), ('hyponyms', 'includes'), ('troponyms', 'includes'),
       ('part holonym', 'part'), ('substance holonym', 'part'), ('holonyms', 'part'),
       ('part meronym', 'has'), ('member meronym', 'has'), ('substance meronym', 'has'), ('meronyms', 'has'),
       ('member holonym', 'member'),
       ('similar to', 'similar'), ('also see', 'similar'), ('verb group', 'similar'), ('coordinate terms', 'similar'),
       ('derivationally related form', 'derived'), ('derived', 'derived'), ('pertainym', 'derived'),
       ('related', 'related'), ('entailment', 'implies'), ('cause', 'causes'), ('attribute', 'property'),
       ('domain category', 'topic'), ('topics', 'topic'), ('member of domain category', 'topic'),
       ('domain region', 'context'), ('member of domain region', 'context'), ('domain usage', 'use'), ('member of domain usage', 'use'),
       ('participle of', 'past'), ('alternative forms', 'alias')]
line = "BUILD CREATE TABLE IF NOT EXISTS relmap ( marker TEXT PRIMARY KEY , kind TEXT ) ; INSERT OR REPLACE INTO relmap ( marker , kind ) VALUES " + " , ".join("( '%s' , '%s' )" % m for m in MAP) + " ; BUILD"
open(D + '/../RELMAP-nk.txt', 'w').write("# RELMAP-nk.txt (2026-11-01): the brain's own table of the sources' relationship markers and the catalog word each names; read by the define's second span's mapping and by the kernel's rels pass.\n" + line + "\n")
print('RELMAP-nk.txt written,', len(MAP), 'markers')
