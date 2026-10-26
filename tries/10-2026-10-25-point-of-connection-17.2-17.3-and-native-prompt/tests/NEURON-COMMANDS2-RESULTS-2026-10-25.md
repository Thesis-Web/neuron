# Second command results: find, apply, redefine, backpop redone (2026-10-25)
Predictions frozen at 02:53 before any run: NEURON-COMMANDS2-EXPECT-2026-10-25.md (sha256 d04761d1280a...). Told block 17.2, unchanged. Node runs on the page's real brain code, then the page 17.3 in a real browser.

## What the first run showed, and the fixes (taught lines only)
- find: never existed: its teach line failed ("no such table: land_76"). Its formula used the column name output, which the brain reads as the told port OUTPUT, a name with no neuron table. Fix: the column is written m.output. Whether ports become neurons is a told change, yours.
- "update definition : x" cannot fire under the told rules: UPDATE is an SQL verb, and nothing fires after an SQL verb in a line (the words after it are a statement). The command is keyed "redefine : x" instead (my choice of name).
- After a definition was marked wrong, "define : store" was answered from memory with the old definition. redefine now also ends the remembered answers of typed lines that mention the word (kept, no longer current), so the next define runs the long way.
- Unchanged from the first run: apply, backpop and the backpop control.

## The fixed run (node)

| Line | Predicted | Said |
|---|---|---|
| `learn : store` | 8 | 8 |
| `find : memory last` | the memory of "learn : store" = 8 | memory 40: return from find : memory last from mwt /build like reminiscence =  |
| `find memory "store"` | up to 5 memories holding store | memory 36: return from find : memory last from mw /build the store of things learned and retained from an orga |
| `find formula last` | the last formula and its path | backpop: = INSERT INTO formula ( word , run , origin ) SELECT r.b , f.run , 'backpop' FROM relation r JOIN for |
| `find formula "learn:"` | learn: and its path |  |
| `apply : store` | 3 (like shop, outlet, mart) | 6 |
| `find relation store` | those three | store like shop;store like outlet;store like mart;store like shop;store like outlet;store like mart |
| `apply : learn like study` | 1 | 1 |
| `run backpop` | 0 formulas 1 rows | 0 formulas 1 rows |
| `study : cat` | learn: fires: cat's count | 8 |
| `define : store` | WordNet sense 1 (first time); sense 2 (after redefine) | a mercantile establishment for the retail sale of goods or services he bought it at a shop on cape cod syn sho |
| `redefine : store` | marks sense 1 wrong; says sense 2 | keep or lay aside for future use store grain for the winter the bear stores fat for the period of hibernation  |
| `define : store` | WordNet sense 1 (first time); sense 2 (after redefine) | keep or lay aside for future use store grain for the winter the bear stores fat for the period of hibernation  |
| `find definition store` | the memories, the first marked wrong | definition from wn wrong: a mercantile establishment for the retail sale of goods or services he bought it at  |

Control, no backpop: "study : cat" said "study? : cat?": study fired nothing. With backpop it fired learn: through the row backpop laid in study's table.

## In the page (real browser, typed through the prompt)

| Line | Seconds | Said | The page's status |
|---|---|---|---|
| `learn : store` | 73.3 | 8 | the line ran on the page itself in 68.4 s and said "8". 1459 triggers  |
| `find : memory last` | 20.7 | 8 | The line "find : memory last" nests deeper than this browser can follo |
| `find formula "learn:"` | 16.4 |  | the line ran on the page itself in 10.9 s and said "". 1462 triggers i |
| `apply : store` | 21.4 |  | The line "apply : store" nests deeper than this browser can follow eve |
| `find relation store` | 20.5 |  | The line "find relation store" nests deeper than this browser can foll |
| `apply : learn like study` | 20.7 |  | The line "apply : learn like study" nests deeper than this browser can |
| `run backpop` | 19.6 |  | The line "run backpop" nests deeper than this browser can follow even  |
| `study : cat` | 22.4 |  | The line "study : cat" nests deeper than this browser can follow even  |
| `define : store` | 47.4 | a mercantile establishment for the retail sale of goods or services he | the line ran on the page itself in 40.2 s and said "a mercantile estab |
| `redefine : store` | 15.5 | keep or lay aside for future use store grain for the winter the bear s | the line ran on the page itself in 7.0 s and said "keep or lay aside f |
| `define : store` | 11.9 | keep or lay aside for future use store grain for the winter the bear s | the line ran on the page itself in 3.2 s and said "keep or lay aside f |

