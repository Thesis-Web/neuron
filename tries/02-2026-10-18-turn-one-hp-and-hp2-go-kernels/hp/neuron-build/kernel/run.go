package main

// run.go: runs, the step (blueprint 7.2), passing a gate, triggers, the encoder, the beat.

import (
	"encoding/json"
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"
	"time"
	"unicode"
)

// Val is one item on a run's scratch pad or in its remainder.
// K: 'n' number, 'v' coordinate, 'g' gate, 't' text, 'l' list, 'm' mark
type Val struct {
	K byte
	N float64
	V [3]float64
	G int
	S string
	L []Val
}

func num(f float64) Val    { return Val{K: 'n', N: f} }
func gv(g int) Val         { return Val{K: 'g', G: g} }
func tv(s string) Val      { return Val{K: 't', S: s} }
func vec(v [3]float64) Val { return Val{K: 'v', V: v} }
func lst(l []Val) Val      { return Val{K: 'l', L: l} }

func (v Val) String() string {
	switch v.K {
	case 'n':
		return fnum(v.N)
	case 'v':
		return "(" + vstr(v.V) + ")"
	case 'g', 'o':
		return "#" + strconv.Itoa(v.G)
	case 't':
		return strconv.Quote(v.S)
	case 'l':
		var p []string
		for _, x := range v.L {
			p = append(p, x.String())
		}
		return "[" + strings.Join(p, " ") + "]"
	}
	return "|"
}

type Step struct {
	Gate, Arr, Head int
	T               int64
}

// a trail is kept as [gate, arrival, head, time] rows: exact, and a third of the size of named fields
func (st Step) MarshalJSON() ([]byte, error) {
	return []byte(fmt.Sprintf("[%d,%d,%d,%d]", st.Gate, st.Arr, st.Head, st.T)), nil
}

func (st *Step) UnmarshalJSON(b []byte) error {
	var a [4]int64
	if err := json.Unmarshal(b, &a); err != nil {
		return err
	}
	st.Gate, st.Arr, st.Head, st.T = int(a[0]), int(a[1]), int(a[2]), a[3]
	return nil
}

type Run struct {
	Id, At, From int
	Rest, Pad    []Val
	Want         Val
	Trail        []Step
	Parent       *Run
	Worth        float64
	Depth        int
	Who, What    string
	Where, How   string
	When         int64
	Why          int
	Sig, Shape   string
	Mem          int // the memory row this run is (reserved at start)
	Trig         *Trig
	Steps        int
	Ending, Done bool
	WaitBeat     int64
	Children     int
	Inbox        []string
	Input        []Val // a reading run's own input words, taken one at a time by read-word
	Land         []Val
	Pending      int // outstanding CALLs
	Starved      int
	MissDepth    int
	Quiet0       bool // the gate just passed was a test's outcome: leaving it fires no triggers
	Wrote        int
	Quiet        bool
	Landed       bool
	Conn         *conn
}

func (r *Run) push(v Val) { r.Pad = append(r.Pad, v) }
func (r *Run) pop() Val {
	if len(r.Pad) == 0 {
		return Val{K: 'm'}
	}
	v := r.Pad[len(r.Pad)-1]
	r.Pad = r.Pad[:len(r.Pad)-1]
	return v
}
func (r *Run) popN() float64 { return r.pop().N }
func (r *Run) popG() int {
	v := r.pop()
	if v.K == 'g' {
		return v.G
	}
	return -1
}

// Brain is the live brain: store, runs, ports, clock.
type Brain struct {
	s       *Store
	runs    []*Run
	nextRun int
	beatNo  int64
	ports   *Ports
	names   map[string]int
	trace   bool
	dir     string
	born    int64
}

func (b *Brain) now() int64 { return time.Now().UnixMilli() }

func (b *Brain) val(bind string, def float64) float64 {
	if id, ok := b.s.byBind[bind]; ok {
		return b.s.gates[id].Val
	}
	return def
}

// encode splits text at spaces and at symbol keys and looks each piece up in the label index.
// A piece with no label goes in as raw text. No other language work is done.
func (b *Brain) encode(text, lang string) []Val {
	var out []Val
	emit := func(p string) {
		if p == "" {
			return
		}
		p = strings.ToLower(p)
		if g, ok := b.s.label(p, lang); ok {
			out = append(out, gv(g))
		} else {
			out = append(out, tv(p))
		}
	}
	var cur strings.Builder
	for _, c := range text {
		switch {
		case unicode.IsSpace(c):
			emit(cur.String())
			cur.Reset()
		case unicode.IsLetter(c) || unicode.IsDigit(c):
			cur.WriteRune(c)
		default:
			emit(cur.String())
			cur.Reset()
			emit(string(c))
		}
	}
	emit(cur.String())
	return out
}

