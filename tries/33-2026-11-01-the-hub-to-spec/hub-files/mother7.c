/* mother7.c (2026-10-29, v7): mother(text, ...): the brain hands mother SQL text and, if it likes, the values to bind to its ? holes.
   She pastes it at the SQL prompt and answers what SQLite answered: 'ok', the rows a SELECT sent back (one row per line, columns
   parted by " | "), or 'error: <SQLite's reason>'. She never stops the brain: a refusal is an answer like any other. She parses
   nothing, decides nothing and carries nothing on her own. (10-23 P2: "just a router and a traverser. That's it.")
   v7, the owner's words of 10-29 night: the pump is gone. In v5 and v6 this function, after the text it was handed, went on to read
   every attached brain's hop table and paste its rows itself, newest first, until none was left (my flat work queue, built against
   SQLite's trigger nesting). That loop knew the hop and refused tables and ran the whole typed line as one statement. Now the hop
   mailbox is read by a router loop outside the triggers (bottom7.py), one per brain on its own connection, and each hop is pasted as
   its own statement, so between any two hops the brain is free. What mother keeps is only a memory of texts she has already prepared
   on this connection, so the same text with other values is not parsed again: that is speed, not a decision.
   NEURON_TRACE=1 prints every text she runs to stderr.
   Build: gcc -shared -fPIC -O2 -o mother.so mother7.c -I.     Load: .load ./mother   */
#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

static int trace = -1;
#define NBUCKET 8192
typedef struct Ent { char *text; sqlite3_stmt *st; int busy; struct Ent *next; } Ent;
typedef struct Cache { Ent *bucket[NBUCKET]; int nent; } Cache;   /* one per connection: a prepared statement belongs to its connection */

static unsigned hash(const char *s){ unsigned h = 5381; while(*s) h = h * 33 + (unsigned char)*s++; return h % NBUCKET; }

static void clear(Cache *c){
  int i; for(i = 0; i < NBUCKET; i++){ Ent *e = c->bucket[i]; while(e){ Ent *n = e->next; sqlite3_finalize(e->st); sqlite3_free(e->text); sqlite3_free(e); e = n; } c->bucket[i] = 0; }
  c->nent = 0;
}

/* a text already prepared is reused unless it is still running (a text can call mother again inside itself: the same text, nested);
   then a second copy is prepared and kept too, so each nesting depth has its own */
static Ent *get(Cache *c, sqlite3 *db, const char *sql, char **err){
  unsigned h = hash(sql); Ent *e;
  for(e = c->bucket[h]; e; e = e->next) if(!e->busy && strcmp(e->text, sql) == 0){ sqlite3_reset(e->st); sqlite3_clear_bindings(e->st); return e; }
  if(c->nent >= 4 * NBUCKET){ int any = 0; int i; for(i = 0; i < NBUCKET && !any; i++) for(e = c->bucket[i]; e; e = e->next) if(e->busy) any = 1; if(!any) clear(c); }
  sqlite3_stmt *st = 0; const char *tail = 0;
  if(sqlite3_prepare_v3(db, sql, -1, SQLITE_PREPARE_PERSISTENT, &st, &tail) != SQLITE_OK){ *err = sqlite3_mprintf("%s", sqlite3_errmsg(db)); return 0; }
  if(!st){ *err = sqlite3_mprintf("nothing to run"); return 0; }
  if(tail && *tail){ /* several statements: not kept; run whole below */ sqlite3_finalize(st); return 0; }
  e = sqlite3_malloc(sizeof(Ent)); e->text = sqlite3_mprintf("%s", sql); e->st = st; e->busy = 0; e->next = c->bucket[h]; c->bucket[h] = e; c->nent++;
  return e;
}

static int rows(void *p, int argc, char **argv, char **col){
  char **acc = (char**)p; int i;
  char *line = sqlite3_mprintf("%s", argc ? (argv[0] ? argv[0] : "") : "");
  for(i = 1; i < argc; i++){ char *t = sqlite3_mprintf("%s | %s", line, argv[i] ? argv[i] : ""); sqlite3_free(line); line = t; }
  if(*acc){ char *t = sqlite3_mprintf("%s\n%s", *acc, line); sqlite3_free(*acc); sqlite3_free(line); *acc = t; } else *acc = line;
  return 0;
}

static void answer(sqlite3_context *ctx, char *got, char *err){
  if(err){ char *msg = sqlite3_mprintf("error: %s", err); if(trace) fprintf(stderr, "  sql< %s\n", msg); sqlite3_free(err); sqlite3_free(got); sqlite3_result_text(ctx, msg, -1, sqlite3_free); return; }
  if(got){ if(trace) fprintf(stderr, "  sql< %.120s\n", got); sqlite3_result_text(ctx, got, -1, sqlite3_free); return; }
  if(trace) fprintf(stderr, "  sql< ok\n");
  sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
}

