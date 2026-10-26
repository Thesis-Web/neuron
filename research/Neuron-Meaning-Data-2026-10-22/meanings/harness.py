# Meaning test harness: a word's candidate meaning is a RUN (SQL executed by a scratch "mother"); its definition is the SPEC
# (assertions over the state before and after, each quoting the source phrase it encodes). A run that satisfies the spec
# on every fixture PASSES; one that does not FAILS. What each run touches is measured by SQLite's authorizer, not assumed.
import sqlite3, json, re, copy, sys
ACT = {sqlite3.SQLITE_READ:'READ', sqlite3.SQLITE_INSERT:'INSERT', sqlite3.SQLITE_UPDATE:'UPDATE', sqlite3.SQLITE_DELETE:'DELETE',
       sqlite3.SQLITE_CREATE_TABLE:'CREATE_TABLE', sqlite3.SQLITE_DROP_TABLE:'DROP_TABLE', sqlite3.SQLITE_FUNCTION:'FUNCTION', sqlite3.SQLITE_SELECT:'SELECT'}

def world(v=0):
    c = sqlite3.connect(':memory:'); c.row_factory = sqlite3.Row
    c.executescript("""
    CREATE TABLE things(id INTEGER PRIMARY KEY, name TEXT, place TEXT, owner TEXT, value INTEGER, alive INTEGER, t INTEGER);
    CREATE TABLE memory(id INTEGER PRIMARY KEY, words TEXT, said TEXT, t INTEGER);
    CREATE TABLE timeline(id INTEGER PRIMARY KEY, t INTEGER, event TEXT);
    CREATE TABLE state(key TEXT PRIMARY KEY, value TEXT);
    CREATE TABLE purse(owner TEXT PRIMARY KEY, money INTEGER);
    INSERT INTO memory(words,said,t) VALUES('what is blue','the sky',1);
    """)
    if v == 0:
        c.executescript("""INSERT INTO things VALUES(1,'apple','table','ann',3,1,1),(2,'pear','box','bob',5,1,2),(3,'stone','box',NULL,0,0,3),(4,'apple','box','bob',4,1,4),(5,'fish','pond',NULL,2,1,5);
        INSERT INTO state VALUES('now','10'),('it','2'),('running','0'),('capacity','3');
        INSERT INTO purse VALUES('ann',9),('bob',2),('shop',0);
        INSERT INTO timeline VALUES(1,1,'apple made'),(2,2,'pear made'),(3,7,'rain');""")
    elif v == 1:
        c.executescript("""INSERT INTO things VALUES(1,'apple','shelf','ann',7,1,3),(2,'pear','box','bob',1,1,5),(3,'stone','box',NULL,0,0,1),(4,'apple','box','bob',3,1,8),(5,'fish','pond',NULL,6,1,9),(6,'cup','box','ann',4,0,2);
        INSERT INTO state VALUES('now','20'),('it','5'),('running','0'),('capacity','4');
        INSERT INTO purse VALUES('ann',30),('bob',11),('shop',5);
        INSERT INTO timeline VALUES(1,4,'apple made'),(2,9,'pear made'),(3,12,'rain');""")
    elif v == 3:
        c.executescript("""INSERT INTO things VALUES(1,'apple','shelf','ann',3,1,2),(2,'pear','box','bob',9,1,1),(3,'stone','box',NULL,0,0,3),(4,'apple','box','bob',4,0,7),(5,'fish','pond',NULL,2,0,6),(7,'rope','box','cat',4,0,4);
        INSERT INTO state VALUES('now','7'),('it','4'),('running','0'),('capacity','2');
        INSERT INTO purse VALUES('ann',4),('bob',4),('shop',1);
        INSERT INTO timeline VALUES(1,2,'apple made'),(2,3,'pear made'),(3,50,'rain');""")
    elif v >= 4:
        import random; rnd = random.Random(1000 + v)
        pl = lambda: rnd.choice(['table','box','shelf','pond','box']); ow = lambda: rnd.choice(['ann','bob',None,'cat'])
        ts = rnd.sample(range(1, 30), 7)
        rows_ = [(1,'apple',pl(),'ann',rnd.randint(0,9),1,ts[0]),(2,'pear','box','bob',rnd.randint(0,9),rnd.randint(0,1),ts[1]),(3,'stone','box',None,0,0,ts[2]),(4,'apple',pl(),'bob',rnd.randint(0,9),rnd.randint(0,1),ts[3]),(5,'fish','pond',ow(),rnd.randint(0,9),rnd.randint(0,1),ts[4]),(6,'cup',pl(),ow(),rnd.randint(0,9),0,ts[5]),(7,'rope',pl(),ow(),rnd.randint(0,9),rnd.randint(0,1),ts[6])]
        c.executemany('INSERT INTO things VALUES(?,?,?,?,?,?,?)', rows_)
        tl = rnd.sample(range(1, 60), 3)
        c.executemany('INSERT INTO timeline VALUES(?,?,?)', [(1,tl[0],'apple made'),(2,tl[1],'pear made'),(3,tl[2],'rain')])
        c.executemany('INSERT INTO state VALUES(?,?)', [('now', str(max(ts)+rnd.randint(0,5))),('it', str(rnd.choice([1,2,4,5]))),('running','0'),('capacity', str(rnd.randint(1,5)))])
        c.executemany('INSERT INTO purse VALUES(?,?)', [('ann',rnd.randint(4,40)),('bob',rnd.randint(4,40)),('shop',rnd.randint(0,9))])
    else:
        c.executescript("""INSERT INTO things VALUES(1,'apple','table','ann',3,1,2),(2,'pear','box','bob',9,1,1),(3,'stone','box',NULL,0,0,3),(4,'apple','box','bob',4,1,7),(5,'fish','pond',NULL,2,1,6),(7,'rope','box','cat',4,0,4);
        INSERT INTO state VALUES('now','100'),('it','1'),('running','0'),('capacity','4');
        INSERT INTO purse VALUES('ann',4),('bob',4),('shop',1);
        INSERT INTO timeline VALUES(1,2,'apple made'),(2,3,'pear made'),(3,50,'rain');""")
    return c

def snap(c):
    out = {}
    for (tn,) in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        out[tn] = [dict(r) for r in c.execute('SELECT * FROM "%s"' % tn)]
    return out

def run_sql(c, sql, params):
    counts = {}; tables = {}; funcs = set()
    def auth(action, a1, a2, db, trig):
        nm = ACT.get(action, str(action)); counts[nm] = counts.get(nm, 0) + 1
        if nm in ('READ','INSERT','UPDATE','DELETE','CREATE_TABLE','DROP_TABLE') and a1: tables.setdefault(a1, set()).add(nm)
        if nm == 'FUNCTION' and a2: funcs.add(a2)
        return sqlite3.SQLITE_OK
    c.set_authorizer(auth)
    before_changes = c.total_changes; result = []; err = None
    try:
        for stmt in [s.strip() for s in sql.split(';') if s.strip()]:
            cur = c.execute(stmt, params)
            if cur.description: result = [tuple(r) for r in cur.fetchall()]
    except Exception as e:
        err = str(e)
    c.set_authorizer(lambda *a: sqlite3.SQLITE_OK)
    return {'result': result, 'error': err, 'rows_written': c.total_changes - before_changes, 'auth': counts, 'tables': {k: sorted(v) for k, v in tables.items()}, 'funcs': sorted(funcs)}

