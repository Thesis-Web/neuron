#!/bin/bash
# timing.sh: lines of known tokens (every token already a neuron), typed into the brain the chain left behind.
cd "$(dirname "$0")"
SRC="sources/wn.db sources/gcide.db sources/mw.db sources/mwt.db sources/moby.db sources/map.db sources/sqldoc.db"
unit="shard INTEGER PRIMARY KEY , arrival INTEGER , "   # 16 tokens (spaces included)
for n in 600 1200 2400; do
  reps=$(( n / 16 ))
  line=""; for ((i=0;i<reps;i++)); do line+="$unit"; done
  toks=$(python3 -c "import re,sys; print(len(re.findall(r'[A-Za-z_]+|[^A-Za-z_]', sys.argv[1])))" "$line")
  echo "### $toks tokens, first time (rows written where new)"; printf '%s\n' "$line" | python3 bottom.py brain.db $SRC 2>/dev/null | grep -E '^\s*\[|run ' | cut -c1-100
  echo "### $toks tokens, again (every row a hit)"; printf '%s\n' "$line" | python3 bottom.py brain.db $SRC 2>/dev/null | grep -E '^\s*\[|run ' | cut -c1-100
done
sqlite3 brain.db "SELECT 'shards', n FROM shards; SELECT 'receipts', count(*) FROM receipt; SELECT 'runs', count(*) FROM input;"
