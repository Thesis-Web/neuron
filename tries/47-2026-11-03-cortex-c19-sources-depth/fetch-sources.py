# fetch public-domain reference texts onto hp2, strip the Gutenberg boilerplate, register each as a reference source, type it in (C19 sources depth, 2026-11-03)
# usage: python3 -I fetch-sources.py manifest.json   (manifest: [{"name","url","note","asof"}, ...]); files land in /tmp/sources/dl/<name>/ each in its own folder
import sys, json, os, re, time, subprocess, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) cortex-source-fetch/1.0"}
C = "/home/james/.local/bin/cortex"
man = json.load(open(sys.argv[1])); box = time.time() + 15 * 60
for m in man:
    if time.time() > box: print("time box reached; stopping before", m["name"]); break
    d = "/tmp/sources/dl/" + m["name"]; os.makedirs(d, exist_ok=True); f = d + "/raw.txt"; t0 = time.time(); b = None
    urls = [m["url"]] if m.get("url") else ["https://www.gutenberg.org/ebooks/%d.txt.utf-8" % m["id"], "https://www.gutenberg.org/cache/epub/%d/pg%d.txt" % (m["id"], m["id"]), "https://www.gutenberg.org/files/%d/%d-0.txt" % (m["id"], m["id"]), "https://www.gutenberg.org/files/%d/%d-8.txt" % (m["id"], m["id"]), "https://www.gutenberg.org/files/%d/%d.txt" % (m["id"], m["id"])]
    for u in urls:
        try: b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read(); m["url"] = u; break
        except Exception as e: err = str(e)[:80]
    if b is None: print(m["name"], "fetch failed:", err); continue
    if m.get("tar"):
        import tarfile, io
        tf = tarfile.open(fileobj=io.BytesIO(b), mode="r:bz2"); parts = []
        for mem in tf.getmembers():
            if mem.isfile() and any(("/" + pre) in mem.name for pre in m["tar"]) and mem.name.endswith(".txt"): parts.append(tf.extractfile(mem).read().decode("utf-8", "replace"))
        b = "\n\n".join(parts).encode()
    if m.get("url", "").endswith(".html"):
        import html as _h
        t = b.decode("utf-8", "replace"); t = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", t); t = re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</li>|</div>|</tr>", "\n", t); t = re.sub(r"<[^>]+>", " ", t); t = _h.unescape(t); b = t.encode()
    open(f, "wb").write(b); t = b.decode("utf-8", "replace")
    a = re.search(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK[^\n]*\n", t); z = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK", t)
    if a and z: t = t[a.end():z.start()]
    t = re.sub(r"\r", "", t); t = re.sub(r"\n(?!\n)", " ", t)   # a paragraph is one line; the sentence splitter does the rest
    open(d + "/body.txt", "w").write(t)
    print("%s: fetched %d bytes in %.1fs, body %d bytes" % (m["name"], len(b), time.time() - t0, len(t)), flush=True)
    r = subprocess.run([C, "source", m["name"], "reference", ":", "%s; from %s; as of %s" % (m["note"], m["url"], m["asof"])], capture_output=True, text=True); print("  " + (r.stdout.strip() or r.stderr.strip())[:140], flush=True)
    t1 = time.time(); r = subprocess.run([C, "source", m["name"], "-"], stdin=open(d + "/body.txt"), capture_output=True, text=True, timeout=max(60, box - time.time()))
    print("  " + (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-200:]), "| %.0fs" % (time.time() - t1), flush=True)