static void motherRun(sqlite3_context *ctx, int argc, sqlite3_value **argv); static long long pnow(void); static void prof_add(const char *sql, long long ns);
static void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){ const char *sql = (const char*)sqlite3_value_text(argv[0]); long long t0 = pnow(); motherRun(ctx, argc, argv); if(sql) prof_add(sql, pnow() - t0); }
static void motherRun(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *sql = (const char*)sqlite3_value_text(argv[0]);
  char *err = 0, *got = 0; int i, rc;
  sqlite3 *db = sqlite3_context_db_handle(ctx);
  Cache *c = (Cache*)sqlite3_user_data(ctx);
  if(trace < 0) trace = getenv("NEURON_TRACE") ? 1 : 0;
  if(!sql){ sqlite3_result_text(ctx, "error: nothing to run", -1, SQLITE_STATIC); return; }
  if(trace) fprintf(stderr, "  sql> %.300s\n", sql);
  if(argc == 1 && strchr(sql, ';')){   /* a text of several statements: the prompt runs them in order, each timed for the profile */
    const char *p = sql; int bad = 0;
    while(p && *p && !bad){ sqlite3_stmt *st = 0; const char *tail = 0; long long t0 = pnow();
      if(sqlite3_prepare_v2(db, p, -1, &st, &tail) != SQLITE_OK){ err = sqlite3_mprintf("%s", sqlite3_errmsg(db)); bad = 1; break; }
      if(!st){ p = tail; continue; }
      int rc2, n = sqlite3_column_count(st);
      while((rc2 = sqlite3_step(st)) == SQLITE_ROW){ char *v[64]; int m = n < 64 ? n : 64; for(i = 0; i < m; i++) v[i] = (char*)sqlite3_column_text(st, i); rows(&got, m, v, 0); }
      if(rc2 != SQLITE_DONE){ err = sqlite3_mprintf("%s", sqlite3_errmsg(db)); bad = 1; }
      sqlite3_finalize(st); prof_add(p, pnow() - t0); p = tail; while(p && (*p == ' ' || *p == '\n')) p++; }
    if(bad){ sqlite3_free(got); got = 0; }
    answer(ctx, got, err); return;
  }
  Ent *ent = get(c, db, sql, &err); sqlite3_stmt *st = ent ? ent->st : 0;
  if(!st){
    if(err){ answer(ctx, 0, err); return; }
    if(sqlite3_exec(db, sql, rows, &got, &err) != SQLITE_OK){ sqlite3_free(got); got = 0; }
    answer(ctx, got, err); return;
  }
  for(i = 1; i < argc; i++) sqlite3_bind_value(st, i, argv[i]);
  ent->busy = 1;
  while((rc = sqlite3_step(st)) == SQLITE_ROW){
    int n = sqlite3_column_count(st), cc; char *line = sqlite3_mprintf("%s", n ? (const char*)sqlite3_column_text(st, 0) : "");
    if(!line) line = sqlite3_mprintf("");
    for(cc = 1; cc < n; cc++){ const char *v = (const char*)sqlite3_column_text(st, cc); char *t = sqlite3_mprintf("%s | %s", line, v ? v : ""); sqlite3_free(line); line = t; }
    if(got){ char *t = sqlite3_mprintf("%s\n%s", got, line); sqlite3_free(got); sqlite3_free(line); got = t; } else got = line;
  }
  if(rc != SQLITE_DONE){ err = sqlite3_mprintf("%s", sqlite3_errmsg(db)); sqlite3_free(got); got = 0; }
  sqlite3_reset(st); ent->busy = 0;
  answer(ctx, got, err);
}

/* encode(schema, text): the encoder, one pass. Letters and _ make one symbol, every other character is one symbol: the kernel's cut. A new symbol is born
   into the label table; the answer is the gates as a JSON list, for json_each. It replaces a recursive query that walked a return character by character, twice. */
