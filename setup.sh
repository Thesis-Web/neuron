#!/bin/bash
# tries/58: a test brain in its own folder (10-30 rule): a copy of the stored brain and its own copy of the sources; the live kernel never stopped
cd ~/nk-roots; t0=$(date +%s)
echo "live before: $(curl -s -m 5 http://127.0.0.1:8058/api/info | python3 -c "import sys,json; s=json.load(sys.stdin)[\"stats\"][\"main\"]; print(s[\"runs\"], s[\"defined\"], s[\"gates\"], s[\"refused\"])")"
cp ~/nk/sources/*.db sources/; echo "sources copied $(($(date +%s)-t0)) s"
for f in main sixth; do sqlite3 ~/nk/out/brain.map.$f.db ".backup out/brain.map.$f.db"; done; cp ~/nk/out/brain.map.xyz out/; echo "side files copied $(($(date +%s)-t0)) s"
cp --sparse=always ~/nk/out/brain.map out/brain.map; echo "brain.map copied $(($(date +%s)-t0)) s, $(du -sh out/brain.map | cut -f1) real"
(NK_MAP=$HOME/nk-roots/out/brain.map nohup ./nk 7009 egg-symbols.txt sources wn gcide mwt moby map sqldoc measured guess wikt > nk.log 2>&1 < /dev/null &)
for i in $(seq 1 300); do python3 -c "import socket; socket.create_connection((\"127.0.0.1\", 7009), timeout=1).close()" 2>/dev/null && break; sleep 1; done
echo "kernel: $(tail -n 1 nk.log)"
(nohup python3 serve8.py 8059 7009 NEURON-POINT-OF-CONNECTION-nk-2026-10-30.html LINES-nk.txt FIRST-RUNS-nk.txt 127.0.0.1 > door.log 2>&1 < /dev/null &); sleep 3
echo "door: $(cat door.log | tail -1)"
echo "test  after: $(curl -s -m 20 http://127.0.0.1:8059/api/info | python3 -c "import sys,json; j=json.load(sys.stdin); s=j[\"stats\"][\"main\"]; print(j[\"ready\"], s[\"runs\"], s[\"defined\"], s[\"gates\"], s[\"refused\"])")"
echo "live  after: $(curl -s -m 5 http://127.0.0.1:8058/api/info | python3 -c "import sys,json; s=json.load(sys.stdin)[\"stats\"][\"main\"]; print(s[\"runs\"], s[\"defined\"], s[\"gates\"], s[\"refused\"])")"
echo "DONE $(($(date +%s)-t0)) s"