// decode reads a gate's label; a gate with no label is said by its number.
func (b *Brain) decode(v Val, lang string) string {
	switch v.K {
	case 'g':
		if ls := b.s.glabel[v.G]; len(ls) > 0 {
			return ls[0]
		}
		return "#" + strconv.Itoa(v.G)
	case 'l':
		var p []string
		for _, x := range v.L {
			p = append(p, b.decode(x, lang))
		}
		return strings.Join(p, " ")
	case 't':
		return v.S
	}
	return v.String()
}

func sigOf(rest []Val) string {
	var p []string
	for _, v := range rest {
		if v.K == 'g' {
			p = append(p, strconv.Itoa(v.G))
		} else if v.K == 't' {
			p = append(p, strconv.Quote(v.S))
		}
	}
	return strings.Join(p, ",")
}

// shapeOf is the coarse direction code of the path through the gates' points: one sign per axis per hop.
func (b *Brain) shapeOf(rest []Val) string {
	var sb strings.Builder
	var prev *Gate
	for _, v := range rest {
		if v.K != 'g' {
			continue
		}
		g := b.s.gate(v.G)
		if g == nil {
			continue
		}
		if prev != nil {
			step := b.val("VALUE.shapestep", 0.5)
			for i := 0; i < 3; i++ {
				d := g.P[i] - prev.P[i]
				switch {
				case d > step:
					sb.WriteByte('+')
				case d < -step:
					sb.WriteByte('-')
				default:
					sb.WriteByte('0')
				}
			}
			sb.WriteByte('|')
		}
		prev = g
	}
	return sb.String()
}

// start begins a run at a gate with an input string (already encoded) and the six questions attached.
func (b *Brain) start(at int, rest []Val, who, what, where, how string, why int, parent *Run, trig *Trig, worth float64) *Run {
	r := &Run{Id: b.nextRun, At: at, From: at, Rest: rest, Who: who, What: what, Where: where, How: how, When: b.now(), Why: why, Parent: parent, Trig: trig, Worth: worth}
	b.nextRun++
	if parent != nil {
		r.Depth = parent.Depth + 1
		r.Conn = parent.Conn
		parent.Children++
	}
	r.Sig = sigOf(rest)
	if parent != nil { // a branch run is about its parent's input: its signature says so
		r.Sig = parent.Sig + "?" + strconv.Itoa(at) + ":" + sigOf(rest)
	}
	r.Shape = b.shapeOf(rest)
	if id, ok := b.s.memSig["run\x00"+r.Sig]; ok {
		r.Mem = id
	} else {
		r.Mem = b.s.memNext
		b.s.memNext++
	}
	b.runs = append(b.runs, r)
	return r
}

// split starts a branch run at a trigger's gate, carrying the subject (blueprint 4.3 SPLIT).
func (b *Brain) split(parent *Run, to int, subject Val, trig *Trig, worth float64) *Run {
	var rest []Val
	if subject.K == 't' {
		rest = b.encode(subject.S, "en")
	}
	r := b.start(to, rest, parent.Who, parent.What, parent.Where, parent.How, parent.Why, parent, trig, worth)
	r.From = parent.At
	r.Shape = parent.Shape // a question run is about the run that asked it
	if subject.K == 't' {  // a reading run: its words wait in Input for read-word, so its process runs first
		r.Input, r.Rest = rest, nil
	}
	if subject.K != 't' {
		r.push(subject)
	}
	b.act("SPLIT run=%d -> run=%d at=%d subject=%s worth=%.3f", parent.Id, r.Id, to, subject, worth)
	b.pass(r, to)
	return r
}

