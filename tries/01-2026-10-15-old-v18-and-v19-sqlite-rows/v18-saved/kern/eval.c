/* eval(sql): run SQL text from inside SQLite, on the same connection. */
#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1
static void evalFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *sql = (const char*)sqlite3_value_text(argv[0]);
  char *err = 0;
  if(!sql) return;
  sqlite3 *db = sqlite3_context_db_handle(ctx);
  if(sqlite3_exec(db, sql, 0, 0, &err) != SQLITE_OK){
    sqlite3_result_error(ctx, err ? err : "eval failed", -1); sqlite3_free(err); return;
  }
  sqlite3_result_int(ctx, 1);
}
int sqlite3_eval_init(sqlite3 *db, char **e, const sqlite3_api_routines *pApi){
  SQLITE_EXTENSION_INIT2(pApi);
  return sqlite3_create_function(db, "eval", 1, SQLITE_UTF8, 0, evalFunc, 0, 0);
}
