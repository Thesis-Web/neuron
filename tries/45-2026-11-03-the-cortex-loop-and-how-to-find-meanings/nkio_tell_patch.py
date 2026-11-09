#!/usr/bin/env python3
# nkio_tell_patch.py (2026-11-03, tries/45): the kernel's own tell, READY and NOT LIVE (C15's remainder; the owner's word is needed for a
# rebuild and restart). A client that sends the line "tell" is kept open; whenever the timeline or the run count grew (after a request
# was handled, after pending work was pumped) the kernel writes one line {"clock","runs","tl"} to it, without blocking (a client that does
# not read is dropped). The door's stream thread would hold that client and tell every page stream. No timer: the kernel speaks when it
# laid a receipt. usage: python3 nkio_tell_patch.py <copy of nkio.c>
import sys
path = sys.argv[1]; t = open(path, encoding='utf-8').read()
old = "static volatile sig_atomic_t STOP; static void on_stop(int n){ STOP = 1; }"
assert t.count(old) == 1, 'STOP line'
new = """/* tries/45: the kernel tells. One client at a time (the door), kept open after it sends "tell"; a line whenever receipts were laid. */
static int TELL_FD = -1; static i64 TOLD_NTL = -1, TOLD_RUNS = -1;
static void tell_now(void){
  if(TELL_FD < 0) return; if(MAINB.ntl == TOLD_NTL && MAINB.nruns == TOLD_RUNS) return;
  char line[160]; int n = snprintf(line, sizeof line, "{\\"clock\\":%lld,\\"runs\\":%lld,\\"tl\\":%lld}\\n", (long long)MAINB.clock, (long long)MAINB.nruns, (long long)MAINB.ntl);
  if(send(TELL_FD, line, n, MSG_DONTWAIT | MSG_NOSIGNAL) != n){ close(TELL_FD); TELL_FD = -1; return; }
  TOLD_NTL = MAINB.ntl; TOLD_RUNS = MAINB.nruns;
}
""" + old
t = t.replace(old, new)
old = "    if(r <= 0){ if(busy) pump_all(256); continue; }"
assert t.count(old) == 1, 'pump line'
t = t.replace(old, "    if(r <= 0){ if(busy) pump_all(256); tell_now(); continue; }   /* tries/45: pending work that ended a run is told */")
old = "    if(req.s){ char *nl = strchr(req.s, '\\n'); if(nl) *nl = 0; SB o = {0}; handle(req.s, &o);"
assert t.count(old) == 1, 'handle line'
t = t.replace(old, "    if(req.s){ char *nl = strchr(req.s, '\\n'); if(nl) *nl = 0; if(strcmp(req.s, \"tell\") == 0){ if(TELL_FD >= 0) close(TELL_FD); TELL_FD = c; TOLD_NTL = -1; TOLD_RUNS = -1; free(req.s); tell_now(); continue; }   /* tries/45: this client is kept and told */\n      SB o = {0}; handle(req.s, &o);")
old = "    free(req.s); close(c);\n"
assert t.count(old) == 1, 'close line'
t = t.replace(old, "    free(req.s); close(c); tell_now();   /* tries/45: a request that laid receipts is told at once */\n")
open(path, 'w', encoding='utf-8').write(t)
print('patched', path, ': the tell verb, a line to the kept client whenever receipts were laid')
