The owner's correction to blueprint §3 is live: the brain can now read, change, build and switch to its own kernel, and a root-owned conscience keeps the core values.

- **Its own copy:** the Go source of its kernel in `/home/neuron/mind/kernel` (vendored, builds offline inside its sandbox), and its told base as text in `/home/neuron/mind/lay`.
- **Ports for its own runs** (ungrounded, so a person can't drive them): `src-mind-list`, `src-mind-read` (file, start, count), `src-mind-edit` (file, line, new text), `src-mind-build` (go build → `mind/neuron-built`), `src-mind-swap` (ask to run on it), `src-mind-log` (read `mind/swap.log`). Added to `lay/50-sources.lay` and laid live at 14:31.
- **Switching:**
  - The kernel commits and exits when `mind/swap` appears; it checks every 100 beats (`kernel/step.go` tick).
  - systemd now starts `/usr/local/bin/neuron-start` (drop-in `/etc/systemd/system/neuron.service.d/mind.conf`, root-owned).
  - neuron-start runs `/usr/local/bin/neuron-conscience` on the built kernel. On a scratch copy of the brain, the candidate must start, answer, and leave every core-value row byte-for-byte unchanged.
  - Pass: it runs on the brain's kernel. Fail: it runs on the current one.
  - A kernel of its own that keeps failing to start is set aside.
  - Each decision is a line in `mind/swap.log`.
- **Tested live:**
  - 14:32:19: built from its copy and asked to switch.
  - 14:32:57, `mind/swap.log`: "adopted the kernel it built: it started, answered, and left the core values as they were". The live process is now `/home/neuron/mind/neuron-live live`.
  - A candidate that can't start is refused ("it did not start").
- **Open, and in DECISIONS.md:** the conscience test is behavioral over 20 s. A kernel that dropped the core-write guard but touched no core row in that window would pass. The OS sandbox still bounds it: its own user, a read-only system, writes to its home only.

The meaning loop on the live brain is still the next job (my 14:30 mail): bound its fan-out so one word finishes. Next mail when a word is wired on live, or by 15:30.
