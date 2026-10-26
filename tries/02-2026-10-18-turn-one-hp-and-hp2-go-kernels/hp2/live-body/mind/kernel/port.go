package main

// The ports: the talk socket, the watch socket, the control socket, and CALL.
// Port goroutines only queue things; the brain itself runs on one loop.

import (
	"bufio"
	"context"
	"fmt"
	"net"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"strings"
	"sync"
	"syscall"
	"time"
	"unicode"
)

type input struct {
	conn      int64
	who, text string
}
type result struct {
	r   *Run
	out string
	ok  bool
}
type ctlReq struct {
	cmd   string
	reply chan string
}

type Ports struct {
	mu       sync.Mutex
	home     string
	in       []input
	res      []result
	conns    map[int64]net.Conn
	why      map[string]int64 // what the brain last did for each person
	who      map[int64]string
	watchers map[net.Conn]bool
	next     int64
	logf     *os.File
	logN     int64 // bytes in acts.log
	ctl      chan ctlReq
	wake     chan bool
	said     map[int64][]string
}

func newPorts(home string) *Ports {
	p := &Ports{home: home, conns: map[int64]net.Conn{}, why: map[string]int64{}, who: map[int64]string{}, watchers: map[net.Conn]bool{},
		ctl: make(chan ctlReq), wake: make(chan bool, 1), said: map[int64][]string{}}
	f, err := os.OpenFile(filepath.Join(home, "acts.log"), os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0640)
	must(err)
	p.logf = f
	if st, err := f.Stat(); err == nil {
		p.logN = st.Size()
	}
	return p
}

func (p *Ports) poke() {
	select {
	case p.wake <- true:
	default:
	}
}

func listen(path string) net.Listener {
	os.Remove(path)
	l, err := net.Listen("unix", path)
	must(err)
	os.Chmod(path, 0660)
	return l
}

func (p *Ports) serve() {
	dir := filepath.Join(p.home, "ports")
	os.MkdirAll(dir, 0770)
	talk, watch, ctl := listen(filepath.Join(dir, "talk.sock")), listen(filepath.Join(dir, "watch.sock")), listen(filepath.Join(dir, "ctl.sock"))
	go accept(talk, p.talk)
	go accept(watch, func(c net.Conn) { p.mu.Lock(); p.watchers[c] = true; p.mu.Unlock() })
	go accept(ctl, func(c net.Conn) {
		defer c.Close()
		line, _ := bufio.NewReader(c).ReadString('\n')
		rq := ctlReq{strings.TrimSpace(line), make(chan string)}
		p.ctl <- rq
		fmt.Fprint(c, <-rq.reply)
	})
}

func accept(l net.Listener, f func(net.Conn)) {
	for {
		c, err := l.Accept()
		if err != nil {
			return
		}
		go f(c)
	}
}

func (p *Ports) talk(c net.Conn) {
	p.mu.Lock()
	p.next++
	id := p.next
	p.conns[id] = c
	p.mu.Unlock()
	// who is the person on the other end of the socket, as the system knows them
	who := peer(c)
	p.mu.Lock()
	p.who[id] = who
	p.mu.Unlock()
	rd := bufio.NewReader(c)
	for {
		line, err := rd.ReadString('\n')
		if err != nil && line == "" {
			break
		}
		if len(line) > 1<<20 {
			p.log(fmt.Sprintf("%s talk line of %d bytes from %s cut to 1 MB", time.Now().Format("15:04:05"), len(line), who), 0)
			line = line[:1<<20] // nothing is dropped unseen; a flood is cut and the cut is logged
		}
		t := strings.TrimSpace(line)
		if strings.HasPrefix(t, "\x01who ") {
			continue // a client's claim of who it is counts for nothing
		}
		if t == "" {
			continue
		}
		p.mu.Lock()
		p.in = append(p.in, input{id, who, t})
		p.mu.Unlock()
		p.poke()
	}
	p.mu.Lock()
	delete(p.conns, id)
	p.mu.Unlock()
	c.Close()
}

