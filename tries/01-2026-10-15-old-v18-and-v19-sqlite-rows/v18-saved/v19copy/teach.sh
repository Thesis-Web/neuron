#!/usr/bin/env bash
# teach.sh <file>: run one teaching file against the brain (eval loaded, recursive triggers on).
set -euo pipefail
cd "$(dirname "$0")"
[ $# -eq 1 ] || { echo "usage: ./teach.sh teach/1_base.sql" >&2; exit 2; }
sqlite3 -bail brain.db ".load ./kernel/eval" "PRAGMA recursive_triggers = ON;" ".read $1"
