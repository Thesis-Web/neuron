
css = open('style-173.css').read(); body = open('body.html').read(); js = open('script-1.js').read() + open('script-2.js').read() + open('script-3.js').read()
extra = """<style>
  /* v6: the rails are tabs; lists of gates, runs and lines; the key-value block under brains (from the tries/15 page) */
  .tabs { flex-wrap: wrap; }
  .list { font-family: var(--mono); font-size: .72rem; max-height: 260px; overflow-y: auto; overscroll-behavior: contain; border: 1px solid var(--line); border-radius: 5px; background: var(--bg); }
  .list div { padding: 3px 7px; border-bottom: 1px solid var(--line); display: grid; grid-template-columns: 3.6em minmax(0, 1fr) auto; gap: 6px; cursor: pointer; overflow-wrap: anywhere; }
  .list div:last-child { border-bottom: 0; } .list div.last { background: var(--panel2); } .list .m { color: var(--muted); }
  #tree { max-height: 300px; } #nlist { max-height: 420px; } #tsheet, #fsheet { max-height: 300px; }
  .kv { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 3px 10px; font-size: .8rem; } .kv .k { font-family: var(--mono); font-size: .72rem; color: var(--muted); }
  .cells td.b { color: var(--accent); } .cells td.e, .cells .e { color: var(--warn); }
  .cells td:first-child { white-space: nowrap; width: 1%; } .cells td { overflow-wrap: anywhere; word-break: normal; }
  .cells table.cells td:first-child { width: auto; white-space: normal; }
  .log div { grid-template-columns: 3.2em 7em 1fr; }
  aside select { max-width: 100%; min-width: 0; }
  #dnarows td { white-space: nowrap; }
  .atlas tr.det td .dt { max-width: calc(100vw - 440px); white-space: pre-wrap; overflow-wrap: anywhere; }
  .mlist { max-height: 300px; } .mlist div { grid-template-columns: 2.6em minmax(0, 1fr) auto; }
  #out .sel { gap: 6px; } #out table.cells { font-size: .72rem; } #out [data-gate] { text-decoration: underline dotted; }
  #prompt { max-width: 11em; }
</style>
"""
head = """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Point Of Connection v6</title>
<meta name="description" content="The 17.3 page on the v6 brains: every gate of the encoder a point, every row the brain holds a line with its kind's pull, the brain's history replayed hit by hit from its receipt table, read live through serve6.py.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<!-- The style block below is 17.3's, byte for byte (its lines 5 to 122, as the tries/15 page carries them); what this page adds is in the second block. -->
"""
page = head + css + extra + body + '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n<script>\n' + js + '</script>\n</html>\n'
open('../NEURON-POINT-OF-CONNECTION-v6-2026-10-29.html', 'w').write(page)
print('page', len(page), 'bytes')
