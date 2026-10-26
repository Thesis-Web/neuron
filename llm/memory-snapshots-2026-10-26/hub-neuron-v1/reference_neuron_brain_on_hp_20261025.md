---
name: reference_neuron_brain_on_hp_20261025
description: The 17.2/17.3 brain installed on the owner's hp (ssh hp = james@10.31.1.106, Debian 13, Python 3.13.5, SQLite 3.46.1) in ~/neuron-prompt-2026-10-25 with a bare-core brain.db; how to run its prompt from the hub; the page runs in the hub's browser with its own in-browser brain
metadata:
  type: reference
---
Installed 2026-10-25 at the owner's request ("install the sqlite db on the ssh hp"), in a NEW folder; the owner's ~/neuron-build on hp was not touched.
- hp: `ssh hp` (james@10.31.1.106; hp2 = 10.31.1.112). Debian 13, Python 3.13.5, SQLite 3.46.1, sqlite3 CLI, R*Tree available natively.
- Folder ~/neuron-prompt-2026-10-25: neuron_prompt.py, host15.py, physics172.json (told block 17.2), sat172.json, sheet173.json, README.md, brain.db (bare core: 96 gates, 165 triggers, formula 'source', 0 typed lines, place table).
- Run from the hub (a real terminal, interactive): `ssh -t hp 'cd ~/neuron-prompt-2026-10-25 && python3 neuron_prompt.py . physics172.json sat172.json brain.db sheet173.json'`; ':sheet' types the teaching sheet, ':save', ':q' saves.
- Tested on hp in a throwaway db: learn : store said 8 in 14.8 s (43 s in node on the hub); a repeated line answered from memory.
- The HTML page runs in the hub's browser (sql.js, its own brain); it cannot see hp's brain.db unless a brain file is loaded into it (not built yet; offered).
Related: [[project_neuron_poc173_find_apply_20261025]].

v18 (10-25, later): ~/neuron-v18-2026-10-25 on hp: `ssh -t hp 'cd ~/neuron-v18-2026-10-25 && python3 neuron_prompt18.py brain18.db'` (brain18.db = taught + dog/cat/store). The 17.2 folder above still holds the old rules.
