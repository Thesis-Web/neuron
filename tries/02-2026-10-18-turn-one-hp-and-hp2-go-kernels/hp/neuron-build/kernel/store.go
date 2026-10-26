package main

// store.go: the brain's body on disk (one SQLite file) and its life in RAM.
// The kernel loads once at start, writes to RAM, and commits dirty rows each beat.

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"

	_ "modernc.org/sqlite"
)

type Gate struct {
	Id      int
	P       [3]float64
	Bind    string // "" | physics word | "value" | "proc" | "rel"
	BVal    string // the physics word, the value, the string of gates, or "fwd back"
	Miss    int
	Made    string
	By      int
	Shards  map[[2]int]*Shard // key: arrival, head
	Trigs   []*Trig
	Rels    []*Rel // relationships from this gate
	RelsIn  []*Rel // relationships to this gate
	Cell    [3]int
	Str     []int // parsed proc string
	Val     float64
	Sources *Source
}

type Shard struct {
	Gate, Arr, Head, Next int
	Seen, Right, Wrong    int
	Last                  int64
	Made                  string
	By                    int
}

type Trig struct {
	Gate, Arr, Head, To int
	Worth               float64
	Made                string
	By                  int
}

type Rel struct {
	From, Type, To int
	Strength       float64
	State          string
	When           int64
	Made           string
	By             int
	dead           bool
}

type Mem struct {
	Id                 int
	Kind               string
	Home               int
	Tier, Fid          string
	Sig, Shape, Body   string
	Outcome            string
	First, Last        int64
	Seen, Right, Wrong int
	Prev               int
	Made               string
	By                 int
	onDisk             bool
	dead               bool
}

type Def struct {
	Gate, Sec, Line int
	Body            string
	Made            string
	By              int
}

type Source struct {
	Gate     int
	Name     string
	How      []string
	Grounded int
}

type Trust struct {
	Source, Topic int
	Right, Wrong  int
	Weight        float64
}

type Receipt struct {
	Kind, Key string
	Mem       int
	When      int64
}

type TL struct {
	T   int64
	Mem int
}

type Store struct {
	db       *sql.DB
	gates    []*Gate
	labels   map[string]int // text\x00lang -> gate
	glabel   map[int][]string
	grid     map[[3]int][]int
	values   map[string][]int
	consts   map[string][]int // told constants (VALUE.const), by value
	mems     map[int]*Mem
	memSig   map[string]int   // kind\x00sig -> mem
	memShape map[string][]int // shape -> mems
	memKind  map[string][]int // kind -> mems (lists)
	memKey   map[string]int   // kind\x00key(sig) for list rows
	tl       []TL
	defs     map[int]map[int][]*Def
	sources  map[int]*Source
	trust    map[[2]int]*Trust
	byBind   map[string]int
	memNext  int
	active   int  // memories in the active tier (kept as rows change, so no sweep is needed)
	told     bool // told ends
	// dirty
	dGate  map[int]bool
	dShard map[*Shard]bool
	dTrig  map[*Trig]bool
	dRel   map[*Rel]bool
	dMem   map[*Mem]bool
	dDef   map[*Def]bool
	dLabel map[string]string
	dTL    []TL
	dRec   []Receipt
	dSrc   map[int]bool
	dTrust map[*Trust]bool
	dKV    map[string]string
	recs   map[string][]int // kind\x00key -> mems
}

