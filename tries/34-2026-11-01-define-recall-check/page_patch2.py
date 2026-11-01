#!/usr/bin/env python3
# g34/page_patch2.py (2026-11-01, 16:40). Three small changes, each to a defect measured live on hp:8058/full:
#  nkio.c   the bundle's rel rows carried 0 for their run, so the page never drew a relationship line (its rule asks when the run happened);
#           they now carry the run. The nodes and mem maps (722k and 1.04M entries, half the 51.6 MB) are sent for the included points only,
#           so they are written after the included set is final, just before the labels.
#  serve8.py the door kept its bundle 600 s even after a line was typed through it, so the page, which reads the brain again after its line,
#           saw no new run and nothing played; a typed line now drops the cached bundle.
#  page     a rel row laid before the history's window is there from its start; one laid inside the window appears with its run (the rule the
#           points already follow).
import sys
D = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad/g34/hp'
def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, s.count(old), old[:80])
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8').write(s); print('patched', path, len(pairs))
patch(D + '/nkio.c', [
    ('snprintf(q, sizeof q, "SELECT gate, kind, other FROM %s.rel", b->name)', 'snprintf(q, sizeof q, "SELECT gate, kind, other, run FROM %s.rel", b->name)'),
    ('sb_fmt(o, "[%d,%d,%d,0]", g, kind, other);', 'sb_fmt(o, "[%d,%d,%d,%lld]", g, kind, other, (long long)sqlite3_column_int64(ALLREL, 3));'),
    ('  sb_str(o, "],\\"nodes\\":{"); first = 1;\n'
     '  for(int g = 1; g <= b->label.n; g++){ Neuron *n = neuron_of(b, g); if(!n || !n->nnode) continue; if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "\\"%d\\":%d", g, n->nnode); }\n'
     '  sb_str(o, "},\\"mem\\":{"); first = 1;\n'
     '  for(int g = 1; g <= b->label.n; g++){ Neuron *n = neuron_of(b, g); if(!n || !n->nmem) continue; if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "\\"%d\\":%d", g, n->nmem); }\n'
     '  sb_str(o, "},\\"runs\\":["); first = 1;',
     '  sb_str(o, "],\\"runs\\":["); first = 1;'),
    ('  sb_str(o, "],\\"label\\":["); first = 1; i64 nlab = 0;',
     '  /* the definition-row and memory counts of the included points only (the page colours and lists by them), once the included set is final */\n'
     '  sb_str(o, "],\\"nodes\\":{"); first = 1;\n'
     '  for(int g = 1; g <= b->label.n; g++){ if(!inc[g]) continue; Neuron *n = neuron_of(b, g); if(!n || !n->nnode) continue; if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "\\"%d\\":%d", g, n->nnode); }\n'
     '  sb_str(o, "},\\"mem\\":{"); first = 1;\n'
     '  for(int g = 1; g <= b->label.n; g++){ if(!inc[g]) continue; Neuron *n = neuron_of(b, g); if(!n || !n->nmem) continue; if(!first) sb_str(o, ","); first = 0; sb_fmt(o, "\\"%d\\":%d", g, n->nmem); }\n'
     '  sb_str(o, "},\\"label\\":["); first = 1; i64 nlab = 0;'),
])
patch(D + '/serve8.py', [
    ("                t = time.time(); r = ask(f'type {schema} {text}'); RUNS.append(r.get('run'))\n",
     "                t = time.time(); r = ask(f'type {schema} {text}'); RUNS.append(r.get('run')); BUNDLE['d'] = None   # the page reads the brain again after its line: it must see this run\n"),
])
patch(D + '/NEURON-POINT-OF-CONNECTION-nk-2026-10-30.html', [
    ("    REL.forEach(function (r) { if (atRun(r[3])) add(r[0], r[2], relKind(r[1]), .8); });",
     "    REL.forEach(function (r) { if (!r[3] || RUNT0[r[3]] === undefined || RUNT0[r[3]] <= tk) add(r[0], r[2], relKind(r[1]), .8); });   // a rel row laid before this history's window is there from its start; one laid inside it appears with its run"),
])
