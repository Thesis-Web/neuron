/* neuron.c: functions compiled INTO the brain's own sqlite3. Today: eval. Later: neuron functions. */
#include "sqlite3.h"
static void evalFunc(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const char *sql = (const char*)sqlite3_value_text(argv[0]);
  char *err = 0;
  if(!sql) return;
  if(sqlite3_exec(sqlite3_context_db_handle(ctx), sql, 0, 0, &err) != SQLITE_OK){
    sqlite3_result_error(ctx, err ? err : "eval failed", -1); sqlite3_free(err); return;
  }
  sqlite3_result_int(ctx, 1);
}
static int neuron_open(sqlite3 *db, char **e, const void *api){
  return sqlite3_create_function(db, "eval", 1, SQLITE_UTF8, 0, evalFunc, 0, 0);
}
int neuron_init(const char *unused){            /* runs once when SQLite starts */
  return sqlite3_auto_extension((void(*)(void))neuron_open);   /* every connection gets eval */
}