const schema = `
CREATE TABLE IF NOT EXISTS gate(gate INTEGER PRIMARY KEY, x REAL NOT NULL, y REAL NOT NULL, z REAL NOT NULL, bind TEXT NOT NULL, bval TEXT NOT NULL, miss INTEGER NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS shard(gate INTEGER NOT NULL, arrival INTEGER NOT NULL, head INTEGER NOT NULL, next INTEGER NOT NULL, seen INTEGER NOT NULL, right INTEGER NOT NULL, wrong INTEGER NOT NULL, last INTEGER NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL, PRIMARY KEY(gate,arrival,head));
CREATE TABLE IF NOT EXISTS trig(gate INTEGER NOT NULL, arrival INTEGER NOT NULL, head INTEGER NOT NULL, togate INTEGER NOT NULL, worth REAL NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL, PRIMARY KEY(gate,arrival,head,togate));
CREATE TABLE IF NOT EXISTS rel(fromg INTEGER NOT NULL, type INTEGER NOT NULL, tog INTEGER NOT NULL, strength REAL NOT NULL, state TEXT NOT NULL, whenat INTEGER NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL, PRIMARY KEY(fromg,type,tog));
CREATE INDEX IF NOT EXISTS rel_to ON rel(tog,type);
CREATE TABLE IF NOT EXISTS mem(id INTEGER PRIMARY KEY, kind TEXT NOT NULL, home INTEGER NOT NULL, tier TEXT NOT NULL, fid TEXT NOT NULL, sig TEXT NOT NULL, shape TEXT NOT NULL, body TEXT NOT NULL, outcome TEXT NOT NULL, first INTEGER NOT NULL, last INTEGER NOT NULL, seen INTEGER NOT NULL, right INTEGER NOT NULL, wrong INTEGER NOT NULL, prev INTEGER NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS mem_sig ON mem(kind,sig);
CREATE INDEX IF NOT EXISTS mem_shape ON mem(shape);
CREATE INDEX IF NOT EXISTS mem_kind ON mem(kind,last);
CREATE TABLE IF NOT EXISTS timeline(t INTEGER NOT NULL, mem INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS tl_t ON timeline(t);
CREATE TABLE IF NOT EXISTS label(text TEXT NOT NULL, lang TEXT NOT NULL, gate INTEGER NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL, PRIMARY KEY(text,lang));
CREATE INDEX IF NOT EXISTS label_gate ON label(gate);
CREATE TABLE IF NOT EXISTS def(gate INTEGER NOT NULL, section INTEGER NOT NULL, line INTEGER NOT NULL, body TEXT NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL, PRIMARY KEY(gate,section,line));
CREATE TABLE IF NOT EXISTS receipt(kind TEXT NOT NULL, key TEXT NOT NULL, mem INTEGER NOT NULL, whenat INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS receipt_key ON receipt(kind,key);
CREATE TABLE IF NOT EXISTS source(gate INTEGER PRIMARY KEY, name TEXT NOT NULL, how TEXT NOT NULL, grounded INTEGER NOT NULL, made TEXT NOT NULL, by INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS trust(source INTEGER NOT NULL, topic INTEGER NOT NULL, right INTEGER NOT NULL, wrong INTEGER NOT NULL, weight REAL NOT NULL, PRIMARY KEY(source,topic));
CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT NOT NULL);
`

func openStore(path string) *Store {
	db, err := sql.Open("sqlite", path+"?_pragma=journal_mode(DELETE)&_pragma=synchronous(NORMAL)&_pragma=busy_timeout(5000)")
	must(err)
	db.SetMaxOpenConns(1)
	_, err = db.Exec(schema)
	must(err)
	s := &Store{db: db, labels: map[string]int{}, glabel: map[int][]string{}, grid: map[[3]int][]int{}, values: map[string][]int{}, consts: map[string][]int{},
		mems: map[int]*Mem{}, memSig: map[string]int{}, memShape: map[string][]int{}, memKind: map[string][]int{}, memKey: map[string]int{},
		defs: map[int]map[int][]*Def{}, recs: map[string][]int{}, sources: map[int]*Source{}, trust: map[[2]int]*Trust{}, byBind: map[string]int{}}
	s.clearDirty()
	s.load()
	return s
}

