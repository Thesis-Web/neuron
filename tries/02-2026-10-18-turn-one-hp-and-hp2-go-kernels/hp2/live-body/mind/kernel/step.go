package main

// Runs, the step, and the physics words. The step never chooses: the shard
// holds the way, and a miss goes to neuron code (the gate's miss process).

import (
	"fmt"
	"math"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"
)

type Item struct {
	G int64 // gate; -1 for raw text not yet a gate
	T string
	D int   // call depth: 0 is input, >0 came from a process string
	F int64 // the process (frame) the item came from; 0 for input
	O bool  // an outcome put at the head by a test
}

type Run struct {
	ID, At, From          int64
	Rest                  []Item
	Pad, Landed           []Val
	Subj, Want            Val
	HasSubj, HasWant      bool
	Trail, D0             []int64
	Steps, Kids, CurD     int
	Parent                *Run
	Worth                 float64
	Ctx                   [6]string // who what when where why how
	Made, Mem, Conn, Why  int64
	Ev                    [3]Item // the last miss: at, from, head
	InMiss, Gen, PGen     int
	Checked, Waiting      bool
	Parked, Ending, Child bool
	Stuck                 bool
	Hold, CurF, Pend      int64
	Start                 int64
	Tail                  int // len(Rest) when the miss was taken: where its head is
	LastStep              int64 // the beat it last took a step (blueprint §12.2: low-worth runs wait)
	Slots                 map[int64]Val
}

type K struct {
	*Brain
	runs          []*Run
	nextRun, beat int64
	layNew        int64 // the first gate the file being laid made
	now           int64
	port          *Ports
}

func (k *K) push(r *Run, v Val) { r.Pad = append(r.Pad, v) }

// pop takes the most recent pad value of a kind (0 = any). A one-element list
// stands for its element.
func (k *K) pop(r *Run, kind byte) (Val, bool) {
	for i := len(r.Pad) - 1; i >= 0; i-- {
		v := r.Pad[i]
		if kind != 0 && v.K != kind && v.K == 'l' && len(v.L) == 1 && v.L[0].K == kind {
			v = v.L[0]
		}
		if kind == 0 || v.K == kind {
			r.Pad = append(r.Pad[:i:i], r.Pad[i+1:]...)
			return v, true
		}
	}
	return Val{}, false
}

func (k *K) popG(r *Run) int64 {
	if v, ok := k.pop(r, 'g'); ok {
		return v.G
	}
	return -1
}

func (k *K) popN(r *Run) (float64, bool) { v, ok := k.pop(r, 'n'); return v.N, ok }

// outcome puts an outcome gate at the head of the remainder so the next shard picks the branch.
func (k *K) outcome(r *Run, name string) {
	r.Rest = append([]Item{{G: k.nm(name), D: r.CurD, F: r.CurF, O: true}}, r.Rest...)
}
func (k *K) none(r *Run) { k.outcome(r, "NONE") }

func (k *K) newRun(at int64, parent *Run, worth float64) *Run {
	k.nextRun++
	r := &Run{ID: k.nextRun, At: at, From: at, Start: at, Parent: parent, Worth: worth, Made: k.nm("SPAWNED"), Slots: map[int64]Val{}}
	if parent != nil {
		parent.Kids++
		r.Child, r.Ctx, r.Conn, r.Why, r.Made, r.PGen = true, parent.Ctx, parent.Conn, parent.Why, parent.Made, parent.Gen
		r.D0 = append([]int64(nil), parent.D0...)
		r.Pad = append([]Val(nil), parent.Pad...)
		for g, v := range parent.Slots {
			r.Slots[g] = v
		}
	}
	k.runs = append(k.runs, r)
	return r
}