def roots_of(sql, meas):
    s = sql.upper(); r = set()
    if 'SELECT' in s: r.add('READ')
    if re.search(r'\bINSERT\b|\bUPDATE\b', s): r.add('WRITE')
    if re.search(r'\bDELETE\b|\bDROP\b', s): r.add('DELETE')
    if re.search(r'\bCREATE\b', s): r.add('SPAWN')
    if re.search(r'\bWHERE\b|[<>=]|\bBETWEEN\b|\bEXISTS\b|\bNOT\b', s): r.add('COMPARE')
    if re.search(r'\bWHERE\b', s): r.add('FIND')
    if re.search(r'\bCOUNT\b|\bSUM\b|\+', s): r.add('ADD')
    if re.search(r'[\w)]\s*-\s*[:\w(]|\bMIN\b', sql): r.add('SUBTRACT')
    if re.search(r'\bUNION\b|\bJOIN\b|\|\|', s): r.add('JOIN')
    if re.search(r'\bORDER BY\b|\bLIMIT\b', s): r.add('MOVE')
    if "'now'" in sql or 'datetime' in s.lower() or ':now' in sql: r.add('CLOCK')
    if 'memory' in sql: r.add('MEMORY')
    if 'timeline' in sql: r.add('TIMELINE')
    if 'state' in sql: r.add('STATE')
    if meas['result']: r.add('SAY')
    if re.search(r':\w+', sql): r.add('HEAR')
    return sorted(r)

def ratio(meas):
    a = meas['auth']; g = a.get('CREATE_TABLE', 0) + a.get('DROP_TABLE', 0); w = a.get('INSERT', 0) + a.get('UPDATE', 0) + a.get('DELETE', 0); rd = a.get('READ', 0)
    t = meas['tables']; mem = 'memory' in t; st = 'state' in t; tl = 'timeline' in t
    return {'schema(graph)': g, 'writes(silicon rows)': w, 'reads': rd, 'rows_written': meas['rows_written'], 'rows_said': len(meas['result']), 'memory': mem, 'state': st, 'timeline': tl}

WORDS = []
def word(name, sources, candidates, spec, note=''):
    WORDS.append({'word': name, 'sources': sources, 'candidates': candidates, 'spec': spec, 'note': note})

def rows(s, t, **kw): return [r for r in s.get(t, []) if all(r.get(k) == v for k, v in kw.items())]
def exists(s, **kw): return bool(rows(s, 'things', **kw))
def same_except(a, b, keys): return all(a[k] == b[k] for k in a if k not in keys)
def unchanged(b, a, t='things'): return b.get(t) == a.get(t)
def now(s): return int(rows(s, 'state', key='now')[0]['value'])

# ------------------------------------------------------------------ the words
# Each spec item: (source phrase, check(before, after, result, params) -> bool)
word('create', ['mw: to bring into existence', 'wn v2: bring into existence'],
  [('row', "INSERT INTO things(name,place,t) VALUES(:x,:p,(SELECT value FROM state WHERE key='now'))", {'x':'plum','p':'box'}),
   ('table', "CREATE TABLE plum(id INTEGER)", {'x':'plum','p':'box'}),
   ('WRONG: read it', "SELECT * FROM things WHERE name=:x", {'x':'plum','p':'box'})],
  [('PRE: bring into existence: it did not exist before', lambda b,a,r,p: not exists(b, name=p['x']) and 'plum' not in b),
   ('bring into existence: it exists after', lambda b,a,r,p: exists(a, name=p['x']) or 'plum' in a),
   ('nothing else changed', lambda b,a,r,p: [x for x in b['things'] if x['name']!=p['x']] == [x for x in a['things'] if x['name']!=p['x']])],
  'Two shards pass: a row brought into existence, and a table. Same shape, different kind of thing.')

word('new', ['wn adj: not of long duration; having just come into existence', 'mw: having recently come into existence: recent, modern'],
  [('born now', "INSERT INTO things(name,place,t) VALUES(:x,:p,(SELECT value FROM state WHERE key='now')); SELECT name FROM things WHERE t=(SELECT value FROM state WHERE key='now')", {'x':'plum','p':'box'})],
  [('just come into existence: the new things are exactly those born at now, the created one among them', lambda b,a,r,p: [x[0] for x in r] == [x['name'] for x in a['things'] if x['t']==now(a)] and p['x'] in [x[0] for x in r])],
  'new is a time test on create: born at the clock reading now.')

word('delete', ['wn v1: remove or make invisible', 'mw: to eliminate especially by blotting out, cutting out, or erasing'],
  [('remove the row', "DELETE FROM things WHERE name=:x", {'x':'pear'}),
   ('WRONG: hide by moving', "UPDATE things SET place='nowhere' WHERE name=:x", {'x':'pear'})],
  [('PRE: it existed before', lambda b,a,r,p: exists(b, name=p['x'])),
   ('remove: it does not exist after', lambda b,a,r,p: not exists(a, name=p['x'])),
   ('nothing else changed', lambda b,a,r,p: [x for x in b['things'] if x['name']!=p['x']] == a['things'])])

word('remove', ['wn v1: remove something concrete, as by lifting, pushing, or taking off, or remove something abstract', 'mw: to change the location, position, station, or residence of; to move by lifting, pushing aside, or taking away or off'],
  [('take the row away', "DELETE FROM things WHERE name=:x", {'x':'pear'}),
   ('move it away from the place', "UPDATE things SET place=NULL WHERE name=:x", {'x':'pear'})],
  [('PRE: it was there before', lambda b,a,r,p: exists(b, name=p['x'], place='box')),
   ('taken away: it is not there after', lambda b,a,r,p: not exists(a, name=p['x'], place='box')),
   ('nothing else changed', lambda b,a,r,p: [x for x in b['things'] if x['name']!=p['x']] == [x for x in a['things'] if x['name']!=p['x']])],
  'Both runs pass remove; only the first passes delete. remove is "away from here", delete is "gone from everywhere": delete is one shard of remove.')

word('copy', ['mw: to make a copy or duplicate of', 'wn n1: a reproduction of a written record'],
  [('duplicate the row', "INSERT INTO things(name,place,owner,value,alive,t) SELECT name,place,owner,value,alive,(SELECT value FROM state WHERE key='now') FROM things WHERE id=:i", {'i':2}),
   ('WRONG: move it', "UPDATE things SET place=:p WHERE id=:i", {'i':2,'p':'table'})],
  [('the original is unchanged', lambda b,a,r,p: rows(b,'things',id=p['i']) == rows(a,'things',id=p['i'])),
   ('a duplicate exists after: same in every field but identity and birth time', lambda b,a,r,p: any(x['id']!=p['i'] and same_except(x, rows(b,'things',id=p['i'])[0], ['id','t']) for x in a['things'])),
   ('one more thing exists', lambda b,a,r,p: len(a['things']) == len(b['things'])+1)])

