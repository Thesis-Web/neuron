# make_d2_v3.py: a typing aid that writes the D2 drawing of "define : who" from a fresh brain, v3.
# A drawing generator, not brain code. Gates are numbered in the order laid; shards are one sequence (10-20 00:34).
import json, sys
SAT = sys.argv[1]; OUT = sys.argv[2]
sat = json.load(open(SAT, encoding='utf-8'))

core = ["heard","said","space","CREATE","TABLE",'"',"(",")",",",";","INTEGER","TEXT","shard","before","trigger","call","spawn",
        "value","definition","source","entry","sense","class","text","example","origin","first_use","synonyms","antonyms","times",
        "first_at","last_at","ended_at","INSERT","INTO","VALUES","SELECT","FROM","WHERE","build","born","hop","write","copy","cut",
        "read","clock","memory","timeline","cell","ask","compile","decide","substitute","compare","say","out","find","split","join",
        "move","add","subtract"]
assert len(core) == 63
enc = {s: i+1 for i, s in enumerate(core)}
def gate(sym):
    if sym not in enc: enc[sym] = len(enc) + 1
    return enc[sym]
G_DEFINE = gate("define"); G_COLON = gate(":"); G_WHO = gate("who")          # 64 65 66
G_KNOW = gate("know (built)"); G_REM = gate("remember (built)"); G_SHAPE = gate("shape (built)")  # 67 68 69
G_FORM = gate("formula: create table (value) (born)")                         # 70
assert (G_DEFINE, G_COLON, G_WHO, G_KNOW, G_REM, G_SHAPE, G_FORM) == (64,65,66,67,68,69,70)

shard_n = [100]
def shard():
    shard_n[0] += 1; return shard_n[0]
hits_per_gate = {}
def hit(g):
    hits_per_gate[g] = hits_per_gate.get(g, 0) + 1

L = []
def w(s=""): L.append(s)
def tip(s): return s.replace('\\', '').replace('"', "'")
def qd(s):
    """a D2 string: double quotes unless the text holds one"""
    if '"' in s:
        return "'" + s.replace("'", "’") + "'"
    return '"' + s + '"'
def G(s): return gate("space" if s == " " else s)
def NAME(s): return "space" if s == " " else s

# ---------------------------------------------------------------- header
w("# define : who  -  the whole run from a fresh brain, drawn 2026-10-28 (v3, after the owner's second correction)")
w("# Every neuron is its own table. Numbers only in the tables. The words are in the tool pins (hover the i).")
w("# [his: date] = the owner's words. [reading] = mine, to strike. [open] = his call.")
w("direction: down")
w("grid-rows: 1")
w("grid-gap: 90")
w("vars: { d2-config: { layout-engine: elk } }")
w("""classes: {
  column: {style.fill: "#ffffff"; style.stroke: "#ffffff"; style.stroke-width: 0}
  lane: {style.fill: "#f8fafc"; style.stroke: "#334155"; style.stroke-width: 2; style.border-radius: 8; style.font-size: 26}
  col: {style.fill: "#ffffff"; style.stroke: "#94a3b8"; style.stroke-width: 1; style.border-radius: 6}
  neuron: {shape: sql_table; style.fill: "#93c5fd"; style.stroke: "#eff6ff"; style.stroke-width: 2}
  hit: {shape: sql_table; style.fill: "#bfdbfe"; style.stroke: "#f8fbff"; style.stroke-width: 1}
  newborn: {shape: sql_table; style.fill: "#f9a8d4"; style.stroke: "#fdf2f8"; style.stroke-width: 2}
  built: {shape: sql_table; style.fill: "#fdba74"; style.stroke: "#fff7ed"; style.stroke-width: 2}
  defn: {shape: sql_table; style.fill: "#fde047"; style.stroke: "#fefce8"; style.stroke-width: 2}
  mem: {shape: sql_table; style.fill: "#86efac"; style.stroke: "#f0fdf4"; style.stroke-width: 2}
  sheet: {shape: sql_table; style.fill: "#6ee7b7"; style.stroke: "#ecfdf5"; style.stroke-width: 1}
  tl: {shape: sql_table; style.fill: "#c4b5fd"; style.stroke: "#f5f3ff"; style.stroke-width: 2}
  encoder: {shape: sql_table; style.fill: "#cbd5e1"; style.stroke: "#f8fafc"; style.stroke-width: 2}
  key: {shape: sql_table; style.fill: "#fca5a5"; style.stroke: "#fef2f2"; style.stroke-width: 1}
  sixth: {shape: sql_table; style.fill: "#d8b4fe"; style.stroke: "#faf5ff"; style.stroke-width: 2}
  guess: {shape: sql_table; style.fill: "#f0abfc"; style.stroke: "#fdf4ff"; style.stroke-width: 2}
  mail: {shape: queue; style.fill: "#e0f2fe"; style.stroke: "#0369a1"}
  mother: {shape: hexagon; style.fill: "#fee2e2"; style.stroke: "#991b1b"; style.stroke-width: 2}
  prompt: {shape: document; style.fill: "#fee2e2"; style.stroke: "#991b1b"}
  src: {shape: package; style.fill: "#ffedd5"; style.stroke: "#c2410c"}
  brain: {shape: package; style.fill: "#ede9fe"; style.stroke: "#7c3aed"; style.stroke-width: 2}
  pick: {shape: diamond; style.fill: "#f1f5f9"; style.stroke: "#334155"}
  note: {style.fill: "#fffbeb"; style.stroke: "#d4a72c"; style.font-size: 14}
  his: {style.fill: "#fef3c7"; style.stroke: "#b45309"; style.font-size: 14}
  open: {style.fill: "#ffe4e6"; style.stroke: "#be123c"; style.font-size: 14}
  closed: {style.fill: "#dcfce7"; style.stroke: "#15803d"; style.font-size: 14}
  hop: {style.stroke: "#1d4ed8"; style.stroke-width: 3}
  trig: {style.stroke: "#ea580c"; style.stroke-dash: 5; style.stroke-width: 2}
  call: {style.stroke: "#15803d"; style.stroke-dash: 2; style.stroke-width: 2}
  spawn: {style.stroke: "#7c3aed"; style.stroke-dash: 8; style.stroke-width: 2}
  jump: {style.stroke: "#0f172a"; style.stroke-width: 4}
  route: {style.stroke: "#991b1b"; style.stroke-width: 3}
  fill: {style.stroke: "#059669"; style.stroke-dash: 2; style.stroke-width: 2}
  readw: {style.stroke: "#64748b"; style.stroke-dash: 1; style.stroke-width: 1}
  back: {style.stroke: "#b45309"; style.stroke-dash: 6; style.stroke-width: 3}
  builtw: {style.stroke: "#c2410c"; style.stroke-dash: 1; style.stroke-width: 2}
  not: {style.stroke: "#94a3b8"; style.stroke-dash: 3; style.stroke-width: 1; style.opacity: 0.6}
}""")

def node(cid, label, cls, rows=None, tt=None, indent="  "):
    parts = [f"class: {cls}"]
    if rows:
        for k, v in rows: parts.append(f"{k}: {qd(v)}")
    if tt: parts.append(f"tooltip: {qd(tip(tt))}")
    w(f"{indent}{cid}: {qd(label)} {{" + "; ".join(parts) + "}")
def edge(a, b, cls, label=None, indent="  "):
    s = f"{indent}{a} -> {b}: {{class: {cls}"
    if label: s += f"; label: {qd(label)}"
    w(s + "}")
def open_col(cid, label, indent="  ", cols=1, gap=14):
    w(f"{indent}{cid}: {qd(label)} {{")
    w(f"{indent}  class: col; grid-columns: {cols}; grid-gap: {gap}")
def close(indent="  "): w(f"{indent}}}")

# ================================================================= COLUMN A
w('A: "" {')
w('  class: column; grid-columns: 1; grid-gap: 70')

# ---- KEY
w('  key: "KEY, and the inside of every step" {')
w('    class: lane; grid-columns: 5; grid-gap: 24')
node("title", "define : who, the whole run from a fresh brain. v3, 2026-10-28, after his two corrections of the day. Read down each column; A the main flow, B the born runs and the formula, C outside and the other brains.", "his", None, "Every box carries his words in its tool pin, with the date. Numbers in the tables are this drawing's numbering: gates in the order laid, shards one sequence.", "    ")
node("k_neuron", "NEURON = its own table (64 · define)", "neuron", [("shard","before > trigger | call | spawn")], "A neuron is its own table; its name is its gate (10-19 21:14). Rows are its DNA: his sketch 10-28 gives shard id | before | trigger | call | spawn. The run arrives from before, goes on to trigger, calls side runs that return, spawns runs that leave.", "    ")
node("k_hit", "one HIT of a gate (the neuron drawn where it is hit)", "hit", [("shard","before > next")], "In a run column every box is one hit of a gate, drawn where the run hits it (his sketch). The row shown is the shard this run hit or wrote.", "    ")
node("k_newborn", "NEWBORN on this line", "newborn", [("shard","...")], "A gate that did not exist when the line arrived: born by the born run (10-20 01:22; 10-19 23:40).", "    ")
node("k_built", "BUILT by the brain in this run (a formula neuron)", "built", [("shard","...")], "His words 10-28: the three standing questions are large processes the brain builds itself from the hand-laid meanings; a long run that worked gets a new neuron born for its formula, relationally matched to the long run, usable with other variables. No spelling in the encoder: the label here is for the reader.", "    ")
node("k_defn", "DEFINITION NODE (born with the neuron; its first memory)", "defn", [("source","> return run"),("rel","kind > gate")], "10-19 23:40; 10-23 P2; 10-23 P5-9: relationships are built from the definition table.", "    ")
node("k_mem", "MEMORY NODE on the shard that ended a run (the run data sheet inside)", "mem", [("run","input, source"),("cell","state, value")], "10-23 P2 B2; 10-26 03:50; his v4 brain.db 10-27: run_memory + run_sheet. A neuron with several ending shards has several memory nodes (his words 10-28).", "    ")
node("k_tl", "TIMELINE: only a memory table", "tl", [("at","receipt > memory node, key words")], "10-16 06:40; 10-26 03:50.", "    ")
node("k_key", "THE KEY: what travels with anything that leaves and comes back", "key", [("run_cell","who, when, why, modifiers")], "His words 10-28: an sql trigger cannot just leave the brain; it is part of a process that says to the mother, the mother routes the script to the sources or the sql prompt and routes the response back through the encoder as secondary input so the brain can use the data to solve a run already in progress. The key is the metadata: what is this data in perspective to this run, where does it belong, what does it solve, who said it, when, why is it needed, what modifiers does it change. His guesses, by his word.", "    ")
node("k_sixth", "THE SIXTH: its own brain, its own runs", "sixth", [("asks","why that way? better way? correct shard? balance?")], "His words 10-28: the inner voice that observes or oversees all the runs and asks questions.", "    ")
node("k_guess", "THE GUESSING BRAIN: a hand-built llm over a small corpus", "guess", [("guess","confidence, belief, times used, times solved")], "His words 10-28: qkv, weights, corpus, hidden layers, back propagation, context; learns on the fly; every answer labeled a guess with a confidence; belief never over 50% on first use.", "    ")
w('    wires: "WIRES" {')
w('      class: col; grid-columns: 5; grid-gap: 10')
for cid, lab, cls, tt in [("w1","hop","hop","The run moves to the remainder head; before and after; the key is the remainder (§12 law 13)."),("w2","trigger","trig","A DNA row excites a run (10-26 05:12); it writes nothing itself (10-26 03:59)."),("w3","call (returns)","call","A side run whose answer comes back to this run (his sketch)."),("w4","spawn (leaves)","spawn","A run that goes off on its own (his sketch)."),("w5","jump (formula path)","jump","Skip the long run: the formula neuron, plug the value in (his words 10-28)."),("w6","carried by mother","route","Mother routes and traverses, decides nothing (10-23 P2)."),("w7","a return fills a cell","fill","10-26 03:50."),("w8","a run reads a table","readw","Read runs: the standing questions, the inspection, the sixth looking."),("w9","step back / eliminate","back","His words 10-28: a failed cell sends the run back to a choice; the failed choice is remembered from the timeline and eliminated."),("w10","built from (tools compounding)","builtw","His words 10-28: tool 1 + tool 2 makes tool 3; the brain builds its tools from the hand-laid ones.")]:
    colour = {"hop":"#1d4ed8","trig":"#ea580c","call":"#15803d","spawn":"#7c3aed","jump":"#0f172a","route":"#991b1b","fill":"#059669","readw":"#64748b","back":"#b45309","builtw":"#c2410c"}[cls]
    w('      ' + cid + ': ' + qd(lab) + ' {style.stroke: "' + colour + '"; style.stroke-width: 3; tooltip: ' + qd(tip(tt)) + '}')
