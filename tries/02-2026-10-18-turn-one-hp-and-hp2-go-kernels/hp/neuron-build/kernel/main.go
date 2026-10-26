package main

// main.go: neuron run | talk | watch | lay FILE | told-ends | told-opens

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"time"
)

func main() {
	home := os.Getenv("NEURON_HOME")
	if home == "" {
		home = "/home/neuron"
	}
	if len(os.Args) < 2 {
		fmt.Println("neuron run [laydir] | talk | watch | lay FILE... | told-ends | told-opens")
		return
	}
	switch os.Args[1] {
	case "run":
		dir := ""
		if len(os.Args) > 2 {
			dir = os.Args[2]
		}
		run(home, dir)
	case "talk":
		talk(home)
	case "watch":
		watch(home)
	case "lay":
		for _, f := range os.Args[2:] {
			text, err := os.ReadFile(f)
			if err != nil {
				fmt.Println(err)
				continue
			}
			sendLay(home, filepath.Base(f), string(text))
		}
	case "told-ends":
		sendLay(home, "TOLD-ENDS", "")
	case "told-opens": // a new turn: the owner opens the told base again; the kernel takes lay files until told ends
		sendLay(home, "TOLD-OPENS", "")
	default:
		fmt.Println("neuron run [laydir] | talk | watch | lay FILE... | told-ends | told-opens")
	}
}

// run is life: load the body once, lay the told base at birth, then beat until killed.
func run(home, laydir string) {
	b := &Brain{dir: home, trace: os.Getenv("NEURON_TRACE") != ""}
	b.s = openStore(home + "/brain.db")
	b.ports = openPorts(home)
	b.nextRun = 1
	t := b.now()
	if len(b.s.gates) == 0 {
		if laydir == "" {
			fmt.Println("an empty brain needs a lay directory to be born from")
			os.Exit(1)
		}
		b.layDir(laydir)
		m := b.s.newMem("born", 0, "born", "told", 0, t)
		b.s.setTier(m, "persistent")
		m.Outcome = "born"
		b.s.addTL(t, m.Id)
		b.act("BORN gates=%d", len(b.s.gates))
		b.born = t
	} else {
		var last int64
		if n := len(b.s.tl); n > 0 {
			last = b.s.tl[n-1].T
		}
		m := b.s.newMem("outage", 0, "outage "+strconv.FormatInt(last, 10), "told", 0, t)
		b.s.setTier(m, "persistent")
		m.Outcome, m.Body = "outage", fmt.Sprintf("from %d to %d", last, t)
		b.s.addTL(t, m.Id)
		b.act("RESUME gates=%d gap=%dms", len(b.s.gates), t-last)
		if laydir != "" {
			b.layDir(laydir)
		}
	}
	b.s.commit()
	for {
		start := time.Now()
		b.beat()
		rest := time.Duration(b.val("VALUE.beat", 1000)) * time.Millisecond
		if len(b.runnable()) == 0 && !b.ports.pending() { // nothing can step: rest for the remainder of the beat
			if b.ports.calling() { // a source is being read: look again soon
				rest = 20 * time.Millisecond
			}
			if d := rest - time.Since(start); d > 0 {
				time.Sleep(d)
			}
		}
	}
}
