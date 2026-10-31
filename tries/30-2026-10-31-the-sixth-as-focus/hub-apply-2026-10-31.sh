#!/bin/bash
# hub-apply-2026-10-31.sh: the fixes proven on the twin, applied to the live hub brain. For the owner to run; the permission system would not let the model stop the door.
#   ! bash /mnt/d/Neuron/tries/30-2026-10-31-the-sixth-as-focus/hub-apply-2026-10-31.sh
# What it does, in order:
#   stops the 8056 door (its open batch rolls back, the mailbox keeps its rows)
#   copies brain.db, sixth.db, bottom7.py and serve7.py to D:\Neuron-sources\backups\before-focus-2026-10-31
#   widens the hop mailbox (p7, p8) in both brains
#   drops the landings of defines the old line sent and never began (their runs stay as rows; their unknowns go back to waiting)
#   the first nap of tries/26: landings and call-less hits of ended runs; the receipts stay
#   clears seen's call so the old observing line (the sweep) does not fire again
#   puts in the router that reads p7, p8 (tries/27) and the door with the one-read graph (tries/30)
#   starts the door on 8056 and types the focus lines, the seven hop lines and the sixth's hop line
# To undo: stop the door, copy the four files back from the backup folder, start serve7.py 8056 in the page folder.
set -e
HERE=$(cd "$(dirname "$0")" && pwd); T27=/mnt/d/Neuron/tries/27-2026-10-30-the-hop-laid-again
L=/tmp/claude-1000/-home-exnulla-neuron-v3/4e06790d-7d80-473e-8cc8-4014a0561261/scratchpad/w/19
B=/mnt/d/Neuron-sources/backups/before-focus-2026-10-31
PID=$(pgrep -f '^python3 -u -I serve7\.py 8056$' || true)
if [ -n "$PID" ]; then echo "stopping the door, process $PID"; kill "$PID"; while kill -0 "$PID" 2>/dev/null; do sleep 1; done; fi
cd "$L/brain"
echo "checkpoint"; sqlite3 brain.db 'PRAGMA wal_checkpoint(TRUNCATE);' > /dev/null; sqlite3 sixth.db 'PRAGMA wal_checkpoint(TRUNCATE);' > /dev/null
echo "backup to $B"; mkdir -p "$B"; cp brain.db sixth.db bottom7.py "$B/"; cp "$L/page/serve7.py" "$B/"
for f in brain.db sixth.db; do
  if [ "$(sqlite3 "$f" "SELECT count(*) FROM pragma_table_info('hop') WHERE name = 'p7'")" = "0" ]; then sqlite3 "$f" 'ALTER TABLE hop ADD COLUMN p7; ALTER TABLE hop ADD COLUMN p8;'; fi
done
echo "the mailbox and the nap"
sqlite3 brain.db "SELECT 'mailbox before', count(*) FROM hop; DELETE FROM hop WHERE p2 = 1 AND p3 = 153 AND p1 IN (SELECT id FROM run r WHERE r.arrival = 5 AND r.kind = 0 AND NOT EXISTS (SELECT 1 FROM run_memory m WHERE m.run = r.id)); SELECT 'mailbox after', count(*) FROM hop; DELETE FROM land WHERE run IN (SELECT run FROM run_memory); DELETE FROM hit WHERE call IS NULL AND spawn IS NULL AND run IN (SELECT run FROM run_memory); SELECT 'land left', count(*) FROM land; SELECT 'hit left', count(*) FROM hit; SELECT 'receipts kept', count(*) FROM run_receipt; PRAGMA wal_checkpoint(TRUNCATE);"
sqlite3 sixth.db 'UPDATE "82" SET call = NULL WHERE before = 6 AND trigger = 68; PRAGMA wal_checkpoint(TRUNCATE);' > /dev/null
cp "$T27/bottom7.py" "$L/brain/bottom7.py"; cp "$HERE/serve7.py" "$L/page/serve7.py"
echo "starting the door"; cd "$L/page"; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done
python3 -I "$HERE/hub-drive.py" 8056 lines "$HERE/HUB-FOCUS-LINES-2026-10-31.txt" "$T27/HOP-LINES-2026-10-30.txt" "$HERE/SIXTH-HOP-LINE.txt" | cut -c1-150
echo "done: open http://localhost:8056/ and reload it; define : main runs on top if typed again"
