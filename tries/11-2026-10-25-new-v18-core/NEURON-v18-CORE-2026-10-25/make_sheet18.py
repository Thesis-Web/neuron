# writes sheet18.json: the four teaching lines typed at the prompt. The born run's gate trigger is the same template the
# hand-laid neurons use (gen18.GATE_TEMPLATE), with its holes as "var" cells.
import json, sys
sys.path.insert(0, '.'); import gen18
sub = "( SELECT word FROM born WHERE id = var subject )"
subd = "( SELECT word || '.definition' FROM born WHERE id = var subject )"
cells = [('gate', 'gate', sub), ('dna', "'g' || gate", sub), ('entry', "'land_' || gate", sub), ('gatet', "'gate_' || gate", sub), ('defgate', 'gate', subd), ('deft', "'g' || gate", subd)]
born = ("born = BUILD INSERT INTO label ( word ) SELECT word FROM born WHERE id = var subject ; INSERT INTO label ( word ) SELECT word || '.definition' FROM born WHERE id = var subject ; "
  + " ; ".join(f"INSERT INTO sheet ( run , name , value ) SELECT var run , '{n}' , {v} FROM label WHERE word = {w}" for n, v, w in cells) + " BUILD "
  "BUILD CREATE TABLE var dna ( shard INTEGER PRIMARY KEY , arrival INTEGER , remainder INTEGER , trigger INTEGER ) ; "
  "CREATE VIEW var entry AS SELECT arrival , remainder , NULL AS run , NULL AS rest FROM var dna ; "
  + gen18.gate_trigger_holes() + " ; "
  "CREATE TABLE var deft ( id INTEGER PRIMARY KEY , source INTEGER , run INTEGER , score REAL ) ; "
  "INSERT INTO var dna ( shard , trigger ) SELECT n + 1 , var defgate FROM shards ; UPDATE shards SET n = n + 1 BUILD")
old = json.load(open('sheet18.json'))
sheet = [["teach born", born]] + [r for r in old if r[0] != 'teach born']
json.dump(sheet, open('sheet18.json', 'w'), indent=1)
print('born line', len(born), 'characters;', len(gen18.tokens(born)), 'tokens')