close("    ")
w('    step: "THE INSIDE OF EVERY STEP (his words 10-28)" {')
w('      class: col; grid-columns: 1; grid-gap: 10')
node("s1", "what does the brain need to complete this step?", "his", None, "His words 10-28: every inside step is 'what does the brain need to complete this'.", "      ")
node("s2", "with the tools the brain has, how does it build that need?", "his", None, "His words 10-28: 'with the tools the brain has how does it build that need'. At first this is recursive: each process is decomposed and built step by step; more tools may be needed, built step by step, then used, then combined.", "      ")
node("s3", "decide, build, check", "his", None, "His words 10-28: 'it's just one step decide, build, check, next step, build, check, add to the previous, next step decide, build, check, add to steps that are relevant, combine in different ways to make other things that work'.", "      ")
node("s4", "next step; add to the previous; combine", "his", None, "His words 10-28: once five of the correct versatile tools exist there is an abundance of possibilities; the hand-laid core is the decomposition of tools down to the most basic.", "      ")
w('      s1 -> s2 -> s3 -> s4')
w('      s4 -> s1: {class: not; label: "recursive at first"}')
close("    ")
close("  ")

# ---- lane 0: core
w('  core: "0 · THE FRESH BRAIN: the hand-laid tools (his outline 10-25 21:50; v1 10-19; his 14 physical actions 10-23 P2). The count is unknown: 20, 80 or 200 (his words 10-28)" {')
w('    class: lane; grid-columns: 4; grid-gap: 40')
w('    encoder: "ENCODER: a straight conversion table (the only place a spelling lives)" {')
w('      class: encoder')
w('      tooltip: ' + qd(tip("10-26 03:50: a straight database conversion table with gates in a sequential order, new word new gate #. 10-25: there are no words in the graph. The brain holds the numbers. 1..63 is this drawing's numbering of the core in the order laid; it is a reading of what must be hand laid, not his list: his words 10-28: 'hand laid that tool is not wrong, but was just out of order, and it didn't need to be hand laid, it just needed to be built by the brain at a different time'.")))
for s in core:
    w(f'      g{enc[s]}: {qd(s)}')
close("    ")
open_col("schemas", "the hand-laid shapes", "    ")
node("schema_mem", "MEMORY TABLE shape (his own hand, ~/neuron/v4/brain.db, 10-27 01:17)", "mem", [("run","INTEGER PK"),("input","the receipt"),("source","who spoke: user, mother, sixth"),("cell","INTEGER"),("state","0 declared, 1 filled"),("value","what the return put there")], "CREATE TABLE run_memory (run INTEGER PRIMARY KEY, input TEXT NOT NULL, source TEXT NOT NULL); CREATE TABLE run_sheet (run REFERENCES run_memory(run), cell INTEGER, state INTEGER DEFAULT 0 CHECK(state IN (0,1)), value TEXT, PRIMARY KEY(run,cell)). His own typing, 10-27 01:17. This answers the question he asked about on 10-28 ('rows pointed to by the memory row? a table per run, or one cell?'): in SQLite 'the sheet lives in a cell in the memory row' could be (a) one column of the memory row holding the whole sheet, (b) rows of a sheet table keyed by the run number, which the memory row points to, or (c) a separate small table per run. His v4 brain.db is (b). The drawing follows it.", "      ")
node("schema_def", "DEFINITION NODE shape (his own hand, sqlite history)", "defn", [("source","which source brain answered"),("entry","the headword the source sent"),("sense_class","..."),("text","pointer to the return run (gates)"),("synonyms_antonyms","..."),("times_first_last_ended","truth shift keeps the old row"),("rel","kind > gate (built from the table)")], "CREATE TABLE definition (id, neuron, source, entry, sense, class, text, example, origin, first_use, synonyms, antonyms, times, first_at, last_at, ended_at). His own typing. Born with the neuron (10-19 23:40); the first memory (10-23 P2); relationships are built from this table and self-populate (10-23 P5-9; P4).", "      ")
node("schema_tl", "TIMELINE shape", "tl", [("id","INTEGER PK"),("at","the clock neuron (47)"),("receipt","run > memory node"),("key_words","a few gates")], "10-16 06:40; 10-26 03:50; 10-23 P3 B1 (by a trigger hop, never a sweep).", "      ")
node("schema_key", "THE KEY on the out mailbox and the return (his guesses 10-28)", "key", [("run","which run asked"),("cell","which cell it fills"),("gate","who said it: the neuron that sent"),("when","clock reading"),("why","what it solves"),("modifiers","what it changes")], "His words 10-28: 'the key or some thought the metadata is the what is this data in perspective to this run, where does it belong, what does it solve, who said it, when did it happen, why is it needed. what modifiers does it change... pure guesses by me here'. The out neuron (60) writes it; the secondary input carries it back; the return fills the cell by it. 10-26 05:12: 'the only way we have found that a trigger is needed is with a say key'.", "      ")
close("    ")
w('    outside: "OUTSIDE THE BRAIN" {')
w('      class: col; grid-columns: 2; grid-gap: 14')
node("m_user_in", "user > encoder", "mail", None, "His outline 10-25 21:50. Populated-driven, never a timer (10-22 rev17).", "      ")
node("m_mother_in", "mother > encoder (secondary input, with the key)", "mail", None, "His outline: the secondary input mailbox to the encoder from the mother. SQL answers and source answers come back this way, with the key, so the brain can use the data to solve a run already in progress (his words 10-28).", "      ")
node("m_sixth_in", "sixth.db > encoder (third)", "mail", None, "His outline: the third input mailbox to the encoder from the sixth.db.", "      ")
node("m_out", "brain > mother (60 out, with the key) / brain > user", "mail", None, "His outline. The out neuron (60) is the port the run hits to leave; its row carries the key.", "      ")
node("mother", "MOTHER", "mother", None, "10-23 P2: just a router and a traverser. That's it. Takes the output and traverses it to the sources, to another brain, or to its own sql; picks up the outputs and brings them back. Works no data.", "      ")
node("prompt", "THE NEURON PROMPT (the brain's own sql prompt)", "prompt", None, "10-24 msg 36: mother pastes the string in the sql prompt and hits enter, waits for the response, returns it as a secondary input. §2.6 his edit 10-24.", "      ")
for k, name, tt in [("wn","WordNet","1 line for who (the WHO agency), 1 for define"),("gcide","Webster 1913","1 line for who, 1 for define"),("mw","Merriam-Webster","2 lines for who, 2 for define"),("mwt","M-W thesaurus","4 like-lines for define"),("moby","Moby","3 like-lines for define"),("map","his relation map","1 like-line for define"),("sqldoc","SQLite docs","the meaning of the code words to the silicon; nothing for : in this slice")]:
    node(f"src_{k}", name, "src", None, "A source brain: a database with a corpus, an inbox, an outbox and its own trigger that does its work the moment an ask lands (10-22 rev17). In the archived slice (tries/11 sat172.json): " + tt + ".", "      ")
node("sixthdb", "sixth.db (its own brain, lane 11)", "brain", None, "10-25 msg 41: create copy brain.db rename to sixth.db... update mother for mailbox to sixth.", "      ")
node("guessdb", "guessing brain (lane 11b)", "brain", None, "His words 10-28: built more like an llm, hand built, over a small corpus.", "      ")
close("    ")
open_col("notes", "", "    ")
node("core_note", "the core's neurons are gates 1..63 (the encoder table, left): the SQL words the born run speaks, the space and the marks, his 14 physical actions (read, write, compare, add, subtract, move, find, split, join, clock, hear, say, call, spawn) and the write, copy, cut runs. Each is its own table with hand-laid DNA rows and a definition node fed from the SQL docs. Later a core word becomes a row in the real word's neuron.", "his", None, "10-19 21:20: hand lay a table, then hand lay those same words as nodes so the brain lays its own tables. 10-19 23:03: ( , integer, primary, key... all neurons of their own. 10-23 P2: the 14 physical actions. 10-23 P2 B3: core words become a row in the DNA of the actual word neuron. 10-27 05:05: the first core will break the rules... later that should cease to exist. His words 10-28: 'the hand laid core is the decomposition of tools down to the most basic of tools needed to be hand laid... 80 sounds about close, but it might be more like 200 or less or it might be 20'.", "      ")
node("core_note2", "what is NOT hand laid: the standing questions, the born run as a formula, the ask, the compile, the decide, the substitution. The brain builds them in this first run from the tools above (lane 13).", "his", None, "His words 10-28: 'those three questions are large processes in themselves.. so the balance is the simplest way for the brain to ask these at first, using the meanings that it has handlaid to build them itself'. 'there is no first turn that is simple.. every turn even define : who... requires all the things in order to be done correct... fake any of it, and it will be lost'.", "      ")
close("    ")
close("  ")

