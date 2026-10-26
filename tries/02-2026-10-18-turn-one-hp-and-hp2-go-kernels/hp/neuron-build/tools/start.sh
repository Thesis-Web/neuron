#!/bin/bash
# start.sh: start the live brain by hand as user neuron, inside a memory cap, so a runaway can never take hp down.
# No auto-restart: killing it ends it (blueprint 12.3); a power loss is resumed by running this again.
# usage: tools/start.sh            (resumes /home/neuron/brain.db; a first birth needs /opt/neuron/lay)
set -e
if pgrep -u neuron -x neuron >/dev/null; then echo "the brain is already running"; exit 1; fi
LAY=""
if ! sudo -n test -s /home/neuron/brain.db; then LAY=/opt/neuron/lay; fi
sudo -n systemctl stop neuron-brain.scope 2>/dev/null || true
sudo -n systemd-run --unit=neuron-brain --uid=neuron --gid=neuron --working-directory=/home/neuron \
  -p MemoryMax=2G -p MemorySwapMax=0 -p TasksMax=512 -p OOMPolicy=kill \
  --setenv=HOME=/home/neuron --setenv=USER=neuron --setenv=GOMEMLIMIT=1200MiB --setenv=PATH=/usr/local/bin:/usr/bin:/bin \
  -q bash -c "exec /usr/local/bin/neuron run $LAY >> /home/neuron/run.out 2>&1"
sleep 2
systemctl status neuron-brain --no-pager 2>/dev/null | sed -n '1,3p;/Memory/p'
sg neuron -c 'tail -2 /home/neuron/acts.log' 2>/dev/null || true
