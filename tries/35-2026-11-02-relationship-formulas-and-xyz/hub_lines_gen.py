#!/usr/bin/env python3
# g35/hub_lines_gen.py (2026-11-02): writes the hub's typed lines for the places (HUB-XYZ-v7.txt: the tables and the xyz_go trigger),
# the back population of the places (HUB-SETTLE-v7.txt: a placing line and a stepping line, 3000 points each) and the catalog
# relationships for the already-defined points (HUB-RELS-BACKPOP-v7.txt: 500 points a line). One law, written once here, the same as the
# kernel's nkxyz.c: a point never placed starts at the mean of its placed relations plus a unit vector of its own (4 away), or a unit from
# the origin; a step is 0.04 of the sum of its relationships' pulls through their kinds' formulas (both ways), capped at 6.
T = "/mnt/d/Neuron/tries/35-2026-11-02-relationship-formulas-and-xyz"
LB, RB, LC, RC, COLON, SEMI, COMMA, SPACE, WN, WIKT = 140, 144, 169, 173, 68, 45, 38, 3, 7, 3369
ORIGIN = "( SELECT gate FROM label WHERE symbol = 'origin' )"
def unit(g):
    """the unit vector of a gate, deterministic (the kernel's unit_of): ua an angle, uz a height; the vector is (r cos ua, r sin ua, uz)"""
    h = "( ( %s * 2654435761 ) %% 4294967296 )" % g
    h2 = "( ( ( %s | 2654435769 ) - ( %s & 2654435769 ) ) * 2246822519 %% 4294967296 )" % (h, h)
    ua = "( %s / 4294967296.0 * 6.283185307179586 )" % h; uz = "( %s / 4294967296.0 * 2 - 1 )" % h2
    r = "sqrt ( 1 - %s * %s )" % (uz, uz)
    return ("( %s * cos ( %s ) )" % (r, ua), "( %s * sin ( %s ) )" % (r, ua), uz)
def both(g): return "( SELECT other AS h FROM rel WHERE gate = %s UNION ALL SELECT gate FROM rel WHERE other = %s )" % (g, g)
def place_cols(g):
    """x, y, z of a point placed now: the mean of its placed relations plus 4 times its unit vector, or the unit vector alone"""
    ux, uy, uz = unit(g); near = "( CASE WHEN EXISTS ( SELECT 1 FROM %s q JOIN xyz o ON o.gate = q.h ) THEN 4 ELSE 1 END )" % both(g)
    return ["coalesce ( ( SELECT avg ( o.%s ) FROM %s q JOIN xyz o ON o.gate = q.h ) , 0 ) + %s * %s" % (c, both(g), near, u) for c, u in (("x", ux), ("y", uy), ("z", uz))]
def forces(g, gsel):
    """the pull on the point g of every relationship row, both ways, through the kind's formula against the other point's place; one row each"""
    L = "max ( sqrt ( ( o.x - m.x ) * ( o.x - m.x ) + ( o.y - m.y ) * ( o.y - m.y ) + ( o.z - m.z ) * ( o.z - m.z ) ) , 0.01 )"
    inner = ("SELECT %s AS g , f.pull AS pull , f.rest AS rest , f.dx * q.sg AS dx , f.dy * q.sg AS dy , f.dz * q.sg AS dz , f.mode AS mode , o.x AS ox , o.y AS oy , o.z AS oz , m.x AS mx , m.y AS my , m.z AS mz , o.x - m.x AS vx , o.y - m.y AS vy , o.z - m.z AS vz , f.pull * ( %s - f.rest ) / %s * 0.04 AS sp "
             "FROM ( SELECT kind , other AS h , 1 AS sg FROM rel WHERE gate = %s UNION ALL SELECT kind , gate , -1 FROM rel WHERE other = %s ) q JOIN pull p ON p.kind = q.kind JOIN formula f ON f.id = p.formula JOIN xyz o ON o.gate = q.h JOIN xyz m ON m.gate = %s WHERE o.gate <> %s" % (gsel, L, L, g, g, g, g))
    comp = lambda c: "CASE mode WHEN 1 THEN - pull * 0.04 * ( ( m%s + rest * d%s ) - o%s ) WHEN 2 THEN pull * 0.25 * ( - o%s - m%s ) + v%s * sp ELSE v%s * sp END AS f%s" % (c, c, c, c, c, c, c, c)
    return "SELECT g , %s , %s , %s FROM ( %s )" % (comp("x"), comp("y"), comp("z"), inner)
