#!/bin/bash
# hub-go2.sh (2026-11-01): the encoder in one function (the kernel's cut rule), the door served between hops, no re-reading of the lines on a typed line.
log(){ echo "$(date +%H:%M:%S) $*"; }
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; log "door down"
cd $HUB/brain
python3 - <<'PY'
s = open("mother7.c").read()
a = "static void forget(void *p){"
b = r'''/* encode(schema, text): the encoder, one pass. Letters and _ make one symbol, every other character is one symbol: the kernel's cut. A new symbol is born
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

static void forget(void *p){'''
assert s.count(a) == 1; s = s.replace(a, b)
a = "  return sqlite3_create_function_v2(db, \"mother\", -1, SQLITE_UTF8, (void*)c, motherFunc, 0, 0, forget);"
b = "  sqlite3_create_function_v2(db, \"encode\", 2, SQLITE_UTF8, 0, encodeFunc, 0, 0, 0);\n" + a
assert s.count(a) == 1; open("mother7.c", "w").write(s.replace(a, b))
s = open("bottom7.py").read()
a = """            n += 1
        db.execute('COMMIT'); self.commits += 1; self.hops[s] += n"""
b = """            n += 1
            self.serve()   # the door between hops: a typed line and a read never wait for a batch
        db.execute('COMMIT'); self.commits += 1; self.hops[s] += n"""
assert s.count(a) == 1; s = s.replace(a, b)
a = """    def batch(self, s):"""
b = """    def serve(self):
        while not self.jobs.empty():
            fn, out = self.jobs.get()
            try: out['result'] = fn(self.db)
            except Exception as e: out['error'] = e
            out['done'].set()
    def batch(self, s):"""
assert s.count(a) == 1; s = s.replace(a, b)
a = """            while not self.jobs.empty():
                fn, out = self.jobs.get()
                try: out['result'] = fn(self.db)
                except Exception as e: out['error'] = e
                out['done'].set()
            self.env.changed.set()"""
b = """            self.serve()
            self.env.changed.set()"""
assert s.count(a) == 1; open("bottom7.py", "w").write(s.replace(a, b))
s = open("../page/serve7.py").read()
a = "if not bottom7.RUNS and os.path.exists(LINES): bottom7.match_runs"
b = "if '{run:' in j.args['line'] and not bottom7.RUNS and os.path.exists(LINES): bottom7.match_runs"
assert s.count(a) == 1; open("../page/serve7.py", "w").write(s.replace(a, b))
PY
gcc -shared -fPIC -O2 -o mother.so mother7.c -I. 2>&1 | grep -E "error" | head -n 5 | cut -c1-170; ls -la mother.so | cut -c24-70
python3 -I - <<'PY'
import sqlite3
for path, S in (("brain.db", "main"), ("sixth.db", "sixth")):
    db = sqlite3.connect(path, isolation_level=None, timeout=60); db.execute("PRAGMA journal_mode = WAL")
    sec = db.execute("SELECT sql FROM sqlite_master WHERE type='trigger' AND name='secondary_go'").fetchone()[0]
    if "encode(" in sec: print(S, "already"); continue
    i = sec.index("  INSERT INTO label (symbol) SELECT s FROM (WITH RECURSIVE ch"); j = sec.index(" INSERT OR REPLACE INTO run_sheet (run, cell, state, value) SELECT parent, cell, 1, id FROM run")
    new = sec[:i] + f"  INSERT INTO seq (run, pos, gate) SELECT (SELECT max(id) FROM run), key + 1, value FROM json_each(encode('{S}', NEW.text));\n" + sec[j:]
    db.execute("BEGIN IMMEDIATE"); db.execute("DROP TRIGGER secondary_go"); db.execute(new); db.execute("COMMIT"); print(S, "encoder in"); db.close()
print(sqlite3.connect("brain.db").execute("SELECT sql FROM sqlite_master WHERE name='label'").fetchone()[0][:120])
PY
log "laid"; cd $HUB/page; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
log "door up"; echo FINISHED