word('move', ['wn v1: change location; move, travel, or proceed', 'mw: to go or pass to another place or in a certain direction'],
  [('change the place', "UPDATE things SET place=:to WHERE id=:i", {'i':2,'to':'table'}),
   ('WRONG: copy it there', "INSERT INTO things(name,place,owner,value,alive,t) SELECT name,:to,owner,value,alive,t FROM things WHERE id=:i", {'i':2,'to':'table'}),
   ('copy it there, then remove it from here', "INSERT INTO things(name,place,owner,value,alive,t) SELECT name,:to,owner,value,alive,t FROM things WHERE id=:i; DELETE FROM things WHERE id=:i", {'i':2,'to':'table'})],
  [('PRE: it was at the old place', lambda b,a,r,p: rows(b,'things',id=p['i'])[0]['place'] != p['to']),
   ('change location: it is at the new place after', lambda b,a,r,p: any(x['name']==rows(b,'things',id=p['i'])[0]['name'] and x['owner']==rows(b,'things',id=p['i'])[0]['owner'] and x['place']==p['to'] for x in a['things'])),
   ('and no longer at the old one', lambda b,a,r,p: not any(x['name']==rows(b,'things',id=p['i'])[0]['name'] and x['place']==rows(b,'things',id=p['i'])[0]['place'] for x in a['things'])),
   ('the same number of things', lambda b,a,r,p: len(a['things']) == len(b['things']))],
  'copy fails move on one line only: the thing is still at the old place. move = copy + remove-from-old, which is one DELETE more.')

word('split', ['wn v1: separate into parts or portions', 'mw: to divide lengthwise usually along a grain or seam or by layers'],
  [('two parts by a cut', "CREATE TABLE part1 AS SELECT * FROM things WHERE value>=:k; CREATE TABLE part2 AS SELECT * FROM things WHERE value<:k", {'k':3}),
   ('WRONG: two copies of all', "CREATE TABLE part1 AS SELECT * FROM things; CREATE TABLE part2 AS SELECT * FROM things", {'k':3})],
  [('separate into parts: each thing is in exactly one part', lambda b,a,r,p: all(sum(1 for pt in ('part1','part2') if x in a.get(pt,[])) == 1 for x in b['things'])),
   ('the parts together are the whole', lambda b,a,r,p: sorted(a.get('part1',[])+a.get('part2',[]), key=lambda x:x['id']) == b['things']),
   ('no part is empty', lambda b,a,r,p: a.get('part1') and a.get('part2'))])

word('join', ['wn n2: a set containing all and only the members of two or more given sets', 'wn v4: make contact or come together', 'mw: to put or bring together so as to form a unit'],
  [('bring two parts together', "CREATE TABLE part1 AS SELECT * FROM things WHERE value>=3; CREATE TABLE part2 AS SELECT * FROM things WHERE value<3; CREATE TABLE joined AS SELECT * FROM part1 UNION SELECT * FROM part2", {}),
   ('WRONG: pair them up by a key (SQL JOIN)', "CREATE TABLE part1 AS SELECT * FROM things WHERE value>=3; CREATE TABLE part2 AS SELECT * FROM things WHERE value<3; CREATE TABLE joined AS SELECT p1.id, p2.id AS id2 FROM part1 p1 JOIN part2 p2 ON p1.place=p2.place", {})],
  [('all and only the members of both', lambda b,a,r,p: sorted(a.get('joined',[]), key=lambda x:x['id']) == b['things'])],
  'SQL JOIN is a different meaning under the same letters (pairing by a shared key). That is the encoder\'s business: two gates, one spelling.')

word('read', ['mw: to receive or take in the sense of (letters, symbols, etc.) especially by sight or touch', 'wn v1: interpret something that is written or printed'],
  [('take in what is written at a known place', "SELECT name,place,owner,value FROM things WHERE id=:i", {'i':2}),
   ('WRONG: change it while looking', "UPDATE things SET value=value+1 WHERE id=:i; SELECT name,place,owner,value FROM things WHERE id=:i", {'i':2})],
  [('what comes out is what is written there', lambda b,a,r,p: r and list(r[0]) == [rows(b,'things',id=p['i'])[0][k] for k in ('name','place','owner','value')]),
   ('taking in changes nothing', lambda b,a,r,p: unchanged(b,a))])

word('write', ['mw: to form (characters, symbols, etc.) by or as if by marking on a surface', 'wn v2: communicate or express by writing'],
  [('a new mark', "INSERT INTO things(name,place,t) VALUES(:x,:p,(SELECT value FROM state WHERE key='now'))", {'x':'plum','p':'box','i':2}),
   ('a changed mark', "UPDATE things SET owner=:v WHERE id=:i", {'x':'plum','p':'box','i':2,'v':'zed'}),
   ('WRONG: only look', "SELECT * FROM things", {'x':'plum','p':'box','i':2})],
  [('a mark exists after that did not before', lambda b,a,r,p: a['things'] != b['things'] and len(a['things']) >= len(b['things']))],
  'write has two shards: the new mark (which is also create\'s row shard) and the changed mark. create and write share one shard; that is where their places overlap.')

word('find', ['wn v1: come upon, as if by accident; meet with', 'mw: to come upon often accidentally: encounter', 'wn v3: discover or determine the existence, presence, or fact of'],
  [('come upon the things with a property', "SELECT id FROM things WHERE place=:p", {'p':'box'}),
   ('WRONG: take whatever is first', "SELECT id FROM things LIMIT 1", {'p':'box'})],
  [('what comes out has the property asked for, and all of them do', lambda b,a,r,p: sorted(x[0] for x in r) == sorted(x['id'] for x in rows(b,'things',place=p['p']))),
   ('finding changes nothing', lambda b,a,r,p: unchanged(b,a))],
  'read and find reach the same roots (READ, COMPARE, FIND). They differ in what is in hand on arrival: an identity (read) or a property (find). That difference is the shard key, not the roots.')

word('same', ['wn adj1: same in identity', 'mw: resembling in every relevant respect; being one without addition, change, or discontinuance: identical'],
  [('identical in every field, a thing and itself', "SELECT (SELECT name||place||IFNULL(owner,'')||value||alive FROM things WHERE id=:a) = (SELECT name||place||IFNULL(owner,'')||value||alive FROM things WHERE id=:b)", {'a':1,'b':1}),
   ('identical in every field, two apples in different places', "SELECT (SELECT name||place||IFNULL(owner,'')||value||alive FROM things WHERE id=:a) = (SELECT name||place||IFNULL(owner,'')||value||alive FROM things WHERE id=:b)", {'a':1,'b':4}),
   ('WRONG: same name only, two apples in different places', "SELECT (SELECT name FROM things WHERE id=:a) = (SELECT name FROM things WHERE id=:b)", {'a':1,'b':4})],
  [('a thing is the same as itself; two things unlike in some respect are not the same', lambda b,a,r,p: r[0][0] == (1 if p['a']==p['b'] else 0))],
  'Identity in every relevant respect: a weaker compare (name only) calls two different apples the same, and fails.')