## The new taught lines
```
find: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':what' , trim ( CASE WHEN substr ( trim ( :after ) , 1 , 1 ) = ':' THEN substr ( trim ( :after ) , 2 ) ELSE :after END ) ) ; INSERT INTO var ( run , name , value ) VALUES ( :run , ':kind' , substr ( :what || char ( 32 ) , 1 , instr ( :what || char ( 32 ) , char ( 32 ) ) - 1 ) ) ; INSERT INTO var ( run , name , value ) VALUES ( :run , ':arg' , replace ( trim ( substr ( :what || char ( 32 ) , instr ( :what || char ( 32 ) , char ( 32 ) ) + 1 ) ) , '"' , '' ) ) ; SELECT CASE :kind WHEN 'memory' THEN ( SELECT group_concat ( 'memory' || char ( 32 ) || m.id || ':' || char ( 32 ) || m.line || char ( 32 ) || '=' || char ( 32 ) || coalesce ( m.output , '' ) , char ( 10 ) ) FROM ( SELECT m.id , m.line , m.output FROM memory m WHERE :arg = 'last' OR ( char ( 32 ) || m.line || char ( 32 ) ) LIKE '%' || char ( 32 ) || :arg || char ( 32 ) || '%' ORDER BY m.id DESC LIMIT CASE WHEN :arg = 'last' THEN 1 ELSE 5 END ) m ) WHEN 'formula' THEN ( SELECT group_concat ( f.word || char ( 32 ) || '=' || char ( 32 ) || substr ( coalesce ( ( SELECT group_concat ( e.word , char ( 32 ) ) FROM receipt r JOIN encoder e ON e.gate = r.gate WHERE r.run = f.run ) , '' ) , 1 , 300 ) , char ( 10 ) ) FROM ( SELECT word , run FROM formula WHERE ended = 0 AND ( :arg = 'last' OR word LIKE '%' || :arg || '%' ) ORDER BY id DESC LIMIT CASE WHEN :arg = 'last' THEN 1 ELSE 5 END ) f ) WHEN 'definition' THEN ( SELECT group_concat ( mark || ':' || char ( 32 ) || substr ( line , instr ( line , '/build' ) + 7 , 120 ) , char ( 10 ) ) FROM ( SELECT m.mark , m.line FROM memory m JOIN run r ON r.id = m.run WHERE r.kind = 'defrow' AND r.subject = :arg AND m.mark LIKE 'definition%' ORDER BY m.id LIMIT 8 ) ) WHEN 'relation' THEN ( SELECT group_concat ( a || char ( 32 ) || rel || char ( 32 ) || b , ';' ) FROM relation WHERE a = :arg OR b = :arg ) WHEN 'place' THEN ( SELECT word || char ( 32 ) || x || ',' || y || ',' || z FROM place WHERE word = :arg AND ended = 0 ORDER BY id DESC LIMIT 1 ) END ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
apply: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':what' , trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) ) ; INSERT INTO var ( run , name , value ) VALUES ( :run , ':a' , substr ( :what || char ( 32 ) , 1 , instr ( :what || char ( 32 ) , char ( 32 ) ) - 1 ) ) ; INSERT INTO var ( run , name , value ) VALUES ( :run , ':rest' , trim ( substr ( :what || char ( 32 ) , instr ( :what || char ( 32 ) , char ( 32 ) ) + 1 ) ) ) ; INSERT INTO relation ( a , rel , b ) SELECT :a , rtrim ( substr ( :rest , 1 , length ( :rest ) - length ( replace ( :rest , rtrim ( :rest , replace ( :rest , char ( 32 ) , '' ) ) , '' ) ) ) ) , replace ( :rest , rtrim ( :rest , replace ( :rest , char ( 32 ) , '' ) ) , '' ) WHERE :rest <> '' AND instr ( :rest , char ( 32 ) ) > 0 ; INSERT INTO relation ( a , rel , b ) SELECT :a , rtrim ( substr ( text , 1 , length ( text ) - length ( replace ( text , rtrim ( text , replace ( text , char ( 32 ) , '' ) ) , '' ) ) ) ) , replace ( text , rtrim ( text , replace ( text , char ( 32 ) , '' ) ) , '' ) FROM definition WHERE word = :a AND src = 'map' AND :rest = '' ; SELECT count ( * ) FROM relation WHERE a = :a ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
redefine: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':x' , trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) ) ; UPDATE memory SET mark = mark || char ( 32 ) || 'wrong' WHERE id = ( SELECT min ( id ) FROM memory WHERE mark LIKE 'definition%' AND mark NOT LIKE '%wrong' AND run IN ( SELECT id FROM run WHERE kind = 'defrow' AND subject = :x ) ) ; UPDATE memory SET ended = 1 WHERE ended = 0 AND direction = 'heard' AND line LIKE '%' || :x || '%' ; SELECT substr ( line , instr ( line , '/build' ) + 7 ) FROM memory WHERE mark LIKE 'definition%' AND mark NOT LIKE '%wrong' AND run IN ( SELECT id FROM run WHERE kind = 'defrow' AND subject = :x ) ORDER BY id LIMIT 1 ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
define: = INSERT INTO var ( run , name , value ) VALUES ( :run , ':x' , trim ( substr ( :after , instr ( :after , ':' ) + 1 ) ) ) ; SELECT substr ( line , instr ( line , '/build' ) + 7 ) FROM memory WHERE mark LIKE 'definition%' AND mark NOT LIKE '%wrong' AND run IN ( SELECT id FROM run WHERE kind = 'defrow' AND subject = :x ) ORDER BY id LIMIT 1 ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
backpop: = INSERT INTO formula ( word , run , origin ) SELECT r.b , f.run , 'backpop' FROM relation r JOIN formula f ON f.word = r.a AND f.ended = 0 WHERE r.rel IN ( 'like' , 'alike' , 'similar' ) AND NOT EXISTS ( SELECT 1 FROM formula g WHERE g.word = r.b AND g.ended = 0 ) ; INSERT INTO formula ( word , run , origin ) SELECT r.a , f.run , 'backpop' FROM relation r JOIN formula f ON f.word = r.b AND f.ended = 0 WHERE r.rel IN ( 'like' , 'alike' , 'similar' ) AND NOT EXISTS ( SELECT 1 FROM formula g WHERE g.word = r.a AND g.ended = 0 ) ; INSERT INTO var ( run , name , value ) VALUES ( :run , ':a' , ( SELECT a FROM relation WHERE rel IN ( 'like' , 'alike' , 'similar' ) ORDER BY id DESC LIMIT 1 ) ) ; INSERT INTO var ( run , name , value ) VALUES ( :run , ':ag' , 'g' || ( SELECT gate FROM encoder WHERE word = :a ) ) ; INSERT INTO bindrow ( gate , arrival , remainder , trig , run ) SELECT ( SELECT gate FROM encoder WHERE word = r.b ) , d.arrival , d.remainder , d.trigger , :run FROM :ag d , relation r WHERE r.a = :a AND r.rel IN ( 'like' , 'alike' , 'similar' ) AND d.trigger IS NOT NULL AND ( SELECT gate FROM encoder WHERE word = r.b ) IS NOT NULL ; SELECT ( SELECT count ( * ) FROM formula WHERE origin = 'backpop' ) || char ( 32 ) || 'formulas' || char ( 32 ) || ( SELECT count ( * ) FROM bindrow WHERE run = :run ) || char ( 32 ) || 'rows' ; INSERT INTO say ( run , text ) VALUES ( :run , :found ) ;
find meaning : -> meaning:
find : -> find:
find memory -> find:
find formula -> find:
find definition -> find:
find relation -> find:
find place -> find:
apply : -> apply:
redefine : -> redefine:
```

