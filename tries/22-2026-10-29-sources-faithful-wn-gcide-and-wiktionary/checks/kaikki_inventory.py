import json, sys, collections
paths = collections.Counter(); strbytes = collections.Counter(); samples = {}
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, path + '.' + k)
    elif isinstance(o, list):
        for v in o: walk(v, path + '[]')
    else:
        paths[path] += 1
        if isinstance(o, str): strbytes[path] += len(o)
        if path not in samples: samples[path] = repr(o)[:80]
n = 0
with open(sys.argv[1], encoding='utf-8') as f:
    for line in f:
        walk(json.loads(line), ''); n += 1
print('entries', n)
for p, c in sorted(paths.items(), key=lambda x: -strbytes[x[0]]):
    print(f'{c:10d} {strbytes[p]/1e6:10.1f}MB {p}  e.g. {samples[p]}')
