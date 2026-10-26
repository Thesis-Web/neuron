package main

// The store words. Each takes a selector gate from the pad (what kind of row),
// then that row's keys. Absent is never a value: need() puts NONE at the head.

import (
	"fmt"
	"math"
	"regexp"
	"slices"
	"sort"
	"strconv"
	"strings"
)

type absent struct{}

// need: when something a word needs is absent, the word stops and NONE goes to the head.
func need(c bool) {
	if !c {
		panic(absent{})
	}
}

func (k *K) sel(r *Run) string {
	if n := k.rnames[k.popG(r)]; n == strings.ToUpper(n) {
		return n
	}
	return ""
}

// g pops a gate that must exist; n a number; m a memory id.
func (k *K) g(r *Run) int64   { g := k.popG(r); need(k.gate(g) != nil); return g }
func (k *K) n(r *Run) float64 { n, ok := k.popN(r); need(ok); return n }
func (k *K) m(r *Run) *Mem    { m := k.M[int64(k.n(r))]; need(m != nil); return m }
func (k *K) any(r *Run) Val   { v, ok := k.pop(r, 0); need(ok); return v }
func (k *K) top(r *Run) Val   { need(len(r.Pad) > 0); return r.Pad[len(r.Pad)-1] }

func (k *K) pushOr(r *Run, v Val, ok bool) { need(ok); k.push(r, v) }

func (k *K) labelOf(g int64) (string, bool) {
	if gt := k.gate(g); gt != nil {
		for _, lang := range []string{"en", "key"} {
			for _, l := range gt.Labels {
				if l[1] == lang {
					return l[0], true
				}
			}
		}
	}
	return "", false
}

// lines is a gate's lines of a type in the store's strength index (strongest first,
// then by gate number); which of them a run takes is the told strongest's pick.
func (k *K) lines(g, t int64) []int64 {
	var rs []*Rel
	for key, x := range gOr(k.gate(g)).Out {
		if key[0] == t {
			rs = append(rs, x)
		}
	}
	sort.Slice(rs, func(i, j int) bool { return rs[i].S > rs[j].S || rs[i].S == rs[j].S && rs[i].B < rs[j].B })
	out := make([]int64, len(rs))
	for i, x := range rs {
		out[i] = x.B
	}
	return out
}

func gl(gs []int64) Val {
	v := Val{K: 'l'}
	for _, g := range gs {
		v.L = append(v.L, gv(g))
	}
	return v
}

func (k *K) rel(r *Run) *Rel {
	c, t, a := k.g(r), k.g(r), k.g(r)
	x := k.G[a].Out[[2]int64{t, c}]
	need(x != nil)
	return x
}

