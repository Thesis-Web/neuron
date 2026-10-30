#!/usr/bin/env python3
# build_faithful.py (2026-10-29): lays WordNet 3.1 and GCIDE 0.54 as source brains keeping ALL their context (the owner, 10-29:
# "if you strip formating, or put the data into a shape that is more usable that is ok, but you cannot loose the context or
# summerize it or change it, it is used to find meanings later and must be accurate"). The shape of a source brain is the one
# every source has had since v5 (me, corpus, inbox, outbox, the work and carry triggers), so the door's attachment and the
# brain's ask are untouched. What is reshaped, and how, is in NOTE.md; every label word is the source's own name for the thing.
# usage: python3 -I build_faithful.py <raw dir> <out dir> wn gcide
import os, re, sys, sqlite3, time, collections, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gcide_tags as G

GATES = {'wn': 7, 'gcide': 8, 'moby': 11}
SHAPE = """
CREATE TABLE me (gate INTEGER NOT NULL);
INSERT INTO me VALUES ({gate});
CREATE TABLE corpus (id INTEGER PRIMARY KEY, word TEXT NOT NULL, hw TEXT, text TEXT NOT NULL);
CREATE TABLE inbox (id INTEGER PRIMARY KEY, run INTEGER, cell INTEGER, about INTEGER, word TEXT);
CREATE TABLE outbox (id INTEGER PRIMARY KEY, run INTEGER, cell INTEGER, about INTEGER, text TEXT);
CREATE TRIGGER work AFTER INSERT ON inbox BEGIN
  INSERT INTO outbox (run, cell, about, text) SELECT NEW.run, NEW.cell, NEW.about, text FROM corpus WHERE word = NEW.word ORDER BY id;
  DELETE FROM inbox WHERE id = NEW.id;
END;
CREATE TRIGGER carry AFTER INSERT ON outbox BEGIN
  SELECT mother('INSERT INTO main.secondary (run, cell, gate, about, text) VALUES (' || NEW.run || ', ' || NEW.cell || ', ' || (SELECT gate FROM me) || ', ' || NEW.about || ', ' || quote(NEW.text) || ')');
  DELETE FROM outbox WHERE id = NEW.id;
END;"""

def lay(name, rows, out):
    p = os.path.join(out, name + '.db')
    if os.path.exists(p): os.remove(p)
    db = sqlite3.connect(p)
    db.executescript(SHAPE.format(gate=GATES[name]))
    db.executemany("INSERT INTO corpus (word, hw, text) VALUES (?, ?, ?)", rows)
    db.execute("CREATE INDEX corpus_word ON corpus (word)")
    db.commit()
    n, w, b = db.execute("SELECT count(*), count(DISTINCT word), sum(length(text)) FROM corpus").fetchone()
    db.close()
    print(f"{name}: {n} rows, {w} words, {b} chars of text, {os.path.getsize(p) // 1024} KB", flush=True)

# ------------------------------------------------------------------ WordNet 3.1
# wninput(5WN): the pointer symbols and their names; wndb(5WN): the lexicographer file numbers and names.
POINTER = {'!': 'ant', '@': 'hypernym', '@i': 'instance hypernym', '~': 'hyponym', '~i': 'instance hyponym',
  '#m': 'member holonym', '#s': 'substance holonym', '#p': 'part holonym', '%m': 'member meronym', '%s': 'substance meronym',
  '%p': 'part meronym', '=': 'attribute', '+': 'derivationally related form', ';c': 'domain of synset topic',
  '-c': 'member of this domain topic', ';r': 'domain of synset region', '-r': 'member of this domain region',
  ';u': 'domain of synset usage', '-u': 'member of this domain usage', '*': 'entailment', '>': 'cause', '^': 'also see',
  '$': 'verb group', '&': 'similar to', '<': 'participle of verb', '\\': 'pertainym'}
LEXNAMES = '''adj.all adj.pert adv.all noun.Tops noun.act noun.animal noun.artifact noun.attribute noun.body noun.cognition
noun.communication noun.event noun.feeling noun.food noun.group noun.location noun.motive noun.object noun.person noun.phenomenon
noun.plant noun.possession noun.process noun.quantity noun.relation noun.shape noun.state noun.substance noun.time verb.body
verb.change verb.cognition verb.communication verb.competition verb.consumption verb.contact verb.creation verb.emotion verb.motion
verb.perception verb.possession verb.social verb.stative verb.weather adj.ppl'''.split()
POSNAME = {'n': 'noun', 'v': 'verb', 'a': 'adjective', 's': 'adjective satellite', 'r': 'adverb'}
POSFILE = {'n': 'noun', 'v': 'verb', 'a': 'adj', 's': 'adj', 'r': 'adv'}

