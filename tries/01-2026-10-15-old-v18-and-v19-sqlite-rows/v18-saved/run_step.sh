#!/bin/bash
# the exact sequence for the real brain; $1 = the brain's folder. physics_before.sql = the physics as it stands now.
set -e
cd "$1"
P=physics_new.sql; mv physics.sql $P; cp physics_before.sql physics.sql      # steps 1-3 run on the physics as it stands
sqlite3 -init skull.sql brain.db \
  "INSERT INTO code (word) VALUES ('var'), ('now'), ('new'), ('code'), ('word'), ('formula'), ('head'), ('row');" \
  "INSERT INTO ear (line) VALUES ('CREATE TABLE formula ( id INTEGER PRIMARY KEY , neuron INTEGER NOT NULL , KEY INTEGER , head TEXT NOT NULL , row TEXT ) ; /build');" \
  "INSERT INTO ear (line) VALUES ('SELECT max ( id ) + 1 FROM TIMELINE ; /build');" \
  ".read formulas.sql" 2>&1 | { grep -v Loading || true; }
mv $P physics.sql; rm physics_before.sql                                      # then the formula physics
sqlite3 -init skull.sql brain.db \
  "INSERT INTO ear (line) VALUES ('new word read write end find count forget same if do again hear say hold get put /build');" 2>&1 | { grep -v Loading || true; }