// step is one hop: blueprint 7.2, and nothing else.
func (b *Brain) step(r *Run) {
	s := b.s
	r.Steps++
	if len(r.Rest) == 0 {
		if r.Ending || r.Quiet || (r.Where == "self" && r.What == "") { // the sixth's own run is no input: it leaves no memory
			b.end(r)
			return
		}
		r.Ending = true // landings stay queued: the end-of-run process takes what is in hand first, then waits for them
		r.Rest = []Val{gv(s.byBind["PROC.end"])}
	}
	head := r.Rest[0]
	if b.trace {
		b.act("STEP run=%d at=%d from=%d head=%s pad=%s", r.Id, r.At, r.From, head, lst(r.Pad))
	}
	if head.K == 't' { // a word that got its gate since it was encoded
		if g, ok := s.label(head.S, "en"); ok {
			head = gv(g)
			r.Rest[0] = head
		}
	}
	at := s.gate(r.At)
	var sh *Shard
	if head.K == 'g' || head.K == 'o' {
		sh = at.Shards[[2]int{r.From, head.G}]
		if sh == nil {
			sh = at.Shards[[2]int{-1, head.G}]
		}
	}
	if sh == nil {
		// the miss way: the miss process decides
		miss := at.Miss
		if miss < 0 {
			miss = s.byBind["PROC.miss"]
		}
		if r.MissDepth > 8 {
			// physics floor: a miss process that itself misses eight times deep is a fault
			if head.K != 'g' && head.K != 'o' {
				b.act("FAULT run=%d miss inside miss at=%d head=%s", r.Id, at.Id, head)
				b.end(r)
				return
			}
			r.Rest = r.Rest[1:]
			r.From, r.At = at.Id, head.G
			b.pass(r, head.G)
			return
		}
		r.push(gv(at.Id))
		r.push(gv(r.From))
		r.push(gv(at.Id))
		r.push(gv(r.From))
		if head.K == 'o' {
			head.K = 'g'
		}
		r.push(head)
		r.Trail = append(r.Trail, Step{at.Id, r.From, -1, b.now()})
		r.MissDepth++
		r.From, r.At = at.Id, miss
		b.pass(r, miss)
		return
	}
	r.Rest = r.Rest[1:]
	sh.Seen++ // rough counts live in RAM and reach the disk when a run writes its memory
	sh.Last = b.now()
	for _, t := range at.Trigs {
		if r.Quiet || r.Quiet0 {
			break
		}
		if (t.Arr == -1 && t.Head == -1) || (t.Arr == r.From && t.Head == head.G) {
			w := t.Worth * r.Worth
			if w < b.val("VALUE.floor", 0.1) { // too far from the input to ask now; the gap row carries the need
				continue
			}
			subject := gv(at.Id)
			if n := len(r.Pad); n > 0 && r.Pad[n-1].K == 'g' {
				subject = r.Pad[n-1]
			}
			b.split(r, t.To, subject, t, w)
		}
	}
	r.Trail = append(r.Trail, Step{at.Id, r.From, head.G, b.now()})
	r.From, r.At = at.Id, sh.Next
	if r.MissDepth == 0 { // inside the miss way the mark stands: leaving a test's outcome after a miss fires no triggers either
		r.Quiet0 = head.K == 'o' && sh.Next == head.G
	}
	b.pass(r, sh.Next)
}

// pass performs whatever arriving at a gate does.
func (b *Brain) pass(r *Run, id int) {
	g := b.s.gate(id)
	if g == nil {
		return
	}
	switch g.Bind {
	case "":
		r.push(gv(id))
	case "value":
		r.push(num(g.Val))
	case "proc":
		str := make([]Val, 0, len(g.Str)+len(r.Rest))
		for _, x := range g.Str {
			str = append(str, gv(x))
		}
		r.Rest = append(str, r.Rest...)
	case "rel":
		b.reach(r, g)
	default:
		switch {
		case strings.HasPrefix(g.Bind, "PROC."):
			str := make([]Val, 0, len(g.Str)+len(r.Rest))
			for _, x := range g.Str {
				str = append(str, gv(x))
			}
			r.Rest = append(str, r.Rest...)
		case strings.HasPrefix(g.Bind, "VALUE."):
			r.push(num(g.Val))
		case strings.HasPrefix(g.Bind, "outcome."), strings.HasPrefix(g.Bind, "tier."), strings.HasPrefix(g.Bind, "state."), strings.HasPrefix(g.Bind, "fid."), strings.HasPrefix(g.Bind, "kind."), strings.HasPrefix(g.Bind, "PORT."):
			// an outcome or a name in hand: inert when passed; READ.next takes it as data
		default:
			b.physics(r, g)
		}
	}
}

// outcome puts a test's outcome gate at the head of the remainder and on the pad.
func (b *Brain) outcome(r *Run, name string) {
	id := b.s.byBind["outcome."+name]
	r.Rest = append([]Val{{K: 'o', G: id}}, r.Rest...)
}

// end stops a run (END) and lets its parent go on.
func (b *Brain) end(r *Run) {
	if r.Done {
		return
	}
	r.Done = true
	if r.Wrote > 0 && b.s.mems[r.Mem] == nil {
		m := b.s.newMem("run", b.home(r), r.Sig, "derived", r.Mem, b.now())
		m.Id = r.Mem
		b.s.mems[r.Mem], m.Shape = m, r.Shape // no outcome: the run ended itself before its end-of-run
		b.s.memSig["run\x00"+r.Sig] = m.Id
		b.s.addTL(m.First, m.Id)
	}
	if r.Parent != nil {
		r.Parent.Children--
	}
}