# ---- lane 1: the line
w('  line: "1 · THE LINE ARRIVES: prompt > encoder > brain" {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
node("typed", "user types   define : who", "note", None, "Lands in the user input mailbox (his outline 10-25 21:50).", "    ")
node("enc", "encoder: define > 64 (new)   space > 3   : > 65 (new)   space > 3   who > 66 (new)", "encoder", None, "A symbol with no gate gets the next number; nothing else is figured here (10-26 03:50; 10-23 P2). Who is speaking is part of the input: user, heard (10-26 03:50).", "    ")
node("r1", "input row R1", "sheet", [("run","1"),("gates","64 3 65 3 66"),("arrival","1 (heard)"),("speaker","user"),("clock","t0 (47)")], "The main run's input row. The clock neuron (47) is hit on every run (10-26 03:50). The remainder is the rest of the line as gate numbers; its head is the key at every gate (10-23 P3).", "    ")
w('    typed -> enc -> r1')
close("  ")

# ---- lane 2: standing questions, built
w('  sq: "2 · THE STANDING QUESTIONS, BUILT BY THE BRAIN the simplest way from the hand-laid tools, before the main run runs (10-23 P3 B2; his words 10-28). Each is a long run the first time; its formula neuron is born when it works; then it is a jump." {')
w('    class: lane; grid-columns: 4; grid-gap: 30')
sq_defs = [
  (G_KNOW, "know", "do I know anything about this?", [("46 read","the encoder gates of the line, their definition nodes"),("55 compare","each gate against: exists? definition rows?"),("43 write","the answer cell")], "SQ1 'Do I know anything about this?' (10-23 P3 B2). Built from read + compare + write: the brain needs to know whether 64, 65, 66 exist and have definition rows; the tools it has are read (46), compare (55), write (43); it builds the run from them, checks, and the answer is a cell. Fresh brain: 0."),
  (G_REM, "remember", "do I have memories of this?", [("46 read","memory nodes, timeline receipts"),("55 compare","receipt against 64 3 65 3 66"),("43 write","the answer cell")], "SQ2 'Do I have a memory of this?' (10-23 P3 B2). 10-16: 'have I seen 1+1+1... before, yes... instead of doing the math I just remembered the answer'. Fresh brain: no memory rows: 0."),
  (G_SHAPE, "shape", "does this run shape match a shape I have? a formula proven to try first?", [("46 read","timeline receipts; formula neurons"),("61 find","the pattern X 3 65 3 Y"),("55 compare","shape against shape"),("43 write","the answer cell")], "SQ3 (10-23 P3 B2; his words 10-28: 'do I have a formula that is proven to try first.... this is the step at the beginning that skips the long run... and uses the variable formula path or the shortcut path if the variable formula path is not found yet'). Fresh brain: 0."),
]
sq_shards = {}
for g, name, q, tools, tt in sq_defs:
    open_col(f"q{g}", f"{g} · {name}", "    ")
    node("need", q, "his", None, "His words 10-28: every inside step: what does the brain need to complete this; with the tools the brain has how does it build that need.", "      ")
    prev = 1; shs = []
    for i, (t, what) in enumerate(tools):
        tg = int(t.split()[0]); sh = shard(); hit(tg); shs.append(sh)
        nxt = int(tools[i+1][0].split()[0]) if i+1 < len(tools) else 0
        node(f"h{i}", t, "hit", [(f"s{sh}", f"{prev} > {nxt if nxt else '-'} | - | {'48 memory' if not nxt else '-'}")], f"hit {i+1} of {len(tools)} of the long run of the question: {what}. shard s{sh}, arrived from {prev}.", "      ")
        if i: edge(f"h{i-1}.s{shs[i-1]}", f"h{i}.s{sh}", "hop", None, "      ")
        prev = tg
    sq_shards[g] = shs[-1]
    node("m", f"memory node on 43.s{shs[-1]} (the question run)", "mem", [("run",str(shs[-1])),("input","receipt of the question run"),("source","R1"),("c_answer","0")], "The question is a run that ends; its memory row sits on the shard that ended it, with its one-cell sheet inside. Its answer is a cell on R1's sheet.", "      ")
    node("f", f"{g} · {name} (formula neuron, born when the run worked)", "built", [(f"s{shard()}", "1 > 46 | - | -"),("points_at", f"memory of the long run (43.s{shs[-1]})")], f"His words 10-28: 'a long run has an end, that run basically = a specific formula sometimes but the variables are already filled in. determining the formula neuron is figuring out what the variables of the formula is... a new neuron must be born, that is relationally matched to that long run'. Gate {g} is born after the question worked once; on every later run the question is a jump to it, and the variables (the gates of the new line) are plugged in. No spelling in the encoder.", "      ")
    edge(f"h{len(tools)-1}.s{shs[-1]}", "m", "trig", "no remainder", "      ")
    edge("m", "f", "builtw", "born: the formula", "      ")
    close("    ")
open_col("path", "which path", "    ")
node("pick", "all three 0 > the long way", "pick", None, "10-23 P3 B2: if they all come back no, then we have to go the long way... yes we know something, yes we have a shortcut, yes a formula shortcut, then the formula shortcut path, if belief and truth show it can be done correctly.", "      ")
node("short", "shortcut: one hop to the memory (replay the long run)", "note", None, "Not taken on this line. His words 10-28: 'the shortcut path if the variable formula path is not found yet'.", "      ")
node("formula_path", "formula path: jump to the formula neuron, plug the variables in", "note", None, "Not taken on this line for R1 (nothing is bound to 64 yet). Taken by the born runs for 65 and 66 (column B).", "      ")
node("circle", "and it all circles back here: every run, side runs too, begins with the three questions", "his", None, "His words 10-28: 'on the pointer the circle is back to the memory of the run ... or maybe the run data sheet and it all circles back to the standing questions, do I know anything about this, do I have memories about this, do I have a formula that is proven to try first'.", "      ")
edge("pick", "short", "not", None, "      ")
edge("pick", "formula_path", "not", None, "      ")
close("    ")
for g, name, q, tools, tt in sq_defs:
    edge(f"q{g}.m", "path.pick", "fill", None, "    ")
close("  ")
for g, name, q, tools, tt in sq_defs:
    edge("line.r1", f"sq.q{g}.need", "spawn", None, "  ")

# ---- lane 3: main run
w('  main: "3 · THE MAIN RUN R1, the hallway: 64 > 3 > 65 > 3 > 66. Born inline at every missing gate (mechanical intelligence: missing neuron = missing step). The receipt is written by the brain into R1\'s sheet." {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
open_col("hall", "the hallway, top to bottom", "    ")
s_main = {}
for key, g, before, trig, tt, cls in [
  ("a", G_DEFINE, 1, 3, "define, gate 64, born this line. No gate existed: born INLINE, 'missing neuron = missing step... new neuron must be born such that the next step can be completed' (his words 10-28); the run does not go back to its start. Then the write run lays s%d: arrived from 1 (heard), goes on to 3. Its trigger column holds nothing yet: a symbol with no action (10-27 05:37).", "newborn"),
  ("b", 3, G_DEFINE, G_COLON, "the space, gate 3, a core neuron. ( ) is a meaning that we know happens to the graph or the silicon (10-27 05:37). s%d: 64 > 65.", "neuron"),
  ("c", G_COLON, 3, 3, ":, gate 65, born inline. In sql ':' has an action we know; on this line it has none yet (10-27 05:37). s%d: 3 > 3.", "newborn"),
  ("d", 3, G_COLON, G_WHO, "the same neuron 3, hit a second time, drawn where it is hit (his sketch). s%d: 65 > 66.", "neuron"),
  ("e", G_WHO, 3, 0, "who, gate 66, born inline. s%d has no remainder: 'the dna shard that has no remainder is what triggers the write of the memories' (10-15 21:50). This shard's memory node holds R1's row with the whole sheet inside. Later rows: 'who is, who are, who did and who was each fire a different row inside the one neuron for who' (10-22 rev17).", "newborn")]:
    s = shard(); hit(g); s_main[key] = s
    lab = {G_DEFINE:"64 · define",3:"3 · space",G_COLON:"65 · :",G_WHO:"66 · who"}[g]
    node(f"h{key}", lab, cls, [(f"s{s}", f"{before} > {trig if trig else '-'} | - | {'48 memory' if not trig else '-'}")], tt % s, "      ")
close("    ")
for a, b in (("a","b"),("b","c"),("c","d"),("d","e")):
    edge(f"hall.h{a}.s{s_main[a]}", f"hall.h{b}.s{s_main[b]}", "hop", None, "    ")
open_col("rec", "the receipt: written by the brain, read by the brain", "    ")
s_hop = shard(); hit(42); s_wr = shard(); hit(43)
node("hop42", "42 · hop", "neuron", [(f"s{s_hop}", "- > - | 43 write | -")], "The hop neuron: 'hop neuron is just a hop neuron... different dna row' (10-26 05:12). Each hop calls the write run, which writes the receipt row into R1's sheet. His words 10-28: 'if physics writes the brain will not be able to see or observe what happened,, anything the brain cannot see is a step the brain cannot build upon... run receipt is just the order of the main run plus the hops, so it's just recorded in the run data sheet as a row and columns, then read and written by the brain'.", "      ")
node("wr43", "43 · write", "neuron", [(f"s{s_wr}", "42 > - | - | -")], "The write run lays one row of R1's sheet per hop.", "      ")
node("receipt", "R1's sheet, the receipt rows", "sheet", [("h1",f"1 > 64.s{s_main['a']}"),("h2",f"64 > 3.s{s_main['b']}"),("h3",f"3 > 65.s{s_main['c']}"),("h4",f"65 > 3.s{s_main['d']}"),("h5",f"3 > 66.s{s_main['e']} (end)")], "The path of gates and shards: a pointer to the run, never the run again (10-23 P2). Rows and columns of the run data sheet, written by the write run (his words 10-28).", "      ")
edge(f"hop42.s{s_hop}", f"wr43.s{s_wr}", "call", None, "      ")
edge(f"wr43.s{s_wr}", "receipt", "fill", None, "      ")
close("    ")
edge(f"hall.hb.s{s_main['b']}", f"rec.hop42.s{s_hop}", "call", "every hit: the hop calls write", "    ")
open_col("notes", "", "    ")
node("inline", "BORN INLINE (this lane) vs STEP BACK (lane 6): two different cases", "his", None, "His words 10-28: 'born inline is mechanical intelligence perspective... meaning missing neuron = missing step ... new neuron must be born such that the next step can be completed.... traverse back and retry.... has to do with a failed cell on the run data sheet, if the new step, or the next step fails to provide the run data sheet with data then the run must be re ran via different substitution theory or using a different formula, via process of elimination theory ... meaning there is a check back or even step back to a run that had a choice ... the failed choice is remembered from the time line and eliminated'.", "      ")
close("    ")
close("  ")
edge("sq.path.pick", "main.hall.ha", "hop", "long way", "  ")

# ---- lane 9: end + timeline  (filled later, needs shards from other lanes; emit after columns B and C by deferring rows)
# we emit lane 9, 10, 12 at the end of column A; collect timeline rows as we go
tl_rows = [("r1", f"t0 | SQ1 know > 43.s{sq_shards[G_KNOW]} | 67"), ("r2", f"t0 | SQ2 remember > 43.s{sq_shards[G_REM]} | 68"), ("r3", f"t0 | SQ3 shape > 43.s{sq_shards[G_SHAPE]} | 69")]
A_tail = []   # lines to append to column A later
# close column A later

# ================================================================= COLUMN B
B = []
def wb(s=""): B.append(s)

cols_dna = ["shard","before","trigger","call","spawn"]
stmt1 = ["CREATE"," ","TABLE"," ",'"',"value",'"'," ","("," "]
for i, c in enumerate(cols_dna):
    stmt1 += [c," ","INTEGER"]
    if i < len(cols_dna)-1: stmt1 += [" ",","," "]
stmt1 += [" ",")"," ",";"]
cols_def = ["source","entry","sense","class","text","example","origin","first_use","synonyms","antonyms","times","first_at","last_at","ended_at"]
stmt2 = ["CREATE"," ","TABLE"," ",'"',"value"," ","definition",'"'," ","("," "]
for i, c in enumerate(cols_def):
    stmt2 += [c," ","INTEGER" if c == "times" else "TEXT"]
    if i < len(cols_def)-1: stmt2 += [" ",","," "]
stmt2 += [" ",")"," ",";"]

# temporarily redirect w to B
_saved = L
L = B
w('B: "" {')
w('  class: column; grid-columns: 1; grid-gap: 70')
w('  born64: "4 · BORN RUN R2 for 64, THE LONG WAY: one hit per symbol through the SQL-word neurons; the value neuron holds the hole; build routes to mother (10-19 21:52; 23:03; his words 10-28: like 50 neurons gates, a different shard in the value neuron for each new run)" {')
w('    class: lane; grid-columns: 4; grid-gap: 30')
sb = shard(); hit(41)
open_col("colA", "born, and the out key", "    ")
node("b41", "41 · born", "neuron", [(f"s{sb}", "64 > 4 | - | 51 ask")], "The born run, excited by the no-gate condition at 64 (10-20 01:22). Arrived from 64, goes on to 4 (CREATE); spawn column: the ask run (51) for the newborn's sources (10-23 P4). It declares on R1's sheet the cell gate.64 and its own sheet: value, text, reply.", "      ")
node("keyrow", "the key this run puts on the out mailbox", "key", [("run","R2"),("cell","reply"),("gate","40 build"),("when","t1"),("why","R1 needs gate 64"),("modifiers","-")], "His words 10-28 (the say key): the metadata that travels with the script to mother and back with the response, so the return fills the right cell of the right run.", "      ")
close("    ")
def run_snake(cid, title, syms, first_before, ncols, run_tag, indent="    "):
    """a statement laid out in ncols sub-columns, snaking down each"""
    w(f'{indent}{cid}: {qd(title)} {{')
    w(f'{indent}  class: col; grid-columns: {ncols}; grid-gap: 24')
    per = -(-len(syms) // ncols)
    ids, shs = [], []
    prev_g = first_before
    for c in range(ncols):
        w(f'{indent}  c{c}: "" {{')
        w(f'{indent}    class: col; grid-columns: 1; grid-gap: 14')
        for i in range(c*per, min((c+1)*per, len(syms))):
            s = syms[i]; g = G(s); sh = shard(); hit(g)
            nxt = G(syms[i+1]) if i+1 < len(syms) else 0
            call = "43 write" if s == "value" else "-"
            extra = ""
            if s == "value":
                extra = " THE HOLE: 'create table (var a)... a table of what ever is sitting at the newest memory at var a' (10-19 23:08); 'a different shard in the value neuron for each new run' (his words 10-28). Its call: the write run (43) writes this run's value, 64, into the run's sheet cell value; the substitution fills the hole from the sheet (10-24 msg 36)."
            node(f"h{i}", f"{g} · {NAME(s)}", "hit", [(f"s{sh}", f"{prev_g} > {nxt if nxt else '40'} | {call} | -")], f"hit {i+1} of {len(syms)} in {run_tag}: gate {g} ({NAME(s)}), shard s{sh}, arrived from {prev_g}, goes on to {nxt if nxt else '40 build'}.{extra}", indent + "    ")
            ids.append((c, f"h{i}")); shs.append(sh)
            prev_g = g
        close(indent + "  ")
    for i in range(1, len(syms)):
        ca, ha = ids[i-1]; cb, hb = ids[i]
        edge(f"c{ca}.{ha}.s{shs[i-1]}", f"c{cb}.{hb}.s{shs[i]}", "hop", None, indent + "  ")
    close(indent)
    return ids, shs
ids1, shs1 = run_snake("st1", f"statement 1: CREATE TABLE ' 64 ' ( shard INTEGER , before INTEGER , trigger INTEGER , call INTEGER , spawn INTEGER ) ;  ({len(stmt1)} hits)", stmt1, 41, 2, "R2")
ids2, shs2 = run_snake("st2", f"statement 2: CREATE TABLE ' 64 definition ' ( source TEXT , ... , ended_at TEXT ) ;  ({len(stmt2)} hits; the definition node born with the neuron, 10-19 23:40)", stmt2, 10, 3, "R2")
i_val1 = stmt1.index("value"); i_val2 = stmt2.index("value")
edge(f"colA.b41.s{sb}", f"st1.c0.h0.s{shs1[0]}", "hop", None, "    ")
ca, ha = ids1[-1]; cb, hb = ids2[0]
edge(f"st1.c{ca}.{ha}.s{shs1[-1]}", f"st2.c{cb}.{hb}.s{shs2[0]}", "hop", "; > CREATE", "    ")
s_build2 = shard(); hit(40); s_out = shard(); hit(60)
open_col("endcol", "the end of R2", "    ")
node("b40", "40 · build", "neuron", [(f"s{s_build2}", "10 > 60 | - | 48 memory")], "The build neuron: 'the last build word was the build neuron... routing information for the mother... build neuron = routing to sql prompt' (10-26 03:50). Its row, picked by before (10 ;) and no remainder, is a build row because of how before and remainder are set, not by counting. No remainder: this shard ends R2 and carries R2's memory node. The build neuron ends every born run, so it gains one memory node per born run (his words 10-28).", "      ")
node("o60", "60 · out (the port)", "neuron", [(f"s{s_out}", "40 > - | - | -")], "The port the run hits to leave: the product and the key go on the brain > mother mailbox. 10-23 msg 1: output to sources is a dna row and trigger to port.", "      ")
node("text", "the product: the two statements as text, hole filled from cell value = 64, with the key", "note", None, "10-19 23:03: the statement as the product of the run. 10-24 msg 36: the run data sheet produces the exact code that sql needs to run as output the same way that it forms human sentences; given to the mother to route to the sql prompt.", "      ")
node("reply", "SQL answers ok > mother > encoder (secondary, with the key) > fills R2.reply", "sheet", [("key","R2 | reply | 40 | t1")], "10-24 msg 36; 10-26 03:50: each return fills its spot. The key says which run and which cell. An error is not an end (10-27 03:52).", "      ")
node("m2", f"memory node on 40.s{s_build2} (R2)", "mem", [("run","R2"),("input",f"receipt: 41.s{sb} 4.s{shs1[0]} ... 10.s{shs2[-1]} 40.s{s_build2}"),("source","R1 (no gate at 64)"),("c_value","64"),("c_text","> the product"),("c_reply","ok"),("c_next_step","1: 64 exists, R1 wrote 64.s%d" % s_main['a']),("c_formula",f"> receipt with the hole at 18.s{shs1[i_val1]}, 18.s{shs2[i_val2]}")], "R2's memory row on the shard that ended it, with its sheet inside. Cells declared by the triggers that tripped (10-26 03:50).", "      ")
node("tl2", f"timeline row: t1 | R2 > 40.s{s_build2} | 41 64", "tl", None, "One row per run that ends (10-16 06:40).", "      ")
edge(f"b40.s{s_build2}", f"o60.s{s_out}", "hop", None, "      ")
edge(f"o60.s{s_out}", "text", "route", None, "      ")
edge("text", "reply", "route", "mother > neuron prompt > SQL > mother", "      ")
edge("reply", "m2", "fill", None, "      ")
edge("m2", "tl2", "trig", "memory > timeline, stops", "      ")
close("    ")
ca, ha = ids2[-1]
edge(f"st2.c{ca}.{ha}.s{shs2[-1]}", f"endcol.b40.s{s_build2}", "hop", None, "    ")
s_w = shard(); hit(43)
open_col("wcol", "the write run the hole calls", "    ")
node("w43", "43 · write", "neuron", [(f"s{s_w}", "18 > - | - | -")], "The write run: excited by the value neuron's call; writes value = 64 into R2's sheet (10-26 03:59: the trigger just triggers that run, often used with the copy run, and cut run).", "      ")
close("    ")
ca, ha = ids1[i_val1]
edge(f"st1.c{ca}.{ha}.s{shs1[i_val1]}", f"wcol.w43.s{s_w}", "call", "call", "    ")
ca, ha = ids2[i_val2]
edge(f"st2.c{ca}.{ha}.s{shs2[i_val2]}", f"wcol.w43.s{s_w}", "call", None, "    ")
edge(f"wcol.w43.s{s_w}", "endcol.m2", "fill", "value = 64", "    ")
close("  ")
tl_rows.append(("r4", f"t1 | R2 born 64 > 40.s{s_build2} | 41 64"))

# ---- lane 5: the formula neuron born, back population
w('  formula: "5 · THE FORMULA: when the long run worked (the next step completed) a decide formula run finds the variables; a NEW NEURON is born for the formula, relationally matched to the long run; back population lays the jump (his words 10-28)" {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
s_dec = shard(); hit(53); s_cmp = shard(); hit(55); s_bw = shard(); hit(43)
open_col("decide", "the decide formula run", "    ")
node("worked", "R2 worked: the next step of R1 completed (64 exists; R1 wrote 64.s%d)" % s_main['a'], "his", None, "His words 10-28: 'it's done by way of the first time it works, and is correct'; in context: 'when it works and is correct the graph will have meanings of its own, the graph shape of runs will start to show us more information'. [reading] 'works' = the next step of the run that needed it completed; 'correct' grows with the user's correct/incorrect and the sixth's observation (lanes 10, 11).", "      ")
node("d53", "53 · decide (formula)", "neuron", [(f"s{s_dec}", "40 > 55 | 46 read | -")], "His words 10-28: 'it triggers a decide formula run that decides what the formula is, then writes it in that runs data sheet'. It reads R2's receipt (46), compares (55) the hits against the run's input to find which hits carried the variable (the value neuron's shards), and the write run (43) writes the formula into R2's sheet cell formula: the receipt with the holes marked.", "      ")
node("c55", "55 · compare", "neuron", [(f"s{s_cmp}", "53 > 43 | - | -")], "Which hits are the variables: the ones whose value came from the sheet, not from the line.", "      ")
node("w43", "43 · write", "neuron", [(f"s{s_bw}", "55 > - | - | -")], "Writes cell formula into R2's memory node.", "      ")
edge(f"d53.s{s_dec}", f"c55.s{s_cmp}", "hop", None, "      ")
edge(f"c55.s{s_cmp}", f"w43.s{s_bw}", "hop", None, "      ")
close("    ")
s_f = shard(); hit(G_FORM)
open_col("fcol", "the formula neuron, born", "    ")
node("f70", "70 · formula: create table (value) (born)", "built", [(f"s{s_f}", "41 > 18 | 54 substitute | -"),("other_rows", "(other variables or modifiers: another row, or another formula neuron)")], "His words 10-28: 'a long run has an end, that run basically = a specific formula sometimes but the variables are already filled in. determining the formula neuron is figuring out what the variables of the formula is... once the variables are determined then that row cannot live in the main run because it doesn't match the run receipt of that run... thus a new neuron must be born, that is relationally matched to that long run, but can be used with different variables on other runs also.... you have to take in account variables and modifiers'. Born by the born run (the long way, the last time: [reading] its own birth has no formula yet). Its row: arrived from born (41), goes on to the value neuron (18) with a new shard per run; calls the substitution run (54).", "      ")
node("fdef", "definition node of 70: relationally matched to the long run", "defn", [("formula_of", f"> R2 memory node 40.s{s_build2} (the run data sheet)"),("variables", f"18.s{shs1[i_val1]}, 18.s{shs2[i_val2]} (the holes)"),("rel", "kind > 4 CREATE, 5 TABLE (the words it stands for)")], "The pointer circles back to the memory of the long run (his words 10-28: 'on the pointer the circle is back to the memory of the run ... or maybe the run data sheet'). The standing question SQ3 finds it next time: 'do I have a formula that is proven to try first'.", "      ")
node("bp", f"back population: the write run lays on 4.s{shs1[0]} the jump > 70.s{s_f}", "note", None, "His words 10-28: 'through back population the triggers or calls or jumps or hops from a run create table (value) would have to show the substitution run and the write run writing the value, then the trigger of the substitution run copying into the substitution run so that you can then skip the long run and use the formula neuron'. 10-23 P5-9: back population is the application of a newly understood process to the other things it fits.", "      ")
edge("f70", "fdef", "readw", "born with it", "      ")
edge(f"f70.s{s_f}", "bp", "trig", None, "      ")
close("    ")
open_col("sqcol", "and the standing questions now find it", "    ")
node("sq3", "69 · shape (formula neuron): on the next born run, cell = 70", "built", [("answer","formula proven: 70")], "His words 10-28: 'it all circles back to the standing questions... do I have a formula that is proven to try first.... this is the step at the beginning that skips the long run'.", "      ")
node("sq2", "68 · remember: on the next born run, cell = R2's memory", "built", [("answer",f"memory: 40.s{s_build2}")], "If no formula were born yet, the shortcut path would replay the long run from this memory (his words 10-28: 'the shortcut path if the variable formula path is not found yet').", "      ")
close("    ")
close("  ")
edge("born64.endcol.m2", "formula.decide.worked", "trig", "reply ok, next step done", "  ")
edge("formula.decide.worked", f"formula.decide.d53.s{s_dec}", "trig", None, "  ")
edge(f"formula.decide.w43.s{s_bw}", "born64.endcol.m2", "fill", "writes cell formula", "  ")
edge(f"formula.decide.w43.s{s_bw}", "formula.fcol.f70", "builtw", "a new neuron is born for the formula", "  ")
edge("formula.fcol.bp", f"born64.st1.c0.h0", "jump", f"jump laid on 4.s{shs1[0]}", "  ")
edge("formula.fcol.fdef", "formula.sqcol.sq3", "readw", "SQ3 reads it", "  ")

# ---- lane 5b: shortcut born runs for 65 and 66
w('  born_short: "5b · BORN RUNS R4 (65) and R6 (66) BY THE FORMULA PATH: the three questions (now jumps), born > CREATE jumps to the formula neuron, the value neuron gets a new shard and calls write, substitution plugs the value in, build routes (his words 10-28)" {')
w('    class: lane; grid-columns: 2; grid-gap: 30')
short_mem = {}
for tag, g in [("R4", G_COLON), ("R6", G_WHO)]:
    s_b = shard(); hit(41); s_q1 = shard(); hit(G_KNOW); s_q2 = shard(); hit(G_REM); s_q3 = shard(); hit(G_SHAPE)
    s_v = shard(); hit(18); s_w2 = shard(); hit(43); s_sub = shard(); hit(54); s_cp = shard(); hit(44); s_bld = shard(); hit(40); s_o = shard(); hit(60)
    hit(4); hit(G_FORM)
    short_mem[g] = s_bld
    open_col(tag, f"{tag}: born {g}", "    ")
    node("b41", "41 · born", "neuron", [(f"s{s_b}", f"{g} > 67 | - | 51 ask")], f"The same born neuron, a new shard for this run: arrived from {g}. Every run begins with the three questions (his words 10-28), so it goes on to 67 (know). Spawns the ask run (51).", "      ")
    node("q1", "67 · know (formula neuron)", "built", [(f"s{s_q1}", "41 > 68 | - | -"),("cell","born: known")], "The question is a jump now: the formula neuron born in lane 2, variables plugged in.", "      ")
    node("q2", "68 · remember (formula neuron)", "built", [(f"s{s_q2}", "67 > 69 | - | -"),("cell",f"memory of a born run: 40.s{s_build2}")], "", "      ")
    node("q3", "69 · shape (formula neuron)", "built", [(f"s{s_q3}", "69 > 4 | - | -"),("cell","formula proven: 70 > the formula path")], "His words 10-28: 'uses the variable formula path or the shortcut path if the variable formula path is not found yet'.", "      ")
    node("c4", "4 · CREATE", "hit", [(f"s{shs1[0]}", f"41 > 3 | - | -   jump > 70.s{s_f}")], f"The same shard 4.s{shs1[0]} the long run wrote, now carrying the jump laid by back population: the long run is skipped. 10-08: 'if I know where I am standing I can hop to any point in my brain in one step... all the work was done at learning, not at runtime'.", "      ")
    node("f70", "70 · formula: create table (value)", "built", [(f"s{s_f}", "41 > 18 | 54 substitute | -")], "The formula neuron born after R2. Goes on to the value neuron; calls the substitution run.", "      ")
    node("v18", "18 · value", "neuron", [(f"s{s_v}", "70 > 54 | 43 write | -")], f"A different shard in the value neuron for each new run (his words 10-28): s{s_v} for {tag}. Its call: the write run writes the value variable, {g}, into {tag}'s sheet.", "      ")
    node("w43", "43 · write", "neuron", [(f"s{s_w2}", "18 > - | - | -")], f"Writes value = {g} into {tag}'s sheet cell value ('the formula shortcut is just to the data sheet writing the value variable', his words 10-28).", "      ")
    node("sub54", "54 · substitute", "neuron", [(f"s{s_sub}", "18 > 40 | 44 copy | -")], "'substitution run grabbing that value and plugging it into the run data sheet so a new memory node can be made or a new neuron can be made' (his words 10-28). Its call: the copy run copies the formula (R2's sheet cell formula, the receipt with the holes) into this run's sheet; the holes are filled with cell value.", "      ")
    node("cp44", "44 · copy", "neuron", [(f"s{s_cp}", "54 > - | - | -")], f"Copies R2.sheet.formula into {tag}'s sheet cell text ('the trigger of the substitution run copying into the substitution run', his words 10-28).", "      ")
    node("b40", "40 · build", "neuron", [(f"s{s_bld}", "54 > 60 | - | 48 memory")], f"The build neuron again, a new shard for {tag}: it ends the run, so it carries another memory node. The build neuron now holds memory nodes for R2, {tag}, ...", "      ")
    node("o60", "60 · out", "neuron", [(f"s{s_o}", "40 > - | - | -")], f"The port: the product and the key ({tag} | reply | 40 | t) go to mother.", "      ")
    node("m", f"memory node on 40.s{s_bld} ({tag})", "mem", [("run",tag),("input",f"receipt: 41.s{s_b} 67.s{s_q1} 68.s{s_q2} 69.s{s_q3} 4.s{shs1[0]} 70.s{s_f} 18.s{s_v} 54.s{s_sub} 40.s{s_bld} 60.s{s_o}"),("source",f"R1 (no gate at {g})"),("c_value",str(g)),("c_text",f"> R2.formula with {g} in the holes"),("c_reply","ok")], "A separate memory node on a separate ending shard of the same neuron 40, with its own sheet inside (his words 10-28). 10 hits instead of 99.", "      ")
    node("tl", f"timeline row: t | {tag} > 40.s{s_bld} | 41 {g}", "tl", None, "", "      ")
    edge(f"b41.s{s_b}", f"q1.s{s_q1}", "hop", None, "      "); edge(f"q1.s{s_q1}", f"q2.s{s_q2}", "hop", None, "      "); edge(f"q2.s{s_q2}", f"q3.s{s_q3}", "hop", None, "      ")
    edge(f"q3.s{s_q3}", f"c4.s{shs1[0]}", "hop", "formula path", "      ")
    edge(f"c4.s{shs1[0]}", f"f70.s{s_f}", "jump", "jump", "      ")
    edge(f"f70.s{s_f}", f"v18.s{s_v}", "hop", None, "      ")
    edge(f"v18.s{s_v}", f"w43.s{s_w2}", "call", None, "      ")
    edge(f"f70.s{s_f}", f"sub54.s{s_sub}", "call", None, "      ")
    edge(f"sub54.s{s_sub}", f"cp44.s{s_cp}", "call", None, "      ")
    edge(f"w43.s{s_w2}", "m", "fill", f"value = {g}", "      ")
    edge(f"cp44.s{s_cp}", "m", "fill", "text", "      ")
    edge(f"sub54.s{s_sub}", f"b40.s{s_bld}", "hop", None, "      ")
    edge(f"b40.s{s_bld}", f"o60.s{s_o}", "hop", None, "      ")
    edge(f"o60.s{s_o}", "m", "route", "mother > prompt > ok > encoder > reply", "      ")
    edge("m", "tl", "trig", None, "      ")
    close("    ")
    tl_rows.append((f"r{len(tl_rows)+1}", f"t | {tag} born {g} > 40.s{s_bld} | 41 {g}"))
close("  ")
# B column tail: neurons gaining shards (emitted after sources, since counts depend) -> deferred
L = _saved

# ================================================================= COLUMN C
C = []
L = C
w('C: "" {')
w('  class: column; grid-columns: 1; grid-gap: 70')
srcs = ["wn","gcide","mw","mwt","moby","map","sqldoc"]
def src_lines(word): return {k: [r for r in sat.get(k, []) if r[0] == word] for k in srcs}
w('  sources: "6 · SOURCE RUNS R3 (64), R5 (65), R7 (66): the newborn\'s first memory is its definition, pulled from every source and compared (10-23 P5-9; 10-25 msg 51). Each has its own sheet; the return carries the key; a failed cell steps back to the choice (his words 10-28)" {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
expanded_done = False; ret_total = 0; ret_counts = {}
for g, word in [(G_DEFINE,"define"),(G_COLON,":"),(G_WHO,"who")]:
    lines = src_lines(word); s_ask = shard(); hit(51); s_o = shard(); hit(60)
    open_col(f"src{g}", f"source run for {g} · {word}", "    ")
    node("a51", "51 · ask", "neuron", [(f"s{s_ask}", "41 > 60 | - | -")], f"The ask run, spawned by the born run. Declares its own sheet: one cell per source and compile; declares on R1's sheet the cell def.{g}. Assembles the ask from the encoder's label of the newborn and goes on to 60 (out). The run names the sources; mother carries the ask to each inbox and decides nothing (10-23 P2; 10-23 01:28).", "      ")
    node("keyrow", "the key on the out mailbox", "key", [("run",f"R{ {G_DEFINE:3,G_COLON:5,G_WHO:7}[g] }"),("cell","one per source"),("gate","51 ask"),("why",f"R1 needs def.{g}")], "The key travels to each source and back with each answer (his words 10-28).", "      ")
    rows = [(f"c_{k}", f"{len(lines[k])} line(s)" if lines[k] else "0: empty") for k in srcs]
    node("sh", f"sheet of the source run ({word})", "sheet", rows + [("c_compile", f"> definition node of {g}")], "The source run's own sheet: a cell per source, filled by each return; when no declared cell is empty the compile runs (10-26 03:50). Counts are the real lines in the archived slice (tries/11 sat172.json).", "      ")
    edge(f"a51.s{s_ask}", "sh", "readw", None, "      ")
    nret = 0
    for k in srcs:
        for j, r in enumerate(lines[k]):
            nret += 1; ret_total += 1
            words = (r[3] or r[2]).split()
            syms = []
            for t, wd in enumerate(words):
                syms.append(wd)
                if t < len(words)-1: syms.append(" ")
            newcount = len(set(s for s in words if s not in enc))
            rid = f"ret_{k}{j}"
            flag = " The run checks what came back: WordNet answered with the acronym WHO, the agency, a neighbour of the symbol asked (10-22 rev17: dictionaries answer with neighbours). The cell is filled and the compile keeps it apart." if (k == "wn" and word == "who") else ""
            tt = f"Return run {nret} for {word}, from {k}: the source's line delivered to the encoder arrives as a run of gates with the key (10-25 msg 37: 'return from define : {word} from source {k} run /build the definition as gates'). {len(syms)} hits; {newcount} symbols had no gate and are born on the way by the formula path (the cascade, 10-23 P4). The run ends at its last symbol: its memory node sits there; the definition node row for {g} points at this receipt. Line: " + r[2][:200] + flag
            if k == "mw" and word == "who" and j == 1 and not expanded_done:
                expanded_done = True
                w(f'      {rid}: {qd(f"return run {nret} · {k}, expanded: {len(syms)} hits, {newcount} born here")} {{')
                w('        class: col; grid-columns: 2; grid-gap: 14')
                prev_g = 60; hsh = []; hids = []
                per = -(-len(syms)//2)
                for c in range(2):
                    w(f'        c{c}: "" {{'); w('          class: col; grid-columns: 1; grid-gap: 14')
                    for i in range(c*per, min((c+1)*per, len(syms))):
                        s = syms[i]; gg = G(s); sh_ = shard(); hit(gg); hsh.append(sh_); hids.append((c, f"h{i}"))
                        nxt = G(syms[i+1]) if i+1 < len(syms) else 0
                        cls = "newborn" if (s != " " and gg > 70 and s in ("that","whoever")) else "hit"
                        note = ""
                        if s == ":": note = f" Gate 65 exists from this line; its second shard is written here: arrived from {prev_g}, remainder {nxt}. Two shards, two arrivals: picked deterministically by before and remainder (lane 7b)."
                        if cls == "newborn": note = f" Gate {gg} had no gate: born here by the formula path, then sourced in turn (not drawn: the same shape as this lane)."
                        node(f"h{i}", f"{gg} · {NAME(s)}", cls, [(f"s{sh_}", f"{prev_g} > {nxt if nxt else '-'} | - | {'48 memory' if not nxt else '-'}")], f"hit {i+1} of {len(syms)}: gate {gg} ({NAME(s)}), shard s{sh_}, arrived from {prev_g}." + note + (" No remainder: the return run ends here; its memory node is what the definition node row points at." if not nxt else ""), "          ")
                        prev_g = gg
                    close("        ")
                for i in range(1, len(syms)):
                    ca, ha = hids[i-1]; cb, hb = hids[i]
                    edge(f"c{ca}.{ha}.s{hsh[i-1]}", f"c{cb}.{hb}.s{hsh[i]}", "hop", None, "        ")
                last_g = G(syms[-1]); cl, hl = hids[-1]
                node("m", f"memory node on {last_g}.s{hsh[-1]} (return run {nret})", "mem", [("run",f"ret{nret}"),("input","receipt: " + " ".join(str(x) for x in hsh)),("source",f"mother ({k}), key R7 | c_{k}")], "The return run ended at its last symbol; its memory row sits there (10-15 21:50). The definition node of 66 points at it.", "        ")
                edge(f"c{cl}.{hl}.s{hsh[-1]}", "m", "trig", None, "        ")
                close("      ")
                edge(rid, "sh", "fill", f"fills c_{k}", "      ")
            else:
                for s in words: gate(s)
                for s in syms: hit(G(s))
                node(rid, f"return run {nret} · {k}: {len(syms)} hits, {newcount} born, ends > memory", "hit", None, tt, "      ")
                edge(rid, "sh", "fill", f"fills c_{k}", "      ")
            edge(f"a51.s{s_ask}", rid, "route", ("60 out + key > mother > each inbox > its trigger > outbox > mother > encoder + key" if nret == 1 else None), "      ")
    ret_counts[g] = nret
    if nret:
        s_comp = shard(); hit(52)
        node("c52", "52 · compile (diff and similar)", "neuron", [(f"s{s_comp}", "50 > 43 | 46 read, 55 compare, 44 copy, 45 cut | -")], "When no declared cell is empty the larger formula runs: 'diff those so that I hopefully can get the most accurate definition... diff and similar those... build the definition table, and build the relationships from the definition table' (10-23 P5-9). It reads the return runs, compares them, copies what agrees, cuts what differs, and the write run lays the definition node rows: the neuron's first memory. [open] see lane 12.", "      ")
        edge("sh", f"c52.s{s_comp}", "trig", "complete", "      ")
    else:
        node("empty", "every source cell stays 0: no source has :", "open", None, "In the archived slice no source holds ':' (the measured source holds ; and ( but not :). 10-27 03:52: 'just because the cell doesn't populate it doesn't end the run, it gives the brain reason to search harder'.", "      ")
        edge("sh", "empty", "trig", "no cell fills", "      ")
        # the step-back path
        node("sb1", "STEP BACK to the choice: which sources to ask (the run had a choice here)", "his", None, "His words 10-28: 'if the new step, or the next step fails to provide the run data sheet with data then the run must be re ran via different substitution theory or using a different formula, via process of elimination theory ... meaning there is a check back or even step back to a run that had a choice'.", "      ")
        node("sb2", "the failed choice is remembered from the timeline and eliminated: these 7 sources, asked for 65, answered nothing", "tl", [("r", "t4 | R5 sources 65: 0 returns | 51 65  (eliminated)")], "His words 10-28: 'the failed choice is remembered from the time line and eliminated as a possible run answer because it was either determined incorrect or didn't provide useable cell data'.", "      ")
        node("sb3", "before answering 'define?' to the user: ask the sixth 'why?'", "sixth", [("ask","R5: why did def.65 not fill?"),("sixth","your run data sheet at R1 is missing cells def.65; suggest rerun to populate")], "His words 10-28: 'before a run answers define? back to the user, it asks the sixth why define? and the sixth replies your run data sheet at location x,y,z is missing cells ???,???,??? suggest rerun to populate those cells, or it calls to the sixth or the guessing brain for a balance/progression check'.", "      ")
        node("sb4", "rerun by a different substitution: ask for : in its code use (the SQL docs, the measured source): still 0", "note", None, "Process of elimination: the eliminated choice is not tried again; a different formula or substitution is. In the archived slice the SQL sources hold ; and ( but not : so this too answers nothing.", "      ")
        node("sb5", "> the guessing brain (lane 11b): a guess, labeled, with a confidence; belief at most 50% on first use", "guess", [("def_65","a guess: the hole mark | confidence c | belief <= 50%")], "10-23 P5-9: memory, then state, then sources, then a guess. His words 10-28: 'a 99 percent confidence factor on a run that is use for the first time can never have a belief factor of over 50%'.", "      ")
        edge("empty", "sb1", "back", "step back", "      ")
        edge("sb1", "sb2", "back", None, "      ")
        edge("sb2", "sb3", "route", "through mother", "      ")
        edge("sb3", "sb4", "back", "rerun", "      ")
        edge("sb4", "sb5", "route", None, "      ")
    close("    ")
close("  ")
tl_rows.append(("r5", f"t2 | R3 sources 64: {ret_counts[G_DEFINE]} return runs, compile | 51 64"))
tl_rows.append(("r7", "t4 | R5 sources 65: 0 returns (eliminated) > sixth > guess | 51 65"))
tl_rows.append(("r9", f"t6 | R7 sources 66: {ret_counts[G_WHO]} return runs, compile | 51 66"))

# ---- lane 7: the newborns after
w('  after: "7 · THE THREE NEWBORNS AFTER THE LINE: DNA, definition node with its rows and relationships, memory nodes per ending shard" {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
d64 = src_lines("define"); d66 = src_lines("who")
open_col("n64", "64 · define", "    ")
node("dna", "64 · define  DNA", "newborn", [(f"s{s_main['a']}", "1 > 3 | - | -")], "One row so far. No trigger yet: define has no action until a formula is taught or learned for it (10-25 msg 51: define : dog = look up definition memory, print).", "      ")
rows = []; n = 0
for k in srcs:
    for r in d64[k]:
        n += 1
        if r[2].startswith("like "):
            rows.append((f"rel{n}", f"like > {gate(r[2][5:].strip())} ({r[2][5:].strip()})"))
        else:
            rows.append((f"def{n}", f"{k}: > return run (…{r[2][:28]}…)"))
node("defn", "definition node of 64", "defn", rows, "Rows laid by the compile from the real source lines: wn 1, gcide 1, mw 2 definitions; mwt 4, moby 3, map 1 'like' lines, which are relationship rows: like > the gate of the related symbol (born as it arrived). 10-23 P4: 'any section that can have a relationship to something else is a self-fulfilling relationship section. All of them.'", "      ")
node("mem_note", "no memory node yet: no run has ended at 64", "note", None, "Memory nodes exist only on shards that end runs (his words 10-28; 10-23 P2 B2).", "      ")
edge("dna", "defn", "readw", "born with it", "      ")
close("    ")
open_col("n65", "65 · :", "    ")
node("dna", "65 · :  DNA", "newborn", [(f"s{s_main['c']}", "3 > 3 | - | -"),("s_ret", f"{gate('that')} > {gate('whoever')} | - | -  (from the mw return run)")], "Two rows after this line: R1's (space > space) and the mw return run's (that > whoever). Two arrivals, two rows: the pick is by before and remainder (§12 law 13). A third kind of row comes when : is used as the hole mark in a build run. When two rows share one arrival, the call column holds the inspection run (lane 8).", "      ")
node("defn", "definition node of 65", "defn", [("def", "guess: the hole mark | confidence c | belief <= 50% (from the guessing brain)"),("sqldoc", "0: no source in the slice holds :")], "No source in the archived slice answers for ':'. After the step back and the sixth, the guessing brain's guess fills the cell, labeled, and the output asks the user correct?/incorrect?/progression?/degression? (his words 10-28).", "      ")
edge("dna", "defn", "readw", None, "      ")
close("    ")
open_col("n66", "66 · who", "    ")
node("dna", "66 · who  DNA", "newborn", [(f"s{s_main['e']}", "3 > - | - | 48 memory"),("later", "(later: who is, who are, who did, who was: a row each)")], "s%d ends R1. 10-22 rev17: who is, who are, who did and who was each fire a different row inside the one neuron for who, each pointing at a different formula. 10-24: 'Go get me some coffee now... me who, coffee what...'." % s_main['e'], "      ")
rows = []; n = 0
for k in srcs:
    for r in d66[k]:
        n += 1
        rows.append((f"def{n}", f"{k}: > return run (…{r[2][:30]}…)" + (" [kept apart: the WHO agency]" if k == "wn" else "")))
rows += [("rel1", f"? > {gate('whom')} (whom) named beside who by gcide"),("rel2", f"? > {gate('whoever')} (whoever) named by mw"),("rel3", f"? > {gate('person')} (person) named by mw")]
node("defn", "definition node of 66", "defn", rows, "Rows from the real source lines: wn 1 (the WHO agency, kept apart by the check), gcide 1, mw 2. The relationship rows: the symbols the definitions name beside who; their KIND is not decided here (law 5: no facts from the builder's head).", "      ")
mem_rows = [("run","1"),("input","64 3 65 3 66 (receipt rows h1..h5)"),("source","user"),("c_clock","t0"),("c_speaker","user, heard"),("c_know","0 (67)"),("c_remember","0 (68)"),("c_shape","0 (69)"),("c_path","long"),("c_gate_64","64"),("c_def_64","> definition node of 64"),("c_gate_65","65"),("c_def_65","a guess, labeled, confidence c, belief <= 50%"),("c_gate_66","66"),("c_def_66","> definition node of 66"),("c_say","> what was said (R8), the guess labeled")]
node("m1", f"memory node on 66.s{s_main['e']} (R1, the main run)", "mem", mem_rows, "R1's memory row, on the shard of who that ended it, with the whole data sheet inside (10-26 03:50; his v4 run_sheet). Each cell was declared by the trigger that tripped and filled by a return.", "      ")
node("m_more", "another run ending at a different shard of who gets its own memory node here", "note", None, "His words 10-28: 'some neuron might have many memory tables because many of their dna shards end runs... each will have its own memory table and data runsheet in it'.", "      ")
edge("dna", "defn", "readw", None, "      ")
edge(f"dna.s{s_main['e']}", "m1", "trig", "no remainder: 48 memory write run", "      ")
close("    ")
close("  ")
edge("sources.src64.c52", "after.n64.defn", "fill", "lays the rows: first memory", "  ")
edge("sources.src66.c52", "after.n66.defn", "fill", "lays the rows: first memory", "  ")
edge("sources.src65.sb5", "after.n65.defn", "fill", "the guess, labeled", "  ")
edge("after.n64.defn", "after.n66.m1", "fill", "def.64", "  ")
edge("after.n66.defn", "after.n66.m1", "fill", "def.66", "  ")

# ---- lane 8: inspection
w('  inspect: "8 · THE INSPECTION RUN: a row that decides which row to hit when more than one shard answers the same arrival (10-23 P2 B1; P3 B1). Not called on this line." {')
w('    class: lane; grid-columns: 2; grid-gap: 30')
s_i = shard(); hit(46)
open_col("i1", "the gate", "    ")
node("gate_x", "a gate with two shards for one before", "neuron", [("sA","x > y | 46 inspect | -"),("sB","x > z | 46 inspect | -")], "When the hop's read by before + remainder head cannot pick one shard, the call column holds the inspection run. 10-23 P2 B1: 'I need to find the noun, or the verb and the noun, or see if there's any adjectives in this sentence, because that determines what row I actually have to hit inside my node... it might go back to that node and hit a different shard'.", "      ")
close("    ")
open_col("i2", "the call", "    ")
node("r46", "46 · read (the inspection run)", "neuron", [(f"s{s_i}", "x > x | 55 compare | -")], "1. reads the run's input row: the symbols after and before this gate (10-20 00:31); 2. reads their definition nodes: class, tense, perspective; 3. reads the run's sheet: speaker, what is known, memories; 4. compares; its answer is the shard to hit; 5. returns to the gate, which hits THAT shard (10-23 P3 B1). His words 10-28: 'pick the correct one deterministically such that a meaning of the neuron will have many different uses, and or changed meanings based on the modifiers in the script (or sentence)(or context)(or memories)'.", "      ")
node("sh", "inspection sheet", "sheet", [("c_after","gates after"),("c_before","gates before"),("c_classes","from their definition nodes"),("c_memories","from memory nodes"),("c_answer","> the shard to hit")], "", "      ")
close("    ")
edge("i1.gate_x.sA", "i2.r46", "call", "call", "    ")
edge("i2.r46", "i2.sh", "readw", None, "    ")
edge("i2.sh", "i1.gate_x.sB", "call", "re-hit that shard", "    ")
close("  ")

# ---- lane 11: the sixth
w('  sixth: "11 · THE SIXTH: its own brain; the inner voice that observes or oversees all the runs and asks questions (his words 10-28; 10-23 P2). Reaches the main brain only through mother and its mailbox." {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
open_col("sees", "what it sees (through mother, read runs of its own)", "    ")
node("see1", "the main brain's memory nodes and their sheets", "sixth", [("reads","every run data sheet: which cells are 0")], "His words 10-28: 'your run data sheet at location x,y,z is missing cells'. 10-23 03:18: 'its own questions and prompts from observations basically (sight) of the brain'.", "      ")
node("see2", "the timeline", "sixth", [("reads","receipts, the failed choices, what was eliminated")], "", "      ")
node("see3", "the DNA rows hit and the receipts", "sixth", [("reads","which shard was hit, from which arrival")], "'am I using the correct dna shard' (his words 10-28).", "      ")
node("see4", "anything it cannot see bothers it", "his", None, "His words 10-28: 'anything the sixth cannot see should bother it, what did I do there? how did that happen? can I do that on my own?'. So nothing is written by physics the brain cannot read (lane 3).", "      ")
close("    ")
open_col("asks", "its questions: each is a run in sixth.db (its own neurons)", "    ")
for i, (q, tt) in enumerate([
  ("why am I doing it that way?", "His words 10-28."),
  ("is there a better way?", "His words 10-28; 10-23 P2: 'tries to find more efficient'."),
  ("am I using the correct dna shard?", "His words 10-28."),
  ("does that answer seem like progression, balance, make sense? or regression?", "His words 10-28; 10-23 P5-9 B1: desired vs current vs new."),
  ("what data seems wrong that should be corrected?", "His words 10-28."),
  ("what process could be more efficient?", "His words 10-28."),
  ("why did the cell not populate?", "10-27 03:52."),
  ("balance check of the guessing brain's answer against the expected shape of output", "His words 10-28: 'has its last step or answer checked by another brain for balance of output to expected shape of output'.")]):
    node(f"a{i}", q, "sixth", [("run", f"sixth.db run {i+1}")], tt, "      ")
close("    ")
open_col("acts", "what it sends back", "    ")
node("x1", "answer to a run's 'why?': the missing cells, suggest rerun", "mail", None, "His words 10-28: 'the sixth replies your run data sheet at location x,y,z is missing cells ???,???,??? suggest rerun to populate those cells'.", "      ")
node("x2", "its own line into its mailbox, speaker = sixth: a new run through the same hallway", "mail", None, "10-16 05:50: 'at first we would have to prompt these, but later many of these are written by the sixth'. 10-22 rev17: whatever SQL it writes into the main brain is told, not learned.", "      ")
node("x3", "to the guessing brain: why the guess was wrong, with reasons", "mail", None, "10-23 03:18: 'if that word comes back was wrong from the sixth with reasons why it didn't work, then the guessing brain can back prop again over the adjusted corpus'.", "      ")
edge("x1", "x2", "not", None, "      ")
close("    ")
edge("sees.see1", "asks.a6", "readw", None, "    ")
edge("asks.a6", "acts.x1", "trig", None, "    ")
edge("asks.a7", "acts.x3", "trig", None, "    ")
close("  ")
edge("sources.src65.sb3", "sixth.asks.a6", "route", "R5 asks: why?", "  ")
edge("sixth.acts.x1", "sources.src65.sb3", "route", "the reply", "  ")

# ---- lane 11b: the guessing brain
w('  guessing: "11b · THE GUESSING BRAIN: a hand-built llm over a small corpus that learns on the fly; every answer a labeled guess with a confidence; belief grows only by use, success and the user\'s answer (his words 10-28)" {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
open_col("parts", "its parts (his words 10-28)", "    ")
node("p1", "a small corpus, expanded or eliminated by the answers it finds", "guess", [("corpus","what the main brain sent: the run, the sheet, the sources' nothing")], "His words 10-28: 'check state to eliminate answers and expand or eliminate corpus based on the answers it finds'. 10-23 03:18: after a corpus it saves the useful bits, the rest goes to storage in the source db.", "      ")
node("p2", "context, qkv, weights, hidden layers, back propagation", "guess", [("state","what it tried before, and why each was wrong")], "His words 10-28: 'built more like you, or a llm with qkv, weights, and corpus, hidden layers, back propagation, context, all the things ... the biggest difference is that it's a hand built llm because no llm work this way over a small corpus that can learn on the fly'. 10-23 P5-9: QKV is the guessing piece.", "      ")
node("p3", "its last step is checked by another brain (the sixth) for balance of output to the expected shape of output", "guess", None, "His words 10-28.", "      ")
close("    ")
open_col("table", "its answer: a guess, labeled", "    ")
node("g1", "the guess for def.65", "guess", [("guess","the hole mark (a reading of : in a build run)"),("confidence","c (its own number)"),("belief","<= 50% on first use, whatever c is"),("times_used","0"),("times_solved","0"),("user","asked: correct? incorrect? progression? degression?")], "His words 10-28: 'label the entirety of it's answer as a guess with a confidence factor on the guess... a 99 percent confidence factor on a run that is use for the first time can never have a belief factor of over 50%, and what changes that is the success of the run (actually allows an output) and the response from the user, that guess or this guess seems correct or incorrect.... all guesses in an output are labeled and asked correct?/incorrect?/progression?/degression? <-- that answer is what helps adjust the weights and build the confidence to change a guess into a belief plus the number of times that guess is used and it solves the problem'.", "      ")
node("g2", "how a guess becomes a belief", "his", None, "His words 10-28: the success of the run (it allows an output) + the user's correct/incorrect/progression/degression + the number of times the guess is used and solves the problem. 10-23 P5-9: guesses announced, never lost; 10-15 21:17: 'Always state that this is a guess or belief not known source truth'.", "      ")
close("    ")
open_col("loop", "the loop with the sixth", "    ")
node("l1", "guess > sixth: balance against the expected shape", "mail", None, "", "      ")
node("l2", "wrong, with reasons > back prop over the adjusted corpus > guess again until it balances", "guess", None, "10-23 03:18.", "      ")
node("l3", "the guess fills the cell, labeled; the output carries the label and the question to the user", "mail", None, "", "      ")
edge("l1", "l2", "back", "wrong", "      ")
edge("l2", "l1", "route", "again", "      ")
edge("l1", "l3", "fill", "balanced", "      ")
close("    ")
edge("parts.p2", "table.g1", "trig", None, "    ")
edge("table.g1", "loop.l1", "route", None, "    ")
close("  ")
edge("sources.src65.sb5", "guessing.parts.p1", "route", "the question, with the key", "  ")
edge("guessing.loop.l3", "sources.src65.sb5", "fill", None, "  ")
edge("guessing.loop.l1", "sixth.asks.a7", "route", None, "  ")

# ---- lane 13: tools compounding
w('  tools: "13 · TOOLS COMPOUND: the hand-laid tools, and what the brain builds from them inside this first run (his words 10-28: tool 1 + tool 2 makes tool 3; the stick, the sharp stick, the sinew, the bow)" {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
open_col("hand", "hand laid (the core, lane 0)", "    ")
for cid, lab in [("t46","46 · read"),("t43","43 · write"),("t44","44 · copy"),("t45","45 · cut"),("t55","55 · compare"),("t61","61 · find"),("t42","42 · hop"),("t16","16 · call"),("t17","17 · spawn"),("t47","47 · clock"),("t60","60 · out (say to mother)"),("tsql","4..39 · the SQL words and marks"),("t41","41 · born"),("t40","40 · build")]:
    node(cid, lab, "neuron", None, "A hand-laid tool: its own table, hand-laid DNA rows, a definition node from the SQL docs. His words 10-28: which of these truly must be hand laid is found as the brain grows: 'hand laid that tool is not wrong, but was just out of order'.", "      ")
close("    ")
open_col("made", "built by the brain in this run (long runs first, then formula neurons)", "    ")
built = [("b67","67 · know = read + compare + write","SQ1 (lane 2)"),("b68","68 · remember = read + compare + write","SQ2"),("b69","69 · shape = read + find + compare + write","SQ3"),("b70","70 · create table (value) = the SQL words + value + build + out","the born run's formula (lane 5)"),("b51","the ask = out + the key","lane 6"),("b52","the compile = read + compare + copy + cut + write","lane 6"),("b53","the decide formula = read + compare + write","lane 5"),("b54","the substitution = copy + write","lane 5b"),("b48","the memory write = copy + write","lane 9"),("b49","the timeline write = write","lane 9"),("b56","the say = read the sheet + compare (balance) + out","lane 10")]
for cid, lab, where in built:
    node(cid, lab, "built", None, f"Built from the hand-laid tools in this run; {where}. His words 10-28: 'use tool 1 to build tool 2 or maybe tool 2 must be handlaid, but tool 1 plus tool 2 might make tool 3, tool 1 minus tool 2 might make tool 4...'.", "      ")
close("    ")
open_col("next", "and then (not on this line)", "    ")
node("n1", "tool 3 * tool 1 - tool 2 = tool 11; tool 11 + tool 1 / tool 7 * tool 2 = tool 12", "his", None, "His words 10-28: 'it compounds as it expands... the idea is the handlay the most useful or diverse tools first that the brain can build its tools from'.", "      ")
node("n2", "the stick, the sharp stick, sinew + rock, sinew + stick + stick, needle + thread, rock + rock + smash, fire + earth, copper + fire + hammer", "his", None, "His words 10-28, the metaphor: 'give the nuts and bolts, learn to put the nuts and bolts together in different ways to make the tools that work now, but can be improved later to be the better tools'.", "      ")
node("n3", "a tool found to be buildable later is not wrong, just out of order", "his", None, "His words 10-28: 'as you thought this tool needed to be hand laid but the guessing or sixth or yourself see a different way that could build that tool from inside the brain once something else is built by the brain'.", "      ")
close("    ")
edge("hand.t46", "made.b67", "builtw", None, "    ")
edge("hand.t55", "made.b67", "builtw", None, "    ")
edge("hand.t43", "made.b67", "builtw", None, "    ")
edge("hand.tsql", "made.b70", "builtw", None, "    ")
edge("hand.t40", "made.b70", "builtw", None, "    ")
edge("hand.t44", "made.b54", "builtw", None, "    ")
edge("hand.t60", "made.b51", "builtw", None, "    ")
edge("made.b70", "next.n1", "builtw", None, "    ")
close("  ")
close("")   # end column C
L = _saved

# ================================================================= COLUMN B tail: neurons gaining shards
L = B
w('  grow: "7b · NEURONS GAINING SHARDS as the brain grows: the same neuron, many rows, one picked deterministically by before and remainder, and by the modifiers through the inspection run (his words 10-28)" {')
w('    class: lane; grid-columns: 4; grid-gap: 30')
node("g3", "3 · space after this line", "neuron", [("rows", f"{hits_per_gate.get(3,0)} hits on this line: one row per distinct (before, remainder)"),(f"s{s_main['b']}", "64 > 65 | - | -"),(f"s{s_main['d']}", "65 > 66 | - | -"),("s113", "4 > 5 | - | -  (CREATE > TABLE, the born run)"),("more", "and every pair the born run and the return runs crossed")], f"The space is hit {hits_per_gate.get(3,0)} times on this line (the main run, the long born run, the return runs). Each distinct before and remainder is a row; the same pair is the same row hit again, counted (10-22 rev17). The pick is deterministic: before and the remainder head.", "    ")
node("g18", "18 · value: one shard per run that used the hole", "neuron", [(f"s{shs1[i_val1]}", "6 > 6 | 43 write | -  (R2, statement 1)"),(f"s{shs2[i_val2]}", "6 > 3 | 43 write | -  (R2, statement 2)"),("s_R4", "70 > 54 | 43 write | -  (R4)"),("s_R6", "70 > 54 | 43 write | -  (R6)"),("more", "one per newborn of the cascade")], "His words 10-28: 'a different shard in the value neuron for each new run'.", "    ")
node("g40", "40 · build: one ending shard, one memory node, per run it ends", "neuron", [(f"s{s_build2}", "10 > 60 | - | 48 memory  (R2)"),(f"s{short_mem[G_COLON]}", "54 > 60 | - | 48 memory  (R4)"),(f"s{short_mem[G_WHO]}", "54 > 60 | - | 48 memory  (R6)"),("more", "one per born run of the cascade")], "His words 10-28: 'some neuron might have many memory tables because many of their dna shards end runs'.", "    ")
node("g65", "65 · : three kinds of row, three uses", "neuron", [(f"s{s_main['c']}", "3 > 3 | - | -  (the ask mark, this line)"),("s_ret", f"{gate('that')} > {gate('whoever')} | - | -  (inside a definition)"),("s_hole", "6 > 18 | - | -  (later: the hole mark in a build run: its SQL action)")], "His words 10-28: 'a meaning of the neuron will have many different uses, and or changed meanings based on the modifiers in the script (or sentence)(or context)(or memories) that it encounters'. 10-27 05:37: in sql ':' has an action we know, but a different dna row might not have the same action.", "    ")
node("g66", "66 · who: rows to come", "neuron", [(f"s{s_main['e']}", "3 > - | - | 48 memory  (define : who)"),("s_is", "66 > is | ? | -  (who is ...: a different formula)"),("s_are", "66 > are | ? | -"),("s_did", "66 > did | ? | -"),("s_was", "66 > was | ? | -")], "10-22 rev17: 'Who is, who are, who did and who was each fire a different row inside the one neuron for who, and each row points at a different formula: a different place to look, a different thing to read, a different thing to say.' The trigger of each is found by test, not assigned (10-22 rev17).", "    ")
node("g4", "4 · CREATE", "neuron", [(f"s{shs1[0]}", f"41 > 3 | - | -   jump > 70.s{s_f}  (from born)"),(f"s{shs2[0]}", "10 > 3 | - | -  (after ; inside the born run)"),("s_core", "(its hand-laid rows: the core word function, 10-23 P2 B3)")], "10-23 P2 B3: 'create, at certain row, is the core word function... there might be 70 rows that are all core word functions of the word create, versus say word functions of the word create'.", "    ")
node("pick", "the deterministic pick: before + remainder head; when two rows share them, the inspection run (lane 8) reads the modifiers, the context, the memories and picks", "his", None, "His words 10-28.", "    ")
close("  ")
close("")   # end column B
L = _saved

# ================================================================= COLUMN A tail: end, output, open
w('  ending: "9 · THE END OF R1 and THE TIMELINE: no remainder > memory write run > timeline write run > stop (10-26 03:50)" {')
w('    class: lane; grid-columns: 2; grid-gap: 30')
s_mw = shard(); hit(48); s_tw = shard(); hit(49)
open_col("writes", "the two write runs", "    ")
node("m48", "48 · memory (write run)", "neuron", [(f"s{s_mw}", "66 > 49 | 44 copy | -")], f"A copy run the ending shard excites; the trigger writes nothing itself (10-26 03:59). It lays run_memory(1, receipt, user) on 66.s{s_main['e']} and the run_sheet rows inside it (his v4 shape).", "      ")
node("t49", "49 · timeline (write run)", "neuron", [(f"s{s_tw}", "48 > - | - | -")], "By a trigger hop, never a sweep (10-23 P3 B1). One row: the clock reading, the receipt pointer, a couple of key words (10-16 06:40). Then it stops (10-26 03:50).", "      ")
edge(f"m48.s{s_mw}", f"t49.s{s_tw}", "trig", "memory > timeline", "      ")
close("    ")
tl_rows.append(("r10", f"t7 | R1 define : who > 66.s{s_main['e']} | 64 66"))
tl_rows.append(("r11", "t8 | R8 say > 56.s | 56"))
tl_rows.sort(key=lambda r: int(r[0][1:]))
node("timeline", "TIMELINE after this line", "tl", tl_rows, "A row per run that ended, in the order the drawing says they happen. The cascade's born runs add their own rows, not listed. The failed choice of R5 stays in the timeline, marked eliminated (his words 10-28).", "    ")
edge(f"writes.t49.s{s_tw}", "timeline", "fill", "one row; then stops", "    ")
close("  ")
edge("main.hall.he", "ending.writes.m48", "trig", "no remainder", "  ")

w('  output: "10 · OUTPUT: a separate mechanism from the same memory table (10-26 03:50). Before \'define?\' goes to the user the run asks the sixth why; guesses go out labeled with the question correct? incorrect? progression? degression?" {')
w('    class: lane; grid-columns: 3; grid-gap: 30')
s_say = shard(); hit(56)
open_col("o1", "from the memory table", "    ")
node("when", "no declared cell of R1 empty? (def.65 filled by the labeled guess)", "pick", None, "10-26 03:50: when the run's data table is complete the run can populate and finish its larger formulas.", "      ")
node("formulas", "the larger formulas over the sheet (substitute the cells as variables)", "note", None, "10-23 P3 B2. On a fresh brain nothing is bound to define yet; the material is the sheet: the compiled definitions of 64 and 66 and the labeled guess for 65.", "      ")
node("balance", "makes sense: desired vs current vs new; progression or regression", "note", None, "10-23 P5-9 B1. Not balanced: step back to the decision that picked this path and take another row; the failed try stays in memory marked wrong (10-22 rev17; his words 10-28).", "      ")
edge("when", "formulas", "hop", None, "      "); edge("formulas", "balance", "hop", None, "      ")
close("    ")
open_col("o2", "before it goes out", "    ")
node("askwhy", "the run asks the sixth: why would I say 'define?'", "sixth", [("ask","R1: is this balanced? what is missing?"),("sixth","cells: def.65 is a guess; say it labeled")], "His words 10-28: 'before a run answers define? back to the user, it askes the sixth why define? and the sixth replies your run data sheet at location x,y,z is missing cells... or it calls to the sixth or the guessing brain for a balance/progression check'.", "      ")
node("s56", "56 · say", "neuron", [(f"s{s_say}", "48 > 60 | 55 compare | -")], "The say run: the reply as a tree of arrays, each pick opening the next (10-23 P3 B2); the brain chooses what it wants to say (10-27 03:52); no sentence drawn here on purpose (10-27 04:07). 10-26 05:12: the say key = the metadata on what leaves (lane 0).", "      ")
edge("askwhy", f"s56.s{s_say}", "trig", "balanced", "      ")
close("    ")
open_col("o3", "out", "    ")
node("dec", "DECODER: gates > symbols", "encoder", None, "10-23 P3 B2: just gate numbers, maybe head data.", "      ")
node("to_user", "brain > user mailbox: the answer, with the guess labeled and the question: correct? incorrect? progression? degression?", "mail", None, "His words 10-28: 'all guesses in an output are labeled and asked correct?/incorrect?/progression?/ degression? <-- that answer is what helps adjust the weights and build the confidence to change a guess into a belief'.", "      ")
node("to_sixth", "> sixth.db mailbox", "mail", None, "10-25 msg 41: run output to sixth.", "      ")
node("answer", "the user's answer comes back as a line (heard): it adjusts the guess's weights and belief; a correct raises the formula's belief too", "his", None, "His words 10-28. 10-23 P5-9 B1: taught is not believed; belief from memory, source trust, supporting knowledge.", "      ")
edge("dec", "to_user", "hop", None, "      ")
edge("to_user", "answer", "route", None, "      ")
close("    ")
edge("o1.balance", "o2.askwhy", "route", "through mother", "    ")
edge(f"o2.s56.s{s_say}", "o3.dec", "hop", None, "    ")
edge(f"o2.s56.s{s_say}", "o3.to_sixth", "spawn", None, "    ")
close("  ")
edge("ending.timeline", "output.o1.when", "trig", "the memory row exists", "  ")

w('  open: "12 · HIS ANSWERS OF 10-28 (closed) and WHAT IS STILL HIS CALL" {')
w('    class: lane; grid-columns: 2; grid-gap: 30')
open_col("closed", "closed by his words of 10-28", "    ")
for i, (t, tt) in enumerate([
 ("born inline AND step back: two cases, not one choice", "Born inline when a gate is missing (missing neuron = missing step). Step back to a run that had a choice when a cell fails; the failed choice is remembered from the timeline and eliminated; rerun by a different substitution or formula. Drawn: lane 3 and lane 6."),
 ("the receipt is written by the brain's write run into the run data sheet, never by physics", "'if physics writes the brain will not be able to see or observe what happened... run receipt is just the order of the main run plus the hops, so it's just recorded in the run data sheet as a row and columns'. Drawn: lane 3."),
 ("the sheet's physical form: his v4 brain.db (rows keyed by the run, pointed to by the memory row)", "The question explained in lane 0 (the memory table shape). His own typing of 10-27 01:17 is the answer the drawing follows."),
 ("the formula is a NEW neuron, born, relationally matched to the long run; not a row in one formula neuron", "'once the variables are determined then that row cannot live in the main run... thus a new neuron must be born'. Drawn: lane 5 (70) and lane 2 (67, 68, 69)."),
 ("the standing questions are built by the brain from the hand-laid tools, in this first run, the simplest way; every run circles back to them", "Drawn: lane 2 (the long runs and the formula neurons born), lane 5b (the jumps)."),
 ("define is not in the core: there is no simple first turn; the first run builds what it needs step by step", "'every turn even define : who or learn : who or meaning : who requires all the things in order to be done correct... give the brain the ability to build it all through systems or processes it builds step by step by step inside the first run'. Drawn: lane 13 and the inside of every step (KEY)."),
 ("'the first time it works and is correct' is not 'ok': it is the next step completing, and later the user's correct/incorrect and the sixth's observation", "Drawn: lane 5 (worked), lane 10 (correct?), lane 11."),
 ("the say key = the metadata that travels with what leaves and returns through mother", "His guesses for its columns: what is this data in perspective to this run, where does it belong, what does it solve, who said it, when, why, what modifiers. Drawn: lane 0 (the key shape), lanes 4, 6."),
]):
    node(f"c{i+1}", f"{i+1}. {t}", "closed", None, tt, "      ")
close("    ")
open_col("still", "still his call", "    ")
for i, (t, tt) in enumerate([
 ("the compile, explained: when the sources disagree, what goes in the definition node?", "The example on this line: for who, WordNet sent 'a United Nations agency' (the WHO), Webster 'an interrogative pronoun, later a relative pronoun', Merriam-Webster 'what or which person or persons' and 'the person or persons that: whoever'. The earlier build kept only the words two sources shared and dropped the rest, and on 10-23 P4 B1 he said 'the diffs are kind of dropped or scattered and the similars are kept. But I don't know that we're getting a good, valid definition that way... if the definitions are wrong, then the description of the meaning is wrong'. The drawing keeps every source's line as its own row, kept apart by source, and lets the compile lay relationship rows from them; what the compile DROPS, if anything, and what counts as 'similar' (the same gates? the same relationships?) is the open part."),
 ("the key's columns", "His guesses listed in lane 0; which are needed is found as the brain grows."),
 ("how deep a symbol born from a definition text is sourced", "10-23 P4: 'in order to have the definitions, you have to have 500 or 1,000 words that you don't have meanings for'. The drawing stops one level down."),
 ("the formula neuron's rows for other variables and modifiers: another row, or another neuron", "His words 10-28: 'you have to take in account variables and modifiers sometimes in this aspect such to get the full use of a formula in any one context'."),
 ("the count of hand-laid tools: 20, 80 or 200; which turn out to be buildable later", "His words 10-28. The core drawn here is 63 and is a reading."),
 ("what the inspection run reads first: the script, the context, or the memories", "His words 10-28 name all three."),
]):
    node(f"o{i+1}", f"{i+1}. {t}", "open", None, tt, "      ")
close("    ")
close("  ")
close("")   # end column A

# assemble: A then B then C
L = _saved
out = "\n".join(_saved) + "\n" + "\n".join(B) + "\n" + "\n".join(C) + "\n"
open(OUT, "w", encoding="utf-8").write(out)
print("gates:", len(enc), "last shard:", shard_n[0], "return runs:", ret_total, "space hits:", hits_per_gate.get(3))