func (k *K) read(r *Run) {
	s := k.sel(r)
	switch s {
	case "ITEM":
		need(len(r.Rest) > 0 && r.Rest[0].G >= 0)
		k.push(r, gv(r.Rest[0].G))
		r.Rest = r.Rest[1:]
	case "LAST":
		k.push(r, k.top(r))
	case "KIND":
		k.outcome(r, map[byte]string{'g': "GATE", 'n': "NUMBER", 't': "TEXT", 'p': "POINT", 'l': "LIST"}[k.top(r).K])
	case "MAT", "MFROM", "MHEAD":
		it := r.Ev[map[string]int{"MAT": 0, "MFROM": 1, "MHEAD": 2}[s]]
		k.push(r, itemVal(it))
	case "SUBJ":
		k.pushOr(r, r.Subj, r.HasSubj)
	case "WANT":
		k.pushOr(r, r.Want, r.HasWant)
	case "WHO", "WHAT", "WHERE":
		i := map[string]int{"WHO": 0, "WHAT": 1, "WHERE": 3}[s]
		k.pushOr(r, tv(r.Ctx[i]), r.Ctx[i] != "")
	case "WHY":
		k.pushOr(r, nv(float64(r.Why)), r.Why != 0)
	case "MODE":
		k.push(r, gv(r.Made))
	case "MEMID":
		k.pushOr(r, nv(float64(r.Mem)), r.Mem != 0)
	case "START":
		if r.Parent == nil {
			k.push(r, gv(r.home())) // an input run: where its input began
		} else {
			k.push(r, gv(r.Start))
		}
	case "MINE":
		// did the brain start this run tree itself, or did a person?
		k.outcome(r, map[bool]string{true: "YES", false: "NO"}[r.root().Conn == 0])
	case "MSIG":
		m := k.m(r)
		k.pushOr(r, gl(parseStr(m.Sig)), m.HasSig)
	case "SLOT":
		v, ok := r.Slots[k.popG(r)]
		k.pushOr(r, v, ok)
	case "SIG":
		k.push(r, gl(r.D0))
	case "TRAIL":
		k.push(r, gl(r.Trail))
	case "REL", "RELS":
		t, a := k.popG(r), k.popG(r)
		bs := k.lines(a, t)
		need(len(bs) > 0)
		if s == "REL" {
			k.hand(r, "strongest", bs, gv(a), gv(t))
			return
		}
		k.push(r, gl(bs))
	case "STRENGTH":
		k.push(r, nv(k.rel(r).S))
	case "STATE":
		k.push(r, gv(k.rel(r).State))
	case "POINT":
		k.push(r, pv(k.G[k.g(r)].P))
	case "VALUE":
		if len(r.Pad) > 0 && k.top(r).K == 't' { // written digits read as the number they write (SAY writes a number as digits)
			n, err := strconv.ParseFloat(strings.TrimSpace(k.any(r).T), 64)
			k.pushOr(r, nv(n), err == nil && !math.IsInf(n, 0) && !math.IsNaN(n))
			return
		}
		g := k.G[k.g(r)]
		k.pushOr(r, nv(g.Val), g.HasVal)
	case "LABEL":
		l, ok := k.labelOf(k.popG(r))
		k.pushOr(r, tv(l), ok)
	case "SECTION", "SECTIONS":
		sec, g := k.popG(r), k.g(r)
		ss := k.G[g].Sect[sec]
		need(len(ss) > 0)
		if s == "SECTION" {
			k.push(r, ss[len(ss)-1].V)
			return
		}
		v := Val{K: 'l'}
		for _, x := range ss {
			v.L = append(v.L, x.V)
		}
		k.push(r, v)
	case "PROC":
		g := k.G[k.g(r)]
		k.pushOr(r, gl(g.Proc), g.Proc != nil)
	case "USUAL", "WORTH":
		var out int64
		if s == "WORTH" {
			out = k.popG(r)
		}
		var gs []int64
		for _, t := range k.G[k.g(r)].Usual {
			if s == "WORTH" && t.Out == out {
				k.push(r, nv(t.Worth))
				return
			}
			gs = append(gs, t.Out)
		}
		k.pushOr(r, gl(gs), s == "USUAL" && len(gs) > 0)
	case "SHARD":
		h, a, g := k.popG(r), k.popG(r), k.g(r)
		sh := k.G[g].Sh[SK{a, h}]
		need(sh != nil)
		k.push(r, gv(sh.Next))
	case "MADE":
		if k.top(r).K == 'g' {
			k.push(r, gv(k.G[k.g(r)].Made))
			return
		}
		k.push(r, gv(k.m(r).Made))
	case "OUTCOME":
		m := k.m(r)
		k.pushOr(r, m.Out, m.HasOut)
	case "BODY":
		body, ok := k.bodyOf(k.m(r))
		k.pushOr(r, Val{K: 'l', L: body}, ok)
	case "RIGHT", "WRONG", "SEEN", "TIME", "BEGAN":
		m := k.m(r)
		k.push(r, nv(map[string]float64{"RIGHT": float64(m.Right), "WRONG": float64(m.Wrong), "SEEN": float64(m.Seen), "TIME": float64(m.Last), "BEGAN": float64(m.First)}[s]))
	case "HOME", "TIER", "FID":
		m := k.m(r)
		k.push(r, gv(map[string]int64{"HOME": m.Home, "TIER": m.Tier, "FID": m.Fid}[s]))
	case "SHAPE":
		// a memory's path redrawn from today's points, then the shape it was stored with
		m := k.m(r)
		need(m.HasSig)
		k.push(r, tv(k.shapeOf(&Run{D0: parseStr(m.Sig)})))
		k.push(r, tv(m.Shape))
	case "SIZE":
		k.push(r, nv(float64(len(k.G))))
	case "ACTIVE":
		k.push(r, nv(float64(k.active)))
	case "COUNT", "FIRST", "REST":
		v, ok := k.pop(r, 'l')
		need(ok && (s == "COUNT" || len(v.L) > 0))
		switch s {
		case "COUNT":
			k.push(r, nv(float64(len(v.L))))
		case "FIRST":
			k.push(r, v.L[0])
		default:
			k.push(r, Val{K: 'l', L: v.L[1:]})
		}
	case "TRUST":
		t, sg := k.popG(r), k.popG(r)
		c := k.trust[[2]int64{sg, t}]
		k.push(r, nv(float64(c[0])))
		k.push(r, nv(float64(c[1])))
	case "GROUNDED":
		// a peek at the source gate CALL would use
		src, ok := k.src[k.srcGate(r)]
		need(ok)
		k.outcome(r, map[bool]string{true: "YES", false: "NO"}[src.Grounded])
	default:
		k.act(r, "fault", "READ with no selector")
		need(false)
	}
}

