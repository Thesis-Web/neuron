/* Mother: route only.
   mother(destination, payload)

   sqlite -> execute SQL, return ok/error
   other  -> deposit payload in addressed mailbox

   No interpretation, no decisions, no queues in C.
*/

#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1

static void motherFunc(sqlite3_context *ctx, int argc,
                       sqlite3_value **argv) {
    (void)argc;

    const char *dest =
        (const char *)sqlite3_value_text(argv[0]);
    const char *payload =
        (const char *)sqlite3_value_text(argv[1]);

    sqlite3 *db = sqlite3_context_db_handle(ctx);
    char *err = 0;

    if (!dest || !payload) {
        sqlite3_result_text(ctx,
            "error: missing destination or payload",
            -1, SQLITE_STATIC);
        return;
    }

    if (sqlite3_stricmp(dest, "sqlite") == 0) {
        if (sqlite3_exec(db, payload, 0, 0, &err)
            != SQLITE_OK) {
            char *msg = sqlite3_mprintf("error: %s",
                err ? err : "unknown");
            sqlite3_result_text(ctx, msg, -1, sqlite3_free);
            sqlite3_free(err);
            return;
        }

        sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
        return;
    }

    sqlite3_stmt *stmt = 0;
    int rc = sqlite3_prepare_v2(db,
        "INSERT INTO mailbox_out(destination,payload)"
        " VALUES(?1,?2)",
        -1, &stmt, 0);

    if (rc == SQLITE_OK) {
        sqlite3_bind_text(stmt, 1, dest, -1,
                          SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, payload, -1,
                          SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
    }

    if (rc != SQLITE_DONE) {
        char *msg = sqlite3_mprintf("error: %s",
            sqlite3_errmsg(db));
        sqlite3_result_text(ctx, msg, -1, sqlite3_free);
    } else {
        sqlite3_result_text(ctx, "ok", -1, SQLITE_STATIC);
    }

    sqlite3_finalize(stmt);
}

int sqlite3_mother_init(sqlite3 *db, char **e,
                        const sqlite3_api_routines *api) {
    (void)e;
    SQLITE_EXTENSION_INIT2(api);

    return sqlite3_create_function(
        db, "mother", 2, SQLITE_UTF8,
        0, motherFunc, 0, 0);
}