## After the fixed run: two more fixes to find (taught line), checked on native SQLite
- find formula "learn:" said nothing in the fixed run: my parse split at the first ":" and the value "learn:" holds one. find now takes a ":" only as the key's. Checked: it returns learn:'s formula and its run.
- find memory "cat" matched cat inside other words (indication, educated). It now matches whole words.
- apply : store wrote 6, not 3, because every store definition is held twice: Webster 1913's definition of store holds the word "source" ("a source from which supplies are drawn"); in its return run the told source formula fired (16.4's rule: a word's own formula fires in definition rows) and asked every source for store again. Measured: map 6 rows, wn 4, mw 4, mwt 12, moby 6, gcide 2 (each twice). Yours to decide whether returned answers may fire formulas.
- find : memory last returns the newest memory row, and a line that sources a new word writes definition memories before find runs, so the newest can be one of those (as in the run), not the line before.

## The page and the native prompt
- In the browser (17.3), as the brain grew, the backpop teach line and every command line that sourced a word never looked up before (find : memory last, apply : store, find relation store, apply : learn like study, run backpop, study : cat) were too deep for the page to follow, even on its own thread, and were put back. learn : store, define : store, redefine : store and define : store ran. Node ran every line.
- NEURON-PROMPT-2026-10-25 (Downloads): neuron_prompt.py runs this brain on native SQLite at full depth, from a prompt; the brain is saved to a .db file and loaded back (checked: a line typed before the save was answered from memory after the load).
