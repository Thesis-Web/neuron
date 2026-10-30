# The kernel measured, 2026-10-30: after the sixty tool lines of LINES-nk.txt on hp (Debian 13, 2 cores)

## stats (the kernel's stats request)

hop_us: the time inside one hop of the kernel (a landing, a hit, an end, a replay), mother's pastes left out. paste_us: the mean time of one text pasted to mother (SQLite). hop_s and paste_s: the totals.

```
{
 "main": {
  "runs": 702,
  "hops": 48664,
  "pending": 0,
  "gates": 261,
  "refused": 1,
  "shards": 1283,
  "hop_us": 0.341,
  "pastes": 405,
  "paste_us": 272.6,
  "hop_s": 0.017,
  "paste_s": 0.11
 },
 "sixth": {
  "runs": 213,
  "hops": 17493,
  "pending": 0,
  "gates": 117,
  "refused": 1,
  "shards": 392,
  "hop_us": 0.297,
  "pastes": 78,
  "paste_us": 235.0,
  "hop_s": 0.005,
  "paste_s": 0.018
 }
}
```

## reads by key and reads that walked a whole region (the scans request)

A keyed read found its rows by gate, run, (run, cell), (gate, before, trigger), symbol, input or id. A scanned read walked the whole region: that is a formula the owner may want to change at the prompt.

```
{'table': 'label', 'keyed': 729, 'scanned': 0}
{'table': 'dna', 'keyed': 19, 'scanned': 0}
{'table': 'run', 'keyed': 10799, 'scanned': 50}
{'table': 'seq', 'keyed': 238, 'scanned': 0}
{'table': 'run_sheet', 'keyed': 2, 'scanned': 47}
{'table': 'run_memory', 'keyed': 74, 'scanned': 0}
{'table': 'hit', 'keyed': 51, 'scanned': 0}
```

## where mother's time went: 434 distinct texts pasted, 0.128 s in all (the profile request)

```
  0.026 s      1 x     25943 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( 185 , 24 , 0 , NULL ) ; INSERT INTO wn.inbox ( run , cell , about , word ) SELECT 185 
  0.020 s      1 x     20279 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( 380 , 24 , 0 , NULL ) ; INSERT INTO wn.inbox ( run , cell , about , word ) SELECT 380 
  0.019 s      1 x     19039 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) VALUES ( 360 , 24 , 0 , NULL ) ; INSERT INTO wn.inbox ( run , cell , about , word ) SELECT 360 
  0.017 s     47 x       369 us   INSERT INTO sixth.asked ( run , cell , returns ) SELECT s.run , s.cell , ( SELECT count ( * ) FROM main.run WHERE kind = 3 AND arrival BETWEEN 7 AND 14 ) FROM 
  0.004 s      1 x      3908 us   INSERT OR IGNORE INTO guess.corpus ( line , word ) SELECT DISTINCT s.run , l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run IN ( SELECT id FROM 
  0.003 s      1 x      2581 us   UPDATE guess.guesses SET incorrect = incorrect + 1 , belief = max ( 0.0 , belief - 0.25 ) WHERE asked_by = CAST ( ( SELECT group_concat ( symbol , '' ) FROM ( 
  0.001 s      1 x      1144 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 116 , 26 , 1 , ( SELECT count ( * ) FROM seq s WHERE s.run = 116 AND EXISTS ( SELECT 1 F
  0.001 s      1 x      1093 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 682 , 26 , 1 , ( SELECT count ( * ) FROM seq s WHERE s.run = 682 AND EXISTS ( SELECT 1 F
  0.001 s      1 x      1036 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 576 , 26 , 1 , ( SELECT count ( * ) FROM seq s WHERE s.run = 576 AND EXISTS ( SELECT 1 F
  0.001 s      1 x      1023 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 617 , 26 , 1 , ( SELECT count ( * ) FROM seq s WHERE s.run = 617 AND EXISTS ( SELECT 1 F
  0.001 s      1 x       968 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 636 , 26 , 1 , ( SELECT count ( * ) FROM seq s WHERE s.run = 636 AND EXISTS ( SELECT 1 F
  0.001 s      1 x       844 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 116 , 27 , 1 , coalesce ( ( SELECT max ( m.run ) FROM run_memory m WHERE m.run < 116 AND
  0.001 s      1 x       782 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 682 , 27 , 1 , coalesce ( ( SELECT max ( m.run ) FROM run_memory m WHERE m.run < 682 AND
  0.001 s      1 x       695 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 617 , 27 , 1 , coalesce ( ( SELECT max ( m.run ) FROM run_memory m WHERE m.run < 617 AND
  0.001 s      1 x       695 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 636 , 27 , 1 , coalesce ( ( SELECT max ( m.run ) FROM run_memory m WHERE m.run < 636 AND
  0.001 s      1 x       694 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 576 , 27 , 1 , coalesce ( ( SELECT max ( m.run ) FROM run_memory m WHERE m.run < 576 AND
  0.001 s      1 x       659 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT 92 , 26 , 1 , ( SELECT count ( * ) FROM seq s WHERE s.run = 92 AND EXISTS ( SELECT 1 FRO
  0.001 s      4 x       159 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , ( SELECT gate FROM seq WHERE run = above AND pos = ( SELECT min ( pos )
  0.001 s      1 x       592 us   INSERT OR IGNORE INTO guess.corpus ( line , word ) SELECT DISTINCT s.run , l.symbol FROM seq s JOIN label l ON l.gate = s.gate WHERE s.run IN ( SELECT id FROM 
  0.001 s      5 x       114 us   INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , 23 , 1 , ( SELECT gate FROM seq WHERE run = above AND pos = ( SELECT min ( pos )
```
