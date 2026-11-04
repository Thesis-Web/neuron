# the RECEIPTS line of a hydration: the newest three commands only, those the expected names first (a session's prints land on the open checkpoint, related or not)
p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''        if rc: lines.append("RECEIPTS (the machine's own prints for C%d, the newest of each command): " % nxt + " | ".join("%s => %s [%s]" % (cmd, " / ".join(receipt_line(l)[:70] for l in d.get("lines", [])[:3]), time.strftime("%m-%d %H:%M", time.localtime(d.get("ts", 0)))) for cmd, d in rc.items()))
'''
new = '''        if rc:
            et = toks(ex[3]) if ex else set()
            order = sorted(rc.items(), key=lambda kv: (0 if toks(kv[0]) & et else 1, -kv[1].get("ts", 0)))[:3]   # the prints the expected names first, then the newest; three at most
            lines.append("RECEIPTS (the machine's own prints for C%d, %d commands, the newest of each; showing %d): " % (nxt, len(rc), len(order)) + " | ".join("%s => %s [%s]" % (cmd[:50], " / ".join(receipt_line(l)[:70] for l in d.get("lines", [])[:3]), time.strftime("%m-%d %H:%M", time.localtime(d.get("ts", 0)))) for cmd, d in order))
'''
assert s.count(old) == 1; s = s.replace(old, new); open(p, "w").write(s); print("patched c20c")