CAP = "min ( 1 , 6 / max ( sqrt ( fx * fx + fy * fy + fz * fz ) , 0.000000001 ) )"
def write(name, head, lines):
    open(T + "/" + name, "w", encoding="utf-8").write(head + "\n" + "\n".join(lines) + "\n"); print("wrote", name, [len(l) for l in lines])

# --- HUB-XYZ-v7.txt: the tables and the trigger
px, py, pz = place_cols("NEW.gate")
tables = ("BUILD CREATE TABLE IF NOT EXISTS xyz ( gate INTEGER PRIMARY KEY , x REAL , y REAL , z REAL , shard INTEGER , before INTEGER , next INTEGER , at INTEGER , run INTEGER , moved INTEGER ) ; "
          "CREATE TABLE IF NOT EXISTS xyz_step ( k INTEGER PRIMARY KEY CHECK ( k = 1 ) , fx REAL , fy REAL , fz REAL ) ; "
          "INSERT OR IGNORE INTO xyz ( gate , x , y , z , shard , before , next , at , run , moved ) SELECT gate , 0 , 0 , 0 , 0 , NULL , NULL , ( SELECT n FROM clock ) , 0 , 1 FROM label WHERE symbol = 'origin' ; "
          "CREATE INDEX IF NOT EXISTS rel_other ON rel ( other ) ; BUILD")
trigger = ("BUILD CREATE TRIGGER IF NOT EXISTS xyz_go AFTER INSERT ON hit WHEN NEW.pos > 0 AND NEW.via = 0 AND NEW.gate <> 3 AND NEW.gate <> %s BEGIN "
           "INSERT OR IGNORE INTO xyz ( gate , x , y , z , shard , before , next , at , run , moved ) SELECT NEW.gate , %s , %s , %s , NEW.shard , NEW.kb , NEW.kn , ( SELECT n FROM clock ) , NEW.run , 1 WHERE NOT EXISTS ( SELECT 1 FROM xyz WHERE gate = NEW.gate ) ; "
           "INSERT OR REPLACE INTO xyz_step ( k , fx , fy , fz ) SELECT 1 , total ( fx ) , total ( fy ) , total ( fz ) FROM ( %s ) WHERE EXISTS ( SELECT 1 FROM xyz WHERE gate = NEW.gate AND NOT ( shard = NEW.shard AND before IS NEW.kb AND next IS NEW.kn ) ) ; "
           "UPDATE xyz SET x = x + ( SELECT fx * %s FROM xyz_step ) , y = y + ( SELECT fy * %s FROM xyz_step ) , z = z + ( SELECT fz * %s FROM xyz_step ) , shard = NEW.shard , before = NEW.kb , next = NEW.kn , at = ( SELECT n FROM clock ) , run = NEW.run , moved = moved + 1 WHERE gate = NEW.gate AND NOT ( shard = NEW.shard AND before IS NEW.kb AND next IS NEW.kn ) ; END ; BUILD"
           % (ORIGIN, px, py, pz, forces("NEW.gate", "NEW.gate"), CAP, CAP, CAP))
write("HUB-XYZ-v7.txt", "# HUB-XYZ-v7.txt (2026-11-02, written by hub_lines_gen.py): the hub holds a point's place and moves it by its relationships when a shard with another meaning is used on it (the owner, 11-01: 'the points float over a stationary graph based on the push or the pull of relationships, the gates x,y,z number is determinate on state and time'; 'when a shard is used on a meaning point that point will likely move on the graph, unless the shard being used has the same meaning as the last one used'). The same law as the kernel's nkxyz.c. 1. the tables and the key on rel.other; 2. the trigger on the hit.", [tables, trigger])

