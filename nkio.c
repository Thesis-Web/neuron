/* nkio.c (2026-10-30): mother (the paste and the mother() function the sources' triggers call), the egg, the socket the door talks to,
   the export of every region as rows for the diff, and the loop: a request when one arrives, a batch of each brain's stack otherwise. */
#include "nk.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <poll.h>
#include <stdarg.h>

static sqlite3 *DB; static Brain MAINB, SIXTHB;
sqlite3 *mother_db(void){ return DB; }

/* ---- a string builder ---- */
typedef struct { char *s; size_t n, cap; } SB;
static void sb_put(SB *b, const char *s, size_t n){ if(b->n + n + 1 > b->cap){ while(b->n + n + 1 > b->cap) b->cap = b->cap ? b->cap * 2 : 256; b->s = realloc(b->s, b->cap); } memcpy(b->s + b->n, s, n); b->n += n; b->s[b->n] = 0; }
static void sb_str(SB *b, const char *s){ sb_put(b, s, strlen(s)); }
static void sb_json(SB *b, const char *s){ sb_str(b, "\""); for(; *s; s++){ unsigned char c = *s; if(c == '"' || c == '\\'){ char t[3] = {'\\', c, 0}; sb_str(b, t); } else if(c < 0x20){ char t[8]; snprintf(t, sizeof t, "\\u%04x", c); sb_str(b, t); } else sb_put(b, (const char*)&c, 1); } sb_str(b, "\""); }
static void sb_fmt(SB *b, const char *f, ...){ char t[512]; va_list ap; va_start(ap, f); vsnprintf(t, sizeof t, f, ap); va_end(ap); sb_str(b, t); }

