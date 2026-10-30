#!/usr/bin/env python3
# build_wikt.py (2026-10-29): lays Wiktionary (the kaikki.org extract of the English Wiktionary, one JSON entry per line) as a
# source brain in the shape every source has (me, corpus, inbox, outbox, work, carry), keeping ALL its content (the owner, 10-29).
# Every string in an entry is laid under the entry's word, except what is markup or machinery, listed in MARKUP in
# check_faithful.py and in NOTE.md: wiki links, byte offsets, machine ids, template names and arguments (their expansions stay),
# category machinery (the category name stays), audio file names and URLs, language codes (the language name stays), and a
# field that only repeats another ("translation" beside "english"). Labels are kaikki's own field names, spaced.
# Rows of an entry, in order: the head (word, part of speech, etymology, forms, pronunciation, categories ...), one row per
# sense, a row per group of translations of a sense, and a row per list of related words at the entry level.
# usage: python3 -I build_wikt.py <kaikki jsonl> <out.db> [gate] [--no-translations] [--lean]   (gate: the symbol's gate in main, set later)
# --lean (the call of 2026-10-29 evening, the owner's to overrule): the slice the brain reads. Left out: translations (other languages' labels
# for the meaning, which no source of the brain describes), descendants (the word's forms in other languages), categories (Wiktionary's own
# housekeeping: 'Terms with Abkhaz translations', 'Pages with 2 entries'), wikidata ids. Everything else stays. The full file is built without it.
import os, re, sys, json, sqlite3, time
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
DROP = {'links', 'bold_text_offsets', 'id', 'code', 'lang_code', 'info_templates', 'etymology_links', 'ogg_url', 'mp3_url', 'audio'}
RELS = ['synonyms', 'antonyms', 'hypernyms', 'hyponyms', 'meronyms', 'holonyms', 'troponyms', 'coordinate_terms', 'related',
        'derived', 'descendants', 'instances', 'abbreviations', 'alt_of', 'form_of']
def ws(s): return re.sub(r'\s+', ' ', s).strip()
def label(k): return k.replace('_', ' ')

def item(d, first=('word', 'form', 'text', 'ipa', 'enpr', 'rhymes', 'homophone', 'date', 'name')):
    """one dict of a list (a synonym, a form, an example, a sound, a translation ...): its main value, then every other field as field=value"""
    if isinstance(d, str): return ws(d)
    parts = []; done = set()
    for k in first:
        if k in d and isinstance(d[k], str): parts.append(ws(d[k])); done.add(k); break
    for k, v in d.items():
        if k in done or k in DROP or k.startswith('_dis'): continue
        if k == 'translation' and d.get('english') == v: continue
        if isinstance(v, str): parts.append(f'{label(k)}: {ws(v)}') if v.strip() else None
        elif isinstance(v, list):
            vs = [item(x) if isinstance(x, dict) else ws(str(x)) for x in v]
            vs = [x for x in vs if x]
            if vs: parts.append(f'{label(k)}: ' + ', '.join(vs))
        elif isinstance(v, dict):
            s = item(v, first=())
            if s: parts.append(f'{label(k)}: {s}')
        elif v is not None and not isinstance(v, bool): parts.append(f'{label(k)}: {v}')
    return ' | '.join(p for p in parts if p)

def lst(name, items):
    vs = [item(x) for x in items]; vs = [v for v in vs if v]
    return f' [{label(name)}: ' + '; '.join(vs) + ']' if vs else ''

def categories(cs):
    names = []
    for c in cs:
        n = c.get('name') if isinstance(c, dict) else c
        if n and n not in names: names.append(n)
    return ' [categories: ' + '; '.join(names) + ']' if names else ''