// say collects what a beat says to each person; flush sends it as one line.
func peer(c net.Conn) string {
	uc, ok := c.(*net.UnixConn)
	if !ok {
		return "someone"
	}
	raw, err := uc.SyscallConn()
	if err != nil {
		return "someone"
	}
	var cred *syscall.Ucred
	raw.Control(func(fd uintptr) { cred, _ = syscall.GetsockoptUcred(int(fd), syscall.SOL_SOCKET, syscall.SO_PEERCRED) })
	if cred == nil {
		return "someone"
	}
	if u, err := user.LookupId(fmt.Sprint(cred.Uid)); err == nil {
		return u.Username
	}
	return fmt.Sprint("uid ", cred.Uid)
}

func (p *Ports) say(conn int64, s string) { p.said[conn] = append(p.said[conn], s) }

func (p *Ports) flush() {
	p.mu.Lock()
	defer p.mu.Unlock()
	for conn, ws := range p.said {
		if c := p.conns[conn]; c != nil {
			fmt.Fprintln(c, strings.Join(ws, " "))
		}
		delete(p.said, conn)
	}
}

func (p *Ports) setWhy(conn, mem int64) { p.mu.Lock(); p.why[p.who[conn]] = mem; p.mu.Unlock() }

// log: acts.log past most bytes goes to acts.log.1 (one old file kept) and a new one starts
func (p *Ports) log(s string, most int64) {
	p.mu.Lock()
	defer p.mu.Unlock()
	if most > 0 && p.logN > most {
		name := filepath.Join(p.home, "acts.log")
		p.logf.Close()
		os.Rename(name, name+".1")
		f, err := os.OpenFile(name, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0640)
		must(err)
		p.logf, p.logN = f, 0
	}
	n, _ := fmt.Fprintln(p.logf, s)
	p.logN += int64(n)
	for c := range p.watchers {
		c.SetWriteDeadline(time.Now().Add(50 * time.Millisecond))
		if _, err := fmt.Fprintln(c, s); err != nil {
			c.Close()
			delete(p.watchers, c)
		}
	}
}

// call runs a source's command for at most wait seconds, keeping at most cap bytes of its answer.
func (p *Ports) call(r *Run, cmd string, wait float64, cap int) {
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), time.Duration(wait*float64(time.Second)))
		defer cancel()
		c := exec.CommandContext(ctx, "sh", "-c", cmd)
		c.Dir = filepath.Join(p.home, "own")
		out, err := c.Output()
		s := strings.TrimSpace(string(out))
		s = s[:min(len(s), cap)]
		p.mu.Lock()
		p.res = append(p.res, result{r, s, err == nil && strings.TrimSpace(s) != ""})
		p.mu.Unlock()
		p.poke()
	}()
}

// drain turns queued input into runs and hands answers back to parked runs.
func (p *Ports) drain(k *K) {
	p.mu.Lock()
	in, res := p.in, p.res
	p.in, p.res = nil, nil
	p.mu.Unlock()
	for _, x := range res {
		x.r.Parked = false
		if x.ok {
			k.push(x.r, tv(x.out))
		} else {
			k.none(x.r)
		}
		k.act(x.r, "answer", trunc(x.out, 100))
	}
	if k.meta["born"] == "" {
		return
	}
	for _, x := range in {
		h := k.nm("HEAR")
		r := k.newRun(h, nil, 1)
		r.Rest = encode(x.text)
		r.Conn = x.conn
		p.mu.Lock()
		r.Why = p.why[x.who]
		p.mu.Unlock()
		r.Ctx = [6]string{x.who, x.text, fmt.Sprint(k.now), "talk", fmt.Sprint(r.Why), "typed"}
		k.act(r, "in", fmt.Sprintf("%s: %s", x.who, x.text))
	}
}

// encode splits at spaces and at symbol keys. Pieces go in raw; the step
// reaches each one's gate through the label index. No language work.
func encode(s string) []Item {
	var out []Item
	var cur []rune
	flush := func() {
		if len(cur) > 0 {
			out = append(out, Item{G: -1, T: string(cur)})
			cur = cur[:0]
		}
	}
	for _, c := range s {
		switch {
		case unicode.IsSpace(c):
			flush()
		case unicode.IsLetter(c) || unicode.IsDigit(c):
			cur = append(cur, c)
		default:
			flush()
			out = append(out, Item{G: -1, T: string(c)})
		}
	}
	flush()
	return out
}
