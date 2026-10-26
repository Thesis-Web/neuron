package main

// lay.go: the told base loader. It turns the small lay notation into gates, shards, strings,
// relationships, labels, triggers and sources, every row marked told. After "told ends" it refuses.

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

type layer struct {
	b     *Brain
	names map[string]int
	by    int
	errs  []string
	rows  int
	file  string
}

func (b *Brain) loadNames() map[string]int {
	if b.names == nil {
		b.names = map[string]int{}
		rows, err := b.s.db.Query("SELECT k,v FROM kv WHERE k LIKE 'name:%'")
		must(err)
		defer rows.Close()
		for rows.Next() {
			var k, v string
			rows.Scan(&k, &v)
			n, _ := strconv.Atoi(v)
			b.names[k[5:]] = n
		}
	}
	return b.names
}

// lay loads one lay file into the live brain (from the lay port, or at birth).
func (b *Brain) lay(text, name string, c *conn) {
	report := b.layText(text, name)
	if c != nil {
		b.ports.say(c, report)
		c.c.Close()
	} else {
		fmt.Println(report)
	}
}

func (b *Brain) layText(text, name string) string {
	s := b.s
	if name == "TOLD-ENDS" {
		s.kv("told", "ends")
		s.told = true
		m := s.newMem("told", 0, "told ends", "told", 0, b.now())
		s.setTier(m, "persistent")
		m.Outcome = "ends"
		s.addTL(m.First, m.Id)
		b.act("TOLD ENDS")
		return "told ends. the kernel refuses lay files from now on."
	}
	if name == "TOLD-OPENS" { // a new turn opens on this body: told rows may be laid again until the next told ends
		s.kv("told", "open")
		s.told = false
		m := s.newMem("told", 0, "told opens", "told", 0, b.now())
		s.setTier(m, "persistent")
		m.Outcome = "opens"
		s.addTL(m.First, m.Id)
		b.act("TOLD OPENS")
		return "told opens. the kernel takes lay files again until told ends."
	}
	if s.told {
		b.act("REFUSE lay %s: told ends", name)
		return "refused: told ends"
	}
	t := b.now()
	m := s.newMem("told", 0, name, "told", 0, t)
	s.setTier(m, "persistent")
	m.Outcome, m.Body = "laid", name
	s.addTL(t, m.Id)
	l := &layer{b: b, names: b.loadNames(), by: m.Id, file: name}
	before := len(l.names)
	l.load(text)
	earlier := map[int]bool{} // this file's earlier loads: a trigger they laid that this load did not re-lay is gone
	for _, x := range s.mems {
		if x.Kind == "told" && x.Sig == name && x.Id != m.Id {
			earlier[x.Id] = true
		}
	}
	if len(earlier) > 0 {
		for _, g := range s.gates {
			if g == nil {
				continue
			}
			kept := g.Trigs[:0]
			for _, tr := range g.Trigs {
				if tr.Made == "told" && earlier[tr.By] {
					tr.Worth = -1
					s.dTrig[tr] = true
					continue
				}
				kept = append(kept, tr)
			}
			g.Trigs = kept
		}
	}
	if len(l.names) > before {
		for n, id := range l.names {
			if s.gates[id].By == m.Id || s.gates[id].Made == "core" && s.gates[id].By == m.Id {
				s.kv("name:"+n, strconv.Itoa(id))
			}
		}
	}
	if len(l.errs) > 0 {
		b.act("LAY %s rows=%d errors=%d", name, l.rows, len(l.errs))
		return fmt.Sprintf("%s: %d rows, %d errors\n%s", name, l.rows, len(l.errs), strings.Join(l.errs, "\n"))
	}
	b.act("LAY %s rows=%d", name, l.rows)
	return fmt.Sprintf("%s: %d rows laid", name, l.rows)
}

func (l *layer) err(line int, f string, a ...any) {
	l.errs = append(l.errs, fmt.Sprintf("%s:%d: %s", l.file, line, fmt.Sprintf(f, a...)))
}

