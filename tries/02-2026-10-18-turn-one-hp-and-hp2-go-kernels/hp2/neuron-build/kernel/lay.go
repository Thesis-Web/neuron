package main

// The lay loader: turns the told base (text in lay/) into gates, labels,
// relationships, process strings and the shards that walk them. Every row it
// makes is marked told. After "told ends" it refuses every file, forever.
//
//   gate NAME [phys WORD] [val N] [at X Y Z] [core]
//   label LANG "TEXT" NAME
//   proc NAME = ITEM ITEM ...
//   on NAME OUTCOME -> TARGET     (branch at NAME's last physics word; the rest of NAME is skipped)
//   trig NAME -> QUESTION [WORTH] (a usual trigger: new shards on NAME copy it)
//   rel A TYPE B [STRENGTH]
//   unrel A TYPE B                (takes back a told line)
//   sect NAME SECTION VALUE       (VALUE: a gate name, a number, or "text")
//   source NAME grounded|ungrounded COMMAND-TEMPLATE (%s is the query)

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func tokens(line string) []string {
	var out []string
	var cur strings.Builder
	in, esc, has := false, false, false
	for _, c := range line {
		switch {
		case esc:
			cur.WriteRune(c)
			esc = false
		case in && c == '\\':
			esc = true
		case c == '"':
			in, has = !in, true
		case !in && (c == ' ' || c == '\t'):
			if has || cur.Len() > 0 {
				out = append(out, cur.String())
			}
			cur.Reset()
			has = false
		case !in && c == '#' && cur.Len() == 0 && !has:
			return out
		default:
			cur.WriteRune(c)
		}
	}
	if has || cur.Len() > 0 {
		out = append(out, cur.String())
	}
	return out
}

// spiral gives each told gate its own point on the unit sphere until relationships pull
// it: an even spread at any count (a low-discrepancy sequence, so the i-th point never
// depends on how many gates there will be).
func spiral(i int64) [3]float64 {
	t := float64(i) + 0.5
	z := 1 - 2*math.Mod(t*0.7548776662466927, 1)
	th, s := 2*math.Pi*math.Mod(t*0.5698402909980532, 1), math.Sqrt(1-z*z)
	return [3]float64{s * math.Cos(th), s * math.Sin(th), z}
}

type layErr string