static int enc_letter(unsigned char c){ return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || c == '_'; }
static int enc_u8(unsigned char c){ if(c < 0x80) return 1; if((c >> 5) == 6) return 2; if((c >> 4) == 14) return 3; if((c >> 3) == 30) return 4; return 1; }
static void encodeFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *schema = (const char*)sqlite3_value_text(argv[0]); const char *text = (const char*)sqlite3_value_text(argv[1]);
  if(!text || !schema){ sqlite3_result_text(ctx, "[]", -1, SQLITE_STATIC); return; }
  sqlite3 *db = sqlite3_context_db_handle(ctx); sqlite3_stmt *get = 0, *put = 0; size_t L = strlen(text), i = 0, cap = L * 11 + 16, n = 0; char *out = sqlite3_malloc64(cap); out[n++] = '['; int first = 1;
  char *q = sqlite3_mprintf("SELECT gate FROM %w.label WHERE symbol = ?", schema); sqlite3_prepare_v2(db, q, -1, &get, 0); sqlite3_free(q);
  q = sqlite3_mprintf("INSERT INTO %w.label (symbol) VALUES (?)", schema); sqlite3_prepare_v2(db, q, -1, &put, 0); sqlite3_free(q);
  while(i < L){
    size_t j = i; if(enc_letter((unsigned char)text[i])){ while(j < L && enc_letter((unsigned char)text[j])) j++; } else j = i + enc_u8((unsigned char)text[i]); if(j > L) j = L;
    sqlite3_int64 g = 0; sqlite3_bind_text(get, 1, text + i, (int)(j - i), SQLITE_STATIC);
    if(sqlite3_step(get) == SQLITE_ROW) g = sqlite3_column_int64(get, 0);
    sqlite3_reset(get);
    if(!g){ sqlite3_bind_text(put, 1, text + i, (int)(j - i), SQLITE_STATIC); sqlite3_step(put); sqlite3_reset(put); g = sqlite3_last_insert_rowid(db); }
    n += (size_t)sprintf(out + n, first ? "%lld" : ",%lld", (long long)g); first = 0; i = j;
  }
  out[n++] = ']'; out[n] = 0; sqlite3_finalize(get); sqlite3_finalize(put); sqlite3_result_text(ctx, out, (int)n, sqlite3_free);
}

/* the profile: what each text pasted costs, digits masked, the first 90 characters; mother_prof() answers the costliest 24 as lines */
#include <time.h>
typedef struct PEnt { char key[96]; long long n, ns; struct PEnt *next; } PEnt;
static PEnt *pbucket[4096]; static int pn;
static long long pnow(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1000000000LL + t.tv_nsec; }
static void prof_add(const char *sql, long long ns){
  char key[96]; int n = 0; for(const char *s = sql; *s && n < 94; s++){ if(*s >= '0' && *s <= '9'){ if(n && key[n-1] == '#') continue; key[n++] = '#'; } else key[n++] = *s; } key[n] = 0;
  unsigned h = 5381; for(const char *k = key; *k; k++) h = h * 33 + (unsigned char)*k; h &= 4095;
  PEnt *e; for(e = pbucket[h]; e; e = e->next) if(strcmp(e->key, key) == 0){ e->n++; e->ns += ns; return; }
  if(pn > 20000) return; e = sqlite3_malloc(sizeof(PEnt)); memcpy(e->key, key, sizeof key); e->n = 1; e->ns = ns; e->next = pbucket[h]; pbucket[h] = e; pn++;
}
static int pcmp(const void *a, const void *b){ long long x = (*(PEnt**)a)->ns, y = (*(PEnt**)b)->ns; return x < y ? 1 : x > y ? -1 : 0; }
static void profFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  PEnt **all = sqlite3_malloc(sizeof(PEnt*) * (pn ? pn : 1)); int n = 0; for(int i = 0; i < 4096; i++) for(PEnt *e = pbucket[i]; e; e = e->next) all[n++] = e;
  qsort(all, n, sizeof(PEnt*), pcmp); char *out = sqlite3_mprintf("%s", "");
  for(int i = 0; i < n && i < 24; i++){ char *t = sqlite3_mprintf("%s%.3f s | n %lld | %.2f ms | %s\n", out, all[i]->ns / 1e9, all[i]->n, all[i]->ns / 1e6 / all[i]->n, all[i]->key); sqlite3_free(out); out = t; }
  sqlite3_free(all); sqlite3_result_text(ctx, out, -1, sqlite3_free);
}

static void forget(void *p){ Cache *c = (Cache*)p; clear(c); sqlite3_free(c); }

#ifdef _WIN32
__declspec(dllexport)
#endif
int sqlite3_mother_init(sqlite3 *db, char **e, const sqlite3_api_routines *pApi){
  SQLITE_EXTENSION_INIT2(pApi);
  Cache *c = sqlite3_malloc(sizeof(Cache)); memset(c, 0, sizeof(Cache));
  sqlite3_create_function_v2(db, "mother_prof", 0, SQLITE_UTF8, 0, profFunc, 0, 0, 0);
  sqlite3_create_function_v2(db, "encode", 2, SQLITE_UTF8, 0, encodeFunc, 0, 0, 0);
  return sqlite3_create_function_v2(db, "mother", -1, SQLITE_UTF8, (void*)c, motherFunc, 0, 0, forget);
}
