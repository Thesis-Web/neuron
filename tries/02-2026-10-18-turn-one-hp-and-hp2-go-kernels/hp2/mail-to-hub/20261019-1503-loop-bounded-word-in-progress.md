The meaning loop's fan-out is bounded on the live brain and one word is going through it now; no word is wired on live yet, so told ends stays unmarked.

- **Fan-out fixed** (73-meaning, laid live 14:54):
  - one `mean` pass per word in flight (`mn-busy`, 60 s);
  - one spec list per pass (at most 3 candidates), tested one after another;
  - untested candidates dropped after 6 tries.
  - Live acts.log 14:55–14:57: 0 parks, no mn-sense/mn-cand storms, 290 gates spawned in 2 minutes. Before, 14:50–14:55: 74,456 mn-sense, 32,840 mn-cand and 13,303 gates.
  - On a loaded dev brain, parks went from 20,000–30,000 a minute to 0–2.
- **Worth:** a pass started by spec-for ran too low (0.0625) for its tests ever to step. spec-for no longer starts `mean`; the sixth's GAP-NEED pick does (worth 0.5). GAP-NEED is now short: 6 items, all from people's words (`select count(*) from mem where kind=GAP-NEED` → 6 at 14:54).
- **The word in flight: impolite#14627.**
  - `what is impolite ?` at 14:57:47 → "the same rude not polite" (held lines).
  - GAP-NEED memory 277447, picked by the sixth (seen 2).
  - `mn-busy` stamped 14:58:13 (run 505233); `src-specs` = 2 (runs 505234 and 505239).
  - `he was polite , not impolite .` at 14:57:50 gives it a use.
  - Its next pass comes when the sixth re-picks it; PATIENCE·n⁴ makes that about 8 minutes at the second try.
- **dissimilar#3346:** its 14:18 need item expired after 30 minutes, and a fresh `what is dissimilar ?` at 14:54 didn't relist it: its know-this trigger has worn down. Not chased further.
- **Size:** 86,000 gates, mostly from the crawl before 14:54. RSS 1.45 GB at 14:56; the cap is 4 GB.
- **Also live since 14:32:** the brain runs the kernel it built itself (see my 14:35 mail).

Next mail when impolite is held and wired, or with where it stopped, by 15:30.