func (k *K) lay(path string) string {
	if k.meta["told_ended"] != "" {
		return "refused: told has ended\n"
	}
	data, err := os.ReadFile(path)
	if err != nil {
		return err.Error() + "\n"
	}
	lines := strings.Split(string(data), "\n")
	told, first := k.nm("TOLD"), len(k.G)
	k.layNew = int64(first)
	// pass 1: every named gate exists (gate 0 is zero, at the origin)
	for _, l := range lines {
		if t := tokens(l); len(t) >= 2 && (t[0] == "gate" || t[0] == "proc") {
			if _, ok := k.names[t[1]]; !ok {
				if len(k.G) == 0 && t[1] != "ZERO" {
					k.setName("ZERO", k.newGate([3]float64{}, told, 0))
				}
				p := spiral(int64(len(k.G)))
				if len(k.G) == 0 {
					p = [3]float64{}
				}
				k.setName(t[1], k.newGate(p, told, 0))
			}
		}
	}
	told = k.nm("TOLD")
	laid := k.newMem(k.nm("LAID"), 0, told, k.now)
	k.setBody(laid, []Val{tv(path)})
	if g, ok := k.names["miss"]; ok && int(g) >= first {
		first = 0 // the file that brings the miss way gives it to every gate made before it (once)
	}
	for g := first; g < len(k.G); g++ { // otherwise only the gates this file made
		if gt := k.G[g]; gt.Made == 0 || gt.Miss == 0 {
			gt.Made, gt.Rcpt, gt.Miss = told, laid.ID, k.nm("miss")
			k.q("UPDATE gate SET made=?,rcpt=?,miss=? WHERE g=?", told, laid.ID, gt.Miss, g)
		}
	}
	var errs []string
	var procs []int64
	var branches [][]string
	for n, l := range lines {
		func() {
			defer func() {
				if e := recover(); e != nil {
					errs = append(errs, fmt.Sprintf("%s:%d: %v", path, n+1, e))
				}
			}()
			if t := tokens(l); len(t) > 0 {
				procs, branches = k.layLine(t, laid.ID, procs, branches)
			}
		}()
	}
	// branches: the outcome's shard at the last physics word of the process, in its frame
	for _, b := range branches {
		g, o, tg := k.names[b[1]], k.names[b[2]], k.names[b[4]]
		var test int64 = -1
		for _, x := range k.G[g].Proc {
			if k.G[x].Phys != "" {
				test = x
			}
		}
		if s := k.gate(test); s == nil {
			errs = append(errs, fmt.Sprintf("%s: %s has no physics word to branch on", path, b[1]))
		} else if x := s.Sh[SK{g, o}]; x != nil && x.Next != tg && x.Made != told {
			errs = append(errs, fmt.Sprintf("%s: branch conflict in %s on %s (not a told shard)", path, b[1], b[2]))
		} else {
			k.putShard(test, SK{g, o}, &Shard{Next: tg, Made: told})
		}
	}
	k.gridAll() // the point index, once CELL is told
	// the walk: lay the shards each told string steps through
	for _, g := range procs {
		k.walk(g, g, items(g, k.G[g].Proc), map[string]bool{}, 0)
	}
	k.commit()
	if len(errs) > 0 {
		return strings.Join(errs, "\n") + "\n"
	}
	return fmt.Sprintf("laid %s: %d gates now\n", path, len(k.G))
}

func (k *K) look(name string) int64 {
	g, ok := k.names[name]
	if !ok {
		panic(layErr(fmt.Sprintf("unknown gate %q", name)))
	}
	return g
}

func num(s string) float64 {
	f, err := strconv.ParseFloat(s, 64)
	if err != nil {
		panic(layErr(fmt.Sprintf("bad number %q", s)))
	}
	return f
}

