#!/usr/bin/env python3
# check_faithful.py (2026-10-29): the test, written from the owner's words before the loaders were run: "you cannot loose the
# context or summerize it or change it". For every piece of the raw source, the built source brain must hold it, in order, under
# the word it belongs to. A negative control runs the same test against the morning's load (tries/20), which dropped pieces.
# usage: python3 -I check_faithful.py <raw dir> gcide <gcide.db> [limit]
#        python3 -I check_faithful.py <raw dir> wn <wn.db>
#        python3 -I check_faithful.py <raw dir> wikt <wikt.db> <every nth entry>
import os, re, sys, sqlite3, collections, json, html, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gcide_tags as G
W = re.compile(r'\w+')

def subseq(small, big):
    it = iter(big)
    return all(any(x == y for y in it) for x in small)

# ---- GCIDE: the text chunks of a paragraph (the text between its tags, entities and escapes decoded, whitespace collapsed) must
# appear in order in the row laid for each of the paragraph's words. chunk-check: no tokenizing, so a tag that stands between two
# words with no space (See<er>Couth</er>) and a tag inside a word (<it>a</it>lternating) are both judged on the text alone.
def raw_chunks(s):
    s = re.sub(r'<--.*?-->', '', s, flags=re.S)     # a page comment goes without a trace, as in the renderer (comments-no-space)
    s = re.sub(r"\\'([0-9a-f]{2})", lambda m: G.ESC.get(m.group(1), ''), s)
    s = re.sub(r'<([A-Za-z?0-9]+)/', lambda m: G.entity(m.group(1)), s)
    parts = re.split(r'</?[A-Za-z0-9]+(?:\s[^<>]*)?>', s)
    return [c for c in (re.sub(r'\s+', ' ', x).strip() for x in parts) if c]

def chunks_in(chunks, text):
    pos = 0
    for c in chunks:
        i = text.find(c, pos)
        if i < 0: return c
        pos = i + len(c)
    return None

def check_gcide(raw, dbpath, limit=None):
    db = sqlite3.connect(dbpath)
    rows = collections.defaultdict(list)
    for word, text in db.execute("SELECT word, text FROM corpus ORDER BY id"):
        rows[word].append(re.sub(r'\s+', ' ', text))
    cursor = collections.defaultdict(int)
    paras = 0; checked = 0; missing = 0; nokey = 0; examples = []
    PARA = re.compile(r'<p>(.*?)</p>', re.S); ENT = re.compile(r'<ent>(.*?)</ent>', re.S); HW = re.compile(r'<hw>(.*?)</hw>', re.S)
    dec = lambda e: re.sub(r'\s+', ' ', re.sub(r'<[^<>]*>', '', re.sub(r'<([A-Za-z?0-9]+)/', lambda m: G.entity(m.group(1)), re.sub(r"\\'([0-9a-f]{2})", lambda m: G.ESC.get(m.group(1), ''), e)))).strip()
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        s = open(os.path.join(raw, 'gcide-0.54', 'CIDE.' + letter), encoding='latin-1').read()
        ents = []
        for m in PARA.finditer(s):
            p = m.group(1); paras += 1
            es = [dec(e) for e in ENT.findall(p)]
            if es: ents = [e for e in es if e]
            elif '<hw>' in p and '<ent>' not in p and p.lstrip().startswith('<hw>'):
                ents = [re.sub(r'[*"`\u00b4\u02dd\u2016]', '', dec(HW.search(p).group(1))).strip()]
            chunks = raw_chunks(p)
            if not chunks or not ents: continue
            for e in ents:
                key = e.lower(); checked += 1
                lst = rows.get(key)
                if not lst: nokey += 1; missing += 1; examples.append((key, 'no rows')); continue
                j = cursor[key]; found = False
                if j < len(lst) and chunks_in(chunks, lst[j]) is None: cursor[key] = j + 1; found = True
                elif j + 1 < len(lst) and chunks_in(chunks, lst[j + 1]) is None: cursor[key] = j + 2; found = True
                else: cursor[key] = j + 1
                if not found:
                    missing += 1
                    if len(examples) < 12: examples.append((key, chunks_in(chunks, lst[j]) if j < len(lst) else 'no row left', chunks[:3]))
            if limit and paras >= limit: break
        if limit and paras >= limit: break
    print(f'gcide {dbpath}: paragraphs {paras}, (paragraph, word) pairs checked {checked}, missing {missing} (of which words with no rows {nokey})')
    for e in examples[:12]: print('   missing:', e)
    return missing == 0