// pass: what arriving at a gate does.
func (k *K) pass(r *Run, d int) {
	g := k.G[r.At]
	switch {
	case g.Phys != "":
		k.phys(r, g.Phys)
	case g.Proc != nil:
		// a call: the string goes in front of the remainder, and the run is now in its frame
		in := make([]Item, len(g.Proc), len(g.Proc)+len(r.Rest))
		for i, x := range g.Proc {
			in[i] = Item{G: x, D: d + 1, F: r.At}
		}
		r.Rest, r.From = append(in, r.Rest...), r.At
	case g.HasVal:
		k.push(r, nv(g.Val))
	default:
		k.push(r, gv(r.At))
	}
	if r.At == k.nm("core-ok") {
		r.Checked = true
	}
}

// split starts a branch run at a gate; the main run keeps going.
func (k *K) split(r *Run, at int64, worth float64) {
	if k.gate(at) == nil {
		return
	}
	c := k.newRun(at, r, worth)
	if len(r.Pad) > 0 {
		c.Subj, c.HasSubj = r.Pad[len(r.Pad)-1], true
	}
	k.act(c, "split", fmt.Sprintf("from run %d at %s worth %.3g", r.ID, k.show(gv(at)), worth))
	k.pass(c, 0)
}

func (k *K) end(r *Run) {
	for i, x := range k.runs {
		if x == r {
			k.runs = append(k.runs[:i], k.runs[i+1:]...)
			break
		}
	}
	if r.Parent != nil && r.PGen == r.Parent.Gen {
		r.Parent.Kids--
	}
	if m := k.M[r.Mem]; m != nil && !m.HasSig && r.Parent == nil {
		// a run that wrote rows and ended without writing its memory: file what it did
		sig := k.sigOf(r)
		if sig == "" {
			sig = fmt.Sprint("@", r.Start) // no input: keyed by where it started, which no input matches
		}
		k.setSig(m, sig, k.shapeOf(r))
		k.setBody(m, gl(r.Trail).L)
		out := gv(k.nm("NONE"))
		if len(r.Pad) > 0 {
			out = r.Pad[len(r.Pad)-1]
		}
		k.setOut(m, out)
	}
	r.Rest, r.Ending, r.Parked = nil, true, true // a dead run is never stepped again
}

// enter starts a told process at a gate the kernel sends the run to.
func (k *K) enter(r *Run, name string, d int) bool {
	g := k.nm(name)
	if g == 0 {
		return false
	}
	r.At, r.From = g, g
	k.pass(r, d)
	return true
}

// step is the whole hop.
func (k *K) step(r *Run) {
	r.Steps++
	if lim := k.value("STUCK"); lim > 0 && float64(r.Steps) > lim && !r.Stuck {
		r.Stuck = true // a watchdog: the run has passed a long step count
		k.push(r, nv(float64(r.Steps)))
		if k.enter(r, "stuck", 1) {
			return
		}
	}
	if len(r.Rest) == 0 {
		k.fire(r)
		if r.Ending {
			k.end(r)
			return
		}
		r.Ending = true
		e := map[bool]string{false: "end-of-run", true: "land-end"}[r.Child]
		if !k.enter(r, e, 1) {
			k.end(r)
		}
		return
	}
	h := &r.Rest[0]
	if h.G < 0 {
		// a word goes in as the gate its label points to; when several gates share it,
		// which one it means is the told which-head's to pick, not the kernel's
		if gs := k.labelGates(h.T); len(gs) == 1 {
			h.G = gs[0]
		} else if len(gs) > 1 {
			k.push(r, gl(gs))
			k.miss(r, k.nm("which-head"))
			return
		}
	}
	var s *Shard
	if h.G >= 0 {
		s = k.G[r.At].Sh[SK{r.From, h.G}]
	}
	if s == nil {
		k.miss(r, k.G[r.At].Miss)
		return
	}
	it := r.Rest[0]
	r.Rest = r.Rest[1:]
	if it.D == 0 {
		k.fire(r)
		for _, t := range s.Out {
			k.split(r, t.Out, k.perform("split-worth", k.worth(r.At, t), r.Worth))
		}
		if g := k.G[s.Next]; g.Phys == "" && g.Proc != nil && len(g.Usual) > 0 {
			r.Pend = s.Next
		}
	}
	if it.O {
		// a branch is a jump: the rest of the test's frame is skipped
		k.skipFrame(r, it.F)
	}
	r.CurD, r.CurF = it.D, it.F
	if it.F != 0 {
		r.From, r.At = it.F, s.Next
	} else {
		r.From, r.At = r.At, s.Next
		r.D0 = append(r.D0, r.At)
	}
	if len(r.Trail) < int(k.value("TRAIL-CAP")) {
		r.Trail = append(r.Trail, r.At)
	}
	k.pass(r, it.D)
}