/* ---- mother: a text pasted at SQLite's prompt; the answer is ok, the rows, or the error ---- */
typedef struct Ent { char *text; sqlite3_stmt *st; int busy; struct Ent *next; } Ent;
#define NB 8192
static Ent *bucket[NB]; static int nent;
static unsigned hsh(const char *s){ unsigned h = 5381; while(*s) h = h * 33 + (unsigned char)*s++; return h % NB; }
static Ent *get(const char *sql, char **err){
  unsigned h = hsh(sql); Ent *e; for(e = bucket[h]; e; e = e->next) if(!e->busy && strcmp(e->text, sql) == 0){ sqlite3_reset(e->st); sqlite3_clear_bindings(e->st); return e; }
  sqlite3_stmt *st = 0; const char *tail = 0;
  if(sqlite3_prepare_v3(DB, sql, -1, SQLITE_PREPARE_PERSISTENT, &st, &tail) != SQLITE_OK){ *err = sqlite3_mprintf("%s", sqlite3_errmsg(DB)); return 0; }
  if(!st){ *err = sqlite3_mprintf("nothing to run"); return 0; }
  if(tail && *tail){ sqlite3_finalize(st); return 0; }
  e = sqlite3_malloc(sizeof(Ent)); e->text = sqlite3_mprintf("%s", sql); e->st = st; e->busy = 0; e->next = bucket[h]; bucket[h] = e; nent++; return e;
}
static int rows_cb(void *p, int argc, char **argv, char **col){ SB *b = (SB*)p; if(b->n) sb_str(b, "\n"); for(int i = 0; i < argc; i++){ if(i) sb_str(b, " | "); sb_str(b, argv[i] ? argv[i] : ""); } return 0; }
static char *run_text(const char *sql, int argc, sqlite3_value **argv){
  char *err = 0; SB got = {0};
  if(argc == 0 && strchr(sql, ';')){ if(sqlite3_exec(DB, sql, rows_cb, &got, &err) != SQLITE_OK){ char *m = sqlite3_mprintf("error: %s", err); sqlite3_free(err); free(got.s); char *r = strdup(m); sqlite3_free(m); return r; } char *r = strdup(got.n ? got.s : "ok"); free(got.s); return r; }
  if(argc == 0){ if(sqlite3_exec(DB, sql, rows_cb, &got, &err) != SQLITE_OK){ char *m = sqlite3_mprintf("error: %s", err); sqlite3_free(err); free(got.s); char *r = strdup(m); sqlite3_free(m); return r; } char *r = strdup(got.n ? got.s : "ok"); free(got.s); return r; }
  Ent *e = get(sql, &err); sqlite3_stmt *st = e ? e->st : 0;
  if(!st){ if(err){ char *m = sqlite3_mprintf("error: %s", err); sqlite3_free(err); char *r = strdup(m); sqlite3_free(m); return r; }
    if(sqlite3_exec(DB, sql, rows_cb, &got, &err) != SQLITE_OK){ char *m = sqlite3_mprintf("error: %s", err); sqlite3_free(err); free(got.s); char *r = strdup(m); sqlite3_free(m); return r; } char *r = strdup(got.n ? got.s : "ok"); free(got.s); return r; }
  for(int i = 0; i < argc; i++) sqlite3_bind_value(st, i + 1, argv[i]);
  e->busy = 1; int rc;
  while((rc = sqlite3_step(st)) == SQLITE_ROW){ int n = sqlite3_column_count(st); if(got.n) sb_str(&got, "\n"); for(int c = 0; c < n; c++){ if(c) sb_str(&got, " | "); const char *v = (const char*)sqlite3_column_text(st, c); sb_str(&got, v ? v : ""); } }
  e->busy = 0;
  if(rc != SQLITE_DONE){ char *m = sqlite3_mprintf("error: %s", sqlite3_errmsg(DB)); sqlite3_reset(st); free(got.s); char *r = strdup(m); sqlite3_free(m); return r; }
  sqlite3_reset(st); char *r = strdup(got.n ? got.s : "ok"); free(got.s); return r;
}
/* where mother's time goes, per text pasted (the owner: profile every statement before reporting a run time) */
typedef struct Prof { char *text; i64 ns, n; struct Prof *next; } Prof;
static Prof *pbucket[NB]; static int nprof;
static void prof_add(const char *sql0, i64 ns){ static char key[400]; size_t n = 0; for(const char *s = sql0; *s && n < sizeof key - 2; s++){ if(*s >= '0' && *s <= '9'){ if(n && key[n-1] == '#') continue; key[n++] = '#'; } else key[n++] = *s; } key[n] = 0; const char *sql = key; unsigned h = hsh(sql); Prof *p; for(p = pbucket[h]; p; p = p->next) if(strcmp(p->text, sql) == 0){ p->ns += ns; p->n++; return; } p = malloc(sizeof(Prof)); p->text = strdup(sql); p->ns = ns; p->n = 1; p->next = pbucket[h]; pbucket[h] = p; nprof++; }
char *mother_paste(const char *sql){ i64 t0 = now_ns(); char *r = run_text(sql, 0, 0); prof_add(sql, now_ns() - t0); return r; }
static void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){ const char *sql = (const char*)sqlite3_value_text(argv[0]); if(!sql){ sqlite3_result_text(ctx, "error: nothing to run", -1, SQLITE_STATIC); return; } i64 t0 = now_ns(); char *r = run_text(sql, argc - 1, argv + 1); prof_add(sql, now_ns() - t0); sqlite3_result_text(ctx, r, -1, SQLITE_TRANSIENT); free(r); }
int mother_open(Brain *main, Brain *sixth, const char **sources, int nsources, const char *srcdir){
  if(sqlite3_open(":memory:", &DB) != SQLITE_OK) return -1;
  sqlite3_exec(DB, "PRAGMA recursive_triggers = ON", 0, 0, 0);
  sqlite3_exec(DB, "ATTACH ':memory:' AS sixth", 0, 0, 0);
  for(int i = 0; i < nsources; i++){ char *q = sqlite3_mprintf("ATTACH '%q/%q.db' AS %w", srcdir, sources[i], sources[i]); char *e = 0; if(sqlite3_exec(DB, q, 0, 0, &e) != SQLITE_OK){ fprintf(stderr, "attach %s: %s\n", sources[i], e); sqlite3_free(e); } sqlite3_free(q); }
  sqlite3_create_function_v2(DB, "mother", -1, SQLITE_UTF8, 0, motherFunc, 0, 0, 0);
  nkvt_register(DB, main, sixth);
  return 0;
}