// labelGates: the gates a text's label points to, as written, then lower-cased (a
// capital is shift + the letter key); index order
func (k *K) labelGates(t string) []int64 {
	gs := append([]int64(nil), k.labels[t]...)
	for _, g := range k.labels[strings.ToLower(t)] {
		if !slices.Contains(gs, g) {
			gs = append(gs, g)
		}
	}
	return gs
}

func itemVal(it Item) Val {
	if it.G >= 0 {
		return gv(it.G)
	}
	return tv(it.T)
}

func (k *K) srcGate(r *Run) int64 {
	for i := len(r.Pad) - 1; i >= 0; i-- {
		if r.Pad[i].K == 'g' {
			return r.Pad[i].G
		}
	}
	return -1
}

var nogate = newGate()

func gOr(g *Gate) *Gate {
	if g == nil {
		return nogate
	}
	return g
}

func (k *K) write(r *Run) {
	s := k.sel(r)
	if k.meta["told_ended"] == "" && r.Made == k.nm("TOLD") {
		r.Made = k.nm("SPAWNED")
	}
	w := func(f string, a ...any) { k.act(r, "write", fmt.Sprintf(f, a...)) }
	switch s {
	case "SHARD":
		n, h, a, g := k.g(r), k.popG(r), k.popG(r), k.g(r)
		need(k.guard(r, g, s))
		sh := k.G[g].Sh[SK{a, h}]
		if sh == nil {
			sh = &Shard{Out: append([]Trig(nil), k.G[g].Usual...), Made: r.Made}
		}
		sh.Next, sh.Last = n, k.now
		k.putShard(g, SK{a, h}, sh)
		w("shard %s from %s on %s -> %s", k.show(gv(g)), k.show(gv(a)), k.show(gv(h)), k.show(gv(n)))
	case "LABEL":
		g := k.g(r)
		t, ok := k.pop(r, 't')
		need(ok && k.guard(r, g, s))
		k.addLabel(strings.ToLower(t.T), "en", g, r.Made) // a capital is shift + the letter key
		w("label %q -> %s", t.T, k.show(gv(g)))
	case "REL":
		st, c, t, a := k.n(r), k.g(r), k.g(r), k.g(r)
		need(k.guard(r, a, s))
		x := k.G[a].Out[[2]int64{t, c}]
		if x == nil {
			x = &Rel{A: a, Type: t, B: c, State: k.state(r), Made: r.Made}
		}
		x.S, x.T, x.Rcpt = st, k.now, k.rcpt(r)
		k.putRel(x)
		w("rel %s %s %s %.3g", k.show(gv(a)), k.show(gv(t)), k.show(gv(c)), st)
	case "STATE":
		st := k.g(r)
		x := k.rel(r)
		need(k.guard(r, x.A, s))
		x.State = st
		k.putRel(x)
		w("state %s %s %s = %s", k.show(gv(x.A)), k.show(gv(x.Type)), k.show(gv(x.B)), k.show(gv(st)))
	case "VALUE":
		v, g := k.n(r), k.g(r)
		need(k.guard(r, g, s))
		k.setVal(g, v)
		w("value %s = %g", k.show(gv(g)), v)
	case "SECTION":
		v, sec, g := k.any(r), k.g(r), k.g(r)
		need(k.guard(r, g, s))
		k.addSect(g, sec, v, k.rcpt(r), k.now)
		w("section %s of %s: %s", k.show(gv(sec)), k.show(gv(g)), trunc(k.show(v), 80))
	case "PROC":
		l, ok := k.pop(r, 'l')
		g := k.popG(r)
		need(k.checked(r, "WRITE PROC"))
		need(ok && k.gate(g) != nil && k.guard(r, g, s) && len(l.L) > 0)
		var p []int64
		for _, x := range l.L {
			need(x.K == 'g' && k.gate(x.G) != nil)
			p = append(p, x.G)
		}
		k.setProc(g, p, r.Made)
		w("process %s = %s", k.show(gv(g)), k.show(l))
	case "USUAL":
		v, o, g := k.n(r), k.g(r), k.g(r)
		need(k.guard(r, g, s))
		k.setUsual(g, o, v)
		w("trigger %s on %s worth %.3g", k.show(gv(o)), k.show(gv(g)), v)
	case "MEM":
		k.writeMem(r)
	case "MHEAD":
		// the missed head is this gate (which-head's pick among the gates sharing its label)
		g, i := k.g(r), len(r.Rest)-r.Tail
		need(i >= 0 && i < len(r.Rest) && r.Rest[i].G < 0)
		r.Rest[i].G, r.Ev[2].G = g, g
	case "SLOT":
		g, v := k.g(r), k.any(r)
		if r.Slots == nil {
			r.Slots = map[int64]Val{}
		}
		r.Slots[g] = v
	case "RIGHT", "WRONG", "TOUCH":
		m := k.m(r)
		m.Right, m.Wrong = m.Right+b2i(s == "RIGHT"), m.Wrong+b2i(s == "WRONG")
		if s == "TOUCH" {
			k.touchMem(m, k.now)
			k.lastMem(r, m.ID)
		} else {
			k.saveMem(m)
		}
		w("%s memory %d", strings.ToLower(s), m.ID)
	case "OUTCOME", "BODY":
		v, m := k.any(r), k.m(r)
		if s == "BODY" && v.K == 'l' {
			k.setBody(m, v.L)
		} else if s == "OUTCOME" {
			k.setOut(m, v)
		}
		w("%s of memory %d: %s", strings.ToLower(s), m.ID, trunc(k.show(v), 60))
	case "SHIFT":
		// a truth shift: a new row that holds what was true then and what is true now
		v, m := k.any(r), k.m(r)
		sh := k.newMem(k.nm("SHIFT"), m.Home, r.Made, k.now)
		was := gv(k.nm("NONE"))
		if m.HasOut {
			was = m.Out
		}
		k.setBody(sh, []Val{nv(float64(m.ID)), was, v})
		k.setOut(m, v)
		if m.HasSig {
			k.setSig(m, m.Sig, k.shapeOf(&Run{D0: parseStr(m.Sig)}))
		}
		w("truth shift on memory %d: %s -> %s (memory %d)", m.ID, k.show(was), k.show(v), sh.ID)
		k.push(r, nv(float64(sh.ID)))
	case "TODO":
		// one of the sixth's lists: one row per subject gate and kind
		kind, v := k.g(r), k.any(r)
		home := k.nm("ZERO")
		if v.K == 'g' {
			home = v.G
			if len(k.homes[[2]int64{home, kind}]) > 0 {
				return
			}
		}
		m := k.newMem(kind, home, r.Made, k.now)
		m.Seen = 0
		k.saveMem(m)
		k.kinds[kind] = append([]int64{m.ID}, del(k.kinds[kind], m.ID)...) // never touched: touched longest ago
		k.setBody(m, []Val{v})
		w("%s %s (memory %d)", k.show(gv(kind)), trunc(k.show(v), 60), m.ID)
	case "MADE":
		r.Made = k.popG(r)
		if r.Made == k.nm("TOLD") && k.meta["told_ended"] == "" {
			r.Made = k.nm("SPAWNED")
		}
	case "WANT":
		r.Want, r.HasWant = k.pop(r, 0)
	case "TRUST":
		o, t, sg := k.popG(r), k.popG(r), k.popG(r)
		c := k.trust[[2]int64{sg, t}]
		if o == k.nm("YES") {
			c[0]++
		} else {
			c[1]++
		}
		k.trust[[2]int64{sg, t}] = c
		k.q("INSERT OR REPLACE INTO trust VALUES(?,?,?,?)", sg, t, c[0], c[1])
	default:
		k.act(r, "fault", "WRITE with no selector")
		need(false)
	}
}