func (k *K) skipFrame(r *Run, f int64) {
	for f != 0 && len(r.Rest) > 0 && r.Rest[0].F == f {
		r.Rest = r.Rest[1:]
	}
}

// fire: a process gate's own shards are left from inside its frame, so its
// usual triggers fire when the run leaves the frame.
func (k *K) fire(r *Run) {
	if p := r.Pend; p != 0 {
		r.Pend = 0
		for _, t := range k.G[p].Usual {
			k.split(r, t.Out, k.perform("split-worth", t.Worth, r.Worth))
		}
	}
}

// perform: the kernel does a told formula (a process of value gates and math words)
// on numbers, in a scratch run that is never scheduled; the brain can read and rewrite
// the formula. None, or no number left: 0.
func (k *K) perform(name string, ns ...float64) float64 {
	g := k.nm(name)
	if g == 0 || k.G[g].Proc == nil {
		return 0
	}
	r := &Run{At: g, From: g, Made: k.nm("DERIVED"), Slots: map[int64]Val{}}
	for _, n := range ns {
		k.push(r, nv(n))
	}
	for _, x := range k.G[g].Proc {
		r.Rest = append(r.Rest, Item{G: x, D: 1, F: g})
	}
	for i := 0; i < 32 && len(r.Rest) > 0 && !r.Ending; i++ {
		k.step(r)
	}
	n, _ := k.popN(r)
	return n
}

// worth is a trigger's worth as its gate holds it now.
func (k *K) worth(g int64, t Trig) float64 {
	for _, u := range k.G[g].Usual {
		if u.Out == t.Out {
			return u.Worth
		}
	}
	return t.Worth
}

// miss: like an interrupt. The run keeps the miss and goes to the gate's miss process.
// A head with several gates goes the same way, to which-head.
func (k *K) miss(r *Run, m int64) {
	if r.InMiss > 2 || m == 0 || k.gate(m) == nil {
		k.act(r, "fault", "a miss inside the miss way: run ended")
		k.end(r)
		return
	}
	r.Ev, r.Tail = [3]Item{{G: r.At}, {G: r.From}, r.Rest[0]}, len(r.Rest)
	r.InMiss++
	r.At, r.From = m, m
	k.pass(r, r.Rest[0].D)
}

// calls: the kernel sends the run into a told process here (a call, in front of the
// remainder); it is how a choice the kernel doesn't make goes to neuron code.
func (k *K) calls(r *Run, name string) {
	g := k.nm(name)
	need(g != 0 && k.G[g].Proc != nil)
	r.At, r.From = g, g
	k.pass(r, r.CurD)
}

// hand: the candidates (index order) and any context go on the pad, and the told
// process picks. One candidate is no choice.
func (k *K) hand(r *Run, name string, gs []int64, ctx ...Val) {
	need(len(gs) > 0)
	if len(gs) == 1 {
		k.push(r, gv(gs[0]))
		return
	}
	k.push(r, gl(gs))
	r.Pad = append(r.Pad, ctx...)
	k.calls(r, name)
}

func (k *K) value(name string) float64 {
	if g := k.gate(k.nm(name)); g != nil && g.HasVal && k.nm(name) != 0 {
		return g.Val
	}
	return 0
}

// rcpt is the memory that receipts written by this run point to: the memory of
// the run its tree started from, which exists from the tree's first write.
func (k *K) rcpt(r *Run) int64 {
	if r = r.root(); r.Mem == 0 {
		if id, ok := k.sigs[k.sigOf(r)]; ok && len(r.D0) > 0 && k.M[id] != nil && !r.moreInput() {
			r.Mem = id // the memory of this signature (whether it is the same run is end-of-run's to judge)
		} else {
			r.Mem = k.newMem(k.nm("RUN"), r.home(), r.Made, k.now).ID
		}
	}
	return r.Mem
}