/* ---- the egg: the hand-laid symbols of egg6, in their order; the regions of all of them; row 0 of the arrivals and born ---- */
static void lay_egg(Brain *b, const char *symfile){
  FILE *f = fopen(symfile, "r"); if(!f){ perror(symfile); exit(1); }
  char line[4096]; while(fgets(line, sizeof line, f)){ size_t n = strlen(line); while(n && (line[n-1] == '\n' || line[n-1] == '\r')) line[--n] = 0; if(!n) continue; char *s = line; if(strcmp(s, "<space>") == 0) s = " "; label_new(b, s); }
  fclose(f);
  for(int g = 1; g <= b->label.n; g++) neuron_of(b, g)->born = 1;
  const char *row0[] = {"heard", "said", "mother", "sixth", "main", "born", "wn", "gcide", "mw", "mwt", "moby", "map", "sqldoc", "measured", "guess"};
  for(int i = 0; i < 15; i++){ int g = label_gate(b, row0[i]); if(g) shard_lay(b, g, 0, 0, 0); }
}

/* ---- reading back through the encoder (the bottom's show_out), for the door ---- */
static void decode_run(Brain *b, i64 run, SB *o, int limit){ Run *r = run_of(b, run); if(!r) return; int len = 0; for(int i = 0; i < r->nseq && len < limit; i++){ const char *s = b->label.sym[r->seq[i]]; sb_str(o, s); len += (int)strlen(s); } }
static void out_rows(Brain *b, i64 since, SB *o, int *first){
  for(i64 i = since; i < b->nout; i++){
    Out *w = &b->out[i]; if(!*first) sb_str(o, ","); *first = 0;
    const char *cname = (w->cell > 0 && w->cell <= b->label.n) ? b->label.sym[w->cell] : "?";
    SB v = {0};
    int is_ptr = (w->cell == REPLY || w->cell == DEF || w->cell == SAY || w->cell == REMEMBER);
    if(is_ptr && w->value && atoll(w->value) > 0){ i64 rr = atoll(w->value); Run *x = run_of(b, rr); sb_fmt(&v, "run %lld from %s: ", (long long)rr, (x && x->arrival <= b->label.n) ? b->label.sym[x->arrival] : "?"); decode_run(b, rr, &v, 160); }
    else if((strcmp(cname, "known") == 0 || strcmp(cname, "unknown") == 0) && w->value){ const char *p = w->value; int any = 0; while(*p){ while(*p == ' ') p++; if(!*p) break; int g = atoi(p); while(*p && *p != ' ') p++; if(any) sb_str(&v, " "); any = 1; sb_str(&v, (g > 0 && g <= b->label.n) ? b->label.sym[g] : "?"); } if(!any) sb_str(&v, "(none)"); }
    else sb_str(&v, w->value ? w->value : "");
    sb_str(o, "["); sb_json(o, b->name); sb_fmt(o, ",%lld,", (long long)w->run); sb_json(o, cname); sb_str(o, ","); sb_json(o, v.s ? v.s : ""); sb_str(o, "]"); free(v.s);
  }
}

/* ---- the loop over both brains' stacks: a batch of each in turn ---- */
static void pump_all(int batch){ pump_batch(&MAINB, batch); pump_batch(&SIXTHB, batch); }
static double now_s(void){ struct timeval tv; gettimeofday(&tv, 0); return tv.tv_sec + tv.tv_usec / 1e6; }