def lemma_text(l): return l.replace('_', ' ')

def wordnet(raw, out):
    d = os.path.join(raw, 'dict')
    syn = {}   # (pos file, offset) -> dict
    order = []
    for pos in ('noun', 'verb', 'adj', 'adv'):
        with open(os.path.join(d, 'data.' + pos), encoding='utf-8') as f:
            for line in f:
                if line.startswith('  '): continue
                left, _, gloss = line.rstrip('\n').partition(' | ')
                t = left.split()
                off, lexf, ss = t[0], t[1], t[2]
                n = int(t[3], 16); lem = [(t[4 + 2 * i], t[5 + 2 * i]) for i in range(n)]
                i = 4 + 2 * n; p = int(t[i]); i += 1
                ptr = []
                for _ in range(p):
                    sym, toff, tpos, st = t[i], t[i + 1], t[i + 2], t[i + 3]; i += 4
                    ptr.append((sym, toff, tpos, int(st[:2], 16), int(st[2:], 16)))
                frames = []
                if ss == 'v':
                    fcount = int(t[i]); i += 1
                    for _ in range(fcount):
                        frames.append((int(t[i + 1]), int(t[i + 2], 16))); i += 3
                s = {'off': off, 'lexf': lexf, 'ss': ss, 'lem': lem, 'ptr': ptr, 'frames': frames, 'gloss': gloss.strip()}
                syn[(POSFILE[ss], off)] = s; order.append(s)
    # index.sense: sense_key synset_offset sense_number tag_cnt  (the sense number and the tagged count per lemma sense)
    sense = {}
    with open(os.path.join(d, 'index.sense'), encoding='utf-8') as f:
        for line in f:
            key, off, num, cnt = line.split()
            lemma = key.split('%')[0]; sense[(lemma, off)] = (key, int(num), int(cnt))
    frametext = {}
    with open(os.path.join(d, 'verb.Framestext'), encoding='utf-8') as f:
        for line in f:
            if line.strip(): k, _, v = line.strip().partition(' '); frametext[int(k)] = v.strip()
    sents = {}
    with open(os.path.join(d, 'sents.vrb'), encoding='utf-8') as f:
        for line in f:
            if line.strip(): k, _, v = line.strip().partition(' '); sents[int(k)] = v
    sentidx = {}
    with open(os.path.join(d, 'sentidx.vrb'), encoding='utf-8') as f:
        for line in f:
            if line.strip(): k, _, v = line.strip().partition(' '); sentidx[k] = [int(x) for x in v.split(',') if x]
    rows = []
    for s in order:
        lemmas = [lemma_text(l) for l, _ in s['lem']]
        syn_br = '[syn: ' + ', '.join('{' + l + '}' for l in lemmas) + ']'
        # semantic pointers (source 0): every lemma row; lexical pointers: the row of the source lemma, naming the target lemma
        sem = collections.OrderedDict(); lex = collections.defaultdict(lambda: collections.OrderedDict())
        for sym, toff, tpos, src, tgt in s['ptr']:
            name = POINTER.get(sym, sym)
            if sym == '\\' and s['ss'] == 'r': name = 'derived from adjective'
            target = syn.get((POSFILE[tpos], toff))
            if target is None: continue
            if src == 0:
                sem.setdefault(name, []).extend('{' + lemma_text(l) + '}' for l, _ in target['lem'])
            else:
                tl = lemma_text(target['lem'][tgt - 1][0]) if tgt > 0 else ', '.join(lemma_text(l) for l, _ in target['lem'])
                lex[src].setdefault(name, []).append('{' + tl + '}')
        sem_br = ''.join(f' [{k}: ' + ', '.join(v) + ']' for k, v in sem.items())
        frames_all = [frametext[fn] for fn, w in s['frames'] if w == 0]
        for i, (l, lexid) in enumerate(s['lem'], start=1):
            lt = lemma_text(l)
            bare = re.sub(r'\(.*?\)$', '', l).lower()
            key, num, cnt = sense.get((bare, s['off']), (None, None, None))
            parts = [f"{POSNAME[s['ss']]} {num if num is not None else '?'}: {s['gloss']} {syn_br}{sem_br}"]
            parts.append(''.join(f' [{k}: ' + ', '.join(v) + ']' for k, v in lex[i].items()))
            fr = frames_all + [frametext[fn] for fn, w in s['frames'] if w == i]
            if fr: parts.append(' [frames: ' + '; '.join(fr) + ']')
            if key and key in sentidx:
                parts.append(' [examples: ' + '; '.join(sents[n].replace('%s', bare) for n in sentidx[key] if n in sents) + ']')
            parts.append(f" [lexicographer file: {LEXNAMES[int(s['lexf'])]}]")
            if key: parts.append(f" [sense key: {key}] [tag count: {cnt}]")
            rows.append((bare, lt, ''.join(parts)))
    # the exception lists (morphology): inflected form -> base form(s), one row per line, keyed by the inflected form
    for pos in ('noun', 'verb', 'adj', 'adv'):
        with open(os.path.join(d, pos + '.exc'), encoding='utf-8') as f:
            for line in f:
                t = line.split()
                if t: rows.append((lemma_text(t[0]).lower(), lemma_text(t[0]), f"[{POSNAME[{'noun':'n','verb':'v','adj':'a','adv':'r'}[pos]]} exceptions: " + ' '.join(lemma_text(x) for x in t) + ']'))
    lay('wn', rows, out)