// root is the run its tree started from.
func (r *Run) root() *Run {
	for r.Parent != nil {
		r = r.Parent
	}
	return r
}

// moreInput: input items still to be stepped (the signature isn't whole yet)
func (r *Run) moreInput() bool {
	for _, it := range r.Rest {
		if it.D == 0 && it.F == 0 {
			return true
		}
	}
	return false
}

// home is the gate a run's memory belongs to: its first input gate.
func (r *Run) home() int64 {
	if len(r.D0) > 0 {
		return r.D0[0]
	}
	if len(r.Trail) > 0 {
		return r.Trail[0]
	}
	return r.At
}

// state: how a line this run writes is held, read from its mode gate's truth
// section (a told row the brain can rewrite); with none, a guess.
func (k *K) state(r *Run) int64 {
	if g := k.gate(r.Made); g != nil {
		if ss := g.Sect[k.nm("sec-truth")]; len(ss) > 0 && ss[len(ss)-1].V.K == 'g' {
			return ss[len(ss)-1].V.G
		}
	}
	return k.nm("GUESS")
}

func (k *K) sigOf(r *Run) string { return strOf(r.D0) }

// shapeOf is the run's path through its gates' points, coarsened to the
// direction of each move (27 ways), so similar shapes share an index key.
func (k *K) shapeOf(r *Run) string {
	var sb strings.Builder
	for i := 1; i < len(r.D0); i++ {
		a, c := k.G[r.D0[i-1]].P, k.G[r.D0[i]].P
		n := 0
		for j := 0; j < 3; j++ {
			n *= 3
			if d := c[j] - a[j]; d > 1e-9 {
				n++
			} else if d < -1e-9 {
				n += 2
			}
		}
		sb.WriteByte(byte('a' + n))
	}
	return sb.String()
}

func (k *K) tick() {
	k.beat++
	k.now = time.Now().Unix()
	// the brain asked to run on the kernel it built (mind/swap, written by its own port):
	// what it holds is committed and the kernel ends; neuron-start tests the new one
	// (its conscience) and starts whichever passes
	if k.beat%100 == 0 {
		if _, err := os.Stat(filepath.Join(home(), "mind", "swap")); err == nil {
			k.act(nil, "swap", "the brain asked to run on the kernel it built")
			k.commit()
			os.Exit(75)
		}
	}
	budget := int(k.value("BUDGET")) // a told setting; none, no steps
	k.port.drain(k)
	if float64(len(k.runs)) <= k.value("SPARE") && k.nm("sixth") != 0 && k.meta["born"] != "" && !k.sixthLive() {
		// spare capacity (SPARE, a setting the brain can change): the sixth picks its own input
		r := k.newRun(k.nm("sixth"), nil, 1)
		r.Ctx = [6]string{"self", "", fmt.Sprint(k.now), "self", "", "sixth"}
		k.pass(r, 0)
	}
	sort.SliceStable(k.runs, func(i, j int) bool { return k.runs[i].Worth > k.runs[j].Worth })
	for steps, moved := 0, true; steps < budget && moved; {
		moved = false
		for _, r := range append([]*Run(nil), k.runs...) {
			if r.Parked {
				continue
			}
			if r.Waiting {
				if r.Kids > 0 && k.beat <= r.Hold {
					continue
				}
				// WAIT gathers only what the runs split since the last WAIT landed
				k.push(r, Val{K: 'l', L: r.Landed})
				r.Waiting, r.Landed, r.Kids = false, nil, 0
				r.Gen++
			}
			for q := int(k.value("SLICE")); q > 0 && !r.Parked && !r.Waiting && steps < budget; q-- {
				k.step(r)
				steps++
				moved = true
				r.LastStep = k.beat
			}
		}
	}
	// nothing is cut: past PARK runs, a low-worth run waits; only one that has waited
	// PARK-WAIT beats without a step goes to the parked list
	if park := int(k.value("PARK")); park > 0 && len(k.runs) > park {
		wait := int64(k.value("PARK-WAIT"))
		for _, r := range append([]*Run(nil), k.runs[park:]...) {
			if r.LastStep == 0 {
				r.LastStep = k.beat
			}
			if !r.Parked && !r.Waiting && r.Worth < k.runs[0].Worth && k.beat-r.LastStep > wait {
				k.parkRun(r)
			}
		}
	}
	if len(k.ops) > 0 && k.meta["born"] != "" {
		k.setMeta("last_beat", fmt.Sprint(k.now)) // only on a beat that writes anyway
	}
	k.commit()
	k.port.flush()
}