static FILE *JOURNAL;
static void do_type(Brain *b, const char *text, SB *o){
  if(JOURNAL){ fprintf(JOURNAL, "%s%s\n", b->is_main ? "" : "6> ", text); fflush(JOURNAL); }
  i64 runs0 = b->nruns, hops0 = MAINB.hops_done + SIXTHB.hops_done, gates0 = MAINB.label.n, ref0 = MAINB.refused_n + SIXTHB.refused_n, outm = MAINB.nout, outs = SIXTHB.nout;
  double t0 = now_s();
  line_in(b, 0, text);
  i64 rid = runs0 + 1;
  /* until the typed line's own run has ended, or nothing is left to run */
  for(;;){ Run *r = run_of(b, rid); if((r && r->ended) || (pending(&MAINB) == 0 && pending(&SIXTHB) == 0)) break; pump_all(64); }
  /* then let what it left run out, so the sheet is whole (as the bottom waited) */
  while(pending(&MAINB) || pending(&SIXTHB)) pump_all(64);
  i64 hits = 0; for(i64 i = rid; i <= b->nruns; i++){ Run *r = run_of(b, i); if(r && (r->root == rid || i == rid)) hits += r->nrc; }
  sb_fmt(o, "{\"schema\":\"%s\",\"run\":%lld,\"runs\":%lld,\"hits\":%lld,\"hops\":%lld,\"born\":%lld,\"refused\":%lld,\"seconds\":%.3f,\"out\":[", b->name, (long long)rid, (long long)(b->nruns - runs0), (long long)hits, (long long)(MAINB.hops_done + SIXTHB.hops_done - hops0), (long long)(MAINB.label.n - gates0), (long long)(MAINB.refused_n + SIXTHB.refused_n - ref0), now_s() - t0);
  int first = 1; out_rows(&MAINB, outm, o, &first); out_rows(&SIXTHB, outs, o, &first); sb_str(o, "]}");
}
static void do_q(const char *sql, SB *o){
  sqlite3_stmt *st = 0; if(sqlite3_prepare_v2(DB, sql, -1, &st, 0) != SQLITE_OK){ sb_str(o, "{\"error\":"); sb_json(o, sqlite3_errmsg(DB)); sb_str(o, "}"); return; }
  int n = sqlite3_column_count(st); sb_str(o, "{\"cols\":["); for(int i = 0; i < n; i++){ if(i) sb_str(o, ","); sb_json(o, sqlite3_column_name(st, i)); } sb_str(o, "],\"rows\":[");
  int first = 1, rc;
  while((rc = sqlite3_step(st)) == SQLITE_ROW){ if(!first) sb_str(o, ","); first = 0; sb_str(o, "["); for(int i = 0; i < n; i++){ if(i) sb_str(o, ","); int t = sqlite3_column_type(st, i); if(t == SQLITE_NULL) sb_str(o, "null"); else if(t == SQLITE_INTEGER) sb_fmt(o, "%lld", (long long)sqlite3_column_int64(st, i)); else if(t == SQLITE_FLOAT) sb_fmt(o, "%g", sqlite3_column_double(st, i)); else sb_json(o, (const char*)sqlite3_column_text(st, i)); } sb_str(o, "]"); }
  sb_str(o, "]"); if(rc != SQLITE_DONE){ sb_str(o, ",\"error\":"); sb_json(o, sqlite3_errmsg(DB)); } sb_str(o, "}"); sqlite3_finalize(st);
}
static void do_graph(Brain *b, SB *o){
  sb_str(o, "{\"dna\":["); int first = 1; int tables = 0;
  for(int g = 1; g <= b->label.n; g++){ Neuron *n = neuron_of(b, g); if(!n || !n->born) continue; tables++; for(int i = 0; i < n->nsh; i++){ Shard *s = &n->sh[i]; if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "[%d,%lld,", g, (long long)s->id); if(s->before) sb_fmt(o, "%d,", s->before); else sb_str(o, "null,"); if(s->trigger) sb_fmt(o, "%d,", s->trigger); else sb_str(o, "null,"); if(s->call) sb_fmt(o, "%lld,", (long long)s->call); else sb_str(o, "null,"); if(s->spawn) sb_fmt(o, "%lld,", (long long)s->spawn); else sb_str(o, "null,"); sb_fmt(o, "%lld]", (long long)s->times); } }
  sb_str(o, "],\"nodes\":{"); first = 1; for(int g = 1; g <= b->label.n; g++){ Neuron *n = neuron_of(b, g); if(!n || !n->born) continue; if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "\"%d\":%d", g, n->nnode); }
  sb_str(o, "},\"mem\":{"); first = 1; for(int g = 1; g <= b->label.n; g++){ Neuron *n = neuron_of(b, g); if(!n || !n->nmem) continue; if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "\"%d\":%d", g, n->nmem); }
  sb_str(o, "},\"first\":{"); first = 1; for(i64 i = 1; i <= b->nruns; i++){ Run *r = run_of(b, i); if(!r || !r->nseq) continue; if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "\"%lld\":%d", (long long)i, r->seq[0]); }
  sb_fmt(o, "},\"tables\":%d,\"rel\":[", tables);
  char q[64]; snprintf(q, sizeof q, "SELECT gate, kind, other, run FROM %s.rel", b->name); sqlite3_stmt *st = 0; first = 1;
  if(sqlite3_prepare_v2(DB, q, -1, &st, 0) == SQLITE_OK){ while(sqlite3_step(st) == SQLITE_ROW){ if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "[%lld,%lld,%lld,%lld]", (long long)sqlite3_column_int64(st, 0), (long long)sqlite3_column_int64(st, 1), (long long)sqlite3_column_int64(st, 2), (long long)sqlite3_column_int64(st, 3)); } sqlite3_finalize(st); }
  sb_str(o, "]}");
}
static const char *EXPORT_TABLES[] = {"label", "neuron", "dna", "node", "run", "seq", "run_sheet", "run_receipt", "run_memory", "timeline", "input", "third", "secondary", "out_user", "refused", "hit", "clock", "shards", "complete", "hop"};
static const char *SRCDIR = "sources"; static const char **SRCS; static int NSRCS;
static void copy_table(sqlite3 *dst, const char *schema, const char *name, const char *ddl_cols){
  /* read the rows through mother's connection (the regions), write them as plain rows into the export */
  char *q = sqlite3_mprintf("SELECT * FROM %w.%w", schema, name); sqlite3_stmt *st = 0;
  if(sqlite3_prepare_v2(DB, q, -1, &st, 0) != SQLITE_OK){ sqlite3_free(q); return; } sqlite3_free(q);
  int n = sqlite3_column_count(st);
  SB ddl = {0}; sb_fmt(&ddl, "CREATE TABLE \"%s\" (", name); for(int i = 0; i < n; i++){ if(i) sb_str(&ddl, ", "); sb_fmt(&ddl, "\"%s\"", sqlite3_column_name(st, i)); } sb_str(&ddl, ")");
  sqlite3_exec(dst, ddl.s, 0, 0, 0); free(ddl.s);
  SB ins = {0}; sb_fmt(&ins, "INSERT INTO \"%s\" VALUES (", name); for(int i = 0; i < n; i++){ sb_str(&ins, i ? ",?" : "?"); } sb_str(&ins, ")");
  sqlite3_stmt *w = 0; sqlite3_prepare_v2(dst, ins.s, -1, &w, 0); free(ins.s);
  while(sqlite3_step(st) == SQLITE_ROW){ for(int i = 0; i < n; i++) sqlite3_bind_value(w, i + 1, sqlite3_column_value(st, i)); sqlite3_step(w); sqlite3_reset(w); sqlite3_clear_bindings(w); }
  sqlite3_finalize(w); sqlite3_finalize(st);
}
static void do_export(const char *dir, SB *o){
  const char *names[2] = {"main", "sixth"}; const char *files[2] = {"brain.db", "sixth.db"};
  for(int bi = 0; bi < 2; bi++){
    char *path = sqlite3_mprintf("%s/%s", dir, files[bi]); unlink(path);
    sqlite3 *dst = 0; if(sqlite3_open(path, &dst) != SQLITE_OK){ sb_str(o, "{\"error\":\"export open\"}"); sqlite3_free(path); return; }
    sqlite3_exec(dst, "PRAGMA journal_mode = OFF; PRAGMA synchronous = OFF; BEGIN", 0, 0, 0);
    for(size_t i = 0; i < sizeof(EXPORT_TABLES) / sizeof(EXPORT_TABLES[0]); i++) copy_table(dst, names[bi], EXPORT_TABLES[i], 0);
    /* the tables the brain laid itself in this schema (rel, asked, spawned ...): plain tables, copied as they are */
    char *q = sqlite3_mprintf("SELECT name, sql FROM %w.sqlite_master WHERE type = 'table' AND sql NOT LIKE 'CREATE VIRTUAL%%' AND name NOT LIKE 'sqlite_%%'", names[bi]); sqlite3_stmt *st = 0;
    sqlite3_exec(dst, "CREATE TABLE \"__ddl\" (name TEXT, sql TEXT)", 0, 0, 0); sqlite3_stmt *w = 0; sqlite3_prepare_v2(dst, "INSERT INTO \"__ddl\" VALUES (?, ?)", -1, &w, 0);
    if(sqlite3_prepare_v2(DB, q, -1, &st, 0) == SQLITE_OK){ while(sqlite3_step(st) == SQLITE_ROW){ copy_table(dst, names[bi], (const char*)sqlite3_column_text(st, 0), 0); sqlite3_bind_text(w, 1, (const char*)sqlite3_column_text(st, 0), -1, SQLITE_TRANSIENT); sqlite3_bind_text(w, 2, (const char*)sqlite3_column_text(st, 1), -1, SQLITE_TRANSIENT); sqlite3_step(w); sqlite3_reset(w); } sqlite3_finalize(st); } sqlite3_free(q); sqlite3_finalize(w);
    sqlite3_exec(dst, "COMMIT", 0, 0, 0); sqlite3_close(dst); sqlite3_free(path);
  }
  sb_str(o, "{\"exported\":true}");
}
static void brain_stats(Brain *b, SB *o){
  double hop_us = b->hops_done ? (b->hop_ns - b->paste_ns) / 1000.0 / b->hops_done : 0, paste_us = b->pastes ? b->paste_ns / 1000.0 / b->pastes : 0;
  sb_fmt(o, "{\"runs\":%lld,\"hops\":%lld,\"pending\":%d,\"gates\":%d,\"refused\":%lld,\"shards\":%lld,\"hop_us\":%.3f,\"pastes\":%lld,\"paste_us\":%.1f,\"hop_s\":%.3f,\"paste_s\":%.3f,\"returns\":%lld,\"return_us\":%.1f,\"return_s\":%.3f,\"receipts\":%lld}", (long long)b->nruns, (long long)b->hops_done, pending(b), b->label.n, (long long)b->refused_n, (long long)b->shards, hop_us, (long long)b->pastes, paste_us, (b->hop_ns - b->paste_ns) / 1e9, b->paste_ns / 1e9, (long long)b->secs, b->secs ? b->sec_ns / 1000.0 / b->secs : 0, b->sec_ns / 1e9, (long long)b->nrcs);
}
/* the brain's own tables (rel, asked, spawned ...) back from an export, with their DDL, into mother's connection under the schema */
static void load_own_tables(const char *schema, const char *path){
  sqlite3 *src = 0; if(sqlite3_open_v2(path, &src, SQLITE_OPEN_READONLY, 0) != SQLITE_OK) return;
  sqlite3_stmt *st = 0; if(sqlite3_prepare_v2(src, "SELECT name, sql FROM \"__ddl\"", -1, &st, 0) != SQLITE_OK){ sqlite3_close(src); return; }
  while(sqlite3_step(st) == SQLITE_ROW){
    const char *name = (const char*)sqlite3_column_text(st, 0), *ddl = (const char*)sqlite3_column_text(st, 1); if(!name || !ddl) continue;
    const char *p = strstr(ddl, "TABLE "); if(!p) continue;
    char *q = sqlite3_mprintf("%.*s%w.%s", (int)(p + 6 - ddl), ddl, schema, p + 6); char *e = 0;
    if(sqlite3_exec(DB, q, 0, 0, &e) != SQLITE_OK){ fprintf(stderr, "load %s.%s: %s\n", schema, name, e); sqlite3_free(e); sqlite3_free(q); continue; } sqlite3_free(q);
    q = sqlite3_mprintf("SELECT * FROM \"%w\"", name); sqlite3_stmt *r = 0; if(sqlite3_prepare_v2(src, q, -1, &r, 0) != SQLITE_OK){ sqlite3_free(q); continue; } sqlite3_free(q);
    int n = sqlite3_column_count(r); SB ins = {0}; sb_fmt(&ins, "INSERT INTO %s.\"%s\" VALUES (", schema, name); for(int i = 0; i < n; i++) sb_str(&ins, i ? ",?" : "?"); sb_str(&ins, ")");
    sqlite3_stmt *w = 0; sqlite3_prepare_v2(DB, ins.s, -1, &w, 0); free(ins.s); i64 rows = 0;
    while(sqlite3_step(r) == SQLITE_ROW){ for(int i = 0; i < n; i++) sqlite3_bind_value(w, i + 1, sqlite3_column_value(r, i)); sqlite3_step(w); sqlite3_reset(w); sqlite3_clear_bindings(w); rows++; }
    sqlite3_finalize(w); sqlite3_finalize(r); fprintf(stderr, "load %s.%s: %lld rows\n", schema, name, (long long)rows);
  }
  sqlite3_finalize(st); sqlite3_close(src);
}
/* a snapshot: the export, the small source files beside it (the guesser's state), and how many journal lines were typed by then */
static int copy_file(const char *from, const char *to){ FILE *a = fopen(from, "rb"); if(!a) return -1; FILE *z = fopen(to, "wb"); if(!z){ fclose(a); return -1; } char buf[1 << 16]; size_t n; while((n = fread(buf, 1, sizeof buf, a)) > 0) fwrite(buf, 1, n, z); fclose(a); fclose(z); return 0; }
static void do_snapshot(const char *dir, SB *o){
  char *mk = sqlite3_mprintf("mkdir -p '%q'", dir); if(system(mk) != 0){ sb_str(o, "{\"error\":\"mkdir\"}"); sqlite3_free(mk); return; } sqlite3_free(mk);
  SB x = {0}; do_export(dir, &x); free(x.s);
  int copied = 0;
  for(int i = 0; i < NSRCS; i++){ char *from = sqlite3_mprintf("%s/%s.db", SRCDIR, SRCS[i]); FILE *f = fopen(from, "rb"); long sz = 0; if(f){ fseek(f, 0, SEEK_END); sz = ftell(f); fclose(f); } if(f && sz <= (16 << 20)){ char *to = sqlite3_mprintf("%s/%s.db", dir, SRCS[i]); if(copy_file(from, to) == 0) copied++; sqlite3_free(to); } sqlite3_free(from); }
  long typed = 0; if(getenv("NK_JOURNAL")){ FILE *j = fopen(getenv("NK_JOURNAL"), "r"); if(j){ int ch; while((ch = fgetc(j)) != EOF) if(ch == '\n') typed++; fclose(j); } }
  char *tp = sqlite3_mprintf("%s/typed-lines.txt", dir); FILE *t = fopen(tp, "w"); if(t){ fprintf(t, "%ld\n", typed); fclose(t); } sqlite3_free(tp);
  sb_fmt(o, "{\"snapshot\":\"%s\",\"typed_lines\":%ld,\"source_files\":%d,\"main_runs\":%lld,\"sixth_runs\":%lld}", dir, typed, copied, (long long)MAINB.nruns, (long long)SIXTHB.nruns);
}
static void do_stats(SB *o){ sb_str(o, "{\"main\":"); brain_stats(&MAINB, o); sb_str(o, ",\"sixth\":"); brain_stats(&SIXTHB, o); sb_str(o, "}"); }

