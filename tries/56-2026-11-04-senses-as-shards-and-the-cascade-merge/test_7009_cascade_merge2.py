import os, sys
sys.path.insert(0, os.path.expanduser('~/nk-c27'))
from client import ask
print('VALUES in the egg:', ask("q SELECT gate FROM main.label WHERE symbol = 'VALUES'")['rows'])
r = ask('type main the word values stands here'); T = ask("q SELECT gate FROM main.label WHERE symbol = 'values'")['rows'][0][0]; H = ask("q SELECT gate FROM main.label WHERE symbol = 'VALUES'")['rows'][0][0]
print('values born as gate %d; VALUES is gate %d' % (T, H))
r = ask('type main BUILD INSERT INTO node ( gate , id , source , run ) VALUES ( %d , 1 , 7 , 1 ) ; BUILD' % T)
print('a span with VALUES while values has no definition: refused %s; label VALUES -> %s (no merge yet); nodes of values now %s' % (r.get('refused'), ask("q SELECT gate FROM main.label WHERE symbol = 'VALUES'")['rows'], ask('q SELECT nodes FROM main.neuron WHERE gate = %d' % T)['rows']))
r = ask('type main BUILD INSERT INTO node ( gate , id , source , run ) VALUES ( %d , 2 , 7 , 1 ) ; BUILD' % T)
print('a span with VALUES once values holds a definition: refused %s; label VALUES -> %s; neuron %d born %s; neuron %d born %s' % (r.get('refused'), ask("q SELECT gate FROM main.label WHERE symbol = 'VALUES'")['rows'], H, ask('q SELECT born FROM main.neuron WHERE gate = %d' % H)['rows'], T, ask('q SELECT born FROM main.neuron WHERE gate = %d' % T)['rows']))
r = ask('type main BUILD INSERT INTO node ( gate , id , source , run ) VALUES ( %d , 3 , 7 , 1 ) ; BUILD' % T)
print('the next span encodes: %s' % ' '.join(s[0] for s in ask("q SELECT l.symbol FROM main.seq s JOIN main.label l ON l.gate = s.gate WHERE s.run = %d AND l.symbol <> ' ' ORDER BY s.pos" % r['run'])['rows']))
r = ask('type main the WHO stands here and who too'); print('WHO in a plain line: label WHO -> %s (untouched)' % ask("q SELECT gate, symbol FROM main.label WHERE symbol = 'WHO'")['rows'])