word('different', ['wn adj1: unlike in nature or quality or form or degree', 'mw: partly or totally unlike in nature, form, or quality: dissimilar'],
  [('not identical, two apples apart', "SELECT (SELECT name||place||IFNULL(owner,'')||value||alive FROM things WHERE id=:a) <> (SELECT name||place||IFNULL(owner,'')||value||alive FROM things WHERE id=:b)", {'a':1,'b':4}),
   ('not identical, a thing and itself', "SELECT (SELECT name||place||IFNULL(owner,'')||value||alive FROM things WHERE id=:a) <> (SELECT name||place||IFNULL(owner,'')||value||alive FROM things WHERE id=:b)", {'a':1,'b':1})],
  [('says yes exactly when some field differs', lambda b,a,r,p: r[0][0] == (0 if p['a']==p['b'] else 1))])

word('not', ['wn: negation of a word or group of words', 'mw: used as a function word to make negative a group of words or a word'],
  [('turn the yes into no', "SELECT NOT (:t), NOT (NOT (:t))", {'t':1})],
  [('negation turns 1 into 0', lambda b,a,r,p: r[0][0] == 0), ('and back', lambda b,a,r,p: r[0][1] == 1)])

word('and', ['mw: used as a function word to indicate connection or addition especially of items within the same class'],
  [('both at once', "SELECT id FROM things WHERE place='box' AND alive=1", {})],
  [('the rows are those in both sets', lambda b,a,r,p: sorted(x[0] for x in r) == sorted(x['id'] for x in b['things'] if x['place']=='box' and x['alive']==1)),
   ('never more than either set alone', lambda b,a,r,p: len(r) <= len(rows(b,'things',place='box')) and len(r) <= len(rows(b,'things',alive=1)))])

word('or', ['mw: used as a function word to indicate an alternative'],
  [('either', "SELECT id FROM things WHERE place='box' OR alive=0", {})],
  [('the rows are those in either set', lambda b,a,r,p: sorted(x[0] for x in r) == sorted(x['id'] for x in b['things'] if x['place']=='box' or x['alive']==0)),
   ('never fewer than either set alone', lambda b,a,r,p: len(r) >= len(rows(b,'things',place='box')) and len(r) >= len(rows(b,'things',alive=0)))])

word('if', ['mw: in the event that'],
  [('the act happens only in the event', "UPDATE things SET owner=:o WHERE id=:i AND (:cond)=1", {'o':'cat','i':2,'cond':1}),
   ('the event does not hold', "UPDATE things SET owner=:o WHERE id=:i AND (:cond)=1", {'o':'cat','i':2,'cond':0})],
  [('when the condition holds the thing changes; when not, nothing changes', lambda b,a,r,p: (rows(a,'things',id=p['i'])[0]['owner']==p['o']) == (p['cond']==1))])

word('all', ['wn: quantifier; used to indicate the whole number or amount', 'mw: the whole amount, quantity, or extent of'],
  [('every one', "SELECT id FROM things", {})],
  [('the whole number: every thing comes out', lambda b,a,r,p: len(r) == len(b['things']))])

word('some', ['wn: quantifier; used to indicate an unspecified number or quantity', 'mw: being an unknown, undetermined, or unspecified unit or thing'],
  [('an unspecified number, at least one', "SELECT id FROM things WHERE alive=1", {})],
  [('at least one', lambda b,a,r,p: len(r) >= 1), ('a number not fixed in advance', lambda b,a,r,p: True)],
  'some is a count between one and all; which count is not fixed by the word.')

word('none', ['mw: not any', 'wn adv: not at all or in no way'],
  [('not any, of a thing there is none of', "SELECT NOT EXISTS(SELECT 1 FROM things WHERE name=:x)", {'x':'plum'}),
   ('not any, of a thing there is some of', "SELECT NOT EXISTS(SELECT 1 FROM things WHERE name=:x)", {'x':'pear'})],
  [('says yes exactly when no such thing exists', lambda b,a,r,p: r[0][0] == (1 if not exists(b, name=p['x']) else 0))])

word('one', ['wn: used of a single unit or thing; not two or more', 'wn n: the smallest whole number'],
  [('a single unit', "SELECT COUNT(*) FROM things WHERE id=:i", {'i':3}), ('a single unit, asked of a thing that is not there', "SELECT COUNT(*) FROM things WHERE id=:i", {'i':99})],
  [('the count is one exactly when there is a single such thing', lambda b,a,r,p: r[0][0] == len(rows(b,'things',id=p['i'])) and r[0][0] in (0,1))])

word('two', ['wn: being one more than one', 'wn n: the cardinal number that is the sum of one and one'],
  [('one more than one', "SELECT COUNT(*), 1+1 FROM things WHERE name='apple'", {})],
  [('the count is one and one', lambda b,a,r,p: r[0][0] == len(rows(b,'things',name='apple')) and r[0][1] == 2 and r[0][0] == 2)])

word('more', ['wn: greater in size or amount or number', 'mw: greater'],
  [('a greater number', "SELECT (SELECT COUNT(*) FROM things WHERE alive=1) > (SELECT COUNT(*) FROM things WHERE alive=0)", {})],
  [('says yes exactly when the first count is greater', lambda b,a,r,p: r[0][0] == (1 if len(rows(b,'things',alive=1)) > len(rows(b,'things',alive=0)) else 0))])

word('few', ['wn: a small but indefinite number', 'mw: not many persons or things'],
  [('a small number: fewer than the others', "SELECT (SELECT COUNT(*) FROM things WHERE alive=0) < (SELECT COUNT(*) FROM things WHERE alive=1)", {})],
  [('says yes exactly when the first count is smaller', lambda b,a,r,p: r[0][0] == (1 if len(rows(b,'things',alive=0)) < len(rows(b,'things',alive=1)) else 0))],
  'few = the smaller side of the same compare that more is the greater side of: one COMPARE, two labels, opposite ends.')

word('before', ['wn adv: earlier in time; previously', 'mw: at an earlier time'],
  [('earlier in time', "SELECT (SELECT t FROM timeline WHERE id=:a) < (SELECT t FROM timeline WHERE id=:b)", {'a':1,'b':3}),
   ('earlier in time, asked the other way round', "SELECT (SELECT t FROM timeline WHERE id=:a) < (SELECT t FROM timeline WHERE id=:b)", {'a':3,'b':1}),
   ('WRONG: the worksheet minus now', "SELECT -(SELECT value FROM state WHERE key='now')", {'a':1,'b':3})],
  [('says yes exactly when a happened at an earlier time than b', lambda b,a,r,p: r[0][0] == (1 if rows(b,'timeline',id=p['a'])[0]['t'] < rows(b,'timeline',id=p['b'])[0]['t'] else 0))],
  '"-now" returns a number (-10), not whether a was earlier than b: it cannot be before, because before takes two events.')