static int prof_cmp(const void *a, const void *b){ const Prof *x = *(Prof* const*)a, *y = *(Prof* const*)b; return y->ns > x->ns ? 1 : (y->ns < x->ns ? -1 : 0); }
static void do_profile(SB *o, int top){
  Prof **all = malloc(sizeof(Prof*) * (nprof ? nprof : 1)); int n = 0; for(int i = 0; i < NB; i++) for(Prof *p = pbucket[i]; p; p = p->next) all[n++] = p;
  qsort(all, n, sizeof(Prof*), prof_cmp); i64 total = 0; for(int i = 0; i < n; i++) total += all[i]->ns;
  sb_fmt(o, "{\"texts\":%d,\"total_s\":%.3f,\"top\":[", n, total / 1e9);
  for(int i = 0; i < n && i < top; i++){ if(i) sb_str(o, ","); sb_fmt(o, "{\"s\":%.3f,\"n\":%lld,\"us\":%.0f,\"text\":", all[i]->ns / 1e9, (long long)all[i]->n, all[i]->ns / 1000.0 / all[i]->n); char t[200]; snprintf(t, sizeof t, "%.190s", all[i]->text); sb_json(o, t); sb_str(o, "}"); }
  sb_str(o, "]}"); free(all);
}
static void handle(const char *req, SB *o){
  if(strncmp(req, "profile", 7) == 0){ do_profile(o, atoi(req + 7) > 0 ? atoi(req + 7) : 15); return; }
  if(strcmp(req, "scans") == 0){ char t[4096]; nkvt_scans(t, sizeof t); sb_str(o, "["); sb_str(o, t); sb_str(o, "]"); return; }
  if(strncmp(req, "type main ", 10) == 0) do_type(&MAINB, req + 10, o);
  else if(strncmp(req, "type sixth ", 11) == 0) do_type(&SIXTHB, req + 11, o);
  else if(strncmp(req, "q ", 2) == 0) do_q(req + 2, o);
  else if(strncmp(req, "graph main", 10) == 0) do_graph(&MAINB, o);
  else if(strncmp(req, "graph sixth", 11) == 0) do_graph(&SIXTHB, o);
  else if(strncmp(req, "export ", 7) == 0) do_export(req + 7, o);
  else if(strncmp(req, "snapshot ", 9) == 0) do_snapshot(req + 9, o);
  else if(strcmp(req, "stats") == 0) do_stats(o);
  else if(strncmp(req, "pump ", 5) == 0){ int n = atoi(req + 5); for(int i = 0; i < n; i++) pump_all(64); do_stats(o); }
  else sb_str(o, "{\"error\":\"unknown request\"}");
}

