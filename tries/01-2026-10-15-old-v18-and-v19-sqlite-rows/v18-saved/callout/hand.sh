#!/bin/bash
# the hand: runs whatever SQL the brain wrote into call, in order, then marks it done. decides nothing.
db="$1"
max=$(sqlite3 "$db" "SELECT max(id) FROM call WHERE done IS NULL")
[ -z "$max" ] && exit 0
sqlite3 "$db" "SELECT sql || ';' FROM call WHERE done IS NULL AND id <= $max ORDER BY id" | sqlite3 -bail "$db" \
  && sqlite3 "$db" "UPDATE call SET done = CURRENT_TIMESTAMP WHERE done IS NULL AND id <= $max"