func (s *Store) clearDirty() {
	s.dGate, s.dShard, s.dTrig, s.dRel = map[int]bool{}, map[*Shard]bool{}, map[*Trig]bool{}, map[*Rel]bool{}
	s.dMem, s.dDef, s.dLabel, s.dSrc, s.dTrust = map[*Mem]bool{}, map[*Def]bool{}, map[string]string{}, map[int]bool{}, map[*Trust]bool{}
	s.dTL, s.dRec, s.dKV = nil, nil, map[string]string{}
}

func (s *Store) load() {
	q := func(sql string, f func(*sql.Rows)) {
		rows, err := s.db.Query(sql)
		must(err)
		defer rows.Close()
		for rows.Next() {
			f(rows)
		}
	}
	q("SELECT gate,x,y,z,bind,bval,miss,made,by FROM gate ORDER BY gate", func(r *sql.Rows) {
		g := &Gate{Shards: map[[2]int]*Shard{}}
		must(r.Scan(&g.Id, &g.P[0], &g.P[1], &g.P[2], &g.Bind, &g.BVal, &g.Miss, &g.Made, &g.By))
		for len(s.gates) < g.Id {
			s.gates = append(s.gates, nil)
		}
		s.gates = append(s.gates, g)
		s.index(g)
	})
	q("SELECT gate,arrival,head,next,seen,right,wrong,last,made,by FROM shard", func(r *sql.Rows) {
		sh := &Shard{}
		must(r.Scan(&sh.Gate, &sh.Arr, &sh.Head, &sh.Next, &sh.Seen, &sh.Right, &sh.Wrong, &sh.Last, &sh.Made, &sh.By))
		s.gates[sh.Gate].Shards[[2]int{sh.Arr, sh.Head}] = sh
	})
	q("SELECT gate,arrival,head,togate,worth,made,by FROM trig", func(r *sql.Rows) {
		t := &Trig{}
		must(r.Scan(&t.Gate, &t.Arr, &t.Head, &t.To, &t.Worth, &t.Made, &t.By))
		s.gates[t.Gate].Trigs = append(s.gates[t.Gate].Trigs, t)
	})
	q("SELECT fromg,type,tog,strength,state,whenat,made,by FROM rel", func(r *sql.Rows) {
		rl := &Rel{}
		must(r.Scan(&rl.From, &rl.Type, &rl.To, &rl.Strength, &rl.State, &rl.When, &rl.Made, &rl.By))
		s.gates[rl.From].Rels = append(s.gates[rl.From].Rels, rl)
		s.gates[rl.To].RelsIn = append(s.gates[rl.To].RelsIn, rl)
	})
	q("SELECT id,kind,home,tier,fid,sig,shape,CASE WHEN tier='long' THEN '' ELSE body END,outcome,first,last,seen,right,wrong,prev,made,by FROM mem", func(r *sql.Rows) {
		m := &Mem{}
		must(r.Scan(&m.Id, &m.Kind, &m.Home, &m.Tier, &m.Fid, &m.Sig, &m.Shape, &m.Body, &m.Outcome, &m.First, &m.Last, &m.Seen, &m.Right, &m.Wrong, &m.Prev, &m.Made, &m.By))
		m.onDisk = m.Tier == "long"
		s.indexMem(m)
	})
	q("SELECT t,mem FROM timeline ORDER BY t", func(r *sql.Rows) {
		var t TL
		must(r.Scan(&t.T, &t.Mem))
		s.tl = append(s.tl, t)
	})
	q("SELECT text,lang,gate FROM label ORDER BY rowid", func(r *sql.Rows) {
		var t, l string
		var g int
		must(r.Scan(&t, &l, &g))
		s.labels[t+"\x00"+l] = g
		s.glabel[g] = append(s.glabel[g], t)
	})
	q("SELECT gate,section,line,body,made,by FROM def", func(r *sql.Rows) {
		d := &Def{}
		must(r.Scan(&d.Gate, &d.Sec, &d.Line, &d.Body, &d.Made, &d.By))
		s.putDef(d)
	})
	q("SELECT kind,key,mem FROM receipt", func(r *sql.Rows) {
		var k, key string
		var m int
		must(r.Scan(&k, &key, &m))
		s.recs[k+"\x00"+key] = append(s.recs[k+"\x00"+key], m)
	})
	q("SELECT gate,name,how,grounded FROM source", func(r *sql.Rows) {
		src := &Source{}
		var how string
		must(r.Scan(&src.Gate, &src.Name, &how, &src.Grounded))
		json.Unmarshal([]byte(how), &src.How)
		s.sources[src.Gate] = src
	})
	q("SELECT source,topic,right,wrong,weight FROM trust", func(r *sql.Rows) {
		t := &Trust{}
		must(r.Scan(&t.Source, &t.Topic, &t.Right, &t.Wrong, &t.Weight))
		s.trust[[2]int{t.Source, t.Topic}] = t
	})
	q("SELECT k,v FROM kv", func(r *sql.Rows) {
		var k, v string
		must(r.Scan(&k, &v))
		if k == "told" && v == "ends" {
			s.told = true
		}
	})
	for _, g := range s.gates { // a told value gate with no label is a constant, not a number's gate
		if g != nil && g.Bind == "value" && g.Made == "told" && len(s.glabel[g.Id]) == 0 {
			s.rebind(g, "VALUE.const", g.BVal)
		}
	}
	for id := range s.mems {
		if id >= s.memNext {
			s.memNext = id + 1
		}
	}
	if s.memNext == 0 {
		s.memNext = 1
	}
}

