/* nk.c (2026-10-30): the physics of v7's egg, done natively over regions in memory. Every function here is one of the egg's triggers
   (gen_egg6.py) said in C: input_go/third_go/secondary_go (line_in, secondary_in), replay_go (replay), land_go (land), hit_go (hit),
   ended_go + memory_go + sheet_fill + complete_go (ended, cell_set), out_mother_go (the span to mother). It decides nothing a row
   did not ask for, and it scans nothing: every find is by key. */
#include "nk.h"
#include <time.h>
i64 now_ns(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return (i64)t.tv_sec * 1000000000LL + t.tv_nsec; }
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* ---------------- hash map ---------------- */
static inline uint64_t mix(uint64_t a, uint64_t b){ uint64_t h = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL); h ^= h >> 29; h *= 0xBF58476D1CE4E5B9ULL; h ^= h >> 32; return h; }
void hmap_init(HMap *m, size_t cap){ m->cap = cap < 8 ? 8 : cap; m->n = 0; m->e = calloc(m->cap, sizeof(HEnt)); }
static void hmap_grow(HMap *m){ HEnt *old = m->e; size_t oc = m->cap; m->cap *= 2; m->e = calloc(m->cap, sizeof(HEnt)); m->n = 0; for(size_t i = 0; i < oc; i++) if(old[i].v) hmap_put(m, old[i].k1, old[i].k2, old[i].v); free(old); }
i64 hmap_get(HMap *m, i64 k1, i64 k2){ if(!m->e) return 0; size_t i = mix(k1, k2) & (m->cap - 1); for(;;){ HEnt *e = &m->e[i]; if(!e->v) return 0; if(e->k1 == k1 && e->k2 == k2) return e->v; i = (i + 1) & (m->cap - 1); } }
void hmap_put(HMap *m, i64 k1, i64 k2, i64 v){ if(!m->e) hmap_init(m, 8); if((m->n + 1) * 10 > m->cap * 7) hmap_grow(m); size_t i = mix(k1, k2) & (m->cap - 1); for(;;){ HEnt *e = &m->e[i]; if(!e->v){ e->k1 = k1; e->k2 = k2; e->v = v; m->n++; return; } if(e->k1 == k1 && e->k2 == k2){ e->v = v; return; } i = (i + 1) & (m->cap - 1); } }
void hmap_del(HMap *m, i64 k1, i64 k2){ /* rebuild without the key (rare) */ if(!hmap_get(m, k1, k2)) return; HEnt *old = m->e; size_t oc = m->cap; m->e = calloc(m->cap, sizeof(HEnt)); m->n = 0; for(size_t i = 0; i < oc; i++) if(old[i].v && !(old[i].k1 == k1 && old[i].k2 == k2)) hmap_put(m, old[i].k1, old[i].k2, old[i].v); free(old); }
uint64_t strhash(const char *s){ uint64_t h = 1469598103934665603ULL; while(*s){ h ^= (unsigned char)*s++; h *= 1099511628211ULL; } return h; }

#define GROW(arr, n, cap, T) do { if((n) >= (cap)){ (cap) = (cap) ? (cap) * 2 : 64; (arr) = realloc((arr), (cap) * sizeof(T)); } } while(0)

