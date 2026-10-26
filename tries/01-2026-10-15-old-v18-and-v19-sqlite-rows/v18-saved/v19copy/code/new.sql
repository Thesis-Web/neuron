-- new: a neuron is born. Given a place (a), it is born at that place; given none, it is born unplaced.
INSERT OR IGNORE INTO neuron (gate, born)
  SELECT CAST(a AS TEXT), (SELECT max(id) FROM TIMELINE) FROM step WHERE id = :S:;
-- a typed number goes on to the neuron at its place
INSERT INTO step (neuron, ear)
  SELECT n.id, s.ear FROM step s JOIN neuron n ON n.gate = CAST(s.a AS TEXT)
  WHERE s.id = :S: AND s.ear IS NOT NULL;