func cellOf(p [3]float64) [3]int {
	return [3]int{int(math.Floor(p[0])), int(math.Floor(p[1])), int(math.Floor(p[2]))}
}

// index puts a gate in the RAM indexes (grid, bindings, values, parsed string).
func (s *Store) index(g *Gate) {
	g.Cell = cellOf(g.P)
	s.grid[g.Cell] = append(s.grid[g.Cell], g.Id)
	switch g.Bind {
	case "":
	case "value":
		g.Val, _ = strconv.ParseFloat(g.BVal, 64)
		s.values[g.BVal] = append(s.values[g.BVal], g.Id)
	case "proc", "rel":
		g.Str = nil
		for _, f := range strings.Fields(g.BVal) {
			n, _ := strconv.Atoi(f)
			g.Str = append(g.Str, n)
		}
	case "VALUE.const":
		g.Val, _ = strconv.ParseFloat(g.BVal, 64)
		s.consts[g.BVal] = append(s.consts[g.BVal], g.Id)
	default:
		s.byBind[g.Bind] = g.Id
		if strings.HasPrefix(g.Bind, "PROC.") {
			g.Str = nil
			for _, f := range strings.Fields(g.BVal) {
				n, _ := strconv.Atoi(f)
				g.Str = append(g.Str, n)
			}
		} else if g.BVal != "" {
			g.Val, _ = strconv.ParseFloat(g.BVal, 64)
		}
	}
}

func (s *Store) unindex(g *Gate) {
	c := s.grid[g.Cell]
	for i, id := range c {
		if id == g.Id {
			s.grid[g.Cell] = append(c[:i], c[i+1:]...)
			break
		}
	}
	if g.Bind == "value" {
		v := s.values[g.BVal]
		for i, id := range v {
			if id == g.Id {
				s.values[g.BVal] = append(v[:i], v[i+1:]...)
				break
			}
		}
	}
}

func (s *Store) indexMem(m *Mem) {
	s.mems[m.Id] = m
	if m.Tier == "active" {
		s.active++
	}
	if m.Kind == "run" || m.Kind == "birth" {
		s.memSig[m.Kind+"\x00"+m.Sig] = m.Id
	} else {
		s.memKey[m.Kind+"\x00"+m.Sig] = m.Id
	}
	if m.Shape != "" {
		s.memShape[m.Shape] = append(s.memShape[m.Shape], m.Id)
	}
	s.memKind[m.Kind] = append(s.memKind[m.Kind], m.Id)
}