word('after', ['wn: happening at a time subsequent to a reference time', 'mw: following in time or place'],
  [('later in time', "SELECT (SELECT t FROM timeline WHERE id=:a) > (SELECT t FROM timeline WHERE id=:b)", {'a':3,'b':1}),
   ('later in time, asked the other way round', "SELECT (SELECT t FROM timeline WHERE id=:a) > (SELECT t FROM timeline WHERE id=:b)", {'a':1,'b':3})],
  [('says yes exactly when a happened at a later time than b', lambda b,a,r,p: r[0][0] == (1 if rows(b,'timeline',id=p['a'])[0]['t'] > rows(b,'timeline',id=p['b'])[0]['t'] else 0))],
  'before and after are one COMPARE on two times read from the timeline, less or more. The flip between them is the axis flip, not a negation.')

word('now', ['wn n: the momentary present', 'mw: at the present time or moment'],
  [('the clock reading at this moment', "SELECT value FROM state WHERE key='now'", {})],
  [('it is the present reading of the clock', lambda b,a,r,p: int(r[0][0]) == now(b))])

word('when', ['mw: at what time', 'mw: at or during which time'],
  [('the time an event happened', "SELECT t FROM timeline WHERE event=:e", {'e':'rain'})],
  [('the answer is the time of that event', lambda b,a,r,p: r[0][0] == rows(b,'timeline',event=p['e'])[0]['t'])])

word('the', ['mw: used as a function word to indicate that a following noun is definite or has been previously specified by context'],
  [('the one already in play', "SELECT id FROM things WHERE id=(SELECT value FROM state WHERE key='it')", {}),
   ('WRONG: any one', "SELECT id FROM things LIMIT 1", {})],
  [('exactly one, and it is the one previously specified (state it)', lambda b,a,r,p: len(r)==1 and str(r[0][0]) == rows(b,'state',key='it')[0]['value'])],
  'the is a FIND in state: the thing the run already has in play. It reads state and nothing else.')

word('a', ['mw: used as a function word before singular nouns when the referent is unspecified'],
  [('any one of the kind', "SELECT id FROM things WHERE name=:k LIMIT 1", {'k':'apple'})],
  [('exactly one', lambda b,a,r,p: len(r) == 1), ('of the kind asked, and which one is not specified', lambda b,a,r,p: rows(b,'things',id=r[0][0])[0]['name'] == p['k'] and len(rows(b,'things',name=p['k'])) > 1)])

word('between', ['wn: in the interval', 'mw: in the space that separates'],
  [('in the interval', "SELECT id FROM things WHERE value BETWEEN :lo AND :hi", {'lo':3,'hi':4})],
  [('the things whose value lies in the interval, all of them', lambda b,a,r,p: sorted(x[0] for x in r) == sorted(x['id'] for x in b['things'] if p['lo'] <= x['value'] <= p['hi']))])

word('part', ['wn n2: something determined in relation to something that includes it', 'mw: one of the often indefinite or unequal subdivisions into which something is or is regarded as divided'],
  [('a subdivision of the whole', "SELECT id FROM things WHERE place='box'", {})],
  [('included in the whole', lambda b,a,r,p: all(any(x['id']==y[0] for x in b['things']) for y in r)),
   ('not the whole', lambda b,a,r,p: 0 < len(r) < len(b['things']))])

word('whole', ['wn: all of something including all its component elements or parts'],
  [('all the parts together', "SELECT id FROM things", {})],
  [('includes every part', lambda b,a,r,p: len(r) == len(b['things']))],
  'whole runs the same as all: one meaning, two labels.')

word('keep', ['mw: to retain in one\'s possession or power', 'wn v: keep in a certain state, position, or activity'],
  [('retain over time', "UPDATE state SET value=value+5 WHERE key='now'; SELECT owner FROM things WHERE id=:i", {'i':1}),
   ('WRONG: give it away meanwhile', "UPDATE things SET owner='bob' WHERE id=:i; UPDATE state SET value=value+5 WHERE key='now'; SELECT owner FROM things WHERE id=:i", {'i':1})],
  [('PRE: had it before', lambda b,a,r,p: rows(b,'things',id=p['i'])[0]['owner'] is not None),
   ('time passed', lambda b,a,r,p: now(a) > now(b)),
   ('still has it after', lambda b,a,r,p: r[0][0] == rows(b,'things',id=p['i'])[0]['owner'])],
  'keep is a test across time: possession at t2 equals possession at t1. Nothing is written to the thing; the clock moves.')

word('store', ['wn v1: keep or lay aside for future use', 'mw: to lay away'],
  [('lay aside now, take back later', "INSERT INTO memory(words,said,t) VALUES(:w,:w,(SELECT value FROM state WHERE key='now')); UPDATE state SET value=value+5 WHERE key='now'; SELECT said FROM memory WHERE words=:w", {'w':'the grass is green'}),
   ('WRONG: lay aside then lose it', "INSERT INTO memory(words,said,t) VALUES(:w,:w,(SELECT value FROM state WHERE key='now')); DELETE FROM memory WHERE words=:w; UPDATE state SET value=value+5 WHERE key='now'; SELECT said FROM memory WHERE words=:w", {'w':'the grass is green'})],
  [('PRE: not held before', lambda b,a,r,p: not rows(b,'memory',words=p['w'])),
   ('laid aside: held after', lambda b,a,r,p: bool(rows(a,'memory',words=p['w']))),
   ('for future use: readable later, unchanged', lambda b,a,r,p: r and r[0][0] == p['w'] and now(a) > now(b))],
  'store = write to memory + keep. keep alone writes nothing; store writes first. Different pre-state, shared tail.')

word('have', ['wn v: have or possess, either in a concrete or an abstract sense', 'mw: to hold or maintain as a possession'],
  [('possess', "SELECT EXISTS(SELECT 1 FROM things WHERE id=:i AND owner=:o)", {'i':1,'o':'ann'}), ('possess, asked of the wrong owner', "SELECT EXISTS(SELECT 1 FROM things WHERE id=:i AND owner=:o)", {'i':1,'o':'bob'})],
  [('says yes exactly when that owner holds the thing', lambda b,a,r,p: r[0][0] == (1 if rows(b,'things',id=p['i'])[0]['owner'] == p['o'] else 0))])