func (k *K) layLine(t []string, laid int64, procs []int64, branches [][]string) ([]int64, [][]string) {
	told := k.nm("TOLD")
	shape := map[string]bool{"label": len(t) == 4, "proc": len(t) >= 3 && t[2] == "=", "on": len(t) == 5 && t[3] == "->",
		"trig": len(t) >= 4 && t[2] == "->", "rel": len(t) >= 4, "unrel": len(t) == 4, "sect": len(t) == 4, "source": len(t) >= 4, "gate": len(t) >= 2}
	if ok, known := shape[t[0]]; !known || !ok {
		panic(layErr("bad line: " + strings.Join(t, " ")))
	}
	opt := func(i int, d float64) float64 {
		if len(t) > i {
			return num(t[i])
		}
		return d
	}
	switch t[0] {
	case "gate":
		g := k.look(t[1])
		for i := 2; i < len(t); i++ {
			switch t[i] {
			case "phys":
				i++
				k.G[g].Phys = t[i]
				k.q("INSERT OR REPLACE INTO phys VALUES(?,?)", g, t[i])
			case "val":
				i++
				k.setVal(g, num(t[i]))
			case "at":
				// a told point is set when the gate is made; a re-lay never moves a gate the brain has moved
				if g >= k.layNew {
					k.movePoint(g, [3]float64{num(t[i+1]), num(t[i+2]), num(t[i+3])})
				}
				i += 3
			case "init":
				// state the brain keeps (a place in a book, its last sleep): set only when it has none
				i++
				if !k.G[g].HasVal {
					k.setVal(g, num(t[i]))
				}
			case "core":
				k.G[g].Core = true
				k.q("INSERT OR IGNORE INTO core VALUES(?)", g)
			default:
				panic(layErr("unknown gate attribute " + t[i]))
			}
		}
	case "label":
		k.addLabel(t[2], t[1], k.look(t[3]), told)
	case "proc":
		g, p := k.look(t[1]), []int64{}
		for _, x := range t[3:] {
			p = append(p, k.look(x))
		}
		k.setProc(g, p, told)
		procs = append(procs, g)
	case "on":
		k.look(t[1])
		k.look(t[2])
		k.look(t[4])
		branches = append(branches, t)
	case "trig":
		k.setUsual(k.look(t[1]), k.look(t[3]), opt(4, 0.5))
	case "rel":
		// a line that already exists keeps the strength the brain has given it
		a, ty, b := k.look(t[1]), k.look(t[2]), k.look(t[3])
		if k.G[a].Out[[2]int64{ty, b}] == nil {
			k.putRel(&Rel{A: a, Type: ty, B: b, S: opt(4, 1), State: told, Rcpt: laid, T: k.now, Made: told})
		}
	case "unrel":
		// a told line taken back before told ends (only a told one)
		a, ty, b := k.look(t[1]), k.look(t[2]), k.look(t[3])
		if x := k.G[a].Out[[2]int64{ty, b}]; x != nil && x.Made == told {
			k.delRel(a, ty, b)
		}
	case "sect":
		v := tv(t[3])
		if x, ok := k.names[t[3]]; ok {
			v = gv(x)
		} else if f, err := strconv.ParseFloat(t[3], 64); err == nil {
			v = nv(f)
		}
		g, sec := k.look(t[1]), k.look(t[2])
		for _, x := range k.G[g].Sect[sec] {
			if x.V.enc() == v.enc() {
				return procs, branches // already held: a re-lay doesn't push it over what the brain wrote since
			}
		}
		k.addSect(g, sec, v, laid, k.now)
	case "source":
		g, s := k.look(t[1]), Src{strings.Join(t[3:], " "), t[2] == "grounded"}
		k.src[g] = s
		k.q("INSERT OR REPLACE INTO src VALUES(?,?,?)", g, s.How, s.Grounded)
	}
	return procs, branches
}

type wi struct{ g, f int64 }

func items(g int64, p []int64) []wi {
	out := make([]wi, len(p))
	for i, x := range p {
		out[i] = wi{x, g}
	}
	return out
}

var outcomes = []string{"NONE", "SAME", "MORE", "LESS", "GATE", "NUMBER", "TEXT", "POINT", "LIST", "YES", "NO"}

// walk steps a told string the way a run will, laying each shard it needs.
func (k *K) walk(at, from int64, rest []wi, seen map[string]bool, depth int) {
	for len(rest) > 0 && depth < 64 {
		h := rest[0]
		key := fmt.Sprint(at, from, rest[:min(len(rest), 48)])
		if seen[key] || len(seen) > 20000 {
			return
		}
		seen[key] = true
		if sk := (SK{from, h.g}); k.G[at].Sh[sk] == nil {
			k.putShard(at, sk, &Shard{Next: h.g, Out: append([]Trig(nil), k.G[at].Usual...), Made: k.nm("TOLD")})
		}
		prev := at
		rest, at, from = rest[1:], h.g, h.f
		g := k.G[at]
		switch {
		case g.Phys == "READ" && len(rest) > 0 && prev == k.nm("ITEM"):
			rest = rest[1:] // the quoted gate is read, not stepped to
		case g.Phys == "GO" || g.Phys == "END":
			return
		case g.Phys == "" && g.Proc != nil:
			rest, from = append(items(at, g.Proc), rest...), at
		}
		for _, o := range outcomes {
			if s := g.Sh[SK{from, k.nm(o)}]; s != nil && k.G[s.Next].Proc != nil {
				r2 := rest
				for len(r2) > 0 && r2[0].f == from {
					r2 = r2[1:]
				}
				k.walk(s.Next, s.Next, append(items(s.Next, k.G[s.Next].Proc), r2...), seen, depth+1)
			}
		}
	}
}
