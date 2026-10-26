package main

// ports.go: the talk socket, the lay socket, acts.log, and CALL (programs, files, URLs).
// Ports run on their own goroutines; everything they bring in is queued for the beat.

import (
	"bufio"
	"context"
	"fmt"
	"net"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"sync"
	"time"
)

type conn struct {
	id      int
	c       net.Conn
	who     string
	lastMem int
	mu      sync.Mutex
}

type input struct {
	who, text string
	c         *conn
	lay, name string
}

type answer struct {
	r   *Run
	out string
}

type Ports struct {
	mu       sync.Mutex
	queue    []input
	answers  []answer
	conns    map[int]*conn
	nextId   int
	inflight int
	log      func(string)
	logf     *os.File
}

func openPorts(home string) *Ports {
	p := &Ports{conns: map[int]*conn{}}
	f, err := os.OpenFile(home+"/acts.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	must(err)
	p.logf = f
	p.log = func(line string) {
		p.mu.Lock()
		fmt.Fprintln(f, line)
		p.mu.Unlock()
	}
	os.MkdirAll(home+"/ports", 0750)
	p.listen(home+"/ports/talk", 0666, p.serveTalk)
	p.listen(home+"/ports/lay", 0660, p.serveLay)
	return p
}

func (p *Ports) listen(path string, mode os.FileMode, serve func(net.Conn)) {
	os.Remove(path)
	l, err := net.Listen("unix", path)
	must(err)
	os.Chmod(path, mode)
	go func() {
		for {
			c, err := l.Accept()
			if err != nil {
				continue
			}
			go serve(c)
		}
	}()
}

func (p *Ports) serveTalk(c net.Conn) {
	p.mu.Lock()
	p.nextId++
	cn := &conn{id: p.nextId, c: c, who: "person" + strconv.Itoa(p.nextId)}
	p.conns[cn.id] = cn
	p.mu.Unlock()
	sc := bufio.NewScanner(c)
	sc.Buffer(make([]byte, 1<<16), 1<<20)
	for sc.Scan() {
		line := strings.TrimSpace(sc.Text())
		if line == "" {
			continue
		}
		if strings.HasPrefix(line, "/who ") {
			cn.who = strings.TrimSpace(line[5:])
			continue
		}
		p.mu.Lock()
		p.queue = append(p.queue, input{who: cn.who, text: line, c: cn})
		p.mu.Unlock()
	}
	p.mu.Lock()
	delete(p.conns, cn.id)
	p.mu.Unlock()
	c.Close()
}

// serveLay takes one lay file (or TOLD-ENDS) per connection and answers with the loader's report.
func (p *Ports) serveLay(c net.Conn) {
	defer c.Close()
	rd := bufio.NewReader(c)
	head, err := rd.ReadString('\n')
	if err != nil {
		return
	}
	head = strings.TrimSpace(head)
	var body strings.Builder
	for {
		line, err := rd.ReadString('\n')
		body.WriteString(line)
		if err != nil {
			break
		}
	}
	p.mu.Lock()
	p.nextId++
	cn := &conn{id: p.nextId, c: c, who: "builder"}
	p.conns[cn.id] = cn
	p.queue = append(p.queue, input{lay: body.String() + " ", name: head, c: cn})
	p.mu.Unlock()
	// wait for the beat to answer, then the beat closes the conn via say
	time.Sleep(20 * time.Second)
	p.mu.Lock()
	delete(p.conns, cn.id)
	p.mu.Unlock()
}

func (p *Ports) pending() bool {
	p.mu.Lock()
	defer p.mu.Unlock()
	return len(p.queue) > 0 || len(p.answers) > 0
}

func (p *Ports) calling() bool {
	p.mu.Lock()
	defer p.mu.Unlock()
	return p.inflight > 0
}

func (p *Ports) drain() []input {
	p.mu.Lock()
	q := p.queue
	p.queue = nil
	a := p.answers
	p.answers = nil
	p.mu.Unlock()
	for _, x := range a {
		x.r.Inbox = append(x.r.Inbox, x.out)
		x.r.Pending--
	}
	return q
}

// say puts a line out on the talk port: to the run's own connection, or to every talk connection.
func (p *Ports) say(c *conn, line string) {
	p.mu.Lock()
	defer p.mu.Unlock()
	if c != nil {
		c.mu.Lock()
		fmt.Fprintln(c.c, line)
		c.mu.Unlock()
		return
	}
	for _, cn := range p.conns {
		if cn.who == "builder" {
			continue
		}
		cn.mu.Lock()
		fmt.Fprintln(cn.c, line)
		cn.mu.Unlock()
	}
}

// call runs a source's program with the arguments, without a shell, and queues the output for HEAR.
func (p *Ports) call(r *Run, src *Source, args []string) {
	p.mu.Lock()
	p.inflight++
	p.mu.Unlock()
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
		defer cancel()
		var out []byte
		if len(src.How) > 0 {
			argv := append(append([]string{}, src.How[1:]...), args...)
			cmd := exec.CommandContext(ctx, src.How[0], argv...)
			cmd.Dir = os.Getenv("HOME")
			cmd.WaitDelay = 2 * time.Second // a killed program's children may hold the pipe; do not wait on them
			out, _ = cmd.Output()
		}
		if len(out) > 1<<16 {
			out = out[:1<<16]
		}
		p.mu.Lock()
		p.inflight--
		p.answers = append(p.answers, answer{r, strings.TrimSpace(string(out))})
		p.mu.Unlock()
	}()
}

// ---- clients

func talk(home string) {
	c, err := net.Dial("unix", home+"/ports/talk")
	if err != nil {
		fmt.Println("the brain is not listening:", err)
		os.Exit(1)
	}
	if u := os.Getenv("USER"); u != "" {
		fmt.Fprintf(c, "/who %s\n", u)
	}
	go func() {
		sc := bufio.NewScanner(c)
		for sc.Scan() {
			fmt.Println("  <", sc.Text())
		}
		fmt.Println("(the brain hung up)")
		os.Exit(0)
	}()
	sc := bufio.NewScanner(os.Stdin)
	for sc.Scan() {
		fmt.Fprintln(c, sc.Text())
	}
	time.Sleep(3 * time.Second) // piped use: give the brain a moment to answer before hanging up
}

func watch(home string) {
	f, err := os.Open(home + "/acts.log")
	if err != nil {
		fmt.Println("no acts.log yet:", err)
		os.Exit(1)
	}
	f.Seek(0, 2)
	rd := bufio.NewReader(f)
	for {
		line, err := rd.ReadString('\n')
		if err != nil {
			time.Sleep(200 * time.Millisecond)
			continue
		}
		fmt.Print(line)
	}
}

func sendLay(home, head, body string) {
	c, err := net.Dial("unix", home+"/ports/lay")
	if err != nil {
		fmt.Println("the brain is not listening on the lay port:", err)
		os.Exit(1)
	}
	fmt.Fprintf(c, "%s\n%s", head, body)
	c.(*net.UnixConn).CloseWrite()
	sc := bufio.NewScanner(c)
	for sc.Scan() {
		fmt.Println(sc.Text())
	}
}
