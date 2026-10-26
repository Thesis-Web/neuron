package main

// The store: the brain in RAM, its body in brain.db. Every write goes to RAM
// and queues one statement; the queue is committed at the end of each beat.
// Absent is no row: optional things live in their own tables.

import (
	"database/sql"
	"fmt"
	"math"
	"slices"
	"sort"
	"strconv"
	"strings"

	_ "github.com/mattn/go-sqlite3"
)

type Val struct {
	K byte // g gate, n number, p point, t text, l list
	G int64
	N float64
	P [3]float64
	T string
	L []Val
}

func gv(g int64) Val      { return Val{K: 'g', G: g} }
func nv(n float64) Val    { return Val{K: 'n', N: n} }
func tv(t string) Val     { return Val{K: 't', T: t} }
func pv(p [3]float64) Val { return Val{K: 'p', P: p} }

func (v Val) enc() string {
	switch v.K {
	case 'g':
		return "g" + strconv.FormatInt(v.G, 10)
	case 'n':
		return "n" + strconv.FormatFloat(v.N, 'g', -1, 64)
	case 'p':
		return fmt.Sprintf("p%g,%g,%g", v.P[0], v.P[1], v.P[2])
	case 'l':
		s, nested := make([]string, len(v.L)), false
		for i, x := range v.L {
			s[i], nested = x.enc(), nested || x.K == 'l'
		}
		if nested { // a list that holds a list: each item length-first, so the inner lists come back whole
			var b strings.Builder
			b.WriteString("L")
			for _, x := range s {
				b.WriteString(strconv.Itoa(len(x)) + ":" + x)
			}
			return b.String()
		}
		return "l" + strings.Join(s, "\x1f")
	}
	return "t" + v.T
}

func dec(s string) Val {
	if s == "" {
		return Val{K: 'l'}
	}
	b := s[1:]
	switch s[0] {
	case 'g':
		g, _ := strconv.ParseInt(b, 10, 64)
		return gv(g)
	case 'n':
		n, _ := strconv.ParseFloat(b, 64)
		return nv(n)
	case 'p':
		var p [3]float64
		fmt.Sscanf(b, "%g,%g,%g", &p[0], &p[1], &p[2])
		return pv(p)
	case 'l':
		v := Val{K: 'l'}
		for _, x := range strings.Split(b, "\x1f") {
			if x != "" {
				v.L = append(v.L, dec(x))
			}
		}
		return v
	case 'L':
		v := Val{K: 'l'}
		for len(b) > 0 {
			i := strings.IndexByte(b, ':')
			n, err := strconv.Atoi(b[:max(i, 0)])
			if i < 0 || err != nil || i+1+n > len(b) {
				break
			}
			v.L, b = append(v.L, dec(b[i+1:i+1+n])), b[i+1+n:]
		}
		return v
	}
	return tv(b)
}

type SK struct{ Arr, Head int64 }
type Trig struct {
	Out   int64
	Worth float64
}
type Shard struct {
	Next               int64
	Out                []Trig
	Seen, Right, Wrong int
	Last, Made         int64
}
type Rel struct {
	A, Type, B           int64
	S                    float64
	State, Rcpt, T, Made int64
}
type Sect struct {
	V       Val
	Rcpt, T int64
}
type Gate struct {
	P                [3]float64
	Miss, Made, Rcpt int64
	Phys             string
	HasVal, Core     bool
	Val              float64
	Proc             []int64
	Sh               map[SK]*Shard
	Usual            []Trig
	Out              map[[2]int64]*Rel // (type,b)
	Sect             map[int64][]Sect
	Labels           [][2]string // text, lang
}
type Mem struct {
	ID, Kind, Home, Tier, Fid, Made int64
	Sig, Shape                      string
	HasSig, HasBody, HasOut         bool
	Body                            []Val
	Out                             Val
	First, Last                     int64
	Seen, Right, Wrong              int
}
type TL struct{ T, Mem int64 }
type op struct {
	q string
	a []any
}
type Src struct {
	How      string
	Grounded bool
}