func (l *layer) gate(name string, line int) int {
	if id, ok := l.names[name]; ok {
		return id
	}
	l.err(line, "no gate named %q", name)
	return -1
}

// token resolves one proc token to gate ids: a name, 'name (quote), or =number (a value gate).
func (l *layer) token(tok string, line int) []int {
	s := l.b.s
	switch {
	case strings.HasPrefix(tok, "'"):
		q := s.byBind["READ.next"]
		g := l.gate(tok[1:], line)
		return []int{q, g}
	case strings.HasPrefix(tok, "="):
		n, err := strconv.ParseFloat(tok[1:], 64)
		if err != nil {
			l.err(line, "bad number %q", tok)
			return nil
		}
		named := map[int]bool{}
		for _, id := range l.names {
			named[id] = true
		}
		for _, id := range s.consts[fnum(n)] { // only an anonymous told constant is shared
			if s.gates[id].Made == "told" && len(s.glabel[id]) == 0 && !named[id] {
				return []int{id}
			}
		}
		g := s.newGate([3]float64{}, "VALUE.const", fnum(n), "told", l.by) // machinery: never a number's gate
		l.rows++
		return []int{g.Id}
	}
	return []int{l.gate(tok, line)}
}

func (l *layer) load(text string) {
	s := l.b.s
	lines := strings.Split(text, "\n")
	type procDef struct {
		line   int
		gate   int
		toks   []string
		branch [][3]string // tokenIndex(as string), outcome, target
	}
	var procs []*procDef
	var later []func()
	// pass 1: names
	for i, raw := range lines {
		ln := strings.TrimSpace(raw)
		if ln == "" || strings.HasPrefix(ln, "#") {
			continue
		}
		f := strings.Fields(ln)
		kw := f[0]
		switch kw {
		case "gate", "proc", "core", "reltype", "source":
			if len(f) < 2 {
				l.err(i+1, "missing name")
				continue
			}
			name := strings.TrimSuffix(f[1], ":")
			if id, ok := l.names[name]; ok {
				if g := s.gate(id); kw == "core" || (g != nil && g.Made == "core") {
					l.err(i+1, "core gate %q already exists", name)
				} else if g != nil && kw == "proc" && g.BVal != "" { // re-told: the string and its told shards are replaced
					old := map[int]bool{g.Id: true}
					for _, x := range g.Str {
						old[x] = true
					}
					for x := range old {
						xg := s.gate(x)
						for k, sh := range xg.Shards { // its own ways, told or laid by the miss way since
							if x == g.Id || old[k[0]] {
								sh.Next = -1
								s.dShard[sh] = true
								delete(xg.Shards, k)
							}
						}
					}
				}
				continue
			}
			g := s.newGate([3]float64{}, "", "", "told", l.by)
			if kw == "core" {
				g.Made = "core"
			}
			l.names[name] = g.Id
			l.rows++
		}
	}
	// pass 2: everything
	var cur *procDef
	for i, raw := range lines {
		line := i + 1
		ln := strings.TrimSpace(raw)
		if ln == "" || strings.HasPrefix(ln, "#") {
			continue
		}
		if cur != nil && strings.Contains(ln, "->") && (raw[0] == ' ' || raw[0] == '\t') {
			p := strings.SplitN(ln, "->", 2)
			cur.branch = append(cur.branch, [3]string{strconv.Itoa(len(cur.toks) - 1), strings.TrimSpace(p[0]), strings.TrimSpace(p[1])})
			continue
		}
		cur = nil
		f := strings.Fields(ln)
		switch f[0] {
		case "gate":
			g := s.gate(l.names[f[1]])
			rest := f[2:]
			for len(rest) > 0 {
				switch rest[0] {
				case "=":
					if len(rest) < 2 {
						l.err(line, "gate = needs a number")
						rest = nil
						break
					}
					if g.Bind == "" || g.Bind == "value" {
						s.rebind(g, "value", rest[1])
					} else {
						s.rebind(g, g.Bind, rest[1])
					}
					rest = rest[2:]
				case "@":
					if len(rest) < 4 {
						l.err(line, "gate @ needs x y z")
						rest = nil
						break
					}
					var p [3]float64
					for k := 0; k < 3; k++ {
						p[k], _ = strconv.ParseFloat(rest[1+k], 64)
					}
					s.movePoint(g, p)
					rest = rest[4:]
				case ":":
					if len(rest) < 2 {
						l.err(line, "gate : needs a binding")
						rest = nil
						break
					}
					if rest[1] == "plain" { // a told gate made plain again: its binding, string and the hops the brain laid on it go
						for k, sh := range g.Shards {
							if sh.Made != "told" {
								sh.Next = -1
								s.dShard[sh] = true
								delete(g.Shards, k)
							}
						}
						s.rebind(g, "", "")
						g.Str, g.Made, g.By = nil, "told", l.by
					} else if g.Bind == "value" || g.Bind == rest[1] { // a re-told binding keeps its value or its string (a PROC handle's way)
						s.rebind(g, rest[1], g.BVal)
					} else {
						s.rebind(g, rest[1], "")
					}
					rest = rest[2:]
				default:
					l.err(line, "unknown gate clause %q", rest[0])
					rest = nil
				}
			}
			s.touch(g)
		case "label":
			if len(f) < 3 {
				l.err(line, "label NAME text...")
				continue
			}
			g := l.gate(f[1], line)
			if g < 0 {
				continue
			}
			lang := "en"
			texts := f[2:]
			if len(texts) > 1 && strings.HasPrefix(texts[len(texts)-1], "lang=") {
				lang = texts[len(texts)-1][5:]
				texts = texts[:len(texts)-1]
			}
			for _, t := range texts {
				if len(t) > 1 {
					t = strings.Trim(t, "\"")
				}
				t = strings.ToLower(t)
				if old, ok := s.label(t, lang); ok && old != g {
					l.err(line, "label %q already points to gate %d", t, old)
					continue
				}
				s.setLabel(t, lang, g, "told", l.by)
				l.rows++
			}
		case "proc", "core":
			name := strings.TrimSuffix(f[1], ":")
			pd := &procDef{line: line, gate: l.names[name], toks: f[2:]}
			if len(f) > 2 && f[2] == ":" {
				pd.toks = f[3:]
			}
			procs = append(procs, pd)
			cur = pd
		case "reltype":
			// reltype NAME fwd: tokens... back: tokens...
			name := strings.TrimSuffix(f[1], ":")
			g := s.gate(l.names[name])
			var fwd, back []string
			mode := ""
			for _, tok := range f[2:] {
				switch tok {
				case "fwd:":
					mode = "f"
				case "back:":
					mode = "b"
				default:
					if mode == "f" {
						fwd = append(fwd, tok)
					} else {
						back = append(back, tok)
					}
				}
			}
			if len(fwd) == 0 || len(back) == 0 {
				l.err(line, "reltype needs fwd: and back:")
				continue
			}
			fg := s.newGate([3]float64{}, "", "", "told", l.by)
			bg := s.newGate([3]float64{}, "", "", "told", l.by)
			l.names[name+".fwd"], l.names[name+".back"] = fg.Id, bg.Id
			procs = append(procs, &procDef{line: line, gate: fg.Id, toks: fwd}, &procDef{line: line, gate: bg.Id, toks: back})
			s.rebind(g, "rel", fmt.Sprintf("%d %d", fg.Id, bg.Id))
			l.rows += 3
		case "rel":
			if len(f) < 4 {
				l.err(line, "rel FROM TYPE TO [strength] [state]")
				continue
			}
			from, typ, to := l.gate(f[1], line), l.gate(f[2], line), l.gate(f[3], line)
			if from < 0 || typ < 0 || to < 0 {
				continue
			}
			strength, state := 1.0, "told"
			if len(f) > 4 {
				strength, _ = strconv.ParseFloat(f[4], 64)
			}
			if len(f) > 5 {
				state = f[5]
			}
			later = append(later, func() {
				rl := s.rel(from, typ, to)
				if rl == nil {
					rl = &Rel{From: from, Type: typ, To: to, Made: "told", By: l.by}
					s.gates[from].Rels = append(s.gates[from].Rels, rl)
					s.gates[to].RelsIn = append(s.gates[to].RelsIn, rl)
				}
				rl.Strength, rl.State, rl.When = strength, state, l.b.now()
				s.dRel[rl] = true
				l.b.place(from)
				l.b.place(to)
				l.rows++
			})
		case "trig":
			// trig GATE -> PROC [worth]
			if len(f) < 4 || f[2] != "->" {
				l.err(line, "trig GATE -> PROC [worth]")
				continue
			}
			g, to := l.gate(f[1], line), l.gate(f[3], line)
			if g < 0 || to < 0 {
				continue
			}
			w := 0.5
			if len(f) > 4 {
				w, _ = strconv.ParseFloat(f[4], 64)
			}
			var tr *Trig
			for _, x := range s.gates[g].Trigs {
				if x.To == to && x.Arr == -1 {
					tr = x
				}
			}
			if tr == nil {
				tr = &Trig{Gate: g, Arr: -1, Head: -1, To: to, Made: "told", By: l.by}
				s.gates[g].Trigs = append(s.gates[g].Trigs, tr)
			}
			tr.Worth, tr.By = w, l.by // a re-tell re-lays it: its by is this file's memory now
			s.dTrig[tr] = true
			l.rows++
		case "source":
			// source NAME grounded|lower|guess : prog args...
			name := strings.TrimSuffix(f[1], ":")
			g := l.names[name]
			if len(f) < 5 {
				l.err(line, "source NAME grounded|lower|guess : prog args...")
				continue
			}
			grounded := map[string]int{"grounded": 2, "lower": 1, "guess": 0}[f[2]]
			src := &Source{Gate: g, Name: name, Grounded: grounded}
			for _, a := range f[4:] {
				src.How = append(src.How, strings.Trim(a, "\""))
			}
			s.sources[g] = src
			s.gates[g].Sources = src
			s.dSrc[g] = true
			l.rows++
		case "miss":
			g, p := l.gate(f[1], line), l.gate(f[2], line)
			if g >= 0 && p >= 0 {
				s.gates[g].Miss = p
				s.touch(s.gates[g])
			}
		default:
			l.err(line, "unknown keyword %q", f[0])
		}
	}
	// pass 3: process strings and their shards
	for _, pd := range procs {
		g := s.gate(pd.gate)
		var str []int
		var tokGate []int // gate of the last id each token produced
		for _, tok := range pd.toks {
			ids := l.token(tok, pd.line)
			str = append(str, ids...)
			if len(ids) > 0 {
				tokGate = append(tokGate, ids[len(ids)-1])
			} else {
				tokGate = append(tokGate, -1)
			}
		}
		if len(str) == 0 {
			l.err(pd.line, "empty process")
			continue
		}
		bad := false
		for _, x := range str {
			if x < 0 {
				bad = true
			}
		}
		if bad {
			continue
		}
		var p []string
		for _, x := range str {
			p = append(p, strconv.Itoa(x))
		}
		bind := "proc"
		if strings.HasPrefix(g.Bind, "PROC.") {
			bind = g.Bind
		}
		s.rebind(g, bind, strings.Join(p, " "))
		told := map[[3]int]bool{} // (test, arrival, outcome) the branches below lay: no inert pass-through for those
		type branch struct {
			test, arr, out int
			name, target   string
		}
		var brs []branch
		for _, br := range pd.branch {
			ti, _ := strconv.Atoi(br[0])
			test := tokGate[ti]
			k := len(str) - 1
			for k > 0 && str[k] != test {
				k--
			}
			out, ok := s.byBind["outcome."+br[1]]
			if !ok {
				l.err(pd.line, "no outcome %q", br[1])
				continue
			}
			for _, arr := range l.b.arrivals(g, str, k) {
				told[[3]int{test, arr, out}] = true
				brs = append(brs, branch{test, arr, out, br[1], br[2]})
			}
		}
		l.rows += 1 + l.b.layShards(g, "told", l.by, told)
		for _, br := range brs {
			test, arr, out := br.test, br.arr, br.out
			target := l.gate(br.target, pd.line)
			if target < 0 {
				continue
			}
			tg := s.gate(test)
			if tg.Bind == "" || tg.Bind == "proc" || tg.Bind == "value" || strings.HasPrefix(tg.Bind, "PROC.") { // a reltype gate is a test too (reach)
				l.err(pd.line, "branch %s after gate %d, which is not a physics test (a process cannot hand its outcome to its caller)", br.name, test)
				continue
			}
			if old := tg.Shards[[2]int{arr, out}]; old != nil && old.Next != target && old.Made == "told" {
				l.err(pd.line, "branch %s on gate %d from %d already goes to %d", br.name, test, arr, old.Next)
				continue
			}
			sh := &Shard{Gate: test, Arr: arr, Head: out, Next: target, Made: "told", By: l.by}
			tg.Shards[[2]int{arr, out}] = sh
			s.dShard[sh] = true
			l.rows++
		}
		if g.Made == "core" {
			m := s.newMem("core", g.Id, strconv.Itoa(g.Id), "core", l.by, l.b.now())
			s.setTier(m, "persistent")
			m.Body, m.Outcome = g.BVal, "core"
			s.addTL(m.First, m.Id)
			l.rows++
		}
	}
	for _, f := range later {
		f()
	}
}