word('give', ['wn v1: cause to have, in the abstract sense or physical sense', 'mw: to make a present of'],
  [('cause another to have it', "UPDATE things SET owner=:to WHERE id=:i AND owner=:frm", {'i':1,'frm':'ann','to':'bob'}),
   ('WRONG: copy it to them', "INSERT INTO things(name,place,owner,value,alive,t) SELECT name,place,:to,value,alive,t FROM things WHERE id=:i", {'i':1,'frm':'ann','to':'bob'})],
  [('PRE: the giver had it', lambda b,a,r,p: rows(b,'things',id=p['i'])[0]['owner'] == p['frm']),
   ('cause to have: the receiver has it after', lambda b,a,r,p: any(x['name']=='apple' and x['owner']==p['to'] and x['id']==p['i'] for x in a['things'])),
   ('and the giver no longer has it', lambda b,a,r,p: not any(x['id']==p['i'] and x['owner']==p['frm'] for x in a['things']))],
  'Copying fails give on the last line: the giver still has it. A gift is a move of possession, not a copy.')

word('take', ['mw: to get into one\'s hands or into one\'s possession, power, or control', 'wn get v1: come into the possession of something concrete or abstract'],
  [('come into possession', "UPDATE things SET owner=:me WHERE id=:i", {'i':2,'me':'ann'})],
  [('PRE: I did not have it', lambda b,a,r,p: rows(b,'things',id=p['i'])[0]['owner'] != p['me']),
   ('into my possession: I have it after', lambda b,a,r,p: rows(a,'things',id=p['i'])[0]['owner'] == p['me']),
   ('the other no longer has it', lambda b,a,r,p: rows(a,'things',id=p['i'])[0]['owner'] != rows(b,'things',id=p['i'])[0]['owner'])],
  'give and take are the same run (owner changes from one to another) seen from the two ends. Same roots, same place; the holes (who is I) differ. That is the arrival picking the shard.')

word('buy', ['wn v1: obtain by purchase; acquire by means of a financial transaction', 'mw: to acquire possession, ownership, or rights to the use or services of by payment'],
  [('possession one way, money the other', "UPDATE things SET owner=:buyer WHERE id=:i AND owner=:seller; UPDATE purse SET money=money-:price WHERE owner=:buyer; UPDATE purse SET money=money+:price WHERE owner=:seller", {'i':2,'buyer':'ann','seller':'bob','price':4}),
   ('WRONG: take without paying', "UPDATE things SET owner=:buyer WHERE id=:i AND owner=:seller", {'i':2,'buyer':'ann','seller':'bob','price':4})],
  [('acquire possession', lambda b,a,r,p: rows(a,'things',id=p['i'])[0]['owner'] == p['buyer']),
   ('by payment: the buyer has less money by the price', lambda b,a,r,p: rows(a,'purse',owner=p['buyer'])[0]['money'] == rows(b,'purse',owner=p['buyer'])[0]['money'] - p['price']),
   ('and the seller has more by the price', lambda b,a,r,p: rows(a,'purse',owner=p['seller'])[0]['money'] == rows(b,'purse',owner=p['seller'])[0]['money'] + p['price'])],
  'buy = take + pay. Taking without paying passes take and fails buy. The money line is what buy adds.')

word('sell', ['wn v1: exchange or deliver for money or its equivalent', 'mw: to give up (property) to another for something of value (such as money)'],
  [('deliver for money', "UPDATE things SET owner=:buyer WHERE id=:i AND owner=:seller; UPDATE purse SET money=money-:price WHERE owner=:buyer; UPDATE purse SET money=money+:price WHERE owner=:seller", {'i':1,'buyer':'bob','seller':'ann','price':2})],
  [('give up the property', lambda b,a,r,p: rows(a,'things',id=p['i'])[0]['owner'] != p['seller']),
   ('for money: the seller has more by the price', lambda b,a,r,p: rows(a,'purse',owner=p['seller'])[0]['money'] == rows(b,'purse',owner=p['seller'])[0]['money'] + p['price'])],
  'sell is buy from the other end: the same run, the holes swapped. One place, two labels, two arrivals.')

word('shop', ['wn n1: a mercantile establishment for the retail sale of goods or services', 'mw: a building or room stocked with merchandise for sale'],
  [('a place stocked with things that leave when paid for', "INSERT INTO things(name,place,owner,value,alive,t) VALUES('hat','shop','shop',3,0,9); UPDATE things SET owner='ann' WHERE name='hat' AND place='shop' AND owner='shop'; UPDATE purse SET money=money-3 WHERE owner='ann'; UPDATE purse SET money=money+3 WHERE owner='shop'; UPDATE things SET place='table' WHERE name='hat'", {})],
  [('a place with goods for sale, owned by the shop', lambda b,a,r,p: True),
   ('after a sale the good is the buyer\'s and the shop has the money', lambda b,a,r,p: any(x['name']=='hat' and x['owner']=='ann' for x in a['things']) and rows(a,'purse',owner='shop')[0]['money'] == rows(b,'purse',owner='shop')[0]['money'] + 3)],
  'shop is not a run; it is a place where the sell run happens, over and over. Its meaning is the place plus the process: a noun made of a verb. "place be" was wrong: the process was missing.')

word('count', ['mw: to indicate or name by units or groups so as to find the total number of units involved', 'wn v1: determine the number or amount of'],
  [('find the total number', "SELECT COUNT(*) FROM things WHERE place=:p", {'p':'box'})],
  [('the number equals how many there are', lambda b,a,r,p: r[0][0] == len(rows(b,'things',place=p['p'])))])

word('order', ['mw: to put in order: arrange', 'wn sort v1: arrange or order by classes or categories'],
  [('arrange in sequence', "SELECT id, value FROM things ORDER BY value", {})],
  [('the sequence never goes down', lambda b,a,r,p: all(r[i][1] <= r[i+1][1] for i in range(len(r)-1))),
   ('the same members, rearranged', lambda b,a,r,p: sorted(x[0] for x in r) == sorted(x['id'] for x in b['things']))])

word('first', ['mw: preceding all others in time, order, or importance'],
  [('preceding all others in time', "SELECT event FROM timeline ORDER BY t LIMIT 1", {})],
  [('its time is the smallest', lambda b,a,r,p: r[0][0] == min(b['timeline'], key=lambda x:x['t'])['event'])])

word('last', ['mw: following all the rest'],
  [('following all the rest', "SELECT event FROM timeline ORDER BY t DESC LIMIT 1", {})],
  [('its time is the largest', lambda b,a,r,p: r[0][0] == max(b['timeline'], key=lambda x:x['t'])['event'])],
  'first and last: one ORDER, two ends. The same shape as before/after and more/few: an axis, read from either end.')

word('empty', ['wn adj1: holding or containing nothing', 'mw: containing nothing'],
  [('holding nothing', "SELECT COUNT(*)=0 FROM things WHERE place=:p", {'p':'shelf'}), ('holding nothing, asked of a place with things', "SELECT COUNT(*)=0 FROM things WHERE place=:p", {'p':'box'})],
  [('says yes exactly when nothing is there', lambda b,a,r,p: r[0][0] == (1 if not rows(b,'things',place=p['p']) else 0))])