// writeMem writes this run's memory row: its signature, shape, trail and outcome,
// on the timeline. Whether it is the same run again, a truth shift, or new is the
// end-of-run process's to judge, not the store's.
func (k *K) writeMem(r *Run) {
	out, ok := k.pop(r, 0)
	if !ok {
		out = gv(k.nm("NONE"))
	}
	m := k.M[r.Mem]
	if m == nil {
		m = k.newMem(k.nm("RUN"), r.home(), r.Made, k.now)
		r.Mem = m.ID
	}
	k.setSig(m, k.sigOf(r), k.shapeOf(r))
	k.setBody(m, gl(r.Trail).L)
	k.setOut(m, out)
	k.act(r, "memory", fmt.Sprintf("%d: %s -> %s", m.ID, k.show(gl(r.D0)), k.show(out)))
	k.push(r, nv(float64(m.ID)))
	k.lastMem(r, m.ID)
}

// lastMem: what the brain last did for this person (WHY) is the memory of the run
// tree that answered them: set by the root run's own memory, or by any run of the
// tree that says something to them (its receipt memory); a branch's own memory
// (a refused source, a read-up) is not what it did for them
func (k *K) lastMem(r *Run, id int64) {
	if c := r.root().Conn; c != 0 && r.Parent == nil {
		k.port.setWhy(c, id)
	}
}