def translations_rows(head, trs, where):
    """translations grouped by their sense string; each row: [translations of <where> (<sense>): lang: word (roman) ...]"""
    groups = {}
    for t in trs:
        groups.setdefault(ws(t.get('sense', '')), []).append(t)
    rows = []
    for sense, ts in groups.items():
        parts = []
        for t in ts:
            p = [ws(t.get('lang', '?')) + ': ' + ws(t.get('word', '') or '')]
            for k in ('roman', 'alt', 'english', 'note', 'taxonomic'):
                if t.get(k): p.append(f'{label(k)}: {ws(t[k])}')
            for k in ('tags', 'raw_tags', 'topics'):
                if t.get(k): p.append(f'{label(k)}: ' + ', '.join(ws(str(x)) for x in t[k]))
            other = {k: v for k, v in t.items() if k not in ('lang', 'word', 'sense', 'roman', 'alt', 'english', 'note', 'taxonomic', 'tags', 'raw_tags', 'topics') and k not in DROP and not k.startswith('_dis') and not (k == 'translation' and t.get('english') == v)}
            if other: p.append(item(other, first=()))
            parts.append(' | '.join(x for x in p if x))
        rows.append(f'{head} [translations of {where}' + (f' ({sense})' if sense else '') + ': ' + '; '.join(parts) + ']')
    return rows

LEAN = False
def entry_rows(d, with_translations=True):
    word, pos = d['word'], d.get('pos', '?')
    head = f'[word: {word}] [part of speech: {pos}]' + (f" [etymology {d['etymology_number']}]" if d.get('etymology_number') else '')
    rows = []
    h = [head]
    for ht in d.get('head_templates', []):
        if ht.get('expansion'): h.append(f" [head: {ws(ht['expansion'])}]")
    if d.get('forms'): h.append(lst('forms', d['forms']))
    ety = ws(d.get('etymology_text', ''))
    if ety: h.append(f' [etymology: {ety}]')
    extra = [ws(t['expansion']) for t in d.get('etymology_templates', []) if t.get('expansion') and ws(t['expansion']) not in ety]
    seen = []
    for e in extra:
        if e not in seen: seen.append(e)
    if seen: h.append(' [etymology templates: ' + '; '.join(seen) + ']')
    if d.get('sounds'): h.append(lst('pronunciation', d['sounds']))
    if d.get('hyphenations'):
        hy = []
        for x in d['hyphenations']:
            if isinstance(x, dict):
                rest = {k: v for k, v in x.items() if k != 'parts'}
                hy.append('\u2027'.join(x.get('parts', [])) + ((' | ' + item(rest, first=())) if rest else ''))
            else: hy.append(str(x))
        h.append(' [hyphenation: ' + '; '.join(x for x in hy if x) + ']')
    for k in ('wikipedia', 'wikidata', 'categories', 'source', 'original_title'):
        if d.get(k):
            if LEAN and k in ('categories', 'wikidata'): continue
            if k == 'categories': h.append(categories(d[k]))
            elif isinstance(d[k], list): h.append(f' [{label(k)}: ' + '; '.join(ws(str(x)) for x in d[k]) + ']')
            else: h.append(f' [{label(k)}: {ws(str(d[k]))}]')
    known = {'word', 'pos', 'etymology_number', 'head_templates', 'forms', 'etymology_text', 'etymology_templates', 'sounds', 'hyphenations',
             'wikipedia', 'wikidata', 'categories', 'source', 'original_title', 'senses', 'translations', 'lang', 'lang_code', 'etymology_links', 'info_templates'} | set(RELS)
    for k, v in d.items():
        if k in known or k in DROP: continue
        if isinstance(v, list): h.append(lst(k, v))
        elif isinstance(v, str) and v.strip(): h.append(f' [{label(k)}: {ws(v)}]')
        elif isinstance(v, dict): h.append(f' [{label(k)}: {item(v, first=())}]')
    rows.append(''.join(h))
    for n, sn in enumerate(d.get('senses', []), start=1):
        raw = [ws(g) for g in sn.get('raw_glosses', [])]; gl = [ws(g) for g in sn.get('glosses', [])]
        text = '; '.join(raw) if raw else '; '.join(gl)
        s = [f'{pos} {n}: {text}' if text else f'{pos} {n}:']
        if raw and gl and not all(g in text for g in gl): s.append(' [glosses: ' + '; '.join(gl) + ']')
        for k in ('tags', 'raw_tags', 'topics'):
            if sn.get(k): s.append(f' [{label(k)}: ' + ', '.join(ws(str(x)) for x in sn[k]) + ']')
        if sn.get('qualifier'): s.append(f" [qualifier: {ws(sn['qualifier'])}]")
        if sn.get('examples'): s.append(lst('examples', sn['examples']))
        for k in RELS:
            if sn.get(k): s.append(lst(k, sn[k]))
        if sn.get('attestations'): s.append(lst('attestations', sn['attestations']))
        for k in ('senseid', 'wikipedia', 'wikidata'):
            if LEAN and k == 'wikidata': continue
            if sn.get(k): s.append(f' [{label(k)}: ' + '; '.join(ws(str(x)) for x in sn[k]) + ']')
        if sn.get('categories') and not LEAN: s.append(categories(sn['categories']))
        known_s = {'raw_glosses', 'glosses', 'tags', 'raw_tags', 'topics', 'qualifier', 'examples', 'attestations', 'senseid', 'wikipedia', 'wikidata', 'categories', 'translations', 'id', 'links', 'info_templates'} | set(RELS)
        for k, v in sn.items():
            if k in known_s or k in DROP: continue
            if isinstance(v, list): s.append(lst(k, v))
            elif isinstance(v, str) and v.strip(): s.append(f' [{label(k)}: {ws(v)}]')
            elif isinstance(v, dict): s.append(f' [{label(k)}: {item(v, first=())}]')
            elif v is not None and not isinstance(v, bool): s.append(f' [{label(k)}: {v}]')
        rows.append(''.join(s))
        if with_translations and sn.get('translations'):
            rows += translations_rows(head, sn['translations'], f'{pos} {n}')
    for k in RELS:
        if LEAN and k == 'descendants': continue
        if d.get(k): rows.append(head + lst(k, d[k]))
    if with_translations and d.get('translations'):
        rows += translations_rows(head, d['translations'], pos)
    return rows

