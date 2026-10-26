#!/bin/bash
# install.sh: build the kernel and put it, the lay files and the source scripts where the neuron user can read them.
# The brain can read these and cannot write them (blueprint §3).
set -e
B=/home/james/neuron-build
cd $B/kernel && systemd-run --user --scope -q -p MemoryMax=1500M -p MemorySwapMax=0 go build -o /tmp/ndry/neuron . && sudo -n install -o root -g root -m 755 /tmp/ndry/neuron /usr/local/bin/neuron
sudo -n mkdir -p /opt/neuron/lay /opt/neuron/bin /opt/neuron/kernel
sudo -n install -o root -g root -m 644 $B/kernel/*.go /opt/neuron/kernel/
sudo -n rm -f /opt/neuron/lay/*.lay
sudo -n install -o root -g root -m 644 $B/lay/*.lay /opt/neuron/lay/
if ls $B/sources/bin/* >/dev/null 2>&1; then sudo -n install -o root -g root -m 755 $B/sources/bin/* /opt/neuron/bin/; fi
echo "installed: $(wc -l < <(cat $B/kernel/*.go)) kernel lines, $(ls /opt/neuron/lay | wc -l) lay files, $(ls /opt/neuron/bin 2>/dev/null | wc -l) source scripts"