// setShape changes a run memory's shape and keeps the shape index with it.
func (s *Store) setShape(m *Mem, shape string) {
	if m.Shape == shape {
		return
	}
	if m.Shape != "" {
		l := s.memShape[m.Shape]
		for i, id := range l {
			if id == m.Id {
				s.memShape[m.Shape] = append(l[:i], l[i+1:]...)
				break
			}
		}
	}
	m.Shape = shape
	if shape != "" {
		s.memShape[shape] = append(s.memShape[shape], m.Id)
	}
}

// setTier moves a memory between tiers and keeps the active count.
func (s *Store) setTier(m *Mem, tier string) {
	if m.Tier == "active" && tier != "active" {
		s.active--
	} else if m.Tier != "active" && tier == "active" {
		s.active++
	}
	m.Tier = tier
}

func (s *Store) putDef(d *Def) {
	if s.defs[d.Gate] == nil {
		s.defs[d.Gate] = map[int][]*Def{}
	}
	ls := s.defs[d.Gate][d.Sec]
	for i, o := range ls {
		if o.Line == d.Line {
			ls[i] = d
			return
		}
	}
	s.defs[d.Gate][d.Sec] = append(ls, d)
}

func (s *Store) gate(id int) *Gate {
	if id >= 0 && id < len(s.gates) {
		return s.gates[id]
	}
	return nil
}

func (s *Store) touch(g *Gate) { s.dGate[g.Id] = true }

func (s *Store) newGate(p [3]float64, bind, bval string, made string, by int) *Gate {
	g := &Gate{Id: len(s.gates), P: p, Bind: bind, BVal: bval, Made: made, By: by, Shards: map[[2]int]*Shard{}}
	g.Miss = -1 // the told miss process, unless the brain changes it
	s.gates = append(s.gates, g)
	s.index(g)
	s.touch(g)
	return g
}

func (s *Store) rebind(g *Gate, bind, bval string) {
	s.unindex(g)
	g.Bind, g.BVal = bind, bval
	s.index(g)
	s.touch(g)
}

func (s *Store) movePoint(g *Gate, p [3]float64) {
	s.unindex(g)
	g.P = p
	g.Cell = cellOf(p)
	s.grid[g.Cell] = append(s.grid[g.Cell], g.Id)
	s.touch(g)
}

func (s *Store) findPoint(p [3]float64, exclude int) []int {
	c := cellOf(p)
	var out []int
	type cand struct {
		id int
		d  float64
	}
	var cs []cand
	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			for dz := -1; dz <= 1; dz++ {
				for _, id := range s.grid[[3]int{c[0] + dx, c[1] + dy, c[2] + dz}] {
					if id == exclude {
						continue
					}
					q := s.gates[id].P
					d := (q[0]-p[0])*(q[0]-p[0]) + (q[1]-p[1])*(q[1]-p[1]) + (q[2]-p[2])*(q[2]-p[2])
					cs = append(cs, cand{id, d})
				}
			}
		}
	}
	sort.Slice(cs, func(i, j int) bool { return cs[i].d < cs[j].d })
	for _, c := range cs {
		out = append(out, c.id)
	}
	return out
}

func (s *Store) label(text, lang string) (int, bool) {
	g, ok := s.labels[text+"\x00"+lang]
	return g, ok
}

func (s *Store) setLabel(text, lang string, gate int, made string, by int) {
	k := text + "\x00" + lang
	if old, ok := s.labels[k]; ok && old != gate {
		ls := s.glabel[old]
		for i, t := range ls {
			if t == text {
				s.glabel[old] = append(ls[:i], ls[i+1:]...)
				break
			}
		}
	}
	s.labels[k] = gate
	s.glabel[gate] = append(s.glabel[gate], text)
	s.dLabel[k] = made + "\x00" + strconv.Itoa(by)
}