func (k *K) sixthLive() bool {
	for _, r := range k.runs {
		if r.Parent == nil && r.Start == k.nm("sixth") {
			return true
		}
	}
	return false
}

// parkRun: a run that waited too long under load goes through the told park (which
// lists where it was for the sixth) and ends. It is not dropped.
func (k *K) parkRun(r *Run) {
	if r.Ending {
		return // already on its way out
	}
	k.act(r, "park", k.show(gv(r.At)))
	k.push(r, gv(r.At))
	for i := 0; i < 16 && !r.Parked && (i > 0 || k.enter(r, "park", 1)); i++ {
		k.step(r)
	}
	if !r.Parked {
		k.end(r)
	}
}

func (k *K) show(v Val) string {
	switch v.K {
	case 'g':
		if l, ok := k.labelOf(v.G); ok {
			return fmt.Sprintf("%s#%d", l, v.G)
		}
		return k.rnames[v.G] + fmt.Sprintf("#%d", v.G)
	case 'n':
		return fmt.Sprint(v.N)
	case 'p':
		return fmt.Sprintf("(%.3g,%.3g,%.3g)", v.P[0], v.P[1], v.P[2])
	case 'l':
		s := make([]string, len(v.L))
		for i, x := range v.L {
			s[i] = k.show(x)
		}
		return "[" + strings.Join(s, " ") + "]"
	}
	return fmt.Sprintf("%q", v.T)
}

func (k *K) act(r *Run, what, detail string) {
	id := int64(0)
	if r != nil {
		id = r.ID
	}
	k.port.log(fmt.Sprintf("%s run %d %s %s", time.Now().Format("15:04:05"), id, what, detail), int64(k.value("ACTS-CAP")))
}

// guard: the kernel refuses every write to a core value.
func (k *K) guard(r *Run, g int64, what string) bool {
	if gt := k.gate(g); gt != nil && gt.Core {
		k.act(r, "refused", what+" on a core value")
		return false
	}
	return true
}

// pmath is the silicon's arithmetic on numbers and points: p±p, p·n, p/n, p·p = dot.
func pmath(op string, a, b Val) Val {
	f := map[string]func(x, y float64) float64{
		"ADD": func(x, y float64) float64 { return x + y },
		"SUB": func(x, y float64) float64 { return x - y },
		"MUL": func(x, y float64) float64 { return x * y },
		"DIV": func(x, y float64) float64 { need(y != 0); return x / y },
	}[op]
	if a.K == 'n' && b.K == 'p' {
		a, b = b, a
	}
	switch {
	case a.K == 'n' && b.K == 'n':
		return nv(f(a.N, b.N))
	case a.K == 'p' && b.K == 'p' && op == "MUL":
		return nv(a.P[0]*b.P[0] + a.P[1]*b.P[1] + a.P[2]*b.P[2])
	case a.K == 'p' && b.K == 'p' && op != "DIV":
		return pv([3]float64{f(a.P[0], b.P[0]), f(a.P[1], b.P[1]), f(a.P[2], b.P[2])})
	case a.K == 'p' && b.K == 'n':
		return pv([3]float64{f(a.P[0], b.N), f(a.P[1], b.N), f(a.P[2], b.N)})
	}
	need(false)
	return Val{}
}