func (k *K) spawn(r *Run) {
	p, ok := k.pop(r, 'p')
	if !ok { // no point given: where a newborn goes is the told born's to say (it SPAWNs there)
		k.calls(r, "born")
		return
	}
	birth := k.newMem(k.nm("BIRTH"), 0, r.Made, k.now)
	g := k.newGate(p.P, r.Made, birth.ID)
	birth.Home = g
	k.q("UPDATE mem SET home=? WHERE id=?", g, birth.ID)
	k.homes[[2]int64{g, birth.Kind}] = append(k.homes[[2]int64{g, birth.Kind}], birth.ID)
	// a receipt to the memory of the run that spawned it, not a copy of its trail
	k.setBody(birth, []Val{nv(float64(k.rcpt(r))), gv(r.At), gv(r.From), itemVal(r.Ev[2]), tv(r.Ctx[0]), tv(r.Ctx[1])})
	def := k.newMem(k.nm("DEF"), g, r.Made, k.now)
	k.setBody(def, []Val{pv(p.P)})
	k.act(r, "spawn", fmt.Sprintf("gate %d at %s (birth %d, definition %d)", g, k.show(p), birth.ID, def.ID))
	k.push(r, gv(g))
}

func (k *K) delete(r *Run) {
	s := k.sel(r)
	d := func(f string, a ...any) { k.act(r, "delete", fmt.Sprintf(f, a...)) }
	switch s {
	case "REL":
		x := k.rel(r)
		need(k.guard(r, x.A, s))
		k.delRel(x.A, x.Type, x.B)
		d("rel %s %s %s", k.show(gv(x.A)), k.show(gv(x.Type)), k.show(gv(x.B)))
	case "SHARD":
		h, a, g := k.popG(r), k.popG(r), k.g(r)
		need(k.G[g].Sh[SK{a, h}] != nil && k.guard(r, g, s))
		delete(k.G[g].Sh, SK{a, h})
		k.q("DELETE FROM shard WHERE g=? AND arr=? AND head=?", g, a, h)
		k.q("DELETE FROM trig WHERE g=? AND arr=? AND head=?", g, a, h)
		d("shard %s from %s on %s", k.show(gv(g)), k.show(gv(a)), k.show(gv(h)))
	case "USUAL":
		o, g := k.popG(r), k.g(r)
		need(k.guard(r, g, s))
		i := slices.IndexFunc(k.G[g].Usual, func(t Trig) bool { return t.Out == o })
		need(i >= 0)
		k.G[g].Usual = slices.Delete(k.G[g].Usual, i, i+1)
		k.q("DELETE FROM usual WHERE g=? AND out=?", g, o)
		d("trigger %s on %s", k.show(gv(o)), k.show(gv(g)))
	case "LABEL":
		// a label taken back (a person's "no" to a name): g, and the text, in either order
		g := k.g(r)
		t, ok := k.pop(r, 't')
		need(ok && k.guard(r, g, s) && k.delLabel(strings.ToLower(t.T), g))
		d("label %q of %s", t.T, k.show(gv(g)))
	case "LAST":
		k.top(r)
		r.Pad = r.Pad[:len(r.Pad)-1]
	case "MEM":
		m := k.m(r)
		need(!k.G[m.Home].Core)
		k.delMem(m.ID)
		d("memory %d", m.ID)
	default:
		need(false)
	}
}

