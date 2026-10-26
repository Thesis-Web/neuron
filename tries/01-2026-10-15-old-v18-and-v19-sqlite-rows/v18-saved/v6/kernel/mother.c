/* mother(sql): the brain hands SQL text to the mother. She runs it and answers
   'ok' or 'error: ...'. She never stops the brain, so a refusal can be felt and remembered. */
#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1
static void motherFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *sql = (const char*)sqlite3_value_text(argv[0]);
  char *err = 0;
  if(!sql){ sqlite3_result_text(ctx, "error: nothing to run", -1, SQLITE_STATIC); return; }
  if(sqlite3_exec(sqlite3_context_db_handle(ctx), sql, 0, 0, &err) != SQLITE_OK){
    char *msg = sqlite3_mprintf("error: %s", err ? err : "unknown");
    sqlite3_result_text(ctx, msg, -1, sqlite3_free); sqlite3_free(err); return;
  }
  sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
}
int sqlite3_mother_init(sqlite3 *db, char **e, const sqlite3_api_routines *pApi){
  SQLITE_EXTENSION_INIT2(pApi);
  return sqlite3_create_function(db, "mother", 1, SQLITE_UTF8, 0, motherFunc, 0, 0);
}
