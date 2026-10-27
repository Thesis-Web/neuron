# Neuron archive

Everything Neuron that was on the hub (Windows Downloads and the WSL home), on `hp` and on `hp2`, gathered into one tree on 2026-10-26. One copy of each thing. Duplicates were hash-checked and deleted (see `DELETED-DUPLICATES.tsv`). Every file's original path and sha256 is in `MANIFEST.tsv`.

The owner is James. The builders were sessions of Claude (Fable and Opus) and one Codex session (the thesis). Where this archive says "I", it is the Claude session that organized it on 2026-10-26, which is also the session that built and deleted v3 the night before.

## Read in this order

1. `LLM-HANDLER.md`. If you are a model, read this before anything else. It is the record of how every build so far went wrong, in the owner's words and the audits' words.
2. `specs/current/`. What Neuron is. The authority order is in `specs/current/NOTE.md`.
3. `CHANGE-OF-STATE.md`. Every spec and every build, dated, with what it got wrong and what replaced it. The point of it: what was wrong is not forgotten, and it is not mistaken for current.
4. `tries/README.md`, then the `NOTE.md` in any try you need.
5. `prose/`. The owner's own words. They govern over every summary, including the ones in this archive.

## Layout

| Folder | What is in it |
|---|---|
| `specs/current/` | The reference draft (2026-10-23), the thesis (2026-10-15), "What we think we know" rev17, the derived build chain, the owner's own build outline. |
| `specs/superseded/` | Older blueprints and sheets, each with a NOTE saying what replaced it and why. Kept so the mistake is visible, not so it is reused. |
| `prose/` | The owner's words, verbatim: the all-sessions quote file (09-16 to 10-25), the by-topic file, the NOW interview, the 10-23 dictation, the words captured during the old v18 and v1 builds, his worksheet, his sketches. |
| `research/` | Published work behind the ideas, the measured tests of meaning, the dictionary tests, the primes and roots lists, the SQLite long form, the source list, the mechanical-intelligence notes. Things that adjust the spec. |
| `audits/` | Outside reads of a build against the spec: hp and hp2 (10-19), 17.3 forensic (10-25), every version against four tests (10-25), spec against build sheet 2 (10-25). |
| `tries/` | Every build, in order, 00 to 14, and 15, which is not a build but a page on 11's brain. Each folder holds the build's own files, its tests, and a NOTE with the owner's verdict and the audit's verdict. |
| `llm/` | Snapshots of the model-side memory files from the hub, hp and hp2, taken 2026-10-26. The live copies stay where they were. |

## Where things came from

| Source on 2026-10-26 | What was there | Where it went |
|---|---|---|
| hub `C:\Users\AdLibitumVita\Downloads` | 150 Neuron files and folders, 10-13 to 10-26 | everywhere in this tree; the non-Neuron files (Boxstead, LadingDocket, NVIDIA, Display-match, a 3D print) were left in Downloads |
| hub WSL `~/neuron/v1`, `~/neuron/v2`, `~/neuron/v18-saved`, `~/neuron-v1-review.tar.gz`, `~/Downloads/Neuron-Thesis-2026-10-15`, `~/DISK_ALERT_...` | the v1 egg, a leftover mother from the v3 night, the old v18 line, the thesis build | `tries/03`, `tries/14`, `tries/01`, `specs/current` |
| `hp:~/neuron-build`, `hp:/home/neuron`, `hp:~/ndry`, `hp:~/neuron-prompt-2026-10-25`, `hp:~/neuron-v18-2026-10-25`, `hp:~/neuron-egg-test`, `hp:~/neuron-egg3-test`, `/opt/neuron`, `/usr/local/bin/neuron` | the Fable turn-one build and its live brain, 53 dry runs, hp copies of the 10-25 builds | `tries/02/hp`, extras into `tries/10`, `12`, `13`; the 10-25 hp copies that were byte-identical to Downloads were not kept twice |
| `hp2:~/neuron-build`, `hp2:/home/neuron`, `hp2:~/mail-to-hub`, `/usr/local/bin/neuron*`, the systemd unit | the Opus turn-one build, its live brain and the kernel it built itself, the builder's mail | `tries/02/hp2` |
| `~/.claude/projects/*/memory` on hub, hp, hp2 | the model-side memory files | `llm/memory-snapshots-2026-10-26/` (copies; originals left in place) |
| D: | nothing Neuron except an empty scratch ext4 image (`wsl-scratch/neuron-scratch.ext4`, mounted empty at `/mnt/scratch/neuron`) | nothing moved |

Not archived on purpose: the two Merriam-Webster API keys (`keys/mw_collegiate.key`, `keys/mw_thesaurus.key`) that sat in both `neuron-build` folders. The same keys are in `~/webster_keys.md` on the hub. Keys do not belong in a repository.

What was left on hp and hp2 after the sweep is listed at the end of `tries/02-.../NOTE.md`.

## State on 2026-10-26, in one paragraph

No build is alive. v3 (2026-10-26) was deleted at the owner's order the night it was built. The last standing code is build sheet 2 (`tries/13`), which the spec-against-build comparison found contradicts the owner's words on 11 of 21 chain steps; the owner said he would build it himself from here. The versions audit (`audits/NEURON-VERSIONS-AUDIT-2026-10-25.md`) says where to step back to: v1's shape (`tries/03`) plus the two fixes the new v18 core made to it (`tries/11`), and nothing else from any page. The spec is the reference draft plus the owner's corrections of 10-25 and 10-26, which are listed in `CHANGE-OF-STATE.md` and are not yet folded into the draft.

## Git

This folder is a git repository, initialized 2026-10-26 with everything above in the first commit. The point of the history from here on: a change of state is a commit, and an old state stays readable.