func (k *K) move(r *Run) {
	switch s := k.sel(r); s {
	case "POINT":
		p, ok := k.pop(r, 'p')
		g := k.g(r)
		need(ok && k.guard(r, g, "MOVE") && !math.IsNaN(p.P[0]+p.P[1]+p.P[2]))
		if g == 0 {
			k.act(r, "refused", "MOVE of zero: it is the origin")
			need(false)
		}
		k.act(r, "move", fmt.Sprintf("%s %s -> %s", k.show(gv(g)), k.show(pv(k.G[g].P)), k.show(p)))
		k.movePoint(g, p.P)
	case "TIER", "FID":
		t, m := k.g(r), k.m(r)
		if s == "FID" {
			m.Fid = t
		} else {
			if m.Tier == k.nm("ACTIVE") {
				k.active--
			}
			if m.Tier = t; t == k.nm("ACTIVE") {
				k.active++
			}
		}
		if t == k.nm("LONG") {
			k.drop = append(k.drop, m) // the body stays on disk; RAM lets it go at commit
		}
		k.saveMem(m)
		k.act(r, "move", fmt.Sprintf("memory %d to %s", m.ID, k.show(gv(t))))
	default:
		need(false)
	}
}

// find reaches by index only: never a scan.
func (k *K) find(r *Run) {
	s := k.sel(r)
	switch s {
	case "SIG":
		id, ok := k.sigs[k.sigOf(r)]
		k.pushOr(r, nv(float64(id)), ok)
	case "LABEL", "LABELS":
		// several gates for one label: which one is meant is the told which-label's pick
		t, ok := k.pop(r, 't')
		need(ok)
		if gs := k.labelGates(t.T); s == "LABEL" {
			k.hand(r, "which-label", gs)
		} else {
			need(len(gs) > 0)
			k.push(r, gl(gs))
		}
	case "POINT", "NEAR":
		// NEAR: the gates in the point's cell and its neighbours, in index order. POINT: those
		// closer than a cell (as COMPARE); several go to which-gate, with the point
		p, ok := k.pop(r, 'p')
		need(ok)
		var gs []int64
		for _, g := range k.near(p.P) {
			if s == "NEAR" || dist(k.G[g].P, p.P) < k.cell {
				gs = append(gs, g)
			}
		}
		if s == "POINT" {
			k.hand(r, "which-gate", gs, p)
			return
		}
		need(len(gs) > 0)
		k.push(r, gl(gs))
	case "VALUES":
		// every gate holding the value; which one means the number is the brain's to judge (number-gate)
		gs := k.vals[k.n(r)]
		need(len(gs) > 0)
		k.push(r, gl(gs))
	case "TIME", "TIME-END":
		// a page of the timeline (t0 > t1 asks for the newest first); TIME-END gives the
		// time of the last entry that page holds, where the next page can start
		t1, t0 := k.n(r), k.n(r)
		v, last := k.timePage(t1, t0)
		if s == "TIME-END" {
			k.pushOr(r, nv(float64(last)), len(v.L) > 0)
		} else {
			k.pushOr(r, v, len(v.L) > 0)
		}
	case "SHAPE":
		sh, sig, most := k.shapeOf(r), k.sigOf(r), int(k.value("SHAPE-PAGE"))
		v := Val{K: 'l'}
		for _, id := range k.shapes[sh] {
			if m := k.M[id]; m != nil && m.Sig != sig && len(v.L) < most {
				v.L = append(v.L, nv(float64(id)))
			}
		}
		k.pushOr(r, v, len(v.L) > 0 && len(sh) > 0)
	case "KIND", "KINDAT":
		// a page (PAGE, a setting) of a list, least recently touched first; which to try is the sixth's choice
		at := 0
		if s == "KINDAT" {
			at = int(k.n(r))
		}
		ids := k.kinds[k.popG(r)]
		need(at >= 0 && at < len(ids))
		v := Val{K: 'l'}
		for _, id := range ids[at:min(len(ids), at+int(k.value("PAGE")))] {
			v.L = append(v.L, nv(float64(id)))
		}
		k.push(r, v)
	case "HOME":
		kind, g := k.popG(r), k.popG(r)
		ids := k.homes[[2]int64{g, kind}]
		need(len(ids) > 0)
		k.push(r, nv(float64(ids[len(ids)-1])))
	default:
		k.act(r, "fault", "FIND with no selector")
		need(false)
	}
}

