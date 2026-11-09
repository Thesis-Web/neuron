#!/bin/bash
# tries/59: the test brain refreshed from the live stored brain (the live kernel never stopped); the test kernel and door stopped by exact pid
cd ~/nk-roots; for p in $(pgrep -f "^./nk 7009 "); do kill $p; done; for p in $(pgrep -f "serve8.py 8059"); do kill $p; done; sleep 2
pgrep -f "^./nk 7009 " && echo "test kernel still up" || echo "test kernel stopped"; rm -f out/brain.map out/brain.map.main.db out/brain.map.sixth.db out/brain.map.xyz
bash setup.sh