type Brain struct {
	db      *sql.DB
	G       []*Gate
	M       map[int64]*Mem
	nextMem int64
	names   map[string]int64
	rnames  map[int64]string
	labels  map[string][]int64 // text -> gates, newest first
	vals    map[float64][]int64
	grid    map[[3]int64][]int64
	cell    float64
	sigs    map[string]int64
	shapes  map[string][]int64
	kinds   map[int64][]int64 // the sixth's lists: kind -> ids, least recently touched first
	homes   map[[2]int64][]int64
	tl      []TL
	src     map[int64]Src
	trust   map[[2]int64][2]int
	meta    map[string]string
	ops     []op
	active  int    // memories in the ACTIVE tier (kept as they move, never counted by a scan)
	drop    []*Mem // long-term memories whose bodies leave RAM once this beat is committed
}

const schema = `
CREATE TABLE IF NOT EXISTS gate(g INTEGER PRIMARY KEY, x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL, miss INTEGER NOT NULL, made INTEGER NOT NULL, rcpt INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS phys(g INTEGER PRIMARY KEY, word TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS val(g INTEGER PRIMARY KEY, v REAL NOT NULL);
CREATE TABLE IF NOT EXISTS proc(g INTEGER PRIMARY KEY, str TEXT NOT NULL, made INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS name(name TEXT PRIMARY KEY, g INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS label(text TEXT NOT NULL, lang TEXT NOT NULL, g INTEGER NOT NULL, made INTEGER NOT NULL, PRIMARY KEY(text,lang,g));
CREATE INDEX IF NOT EXISTS label_g ON label(g);
CREATE TABLE IF NOT EXISTS shard(g INTEGER NOT NULL, arr INTEGER NOT NULL, head INTEGER NOT NULL, next INTEGER NOT NULL, seen INTEGER NOT NULL, right INTEGER NOT NULL, wrong INTEGER NOT NULL, last INTEGER NOT NULL, made INTEGER NOT NULL, PRIMARY KEY(g,arr,head));
CREATE TABLE IF NOT EXISTS trig(g INTEGER NOT NULL, arr INTEGER NOT NULL, head INTEGER NOT NULL, out INTEGER NOT NULL, worth REAL NOT NULL, PRIMARY KEY(g,arr,head,out));
CREATE TABLE IF NOT EXISTS usual(g INTEGER NOT NULL, out INTEGER NOT NULL, worth REAL NOT NULL, PRIMARY KEY(g,out));
CREATE TABLE IF NOT EXISTS rel(a INTEGER NOT NULL, type INTEGER NOT NULL, b INTEGER NOT NULL, strength REAL NOT NULL, state INTEGER NOT NULL, rcpt INTEGER NOT NULL, t INTEGER NOT NULL, made INTEGER NOT NULL, PRIMARY KEY(a,type,b));
CREATE INDEX IF NOT EXISTS rel_b ON rel(b,type);
CREATE TABLE IF NOT EXISTS sect(g INTEGER NOT NULL, sec INTEGER NOT NULL, n INTEGER NOT NULL, v TEXT NOT NULL, rcpt INTEGER NOT NULL, t INTEGER NOT NULL, PRIMARY KEY(g,sec,n));
CREATE TABLE IF NOT EXISTS mem(id INTEGER PRIMARY KEY, kind INTEGER NOT NULL, home INTEGER NOT NULL, tier INTEGER NOT NULL, fid INTEGER NOT NULL, first INTEGER NOT NULL, last INTEGER NOT NULL, seen INTEGER NOT NULL, right INTEGER NOT NULL, wrong INTEGER NOT NULL, made INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS mem_kind ON mem(kind,last);
CREATE INDEX IF NOT EXISTS mem_home ON mem(home,kind);
CREATE TABLE IF NOT EXISTS msig(mem INTEGER PRIMARY KEY, sig TEXT NOT NULL, shape TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS msig_sig ON msig(sig);
CREATE INDEX IF NOT EXISTS msig_shape ON msig(shape);
CREATE TABLE IF NOT EXISTS mbody(mem INTEGER PRIMARY KEY, body TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS mout(mem INTEGER PRIMARY KEY, out TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tl(t INTEGER NOT NULL, mem INTEGER NOT NULL, PRIMARY KEY(t,mem));
CREATE TABLE IF NOT EXISTS src(g INTEGER PRIMARY KEY, how TEXT NOT NULL, grounded INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS trust(src INTEGER NOT NULL, topic INTEGER NOT NULL, right INTEGER NOT NULL, wrong INTEGER NOT NULL, PRIMARY KEY(src,topic));
CREATE TABLE IF NOT EXISTS core(g INTEGER PRIMARY KEY);
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT NOT NULL);
`

