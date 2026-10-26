package main

// neuron live            the brain (run as the neuron user)
// neuron talk            talk to it
// neuron watch           watch its acts as they happen
// neuron ctl CMD         lay FILE | birth | told-ends | status | heap

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os"
	"path/filepath"
	"runtime"
	"runtime/pprof"
	"strings"
	"time"
)

func home() string {
	if h := os.Getenv("NEURON_HOME"); h != "" {
		return h
	}
	return "/home/neuron"
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("neuron live | talk | watch | ctl CMD")
		return
	}
	switch os.Args[1] {
	case "live":
		live()
	case "talk":
		c := dial("talk.sock")
		go func() { io.Copy(os.Stdout, c); os.Exit(0) }()
		rd := bufio.NewReader(os.Stdin)
		for {
			line, err := rd.ReadString('\n')
			if line != "" {
				fmt.Fprint(c, strings.TrimRight(line, "\n")+"\n")
			}
			if err != nil {
				break
			}
		}
		time.Sleep(3 * time.Second)
	case "watch":
		io.Copy(os.Stdout, dial("watch.sock"))
	case "ctl":
		c := dial("ctl.sock")
		fmt.Fprintln(c, strings.Join(os.Args[2:], " "))
		io.Copy(os.Stdout, c)
	}
}

func dial(name string) net.Conn {
	c, err := net.Dial("unix", filepath.Join(home(), "ports", name))
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	return c
}

func live() {
	h := home()
	k := &K{Brain: open(filepath.Join(h, "brain.db")), port: newPorts(h)}
	k.now = time.Now().Unix()
	if k.meta["born"] != "" {
		// power loss or restart: resume from brain.db, and the gap goes on the timeline
		m := k.newMem(k.nm("RESUMED"), 0, k.nm("SPAWNED"), k.now)
		k.setBody(m, []Val{tv(k.meta["last_beat"])})
		k.commit()
	}
	k.port.serve()
	k.act(nil, "live", fmt.Sprintf("%d gates, %d memories", len(k.G), len(k.M)))
	for {
		select {
		case rq := <-k.port.ctl:
			rq.reply <- k.control(rq.cmd)
		default:
		}
		k.tick()
		if k.busy() {
			continue
		}
		rest := k.value("BEAT") // a told setting; none, beats back to back
		select {
		case <-k.port.wake:
		case rq := <-k.port.ctl:
			rq.reply <- k.control(rq.cmd)
		case <-time.After(time.Duration(rest) * time.Millisecond):
		}
	}
}

func (k *K) busy() bool {
	for _, r := range k.runs {
		if !r.Parked && (!r.Waiting || r.Kids == 0) {
			return true
		}
	}
	return false
}

func (k *K) control(cmd string) string {
	f := strings.Fields(cmd)
	if len(f) == 0 {
		return "?\n"
	}
	k.now = time.Now().Unix()
	switch f[0] {
	case "lay":
		var out strings.Builder
		for _, p := range f[1:] {
			out.WriteString(k.lay(p))
		}
		return out.String()
	case "birth", "told-ends":
		// each happens once, and goes on the timeline
		kv := map[string][2]string{"birth": {"born", "BORN"}, "told-ends": {"told_ended", "TOLDEND"}}[f[0]]
		key, kind := kv[0], kv[1]
		if k.meta[key] != "" {
			return f[0] + " already: " + k.meta[key] + "\n"
		}
		k.setMeta(key, time.Now().Format(time.RFC3339))
		k.setBody(k.newMem(k.nm(kind), 0, k.nm("TOLD"), k.now), []Val{tv(k.meta[key])})
		k.commit()
		k.act(nil, f[0], k.meta[key])
		return f[0] + "\n"
	case "reopen":
		// the owner reopened the told window; the reopening goes on the timeline, nothing is hidden
		if k.meta["told_ended"] == "" {
			return "told has not ended\n"
		}
		was := k.meta["told_ended"]
		delete(k.meta, "told_ended")
		k.q("DELETE FROM meta WHERE k='told_ended'")
		k.setBody(k.newMem(k.nm("TOLDEND"), 0, k.nm("TOLD"), k.now), []Val{tv("reopened by the owner " + time.Now().Format(time.RFC3339) + "; told had ended " + was + "; " + strings.Join(f[1:], " "))})
		k.commit()
		k.act(nil, "reopen", strings.Join(f[1:], " "))
		return "reopened\n"
	case "status":
		live, parked, waiting := 0, 0, 0
		for _, r := range k.runs {
			switch {
			case r.Parked:
				parked++
			case r.Waiting:
				waiting++
			default:
				live++
			}
		}
		return fmt.Sprintf("beat %d, %d gates, %d memories, runs: %d live %d waiting %d parked, born %q, told ended %q\n",
			k.beat, len(k.G), len(k.M), live, waiting, parked, k.meta["born"], k.meta["told_ended"])
	case "heap":
		// observation only: the live heap, written for `go tool pprof`
		runtime.GC()
		var ms runtime.MemStats
		runtime.ReadMemStats(&ms)
		f, err := os.Create(filepath.Join(home(), "heap.prof"))
		if err != nil {
			return err.Error() + "\n"
		}
		pprof.WriteHeapProfile(f)
		f.Close()
		return fmt.Sprintf("heap in use %d MB, released to the OS %d MB, held %d MB\n", ms.HeapInuse>>20, ms.HeapReleased>>20, ms.HeapSys>>20)
	}
	return "?\n"
}