# ------------------------------------------------------------------ GCIDE 0.54
TOK = re.compile(r"<--.*?-->|<([A-Za-z?0-9]+)/|</([A-Za-z0-9]+)>|<([A-Za-z0-9]+)(?:\s[^<>]*)?>|\\'([0-9a-f]{2})|[^<\\]+|.", re.S)
def render(s):
    """GCIDE markup -> text: entities and escapes become their characters, typographic tags go, semantic tags become [label: ...]."""
    out = []; stack = []
    for m in TOK.finditer(s):
        ent, close, open_, esc = m.group(1), m.group(2), m.group(3), m.group(4)
        if m.group(0).startswith('<--'): continue
        if ent is not None: out.append(G.entity(ent)); continue
        if esc is not None: out.append(G.ESC.get(esc, "\\'" + esc)); continue
        if open_ is not None:
            if open_ == 'p': continue
            if open_ in G.TYPO or G.TYPO_RE.match(open_): stack.append((open_, False)); continue
            if out and re.search(r'\w$', out[-1]): out.append(' ')
            out.append('[' + G.LABEL.get(open_, open_) + ': '); stack.append((open_, True)); continue
        if close is not None:
            if close == 'p': continue
            # close the nearest open tag of this name; tags left open above it are closed too (GCIDE's nesting is not strict)
            if any(t == close for t, _ in stack):
                while stack:
                    t, labelled = stack.pop()
                    if labelled: out.append(']')
                    if t == close: break
            continue
        if out and out[-1].endswith(']') and re.match(r'\w', m.group(0)): out.append(' ')
        out.append(m.group(0))
    while stack:
        t, labelled = stack.pop()
        if labelled: out.append(']')
    t = ''.join(out)
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'\[([^\[\]:]+): \]', '', t)     # an empty labelled field
    return t.strip()

def ent_key(e):
    """the lookup key of an entry word: GCIDE's <ent> is the headword without accent or syllable marks; lowercased (the brain's symbols are case-sensitive; this is the convention since the slice)"""
    return e.lower()
def hw_to_ent(hw):
    return re.sub(r'[*"`´˝‖]', '', render(hw)).strip()

PARA = re.compile(r'<p>(.*?)</p>', re.S)
ENT_RE = re.compile(r'<ent>(.*?)</ent>', re.S); HW_RE = re.compile(r'<hw>(.*?)</hw>', re.S)
def gcide(raw, out):
    rows = []; stray = 0; noent = 0
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        s = open(os.path.join(raw, 'gcide-0.54', 'CIDE.' + letter), encoding='latin-1').read()
        ents = []; pos = 0
        def emit(text):
            if not text: return
            for e in ents: rows.append((ent_key(e), e, text))
        for m in PARA.finditer(s):
            between = s[pos:m.start()]; pos = m.end()
            bt = render(between)
            if bt and ents: emit(bt); stray += 1          # text that sits outside every paragraph (a table, a factbook extract): it belongs to the entry above
            p = m.group(1)
            es = [render(x) for x in ENT_RE.findall(p)]
            if es: ents = [e for e in es if e]
            elif '<hw>' in p and not ents or ('<hw>' in p and '<ent>' not in p and HW_RE.search(p) and p.lstrip().startswith('<hw>')):
                ents = [hw_to_ent(HW_RE.search(p).group(1))]; noent += 1   # an entry that begins with <hw> and has no <ent>
            emit(render(p))
        bt = render(s[pos:])
        if bt and ents: emit(bt); stray += 1
    print(f'gcide: {stray} stray text blocks outside paragraphs kept, {noent} entries keyed by their <hw> (no <ent>)', flush=True)
    lay('gcide', rows, out)

if __name__ == '__main__':
    raw, out = sys.argv[1], sys.argv[2]
    for name in sys.argv[3:]:
        t = time.time()
        {'wn': wordnet, 'gcide': gcide}[name](raw, out)
        print(f'  {name}: {time.time() - t:.1f} s', flush=True)