/* ---------------- the brain ---------------- */
void brain_init(Brain *b, const char *name, int is_main){
  memset(b, 0, sizeof(*b)); b->name = name; b->is_main = is_main;
  hmap_init(&b->label.h, 1024); hmap_init(&b->relh, 1024); hmap_init(&b->memh, 1024); hmap_init(&b->hith, 1 << 12);
  b->label.cap = 256; b->label.sym = calloc(b->label.cap, sizeof(char*)); b->label.n = 0;   /* sym[gate], gate from 1 */
  b->cruns = 1024; b->runs = calloc(b->cruns, sizeof(Run)); b->nruns = 0;
  b->cnr = 256; b->nr = calloc(b->cnr, sizeof(Neuron)); b->nnr = 0;
  b->arrival_of_third = is_main ? SIXTH : MAIN;
}
int label_gate(Brain *b, const char *sym){ return (int)hmap_get(&b->label.h, (i64)strhash(sym), 1); }
int label_new(Brain *b, const char *sym){
  int g = label_gate(b, sym); if(g) return g;
  g = ++b->label.n; if(g >= b->label.cap){ b->label.cap *= 2; b->label.sym = realloc(b->label.sym, b->label.cap * sizeof(char*)); }
  b->label.sym[g] = strdup(sym); hmap_put(&b->label.h, (i64)strhash(sym), 1, g);
  /* a symbol's gate exists before its region is born (as in v6 a label row exists before the gate's tables) */
  if(g >= b->cnr){ int oc = b->cnr; b->cnr = g * 2; b->nr = realloc(b->nr, b->cnr * sizeof(Neuron)); memset(b->nr + oc, 0, (b->cnr - oc) * sizeof(Neuron)); }
  if(g > b->nnr) b->nnr = g;
  return g;
}
Neuron *neuron_of(Brain *b, int gate){ if(gate <= 0 || gate >= b->cnr) return 0; return &b->nr[gate]; }
Shard *shard_find(Brain *b, int gate, int before, int trigger){ Neuron *n = neuron_of(b, gate); if(!n || !n->born) return 0; i64 i = hmap_get(&n->h, before, trigger); return i ? &n->sh[i - 1] : 0; }
Shard *shard_lay(Brain *b, int gate, int before, int trigger, i64 times){
  Neuron *n = neuron_of(b, gate); if(!n) return 0;
  GROW(n->sh, n->nsh, n->csh, Shard);
  Shard *s = &n->sh[n->nsh++]; s->id = ++b->shards; s->before = before; s->trigger = trigger; s->call = 0; s->spawn = 0; s->times = times;
  hmap_put(&n->h, before, trigger, n->nsh);
  return s;
}
Run *run_of(Brain *b, i64 id){ if(id <= 0 || id > b->nruns) return 0; return &b->runs[id]; }
i64 new_run(Brain *b, int arrival, i64 parent, int has_parent, int kind, int cell, int about){
  b->clock++;
  i64 id = ++b->nruns; if(id >= b->cruns){ i64 oc = b->cruns; b->cruns *= 2; b->runs = realloc(b->runs, b->cruns * sizeof(Run)); memset(b->runs + oc, 0, (b->cruns - oc) * sizeof(Run)); }
  Run *r = &b->runs[id]; memset(r, 0, sizeof(*r));
  r->arrival = arrival; r->parent_set = has_parent; r->parent = has_parent ? parent : 0; r->kind = kind; r->cell = cell; r->about = about;
  r->at = b->clock; r->moment = (i64)time(0); r->build_pos = -1;
  Run *p = has_parent ? run_of(b, parent) : 0; r->root = p ? p->root : id;
  if(p){ GROW(p->kids, p->nkids, p->ckids, i64); p->kids[p->nkids++] = id; }
  if(about){ Neuron *n = neuron_of(b, about); if(n){ GROW(n->about_runs, n->nabout, n->cabout, i64); n->about_runs[n->nabout++] = id; } }
  char v[32]; snprintf(v, sizeof v, "%lld", (long long)id); cell_set(b, id, ME, 1, v);
  if(has_parent){ snprintf(v, sizeof v, "%lld", (long long)parent); cell_set(b, id, ABOVE, 1, v); }
  return id;
}

/* ---------------- the sheet ---------------- */
static void complete_run(Brain *b, i64 run){
  Run *r = run_of(b, run); if(!r || r->complete) return; r->complete = 1;
  if(r->kind != 0) return;
  /* complete_go: the cells to the user's out mailbox, by cell */
  int order[1024], n = 0; for(int i = 0; i < r->ncells && n < 1024; i++) order[n++] = i;
  for(int i = 1; i < n; i++){ int k = order[i], j = i - 1; while(j >= 0 && r->cells[order[j]].cell > r->cells[k].cell){ order[j + 1] = order[j]; j--; } order[j + 1] = k; }
  for(int i = 0; i < n; i++){ Cell *c = &r->cells[order[i]]; GROW(b->out, b->nout, b->cout, Out); Out *o = &b->out[b->nout]; o->id = b->nout + 1; o->run = run; o->cell = c->cell; o->value = c->value ? strdup(c->value) : 0; b->nout++; }
}
static int sheet_open(Run *r){ for(int i = 0; i < r->ncells; i++) if(r->cells[i].state == 0) return 1; return 0; }
void cell_set(Brain *b, i64 run, int cell, int state, const char *value){
  Run *r = run_of(b, run); if(!r) return;
  Cell *c = 0; for(int i = 0; i < r->ncells; i++) if(r->cells[i].cell == cell){ c = &r->cells[i]; break; }
  if(!c){ GROW(r->cells, r->ncells, r->ccells, Cell); c = &r->cells[r->ncells++]; c->cell = cell; c->value = 0; }
  else { free(c->value); c->value = 0; }
  c->state = state; c->value = value ? strdup(value) : 0;
  if(state == 1 && r->has_mem && !sheet_open(r)) complete_run(b, run);          /* sheet_fill */
}
const char *cell_get(Brain *b, i64 run, int cell){ Run *r = run_of(b, run); if(!r) return 0; for(int i = 0; i < r->ncells; i++) if(r->cells[i].cell == cell && r->cells[i].state == 1 && r->cells[i].value) return r->cells[i].value; return 0; }

