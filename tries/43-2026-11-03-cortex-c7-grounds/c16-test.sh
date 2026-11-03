#!/bin/bash
# C16 grounds: the live test as run on 2026-11-03 13:42 to 13:50 CST from the hub (every verb runs on hp2)
C='ssh -o BatchMode=yes hp2 /home/james/.local/bin/cortex'
# 1. receipts: the machine's own print piped in (the model's hand never retypes it)
ssh hp2 df -h / | $C receipt audit 1 df -h /
ssh hp2 free -m | $C receipt audit 2 free -m
# 2. claims made before the receipt existed: labeled "no print at its time", not judged by it
$C judge audit 1 266432      # 392g test line: supersedes by shape, part refused (the owner rejected it at 13:20), the 393g part stands
$C judge audit 1 266417      # 393g: completes by receipt (a later print confirming an earlier value counts)
$C judge audit 2 268126      # free 300 at 02:10: completes by shape, label: newest print reads 458
# 3. claims made after the receipt
$C ingest audit "df -h / printed 392g avail on the root filesystem at 13:50"      # -> hallucination 1.000 by receipt, 49 ms
$C ingest audit "the mem row of free -m now reads free 458 megabytes"             # -> progresses 1.000 by receipt, 54 ms
$C ingest audit "the mem row of free -m now reads free 300 megabytes"             # kept (values in the restate key) -> hallucination by receipt, 48 ms
# (judge each run the ingest printed: cortex judge audit <n> <run>)
# 4. sources
$C source cortex-handler reference : "CORTEX-HANDLER.md, the frozen handler of the cortex, its code doc, sha 3e831a35, frozen 2026-11-02 21:10; as of 2026-11-02"
ssh hp2 cat /home/james/cortex/CORTEX-HANDLER.md | $C source cortex-handler -     # 167 sentences in 3.2 s
$C source owner-words owner : "the owner own words on the cortex, 574 messages 2026-09-01 to 2026-11-02 ...; as of 2026-11-02"
# scp the Downloads file to hp2:/tmp/sources/owner-words.md, then on hp2: timeout 600 cortex source owner-words - < /tmp/sources/owner-words.md
# 5. where the owner reads it
$C questions audit
$C verdicts audit
$C hydrate audit --at 1
$C hydrate audit --at 2