// layShards lays the shards a process string needs so its own hops never miss:
// (P, -1, g1) for the first hop, then (g_i, g_i-1, g_i+1) for the rest. A test's outcome that has no branch
// (told names those) passes inert (LAY-NOTATION 2): (g_i, g_i-1, outcome -> outcome) and (outcome, g_i, g_i+1).
func (b *Brain) layShards(g *Gate, made string, by int, told map[[3]int]bool) int {
	s := b.s
	n := 0
	put := func(gate, arr, head, next int) {
		og := s.gate(gate)
		if og == nil || og.Shards[[2]int{arr, head}] != nil {
			return
		}
		sh := &Shard{Gate: gate, Arr: arr, Head: head, Next: next, Made: made, By: by}
		og.Shards[[2]int{arr, head}] = sh
		s.dShard[sh] = true
		n++
	}
	str := g.Str
	if len(str) == 0 {
		return 0
	}
	put(g.Id, -1, str[0], str[0])
	q := s.byBind["READ.next"]
	for i := 0; i < len(str); {
		next := i + 1
		if str[i] == q { // a quote takes the next gate as data; the hop after it goes to the one beyond
			next = i + 2
		}
		outs := b.outcomesOf(str[i])
		for _, p := range b.arrivals(g, str, i) {
			if next < len(str) {
				put(str[i], p, str[next], str[next])
			}
			for _, o := range outs {
				if !told[[3]int{str[i], p, o}] {
					put(str[i], p, o, o)
				}
			}
		}
		for _, o := range outs {
			if next < len(str) {
				put(o, str[i], str[next], str[next])
			}
		}
		i = next
	}
	return n
}

// arrivals names the gates a run can arrive from at position i of a process string: the gate before (the quote
// gate when the one before is a quote's data), plus that gate's outcomes when it is a test that passed inert.
func (b *Brain) arrivals(g *Gate, str []int, i int) []int {
	if i == 0 {
		return []int{g.Id}
	}
	p := str[i-1]
	if q := b.s.byBind["READ.next"]; i >= 2 && str[i-2] == q {
		p = q
	}
	return append([]int{p}, b.outcomesOf(p)...)
}

// layDir loads every *.lay file in a directory, in name order (birth).
func (b *Brain) layDir(dir string) {
	files, _ := filepath.Glob(filepath.Join(dir, "*.lay"))
	sort.Strings(files)
	for _, f := range files {
		text, err := os.ReadFile(f)
		if err != nil {
			fmt.Println(err)
			continue
		}
		b.lay(string(text), filepath.Base(f), nil)
	}
}
