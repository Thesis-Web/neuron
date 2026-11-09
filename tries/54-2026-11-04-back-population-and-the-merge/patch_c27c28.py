# patch_c27c28.py (tries/54): the back population pass (relabel) and the merge function laid into the kernel sources in ~/nk-c27.
import os, sys
os.chdir(os.path.expanduser('~/nk-c27'))
h = open('nk.h').read()
if 'int nk_learn_text' not in h:
    h = h.replace("const int *nk_seq(Brain *b, i64 run, int *n);", "const int *nk_seq(Brain *b, i64 run, int *n);\nint nk_learn_text(Brain *b, const char *s);                     /* C27 back population: every symbol of a text given a gate under the encoder as it stands (label_new); the count born */\nint nk_merge(Brain *b, int h, int t, char *out, size_t cap);    /* C28 (the owner, 11-04 05:00): the hand laid neuron h merges into the neuron t of its word: shards (ids kept), node rows, memories, about, hits, arrived; the symbol of h names t */", 1)
    open('nk.h', 'w').write(h); print('nk.h: declarations added')
c = open('nk.c').read()
anchor = "static Rc *RCBUF; static int RCCAP;"
if 'int nk_learn_text' not in c:
    assert c.count(anchor) == 1
    fn = r'''
/* C27 (the owner, 11-04 04:30): a return is re-cut from its source row at every read (nk_seq); after the encoder changed, a symbol never seen
   whole has no gate and reads as 0. The back population gives every symbol of the held rows a gate under the encoder as it stands. */
int nk_learn_text(Brain *b, const char *s){
  size_t i = 0, L = strlen(s); char buf[4096]; int born = 0;
  while(i < L){ size_t j = i; if(is_letter((unsigned char)s[i])){ while(j < L && j - i < sizeof buf - 1 && is_letter((unsigned char)s[j])) j++; } else j = i + u8len((unsigned char)s[i]); if(j > L) j = L;
    size_t m = j - i; memcpy(buf, s + i, m); buf[m] = 0; if(!label_gate(b, buf)){ label_new(b, buf); born++; } i = j; }
  return born;
}
/* C28 (the owner, 11-04 05:00): "the hand laid neurons dna tables and memories should merge with the correct neuron for that word ... the dna
   table of the real gate just adds the dna table of the hand laid, since the rows are numbered in sequence you don't even have to change the
   dna shard numbers ... the memory tables attached or pointed to that shard should just follow". The symbol of h names t from now on; gate h
   keeps its text so the rows already laid still read; a shard of h whose key (before, trigger) t already holds stays with t's own. */
int nk_merge(Brain *b, int h, int t, char *out, size_t cap){
  if(h <= 0 || t <= 0 || h == t || h > b->label.n || t > b->label.n){ snprintf(out, cap, "error: gates %d and %d", h, t); return -1; }
  Neuron *H = neuron_of(b, h), *T = neuron_of(b, t); if(!H || !T){ snprintf(out, cap, "error: no neuron for %d or %d", h, t); return -1; }
  if(!T->born) T->born = 1;
  int moved = 0, kept = 0;
  for(int i = 0; i < H->nsh; i++){ Shard *s = &H->sh[i]; if(hmap_get(&T->h, s->before, s->trigger)){ kept++; continue; }
    GROW(T->sh, T->nsh, T->csh, Shard); T->sh[T->nsh++] = *s; hmap_put(&T->h, s->before, s->trigger, T->nsh); hmap_put(&b->shid, t, s->id, T->nsh); moved++; }
  int nodes = H->nnode, mems = H->nmem, about = H->nabout, hits = H->nhits, arrived = H->narrived;
  for(int i = 0; i < H->nnode; i++){ GROW(T->node, T->nnode, T->cnode, NodeRow); T->node[T->nnode++] = H->node[i]; }
  for(int i = 0; i < H->nmem; i++){ GROW(T->mem_runs, T->nmem, T->cmem, i64); T->mem_runs[T->nmem++] = H->mem_runs[i]; }
  for(int i = 0; i < H->nabout; i++){ GROW(T->about_runs, T->nabout, T->cabout, i64); T->about_runs[T->nabout++] = H->about_runs[i]; }
  for(int i = 0; i < H->nhits; i++){ GROW(T->hits, T->nhits, T->chits, i64); T->hits[T->nhits++] = H->hits[i]; }
  for(int i = 0; i < H->narrived; i++){ GROW(T->arrived, T->narrived, T->carrived, i64); T->arrived[T->narrived++] = H->arrived[i]; }
  H->nsh = 0; H->nnode = 0; H->nmem = 0; H->nabout = 0; H->nhits = 0; H->narrived = 0; H->born = 0;
  hmap_put(&b->label.h, (i64)strhash(b->label.sym[h]), 1, t);
  snprintf(out, cap, "merged %s %d into %s %d: shards %d moved, %d kept by the twin, node rows %d, memories %d, about %d, hits %d, arrived %d", b->label.sym[h], h, b->label.sym[t], t, moved, kept, nodes, mems, about, hits, arrived);
  return 0;
}
'''
    c = c.replace(anchor, fn + anchor, 1); open('nk.c', 'w').write(c); print('nk.c: nk_learn_text and nk_merge added')