# ---- WordNet: every synset's gloss, every lemma, every pointer's target lemmas, the frames, the lexicographer file, the sense key
def check_wn(raw, dbpath):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import build_faithful as B
    d = os.path.join(raw, 'dict')
    syn = {}; order = []
    for pos in ('noun', 'verb', 'adj', 'adv'):
        for line in open(os.path.join(d, 'data.' + pos), encoding='utf-8'):
            if line.startswith('  '): continue
            left, _, gloss = line.rstrip('\n').partition(' | '); t = left.split()
            n = int(t[3], 16); lem = [t[4 + 2 * i] for i in range(n)]
            i = 4 + 2 * n; p = int(t[i]); i += 1; ptr = []
            for _ in range(p): ptr.append((t[i], t[i + 1], t[i + 2], int(t[i + 3][:2], 16), int(t[i + 3][2:], 16))); i += 4
            s = {'ss': t[2], 'lexf': t[1], 'off': t[0], 'lem': lem, 'ptr': ptr, 'gloss': gloss.strip()}
            syn[(B.POSFILE[t[2]], t[0])] = s; order.append(s)
    db = sqlite3.connect(dbpath)
    rows = collections.defaultdict(list)
    for word, text in db.execute("SELECT word, text FROM corpus"): rows[word].append(text)
    checked = 0; missing = 0; examples = []
    for s in order:
        lemmas = [B.lemma_text(l) for l in s['lem']]
        for i, l in enumerate(s['lem'], start=1):
            bare = re.sub(r'\(.*?\)$', '', l).lower(); checked += 1
            need = [s['gloss']] + ['{' + x + '}' for x in lemmas] + ['[lexicographer file: ' + B.LEXNAMES[int(s['lexf'])] + ']']
            for sym, toff, tpos, src, tgt in s['ptr']:
                target = syn.get((B.POSFILE[tpos], toff))
                if target is None: continue
                if src == 0: need += ['{' + B.lemma_text(x) + '}' for x in target['lem']]
                elif src == i: need.append('{' + B.lemma_text(target['lem'][tgt - 1]) + '}' if tgt > 0 else '')
            ok = any(all(x in text for x in need) for text in rows.get(bare, []))
            if not ok:
                missing += 1
                if len(examples) < 10:
                    texts = rows.get(bare, [])
                    lack = [x for x in need if not any(x in t for t in texts)]
                    examples.append((bare, lack[:4]))
    print(f'wn {dbpath}: (lemma, synset) pairs checked {checked}, missing {missing}')
    for e in examples: print('   missing:', e)
    return missing == 0

# ---- Wiktionary: every string leaf of an entry that is not markup must appear in that entry's rows
MARKUP = re.compile(r'(\.links|\.bold_text_offsets|\.id$|\._dis\d*$|\.head_templates\[\]\.(name|args)|\.etymology_templates\[\]\.(name|args)'
                    r'|\.etymology_links|\.categories\[\]\.(kind|source|parents|orig|langcode|_dis)|\.sounds\[\]\.(audio|ogg_url|mp3_url)'
                    r'|^\.lang(_code)?$|\.code$|\.lang_code$|\.info_templates|\.translation$)')
def leaves(o, path, out):
    if isinstance(o, dict):
        for k, v in o.items(): leaves(v, path + '.' + k, out)
    elif isinstance(o, list):
        for v in o: leaves(v, path + '[]', out)
    elif isinstance(o, str) and o.strip() and not MARKUP.search(path): out.append((path, o))

def norm(s): return re.sub(r'\s+', ' ', s).strip()
def check_wikt(raw, dbpath, nth, src=None):
    import itertools
    db = sqlite3.connect(dbpath)
    checked = 0; missing = 0; examples = []; etyexp_missing = 0
    with open(src or os.path.join(raw, 'kaikki.org-dictionary-English.jsonl'), encoding='utf-8') as f:
        for k, line in enumerate(f):
            if k % nth: continue
            d = json.loads(line); checked += 1
            texts = [norm(t) for (t,) in db.execute("SELECT text FROM corpus WHERE word = ? AND hw = ?", (d['word'].lower(), d['word']))]
            blob = '\n'.join(texts)
            out = []; leaves(d, '', out)
            lack = []
            for path, val in out:
                if path.startswith('.etymology_templates[].expansion'):
                    if norm(val) not in blob: etyexp_missing += 1
                    continue
                if norm(val) not in blob: lack.append((path, val[:60]))
            if lack:
                missing += 1
                if len(examples) < 10: examples.append((d['word'], d['pos'], lack[:3]))
    print(f'wikt {dbpath}: entries checked {checked} (every {nth}th), entries with a missing piece {missing}; etymology template expansions not in the rows {etyexp_missing}')
    for e in examples: print('   missing:', e)
    return missing == 0

if __name__ == '__main__':
    raw, kind, dbpath = sys.argv[1], sys.argv[2], sys.argv[3]
    if kind == 'gcide': ok = check_gcide(raw, dbpath, int(sys.argv[4]) if len(sys.argv) > 4 else None)
    elif kind == 'wn': ok = check_wn(raw, dbpath)
    else: ok = check_wikt(raw, dbpath, int(sys.argv[4]) if len(sys.argv) > 4 else 100, sys.argv[5] if len(sys.argv) > 5 else None)
    print('PASS' if ok else 'FAIL')