# --- HUB-SETTLE-v7.txt: the back population of the places, 3000 points a line
bx, by, bz = place_cols("b.g")
place = ("BUILD INSERT INTO xyzbatch ( g , done ) SELECT gate , 0 FROM ( SELECT DISTINCT gate FROM rel WHERE gate > ( SELECT coalesce ( max ( g ) , 0 ) FROM xyzbatch ) AND gate <> %s ORDER BY gate LIMIT 3000 ) ; "
         "INSERT OR IGNORE INTO xyz ( gate , x , y , z , shard , before , next , at , run , moved ) SELECT b.g , %s , %s , %s , 0 , NULL , NULL , ( SELECT n FROM clock ) , 0 , 1 FROM xyzbatch b WHERE b.done = 0 ; "
         "UPDATE xyzbatch SET done = 1 WHERE done = 0 ; BUILD" % (ORIGIN, bx, by, bz))
def forces_batch():
    """the pull on every point of the batch (done = 0), its relationship rows both ways as two plain joins (a FROM subquery may not name the
    batch: SQLite has no lateral join; the first step line did, and moved nothing), one row a relationship, then summed by point"""
    L = "max ( sqrt ( ( o.x - m.x ) * ( o.x - m.x ) + ( o.y - m.y ) * ( o.y - m.y ) + ( o.z - m.z ) * ( o.z - m.z ) ) , 0.01 )"
    def half(join, other, sg):
        return ("SELECT b.g AS g , f.pull AS pull , f.rest AS rest , f.dx * %d AS dx , f.dy * %d AS dy , f.dz * %d AS dz , f.mode AS mode , o.x AS ox , o.y AS oy , o.z AS oz , m.x AS mx , m.y AS my , m.z AS mz , o.x - m.x AS vx , o.y - m.y AS vy , o.z - m.z AS vz , f.pull * ( %s - f.rest ) / %s * 0.04 AS sp "
                "FROM xyzbatch b JOIN rel r ON %s JOIN pull p ON p.kind = r.kind JOIN formula f ON f.id = p.formula JOIN xyz o ON o.gate = %s JOIN xyz m ON m.gate = b.g WHERE b.done = 0 AND o.gate <> b.g" % (sg, sg, sg, L, L, join, other))
    comp = lambda c: "CASE mode WHEN 1 THEN - pull * 0.04 * ( ( m%s + rest * d%s ) - o%s ) WHEN 2 THEN pull * 0.25 * ( - o%s - m%s ) + v%s * sp ELSE v%s * sp END AS f%s" % (c, c, c, c, c, c, c, c)
    one = lambda h: "SELECT g , %s , %s , %s FROM ( %s )" % (comp("x"), comp("y"), comp("z"), h)
    return one(half("r.gate = b.g", "r.other", 1)) + " UNION ALL " + one(half("r.other = b.g", "r.gate", -1))
step = ("BUILD INSERT INTO xyzbatch ( g , done ) SELECT gate , 0 FROM ( SELECT gate FROM xyz WHERE gate > ( SELECT coalesce ( max ( g ) , 0 ) FROM xyzbatch ) AND gate <> %s ORDER BY gate LIMIT 3000 ) ; "
        "DELETE FROM xyzforce ; INSERT INTO xyzforce ( g , fx , fy , fz , sc ) SELECT g , total ( fx ) , total ( fy ) , total ( fz ) , 0 FROM ( %s ) GROUP BY g ; "
        "UPDATE xyzforce SET sc = %s ; "
        "UPDATE xyz SET x = x + coalesce ( ( SELECT fx * sc FROM xyzforce w WHERE w.g = xyz.gate ) , 0 ) , y = y + coalesce ( ( SELECT fy * sc FROM xyzforce w WHERE w.g = xyz.gate ) , 0 ) , z = z + coalesce ( ( SELECT fz * sc FROM xyzforce w WHERE w.g = xyz.gate ) , 0 ) , at = ( SELECT n FROM clock ) , moved = moved + 1 WHERE gate IN ( SELECT g FROM xyzbatch WHERE done = 0 ) ; "
        "UPDATE xyzbatch SET done = 1 WHERE done = 0 ; BUILD" % (ORIGIN, forces_batch(), CAP))
