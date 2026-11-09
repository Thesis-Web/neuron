# tries/61: which acting points are a prefix or suffix by the Wiktionary source (its entries "-X" suffix, "X-" prefix), and what the common affixes hold. Reads only, by key.
import sys, json; sys.path.insert(0, ".")
from nkdoor import Door
d = Door(sys.argv[1]); j = json.load(open(sys.argv[2]))
L = {int(k): v for k, v in j["label"].items()}; acting = sorted(set(r[0] for r in j["rows"]))
def pos(word):
    rows = d.q("SELECT text FROM wikt.corpus WHERE word = ?", [word])
    return [r[0].split("[part of speech: ")[1].split("]")[0] for r in rows if "[part of speech: " in r[0]]
hits = []
for g in acting:
    w = L[g]
    for form in ("-" + w.lower(), w.lower() + "-"):
        p = pos(form)
        if p: hits.append((w, g, form, p))
print("acting points read:", len(acting), "| those with a Wiktionary affix entry:", hits)
print("== the common affixes as points: label, gate, dna rows (any), node rows, and the parts of speech Wiktionary gives the bare form and the affix form")
for w, form in [("re","re-"),("un","un-"),("pre","pre-"),("dis","dis-"),("ing","-ing"),("ed","-ed"),("s","-s"),("ly","-ly"),("ness","-ness"),("er","-er")]:
    g = d.gate(w)
    if not g: print(w, "no point"); continue
    dna = d.q("SELECT shard, before, trigger, call, spawn, times FROM dna WHERE gate = ?", [g])
    nodes = d.q("SELECT count(*) FROM node WHERE gate = ?", [g])[0][0]
    print("%-5s gate %-7s dna rows %-3d acting %d | node rows %-4d | wikt '%s': %s | wikt '%s': %s" % (w, g, len(dna), sum(1 for x in dna if x[3] or x[4]), nodes, w, sorted(set(pos(w))), form, sorted(set(pos(form)))))
print("hyphen forms as points:", [(f, d.gate(f)) for f in ["-ing", "re-", "un-", "-ed"]])
