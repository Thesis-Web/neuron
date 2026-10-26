/* mother(text): the brain hands mother SQL text. She runs it at the SQL prompt and answers what SQLite answered:
   'ok', the rows a SELECT sent back (one row per line, columns parted by " | "), or 'error: <SQLite's reason>'.
   She never stops the brain: a refusal is an answer like any other. When a source brain's outbox says it is populated
   (SQLite tells her the moment a row lands there), she carries those rows into the brain's input as lines arriving
   from that source's gate, and empties the outbox. She parses nothing, decides nothing and keeps nothing.
   NEURON_TRACE=1 in the environment makes her print every text she runs to stderr, so you can watch the SQL prompt.
   Build:  gcc -shared -fPIC -O2 -o mother.so mother.c -I.      Load in sqlite3:  .load ./mother   */
#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

static int trace = -1;
static int populated = 0;   /* set by SQLite the moment a row lands in a source brain's outbox */

static void hook(void *p, int op, const char *dbname, const char *table, sqlite3_int64 rowid){
  if(op == SQLITE_INSERT && strcmp(table, "outbox") == 0 && strcmp(dbname, "main") != 0) populated = 1;
}

static void carry(sqlite3 *db){
  /* an outbox said it is populated: every attached database with an outbox has its rows become input lines of the
     main brain, arriving from that source's gate, and is emptied. Nothing is swept when nothing was written. */
  sqlite3_stmt *dbs = 0;
  if(!populated) return;
  populated = 0;
  if(sqlite3_prepare_v2(db, "SELECT name FROM pragma_database_list WHERE name NOT IN ('main','temp')", -1, &dbs, 0) != SQLITE_OK) return;
  while(sqlite3_step(dbs) == SQLITE_ROW){
    const char *src = (const char*)sqlite3_column_text(dbs, 0);
    char *q = sqlite3_mprintf(
      "INSERT INTO main.input (text, parent, arrival) SELECT text, run, (SELECT gate FROM main.encoder WHERE word = %Q) FROM \"%w\".outbox ORDER BY id; DELETE FROM \"%w\".outbox;",
      src, src, src);
    sqlite3_exec(db, q, 0, 0, 0);   /* a database with no outbox table is simply not a source brain */
    sqlite3_free(q);
  }
  sqlite3_finalize(dbs);
}

static int rows(void *p, int argc, char **argv, char **col){
  char **acc = (char**)p; int i;
  char *line = sqlite3_mprintf("%s", argc ? (argv[0] ? argv[0] : "") : "");
  for(i = 1; i < argc; i++){ char *t = sqlite3_mprintf("%s | %s", line, argv[i] ? argv[i] : ""); sqlite3_free(line); line = t; }
  if(*acc){ char *t = sqlite3_mprintf("%s\n%s", *acc, line); sqlite3_free(*acc); sqlite3_free(line); *acc = t; } else *acc = line;
  return 0;
}

static void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *sql = (const char*)sqlite3_value_text(argv[0]);
  char *err = 0, *got = 0;
  sqlite3 *db = sqlite3_context_db_handle(ctx);
  if(trace < 0) trace = getenv("NEURON_TRACE") ? 1 : 0;
  if(!sql){ sqlite3_result_text(ctx, "error: nothing to run", -1, SQLITE_STATIC); return; }
  if(trace) fprintf(stderr, "  sql> %s\n", sql);
  if(sqlite3_exec(db, sql, rows, &got, &err) != SQLITE_OK){
    sqlite3_free(got);
    char *msg = sqlite3_mprintf("error: %s", err ? err : "unknown");
    if(trace) fprintf(stderr, "  sql< %s\n", msg);
    sqlite3_free(err);
    sqlite3_result_text(ctx, msg, -1, sqlite3_free);
    carry(db);
    return;
  }
  carry(db);
  if(got){ if(trace) fprintf(stderr, "  sql< %s\n", got); sqlite3_result_text(ctx, got, -1, sqlite3_free); return; }
  if(trace) fprintf(stderr, "  sql< ok\n");
  sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
}

#ifdef _WIN32
__declspec(dllexport)
#endif
int sqlite3_mother_init(sqlite3 *db, char **e, const sqlite3_api_routines *pApi){
  SQLITE_EXTENSION_INIT2(pApi);
  sqlite3_update_hook(db, hook, 0);
  return sqlite3_create_function(db, "mother", 1, SQLITE_UTF8 | SQLITE_INNOCUOUS, 0, motherFunc, 0, 0);
}
