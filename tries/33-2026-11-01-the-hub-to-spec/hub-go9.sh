#!/bin/bash
# hub-go9.sh: a profile inside mother (what each pasted text costs); the node-table test by key, not a catalogue scan; the page rereads every 120 s.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; log "door down"
cd $HUB/brain; python3 -I - <<'PY'
import sqlite3
s = open("mother7.c").read()
if "mother_prof" not in s:
    a = "static void forget(void *p){"
    b = r'''/* the profile: what each text pasted costs, digits masked, the first 90 characters; mother_prof() answers the costliest 24 as lines */
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

static void forget(void *p){'''
    assert s.count(a) == 1; s = s.replace(a, b)
    a = "static void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){\n  const char *sql = (const char*)sqlite3_value_text(argv[0]);"
    b = "static void motherRun(sqlite3_context *ctx, int argc, sqlite3_value **argv);\nstatic void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){ const char *sql = (const char*)sqlite3_value_text(argv[0]); long long t0 = pnow(); motherRun(ctx, argc, argv); if(sql) prof_add(sql, pnow() - t0); }\nstatic void motherRun(sqlite3_context *ctx, int argc, sqlite3_value **argv){\n  const char *sql = (const char*)sqlite3_value_text(argv[0]);"
    assert s.count(a) == 1; s = s.replace(a, b)
    a = "  sqlite3_create_function_v2(db, \"encode\", 2,"
    b = "  sqlite3_create_function_v2(db, \"mother_prof\", 0, SQLITE_UTF8, 0, profFunc, 0, 0, 0);\n" + a
    assert s.count(a) == 1; s = s.replace(a, b)
    open("mother7.c", "w").write(s); print("mother: profile in")
for path, S in (("brain.db", "main"), ("sixth.db", "sixth")):
    db = sqlite3.connect(path, isolation_level=None, timeout=120); db.execute("PRAGMA journal_mode = WAL")
    sec = db.execute("SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = 'secondary_go'").fetchone()[0]
    a = "AND NOT EXISTS (SELECT 1 FROM sqlite_master WHERE name = about || '.node');"
    b = "AND NOT EXISTS (SELECT 1 FROM pragma_table_info(about || '.node', 'main'));" if S == "main" else "AND NOT EXISTS (SELECT 1 FROM pragma_table_info(about || '.node', 'sixth'));"
    if a in sec:
        db.execute("BEGIN IMMEDIATE"); db.execute("DROP TRIGGER secondary_go"); db.execute(sec.replace(a, b)); db.execute("COMMIT"); print(S, "node test by key")
    db.close()
p = "../page/NEURON-POINT-OF-CONNECTION-v6-2026-10-29.html"; s = open(p, encoding="utf-8").read()
s = s.replace("render(TK, true); }); }).catch(function () {}); }, 45000);", "render(TK, true); }); }).catch(function () {}); }, 120000);"); open(p, "w", encoding="utf-8").write(s)
PY
gcc -shared -fPIC -O2 -o mother.so mother7.c -I. 2>&1 | grep -E "error" | head -n 5 | cut -c1-170; ls -la mother.so | cut -c24-70
cd $HUB/page; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; echo FINISHED