/* ---------------- the hop stack ---------------- */
static void push(Brain *b, Hop h){ GROW(b->hop, b->nhop, b->chop, Hop); b->hop[b->nhop++] = h; }
int pending(Brain *b){ return (int)b->nhop; }
static void land(Brain *b, i64 run, int pos, int gate, int before, int next, int via);
static void hit(Brain *b, i64 run, int pos, int gate, int before, int next, int via, int had, Shard *s);
static void ended(Brain *b, i64 run, int gate, i64 shard);
static void replay(Brain *b, i64 parent, i64 source, int kind);

/* ---------------- the cut (the encoder) ---------------- */
static int is_letter(unsigned char c){ return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_'; }
static int u8len(unsigned char c){ if(c < 0x80) return 1; if((c >> 5) == 6) return 2; if((c >> 4) == 14) return 3; if((c >> 3) == 30) return 4; return 1; }
/* GROW above for seq uses nseq as cap guard; give seq its own growth */
static void seq_push(Run *r, int g){ if(r->nseq % 64 == 0){ r->seq = realloc(r->seq, (r->nseq + 64) * sizeof(int)); } r->seq[r->nseq++] = g; }

static void cut2(Brain *b, i64 run, const char *text){
  Run *r = run_of(b, run); size_t i = 0, L = strlen(text); char buf[4096];
  while(i < L){
    size_t j = i;
    if(is_letter((unsigned char)text[i])){ while(j < L && is_letter((unsigned char)text[j])) j++; }
    else j = i + u8len((unsigned char)text[i]);
    if(j > L) j = L;
    size_t n = j - i; if(n >= sizeof buf) n = sizeof buf - 1;
    memcpy(buf, text + i, n); buf[n] = 0;
    int g = label_gate(b, buf); if(!g) g = label_new(b, buf);
    seq_push(r, g); i = j;
  }
}
static void first_landing(Brain *b, i64 run){ Run *r = run_of(b, run); if(r->nseq > 0) land(b, run, 0, r->arrival, 0, r->seq[0], 0); }

/* a line arriving at a prompt: input (heard) or third (the other brain) */
void line_in(Brain *b, int which, const char *text){
  int arrival = which == 0 ? HEARD : b->arrival_of_third;
  i64 run = new_run(b, arrival, 0, 0, 0, 0, 0);
  Mail **box = which == 0 ? &b->input : &b->third; i64 *n = which == 0 ? &b->ninput : &b->nthird; i64 *c = which == 0 ? &b->cinput : &b->cthird;
  GROW(*box, *n, *c, Mail); Mail *m = &(*box)[*n]; m->id = *n + 1; m->text = 0; m->run = run; (*n)++;   /* the text is let go */
  cut2(b, run, text); first_landing(b, run);
}
/* a return: mother's or a source's answer, with the key */
void secondary_in(Brain *b, i64 run, int cell, int gate, int about, const char *text){
  i64 id = new_run(b, gate, run, 1, 3, cell, about);
  GROW(b->sec, b->nsec, b->csec, Sec); Sec *s = &b->sec[b->nsec]; s->id = b->nsec + 1; s->run = run; s->cell = cell; s->gate = gate; s->about = about; s->text = 0; s->made = id; b->nsec++;
  cut2(b, id, text ? text : ""); first_landing(b, id);
}
void replay_push(Brain *b, i64 parent, i64 source, int kind){ Hop h = {0}; h.type = HOP_REPLAY; h.run = parent; h.a = source; h.kind = kind; push(b, h); }
static void replay(Brain *b, i64 parent, i64 source, int kind){
  i64 id = new_run(b, SAID, parent, 1, kind, 0, 0);
  Run *src = run_of(b, source), *r = run_of(b, id);
  if(src) for(int i = 0; i < src->nseq; i++) seq_push(r, src->seq[i]);
  if(r->nseq > 0){ Hop h = {0}; h.type = HOP_LAND; h.run = id; h.pos = 0; h.gate = SAID; h.before = 0; h.next = r->seq[0]; h.via = 0; push(b, h); }
}

/* ---------------- the landing and the hit (land_go, hit_go) ---------------- */
static void land(Brain *b, i64 run, int pos, int gate, int before, int next, int via){
  Run *r = run_of(b, run); if(!r) return;
  int kb = 0, kx = 0;
  if(!(pos == 0 || via == 1 || gate == SPACE)){
    kb = r->arrival; for(int p = pos - 1; p >= 1; p--) if(r->seq[p - 1] != SPACE){ kb = r->seq[p - 1]; break; }
    for(int p = pos + 1; p <= r->nseq; p++) if(r->seq[p - 1] != SPACE){ kx = r->seq[p - 1]; break; }
  }
  Neuron *n = neuron_of(b, gate);
  if(!n || !n->born){ /* a landing on a gate with no region: as v6's paste into a missing table, the step is refused and the run stalls */
    GROW(b->ref, b->nref, b->cref, Refused); Refused *f = &b->ref[b->nref]; f->id = b->nref + 1; char t[128]; snprintf(t, sizeof t, "land run %lld pos %d gate %d", (long long)run, pos, gate); f->text = strdup(t); f->error = strdup("no such neuron"); b->nref++; b->refused_n++; return; }
  Shard *s = shard_find(b, gate, kb, kx);
  if(!s) s = shard_lay(b, gate, kb, kx, 0);
  s->times++;
  int had = 0; if(next){ Neuron *nn = neuron_of(b, next); had = (nn && nn->born) ? 1 : 0; }
  hit(b, run, pos, gate, before, next, via, had, s);
}
static char *decode_span(Brain *b, i64 run, int from_pos, int to_pos){
  Run *r = run_of(b, run); size_t cap = 1024, len = 0; char *out = malloc(cap); out[0] = 0;
  i64 parent = r->parent_set ? r->parent : 0; Run *pr = parent ? run_of(b, parent) : 0; i64 gp = (pr && pr->parent_set) ? pr->parent : 0;
  for(int p = from_pos + 1; p < to_pos; p++){
    int g = r->seq[p - 1]; const char *piece = cell_get(b, run, g);
    if(!piece && parent) piece = cell_get(b, parent, g);
    if(!piece && gp) piece = cell_get(b, gp, g);
    if(!piece) piece = b->label.sym[g];
    size_t pl = strlen(piece); if(len + pl + 1 > cap){ while(len + pl + 1 > cap) cap *= 2; out = realloc(out, cap); }
    memcpy(out + len, piece, pl); len += pl; out[len] = 0;
  }
  return out;
}
static void hit(Brain *b, i64 run, int pos, int gate, int before, int next, int via, int had, Shard *s){
  Run *r = run_of(b, run);
  /* the receipt */
  GROW(b->rcs, b->nrcs, b->crcs, Rc); Rc *c = &b->rcs[b->nrcs]; c->run = run; c->pos = pos; c->gate = gate; c->shard = s->id; c->via = (unsigned char)via; c->had = (unsigned char)had; ++b->hops_done;
  GROW(r->rc, r->nrc, r->crc, i64); r->rc[r->nrc++] = b->nrcs++;
  if(s->call || s->spawn){ GROW(b->hit, b->nhit, b->chit, Hit); Hit *h = &b->hit[b->nhit]; h->id = b->hops_done; h->run = run; h->pos = pos; h->gate = gate; h->before = before; h->next = next; h->via = via; h->had = had; h->shard = s->id; h->call = s->call; h->spawn = s->spawn; hmap_put(&b->hith, h->id, 0, b->nhit + 1); Neuron *ng = neuron_of(b, gate); if(ng){ GROW(ng->hits, ng->nhits, ng->chits, i64); ng->hits[ng->nhits++] = b->nhit; } b->nhit++; }
  /* the steps, pushed in hit_go's order; the one pushed last runs first */
  if(next == 0 && via == 0){ Hop h = {0}; h.type = HOP_ENDED; h.run = run; h.gate = gate; h.a = s->id; push(b, h); }
  if(next != 0 && (via == 1 || had == 1)){ Hop h = {0}; h.type = HOP_LAND; h.run = run; h.pos = pos + 1; h.gate = next; h.before = via == 1 ? before : gate; h.next = (pos + 2 <= r->nseq) ? r->seq[pos + 1] : 0; h.via = 0; push(b, h); }
  if(next != 0 && via == 0 && had == 0){
    char v[32]; snprintf(v, sizeof v, "%d", next); cell_set(b, run, NEWGATE, 1, v);
    Hop h = {0}; h.type = HOP_LAND; h.run = run; h.pos = pos; h.gate = BORN; h.before = gate; h.next = next; h.via = 1; push(b, h);
  }
  if(s->spawn) replay_push(b, run, s->spawn, 2);
  if(s->call) replay_push(b, run, s->call, 1);
  if(gate == BUILD && via == 0){
    if(r->build_pos < 0) r->build_pos = pos;
    else {
      int from = r->build_pos; r->build_pos = -1;
      char *text = decode_span(b, run, from, pos);
      i64 t0 = now_ns(); char *ans = mother_paste(text); free(text); b->paste_ns += now_ns() - t0; b->pastes++;
      secondary_in(b, run, REPLY, MOTHER, 0, ans); free(ans);      /* her answer arrives from mother, for the reply cell, under this run */
    }
  }
}
/* ---------------- the end of a run (ended_go, memory_go, the node, complete) ---------------- */
static void ended(Brain *b, i64 run, int gate, i64 shard){
  Run *r = run_of(b, run); if(!r || r->ended) return; r->ended = 1;
  /* the memory: the line as gates, who it arrived from, the ending gate and shard, the clock */
  size_t cap = 64 + (size_t)r->nseq * 12; char *inp = malloc(cap); inp[0] = 0; size_t len = 0;
  for(int i = 0; i < r->nseq; i++){ len += snprintf(inp + len, cap - len, i ? " %d" : "%d", r->seq[i]); }
  r->mem_input = inp; r->mem_source = r->arrival; r->mem_gate = gate; r->mem_shard = shard; r->mem_at = r->at; r->has_mem = 1;
  hmap_put(&b->memh, (i64)strhash(inp), 1, run);                        /* the newest memory with this input (remember) */
  Neuron *ng = neuron_of(b, gate); if(ng){ GROW(ng->mem_runs, ng->nmem, ng->cmem, i64); ng->mem_runs[ng->nmem++] = run; }
  /* memory_go: the timeline, then the other brain is told a prompt's run ended */
  GROW(b->tl, b->ntl, b->ctl, Tl); Tl *t = &b->tl[b->ntl++]; t->at = r->at; t->run = run; t->key1 = r->nseq ? r->seq[0] : 0; t->key2 = r->nseq ? r->seq[r->nseq - 1] : 0;
  if(r->kind == 0 && b->tell){ char line[64]; snprintf(line, sizeof line, "seen : %lld", (long long)run); line_in(b->tell, 1, line); }
  /* a return fills the cell it was asked for, on the run that asked */
  if(r->cell && r->parent_set){ char v[32]; snprintf(v, sizeof v, "%lld", (long long)run); cell_set(b, r->parent, r->cell, 1, v); }
  /* and lands a row in the definition node of the gate it is about */
  if(r->about){ Neuron *n = neuron_of(b, r->about); if(n && n->born){ GROW(n->node, n->nnode, n->cnode, NodeRow); n->node[n->nnode].source = r->arrival; n->node[n->nnode].run = run; n->nnode++; } }
  if(!sheet_open(r)) complete_run(b, run);
}

/* ---------------- the pump of one brain: n steps of its stack, the newest first ---------------- */
void pump_batch(Brain *b, int n){
  while(n-- > 0 && b->nhop > 0){
    Hop h = b->hop[--b->nhop]; i64 t0 = now_ns();
    switch(h.type){
      case HOP_LAND: land(b, h.run, h.pos, h.gate, h.before, h.next, h.via); break;
      case HOP_ENDED: ended(b, h.run, h.gate, h.a); break;
      case HOP_REPLAY: replay(b, h.run, h.a, h.kind); break;
    }
    b->hop_ns += now_ns() - t0;
  }
}
