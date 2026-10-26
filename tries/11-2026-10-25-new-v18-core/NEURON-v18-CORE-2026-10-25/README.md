# Neuron v18 core (2026-10-25), from the owner's words only
Run (from this folder):  python3 neuron_prompt18.py brain18.db
- brain18.db is the tested brain: the hand-laid core, the four teaching lines typed (born, source, define, define : -> define),
  then define : dog / cat / store learned. "define : dog" answers from dog's definition node in under a second.
- To start from the bare core instead: python3 neuron_prompt18.py fresh.db   (a new file lays the core), then type :sheet
  (teaches the four lines, about 100 s). :save saves, :q saves and quits. The brain comes back as it was.
- A new word is slow the first time: every word that comes back in its source lines is born by the born run.

Files
- EXPECT-v18.md: the test, written before any v18 code, with the owner's words it is built from. RESULTS-v18.md: how it held.
- gen18.py -> physics18.json: what is hand-laid (the encoder, the neurons that make the table with their gates, the hop neuron,
  the trigger column, BUILD front and end). host18.py: the bottom (mother and the source brains). sat172.json: the source stand-ins.
- make_sheet18.py -> sheet18.json: the four teaching lines. test18.json: the test run's numbers.