func (s *Store) newMem(kind string, home int, sig string, made string, by int, t int64) *Mem {
	m := &Mem{Id: s.memNext, Kind: kind, Home: home, Tier: "active", Fid: "exact", Sig: sig, First: t, Last: t, Seen: 1, Made: made, By: by}
	s.memNext++
	if by == 0 {
		m.By = m.Id
	}
	s.indexMem(m)
	s.dMem[m] = true
	return m
}

func (s *Store) memBody(m *Mem) string {
	if m.onDisk && m.Body == "" {
		s.db.QueryRow("SELECT body FROM mem WHERE id=?", m.Id).Scan(&m.Body)
	}
	return m.Body
}

func (s *Store) addTL(t int64, mem int) {
	e := TL{t, mem}
	n := len(s.tl)
	if n > 0 && s.tl[n-1].T > t {
		i := sort.Search(n, func(i int) bool { return s.tl[i].T > t })
		s.tl = append(s.tl[:i], append([]TL{e}, s.tl[i:]...)...)
	} else {
		s.tl = append(s.tl, e)
	}
	s.dTL = append(s.dTL, e)
}

func (s *Store) findTime(a, b int64) []int {
	i := sort.Search(len(s.tl), func(i int) bool { return s.tl[i].T >= a })
	var out []int
	for ; i < len(s.tl) && s.tl[i].T <= b; i++ {
		out = append(out, s.tl[i].Mem)
	}
	return out
}

func (s *Store) kv(k, v string) { s.dKV[k] = v }

func (s *Store) receipt(kind, key string, mem int, t int64) {
	k := kind + "\x00" + key
	for _, m := range s.recs[k] {
		if m == mem {
			return
		}
	}
	s.recs[k] = append(s.recs[k], mem)
	s.dRec = append(s.dRec, Receipt{kind, key, mem, t})
}