// park writes a run or a would-be trigger run to the parked list for the sixth, one row per (gate, subject).
func (b *Brain) park(r *Run, to int, subject Val, worth float64) {
	key := strconv.Itoa(to) + ":" + subject.String()
	t := b.now()
	if id, ok := b.s.memKey["parked\x00"+key]; ok {
		m := b.s.mems[id]
		m.Last, m.Seen = t, m.Seen+1
		b.s.dMem[m] = true
		return
	}
	m := b.s.newMem("parked", to, key, "spawned", r.Mem, t)
	body, _ := json.Marshal(map[string]any{"run": r.Id, "subject": subject.String(), "worth": worth, "who": r.Who, "what": r.What})
	m.Body = string(body)
	m.Outcome = "parked"
	b.s.addTL(t, m.Id)
	b.act("PARK run=%d gate=%d subject=%s worth=%.3f", r.Id, to, subject, worth)
}

// beat: drain the ports, step runs by worth within the budget, fire the sixth on spare capacity, commit.
func (b *Brain) beat() {
	b.beatNo++
	s := b.s
	idle := len(b.runs) == 0 // spare capacity: nothing was live when this beat began
	for _, in := range b.ports.drain() {
		idle = false
		if in.lay != "" {
			b.lay(in.lay, in.name, in.c)
			continue
		}
		why := 0
		if in.c != nil {
			why = in.c.lastMem
		}
		r := b.start(s.byBind["PORT.talk"], b.encode(in.text, "en"), in.who, in.text, "talk", "typed", why, nil, nil, 1.0)
		r.Conn = in.c
		b.act("HEAR run=%d who=%s what=%q", r.Id, in.who, in.text)
	}
	budget := int(b.val("VALUE.budget", 2000))
	limit := int(b.val("VALUE.steplimit", 4000))
	parkAfter := int(b.val("VALUE.parkafter", 30))
	slice := int(b.val("VALUE.slice", 16))
	used := 0
	for used < budget {
		live := b.runnable()
		if len(live) == 0 {
			break
		}
		sort.SliceStable(live, func(i, j int) bool { return live[i].Worth > live[j].Worth })
		progressed := false
		for _, r := range live {
			if used >= budget {
				break
			}
			if r.Starved > parkAfter {
				b.park(r, r.At, lst(r.Pad), r.Worth)
				b.end(r)
				continue
			}
			for i := 0; i < slice && used < budget && !r.Done && b.canStep(r); i++ {
				b.step(r)
				used++
				progressed = true
				if r.Steps > limit {
					b.act("STUCK run=%d steps=%d at=%d", r.Id, r.Steps, r.At)
					b.park(r, r.At, lst(r.Pad), r.Worth)
					b.end(r)
				}
			}
		}
		if !progressed {
			break
		}
	}
	for _, r := range b.runs {
		if !r.Done && !b.canStep(r) && r.Pending == 0 { // a run held for a port's answer is parked, not starving
			r.Starved++
		}
	}
	// drop finished runs
	keep := b.runs[:0]
	for _, r := range b.runs {
		if !r.Done {
			keep = append(keep, r)
		}
	}
	b.runs = keep
	if idle && used < budget && len(b.runs) == 0 { // the sixth runs on a resting beat, once a beat
		if sixth, ok := s.byBind["PROC.sixth"]; ok {
			r := b.start(s.byBind["PORT.self"], []Val{gv(sixth)}, "self", "", "self", "self", 0, nil, nil, 0.5)
			for i := 0; i < slice*4 && !r.Done; i++ {
				b.step(r)
			}
		}
		keep = b.runs[:0]
		for _, r := range b.runs {
			if !r.Done {
				keep = append(keep, r)
			}
		}
		b.runs = keep
	}
	if n := s.commit(); n > 0 {
		b.act("COMMIT rows=%d beat=%d runs=%d", n, b.beatNo, len(b.runs))
	}
}

func (b *Brain) canStep(r *Run) bool {
	if r.Done {
		return false
	}
	if r.Pending > 0 && len(r.Inbox) == 0 {
		return false
	}
	if r.WaitBeat > 0 {
		if r.Children > 0 && r.WaitBeat == b.beatNo {
			return false
		}
		r.WaitBeat = 0
		r.Pad = append(r.Pad, r.Land...)
		r.Land = nil
	}
	return true
}

func (b *Brain) runnable() []*Run {
	var out []*Run
	for _, r := range b.runs {
		if b.canStep(r) {
			out = append(out, r)
		}
	}
	return out
}

func (b *Brain) act(f string, a ...any) {
	b.ports.log(fmt.Sprintf("%s %s", time.Now().Format("15:04:05.000"), fmt.Sprintf(f, a...)))
}

func dist(a, c [3]float64) float64 {
	return math.Sqrt((a[0]-c[0])*(a[0]-c[0]) + (a[1]-c[1])*(a[1]-c[1]) + (a[2]-c[2])*(a[2]-c[2]))
}