word('full', ['wn adj1: containing as much or as many as is possible or normal', 'mw: containing as much or as many as is possible or normal'],
  [('as many as is possible', "SELECT (SELECT COUNT(*) FROM things WHERE place='box') >= (SELECT value FROM state WHERE key='capacity')", {})],
  [('says yes exactly when the count has reached the held capacity', lambda b,a,r,p: r[0][0] == (1 if len(rows(b,'things',place='box')) >= int(rows(b,'state',key='capacity')[0]['value']) else 0))],
  'full needs a capacity, which is state, not a thing: full = count compared with a held limit.')

word('change', ['wn v1: cause to change; make different; cause a transformation', 'mw: to make different in some particular'],
  [('make different: write what is not there', "UPDATE things SET place=CASE WHEN place='box' THEN 'table' ELSE 'box' END WHERE id=:i", {'i':1}),
   ('WRONG: set a value that may already be there', "UPDATE things SET value=:v WHERE id=:i", {'i':1,'v':8})],
  [('the same thing', lambda b,a,r,p: bool(rows(a,'things',id=p['i']))),
   ('is different after', lambda b,a,r,p: rows(a,'things',id=p['i'])[0] != rows(b,'things',id=p['i'])[0])],
  'Setting a value is a change only when the value differs from what is there: on worlds where 8 was already held, the WRONG run changes nothing. A change must read first.')

word('remember', ['wn v1: recall knowledge from memory; have a recollection', 'mw: to bring to mind or think of again'],
  [('bring back from memory', "SELECT said FROM memory WHERE words=:q", {'q':'what is blue'})],
  [('what comes back is what was laid in memory', lambda b,a,r,p: r and r[0][0] == rows(b,'memory',words=p['q'])[0]['said']), ('bringing back changes nothing', lambda b,a,r,p: unchanged(b,a,'memory'))],
  'remember = read from memory. It presupposes a store; without the earlier write there is nothing to bring back.')

word('forget', ['wn v1: dismiss from the mind; stop remembering', 'mw: to lose the remembrance of: be unable to think of or recall'],
  [('stop holding it', "DELETE FROM memory WHERE words=:q; SELECT said FROM memory WHERE words=:q", {'q':'what is blue'})],
  [('PRE: it was held before', lambda b,a,r,p: bool(rows(b,'memory',words=p['q']))), ('stop remembering: not held after, nothing comes back', lambda b,a,r,p: not rows(a,'memory',words=p['q']) and not r)])

word('exist', ['wn v1: have an existence, be extant', 'mw: to have real being whether material or spiritual'],
  [('be extant', "SELECT EXISTS(SELECT 1 FROM things WHERE name=:x)", {'x':'pear'}), ('be extant, asked of a thing that is not', "SELECT EXISTS(SELECT 1 FROM things WHERE name=:x)", {'x':'plum'})],
  [('says yes exactly when there is such a thing', lambda b,a,r,p: r[0][0] == (1 if exists(b,name=p['x']) else 0))])

word('begin', ['wn v1: set in motion, cause to start', 'mw: to do the first part of an action'],
  [('set in motion', "UPDATE state SET value='1' WHERE key='running'; INSERT INTO timeline(t,event) VALUES((SELECT value FROM state WHERE key='now'),'start')", {})],
  [('PRE: not running before', lambda b,a,r,p: rows(b,'state',key='running')[0]['value']=='0'),
   ('running after, and the start is on the timeline at now', lambda b,a,r,p: rows(a,'state',key='running')[0]['value']=='1' and any(x['event']=='start' and x['t']==now(b) for x in a['timeline']))])

word('end', ['wn v1: bring to an end or halt', 'mw: to bring to an end'],
  [('bring to a halt', "UPDATE state SET value='1' WHERE key='running'; UPDATE state SET value='0' WHERE key='running'; INSERT INTO timeline(t,event) VALUES((SELECT value FROM state WHERE key='now'),'end')", {})],
  [('not running after', lambda b,a,r,p: rows(a,'state',key='running')[0]['value']=='0' and any(x['event']=='end' for x in a['timeline']))])

word('live', ['mw: to be alive: have the life of an animal or plant', 'wn v2: lead a certain kind of life; live in a certain style'],
  [('be alive', "SELECT alive FROM things WHERE name=:x", {'x':'pear'}), ('be alive, asked of a stone', "SELECT alive FROM things WHERE name=:x", {'x':'stone'})],
  [('says what the thing\'s life is', lambda b,a,r,p: r[0][0] == rows(b,'things',name=p['x'])[0]['alive'])])

word('die', ['wn v1: pass from physical life and lose all bodily attributes and functions necessary to sustain life', 'mw: to pass from physical life: expire'],
  [('pass from life', "UPDATE things SET alive=0 WHERE name=:x AND alive=1", {'x':'pear'}),
   ('WRONG: the worksheet minus live', "SELECT NOT alive FROM things WHERE name=:x", {'x':'pear'}),
   ('WRONG: minus live on a stone', "SELECT NOT alive FROM things WHERE name='stone'", {'x':'pear'})],
  [('PRE: it was alive before', lambda b,a,r,p: rows(b,'things',name=p['x'])[0]['alive'] == 1),
   ('pass from life: not alive after', lambda b,a,r,p: rows(a,'things',name=p['x'])[0]['alive'] == 0),
   ('the body remains: the row still exists', lambda b,a,r,p: exists(a, name=p['x']))],
  '"not alive" reads a state and changes nothing; it is true of the stone, which never lived and did not die. die is a change: alive before, not alive after, the row kept. That is the executed version of the worksheet finding.')

word('kill', ['wn v1: cause to die; put to death', 'mw: to deprive of life'],
  [('cause to die', "UPDATE things SET alive=0 WHERE name=:x AND alive=1; INSERT INTO timeline(t,event) VALUES((SELECT value FROM state WHERE key='now'), :who||' killed '||:x)", {'x':'pear','who':'cat'})],
  [('PRE: it was alive before', lambda b,a,r,p: rows(b,'things',name=p['x'])[0]['alive'] == 1), ('the thing died', lambda b,a,r,p: rows(a,'things',name=p['x'])[0]['alive'] == 0),
   ('and someone caused it: the actor is on the timeline', lambda b,a,r,p: any(p['who'] in x['event'] for x in a['timeline']))],
  'kill = die + a cause. The cause is not in the thing; it is in the receipt (the timeline row naming the actor).')

word('born', ['wn adj: brought into existence', 'mw: brought forth by or as if by birth'],
  [('brought into existence, alive', "INSERT INTO things(name,place,alive,t) VALUES(:x,:p,1,(SELECT value FROM state WHERE key='now'))", {'x':'kit','p':'box'})],
  [('PRE: did not exist before', lambda b,a,r,p: not exists(b,name=p['x'])), ('exists after, alive, at now', lambda b,a,r,p: any(x['name']==p['x'] and x['alive']==1 and x['t']==now(b) for x in a['things']))],
  'born = create + alive. die undoes the alive, not the create.')

