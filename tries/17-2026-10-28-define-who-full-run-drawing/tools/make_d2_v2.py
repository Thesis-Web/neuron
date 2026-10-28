# make_d2_v2.py: a typing aid that writes the D2 drawing of "define : who" from a fresh brain.
# It is a drawing generator, not brain code. Numbers are the drawing's numbers: gates sequential
# in the order laid, shards one sequence through the whole brain (10-20 00:34).
import json, sys, re
SAT = sys.argv[1]; OUT = sys.argv[2]
sat = json.load(open(SAT, encoding='utf-8'))

# ---------------- the encoder: gate numbers ----------------
core = ["heard","said","space","CREATE","TABLE",'"',"(",")",",",";","INTEGER","TEXT","shard","before","trigger","call","spawn",
        "value","definition","source","entry","sense","class","text","example","origin","first_use","synonyms","antonyms","times",
        "first_at","last_at","ended_at","INSERT","INTO","VALUES","SELECT","FROM","WHERE","build","born","hop","write","copy","cut",
        "read","clock","memory","timeline","cell","ask","compile","decide","substitute","formula","say","know","remember","shape","out"]
assert len(core) == 60
enc = {s: i+1 for i, s in enumerate(core)}
def gate(sym):
    """the encoder: a symbol with no gate gets the next number (10-26 03:50)"""
    if sym not in enc: enc[sym] = len(enc) + 1
    return enc[sym]
for s in ["define", ":", "who"]: gate(s)   # 61, 62, 63 in arrival order of the line

shard_n = [100]  # this line's first shard is 101; the core's own shards are 1..100 [drawing's number]
def shard():
    shard_n[0] += 1; return shard_n[0]