// commit writes every dirty row in one transaction.
func (s *Store) commit() int {
	n := len(s.dGate) + len(s.dShard) + len(s.dTrig) + len(s.dRel) + len(s.dMem) + len(s.dDef) + len(s.dLabel) + len(s.dTL) + len(s.dRec) + len(s.dSrc) + len(s.dTrust) + len(s.dKV)
	if n == 0 {
		return 0
	}
	tx, err := s.db.Begin()
	must(err)
	ex := func(q string, a ...any) { _, err := tx.Exec(q, a...); must(err) }
	for id := range s.dGate {
		g := s.gates[id]
		ex("INSERT OR REPLACE INTO gate VALUES(?,?,?,?,?,?,?,?,?)", g.Id, g.P[0], g.P[1], g.P[2], g.Bind, g.BVal, g.Miss, g.Made, g.By)
	}
	// deletes go first: a re-told row and the row it replaces share a key, and the map order is random
	for sh := range s.dShard {
		if sh.Next < 0 {
			ex("DELETE FROM shard WHERE gate=? AND arrival=? AND head=?", sh.Gate, sh.Arr, sh.Head)
		}
	}
	for sh := range s.dShard {
		if sh.Next >= 0 {
			ex("INSERT OR REPLACE INTO shard VALUES(?,?,?,?,?,?,?,?,?,?)", sh.Gate, sh.Arr, sh.Head, sh.Next, sh.Seen, sh.Right, sh.Wrong, sh.Last, sh.Made, sh.By)
		}
	}
	for t := range s.dTrig {
		if t.Worth < 0 {
			ex("DELETE FROM trig WHERE gate=? AND arrival=? AND head=? AND togate=?", t.Gate, t.Arr, t.Head, t.To)
		}
	}
	for t := range s.dTrig {
		if t.Worth >= 0 {
			ex("INSERT OR REPLACE INTO trig VALUES(?,?,?,?,?,?,?)", t.Gate, t.Arr, t.Head, t.To, t.Worth, t.Made, t.By)
		}
	}
	for r := range s.dRel {
		if r.dead {
			ex("DELETE FROM rel WHERE fromg=? AND type=? AND tog=?", r.From, r.Type, r.To)
		}
	}
	for r := range s.dRel {
		if !r.dead {
			ex("INSERT OR REPLACE INTO rel VALUES(?,?,?,?,?,?,?,?)", r.From, r.Type, r.To, r.Strength, r.State, r.When, r.Made, r.By)
		}
	}
	for m := range s.dMem {
		if m.dead {
			ex("DELETE FROM mem WHERE id=?", m.Id)
			ex("DELETE FROM timeline WHERE mem=?", m.Id)
		}
	}
	for m := range s.dMem {
		if m.dead {
			continue
		} else if m.onDisk && m.Body == "" {
			ex("UPDATE mem SET kind=?,home=?,tier=?,fid=?,sig=?,shape=?,outcome=?,first=?,last=?,seen=?,right=?,wrong=?,prev=?,made=?,by=? WHERE id=?", m.Kind, m.Home, m.Tier, m.Fid, m.Sig, m.Shape, m.Outcome, m.First, m.Last, m.Seen, m.Right, m.Wrong, m.Prev, m.Made, m.By, m.Id)
		} else {
			ex("INSERT OR REPLACE INTO mem VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", m.Id, m.Kind, m.Home, m.Tier, m.Fid, m.Sig, m.Shape, m.Body, m.Outcome, m.First, m.Last, m.Seen, m.Right, m.Wrong, m.Prev, m.Made, m.By)
			if m.Tier == "long" {
				m.onDisk, m.Body = true, ""
			}
		}
	}
	for d := range s.dDef {
		if d.Body == "" {
			ex("DELETE FROM def WHERE gate=? AND section=? AND line=?", d.Gate, d.Sec, d.Line)
		} else {
			ex("INSERT OR REPLACE INTO def VALUES(?,?,?,?,?,?)", d.Gate, d.Sec, d.Line, d.Body, d.Made, d.By)
		}
	}
	for k, mb := range s.dLabel {
		tl := strings.SplitN(k, "\x00", 2)
		mbs := strings.SplitN(mb, "\x00", 2)
		g, ok := s.labels[k]
		if !ok {
			ex("DELETE FROM label WHERE text=? AND lang=?", tl[0], tl[1])
		} else {
			ex("INSERT OR REPLACE INTO label VALUES(?,?,?,?,?)", tl[0], tl[1], g, mbs[0], mbs[1])
		}
	}
	for _, t := range s.dTL {
		ex("INSERT INTO timeline VALUES(?,?)", t.T, t.Mem)
	}
	for _, r := range s.dRec {
		ex("INSERT INTO receipt VALUES(?,?,?,?)", r.Kind, r.Key, r.Mem, r.When)
	}
	for id := range s.dSrc {
		src := s.sources[id]
		how, _ := json.Marshal(src.How)
		ex("INSERT OR REPLACE INTO source VALUES(?,?,?,?,?,?)", src.Gate, src.Name, string(how), src.Grounded, s.gates[id].Made, s.gates[id].By)
	}
	for t := range s.dTrust {
		ex("INSERT OR REPLACE INTO trust VALUES(?,?,?,?,?)", t.Source, t.Topic, t.Right, t.Wrong, t.Weight)
	}
	for k, v := range s.dKV {
		ex("INSERT OR REPLACE INTO kv VALUES(?,?)", k, v)
	}
	must(tx.Commit())
	s.clearDirty()
	return n
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func fnum(f float64) string {
	if f == math.Trunc(f) && math.Abs(f) < 1e15 {
		return strconv.FormatInt(int64(f), 10)
	}
	return strconv.FormatFloat(f, 'g', 6, 64)
}

func vstr(v [3]float64) string { return fmt.Sprintf("%s %s %s", fnum(v[0]), fnum(v[1]), fnum(v[2])) }