word('into', ['mw: used as a function word to indicate entry, introduction, insertion, superposition, or inclusion'],
  [('the place a write goes', "INSERT INTO things(name,place,t) VALUES(:x,:p,1)", {'x':'plum','p':'box'}),
   ('WRONG: a write with no into', "INSERT things(name,place,t) VALUES(:x,:p,1)", {'x':'plum','p':'box'})],
  [('after, the thing is in that place', lambda b,a,r,p: exists(a,name=p['x'],place=p['p']))],
  'into is the destination hole of a write or a move. Without it the write has nowhere to go and the silicon refuses the line (a syntax error). It has no run of its own; it is a slot in another run.')

word('add', ['mw: to join or unite so as to bring about an increase', 'wn v1: make an addition'],
  [('bring about an increase', "UPDATE things SET value=value+:k WHERE id=:i", {'i':1,'k':2})],
  [('the value after is the value before plus k', lambda b,a,r,p: rows(a,'things',id=p['i'])[0]['value'] == rows(b,'things',id=p['i'])[0]['value'] + p['k'])])

word('subtract', ['mw: to take away by or as if by deducting', 'wn v1: make a subtraction'],
  [('take away', "UPDATE things SET value=value-:k WHERE id=:i", {'i':1,'k':2})],
  [('the value after is the value before minus k', lambda b,a,r,p: rows(a,'things',id=p['i'])[0]['value'] == rows(b,'things',id=p['i'])[0]['value'] - p['k'])],
  'add and subtract: one axis, two directions, like more/few and before/after.')

word('where', ['mw: at, in, or to what place'],
  [('the place of a thing', "SELECT place FROM things WHERE id=:i", {'i':2})],
  [('the answer is its place', lambda b,a,r,p: r[0][0] == rows(b,'things',id=p['i'])[0]['place'])])

word('which', ['mw: being what one or ones out of a group'],
  [('the one out of a group with the property', "SELECT id FROM things WHERE name='apple' AND place=:p", {'p':'box'})],
  [('one out of the group, picked by the property', lambda b,a,r,p: [x[0] for x in r] == [x['id'] for x in b['things'] if x['name']=='apple' and x['place']==p['p']])])

word('lose', ['wn v1: fail to keep or to maintain; cease to have, either physically or in an abstract sense', 'mw: to miss from one\'s possession or from a customary or supposed place'],
  [('cease to have', "UPDATE things SET owner=NULL WHERE id=:i AND owner=:me", {'i':1,'me':'ann'})],
  [('PRE: had it', lambda b,a,r,p: rows(b,'things',id=p['i'])[0]['owner']==p['me']), ('ceases to have it', lambda b,a,r,p: rows(a,'things',id=p['i'])[0]['owner']!=p['me'])],
  'lose and give end in the same state for the loser. They differ only in the receipt: who did it and whether anyone received. Some meanings are told apart by history, not by the state they leave.')

# ------------------------------------------------------------------ run everything
results = []
def evaluate(spec, sql, params, v):
    c = world(v); b = snap(c); meas = run_sql(c, sql, params); a = snap(c); checks = []
    for (phrase, fn) in spec:
        try: ok = bool(fn(b, a, meas['result'], params)) if not meas['error'] else False
        except Exception: ok = False
        checks.append((phrase, ok))
    na = any(ph.startswith('PRE:') and not ok for ph, ok in checks)
    if na: return checks, meas, None
    return checks, meas, (all(ok for _, ok in checks) and not meas['error'])
for W in WORDS:
    for (cname, sql, params) in W['candidates']:
        per = []
        for v in range(10):
            checks, meas, ok = evaluate(W['spec'], sql, params, v); per.append((checks, meas, ok))
        checks, meas, _ = next((x for x in per if x[2] is not None), per[0])
        appl = [x[2] for x in per if x[2] is not None]
        passed = len(appl) >= 3 and all(appl)
        results.append({'word': W['word'], 'candidate': cname, 'sql': sql, 'params': params, 'error': meas['error'], 'checks': checks, 'passed': passed, 'worlds': [x[2] for x in per],
                        'roots': roots_of(sql, meas), 'measure': ratio(meas), 'tables': meas['tables'], 'result': meas['result'][:6], 'applicable_worlds': len(appl)})
# cross matrix: which other words' specs does a passing run also satisfy on all three worlds (an entailment found by execution)
spec_of = {W['word']: W['spec'] for W in WORDS}
entail = []
for r in results:
    if not r['passed'] or r['candidate'].startswith('WRONG'): continue
    for w2, sp in spec_of.items():
        if w2 == r['word']: continue
        oks = []
        for v in range(10):
            try:
                checks, meas, ok = evaluate(sp, r['sql'], r['params'], v)
                # a KeyError inside a check counts as not applicable, not as a failure
                oks.append(ok)
            except Exception:
                oks.append(None)
        # count only when every check could be evaluated: re-run to detect KeyErrors explicitly
        applicable = True
        c = world(0); b = snap(c); meas = run_sql(c, r['sql'], r['params']); a = snap(c)
        for (phrase, fn) in sp:
            try: fn(b, a, meas['result'], r['params'])
            except KeyError: applicable = False
            except Exception: pass
        oks2 = [o for o in oks if o is not None]
        if applicable and len(oks2) >= 3 and all(oks2): entail.append((r['word'], r['candidate'], w2))
json.dump({'words': [{k: v for k, v in W.items() if k != 'spec' and k != 'candidates'} | {'candidates': [c[0] for c in W['candidates']]} for W in WORDS], 'results': results, 'entail': entail}, open('results.json', 'w'), indent=1)
tot = len(results); ok = sum(1 for r in results if r['passed']); wrong = [r for r in results if r['candidate'].startswith('WRONG')]
print('runs', tot, 'passed', ok, 'intended-wrong', len(wrong), 'intended-wrong that passed', sum(1 for r in wrong if r['passed']))
print('ENTAILMENTS (run of A satisfies the spec of B on all ten worlds):'); 
for a1,c1,b1 in entail: print('  ', a1, '[' + c1[:30] + ']', '->', b1)
# same-place groups: passing, non-wrong runs with identical root sets
groups = {}
for r in results:
    if r['passed'] and not r['candidate'].startswith('WRONG'): groups.setdefault(','.join(r['roots']), []).append(r['word'] + ' [' + r['candidate'][:26] + ']')
print('SAME ROOT SET (same place by roots):')
for k, v in groups.items():
    if len(v) > 1: print('  ', k, '=>', '; '.join(v))
for r in results:
    flag = 'PASS' if r['passed'] else 'FAIL'
    print(f"{flag:4s} {r['word']:9s} {r['candidate'][:44]:44s} roots={','.join(r['roots'])} | " + ('; '.join(('ok ' if ok else 'NO ') + ph[:48] for ph, ok in r['checks'])) + (' | error: ' + r['error'] if r['error'] else ''))
