# The prompt: type a line, the brain's answer is printed. The brain lives in a .db file and comes back as it was.
# usage: python3 neuron_prompt18.py <brain.db> [sat.json]   (:sheet types the teaching lines in sheet18.json, :save, :q saves and quits)
import json, os, sys, time, threading
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from host18 import Brain
sys.setrecursionlimit(200000); threading.stack_size(1 << 29)
def main():
    dbfile = sys.argv[1]
    sat = json.load(open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, 'sat172.json')))
    b = Brain(os.path.join(here, 'physics18.json'), sat=sat, dbfile=dbfile if os.path.exists(dbfile) else None)
    def run(line):
        t = time.time(); out = b.type(line)
        print(f'  [{time.time() - t:.1f} s] {out if out is not None else ""}', flush=True)
    while True:
        try: line = input('neuron> ')
        except EOFError: break
        if line == ':q': break
        if line == ':save': b.save(dbfile); print('brain saved to', dbfile); continue
        if line == ':sheet':
            for k, l in json.load(open(os.path.join(here, 'sheet18.json'))): print(k); run(l)
            continue
        if line.strip(): run(line)
    b.save(dbfile); print('brain saved to', dbfile)
th = threading.Thread(target=main); th.start(); th.join()
