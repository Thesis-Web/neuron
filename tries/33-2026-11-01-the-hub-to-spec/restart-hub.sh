#!/bin/bash
HUB=/home/exnulla/neuron/hub; P=$(pgrep -f 'serve7[.]py 8056'); [ -n "$P" ] && { kill $P; while kill -0 $P 2>/dev/null; do sleep 1; done; }; echo "$(date +%H:%M:%S) door down"
cd $HUB/page; setsid nohup python3 -u -I serve7.py 8056 > door8056.log 2>&1 < /dev/null &
for i in $(seq 1 300); do curl -s -m 3 http://localhost:8056/api/info 2>/dev/null | grep -q '"ready": true' && break; sleep 2; done; echo "$(date +%H:%M:%S) door up"; echo FINISHED