def main():
    src, out = sys.argv[1], sys.argv[2]
    gate = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 0
    global LEAN
    LEAN = '--lean' in sys.argv
    with_tr = '--no-translations' not in sys.argv and not LEAN
    if os.path.exists(out): os.remove(out)
    db = sqlite3.connect(out); db.executescript(SHAPE.format(gate=gate))
    db.execute('PRAGMA journal_mode = OFF'); db.execute('PRAGMA synchronous = OFF')
    t = time.time(); n = 0; rows = 0; batch = []
    with open(src, encoding='utf-8') as f:
        for line in f:
            d = json.loads(line); n += 1
            for text in entry_rows(d, with_tr):
                batch.append((d['word'].lower(), d['word'], text))
            if len(batch) >= 20000:
                db.executemany("INSERT INTO corpus (word, hw, text) VALUES (?, ?, ?)", batch); rows += len(batch); batch = []
            if n % 100000 == 0: print(f'  {n} entries, {rows} rows, {time.time() - t:.0f} s', flush=True)
    if batch: db.executemany("INSERT INTO corpus (word, hw, text) VALUES (?, ?, ?)", batch); rows += len(batch)
    db.commit(); print('indexing', flush=True)
    db.execute("CREATE INDEX corpus_word ON corpus (word)"); db.commit()
    r, w, b = db.execute("SELECT count(*), count(DISTINCT word), sum(length(text)) FROM corpus").fetchone(); db.close()
    print(f'wikt: {n} entries, {r} rows, {w} words, {b} chars of text, {os.path.getsize(out) // 1024 // 1024} MB, {time.time() - t:.0f} s', flush=True)

if __name__ == '__main__': main()
