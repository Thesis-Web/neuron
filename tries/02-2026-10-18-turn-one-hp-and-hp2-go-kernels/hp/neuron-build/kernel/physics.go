package main

// physics.go: what the silicon does when a run passes a physics gate (blueprint 4.3).
// Inputs come off the run's scratch pad; results go back on it. A test also puts
// its outcome gate at the head of the remainder, so the next shard picks the branch.

import (
	"encoding/json"
	"math"
	"strconv"
	"strings"
)

// name gives the kernel-level name a gate stands for: its binding suffix, else its label, else #n.
func (b *Brain) name(id int) string {
	g := b.s.gate(id)
	if g == nil {
		return "#" + strconv.Itoa(id)
	}
	if i := strings.IndexByte(g.Bind, '.'); i > 0 && g.Bind != "value" && g.Bind != "proc" && g.Bind != "rel" {
		return g.Bind[i+1:]
	}
	return b.decode(gv(id), "en")
}

func (b *Brain) text(v Val) string {
	if v.K == 't' {
		return v.S
	}
	return b.decode(v, "en")
}

// keyOf is the row key an item stands for: a gate by its number, a text as itself, a number as itself.
func (b *Brain) keyOf(v Val) string {
	switch v.K {
	case 'g':
		return strconv.Itoa(v.G)
	case 't':
		return v.S
	case 'n':
		return fnum(v.N)
	}
	return v.String()
}

func (b *Brain) core(id int) bool {
	g := b.s.gate(id)
	return g != nil && g.Made == "core"
}

func (b *Brain) coreMem(id int) bool {
	m := b.s.mems[id]
	return m != nil && m.Kind == "core"
}

func (b *Brain) refuse(r *Run, what string) {
	b.act("REFUSE run=%d %s", r.Id, what)
	b.outcome(r, "no")
}

// outcomesOf names the outcomes a word can put at the head of the remainder: a test's branches. Not a test: none.
func (b *Brain) outcomesOf(id int) []int {
	g := b.s.gate(id)
	if g == nil {
		return nil
	}
	var names []string
	switch {
	case g.Bind == "COMPARE":
		names = []string{"same", "more", "less"}
	case g.Bind == "rel" || g.Bind == "HEAR" || strings.HasPrefix(g.Bind, "FIND."):
		names = []string{"found", "none"}
	case strings.HasPrefix(g.Bind, "READ."):
		switch g.Bind[5:] {
		case "bind", "body", "def", "head", "input", "item", "label", "mem", "memkind", "mytrig", "parent", "pick", "rel", "relin", "rels", "row", "shard", "source", "strength", "trailof", "trig", "trust", "use", "value", "want", "why", "word":
			names = []string{"found", "none"}
		}
	}
	var out []int
	for _, n := range names {
		out = append(out, b.s.byBind["outcome."+n])
	}
	return out
}

func (b *Brain) found(r *Run, ok bool) {
	if ok {
		b.outcome(r, "found")
	} else {
		b.outcome(r, "none")
	}
}