io = open('nkio.c').read()
if 'do_relabel' not in io:
    reg = 'sqlite3_create_function_v2(DB, "mother", -1, SQLITE_UTF8, 0, motherFunc, 0, 0, 0);'
    assert io.count(reg) == 1
    io = io.replace(reg, reg + '\n  sqlite3_create_function_v2(DB, "merge", 2, SQLITE_UTF8, 0, mergeFunc, 0, 0, 0);   /* C28: merge(h, t), the hand laid neuron h into the neuron t of its word, on the main brain */', 1)
    mf = 'static void motherFunc('
    assert io.count(mf) == 1
    io = io.replace(mf, 'static void mergeFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv);\n' + mf, 1)
    dt = 'static void do_type(Brain *b, const char *text, SB *o){'
    assert io.count(dt) == 1
    io = io.replace(dt, r'''static void mergeFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){ char out[512]; int h = sqlite3_value_int(argv[0]), t = sqlite3_value_int(argv[1]); nk_merge(&MAINB, h, t, out, sizeof out); sqlite3_result_text(ctx, out, -1, SQLITE_TRANSIENT); }
/* C27 back population (the owner, 11-04: yes to the back population of splits): every held definition row re-read from its source and every symbol given a gate under the encoder as it stands */
static void do_relabel(Brain *b, SB *o){
  double t0 = now_s(); int n0 = b->label.n; i64 points = 0, rows = 0, texts = 0, missing = 0, born = 0;
  for(int g = 1; g <= n0; g++){ Neuron *n = neuron_of(b, g); if(!n || !n->nnode) continue; points++;
    for(int i = 0; i < n->nnode; i++){ Run *r = run_of(b, n->node[i].run); rows++; if(!r || !r->src || !r->srcgate){ missing++; continue; } const char *t = nk_source_text(r->srcgate, r->src); if(!t){ missing++; continue; } texts++; born += nk_learn_text(b, t); } }
  sb_fmt(o, "{\"points\":%lld,\"node_rows\":%lld,\"texts\":%lld,\"missing\":%lld,\"labels_before\":%d,\"labels_after\":%d,\"born\":%lld,\"seconds\":%.1f}", (long long)points, (long long)rows, (long long)texts, (long long)missing, n0, b->label.n, (long long)born, now_s() - t0);
}
''' + dt, 1)
    disp = 'if(strcmp(req, "memory") == 0){'
    assert io.count(disp) == 1
    io = io.replace(disp, 'if(strcmp(req, "relabel") == 0){ do_relabel(&MAINB, o); return; }   /* C27 back population */\n  ' + disp, 1)
    open('nkio.c', 'w').write(io); print('nkio.c: mergeFunc, do_relabel and the relabel request added')
