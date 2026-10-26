/* mother(text): the brain hands SQL text to mother. She runs it at the SQL prompt and answers
   'ok' or 'error: ...'. She never stops the brain, so a refusal can be felt and remembered.
   After the text ran, she carries what the source brains put in their outboxes into the brain's
   secondary input, and empties the outboxes. She decides nothing and works no data.
   Build:  gcc -shared -fPIC -o mother.so mother.c        Load in sqlite3:  .load ./mother   */
#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1
#include <string.h>

static void carry(sqlite3 *db){
  /* every attached database that has an outbox: copy its rows into main.secondary, then empty it */
  sqlite3_stmt *dbs = 0;
  if(sqlite3_prepare_v2(db, "SELECT name FROM pragma_database_list WHERE name NOT IN ('main','temp')", -1, &dbs, 0) != SQLITE_OK) return;
  while(sqlite3_step(dbs) == SQLITE_ROW){
    const char *src = (const char*)sqlite3_column_text(dbs, 0);
    char *q = sqlite3_mprintf(
      "INSERT INTO main.secondary (run, source, word, hw, text) SELECT run, %Q, word, hw, text FROM \"%w\".outbox; DELETE FROM \"%w\".outbox;",
      src, src, src);
    sqlite3_exec(db, q, 0, 0, 0);   /* a source with no outbox table is simply not a source brain */
    sqlite3_free(q);
  }
  sqlite3_finalize(dbs);
}

static void tell(sqlite3 *db, sqlite3_value *run, const char *msg){
  /* mother(text, run): what came back that was not 'ok' goes into the run's output, so the brain hears it */
  if(!run || sqlite3_value_type(run) == SQLITE_NULL) return;
  char *q = sqlite3_mprintf("INSERT INTO main.output (run, text) VALUES (%lld, %Q)", sqlite3_value_int64(run), msg);
  sqlite3_exec(db, q, 0, 0, 0); sqlite3_free(q);
}

static int rows(void *p, int argc, char **argv, char **col){
  /* what a SELECT sent back, one row per line, columns parted by " | " */
  char **acc = (char**)p; int i;
  char *line = sqlite3_mprintf("%s", argc ? (argv[0] ? argv[0] : "") : "");
  for(i = 1; i < argc; i++){ char *t = sqlite3_mprintf("%s | %s", line, argv[i] ? argv[i] : ""); sqlite3_free(line); line = t; }
  if(*acc){ char *t = sqlite3_mprintf("%s\n%s", *acc, line); sqlite3_free(*acc); sqlite3_free(line); *acc = t; } else *acc = line;
  return 0;
}

static void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *sql = (const char*)sqlite3_value_text(argv[0]);
  sqlite3_value *run = argc > 1 ? argv[1] : 0;
  char *err = 0, *got = 0;
  sqlite3 *db = sqlite3_context_db_handle(ctx);
  if(!sql){ tell(db, run, "error: nothing to run"); sqlite3_result_text(ctx, "error: nothing to run", -1, SQLITE_STATIC); return; }
  if(sqlite3_exec(db, sql, rows, &got, &err) != SQLITE_OK){
    sqlite3_free(got);
    if(err && strstr(err, "database table is locked")){
      /* SQLite refuses this inside a run (a DROP while the run itself is still executing). It waits for the run to end. */
      char *q = sqlite3_mprintf("INSERT INTO main.later (text) VALUES (%Q)", sql);
      sqlite3_exec(db, q, 0, 0, 0); sqlite3_free(q); sqlite3_free(err);
      tell(db, run, "later");
      sqlite3_result_text(ctx, "later", -1, SQLITE_STATIC); return;
    }
    char *msg = sqlite3_mprintf("error: %s", err ? err : "unknown");
    tell(db, run, msg);
    sqlite3_result_text(ctx, msg, -1, sqlite3_free); sqlite3_free(err); carry(db); return;
  }
  carry(db);
  if(got){ sqlite3_result_text(ctx, got, -1, sqlite3_free); return; }
  sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
}

#ifdef _WIN32
__declspec(dllexport)
#endif
int sqlite3_mother_init(sqlite3 *db, char **e, const sqlite3_api_routines *pApi){
  SQLITE_EXTENSION_INIT2(pApi);
  int rc = sqlite3_create_function(db, "mother", 1, SQLITE_UTF8 | SQLITE_INNOCUOUS, 0, motherFunc, 0, 0);
  if(rc == SQLITE_OK) rc = sqlite3_create_function(db, "mother", 2, SQLITE_UTF8 | SQLITE_INNOCUOUS, 0, motherFunc, 0, 0);
  return rc;
}