func open(path string) *Brain {
	db, err := sql.Open("sqlite3", path+"?_journal_mode=WAL&_synchronous=NORMAL")
	must(err)
	db.SetMaxOpenConns(1)
	_, err = db.Exec(schema)
	must(err)
	b := &Brain{db: db, M: map[int64]*Mem{}, names: map[string]int64{}, rnames: map[int64]string{}, labels: map[string][]int64{},
		vals: map[float64][]int64{}, grid: map[[3]int64][]int64{}, sigs: map[string]int64{},
		shapes: map[string][]int64{}, kinds: map[int64][]int64{}, homes: map[[2]int64][]int64{},
		src: map[int64]Src{}, trust: map[[2]int64][2]int{}, meta: map[string]string{}, nextMem: 1}
	b.load()
	return b
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

// each scans every row of a query into dst and calls f.
func (b *Brain) each(q string, f func(), dst ...any) {
	r, err := b.db.Query(q)
	must(err)
	defer r.Close()
	for r.Next() {
		must(r.Scan(dst...))
		f()
	}
}

// load reads brain.db into RAM once, at start. Long-term memory bodies stay on disk.
func (b *Brain) load() {
	var g, a, h, n, m int64
	var s, t string
	var v float64
	var mm *Mem
	gt := newGate()
	b.each("SELECT g,x,y,z,miss,made,rcpt FROM gate ORDER BY g", func() {
		x := *gt
		x.Sh, x.Out, x.Sect = map[SK]*Shard{}, map[[2]int64]*Rel{}, map[int64][]Sect{}
		b.G = append(b.G, &x)
	}, &g, &gt.P[0], &gt.P[1], &gt.P[2], &gt.Miss, &gt.Made, &gt.Rcpt)
	b.each("SELECT g,word FROM phys", func() { b.G[g].Phys = s }, &g, &s)
	b.each("SELECT g,v FROM val", func() { b.G[g].HasVal, b.G[g].Val = true, v; b.vals[v] = append(b.vals[v], g) }, &g, &v)
	b.each("SELECT g,str FROM proc", func() { b.G[g].Proc = parseStr(s) }, &g, &s)
	b.each("SELECT name,g FROM name", func() { b.names[s], b.rnames[g] = g, s }, &s, &g)
	b.gridAll()
	b.each("SELECT text,lang,g FROM label ORDER BY rowid", func() {
		if t != "keyname" {
			b.labels[s] = append([]int64{g}, b.labels[s]...) // newest first, as when written
		}
		b.G[g].Labels = append(b.G[g].Labels, [2]string{s, t})
	}, &s, &t, &g)
	var sh Shard
	b.each("SELECT g,arr,head,next,seen,right,wrong,last,made FROM shard", func() { x := sh; b.G[g].Sh[SK{a, h}] = &x },
		&g, &a, &h, &sh.Next, &sh.Seen, &sh.Right, &sh.Wrong, &sh.Last, &sh.Made)
	b.each("SELECT g,arr,head,out,worth FROM trig", func() {
		if x := b.G[g].Sh[SK{a, h}]; x != nil {
			x.Out = append(x.Out, Trig{n, v})
		}
	}, &g, &a, &h, &n, &v)
	b.each("SELECT g,out,worth FROM usual", func() { b.G[g].Usual = append(b.G[g].Usual, Trig{n, v}) }, &g, &n, &v)
	var rl Rel
	b.each("SELECT a,type,b,strength,state,rcpt,t,made FROM rel", func() {
		x := rl
		b.G[x.A].Out[[2]int64{x.Type, x.B}] = &x
	}, &rl.A, &rl.Type, &rl.B, &rl.S, &rl.State, &rl.Rcpt, &rl.T, &rl.Made)
	b.each("SELECT g,sec,v,rcpt,t FROM sect ORDER BY g,sec,n", func() { b.G[g].Sect[a] = append(b.G[g].Sect[a], Sect{dec(s), m, n}) }, &g, &a, &s, &m, &n)
	var me Mem
	b.each("SELECT id,kind,home,tier,fid,first,last,seen,right,wrong,made FROM mem ORDER BY last", func() {
		x := me
		b.indexMem(&x)
		b.nextMem = max(b.nextMem, x.ID+1)
	}, &me.ID, &me.Kind, &me.Home, &me.Tier, &me.Fid, &me.First, &me.Last, &me.Seen, &me.Right, &me.Wrong, &me.Made)
	b.each("SELECT mem,sig,shape FROM msig", func() {
		if mm = b.M[m]; mm != nil {
			mm.HasSig = false
			b.setSigRAM(mm, s, t)
		}
	}, &m, &s, &t)
	b.each("SELECT mem,body FROM mbody", func() {
		if mm = b.M[m]; mm != nil && mm.Tier != b.names["LONG"] {
			mm.Body, mm.HasBody = dec(s).L, true
		}
	}, &m, &s)
	b.each("SELECT mem,out FROM mout", func() {
		if mm = b.M[m]; mm != nil {
			mm.Out, mm.HasOut = dec(s), true
		}
	}, &m, &s)
	b.each("SELECT t,mem FROM tl ORDER BY t,mem", func() { b.tl = append(b.tl, TL{n, m}) }, &n, &m)
	var src Src
	b.each("SELECT g,how,grounded FROM src", func() { b.src[g] = src }, &g, &src.How, &src.Grounded)
	var c [2]int
	b.each("SELECT src,topic,right,wrong FROM trust", func() { b.trust[[2]int64{g, a}] = c }, &g, &a, &c[0], &c[1])
	b.each("SELECT g FROM core", func() { b.G[g].Core = true }, &g)
	b.each("SELECT k,v FROM meta", func() { b.meta[s] = t }, &s, &t)
}

// listed: the sixth's lists are kept in order for FIND KIND; runs, definitions and births are not lists.
func (b *Brain) listed(kind int64) bool {
	return kind != b.names["RUN"] && kind != b.names["DEF"] && kind != b.names["BIRTH"]
}

func (b *Brain) indexMem(m *Mem) {
	b.M[m.ID] = m
	if m.Tier == b.names["ACTIVE"] {
		b.active++
	}
	if b.listed(m.Kind) {
		b.kinds[m.Kind] = append(b.kinds[m.Kind], m.ID)
		if m.Seen == 0 { // never touched: touched longest ago of all
			ids := b.kinds[m.Kind]
			copy(ids[1:], ids[:len(ids)-1])
			ids[0] = m.ID
		}
	}
	k := [2]int64{m.Home, m.Kind}
	b.homes[k] = append(b.homes[k], m.ID)
}

func newGate() *Gate {
	return &Gate{Sh: map[SK]*Shard{}, Out: map[[2]int64]*Rel{}, Sect: map[int64][]Sect{}}
}

func parseStr(s string) []int64 {
	out := []int64{}
	for _, f := range strings.Fields(s) {
		if g, err := strconv.ParseInt(f, 10, 64); err == nil {
			out = append(out, g)
		}
	}
	return out
}

func strOf(p []int64) string {
	s := make([]string, len(p))
	for i, g := range p {
		s[i] = strconv.FormatInt(g, 10)
	}
	return strings.Join(s, " ")
}

func (b *Brain) q(s string, a ...any) { b.ops = append(b.ops, op{s, a}) }

// commit writes the beat's changed rows. An idle beat has no ops and writes nothing.
func (b *Brain) commit() {
	if len(b.ops) == 0 {
		return
	}
	tx, err := b.db.Begin()
	must(err)
	for _, o := range b.ops {
		if _, err := tx.Exec(o.q, o.a...); err != nil {
			panic(fmt.Sprintf("%v: %s", err, o.q))
		}
	}
	must(tx.Commit())
	b.ops = b.ops[:0]
	// a long-term memory lives on disk: its body leaves RAM once it is written
	for _, m := range b.drop {
		if m.Tier == b.names["LONG"] {
			m.Body, m.HasBody = nil, false
		}
	}
	b.drop = b.drop[:0]
}

func (b *Brain) nm(n string) int64 { return b.names[n] }

func (b *Brain) gate(g int64) *Gate {
	if g < 0 || g >= int64(len(b.G)) {
		return nil
	}
	return b.G[g]
}

// grid builds the point index with the cell the told CELL holds (none: no index, and
// nothing is near anything). A changed CELL takes effect when the brain next starts.
func (b *Brain) gridAll() {
	if g := b.gate(b.nm("CELL")); g != nil && g.HasVal && g.Val > 0 && b.cell == 0 {
		b.cell = g.Val
		for i := range b.G {
			b.gridAdd(int64(i))
		}
	}
}

func (b *Brain) cellOf(p [3]float64) [3]int64 {
	c := b.cell
	return [3]int64{int64(math.Floor(p[0] / c)), int64(math.Floor(p[1] / c)), int64(math.Floor(p[2] / c))}
}
func (b *Brain) gridAdd(g int64) {
	if b.cell > 0 {
		c := b.cellOf(b.G[g].P)
		b.grid[c] = append(b.grid[c], g)
	}
}
func (b *Brain) gridDel(g int64) {
	if b.cell > 0 {
		c := b.cellOf(b.G[g].P)
		b.grid[c] = del(b.grid[c], g)
	}
}

func del(s []int64, x int64) []int64 {
	for i, v := range s {
		if v == x {
			return append(s[:i:i], s[i+1:]...)
		}
	}
	return s
}

// near is the gates in a point's cell and its neighbours: an index reach, never a scan.
func (b *Brain) near(p [3]float64) []int64 {
	if b.cell <= 0 {
		return nil
	}
	c := b.cellOf(p)
	var out []int64
	for i := 0; i < 27; i++ {
		out = append(out, b.grid[[3]int64{c[0] + int64(i%3) - 1, c[1] + int64(i/3%3) - 1, c[2] + int64(i/9) - 1}]...)
	}
	return out
}

func dist(a, c [3]float64) float64 {
	return math.Sqrt((a[0]-c[0])*(a[0]-c[0]) + (a[1]-c[1])*(a[1]-c[1]) + (a[2]-c[2])*(a[2]-c[2]))
}

// ---- writes. Each touches RAM and queues its row.

func (b *Brain) newGate(p [3]float64, made, rcpt int64) int64 {
	g := int64(len(b.G))
	gt := newGate()
	gt.P, gt.Made, gt.Rcpt, gt.Miss = p, made, rcpt, b.nm("miss")
	b.G = append(b.G, gt)
	b.gridAdd(g)
	b.q("INSERT INTO gate VALUES(?,?,?,?,?,?,?)", g, p[0], p[1], p[2], gt.Miss, made, rcpt)
	return g
}

func (b *Brain) movePoint(g int64, p [3]float64) {
	b.gridDel(g)
	b.G[g].P = p
	b.gridAdd(g)
	b.q("UPDATE gate SET x=?,y=?,z=? WHERE g=?", p[0], p[1], p[2], g)
}

func (b *Brain) setVal(g int64, v float64) {
	gt := b.G[g]
	if gt.HasVal {
		b.vals[gt.Val] = del(b.vals[gt.Val], g)
	}
	gt.HasVal, gt.Val = true, v
	b.vals[v] = append(b.vals[v], g)
	b.q("INSERT OR REPLACE INTO val VALUES(?,?)", g, v)
}

func (b *Brain) setProc(g int64, p []int64, made int64) {
	b.G[g].Proc = p
	b.q("INSERT OR REPLACE INTO proc VALUES(?,?,?)", g, strOf(p), made)
}

func (b *Brain) addLabel(text, lang string, g, made int64) {
	for _, l := range b.G[g].Labels {
		if l[0] == text && l[1] == lang {
			return
		}
	}
	if lang != "keyname" { // what a special key is called is not a word the encoder reaches
		b.labels[text] = append([]int64{g}, b.labels[text]...)
	}
	b.G[g].Labels = append(b.G[g].Labels, [2]string{text, lang})
	b.q("INSERT OR IGNORE INTO label VALUES(?,?,?,?)", text, lang, g, made)
}

// delLabel takes a word's label off a gate (the encoder's and the decoder's); false if it had none.
func (b *Brain) delLabel(text string, g int64) bool {
	i := slices.Index(b.G[g].Labels, [2]string{text, "en"})
	if i < 0 {
		return false
	}
	b.G[g].Labels = slices.Delete(b.G[g].Labels, i, i+1)
	b.labels[text] = del(b.labels[text], g)
	b.q("DELETE FROM label WHERE text=? AND lang='en' AND g=?", text, g)
	return true
}

func (b *Brain) putShard(g int64, k SK, s *Shard) {
	b.G[g].Sh[k] = s
	b.q("INSERT OR REPLACE INTO shard VALUES(?,?,?,?,?,?,?,?,?)", g, k.Arr, k.Head, s.Next, s.Seen, s.Right, s.Wrong, s.Last, s.Made)
	b.q("DELETE FROM trig WHERE g=? AND arr=? AND head=?", g, k.Arr, k.Head)
	for _, t := range s.Out {
		b.q("INSERT OR REPLACE INTO trig VALUES(?,?,?,?,?)", g, k.Arr, k.Head, t.Out, t.Worth)
	}
}

func (b *Brain) setUsual(g, out int64, w float64) {
	gt := b.G[g]
	for i := range gt.Usual {
		if gt.Usual[i].Out == out {
			gt.Usual[i].Worth = w
			b.q("UPDATE usual SET worth=? WHERE g=? AND out=?", w, g, out)
			return
		}
	}
	gt.Usual = append(gt.Usual, Trig{out, w})
	b.q("INSERT INTO usual VALUES(?,?,?)", g, out, w)
}

func (b *Brain) putRel(x *Rel) {
	b.G[x.A].Out[[2]int64{x.Type, x.B}] = x
	b.q("INSERT OR REPLACE INTO rel VALUES(?,?,?,?,?,?,?,?)", x.A, x.Type, x.B, x.S, x.State, x.Rcpt, x.T, x.Made)
}

func (b *Brain) delRel(a, t, c int64) {
	delete(b.G[a].Out, [2]int64{t, c})
	b.q("DELETE FROM rel WHERE a=? AND type=? AND b=?", a, t, c)
}

func (b *Brain) addSect(g, sec int64, v Val, rcpt, now int64) {
	gt, e := b.G[g], v.enc()
	if ss := gt.Sect[sec]; len(ss) > 0 && ss[len(ss)-1].V.enc() == e {
		return // the same as the latest entry: nothing new to hold
	}
	gt.Sect[sec] = append(gt.Sect[sec], Sect{v, rcpt, now})
	b.q("INSERT INTO sect VALUES(?,?,?,?,?,?)", g, sec, len(gt.Sect[sec])-1, v.enc(), rcpt, now)
}

func (b *Brain) newMem(kind, home, made, now int64) *Mem {
	m := &Mem{ID: b.nextMem, Kind: kind, Home: home, Tier: b.nm("ACTIVE"), Fid: b.nm("EXACT"), First: now, Last: now, Seen: 1, Made: made}
	b.nextMem++
	b.indexMem(m)
	b.q("INSERT INTO mem VALUES(?,?,?,?,?,?,?,?,?,?,?)", m.ID, kind, home, m.Tier, m.Fid, now, now, 1, 0, 0, made)
	b.tlAdd(now, m.ID)
	return m
}

func (b *Brain) tlAdd(t, id int64) {
	i := sort.Search(len(b.tl), func(i int) bool { return b.tl[i].T > t || (b.tl[i].T == t && b.tl[i].Mem >= id) })
	if i < len(b.tl) && b.tl[i] == (TL{t, id}) {
		return
	}
	b.tl = append(b.tl, TL{})
	copy(b.tl[i+1:], b.tl[i:])
	b.tl[i] = TL{t, id}
	b.q("INSERT OR IGNORE INTO tl VALUES(?,?)", t, id)
}

func (b *Brain) saveMem(m *Mem) {
	b.q("UPDATE mem SET tier=?,fid=?,last=?,seen=?,right=?,wrong=? WHERE id=?", m.Tier, m.Fid, m.Last, m.Seen, m.Right, m.Wrong, m.ID)
}

// touchMem is the same run again: same row, a new time on the timeline.
func (b *Brain) touchMem(m *Mem, now int64) {
	if b.listed(m.Kind) {
		b.kinds[m.Kind] = append(del(b.kinds[m.Kind], m.ID), m.ID)
	}
	m.Last, m.Seen = now, min(m.Seen+1, 1000000)
	b.saveMem(m)
	b.tlAdd(now, m.ID)
}

// unsig takes a memory out of the signature and shape indexes.
func (b *Brain) unsig(m *Mem) {
	if m.HasSig {
		if b.sigs[m.Sig] == m.ID {
			delete(b.sigs, m.Sig)
		}
		b.shapes[m.Shape] = del(b.shapes[m.Shape], m.ID)
	}
}

func (b *Brain) setSigRAM(m *Mem, sig, shape string) {
	b.unsig(m)
	m.Sig, m.Shape, m.HasSig = sig, shape, true
	b.sigs[sig] = m.ID
	b.shapes[shape] = append(b.shapes[shape], m.ID)
}

func (b *Brain) setSig(m *Mem, sig, shape string) {
	b.setSigRAM(m, sig, shape)
	b.q("INSERT OR REPLACE INTO msig VALUES(?,?,?)", m.ID, sig, shape)
}

func (b *Brain) setBody(m *Mem, body []Val) {
	m.Body, m.HasBody = body, true
	if m.Tier == b.names["LONG"] {
		b.drop = append(b.drop, m)
	}
	b.q("INSERT OR REPLACE INTO mbody VALUES(?,?)", m.ID, Val{K: 'l', L: body}.enc())
}

func (b *Brain) setOut(m *Mem, v Val) {
	m.Out, m.HasOut = v, true
	b.q("INSERT OR REPLACE INTO mout VALUES(?,?)", m.ID, v.enc())
}

// bodyOf: a body in RAM, or one read from disk for this read only (a long-term
// memory's body is not kept in RAM after it is read)
func (b *Brain) bodyOf(m *Mem) ([]Val, bool) {
	var s string
	if m.HasBody {
		return m.Body, true
	}
	if b.db.QueryRow("SELECT body FROM mbody WHERE mem=?", m.ID).Scan(&s) == nil {
		return dec(s).L, true
	}
	return nil, false
}

func (b *Brain) delMem(id int64) {
	m := b.M[id]
	if m.Tier == b.names["ACTIVE"] {
		b.active--
	}
	b.unsig(m)
	b.kinds[m.Kind] = del(b.kinds[m.Kind], id)
	b.homes[[2]int64{m.Home, m.Kind}] = del(b.homes[[2]int64{m.Home, m.Kind}], id)
	delete(b.M, id)
	for _, t := range []string{"mem WHERE id", "msig WHERE mem", "mbody WHERE mem", "mout WHERE mem"} {
		b.q("DELETE FROM "+t+"=?", id)
	}
}

func (b *Brain) setMeta(k, v string) {
	b.meta[k] = v
	b.q("INSERT OR REPLACE INTO meta VALUES(?,?)", k, v)
}

func (b *Brain) setName(n string, g int64) {
	b.names[n], b.rnames[g] = g, n
	b.q("INSERT OR REPLACE INTO name VALUES(?,?)", n, g)
}