int main(int argc, char **argv){
  if(argc < 4){ fprintf(stderr, "usage: nk <port> <symbols file> <sources dir> [source names...]\n"); return 1; }
  int port = atoi(argv[1]);
  if(getenv("NK_JOURNAL")){ JOURNAL = fopen(getenv("NK_JOURNAL"), "a"); if(!JOURNAL) perror(getenv("NK_JOURNAL")); }
  brain_init(&MAINB, "main", 1); brain_init(&SIXTHB, "sixth", 0); MAINB.tell = &SIXTHB;
  const char *load = getenv("NK_LOAD"); char *lp_main = 0, *lp_sixth = 0;
  if(load){ lp_main = sqlite3_mprintf("%s/brain.db", load); lp_sixth = sqlite3_mprintf("%s/sixth.db", load); if(nk_load(&MAINB, lp_main) != 0 || nk_load(&SIXTHB, lp_sixth) != 0){ fprintf(stderr, "the snapshot did not load whole; stopping rather than running a brain with holes\n"); return 1; } }
  else { lay_egg(&MAINB, argv[2]); lay_egg(&SIXTHB, argv[2]); }
  const char *defaults[] = {"wn", "gcide", "mw", "mwt", "moby", "map", "sqldoc", "measured", "guess"};
  const char **srcs = argc > 4 ? (const char**)argv + 4 : defaults; int nsrc = argc > 4 ? argc - 4 : 9; SRCDIR = argv[3]; SRCS = srcs; NSRCS = nsrc;
  if(mother_open(&MAINB, &SIXTHB, srcs, nsrc, argv[3]) != 0){ fprintf(stderr, "mother could not open\n"); return 1; }
  if(load){ load_own_tables("main", lp_main); load_own_tables("sixth", lp_sixth); sqlite3_free(lp_main); sqlite3_free(lp_sixth); }
  int s = socket(AF_INET, SOCK_STREAM, 0); int one = 1; setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
  struct sockaddr_in a = {0}; a.sin_family = AF_INET; a.sin_port = htons(port); a.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
  if(bind(s, (struct sockaddr*)&a, sizeof a) < 0 || listen(s, 8) < 0){ perror("listen"); return 1; }
  fprintf(stderr, "nk: %d symbols laid in each brain, listening on 127.0.0.1:%d\n", MAINB.label.n, port);
  for(;;){
    struct pollfd p = {s, POLLIN, 0}; int timeout = (pending(&MAINB) || pending(&SIXTHB)) ? 0 : -1;
    int r = poll(&p, 1, timeout);
    if(r <= 0){ pump_all(64); continue; }
    int c = accept(s, 0, 0); if(c < 0) continue;
    SB req = {0}; char buf[65536]; ssize_t n;
    while((n = read(c, buf, sizeof buf)) > 0){ sb_put(&req, buf, n); if(memchr(buf, '\n', n)) break; }
    if(req.s){ char *nl = strchr(req.s, '\n'); if(nl) *nl = 0; SB o = {0}; handle(req.s, &o); sb_str(&o, "\n"); size_t off = 0; while(off < o.n){ ssize_t w = write(c, o.s + off, o.n - off); if(w <= 0) break; off += w; } free(o.s); }
    free(req.s); close(c);
  }
}
