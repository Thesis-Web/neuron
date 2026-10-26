# The brain at a prompt, on native SQLite (2026-10-25)
The same brain as Point Of Connection 17.3: told block 17.2 (physics172.json), the sources (sat172.json), the teaching sheet (sheet173.json).
host15.py is the bottom and mother (the page's host, in Python): it writes a typed line into input, reads output, and routes. It decides nothing.

Run it (from this folder):
    python3 neuron_prompt.py . physics172.json sat172.json brain.db sheet173.json
At the prompt:
- type a line and press enter; the brain's answer is printed with the seconds it took;
- :sheet types the whole teaching sheet (9 + 5 formulas, 17 binds, the example commands); it takes a long time: learning is slow;
- :save writes the brain to brain.db; :q saves and quits. Next time the brain loads from brain.db, alive as it was.
Nothing here writes outside this folder. It does not touch ~/neuron/v1.