L = []  # the d2 lines
def w(s=""): L.append(s)
def q(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
def tip(s): return s.replace('\\','\\\\').replace('"', "'")

# ---------------- header, classes, legend ----------------
w("# define : who  -  the whole run from a fresh brain, drawn 2026-10-28 (v2)")
w("# Every neuron is its own table. Numbers only in the tables: gates as the encoder laid them, shards one sequence.")
w("# The words are in the tool pins (hover the i). [his: date] = the owner's words. [reading] = mine, to strike. [open] = his call.")
w("direction: down")
w("grid-columns: 1")
w("grid-gap: 70")
w("vars: { d2-config: { layout-engine: elk } }")
w("""classes: {
  lane: {style.fill: "#f8fafc"; style.stroke: "#334155"; style.stroke-width: 2; style.border-radius: 8; style.font-size: 26}
  col: {style.fill: "#ffffff"; style.stroke: "#94a3b8"; style.stroke-width: 1; style.border-radius: 6}
  neuron: {shape: sql_table; style.fill: "#93c5fd"; style.stroke: "#eff6ff"; style.stroke-width: 2}
  hit: {shape: sql_table; style.fill: "#bfdbfe"; style.stroke: "#f8fbff"; style.stroke-width: 1}
  newborn: {shape: sql_table; style.fill: "#f9a8d4"; style.stroke: "#fdf2f8"; style.stroke-width: 2}
  defn: {shape: sql_table; style.fill: "#fde047"; style.stroke: "#fefce8"; style.stroke-width: 2}
  mem: {shape: sql_table; style.fill: "#86efac"; style.stroke: "#f0fdf4"; style.stroke-width: 2}
  sheet: {shape: sql_table; style.fill: "#6ee7b7"; style.stroke: "#ecfdf5"; style.stroke-width: 1}
  tl: {shape: sql_table; style.fill: "#c4b5fd"; style.stroke: "#f5f3ff"; style.stroke-width: 2}
  encoder: {shape: sql_table; style.fill: "#cbd5e1"; style.stroke: "#f8fafc"; style.stroke-width: 2}
  mail: {shape: queue; style.fill: "#e0f2fe"; style.stroke: "#0369a1"}
  mother: {shape: hexagon; style.fill: "#fee2e2"; style.stroke: "#991b1b"; style.stroke-width: 2}
  prompt: {shape: document; style.fill: "#fee2e2"; style.stroke: "#991b1b"}
  src: {shape: package; style.fill: "#ffedd5"; style.stroke: "#c2410c"}
  brain: {shape: package; style.fill: "#ede9fe"; style.stroke: "#7c3aed"; style.stroke-width: 2}
  pick: {shape: diamond; style.fill: "#f1f5f9"; style.stroke: "#334155"}
  note: {style.fill: "#fffbeb"; style.stroke: "#d4a72c"; style.font-size: 14}
  open: {style.fill: "#ffe4e6"; style.stroke: "#be123c"; style.font-size: 14}
  hop: {style.stroke: "#1d4ed8"; style.stroke-width: 3}
  trig: {style.stroke: "#ea580c"; style.stroke-dash: 5; style.stroke-width: 2}
  call: {style.stroke: "#15803d"; style.stroke-dash: 2; style.stroke-width: 2}
  spawn: {style.stroke: "#7c3aed"; style.stroke-dash: 8; style.stroke-width: 2}
  jump: {style.stroke: "#0f172a"; style.stroke-width: 4}
  route: {style.stroke: "#991b1b"; style.stroke-width: 3}
  fill: {style.stroke: "#059669"; style.stroke-dash: 2; style.stroke-width: 2}
  readw: {style.stroke: "#64748b"; style.stroke-dash: 1; style.stroke-width: 1}
  not: {style.stroke: "#94a3b8"; style.stroke-dash: 3; style.stroke-width: 1; style.opacity: 0.6}
}""")

w("""legend: "KEY" {
  class: lane
  grid-columns: 6
  k_neuron: "NEURON = its own table (61 · define)" {class: neuron; shard: "before > trigger | call | spawn"; tooltip: "A neuron is its own table; its name is its gate (10-19 21:14). Rows are its DNA: his sketch 10-28 gives the columns shard id | before | trigger | call | spawn. The run arrives from before, goes on to trigger, calls side runs that return, spawns runs that leave."}
  k_hit: "one HIT of a gate in a run (the neuron drawn where it is hit)" {class: hit; shard: "before > next"; tooltip: "In a run column every box is one hit of a gate, drawn where the run hits it, as in his sketch (gate 5,6,7 drawn down the column). The row shown is the shard this run hit or wrote."}
  k_newborn: "NEWBORN this line" {class: newborn; tooltip: "A gate that did not exist when the line arrived: born by the born run (10-20 01:22; 10-19 23:40)."}
  k_defn: "DEFINITION NODE (born with the neuron; its first memory)" {class: defn; source: "> return run"; rel: "kind > gate"; tooltip: "10-19 23:40: a new gate, new dna table and new definition node are born at the same time. 10-23 P2: the first birth memory is the definition, pulled from the sources. Its rows: one per source line, and the relationships built from the definition table (10-23 P5-9)."}
  k_mem: "MEMORY NODE on the shard that ended a run (the data sheet inside)" {class: mem; run: "input, source"; cell: "state, value"; tooltip: "10-23 P2 B2: each DNA shard that ends a run will have a memory table for that shard. 10-26 03:50: the data sheet just lives in a cell in the memory row. His v4 brain.db 10-27: run_memory(run, input, source) + run_sheet(run, cell, state, value). A neuron with several shards that end runs has several memory nodes (his words 10-28)."}
  k_tl: "TIMELINE: only a memory table" {class: tl; at: "receipt > memory node, key words"; tooltip: "10-16 06:40: the timeline only gets the receipt number as a pointer, and a couple key words. 10-26 03:50: memory triggers timeline and it just stops because timeline is only a memory table."}
  k_hop: "hop" {style.stroke: "#1d4ed8"; style.stroke-width: 3; tooltip: "The run moves to the remainder's head: before and after; the key is the remainder (§12 law 13). Blue thick wire."}
  k_trig: "trigger" {style.stroke: "#ea580c"; style.stroke-dash: 5; tooltip: "A DNA row excites a run: one, none or many (10-26 05:12). It writes nothing itself; it excites a write, copy or cut run (10-26 03:59). Orange dashed."}
  k_call: "call (returns)" {style.stroke: "#15803d"; style.stroke-dash: 2; tooltip: "A side run whose answer comes back to this run's cell (his sketch: 'call gate 9,8,7' loops back). Green dotted."}
  k_spawn: "spawn (leaves)" {style.stroke: "#7c3aed"; style.stroke-dash: 8; tooltip: "A run that goes off on its own (his sketch: 'spawn gate 5,4,3' leaves). Purple dashed."}
  k_jump: "jump (formula shortcut)" {style.stroke: "#0f172a"; style.stroke-width: 4; tooltip: "Skip the long run: go straight to the formula neuron, plug the value in (10-18 J: 'plug them in and you go to that gate'; his words 10-28: 'skip the long run and use the formula neuron'). Black thick."}
  k_route: "carried by mother" {style.stroke: "#991b1b"; style.stroke-width: 3; tooltip: "Mother routes and traverses, decides nothing, works no data (10-23 P2). Red."}
  k_fill: "a return fills a cell" {style.stroke: "#059669"; style.stroke-dash: 2; tooltip: "10-26 03:50: each return from the graph, from source or from another brain fills its spot on the table. Teal dotted."}
  k_read: "a run reads a table" {style.stroke: "#64748b"; style.stroke-dash: 1; tooltip: "A read run over memory, timeline or definition nodes (standing questions, inspection). Grey dotted."}
  k_not: "not taken on this line" {style.stroke: "#94a3b8"; style.stroke-dash: 3; tooltip: "A path his words describe that this line does not take."}
  k_open: "OPEN: his call" {class: open; tooltip: "What his words leave to him. Listed in the last lane; not filled in."}
}""")

# ---------------- lane 0: the fresh core ----------------
w('core: "0 · THE FRESH BRAIN: what is hand laid (his outline 10-25 21:50; v1 10-19)" {')
w('  class: lane')
w('  grid-columns: 4')
w('  grid-gap: 40')
# encoder table: all 60 core gates
w('  encoder: "ENCODER (the only place a symbol\'s spelling lives)" {')
w('    class: encoder')
w('    tooltip: ' + q(tip("10-26 03:50: 'its a straight database conversion table with x,y,z gates in a sequential order, new word new gate #'. 10-25: 'there are no words in the graph... the encoder encodes to the brain'. The brain holds the numbers; the labels here are the encoder's. Numbers 1..60 are this drawing's numbering of the core, in the order laid.")))
for s in core:
    w(f'    g{enc[s]}: {q(s)}')
w('  }')
w('  schemas: "the hand-laid shapes" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w('  schema_mem: "MEMORY TABLE shape (his own hand, ~/neuron/v4/brain.db, 10-27 01:17)" {')
w('    class: mem')
w('    tooltip: ' + q(tip("CREATE TABLE run_memory (run INTEGER PRIMARY KEY, input TEXT NOT NULL, source TEXT NOT NULL); CREATE TABLE run_sheet (run REFERENCES run_memory(run), cell INTEGER, state INTEGER DEFAULT 0 CHECK(state IN (0,1)), value TEXT, PRIMARY KEY(run,cell)). His own typing, 10-27 01:17. The sheet lives inside the memory row (10-26 03:50). One such node per shard that ends a run (10-23 P2 B2).")))
w('    run: "INTEGER PK"; input: "the receipt"; source: "who spoke: user, mother, sixth"; cell: "INTEGER"; state: "0 declared, 1 filled"; value: "what the return put there"')
w('  }')
w('  schema_def: "DEFINITION NODE shape (his own hand, sqlite history)" {')
w('    class: defn')
w('    tooltip: ' + q(tip("CREATE TABLE definition (id, neuron, source, entry, sense, class, text, example, origin, first_use, synonyms, antonyms, times, first_at, last_at, ended_at). His own typing. Born with the neuron (10-19 23:40); first memory (10-23 P2); truth shift keeps the old row (10-23 P4: ended_at). Relationships are built from this table and self-populate (10-23 P5-9; P4: opposite, kind of, part, has, plural, past, present, is, same spelling, derived from, used in, prefix, suffix, modifier, mood, rhyming).")))
w('    source: "which source brain answered"; entry: "the headword the source sent"; sense_class: "..."; text: "pointer to the return run (gates)"; synonyms_antonyms: "..."; times_first_last_ended: "truth shift keeps the old row"; rel: "kind > gate (built from the table)"')
w('  }')
w('  schema_tl: "TIMELINE shape" {')
w('    class: tl')
w('    tooltip: ' + q(tip("10-16 06:40: 'the timeline only gets the reciept number as a pointer, and a couple key words'. 10-26 03:50: 'timeline is only a memory table, has no dna table ahead of it'. 10-23 P3 B1: reached 'by a trigger hop. Never a sweep'.")))
w('    id: "INTEGER PK"; at: "the clock neuron\'s reading (47)"; receipt: "run > memory node"; key_words: "a few gates"')
w('  }')
w('  }')
w('  outside: "OUTSIDE THE BRAIN" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w('    grid-columns: 2')
w('    m_user_in: "user > encoder" {class: mail; tooltip: "His outline 10-25 21:50: build the user input mailbox to the encoder. Populated-driven, never a timer (10-22 rev17)."}')
w('    m_mother_in: "mother > encoder (secondary)" {class: mail; tooltip: "His outline: the secondary input mailbox to the encoder from the mother. SQL answers and source answers come back this way (10-24 msg 36)."}')
w('    m_sixth_in: "sixth.db > encoder (third)" {class: mail; tooltip: "His outline: the third input mailbox to the encoder from the sixth.db."}')
w('    m_out: "brain > mother / brain > user (60 out)" {class: mail; tooltip: "His outline: the mailbox output from the brain to the mother and from the brain to the user. Gate 60 is the port neuron the run hits to leave (10-23 msg 1: output to sources is a dna row and trigger to port)."}')
w('    mother: "MOTHER" {class: mother; tooltip: "10-23 P2: the mother is just a router and a traverser. That\'s it... takes the output and traverses it to the sources, or to another brain, or to its own sql... picks up the outputs of whatever it traversed to and brings it back. She works no data. The name is probably wrong."}')
w('    prompt: "THE NEURON PROMPT (the brain\'s own sql prompt)" {class: prompt; tooltip: "10-24 msg 36: that output is given to the mother to route to the sql prompt and paste it in the sql prompt and hit enter, wait for the sql response... when mother is done it returns anything from sql output back to the brain as a secondary input. §2.6 his edit 10-24: a string of sql happens as a run put together by the neurons from the run table and outputed as the string to the mother."}')
for k, name, tt in [("wn","WordNet","holds 1 line for who (the WHO agency), 1 for define"),("gcide","Webster 1913","1 line for who, 1 for define"),("mw","Merriam-Webster","2 lines for who, 2 for define"),("mwt","M-W thesaurus","4 like-lines for define, none for who"),("moby","Moby","3 like-lines for define, none for who"),("map","his relation map","1 like-line for define, none for who"),("sqldoc","SQLite docs","the meaning of the code words to the silicon; nothing for : in this slice")]:
    w(f'    src_{k}: {q(name)} {{class: src; tooltip: {q(tip("A source brain: a database with a corpus, an inbox, an outbox and its own trigger that does its work the moment an ask lands (10-22 rev17). In the archived slice (tries/11 sat172.json, fetched 10-22/10-25): " + tt + ". The brain does not read it: the lines are delivered to the encoder as a run (10-25 msg 37)."))}}}')
w('    sixthdb: "sixth.db" {class: brain; tooltip: "10-25 msg 41: create copy brain.db rename to sixth.db run sqlite sixth.db .. update mother for mailbox to sixth, update mailbox pointer in sixth.db. Empty too, on day one."}')
w('    guessdb: "guessing brain" {class: brain; tooltip: "10-23 P5-9: lookup order memory, then state, then sources, then a guess; guesses announced, never lost. 10-23 03:18: the guessing/invention brain... if that word comes back was wrong from the sixth with reasons why it didn\'t work, then the guessing brain can back prop again over the adjusted corpus and come up with another good guess."}')
w('  }')
w('  notes: "" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w('  core_note: "the core\'s own neurons are gates 1..60 (the encoder table, left).\\nEach is its own table with hand-laid DNA rows and a definition node\\nfed from the SQL docs. Later a core word becomes a row in the real word\'s neuron." {class: note; tooltip: ' + q(tip("10-19 21:20: hand lay a table, then hand lay those same words as nodes so the brain lays its own tables. 10-19 23:03: ( , integer, primary, key... all neurons of their own. 10-23 P2 B3: core words become a row in the DNA of the actual word neuron: create, at certain row, is the core word function. 10-27 05:05: the first core will break the rules... later that should cease to exist when the words and dna and memories, and timeline exist to replace them.")) + '}')
w('  }')
w('}')

# ---------------- lane 1: the line ----------------
w('line: "1 · THE LINE ARRIVES: prompt > encoder > brain (10-25: never a told block between)" {')
w('  class: lane')
w('  typed: "user types   define : who" {shape: page; tooltip: "Lands in the user input mailbox (his outline 10-25 21:50)."}')
w('  enc: "encoder: define > 61 (new)   space > 3   : > 62 (new)   space > 3   who > 63 (new)" {class: encoder; tooltip: ' + q(tip("A symbol with no gate gets the next number; nothing else is figured here (10-26 03:50; 10-23 P2: the encoder never guesses a word or does work). Who is speaking is part of the input: user, heard (10-26 03:50; §2.1).")) + '}')
w('  r1: "input row R1" {class: sheet; run: "1"; gates: "61 3 62 3 63"; arrival: "1 (heard)"; speaker: "user"; clock: "t0 (47)"; tooltip: ' + q(tip("The main run's input row. The clock neuron (47) is hit on every run and its reading goes into the run's meta (10-26 03:50). The remainder is the rest of the line as gate numbers; its head is the key at every gate (10-23 P3).")) + '}')
w('  typed -> enc -> r1')
w('}')

# ---------------- lane 2: standing questions ----------------
w('sq: "2 · STANDING QUESTIONS: three runs that ask before the main run runs (10-23 P3 B2; his sketch 10-28: three columns)" {')
w('  class: lane')
w('  grid-columns: 4')
sq_shards = {}
for g, name, reads, tt in [
  (57, "know", "reads: does a gate exist for 61, 62, 63? do their definition nodes hold rows?", "SQ1 'Do I know anything about this?' (10-23 P3 B2). A read run over the gates of the input and their definition nodes. Fresh brain: 61, 62, 63 have no gate. Answer 0."),
  (58, "remember", "reads: any memory node with a receipt holding 61 3 62 3 63? any timeline row?", "SQ2 'Do I have a memory of this?' (10-23 P3 B2). 10-16: 'have I seen 1+1+1... before, yes on 10/16/26 at 6:15pm the answer was 9... instead of doing the math I just remembered the answer'. Fresh brain: no memory rows. Answer 0."),
  (59, "shape", "reads: timeline receipts with the pattern X 3 62 3 Y? a formula row on gate 61?", "SQ3 'Do I have a shortcut or a formula shortcut?' and his words 10-28: 'does this run shape match another shape I have, so I can know the first formulas to try'. 10-16: 'if no, have I done anything close to that pattern?'. 10-18 J: 'If that gate exists, you go straight to it... plug them in and you go to that gate and you run that run'. Fresh brain: nothing. Answer 0.")]:
    s = shard(); sq_shards[g] = s
    w(f'  q{g}: "{g} · {name}" {{')
    w(f'    class: col; grid-columns: 1; grid-gap: 14')
    w(f'    n: "{g} · {name}" {{class: neuron; s{s}: "1 > - | 46 read | -"; tooltip: {q(tip(tt + " The row: arrived from 1 (heard), spawned from R1’s input row; calls the read run (46); no remainder: the run ends here, so this shard has a memory node."))}}}')
    w(f'    rd: {q(reads)} {{class: note}}')
    w(f'    m: "memory node on {g}.s{s}  (this run)" {{class: mem; run: "{s}"; input: "receipt of the question run"; source: "R1"; c_answer: "0"; tooltip: {q(tip("The question is a run that ends; its memory row sits on the shard that ended it, with its one-cell sheet inside. Its answer is a cell on R1’s sheet (teal wire)."))}}}')
    w(f'    n.s{s} -> rd: {{class: readw}}')
    w(f'    n.s{s} -> m: {{class: trig; label: "no remainder"}}')
    w('  }')
w('  path: "which path" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w('  pick: "all three 0\\n> the long way" {class: pick; tooltip: ' + q(tip("10-23 P3 B2: 'if they all come back no, then we have to go the long way... yes, we know something, yes, we have a shortcut, and yes, we have a formula shortcut, then we go the formula shortcut path. If the belief and the truth part of that shows that we can do the shortcut path and the formula shortcut path correctly. If not, then we still have to hash out the long way.'")) + '}')
w('  short: "shortcut: one hop to the memory" {class: note; tooltip: "Not taken on this line. 10-23 P3 B2."}')
w('  formula_path: "formula shortcut: plug the cells in,\\njump to the formula\'s gate, run it there" {class: note; tooltip: "Not taken on this line (nothing bound to 61 yet). 10-18 J; 10-23 P3 B2."}')
w('  }')
for g in (57,58,59):
    w(f'  q{g}.m -> path.pick: {{class: fill}}')
w('  path.pick -> path.short: {class: not}')
w('  path.pick -> path.formula_path: {class: not}')
w('}')
for g in (57,58,59):
    w(f'line.r1 -> sq.q{g}.n: {{class: spawn}}')

# ---------------- lane 3: the main run ----------------
w('main: "3 · THE MAIN RUN R1, the hallway: 61 > 3 > 62 > 3 > 63 (10-23 P3: it writes nothing but its receipt; the triggers do the rest)" {')
w('  class: lane')
w('  grid-columns: 2')
w('  hall: "the hallway, top to bottom" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
s_main = {}
for key, g, before, trig, tt, cls in [
  ("a", 61, 1, 3, "define, gate 61, born this line. The row s%d: arrived from 1 (heard), goes on to 3 (space). No gate existed: the 'no gate' condition excites the born run (41). Then the write run (43) lays this shard. Its trigger column holds nothing yet: on a fresh brain define is a symbol with no action (10-27 05:37).", "newborn"),
  ("b", 3, 61, 62, "the space, gate 3, a core neuron. Its action ( ) 'is a meaning that we know happens to the graph or the silicon' (10-27 05:37). No row for (61 > 62): the write run lays s%d.", "neuron"),
  ("c", 62, 3, 3, ":, gate 62, born this line. 10-27 05:37: ':' might have an action depending on use; in sql it has an action we know, but a different dna row might not have the same action. On this line it has no action yet. s%d: 3 > 3.", "newborn"),
  ("d", 3, 62, 63, "the space again, the same neuron 3, drawn where it is hit the second time (his sketch). s%d: 62 > 63.", "neuron"),
  ("e", 63, 3, 0, "who, gate 63, born this line. s%d has no remainder: 'the dna shard that has no remainder is what triggers the write of the memories' (10-15 21:50). This shard's memory node holds R1's memory row with the sheet inside. Later rows of who: 'who is, who are, who did and who was each fire a different row inside the one neuron for who' (10-22 rev17).", "newborn")]:
    s = shard(); s_main[key] = s
    trig_s = "-" if trig == 0 else str(trig)
    lab = {61:"61 · define",3:"3 · space",62:"62 · :",63:"63 · who"}[g]
    w(f'  h{key}: {q(lab)} {{class: {cls}; s{s}: "{before} > {trig_s} | - | {"48 memory" if trig == 0 else "-"}"; tooltip: {q(tip(tt % s))}}}')
w('  }')
w('  hall.ha.s%d -> hall.hb.s%d: {class: hop}' % (s_main["a"], s_main["b"]))
w('  hall.hb.s%d -> hall.hc.s%d: {class: hop}' % (s_main["b"], s_main["c"]))
w('  hall.hc.s%d -> hall.hd.s%d: {class: hop}' % (s_main["c"], s_main["d"]))
w('  hall.hd.s%d -> hall.he.s%d: {class: hop}' % (s_main["d"], s_main["e"]))
w('  receipt: "R1 receipt" {class: sheet; h1: "1 > 61.s%d"; h2: "61 > 3.s%d"; h3: "3 > 62.s%d"; h4: "62 > 3.s%d"; h5: "3 > 63.s%d (end)"; tooltip: %s}' % (s_main["a"], s_main["b"], s_main["c"], s_main["d"], s_main["e"], q(tip("The path of gates and shards the run hit: a pointer to the run, never the run again (10-23 P2). [open] whether the receipt is written by the hop's physics or by a write run (audit 10-25 row 5)."))))
w('  hall.he.s%d -> receipt: {class: readw}' % s_main["e"])
w('}')
w('sq.path.pick -> main.hall.ha: {class: hop; label: "long way"}')

# ---------------- the born run text ----------------
cols_dna = ["shard","before","trigger","call","spawn"]
stmt1 = ["CREATE"," ","TABLE"," ",'"',"value",'"'," ","("," "]
for i, c in enumerate(cols_dna):
    stmt1 += [c," ","INTEGER"]
    if i < len(cols_dna)-1: stmt1 += [" ",","," "]
stmt1 += [" ",")"," ",";"]
cols_def = ["source","entry","sense","class","text","example","origin","first_use","synonyms","antonyms","times","first_at","last_at","ended_at"]
stmt2 = ["CREATE"," ","TABLE"," ",'"',"value"," ","definition",'"'," ","("," "]
for i, c in enumerate(cols_def):
    stmt2 += [c," ","INTEGER" if c in ("times",) else "TEXT"]
    if i < len(cols_def)-1: stmt2 += [" ",","," "]
stmt2 += [" ",")"," ",";"]
def sym_gate(s): return gate("space" if s == " " else s)
def sym_label(s): return "space" if s == " " else s

# ---------------- lane 4: born 61, the long way ----------------
w('born61: "4 · BORN RUN R2 for 61, THE LONG WAY: a run through the SQL-word neurons, one hit per symbol, the value neuron holding the hole (10-19 21:52; 23:03; his words 10-28: \'like 50 neurons gates\')" {')
w('  class: lane')
w('  grid-columns: 4')
# born neuron
sb = shard()
w('  colA: "born, and the write run the hole calls" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
sw = shard()
w(f'  b41: "41 · born" {{class: neuron; s{sb}: "61 > 4 | - | 51 ask"; tooltip: {q(tip("The born run. Excited by the no-gate condition at 61 (10-20 01:22). Its row: arrived from 61, goes on to 4 (CREATE); its spawn column: the ask run (51) for the newborn’s sources (’Every newborn is born with at least some sources’, 10-23 P4). It declares on R1’s sheet the cell gate.61 (empty) and its own sheet: value, text, reply (10-26 03:50: each tripped trigger declares the cells its run will fill)."))}}}')
sw = shard()
w(f'  w43: "43 · write" {{class: neuron; s{sw}: "18 > - | - | -"; tooltip: {q(tip("The write run: a run through the neurons that writes a value into a cell or a row; the trigger excites it, it writes nothing itself (10-26 03:59: ’that is why we have a write run through the neurons... the trigger just triggers that run, often used with the copy run, and cut run’). Here it writes value = 61 into R2’s sheet cell value, both times the hole is hit."))}}}')
w('  }')
def run_column(cid, title, syms, first_before, run_tag, tooltip_first):
    """emit a column of hit boxes for a statement; returns (ids, shards)"""
    w(f'  {cid}: {q(title)} {{')
    w('    class: col; grid-columns: 1; grid-gap: 14')
    ids, shs = [], []
    prev_g = first_before
    for i, s in enumerate(syms):
        g = sym_gate(s); sh = shard()
        nxt = sym_gate(syms[i+1]) if i+1 < len(syms) else 0
        hid = f'h{i}'
        ids.append(hid); shs.append(sh)
        call = "-"; spawn = "-"; extra = ""
        if s == "value":
            call = "43 write"
            extra = " The hole: 'create table (var a)... a table of what ever is sitting at the newest memory at var a' (10-19 23:08). 'a different shard in the value neuron for each new run' (his words 10-28). Its call: the write run (43) writes this run's value, 61, into the run's data sheet cell value; the substitution of the hole with the value happens from the sheet (10-24 msg 36)."
        if s == ";" and i == len(syms)-1:
            pass
        label = f'{g} · {sym_label(s)}'
        cls = "hit"
        tt = f"hit {i+1} of {len(syms)} in run {run_tag}: gate {g} ({sym_label(s)}), shard s{sh}: arrived from {prev_g}, goes on to {nxt if nxt else '40 build'}.{extra}"
        if i == 0: tt = tooltip_first + " " + tt
        w(f'    {hid}: {q(label)} {{class: {cls}; s{sh}: "{prev_g} > {nxt if nxt else "40"} | {call} | {spawn}"; tooltip: {q(tip(tt))}}}')
        if i > 0:
            w(f'    h{i-1}.s{shs[i-1]} -> {hid}.s{sh}: {{class: hop}}')
        prev_g = g
    w('  }')
    return ids, shs
ids1, shs1 = run_column("st1", "statement 1: CREATE TABLE \\\" value \\\" ( shard INTEGER , before INTEGER , trigger INTEGER , call INTEGER , spawn INTEGER ) ;   (%d hits)" % len(stmt1), stmt1, 41, "R2", "First statement of the born run.")
ids2, shs2 = run_column("st2", "statement 2: CREATE TABLE \\\" value definition \\\" ( source TEXT , ... , ended_at TEXT ) ;   (%d hits)" % len(stmt2), stmt2, 10, "R2", "Second statement: the definition node, born with the neuron (10-19 23:40). The columns are his own definition table (sqlite history).")
w(f'  colA.b41.s{sb} -> st1.h0.s{shs1[0]}: {{class: hop}}')
w(f'  st1.h{len(stmt1)-1}.s{shs1[-1]} -> st2.h0.s{shs2[0]}: {{class: hop; label: "; > CREATE"}}')
# value hole -> write run -> sheet
i_val1 = stmt1.index("value"); i_val2 = stmt2.index("value")
w(f'  st1.h{i_val1}.s{shs1[i_val1]} -> colA.w43.s{sw}: {{class: call; label: "call"}}')
w(f'  st2.h{i_val2}.s{shs2[i_val2]} -> colA.w43.s{sw}: {{class: call}}')
# build, mother, prompt, reply, memory node, timeline
s_build2 = shard()
w('  endcol: "the end of R2 and what the first correct long run sets off" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w(f'    b40: "40 · build" {{class: neuron; s{s_build2}: "10 > - | 60 out | 48 memory"; tooltip: {q(tip("The build neuron: ’the last build word was the build neuron... routing information for the mother... build neuron = routing to sql prompt’ (10-26 03:50). Its DNA row, picked by before (10 ;) and remainder (none), is a build row ’because of how the before and remainder are set’, not by counting BUILDs. No remainder: this shard ends R2, so it carries R2’s memory node. The build neuron ends every born run, so it has one memory node per born run (his words 10-28)."))}}}')
w(f'    text: "the product of the run: the two statements as text, hole filled from cell value = 61" {{shape: page; tooltip: {q(tip("10-19 23:03: the statement ’as the product of the run’. 10-24 msg 36: the run data sheet ’then produces the exact code that sql needs to run as output the same way that it forms human sentences... that output is given to the mother to route to the sql prompt’."))}}}')
w(f'    reply: "SQL answers: ok" {{class: sheet; tooltip: {q(tip("The answer comes back through the mother > encoder mailbox as secondary input and fills R2’s cell reply (10-24 msg 36; 10-26 03:50). An error is not an end: ’the brain would problem solve’ (10-27 03:52)."))}}}')
w(f'    m2: "memory node on 40.s{s_build2}  (R2)" {{class: mem; run: "R2"; input: "receipt: 41.s{sb} 4.s{shs1[0]} ... 10.s{shs2[-1]} 40.s{s_build2}"; source: "R1 (no gate at 61)"; c_value: "61"; c_text: "> the product"; c_reply: "ok"; c_exists: "1 (read run 46)"; c_formula: "> receipt with the hole at 18.s{shs1[i_val1]}"; c_backpop: "1"; tooltip: {q(tip("R2’s memory row on the shard that ended it, with its data sheet inside (10-26 03:50; his v4 run_sheet). Cells declared by the triggers that tripped: value (write run), text and reply (build), exists (read run), formula (decide run), backpop (write run)."))}}}')
w(f'    tl2: "timeline row: t1 | R2 > 40.s{s_build2} | 41 61" {{class: tl; tooltip: "One row per run that ends: the clock reading, the receipt pointer, a couple of key words (10-16 06:40)."}}')
w(f'    b40.s{s_build2} -> text')
w(f'    text -> reply: {{class: route; label: "60 out > mother > neuron prompt > SQL > mother > encoder"}}')
w(f'    reply -> m2: {{class: fill; label: "fills reply"}}')
w(f'    m2 -> tl2: {{class: trig; label: "memory > timeline, stops"}}')
# first time correct -> decide formula -> formula neuron row -> back population
s_read = shard(); s_dec = shard(); s_form = shard(); s_bp = shard()
w(f'    r46: "46 · read" {{class: neuron; s{s_read}: "40 > - | 60 out | -"; tooltip: {q(tip("[reading] ’the first time it works, and is correct’ (his words 10-28): ok says it ran; correct is read back: the read run asks the prompt (.schema of 61) through mother and the answer fills cell exists = 1. Which check counts as ’correct’ is his call."))}}}')
w(f'    d53: "53 · decide (formula)" {{class: neuron; s{s_dec}: "46 > 43 | 44 copy | -"; tooltip: {q(tip("His words 10-28: ’the first time it works, and is correct, it triggers a decide formula run that decides what the formula is, then writes it in that runs data sheet’. The decide formula run reads R2’s receipt, marks the hole (the value neuron’s shard 18.s" + str(shs1[i_val1]) + "), and writes the formula into R2’s sheet cell formula: the receipt with the hole. The formula is a pointer to the run, never text (10-23 08:47: ’the row holds pointers to the run through the neurons that makes that’)."))}}}')
w(f'    f55: "55 · formula" {{class: neuron; s{s_form}: "4 > 40 | 43 write, 54 substitute | -"; tooltip: {q(tip("The formula neuron for CREATE TABLE value ( shard INTEGER , before INTEGER , trigger INTEGER , call INTEGER , spawn INTEGER ) (his words 10-28). Its new row s" + str(s_form) + ": arrived from 4 (CREATE arriving from born), goes on to 40 (build); calls the write run (43) and the substitution run (54). The row’s trigger points at R2’s sheet cell formula (the receipt with the hole). [open] one formula neuron with a row per formula, as drawn, or one neuron per formula (10-23 08:47 ’a pointer to the shortcut neuron formula’)."))}}}')
w(f'    bp: "back population: 4.s{shs1[0]} gets  jump > 55.s{s_form}" {{class: note; tooltip: {q(tip("His words 10-28: ’through back population the triggers or calls or jumps or hops from a run create table (value) would have to show the substitution run and the write run writing the value... so that you can then skip the long run and use the formula neuron’. The write run (43) updates the first shard of the long run (CREATE arriving from born) with a jump to the formula row. 10-23 P5-9: back population is the application of a newly understood process to the other things it fits."))}}}')
w(f'    m2 -> r46.s{s_read}: {{class: trig; label: "reply ok"}}')
w(f'    r46.s{s_read} -> d53.s{s_dec}: {{class: trig; label: "exists = 1: first time correct"}}')
w(f'    d53.s{s_dec} -> m2: {{class: fill; label: "writes formula"}}')
w(f'    d53.s{s_dec} -> f55.s{s_form}: {{class: trig; label: "write run lays the formula row"}}')
w(f'    f55.s{s_form} -> bp: {{class: trig}}')
w('  }')
w(f'  st2.h{len(stmt2)-1}.s{shs2[-1]} -> endcol.b40.s{s_build2}: {{class: hop}}')
w(f'  colA.w43.s{sw} -> endcol.m2: {{class: fill; label: "value = 61"}}')
w(f'  endcol.bp -> st1.h0: {{class: jump; label: "jump laid on 4.s{shs1[0]}"}}')
w('}')
w(f'main.hall.ha -> born61.colA.b41: {{class: trig; label: "no gate: born"}}')
w(f'born61.endcol.m2 -> main.hall.ha: {{class: fill; label: "gate.61 = 61; try the run again [open: inline or retry]"}}')

# ---------------- lane 5: born 62 and 63, the shortcut ----------------
w('born_short: "5 · BORN RUNS R4 (62) and R6 (63), THE SHORTCUT: born > CREATE jumps to the formula row; write run writes the value; substitution run plugs it in; build (his words 10-28)" {')
w('  class: lane')
w('  grid-columns: 2')
short_mem = {}
for tag, g, run in [("R4", 62, "R4"), ("R6", 63, "R6")]:
    s_b = shard(); s_c = shard(); s_f = shard(); s_w = shard(); s_sub = shard(); s_cp = shard(); s_bld = shard()
    short_mem[g] = (s_bld, s_b)
    w(f'  {tag}: "{run}: born {g}" {{')
    w('    class: col; grid-columns: 1; grid-gap: 14')
    w(f'    b41: "41 · born" {{class: neuron; s{s_b}: "{g} > 4 | - | 51 ask"; tooltip: "The same born neuron, a new shard for this run: arrived from {g}, goes on to 4 (CREATE); spawns the ask run (51) for the newborn\'s sources."}}')
    w(f'    c4: "4 · CREATE" {{class: hit; s{shs1[0]}: "41 > 3 | - | -   jump > 55.s{s_form}"; tooltip: {q(tip("The same shard 4.s" + str(shs1[0]) + " the long run wrote, now carrying the jump laid by back population: the long run is skipped. 10-08: ’if I know where I am standing I can hop to any point in my brain in one step... all the work was done at learning, not at runtime’."))}}}')
    w(f'    f55: "55 · formula" {{class: neuron; s{s_form}: "4 > 40 | 43 write, 54 substitute | -"; tooltip: "The formula row laid after R2. Calls the write run and the substitution run; goes on to build."}}')
    w(f'    w43: "43 · write" {{class: neuron; s{s_w}: "55 > - | - | -"; tooltip: "The write run writes the value variable, {g}, into {run}\'s sheet cell value (his words 10-28: \'the formula shortcut is just to the data sheet writing the value varible\')."}}')
    w(f'    sub54: "54 · substitute" {{class: neuron; s{s_sub}: "55 > - | 44 copy | -"; tooltip: {q(tip("The substitution run: ’substitution run grabbing that value and plugging it into the run data sheet so a new memory node can be made or a new neuron can be made’ (his words 10-28). Its call: the copy run (44) copies the formula (R2’s sheet cell formula, the receipt with the hole) into this run’s sheet; then the hole is filled with cell value = " + str(g) + ". ’the trigger of the substitution run copying into the substitution run’ (10-28)."))}}}')
    w(f'    cp44: "44 · copy" {{class: neuron; s{s_cp}: "54 > - | - | -"; tooltip: "Copies R2.sheet.formula into {run}\'s sheet cell text (the receipt with the hole)."}}')
    w(f'    b40: "40 · build" {{class: neuron; s{s_bld}: "55 > - | 60 out | 48 memory"; tooltip: "The build neuron again, a new shard for {run}: it ends the run, so it carries another memory node. The build neuron now holds memory nodes for R2, {run}, ... one per born run."}}')
    w(f'    m: "memory node on 40.s{s_bld}  ({run})" {{class: mem; run: "{run}"; input: "receipt: 41.s{s_b} 4.s{shs1[0]} 55.s{s_form} 40.s{s_bld}"; source: "R1 (no gate at {g})"; c_value: "{g}"; c_text: "> R2.formula with {g} in the hole"; c_reply: "ok"; tooltip: "A separate memory node on a separate ending shard of the same neuron 40, with its own sheet inside (his words 10-28)."}}')
    w(f'    tl: "timeline row: t | {run} > 40.s{s_bld} | 41 {g}" {{class: tl}}')
    w(f'    b41.s{s_b} -> c4.s{shs1[0]}: {{class: hop}}')
    w(f'    c4.s{shs1[0]} -> f55.s{s_form}: {{class: jump; label: "jump"}}')
    w(f'    f55.s{s_form} -> w43.s{s_w}: {{class: call}}')
    w(f'    f55.s{s_form} -> sub54.s{s_sub}: {{class: call}}')
    w(f'    sub54.s{s_sub} -> cp44.s{s_cp}: {{class: call}}')
    w(f'    w43.s{s_w} -> m: {{class: fill; label: "value = {g}"}}')
    w(f'    cp44.s{s_cp} -> m: {{class: fill; label: "text"}}')
    w(f'    f55.s{s_form} -> b40.s{s_bld}: {{class: hop}}')
    w(f'    b40.s{s_bld} -> m: {{class: route; label: "60 out > mother > prompt > ok > encoder > reply"}}')
    w(f'    m -> tl: {{class: trig}}')
    w('  }')
w('}')
w('main.hall.hc -> born_short.R4.b41: {class: trig; label: "no gate: born"}')
w('main.hall.he -> born_short.R6.b41: {class: trig; label: "no gate: born"}')
w('born_short.R4.m -> main.hall.hc: {class: fill; label: "gate.62 = 62"}')
w('born_short.R6.m -> main.hall.he: {class: fill; label: "gate.63 = 63"}')

# ---------------- lane 6: sources ----------------
srcs = ["wn","gcide","mw","mwt","moby","map","sqldoc"]
def src_lines(word):
    return {k: [r for r in sat.get(k, []) if r[0] == word] for k in srcs}
w('sources: "6 · SOURCE RUNS R3 (61), R5 (62), R7 (63): the newborn\'s first memory is its definition, pulled from every source and compared (10-23 P5-9; 10-25 msg 51). Each source run has its own sheet; one answer goes back to R1." {')
w('  class: lane')
w('  grid-columns: 3')
expanded_done = False
ret_runs_total = 0
for g, word in [(61,"define"),(62,":"),(63,"who")]:
    lines = src_lines(word)
    s_ask = shard()
    w(f'  src{g}: "source run for {g} · {word}" {{')
    w('    class: col; grid-columns: 1; grid-gap: 14')
    w(f'    a51: "51 · ask" {{class: neuron; s{s_ask}: "41 > 60 | - | -"; tooltip: {q(tip("The ask run, spawned by the born run. Declares its own sheet: one cell per source (wn, gcide, mw, mwt, moby, map, sqldoc) and compile; declares on R1’s sheet the cell def." + str(g) + ". Assembles the ask from the encoder’s label of the newborn and goes on to 60 (out): the brain > mother mailbox. The run names the sources; mother carries the ask to each one’s inbox and decides nothing (10-23 P2; 10-23 01:28 asking the sources is the brain’s decide run)."))}}}')
    rows = []
    for k in srcs:
        n = len(lines[k])
        rows.append(f'c_{k}: "{n} line(s)" ' if n else f'c_{k}: "0: empty"')
    w(f'    sh: "sheet of the source run ({word})" {{class: sheet; ' + '; '.join(rows) + f'; c_compile: "> definition node of {g}"; tooltip: ' + q(tip("The source run's own sheet: a cell per source, filled by each return; when no declared cell is empty the compile runs (10-26 03:50). Counts are the real lines in the archived slice (tries/11 sat172.json).")) + '}')
    w(f'    a51.s{s_ask} -> sh: {{class: readw}}')
    # return runs
    nret = 0
    for k in srcs:
        for j, r in enumerate(lines[k]):
            nret += 1
            words = (r[3] or r[2]).split()
            syms = []
            for t, wd in enumerate(words):
                syms.append(wd)
                if t < len(words)-1: syms.append(" ")
            new = [s for s in words if ("space" if s==" " else s) not in enc]
            # count new before assigning (then assign, since the return run births them in arrival order)
            newcount = len(set(new))
            for s in words: gate(s)
            rid = f'ret_{k}{j}'
            flag = ""
            if k == "wn" and word == "who": flag = " The run checks what came back: 'is this the data I asked for?' WordNet answered with the acronym WHO, the agency, a neighbour of the symbol asked (10-22 rev17: 'Dictionaries answer with neighbours: asked for as, Webster 1913 sends So first'). The cell is filled and the compile keeps it apart."
            tt = (f"Return run {nret} for {word}, from {k}: the source's line, scp'd/sed/cat and delivered to the encoder, arrives as a run of gates: 'return from define : {word} from source {k} run /build the definition as gates' (10-25 msg 37). {len(syms)} hits ({len(words)} symbols and the spaces); {newcount} symbols had no gate and are born on the way (the cascade, 10-23 P4: 'in order to have the definitions, you have to have 500 or 1,000 words that you don't have meanings for'), each by the shortcut now. The run ends at its last symbol: its memory node sits there; the definition node row for {g} points at this receipt. Line: " + (r[2][:220]) + flag)
            if k == "mw" and word == "who" and j == 1 and not expanded_done:
                expanded_done = True
                # expand fully
                w(f'    {rid}: "return run {nret} · {k}, expanded: {len(syms)} hits, {newcount} born" {{')
                w('      class: col; grid-columns: 1; grid-gap: 14')
                prev = 1  # arrives as heard? no: arrives from mother through the encoder; before = 1 heard? secondary input arrival: mother
                prev_g = 60
                hids = []; hsh = []
                for i, s in enumerate(syms):
                    gg = sym_gate(s); sh_ = shard(); hids.append(f'h{i}'); hsh.append(sh_)
                    nxt = sym_gate(syms[i+1]) if i+1 < len(syms) else 0
                    cls = "hit"
                    born_note = ""
                    if s != " " and gg > 63 and s not in ("the","person","or","persons","that","whoever"): pass
                    if s != " " and gg > 63: cls = "newborn"; born_note = f" Gate {gg} had no gate when this run arrived: born by the shortcut (R4-style), sourced in turn (not drawn: the same shape as this lane)."
                    if s == ":": born_note = " Gate 62 already exists from this line: the second shard of ':' is written here, arriving from " + str(prev_g) + " (that) with remainder " + str(nxt) + " (whoever). Two shards, two arrivals: no inspection needed yet (lane 8)."
                    w(f'      {hids[i]}: {q(str(gg) + " · " + sym_label(s))} {{class: {cls}; s{sh_}: "{prev_g} > {nxt if nxt else "-"} | - | {"48 memory" if not nxt else "-"}"; tooltip: {q(tip(f"hit {i+1} of {len(syms)}: gate {gg} ({sym_label(s)}), shard s{sh_}, arrived from {prev_g}." + born_note + (" No remainder: the return run ends here; its memory node on this shard holds the run and is what the definition node row points at." if not nxt else "")))}}}')
                    if i > 0: w(f'      h{i-1}.s{hsh[i-1]} -> {hids[i]}.s{sh_}: {{class: hop}}')
                    prev_g = gg
                last_g = sym_gate(syms[-1])
                w(f'      m: "memory node on {last_g}.s{hsh[-1]}  (return run {nret})" {{class: mem; run: "ret{nret}"; input: "receipt: {" ".join(str(x) for x in hsh)}"; source: "mother ({k})"; tooltip: "The return run ended at its last symbol; its memory row sits there (10-15 21:50). The definition node of 63 points at it."}}')
                w(f'      h{len(syms)-1}.s{hsh[-1]} -> m: {{class: trig}}')
                w('    }')
                w(f'    {rid} -> sh: {{class: fill; label: "fills c_{k}"}}')
            else:
                w(f'    {rid}: "return run {nret} · {k}: {len(syms)} hits, {newcount} born, ends > memory" {{class: hit; tooltip: {q(tip(tt))}}}')
                w(f'    {rid} -> sh: {{class: fill; label: "fills c_{k}"}}')
            w(f'    a51.s{s_ask} -> {rid}: {{class: route' + ('; label: "60 out > mother > each inbox > its trigger > outbox > mother > encoder"' if nret == 1 else '') + '}')
    ret_runs_total += nret
    s_comp = shard()
    if nret:
        w(f'    c52: "52 · compile (diff and similar)" {{class: neuron; s{s_comp}: "50 > 43 | 46 read, 44 copy, 45 cut | -"; tooltip: {q(tip("When no declared cell is empty the larger formula runs: ’I’m going to diff those so that I hopefully can get the most accurate definition of that word. So diff and similar those... And then I’m going to build the word. I’m going to build the definition table, and I’m going to build the relationships from the definition table’ (10-23 P5-9). It reads the return runs (46), copies what agrees (44), cuts what differs (45), and the write run (43) lays the definition node rows: the neuron’s first memory (10-25 msg 51). [open 10-23 P4 B1] ’the diffs are kind of dropped or scattered and the similars are kept. But I don’t know that we’re getting a good, valid definition that way’."))}}}')
        w(f'    sh -> c52.s{s_comp}: {{class: trig; label: "complete"}}')
    else:
        w(f'    empty: "every source cell stays 0: no source has :" {{class: open; tooltip: {q(tip("10-27 03:52: ’just because the cell doesn’t populate it doesn’t end the run, it gives the brain reason to search harder... it would spawn a new run, why did the cell not populate, and the reason would be the output... it chooses what it wants to say’. Lookup order after sources: a guess (10-23 P5-9) > the guessing brain (lane 11). In the archived slice no source holds ’:’ (the measured source holds ; and ( but not :)."))}}}')
        w(f'    sh -> empty: {{class: trig; label: "no cell fills"}}')
    w('  }')
w('}')
w(f'born61.colA.b41 -> sources.src61.a51: {{class: spawn; label: "spawn: sources for the newborn"}}')
w(f'born_short.R4.b41 -> sources.src62.a51: {{class: spawn}}')
w(f'born_short.R6.b41 -> sources.src63.a51: {{class: spawn}}')

# ---------------- lane 7: the neurons after the line: definition nodes, memory nodes ----------------
w('after: "7 · THE THREE NEWBORNS AFTER THE LINE: DNA, definition node with its rows and relationships, memory nodes per ending shard" {')
w('  class: lane')
w('  grid-columns: 3')
# define 61
d61 = src_lines("define")
w('  n61: "61 · define" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w(f'    dna: "61 · define  DNA" {{class: newborn; s{s_main["a"]}: "1 > 3 | - | -"; tooltip: "One row so far: the one R1 wrote. No trigger yet: define has no action until a formula is taught or learned for it (10-25 msg 51: define : dog = look up definition memory, print)."}}')
rows = []
n = 0
for k in srcs:
    for r in d61[k]:
        n += 1
        if r[2].startswith("like "):
            rows.append(f'rel{n}: "like > {gate(r[2][5:].strip())} ({r[2][5:].strip()})"')
        else:
            rows.append(f'def{n}: "{k}: > return run (…{r[2][:28]}…)"')
w('    defn: "definition node of 61" {class: defn; ' + '; '.join(rows) + '; tooltip: ' + q(tip("Rows laid by the compile from the real source lines of the archived slice: wn 1, gcide 1, mw 2 definitions; mwt 4, moby 3, map 1 'like' lines, which are relationship rows: like > the gate of the related symbol (born as they arrive). 10-23 P4: 'any section that can have a relationship to something else is a self-fulfilling relationship section. All of them.'")) + '}')
w('    mem_note: "no memory node yet: no run has ended at 61" {class: note; tooltip: "Memory nodes exist only on shards that end runs (his words 10-28; 10-23 P2 B2)."}')
w('    dna -> defn: {class: readw; label: "born with it"}')
w('  }')
# : 62
w('  n62: "62 · :" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
s2b = s_main["c"]
w(f'    dna: "62 · :  DNA" {{class: newborn; s{s2b}: "3 > 3 | - | -"; s_ret: "68 > 69 | - | -   (from the mw return run)"; tooltip: "Two rows after this line: R1\'s (space > space) and the mw return run\'s (that > whoever). Two arrivals, two rows: the key is before and remainder (§12 law 13). When two rows share one arrival, the call column holds the inspection run (lane 8)."}}')
w('    defn: "definition node of 62" {class: defn; empty: "no rows: no source holds :"; sqldoc: "(the SQL docs would hold its action in code: the hole mark)"; tooltip: ' + q(tip("No source in the archived slice answers for ':'. The cells stay 0 and the run searches harder (10-27 03:52) or asks the guessing brain. 10-27 05:37: in sql ':' has an action we know; on this line it has none yet.")) + '}')
w('    dna -> defn: {class: readw}')
w('  }')
# who 63
d63 = src_lines("who")
w('  n63: "63 · who" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w(f'    dna: "63 · who  DNA" {{class: newborn; s{s_main["e"]}: "3 > - | - | 48 memory"; later1: "(later: who is, who are, who did, who was: a row each)"; tooltip: {q(tip("s" + str(s_main["e"]) + " ends R1. 10-22 rev17: ’Who is, who are, who did and who was each fire a different row inside the one neuron for who, and each row points at a different formula: a different place to look, a different thing to read, a different thing to say.’ 10-24: ’Go get me some coffee now... me who, coffee what... involves 4 questions who, what, when, where that I have to ask myself when I hear or see those words’."))}}}')
rows = []; n = 0
for k in srcs:
    for r in d63[k]:
        n += 1
        extra = " [kept apart: the WHO agency]" if k == "wn" else ""
        rows.append(f'def{n}: "{k}: > return run (…{r[2][:30]}…){extra}"')
rows.append(f'rel1: "? > {gate("whom")} (whom)  named beside who by gcide"')
rows.append(f'rel2: "? > {gate("whoever")} (whoever)  named by mw"')
rows.append(f'rel3: "? > {gate("person")} (person)  named by mw"')
w('    defn: "definition node of 63" {class: defn; ' + '; '.join(rows) + '; tooltip: ' + q(tip("Rows from the real source lines: wn 1 (the WHO agency, kept apart by the check 'is this the data I asked for'), gcide 1, mw 2. The relationship rows: the symbols the definitions name beside who; the KIND of each relationship is not decided here (law 5: no facts from the builder's head); 10-23 P4 lists the kinds the compile builds from (kind of, part, has, plural, past, present, is, same spelling, derived from, used in...).")) + '}')
w(f'    m1: "memory node on 63.s{s_main["e"]}  (R1, the main run)" {{class: mem; run: "1"; input: "61 3 62 3 63 (receipt)"; source: "user"; c_clock: "t0"; c_speaker: "user, heard"; c_q_know: "0"; c_q_remember: "0"; c_q_shape: "0"; c_path: "long"; c_gate_61: "61"; c_def_61: "> definition node of 61"; c_gate_62: "62"; c_def_62: "0: empty, search harder"; c_gate_63: "63"; c_def_63: "> definition node of 63"; c_say: "> what was said (R8)"; tooltip: {q(tip("R1’s memory row, on the shard of who that ended it, with the whole data sheet inside (10-26 03:50: ’the data sheet just lives in a cell in the memory row’; his v4 run_sheet rows). Each cell was declared by the trigger that tripped and filled by a return. A cell still 0 after every return is in is the reason to search harder, never a silent end (10-27 03:52)."))}}}')
w('    m_more: "(another run ending at a different shard of who gets its own memory node here)" {class: note; tooltip: "His words 10-28: some neuron might have many memory tables because many of their dna shards end runs... each will have its own memory table and data runsheet in it."}')
w('    dna -> defn: {class: readw}')
w(f'    dna.s{s_main["e"]} -> m1: {{class: trig; label: "no remainder: 48 memory write run"}}')
w('  }')
w('}')
w('sources.src61.c52 -> after.n61.defn: {class: fill; label: "lays the rows: first memory"}')
w('sources.src63.c52 -> after.n63.defn: {class: fill; label: "lays the rows: first memory"}')
w('sources.src62.empty -> after.n62.defn: {class: not}')
w('after.n61.defn -> after.n63.m1: {class: fill; label: "def.61"}')
w('after.n63.defn -> after.n63.m1: {class: fill; label: "def.63"}')
w('main.hall.he -> after.n63.dna: {class: readw; label: "the same neuron"}')

# ---------------- lane 8: inspection ----------------
w('inspect: "8 · INSPECTION RUN: a row that decides which row to hit (10-23 P2 B1; P3 B1). On this line no gate has two rows for one arrival, so it is not called." {')
w('  class: lane')
w('  grid-columns: 3')
s_i = shard()
w('  i1: "the gate" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w(f'  gate_x: "a gate with two shards for one before" {{class: neuron; sA: "x > y | 46 inspect | -"; sB: "x > z | 46 inspect | -"; tooltip: {q(tip("When the hop’s read by before + remainder head cannot pick one shard, the row’s call column holds the inspection run. 10-23 P2 B1: ’that trigger says, Hey, I need to find the noun, or I need to find the verb and the noun, or I need to see if there’s any adjectives in this sentence, because that determines what row I actually have to hit inside my node. And so that trigger might look to the script and say, Oh, I have this and this and this, and then it might go back to that node and hit a different shard.’"))}}}')
w('  }')
w('  i2: "the call" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w(f'  r46: "46 · read (the inspection run)" {{class: neuron; s{s_i}: "x > x | - | -"; tooltip: {q(tip("The inspection run: 1. reads the main run’s input row: the symbols after this gate and before it (10-20 00:31: ’triggers will later look at the run if we need them to look at other parts of the run’); 2. reads their definition nodes: class, tense, perspective; 3. reads the run’s sheet: speaker, what is known; 4. fills its own small sheet; its answer is the shard to hit; 5. returns to the gate, which hits THAT shard (10-23 P3 B1: ’run a DNA row that actually decides what DNA row that actually needs to get hit in that gate’). 10-23 P2 B2: ’it might be more efficient if the DNA row has that... so that the run table becomes more precise’ [open: an extra column on the row]."))}}}')
w('  sh: "inspection sheet" {class: sheet; c_after: "gates after"; c_before: "gates before"; c_classes: "from their definition nodes"; c_answer: "> the shard to hit"}')
w('  }')
w('  i1.gate_x.sA -> i2.r46: {class: call; label: "call"}')
w('  i2.r46 -> i2.sh: {class: readw}')
w('  i2.sh -> i1.gate_x.sB: {class: call; label: "re-hit that shard"}')
w('}')

# ---------------- lane 9: end, timeline ----------------
w('ending: "9 · THE END OF R1 and the TIMELINE: no remainder > memory > timeline > stop (10-26 03:50)" {')
w('  class: lane')
w('  grid-columns: 3')
s_mw = shard(); s_tw = shard()
w('  writes: "the two write runs" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w(f'  m48: "48 · memory (write run)" {{class: neuron; s{s_mw}: "63 > 49 | 44 copy | -"; tooltip: {q(tip("A copy run the ending shard excites; the trigger writes nothing itself (10-26 03:59). It lays run_memory(1, receipt, user) on 63.s" + str(s_main["e"]) + " and the run_sheet rows inside it. 10-21 18:39: ’if no remainder write to memory node (temporary run data, triggered runs data, and results/outcome data)’."))}}}')
w(f'  t49: "49 · timeline (write run)" {{class: neuron; s{s_tw}: "48 > - | - | -"; tooltip: {q(tip("’spawns its memory, which reaches the timeline by a trigger hop. Never a sweep’ (10-23 P3 B1). One row: the clock reading, the receipt pointer, a couple of key words (10-16 06:40). Then it stops: ’timeline is only a memory table has no dna table ahead of it’ (10-26 03:50)."))}}}')
tl_rows = []
tl_rows.append(f'r1: "t0 | SQ1 > 57.s{sq_shards[57]} | 57"')
tl_rows.append(f'r2: "t0 | SQ2 > 58.s{sq_shards[58]} | 58"')
tl_rows.append(f'r3: "t0 | SQ3 > 59.s{sq_shards[59]} | 59"')
tl_rows.append(f'r4: "t1 | R2 born 61 > 40.s{s_build2} | 41 61"')
tl_rows.append(f'r5: "t2 | R3 sources 61: {sum(len(v) for v in d61.values())} return runs, compile | 51 61"')
tl_rows.append(f'r6: "t3 | R4 born 62 > 40.s{short_mem[62][0]} | 41 62"')
tl_rows.append(f'r7: "t4 | R5 sources 62: 0 returns | 51 62"')
tl_rows.append(f'r8: "t5 | R6 born 63 > 40.s{short_mem[63][0]} | 41 63"')
tl_rows.append(f'r9: "t6 | R7 sources 63: {sum(len(v) for v in d63.values())} return runs, compile | 51 63"')
tl_rows.append(f'r10: "t7 | R1 define : who > 63.s{s_main["e"]} | 61 63"')
tl_rows.append(f'r11: "t8 | R8 say > 56.s | 56"')
w('  }')
w('  timeline: "TIMELINE after this line" {class: tl; ' + '; '.join(tl_rows) + '; tooltip: ' + q(tip("A row per run that ended, in the order the drawing says they happen. 't' is the clock neuron's reading. The pointer is the run's memory node; the key words are a couple of gates. The born runs of the symbols inside the definitions (the cascade) add their own rows, not listed.")) + '}')
w(f'  writes.m48.s{s_mw} -> writes.t49.s{s_tw}: {{class: trig; label: "memory > timeline"}}')
w(f'  writes.t49.s{s_tw} -> timeline: {{class: fill; label: "one row; then stops"}}')
w('}')
w(f'after.n63.m1 -> ending.writes.m48: {{class: readw; label: "the row it lays"}}')

# ---------------- lane 10: output ----------------
w('output: "10 · OUTPUT: a separate mechanism from the same memory table (10-26 03:50): when no declared cell of R1 is empty" {')
w('  class: lane')
w('  grid-columns: 4')
s_say = shard()
w('  o1: "from the memory table" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w('  when: "no declared cell of R1 empty?" {class: pick; tooltip: ' + q(tip("10-26 03:50: 'output is triggered by a completely separate mech from the data sheet... output to timeline and output to user, or output to mother all come from the same memory table... such that when the run's data table is complete the run can populate and finish its larger formulas'. On this line def.62 stays 0: the search-harder run (lane 6) must answer first, or the brain says so in its own words.")) + '}')
w('  formulas: "the larger formulas over the sheet" {class: note; tooltip: ' + q(tip("10-23 P3 B2: substitute the cells as variables into the larger formulas that form the reasoning and the answer. On a fresh brain nothing is bound to define yet; the material is the sheet: the compiled definitions of 61 and 63 and the empty cell of 62.")) + '}')
w('  balance: "makes sense: desired vs current vs new" {class: note; tooltip: ' + q(tip("10-23 P5-9 B1: 'desired equation on one side, current equation which you know is not yet the desired, and your new equation... closer or further away... progressing or digressing'. Not balanced: step back to the decision that picked this path and take another row; the failed try stays in memory marked wrong (10-22 rev17).")) + '}')
w('  }')
w('  o2: "say and out" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w(f'  s56: "56 · say" {{class: neuron; s{s_say}: "48 > 60 | - | -"; tooltip: {q(tip("The say run. 10-26 05:12: ’the only way we have found that a trigger is needed is with a say key’ [open: what the say key is]. The reply is a tree of arrays: the first word’s array, each pick opens the next (10-23 P3 B2; 10-19: ’build choose first word array... does that balance now... ship output’). 10-27 03:52: ’it chooses what it wants to say’. No sentence is drawn here on purpose: ’define? canis? find? is not it choosing what to say’ (10-27 04:07)."))}}}')
w('  dec: "DECODER: gates > symbols" {class: encoder; tooltip: "10-23 P3 B2: What comes out of the decoder? Just numbers. Just gate numbers... maybe head data: perspective, situation, topic."}')
w('  to_user: "brain > user mailbox" {class: mail}')
w('  to_sixth: "> sixth.db mailbox" {class: mail; tooltip: "10-25 msg 41: run output to sixth."}')
w('  }')
w('  o1.when -> o1.formulas -> o1.balance')
w(f'  o1.balance -> o2.s56.s{s_say}: {{label: "balanced"}}')
w('  o1.balance -> o1.formulas: {class: not; label: "digressing: another row"}')
w(f'  o2.s56.s{s_say} -> o2.dec -> o2.to_user')
w(f'  o2.s56.s{s_say} -> o2.to_sixth: {{class: spawn}}')
w('}')
w('ending.timeline -> output.o1.when: {class: trig; label: "the memory row exists"}')
w('after.n63.m1 -> output.o2.s56: {class: fill; label: "say > cell say"}')

# ---------------- lane 11: sixth, guessing ----------------
w('others: "11 · THE SIXTH and THE GUESSING BRAIN" {')
w('  class: lane')
w('  grid-columns: 2')
w('  sixth: "the sixth" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w('    see: "sixth.db reads the brain: the new memory row, the timeline, the newborns, the empty cell def.62" {class: brain; tooltip: ' + q(tip("10-23 P2: 'the me that talks to me, that runs me... asks me questions or helps me reason or observes things that I'm doing and tries to find more efficient'. 10-23 03:18: 'in the sixth its own questions and prompts from observations basically (sight) of the brain are what is driving the questions and actions to happen... Why do I do that? hmm I should test if there a better way, or check to see if that is actually correct'.")) + '}')
w('    ask: "it types its own line into its mailbox, speaker = sixth" {class: mail; tooltip: ' + q(tip("What it asks is its own: 'wait why did I think that that way... or does this meaning actually make sense?' (10-23 01:28); 'why did the cell not populate' (10-27 03:52). 10-16 05:50: 'at first we would have to prompt these, but later many of these are written by the sixth'. 10-22 rev17: it reaches the main brain only through mother and mailboxes; whatever SQL it writes into the main brain is told, not learned.")) + '}')
w('    r9: "a new run R9 through the same hallway; SQ2 now finds R1\'s memory" {class: sheet}')
w('    see -> ask -> r9')
w('  }')
w('  guess: "the guessing brain" {')
w('    class: col; grid-columns: 1; grid-gap: 14')
w('    g_ask: "a cell no source fills (def.62) > the question goes to the guessing brain through mother" {class: mail; tooltip: "10-23 P5-9: memory first, then state, then sources, then guess."}')
w('    g_g: "a guess of what the meaning should be: announced, never lost" {class: brain; tooltip: ' + q(tip("10-23 P5-9: 'I don't know; I have a guess I believe is likely; would you like to test it?' 10-15 21:17: 'Always state that this is a guess or belief not known source truth'.")) + '}')
w('    g_wrong: "the sixth says why it was wrong > back prop over the adjusted corpus > guess again until it balances" {class: brain; tooltip: "10-23 03:18."}')
w('    g_ask -> g_g: {class: route}')
w('    g_g -> g_wrong: {class: not}')
w('  }')
w('}')
w('output.o2.to_sixth -> others.sixth.see: {class: route}')
w('others.sixth.r9 -> line.r1: {class: hop; label: "a new line, speaker = sixth"}')
w('sources.src62.empty -> others.guess.g_ask: {class: spawn; label: "search harder"}')
w('others.guess.g_g -> after.n63.m1: {class: fill; label: "def.62 = a guess, marked"}')

# ---------------- lane 12: open ----------------
w('open: "12 · WHAT HIS WORDS LEAVE OPEN (his calls, not filled)" {')
w('  class: lane')
w('  grid-columns: 5')
opens = [
 ("born inline or retry", "10-20 01:22 'writes it, and triggers born... goes to space' (inline) vs 10-21 18:39 'traverse back to the run start and try run again' (retry). Both his."),
 ("the receipt: physics or write run", "Audit 10-25 row 5: whether the hop's physics writes the receipt row or a write run does."),
 ("the sheet's physical form", "10-26 03:50: rows pointed to by the memory row, a table per run, or one cell. His v4 brain.db holds run_sheet rows keyed by run; the drawing follows that."),
 ("the compile", "10-23 P4 B1: 'I don't know that the compile is correct yet'. Diff and similar as drawn is his sketch of it, not a formula."),
 ("sourcing depth of the cascade", "10-23 P4: 'everything expands so fast'. Every symbol born from a definition text is sourced in turn; how deep is his call."),
 ("the say key", "10-26 05:12: 'the only way we have found that a trigger is needed is with a say key'. Not found in his words before that line."),
 ("one formula neuron or many", "Drawn: one formula neuron (55) with a row per formula. 10-23 08:47 says 'a pointer to the shortcut neuron formula for that'. His call."),
 ("what counts as 'correct' the first time", "His words 10-28: 'the first time it works, and is correct'. Drawn as: ok + a read run finds the table. His call."),
 ("the standing questions in the core", "10-23 P3 B2 'maybe those three questions'. Drawn as core neurons 57, 58, 59 because a fresh brain has nothing else to ask with."),
 ("define in the core or not", "Drawn: not in the core; born on this line (10-27 05:37). If in the core, SQ3 says yes and the run jumps to its formula: 'look up definition memory print' (10-25 msg 51)."),
]
for i, (t, tt) in enumerate(opens):
    w(f'  o{i+1}: {q(str(i+1) + ". " + t)} {{class: open; tooltip: {q(tip(tt))}}}')
w('}')

open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print("gates in the encoder after the line:", len(enc), "last shard:", shard_n[0], "return runs:", ret_runs_total)