func (b *Brain) physics(r *Run, g *Gate) {
	s := b.s
	t := b.now()
	if strings.HasPrefix(g.Bind, "WRITE.") || strings.HasPrefix(g.Bind, "DELETE.") || g.Bind == "SPAWN" || g.Bind == "MOVE" {
		r.Wrote++
	}
	switch g.Bind {
	// ---- run
	case "GO":
		from, at := r.popG(), r.popG()
		if at >= 0 {
			r.At, r.From = at, from
		}
		// the miss process came back: if it laid the way, the count resets; if not, a storm is building
		if len(r.Rest) > 0 && (r.Rest[0].K == 'g' || r.Rest[0].K == 'o') {
			if ag := s.gate(r.At); ag != nil && (ag.Shards[[2]int{r.From, r.Rest[0].G}] != nil || ag.Shards[[2]int{-1, r.Rest[0].G}] != nil) {
				r.MissDepth = 0
			}
		}
	case "SPLIT":
		subj, to := r.pop(), r.popG()
		if to >= 0 {
			b.split(r, to, subj, nil, r.Worth*b.val("VALUE.splitworth", 0.8))
		}
	case "LAND":
		v := r.pop()
		r.Landed = true
		if r.Parent != nil && !r.Parent.Done {
			r.Parent.Land = append(r.Parent.Land, v)
			b.act("LAND run=%d -> run=%d %s", r.Id, r.Parent.Id, v)
		} else {
			r.push(v)
		}
	case "WAIT":
		r.WaitBeat = b.beatNo
	case "END":
		b.end(r)
	case "DUP":
		v := r.pop()
		r.push(v)
		r.push(v)
	case "DROP":
		r.pop()
	case "SWAP":
		a, c := r.pop(), r.pop()
		r.push(a)
		r.push(c)
	case "OVER":
		a, c := r.pop(), r.pop()
		r.push(c)
		r.push(a)
		r.push(c)
	case "ROT": // a b c -- b c a
		c, bb, a := r.pop(), r.pop(), r.pop()
		r.push(bb)
		r.push(c)
		r.push(a)
	// ---- read: the run itself
	case "READ.next":
		if len(r.Rest) > 0 {
			v := r.Rest[0]
			if v.K == 'o' {
				v.K = 'g'
			}
			r.push(v)
			r.Rest = r.Rest[1:]
		}
	case "READ.word": // -- x -> found/none : the next word of this run's own input (a reading run)
		if len(r.Input) > 0 {
			r.push(r.Input[0])
			r.Input = r.Input[1:]
			b.found(r, true)
		} else {
			b.found(r, false)
		}
	case "READ.head":
		if len(r.Rest) > 0 {
			v := r.Rest[0]
			if v.K == 'o' {
				v.K = 'g'
			}
			r.push(v)
		}
		b.found(r, len(r.Rest) > 0)
	case "READ.mark":
		r.push(Val{K: 'm'})
	case "READ.tomark": // x.. m -- l : the items above the mark, as a list (the mark goes too)
		var l []Val
		for len(r.Pad) > 0 {
			v := r.pop()
			if v.K == 'm' {
				break
			}
			l = append([]Val{v}, l...)
		}
		r.push(lst(l))
	case "READ.list":
		n := int(r.popN())
		if n > len(r.Pad) {
			n = len(r.Pad)
		}
		l := append([]Val{}, r.Pad[len(r.Pad)-n:]...)
		r.Pad = r.Pad[:len(r.Pad)-n]
		r.push(lst(l))
	case "READ.count":
		v := r.pop()
		if v.K == 'l' {
			r.push(num(float64(len(v.L))))
		} else if v.K == 't' {
			r.push(num(float64(len(strings.Fields(v.S)))))
		} else {
			r.push(num(1))
		}
	case "READ.item":
		i, l := int(r.popN()), r.pop()
		if l.K == 'l' && i >= 0 && i < len(l.L) {
			r.push(l.L[i])
			b.found(r, true)
		} else {
			b.found(r, false)
		}
	case "READ.pick": // l i -- l x : like read-item, keeping the list
		i, l := int(r.popN()), r.pop()
		r.push(l)
		if l.K == 'l' && i >= 0 && i < len(l.L) {
			r.push(l.L[i])
			b.found(r, true)
		} else {
			b.found(r, false)
		}
	case "READ.pad":
		r.push(num(float64(len(r.Pad))))
	case "READ.at":
		r.push(gv(r.At))
	case "READ.from":
		r.push(gv(r.From))
	case "READ.self":
		r.push(num(float64(r.Mem)))
	case "READ.parent":
		if r.Parent != nil {
			r.push(num(float64(r.Parent.Mem)))
		}
		b.found(r, r.Parent != nil)
	case "READ.who":
		r.push(tv(r.Who))
	case "READ.what":
		r.push(tv(r.What))
	case "READ.when":
		r.push(num(float64(r.When)))
	case "READ.where":
		r.push(tv(r.Where))
	case "READ.why":
		r.push(num(float64(r.Why)))
		b.found(r, r.Why > 0)
	case "READ.how":
		r.push(tv(r.How))
	case "READ.want":
		if r.Want.K != 0 {
			r.push(r.Want)
		}
		b.found(r, r.Want.K != 0)
	case "READ.depth":
		r.push(num(float64(r.Depth)))
	case "READ.steps": // the steps of the run being reasoned about: the root of this question
		root := r
		for root.Parent != nil {
			root = root.Parent
		}
		r.push(num(float64(root.Steps)))
	case "READ.worth":
		r.push(num(r.Worth))
	case "READ.sig":
		if r.Parent == nil {
			r.Sig = sigOf(b.encode(r.What, "en"))
		}
		r.push(tv(r.Sig))
	case "READ.words": // -- l : the run's own input as the encoder reads it now (a word that got its gate since is its gate)
		r.push(lst(b.encode(r.What, "en")))
	case "READ.shape":
		r.push(tv(r.Shape))
	case "READ.trail":
		var l []Val
		for _, st := range r.Trail {
			l = append(l, gv(st.Gate))
		}
		r.push(lst(l))
	case "READ.mytrig":
		if r.Trig != nil {
			r.push(gv(r.Trig.Gate))
			r.push(gv(r.Trig.To))
		}
		b.found(r, r.Trig != nil)
	// ---- read: rows reachable from a gate
	case "READ.point":
		if g := s.gate(r.popG()); g != nil {
			r.push(vec(g.P))
		}
	case "READ.value":
		g := s.gate(r.popG())
		if g != nil && g.Bind == "value" {
			r.push(num(g.Val))
		}
		b.found(r, g != nil && g.Bind == "value")
	case "READ.bind":
		g := s.gate(r.popG())
		if g == nil || g.Bind == "" {
			b.found(r, false)
			break
		}
		r.push(tv(g.Bind))
		switch g.Bind {
		case "value":
			r.push(num(g.Val))
		case "proc", "rel":
			var l []Val
			for _, x := range g.Str {
				l = append(l, gv(x))
			}
			r.push(lst(l))
		default:
			r.push(tv(g.Bind))
		}
		b.found(r, true)
	case "READ.label":
		ls := s.glabel[r.popG()]
		if len(ls) > 0 {
			r.push(tv(ls[0]))
		}
		b.found(r, len(ls) > 0)
	case "READ.made":
		if g := s.gate(r.popG()); g != nil {
			r.push(tv(g.Made))
			r.push(num(float64(g.By)))
		}
	case "READ.rel", "READ.relin":
		typ, from := r.popG(), r.popG()
		fg := s.gate(from)
		var l []Val
		if fg != nil {
			rels := fg.Rels
			if g.Bind == "READ.relin" {
				rels = fg.RelsIn
			}
			for _, rl := range rels {
				if rl.Type == typ {
					if rl.From == from {
						l = append(l, gv(rl.To))
					} else {
						l = append(l, gv(rl.From))
					}
				}
			}
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "READ.rels":
		g := s.gate(r.popG())
		var l []Val
		if g != nil {
			for _, rl := range g.Rels {
				l = append(l, lst([]Val{gv(rl.Type), gv(rl.To), num(rl.Strength), tv(rl.State)}))
			}
			for _, rl := range g.RelsIn {
				l = append(l, lst([]Val{gv(rl.Type), gv(rl.From), num(-rl.Strength), tv(rl.State)}))
			}
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "READ.strength":
		to, typ, from := r.popG(), r.popG(), r.popG()
		rl := s.rel(from, typ, to)
		if rl != nil {
			r.push(num(rl.Strength))
			r.push(tv(rl.State))
		}
		b.found(r, rl != nil)
	case "READ.shard":
		head, arr, gate := r.popG(), r.popG(), r.popG()
		var sh *Shard
		if g := s.gate(gate); g != nil {
			sh = g.Shards[[2]int{arr, head}]
		}
		if sh != nil {
			r.push(gv(sh.Next))
			r.push(num(float64(sh.Seen)))
			r.push(num(float64(sh.Right)))
			r.push(num(float64(sh.Wrong)))
		}
		b.found(r, sh != nil)
	case "READ.trig":
		g := s.gate(r.popG())
		var l []Val
		if g != nil {
			for _, tr := range g.Trigs {
				l = append(l, lst([]Val{gv(tr.To), num(tr.Worth)}))
			}
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "READ.def":
		sec, gate := int(r.popN()), r.popG()
		l := b.defSection(gate, sec)
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "READ.mem":
		m := s.mems[int(r.popN())]
		if m != nil && !m.dead {
			r.push(tv(m.Outcome))
			r.push(num(float64(m.Seen)))
			r.push(num(float64(m.Right)))
			r.push(num(float64(m.Wrong)))
			r.push(num(float64(m.Last)))
		}
		b.found(r, m != nil && !m.dead)
	case "READ.input": // a memory's own input: its gates as a list, and its shape
		m := s.mems[int(r.popN())]
		if m != nil && !m.dead {
			var l []Val
			for _, f := range strings.Split(m.Sig, ",") {
				if n, err := strconv.Atoi(f); err == nil {
					l = append(l, gv(n))
				} else if len(f) > 1 {
					l = append(l, tv(strings.Trim(f, "\"")))
				}
			}
			r.push(lst(l))
			r.push(tv(m.Shape))
		}
		b.found(r, m != nil && !m.dead)
	case "READ.memkind": // n -- kind tier -> found/none
		m := s.mems[int(r.popN())]
		if m != nil && !m.dead {
			r.push(tv(m.Kind))
			r.push(tv(m.Tier))
		}
		b.found(r, m != nil && !m.dead)
	case "READ.trailof": // n -- l -> found/none : a memory's trail as a list of [gate arrival head]
		m := s.mems[int(r.popN())]
		var trail []Step
		if m != nil {
			json.Unmarshal([]byte(s.memBody(m)), &trail)
		}
		var l []Val
		for _, st := range trail {
			l = append(l, lst([]Val{gv(st.Gate), gv(st.Arr), gv(st.Head)}))
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "READ.body":
		m := s.mems[int(r.popN())]
		if m != nil {
			r.push(tv(s.memBody(m)))
			r.push(tv(m.Fid))
		}
		b.found(r, m != nil)
	case "READ.row":
		m := s.mems[int(r.popN())]
		if m != nil && !m.dead {
			r.push(tv(m.Sig))
			r.push(gv(m.Home))
			r.push(tv(s.memBody(m)))
			r.push(tv(m.Outcome))
		}
		b.found(r, m != nil && !m.dead)
	case "READ.use":
		gate := r.popG()
		var l []Val
		for _, id := range s.recs["use\x00"+strconv.Itoa(gate)] {
			l = append(l, num(float64(id)))
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "READ.size":
		r.push(num(float64(len(s.gates))))
		r.push(num(float64(len(s.mems))))
		r.push(num(float64(s.active)))
	case "READ.source":
		src := s.sources[r.popG()]
		if src != nil {
			r.push(num(float64(src.Grounded)))
		}
		b.found(r, src != nil)
	case "READ.trust":
		topic, src := r.popG(), r.popG()
		tr := s.trust[[2]int{src, topic}]
		if tr != nil {
			r.push(num(float64(tr.Right)))
			r.push(num(float64(tr.Wrong)))
			r.push(num(tr.Weight))
		}
		b.found(r, tr != nil)
	// ---- write
	case "WRITE.rest":
		v := r.pop()
		if v.K == 'l' {
			r.Rest = append(append([]Val{}, v.L...), r.Rest...)
		} else if v.K == 'g' || v.K == 't' { // a raw word hops too: it misses, and the miss way spawns it
			r.Rest = append([]Val{v}, r.Rest...)
		}
	case "WRITE.want":
		r.Want = r.pop()
	case "WRITE.shard":
		next, head, arr, gate := r.popG(), r.popG(), r.popG(), r.popG()
		g := s.gate(gate)
		if g == nil || next < 0 || head < 0 || b.core(gate) {
			b.refuse(r, "WRITE.shard")
			break
		}
		sh := g.Shards[[2]int{arr, head}]
		if sh == nil {
			sh = &Shard{Gate: gate, Arr: arr, Head: head, Made: "spawned", By: r.Mem}
			g.Shards[[2]int{arr, head}] = sh
		}
		sh.Next, sh.Last = next, t
		s.dShard[sh] = true
	case "WRITE.rel":
		state, strength, to, typ, from := r.popG(), r.popN(), r.popG(), r.popG(), r.popG()
		if s.gate(from) == nil || s.gate(to) == nil || s.gate(typ) == nil || b.core(from) || b.core(to) {
			b.refuse(r, "WRITE.rel")
			break
		}
		rl := s.rel(from, typ, to)
		if rl == nil {
			rl = &Rel{From: from, Type: typ, To: to, Made: "derived", By: r.Mem}
			s.gates[from].Rels = append(s.gates[from].Rels, rl)
			s.gates[to].RelsIn = append(s.gates[to].RelsIn, rl)
		}
		rl.Strength, rl.State, rl.When = strength, b.name(state), t
		s.dRel[rl] = true
		b.place(from)
		b.place(to)
		b.act("REL run=%d %d %s %d strength=%.2f state=%s", r.Id, from, b.name(typ), to, strength, rl.State)
	case "WRITE.strength":
		delta, to, typ, from := r.popN(), r.popG(), r.popG(), r.popG()
		rl := s.rel(from, typ, to)
		if rl == nil || b.core(from) || b.core(to) {
			b.refuse(r, "WRITE.strength")
			break
		}
		rl.Strength += delta
		rl.When = t
		s.dRel[rl] = true
		b.place(from)
		b.place(to)
	case "WRITE.run": // home m out -- n : stores this run's trail and outcome in memory m (none or 0: a new row). Nothing is decided here.
		out, mv, home := r.pop(), r.pop(), r.popG()
		if home < 0 {
			home = r.At
		}
		if r.Parent == nil {
			r.Sig = sigOf(b.encode(r.What, "en")) // the words may have gates now that they lacked when encoded
		}
		var m *Mem
		if mv.K == 'n' && int(mv.N) > 0 {
			m = s.mems[int(mv.N)]
		}
		if m == nil || m.dead || m.Kind != "run" {
			if old := s.mems[r.Mem]; old != nil && !old.dead { // the id reserved at start is taken: a fresh one
				r.Mem = s.memNext
				s.memNext++
			}
			m = s.newMem("run", home, r.Sig, "derived", r.Mem, t)
			m.Id = r.Mem
			s.mems[r.Mem] = m
			s.memSig["run\x00"+r.Sig] = m.Id
		} else {
			r.Mem = m.Id
			m.Last, m.Seen = t, m.Seen+1
		}
		if r.Parent == nil { // only a root run's shape is its own; question runs borrow it
			s.setShape(m, r.Shape)
		}
		trail, _ := json.Marshal(r.Trail)
		m.Body, m.Outcome = string(trail), b.text(out)
		s.dMem[m] = true
		s.addTL(t, m.Id)
		for _, st := range r.Trail { // the shards the run passed carry their rough counts to disk with it
			if g := s.gate(st.Gate); g != nil {
				if sh := g.Shards[[2]int{st.Arr, st.Head}]; sh != nil {
					s.dShard[sh] = true
				} else if sh := g.Shards[[2]int{-1, st.Head}]; sh != nil {
					s.dShard[sh] = true
				}
			}
		}
		if r.Parent == nil { // a root run's input gates get a use receipt to its memory; a question run's use is its parent's
			for _, v := range b.encode(r.What, "en") {
				if v.K == 'g' {
					s.receipt("use", strconv.Itoa(v.G), m.Id, t)
				}
			}
		}
		if r.Conn != nil && r.Parent == nil {
			r.Conn.lastMem = m.Id
		}
		r.push(num(float64(m.Id)))
		b.act("MEM run=%d mem=%d seen=%d outcome=%s", r.Id, m.Id, m.Seen, m.Outcome)
	case "WRITE.row":
		body, out, key, home, kind := r.pop(), r.pop(), r.pop(), r.popG(), r.popG()
		k := b.name(kind)
		if k == "core" || k == "run" || k == "born" || k == "told" {
			b.refuse(r, "WRITE.row "+k)
			break
		}
		ks := b.keyOf(key)
		m := s.mems[s.memKey[k+"\x00"+ks]]
		if m == nil || m.dead {
			m = s.newMem(k, home, ks, "derived", r.Mem, t)
		} else {
			m.Last, m.Seen = t, m.Seen+1
		}
		m.Body, m.Outcome = b.text(body), b.text(out)
		s.dMem[m] = true
		s.addTL(t, m.Id)
		r.push(num(float64(m.Id)))
	case "WRITE.mark":
		out, id := r.popG(), int(r.popN())
		m := s.mems[id]
		if m == nil || b.coreMem(id) {
			b.refuse(r, "WRITE.mark")
			break
		}
		right := b.name(out) == "yes"
		if right {
			m.Right++
		} else {
			m.Wrong++
		}
		s.dMem[m] = true
		var trail []Step
		json.Unmarshal([]byte(s.memBody(m)), &trail)
		for _, st := range trail {
			if g := s.gate(st.Gate); g != nil {
				if sh := g.Shards[[2]int{st.Arr, st.Head}]; sh != nil {
					if right {
						sh.Right++
					} else {
						sh.Wrong++
					}
					s.dShard[sh] = true
				}
			}
		}
		b.act("MARK run=%d mem=%d %s", r.Id, id, b.name(out))
	case "WRITE.outcome":
		out, id := r.pop(), int(r.popN())
		if m := s.mems[id]; m != nil && !b.coreMem(id) {
			m.Outcome = b.text(out)
			s.dMem[m] = true
		}
	case "WRITE.body":
		fid, body, id := r.popG(), r.pop(), int(r.popN())
		if m := s.mems[id]; m != nil && !b.coreMem(id) {
			m.Body, m.Fid = b.text(body), b.name(fid)
			s.dMem[m] = true
		} else {
			b.refuse(r, "WRITE.body")
		}
	case "WRITE.def":
		body, sec, gate := r.pop(), int(r.popN()), r.popG()
		if s.gate(gate) == nil || b.core(gate) || sec < 1 {
			b.refuse(r, "WRITE.def")
			break
		}
		d := &Def{Gate: gate, Sec: sec, Line: len(s.defs[gate][sec]) + 1, Body: b.text(body), Made: "derived", By: r.Mem}
		s.putDef(d)
		s.dDef[d] = true
	case "WRITE.label":
		gate, text := r.popG(), r.pop()
		if s.gate(gate) == nil || text.K != 't' || b.core(gate) {
			b.refuse(r, "WRITE.label")
			break
		}
		if old, ok := s.label(text.S, "en"); ok && old != gate { // one text, one gate: another run got there first
			b.refuse(r, "WRITE.label taken")
			break
		}
		s.setLabel(text.S, "en", gate, "derived", r.Mem)
		b.act("LABEL run=%d %q -> %d", r.Id, text.S, gate)
	case "WRITE.proc":
		l, gate := r.pop(), r.popG()
		g := s.gate(gate)
		if g == nil || l.K != 'l' || b.core(gate) || (g.Bind != "" && g.Bind != "proc" && !strings.HasPrefix(g.Bind, "PROC.")) {
			b.refuse(r, "WRITE.proc")
			break
		}
		var p []string
		for _, x := range l.L {
			if x.K == 'g' {
				p = append(p, strconv.Itoa(x.G))
			}
		}
		if len(p) == 0 && !strings.HasPrefix(g.Bind, "PROC.") { // an empty list: the brain changes its mind back; the gate is plain again
			for k, sh := range g.Shards {
				if sh.Made != "told" {
					sh.Next = -1
					s.dShard[sh] = true
					delete(g.Shards, k)
				}
			}
			s.rebind(g, "", "")
			g.Str, g.Made, g.By = nil, "derived", r.Mem
			b.act("PROC run=%d gate=%d string=", r.Id, gate)
			break
		}
		bind := "proc"
		if strings.HasPrefix(g.Bind, "PROC.") { // a told way (miss, end-of-run, the sixth) keeps its name when the brain rewrites it
			bind = g.Bind
			for k, sh := range g.Shards { // its old told hops go; the branches other gates hold are left for the brain
				sh.Next = -1
				s.dShard[sh] = true
				delete(g.Shards, k)
			}
		}
		s.rebind(g, bind, strings.Join(p, " "))
		g.Made, g.By = "derived", r.Mem // the string is the brain's now, whoever laid the gate
		b.layShards(g, "derived", r.Mem, nil)
		b.act("PROC run=%d gate=%d string=%s", r.Id, gate, g.BVal)
	case "WRITE.value":
		n, gate := r.popN(), r.popG()
		g := s.gate(gate)
		if g == nil || b.core(gate) || (g.Bind != "" && g.Bind != "value" && !strings.HasPrefix(g.Bind, "VALUE.")) {
			b.refuse(r, "WRITE.value")
			break
		}
		if g.Bind == "" {
			s.rebind(g, "value", fnum(n))
		} else {
			s.rebind(g, g.Bind, fnum(n))
		}
	case "WRITE.trig":
		worth, to, gate := r.popN(), r.popG(), r.popG()
		g := s.gate(gate)
		if g == nil || s.gate(to) == nil || b.core(gate) {
			b.refuse(r, "WRITE.trig")
			break
		}
		var tr *Trig
		for _, x := range g.Trigs {
			if x.To == to && x.Arr == -1 {
				tr = x
			}
		}
		if tr == nil {
			tr = &Trig{Gate: gate, Arr: -1, Head: -1, To: to, Made: "derived", By: r.Mem}
			g.Trigs = append(g.Trigs, tr)
		}
		tr.Worth = math.Max(worth, 0)
		s.dTrig[tr] = true
	case "WRITE.trust":
		weight, wrong, right, topic, src := r.popN(), r.popN(), r.popN(), r.popG(), r.popG()
		tr := s.trust[[2]int{src, topic}]
		if tr == nil {
			tr = &Trust{Source: src, Topic: topic}
			s.trust[[2]int{src, topic}] = tr
		}
		tr.Right, tr.Wrong, tr.Weight = int(right), int(wrong), weight
		s.dTrust[tr] = true
	case "WRITE.receipt":
		id, gate := int(r.popN()), r.popG()
		s.receipt("use", strconv.Itoa(gate), id, t)
	// ---- spawn, delete, move
	case "SPAWN":
		p := [3]float64{}
		if n := len(r.Pad); n > 0 && r.Pad[n-1].K == 'v' {
			p = r.pop().V
		}
		ng := s.newGate(p, "", "", "spawned", r.Mem)
		birth := s.newMem("birth", ng.Id, strconv.Itoa(ng.Id), "spawned", r.Mem, t)
		head := ""
		if len(r.Rest) > 0 {
			head = r.Rest[0].String()
		}
		body, _ := json.Marshal(map[string]any{"run": r.Id, "at": r.At, "from": r.From, "head": head, "who": r.Who, "what": r.What, "gates": len(s.gates), "runs": len(b.runs)})
		birth.Body, birth.Outcome = string(body), "born"
		s.addTL(t, birth.Id)
		r.push(gv(ng.Id))
		b.act("SPAWN run=%d gate=%d at=%s", r.Id, ng.Id, vstr(p))
	case "DELETE.rel":
		to, typ, from := r.popG(), r.popG(), r.popG()
		rl := s.rel(from, typ, to)
		if rl == nil || b.core(from) || b.core(to) {
			b.refuse(r, "DELETE.rel")
			break
		}
		rl.dead = true
		s.dRel[rl] = true
		s.unlink(rl)
		b.place(from)
		b.place(to)
	case "DELETE.shard":
		head, arr, gate := r.popG(), r.popG(), r.popG()
		g := s.gate(gate)
		if g == nil || b.core(gate) || g.Shards[[2]int{arr, head}] == nil {
			b.refuse(r, "DELETE.shard")
			break
		}
		sh := g.Shards[[2]int{arr, head}]
		delete(g.Shards, [2]int{arr, head})
		sh.Next = -1
		s.dShard[sh] = true
	case "DELETE.def":
		line, sec, gate := int(r.popN()), int(r.popN()), r.popG()
		if b.core(gate) {
			b.refuse(r, "DELETE.def")
			break
		}
		for _, d := range s.defs[gate][sec] {
			if d.Line == line {
				d.Body = ""
				s.dDef[d] = true
			}
		}
	case "DELETE.row":
		id := int(r.popN())
		m := s.mems[id]
		if m == nil || b.coreMem(id) || m.Kind == "run" || m.Kind == "born" || m.Kind == "told" {
			b.refuse(r, "DELETE.row")
			break
		}
		m.dead = true
		if m.Tier == "active" {
			s.active--
		}
		s.dMem[m] = true
		delete(s.memKey, m.Kind+"\x00"+m.Sig)
	case "DELETE.trig":
		to, gate := r.popG(), r.popG()
		g := s.gate(gate)
		if g == nil || b.core(gate) {
			b.refuse(r, "DELETE.trig")
			break
		}
		for i, tr := range g.Trigs {
			if tr.To == to {
				tr.Worth = -1
				s.dTrig[tr] = true
				g.Trigs = append(g.Trigs[:i], g.Trigs[i+1:]...)
				break
			}
		}
	case "DELETE.label":
		text := r.pop()
		if text.K == 't' {
			if gate, ok := s.label(text.S, "en"); ok && !b.core(gate) {
				delete(s.labels, text.S+"\x00en")
				s.dLabel[text.S+"\x00en"] = ""
				break
			}
		}
		b.refuse(r, "DELETE.label")
	case "MOVE":
		p, gate := r.pop(), r.popG()
		g := s.gate(gate)
		if g == nil || p.K != 'v' || b.core(gate) {
			b.refuse(r, "MOVE")
			break
		}
		s.movePoint(g, p.V)
	case "MOVE.mem":
		tier, id := r.popG(), int(r.popN())
		m := s.mems[id]
		if m == nil || b.coreMem(id) {
			b.refuse(r, "MOVE.mem")
			break
		}
		s.setTier(m, b.name(tier))
		s.dMem[m] = true
	// ---- find: by index only
	case "FIND.point":
		p := r.pop()
		var l []Val
		if p.K == 'v' {
			for _, id := range s.findPoint(p.V, -1) {
				l = append(l, gv(id))
			}
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "FIND.label":
		v := r.pop()
		switch v.K {
		case 'g':
			r.push(v)
			b.found(r, true)
		case 't':
			id, ok := s.label(strings.ToLower(v.S), "en")
			if !ok && strings.HasPrefix(v.S, "#") { // an address said as a name
				n, err := strconv.Atoi(v.S[1:])
				if err == nil && s.gate(n) != nil {
					id, ok = n, true
				}
			}
			if ok {
				r.push(gv(id))
			}
			b.found(r, ok)
		default:
			b.found(r, false)
		}
	case "FIND.sig":
		v := r.pop()
		id, ok := s.memSig["run\x00"+b.text(v)]
		if ok {
			r.push(num(float64(id)))
		}
		b.found(r, ok)
	case "FIND.shape":
		v := r.pop()
		var l []Val
		for _, id := range s.memShape[b.text(v)] {
			if m := s.mems[id]; m != nil && !m.dead && id != r.Mem {
				l = append(l, num(float64(id)))
			}
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "FIND.time":
		to, from := r.popN(), r.popN()
		var l []Val
		for _, id := range s.findTime(int64(from), int64(to)) {
			l = append(l, num(float64(id)))
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "FIND.value":
		n := r.popN()
		var l []Val
		for _, id := range s.values[fnum(n)] {
			l = append(l, gv(id))
		}
		r.push(lst(l))
		b.found(r, len(l) > 0)
	case "FIND.row":
		k := b.name(r.popG())
		var found *Mem
		for _, id := range s.memKind[k] {
			if m := s.mems[id]; m != nil && !m.dead && m.Tier != "long" {
				if found == nil || m.Last < found.Last {
					found = m
				}
			}
		}
		if found != nil {
			r.push(num(float64(found.Id)))
		}
		b.found(r, found != nil)
	case "FIND.rowkey":
		key, kind := r.pop(), r.popG()
		id, ok := s.memKey[b.name(kind)+"\x00"+b.keyOf(key)]
		if ok {
			r.push(num(float64(id)))
		}
		b.found(r, ok)
	// ---- math
	case "ADD", "SUB", "MUL", "DIV":
		y, x := r.pop(), r.pop()
		r.push(b.arith(g.Bind, x, y))
	case "COMPARE":
		y, x := r.pop(), r.pop()
		b.compare(r, x, y)
	// ---- outside
	case "CLOCK":
		r.push(num(float64(t)))
	case "HEAR":
		if len(r.Inbox) > 0 {
			txt := r.Inbox[0]
			r.Inbox = r.Inbox[1:]
			r.push(tv(txt))
			b.found(r, txt != "")
		} else {
			b.found(r, false)
		}
	case "SAY":
		var items []Val
		for len(r.Pad) > 0 {
			v := r.pop()
			if v.K == 'm' {
				break
			}
			items = append([]Val{v}, items...)
		}
		var words []string
		for _, v := range items {
			words = append(words, b.decode(v, "en"))
		}
		line := strings.Join(words, " ")
		b.ports.say(r.Conn, line)
		b.act("SAY run=%d %q", r.Id, line)
	case "CALL":
		args, srcg := r.pop(), r.popG()
		src := s.sources[srcg]
		if src == nil {
			b.refuse(r, "CALL no source")
			break
		}
		var argv []string
		if args.K == 'l' {
			for _, a := range args.L {
				argv = append(argv, b.text(a))
			}
		} else if args.K != 'm' {
			argv = append(argv, b.text(args))
		}
		r.Pending++
		b.ports.call(r, src, argv)
		b.act("CALL run=%d %s %q", r.Id, src.Name, argv)
	default:
		b.act("FAULT run=%d unknown physics %s", r.Id, g.Bind)
	}
}

func (b *Brain) home(r *Run) int {
	for _, v := range b.encode(r.What, "en") {
		if v.K == 'g' {
			return v.G
		}
	}
	return r.At
}

func (s *Store) rel(from, typ, to int) *Rel {
	if g := s.gate(from); g != nil {
		for _, rl := range g.Rels {
			if rl.Type == typ && rl.To == to && !rl.dead {
				return rl
			}
		}
	}
	return nil
}

func (s *Store) unlink(rl *Rel) {
	f, t := s.gates[rl.From], s.gates[rl.To]
	for i, x := range f.Rels {
		if x == rl {
			f.Rels = append(f.Rels[:i], f.Rels[i+1:]...)
			break
		}
	}
	for i, x := range t.RelsIn {
		if x == rl {
			t.RelsIn = append(t.RelsIn[:i], t.RelsIn[i+1:]...)
			break
		}
	}
}

func (b *Brain) arith(op string, x, y Val) Val {
	f := func(a, c float64) float64 {
		switch op {
		case "ADD":
			return a + c
		case "SUB":
			return a - c
		case "MUL":
			return a * c
		}
		if c == 0 {
			return math.Inf(1)
		}
		return a / c
	}
	switch {
	case x.K == 'n' && y.K == 'n':
		return num(f(x.N, y.N))
	case x.K == 'v' && y.K == 'v':
		return vec([3]float64{f(x.V[0], y.V[0]), f(x.V[1], y.V[1]), f(x.V[2], y.V[2])})
	case x.K == 'v' && y.K == 'n':
		return vec([3]float64{f(x.V[0], y.N), f(x.V[1], y.N), f(x.V[2], y.N)})
	case x.K == 'n' && y.K == 'v':
		if op == "DIV" { // n / p = n * p / |p|^2 : inversion through the unit sphere
			d := y.V[0]*y.V[0] + y.V[1]*y.V[1] + y.V[2]*y.V[2]
			if d == 0 {
				return vec(y.V)
			}
			return vec([3]float64{x.N * y.V[0] / d, x.N * y.V[1] / d, x.N * y.V[2] / d})
		}
		return vec([3]float64{f(x.N, y.V[0]), f(x.N, y.V[1]), f(x.N, y.V[2])})
	case x.K == 'l' && op == "ADD":
		return lst(append(append([]Val{}, x.L...), y))
	case x.K == 't' && op == "ADD":
		return tv(x.S + " " + b.text(y))
	}
	return x
}

// compare: same, more or less, and by how much (blueprint 4.3). The root of the balance sense.
func (b *Brain) compare(r *Run, x, y Val) {
	s := b.s
	pt := func(v Val) ([3]float64, bool) {
		if v.K == 'v' {
			return v.V, true
		}
		if v.K == 'g' {
			if g := s.gate(v.G); g != nil {
				return g.P, true
			}
		}
		return [3]float64{}, false
	}
	switch {
	case x.K == 'n' && y.K == 'n':
		d := x.N - y.N
		r.push(num(d))
		switch {
		case d > 0:
			b.outcome(r, "more")
		case d < 0:
			b.outcome(r, "less")
		default:
			b.outcome(r, "same")
		}
	case x.K == 'l' && y.K == 'l':
		// lines that disagree: items in one and not the other
		seen := map[string]int{}
		for _, v := range x.L {
			seen[v.String()]++
		}
		diff := 0
		for _, v := range y.L {
			if seen[v.String()] > 0 {
				seen[v.String()]--
			} else {
				diff++
			}
		}
		for _, n := range seen {
			diff += n
		}
		r.push(num(float64(diff)))
		if diff == 0 {
			b.outcome(r, "same")
		} else {
			b.outcome(r, "more")
		}
	case x.K == 't' && y.K == 't':
		if x.S == y.S {
			r.push(num(0))
			b.outcome(r, "same")
		} else {
			r.push(num(1))
			b.outcome(r, "more")
		}
	default:
		px, okx := pt(x)
		py, oky := pt(y)
		if !okx || !oky {
			if x.K == y.K && x.String() == y.String() {
				r.push(num(0))
				b.outcome(r, "same")
			} else {
				r.push(num(1))
				b.outcome(r, "more")
			}
			return
		}
		d := dist(px, py)
		r.push(num(d))
		if d < b.val("VALUE.same", 0.5) {
			b.outcome(r, "same")
		} else {
			b.outcome(r, "more")
		}
	}
}

// defSection reads one section of a gate's definition memory. Sections 1, 5, 6 and 7 fill themselves.
func (b *Brain) defSection(gate, sec int) []Val {
	s := b.s
	g := s.gate(gate)
	if g == nil {
		return nil
	}
	var l []Val
	switch sec {
	case 1:
		l = append(l, gv(gate), vec(g.P))
	case 2:
		for _, t := range s.glabel[gate] {
			l = append(l, tv(t))
		}
	case 5:
		for _, rl := range g.Rels {
			l = append(l, lst([]Val{gv(rl.Type), gv(rl.To), num(rl.Strength), tv(rl.State)}))
		}
		for _, rl := range g.RelsIn {
			l = append(l, lst([]Val{gv(rl.Type), gv(rl.From), num(-rl.Strength), tv(rl.State)}))
		}
	case 6:
		if g.Bind != "" {
			l = append(l, tv(g.Bind+" "+g.BVal))
		}
		for _, tr := range g.Trigs {
			l = append(l, lst([]Val{gv(tr.To), num(tr.Worth)}))
		}
	case 7:
		for _, id := range s.recs["use\x00"+strconv.Itoa(gate)] {
			l = append(l, num(float64(id)))
		}
	}
	for _, d := range s.defs[gate][sec] {
		if d.Body != "" {
			l = append(l, tv(d.Body))
		}
	}
	return l
}

// eval runs a formula string on a quiet run with one input and returns the pad top.
func (b *Brain) eval(str []int, in Val, at int) Val {
	r := &Run{Id: -1, At: at, From: at, Quiet: true, Worth: 0}
	r.push(in)
	for _, g := range str {
		r.Rest = append(r.Rest, gv(g))
	}
	for i := 0; i < 64 && len(r.Rest) > 0; i++ {
		b.step(r)
	}
	return r.pop()
}

// reach: passing a relationship-type gate with a gate in hand reaches the related gate(s):
// the stored line first, then the type's formula and FIND at that point (blueprint 5.3).
func (b *Brain) reach(r *Run, typ *Gate) {
	s := b.s
	from := r.popG()
	g := s.gate(from)
	if g == nil {
		b.found(r, false)
		return
	}
	var l []Val
	for _, rl := range g.Rels {
		if rl.Type == typ.Id {
			l = append(l, gv(rl.To))
		}
	}
	if len(l) > 0 {
		r.push(lst(l))
		b.found(r, true)
		return
	}
	fwd := s.gate(typ.Str[0])
	p := b.eval(fwd.Str, vec(g.P), fwd.Id)
	if p.K == 'v' {
		for _, id := range s.findPoint(p.V, from) {
			l = append(l, gv(id))
		}
	}
	r.push(lst(l))
	b.found(r, len(l) > 0)
}

// place: the tug of war (blueprint 5.5). A point sits at the strength-weighted mean of where its relationships put it.
func (b *Brain) place(gate int) {
	s := b.s
	g := s.gate(gate)
	if g == nil || b.core(gate) || g.Bind != "" {
		return
	}
	var sum [3]float64
	var w float64
	add := func(p Val, st float64) {
		if p.K != 'v' || st <= 0 || math.IsNaN(p.V[0]) || math.IsInf(p.V[0], 0) {
			return
		}
		for i := 0; i < 3; i++ {
			sum[i] += p.V[i] * st
		}
		w += st
	}
	for _, rl := range g.Rels {
		if t := s.gate(rl.Type); t != nil && t.Bind == "rel" && len(t.Str) == 2 {
			back := s.gate(t.Str[1])
			add(b.eval(back.Str, vec(s.gates[rl.To].P), back.Id), rl.Strength)
		}
	}
	for _, rl := range g.RelsIn {
		if t := s.gate(rl.Type); t != nil && t.Bind == "rel" && len(t.Str) == 2 {
			fwd := s.gate(t.Str[0])
			add(b.eval(fwd.Str, vec(s.gates[rl.From].P), fwd.Id), rl.Strength)
		}
	}
	if w > 0 {
		p := [3]float64{sum[0] / w, sum[1] / w, sum[2] / w}
		if dist(p, g.P) > 1e-9 {
			s.movePoint(g, p)
			b.act("MOVE gate=%d -> %s", gate, vstr(p))
		}
	}
}
