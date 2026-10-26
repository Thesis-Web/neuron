---
name: project_neuron_router_and_as_facts_20261022
description: Measured 2026-10-22 for the owner's mailbox/router design and the AS question - SQLite refuses cross-database writes from any trigger, satellite triggers fire on insert, round-trip costs, and what AS does with and without it
metadata:
  type: project
---

Measured in scratchpad (Python sqlite3 + sql.js 3.39.3), predictions written first:
- A trigger cannot write into another (attached) database: "qualified table names are not allowed on INSERT, UPDATE, and DELETE statements within triggers". A TEMP trigger is refused too (my prediction that it could was wrong). So mother is the only way out of a brain - matches the owner: "the mother only does what the brain cannot do, which is traverse".
- A trigger stored in the satellite fires the moment the main connection writes its inbox: populated-driven, no timer.
- Round trip per ask: 0.011 ms attached in-process; 0.22 ms to a resident satellite process over a kept-open socket; 69 ms when a process is started per ask (~319x). Pickup MUST empty the outbox (a never-emptied, unindexed outbox stalled the run). Network to hp/hp2 not measured (owner's machines).
- AS: removing it breaks CAST(x AS type), CREATE TABLE ... AS SELECT, WITH q AS (...) (syntax error); in a column alias SQLite reads the name by position, so AS changes nothing for the machine. The SQLite docs DO describe AS (three sentences); v13's "AS appears only in the syntax" was my extraction failing.
- Real source replies for English "as" include other words: Webster 1913 sends "So" first plus three "As" entries; MW sends As:1/As:2/AS/as-; MW thesaurus sends "as far as" etc. Basis for the owner's check "is this the data I asked for?".
**Why:** the owner asked whether mailboxes+router would be too slow and whether AS has a meaning; these are the measured answers. **How to apply:** recommend resident satellites with one kept-open connection each, never ssh/process per ask; cite the numbers, not adjectives. Related: [[reference_neuron_pages_20261021]].