write("HUB-SETTLE-v7.txt", "# HUB-SETTLE-v7.txt (2026-11-02, written by hub_lines_gen.py): the places back-populated on the hub, the long way once: line 1 places 3000 points that hold relationship rows (typed until its batch is empty); line 2 steps 3000 placed points once (typed until empty; a pass). Tables xyzbatch (g, done) and xyzforce (g, fx, fy, fz, sc) are the lines' own.", [place, step])

# --- HUB-RELS-BACKPOP-v7.txt: the define's marker span over the returns of 500 already-defined points a line
span = ("WITH br AS MATERIALIZED ( SELECT r.id AS run , r.about AS about , b.pos AS p0 , ( SELECT min ( pos ) FROM seq WHERE run = r.id AND pos > b.pos AND gate IN ( %d , %d ) ) AS pc , ( SELECT min ( pos ) FROM seq WHERE run = r.id AND pos > b.pos AND gate = %d ) AS pe FROM run r JOIN seq b ON b.run = r.id AND b.gate = %d WHERE r.about IN ( SELECT g FROM relsbatch ) AND r.kind = 3 AND r.arrival IN ( %d , %d ) ) , "
        "kb AS MATERIALIZED ( SELECT br.run , br.about , br.pc , br.pe , k.gate AS kind FROM br JOIN relmap m ON m.marker = ( SELECT group_concat ( l3.symbol , ' ' ) FROM ( SELECT l2.symbol FROM seq s2 JOIN label l2 ON l2.gate = s2.gate WHERE s2.run = br.run AND s2.pos > br.p0 AND s2.pos < br.pc AND s2.gate <> %d ORDER BY s2.pos ) l3 ) JOIN label k ON k.symbol = m.kind WHERE br.pe IS NOT NULL AND ( SELECT gate FROM seq WHERE run = br.run AND pos = br.pc ) = %d ) "
        "INSERT OR IGNORE INTO rel ( gate , kind , other , run ) SELECT kb.about , kb.kind , t.gate , kb.run FROM kb JOIN seq t ON t.run = kb.run AND t.pos > kb.pc AND t.pos < kb.pe JOIN label lt ON lt.gate = t.gate WHERE lt.symbol GLOB '[A-Za-z]*' AND t.gate <> kb.about "
        "AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos - 1 ) , %d ) , ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos - 2 ) ) IN ( %d , %d , %d , %d ) "
        "AND coalesce ( nullif ( ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos + 1 ) , %d ) , ( SELECT gate FROM seq WHERE run = kb.run AND pos = t.pos + 2 ) ) IN ( %d , %d , %d , %d )"
        % (COLON, RB, RB, LB, WN, WIKT, SPACE, COLON, SPACE, LC, COLON, SEMI, COMMA, SPACE, RC, SEMI, RB, COMMA))
rels = ("BUILD DELETE FROM relsbatch ; INSERT INTO relsbatch ( g ) SELECT about FROM ( SELECT DISTINCT about FROM run WHERE kind = 3 AND arrival IN ( %d , %d ) AND about > ( SELECT coalesce ( max ( g ) , 0 ) FROM relsdone ) ORDER BY about LIMIT 500 ) ; %s ; INSERT OR IGNORE INTO relsdone ( g ) SELECT g FROM relsbatch ; SELECT count ( * ) FROM relsbatch ; BUILD" % (WN, WIKT, span))
write("HUB-RELS-BACKPOP-v7.txt", "# HUB-RELS-BACKPOP-v7.txt (2026-11-02, written by hub_lines_gen.py): the catalog relationships for the hub's already-defined points, the define's own marker span (HUB-RELS-v7.txt) over the WordNet and Wiktionary returns of 500 points a line, keyed by about; relsdone keeps the place; typed until the batch is empty (hub_g35.py rels). The owner: 'as part of the build step relationships are populated'; 'back population ... will require the building of that process within the neurons'.", [rels])