// checked: SAY, CALL and WRITE PROC go through only after the core-value check.
func (k *K) checked(r *Run, what string) bool {
	if !r.Checked {
		k.act(r, "refused", what+" without the core-value check")
		return false
	}
	r.Checked = false
	return true
}

// say: the decoder reads labels off gates. A gate with no label is not said;
// it goes back on the pad and NONE goes to the head, so the run can ask its name.
func (k *K) say(r *Run) {
	need(k.checked(r, "SAY"))
	if c := r.root().Conn; c != 0 {
		defer k.port.setWhy(c, k.rcpt(r))
	}
	v := k.any(r)
	vs := []Val{v}
	if v.K == 'l' {
		vs = v.L
	}
	var words []string
	for _, x := range vs {
		switch x.K {
		case 'g':
			l, ok := k.labelOf(x.G)
			if !ok {
				k.push(r, x)
				need(false)
			}
			words = append(words, l)
		case 'n':
			words = append(words, fmt.Sprint(x.N))
		case 't':
			words = append(words, x.T)
		default:
			words = append(words, k.show(x))
		}
	}
	out := strings.Join(words, " ")
	k.port.say(r.root().Conn, out)
	k.act(r, "say", out)
}

// call: anything else a computer can do, through a source's template. The run
// parks until the answer comes back as text.
func (k *K) call(r *Run) {
	need(k.checked(r, "CALL"))
	arg, ok := k.pop(r, 't')
	if !ok { // a number query goes as its digits (a line number, a value to look up)
		n, isN := k.popN(r)
		need(isN)
		arg = tv(fmt.Sprint(n))
	}
	cmd := arg.T
	if g := k.srcGate(r); g >= 0 {
		if s, ok := k.src[g]; ok {
			// a source whose gate holds a value has that many calls a day, counted per key file
			// its template reads (sources sharing a key share the count; else per source), kept
			// in brain.db so a restart doesn't reset it
			key := fmt.Sprint(g)
			if m := keyFile.FindString(s.How); m != "" {
				key = m
			}
			day := fmt.Sprint("calls ", key, " @", k.now/86400)
			if gt := k.G[g]; gt.HasVal {
				n, _ := strconv.Atoi(k.meta[day])
				if float64(n) >= gt.Val {
					k.act(r, "refused", fmt.Sprintf("CALL past %s's daily quota of %g (%s)", k.show(gv(g)), gt.Val, key))
					k.popG(r)
					need(false)
				}
				k.setMeta(day, fmt.Sprint(n+1))
			}
			cmd = strings.ReplaceAll(s.How, "%s", shq(arg.T))
			k.popG(r)
		}
	}
	r.Parked = true
	k.act(r, "call", trunc(cmd, 120))
	k.port.call(r, cmd, k.value("CALL-WAIT"), int(k.value("CALL-CAP")))
}

var keyFile = regexp.MustCompile(`[^\s'"$()]+\.key\b`)

func b2i(b bool) int {
	if b {
		return 1
	}
	return 0
}

func shq(s string) string { return "'" + strings.ReplaceAll(s, "'", `'\''`) + "'" }

// timePage: at most TIME-PAGE timeline entries between t0 and t1 (newest first when
// t0 > t1). A page never ends inside a second (the timeline's key is the second): a
// full page takes the rest of its last second, so the next page can start after it.
func (k *K) timePage(t1, t0 float64) (Val, int64) {
	lo, hi, step := t0, t1, 1
	i := sort.Search(len(k.tl), func(i int) bool { return float64(k.tl[i].T) >= lo })
	if t0 > t1 {
		lo, hi, step = t1, t0, -1
		i = sort.Search(len(k.tl), func(i int) bool { return float64(k.tl[i].T) > hi }) - 1
	}
	v, last := Val{K: 'l'}, int64(-1)
	for ; i >= 0 && i < len(k.tl) && float64(k.tl[i].T) >= lo && float64(k.tl[i].T) <= hi && (len(v.L) < int(k.value("TIME-PAGE")) || k.tl[i].T == last); i += step {
		if k.M[k.tl[i].Mem] != nil {
			v.L, last = append(v.L, nv(float64(k.tl[i].Mem))), k.tl[i].T
		}
	}
	return v, last
}