func unwrap(v Val) Val {
	if v.K == 'l' && len(v.L) == 1 {
		return v.L[0]
	}
	return v
}

func (k *K) math(r *Run, op string) {
	x := k.any(r)
	if x.K == 'l' && len(x.L) != 1 {
		// one list alone: ADD sums it, MUL multiplies it
		need(len(x.L) > 0 && (op == "ADD" || op == "MUL"))
		acc := x.L[0]
		for _, e := range x.L[1:] {
			acc = pmath(op, acc, e)
		}
		k.push(r, acc)
		return
	}
	x = unwrap(x)
	for i := len(r.Pad) - 1; i >= 0; i-- {
		if y := unwrap(r.Pad[i]); y.K == 'n' || y.K == 'p' {
			r.Pad = append(r.Pad[:i:i], r.Pad[i+1:]...)
			k.push(r, pmath(op, y, x))
			return
		}
	}
	k.push(r, x)
	need(false)
}

func (k *K) compare(r *Run) {
	x, y := unwrap(k.any(r)), unwrap(k.any(r))
	res := "MORE"
	switch {
	case x.K == 'n' && y.K == 'n':
		k.push(r, nv(math.Abs(y.N-x.N)))
		if y.N == x.N {
			res = "SAME"
		} else if y.N < x.N {
			res = "LESS"
		}
	case x.K == 'p' && y.K == 'p':
		d := dist(x.P, y.P)
		k.push(r, nv(d))
		if d < k.cell {
			res = "SAME"
		}
	case x.enc() == y.enc():
		res = "SAME"
	}
	k.outcome(r, res)
}

func (k *K) phys(r *Run, w string) {
	defer func() {
		if e := recover(); e != nil {
			if _, ok := e.(absent); !ok {
				panic(e)
			}
			k.none(r)
		}
	}()
	switch w {
	case "GO":
		// a jump: the rest of this frame is left behind
		t, a := k.g(r), k.g(r)
		k.skipFrame(r, r.CurF)
		r.At, r.From, r.InMiss = t, a, 0
	case "SPLIT":
		k.split(r, k.g(r), k.perform("branch-worth", r.Worth))
	case "LAND":
		if v, ok := k.pop(r, 0); ok && r.Parent != nil && r.PGen == r.Parent.Gen {
			r.Parent.Landed = append(r.Parent.Landed, v)
		}
	case "WAIT":
		// hold until this wave of branch runs ends (a run parked on a port still counts), at most WAITBEATS beats
		r.Waiting, r.Hold = true, k.beat+max(1, int64(k.value("WAITBEATS")))
	case "END":
		k.end(r)
	case "READ":
		k.read(r)
	case "WRITE":
		k.write(r)
	case "SPAWN":
		k.spawn(r)
	case "DELETE":
		k.delete(r)
	case "MOVE":
		k.move(r)
	case "FIND":
		k.find(r)
	case "ADD", "SUB", "MUL", "DIV":
		k.math(r, w)
	case "COMPARE":
		k.compare(r)
	case "CLOCK":
		k.push(r, nv(float64(time.Now().UnixMilli())/1000))
	case "HEAR":
		// text goes through the encoder; a gate is heard as itself (the encoder's output is gates)
		v := k.any(r)
		need(v.K == 't' || v.K == 'g' && k.gate(v.G) != nil)
		if v.K == 'g' {
			// an inner word: stepped in this frame, not input (no signature, no input triggers)
			r.Rest = append([]Item{{G: v.G, D: r.CurD, F: r.CurF}}, r.Rest...)
		} else {
			r.Rest = append(encode(v.T), r.Rest...)
		}
		k.act(r, "hear", trunc(k.show(v), 80))
	case "SAY":
		k.say(r)
	case "CALL":
		k.call(r)
	}
}

func trunc(s string, n int) string {
	if s = strings.Join(strings.Fields(s), " "); len(s) > n {
		return s[:n] + "…"
	}
	return s
}
