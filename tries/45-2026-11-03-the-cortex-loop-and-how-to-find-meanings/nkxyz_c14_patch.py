#!/usr/bin/env python3
# nkxyz_c14_patch.py (2026-11-03, tries/45): neuron C14, the brain's own tension, READY and NOT LIVE (the owner's word is needed for a
# kernel rebuild and restart). At a landing that moved a point, the points its relationship rows name, both ways, each take one step by
# their own pulls (which now see the moved point), at most NK_TENSION_MAX of them (default 64; the words with tens of thousands of like
# rows would otherwise cost a settle pass per landing); each neighbour's step is a receipt of the timeline of its own (key1 = -other,
# key2 = pos), so restep replays it exactly as it replays every step. One round, no decay: the strength per shard and a second round are
# the owner's formula design, not laid here. usage: python3 nkxyz_c14_patch.py <copy of nkxyz.c>
import sys
path = sys.argv[1]; t = open(path, encoding='utf-8').read()
old = "  int did = xyz_step(b, gate, 1);\n  me->shard = (int)shard; me->before = before; me->next = next; me->at = b->clock; me->run = run; if(did){ me->moved++; tl_move(b, gate, run, pos, did == 1); }\n}"
assert t.count(old) == 1, 'nk_xyz_land tail'
new = """  int did = xyz_step(b, gate, 1);
  me->shard = (int)shard; me->before = before; me->next = next; me->at = b->clock; me->run = run; if(did){ me->moved++; tl_move(b, gate, run, pos, did == 1); }
  /* tries/45 (C14): the neighbours react. The points this point's relationship rows name, both ways, each take one step by their own pulls,
     at most NK_TENSION_MAX of them (64), each step a receipt of its own so restep replays it. The list is read first, then stepped: a step
     resets the shared rel statements. One round; the strength per shard and any further round are the owner's formula design. */
  if(did == 2){
    static int TENSION_MAX = -1; if(TENSION_MAX < 0){ const char *e = getenv("NK_TENSION_MAX"); TENSION_MAX = e ? atoi(e) : 64; if(TENSION_MAX < 0) TENSION_MAX = 0; }
    if(TENSION_MAX > 0){
      sqlite3 *db = mother_db();
      if(!RQ) sqlite3_prepare_v2(db, "SELECT kind, other FROM main.rel WHERE gate = ?", -1, &RQ, 0);
      if(!RQ2) sqlite3_prepare_v2(db, "SELECT kind, gate FROM main.rel WHERE other = ?", -1, &RQ2, 0);
      int *nb = malloc(sizeof(int) * TENSION_MAX); int nn = 0;
      for(int side = 0; side < 2 && nn < TENSION_MAX; side++){ sqlite3_stmt *q = side ? RQ2 : RQ; if(!q) continue; sqlite3_reset(q); sqlite3_bind_int(q, 1, gate);
        while(nn < TENSION_MAX && sqlite3_step(q) == SQLITE_ROW){ int other = sqlite3_column_int(q, 1); if(other <= 0 || (uint64_t)other >= XCAP || other == gate || other == ORIGIN_G || !X[other].placed) continue;
          int dup = 0; for(int k = 0; k < nn; k++) if(nb[k] == other){ dup = 1; break; } if(!dup) nb[nn++] = other; }
        sqlite3_reset(q); }
      for(int k = 0; k < nn; k++){ int d2 = xyz_step(b, nb[k], 1); if(d2 == 2){ X[nb[k]].at = b->clock; X[nb[k]].moved++; tl_move(b, nb[k], run, pos, 0); } }
      free(nb);
    }
  }
}"""
t = t.replace(old, new)
open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': C14, the neighbours of a moved point step by their own pulls, each a receipt')
