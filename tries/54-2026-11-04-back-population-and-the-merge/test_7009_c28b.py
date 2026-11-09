import json, os, sys
sys.path.insert(0, os.path.expanduser('~/nk-c27'))
from client import ask
r = ask('type main BUILD SELECT 1 + 1 ; BUILD'); print('BUILD SELECT 1 + 1 -> run %s refused %s' % (r.get('run'), r.get('refused')))
print('refused rows:', ask('q SELECT id, substr(text, 1, 80), error FROM main.refused')['rows'])
r = ask('type main the word select stands here'); print('the word select stands here -> run %s born %s' % (r.get('run'), r.get('born')))
H = ask("q SELECT gate FROM main.label WHERE symbol = 'SELECT'")['rows'][0][0]; T = ask("q SELECT gate FROM main.label WHERE symbol = 'select'")['rows'][0][0]
print('before: SELECT gate %d, select gate %d' % (H, T))
print('merge through mother:', ask('q SELECT merge(%d, %d)' % (H, T))['rows'])
print('after: label SELECT ->', ask("q SELECT gate, symbol FROM main.label WHERE symbol = 'SELECT'")['rows'], '; label select ->', ask("q SELECT gate, symbol FROM main.label WHERE symbol = 'select'")['rows'])
print('neuron %d (born, nodes, shards):' % H, ask('q SELECT born, nodes, shards FROM main.neuron WHERE gate = %d' % H)['rows'], '; neuron %d:' % T, ask('q SELECT born, nodes, shards FROM main.neuron WHERE gate = %d' % T)['rows'])
r = ask('type main a line with SELECT in it'); print('a line with SELECT in it -> run %s; its symbols by gate:' % r.get('run'), ask('q SELECT s.pos, s.gate, l.symbol FROM main.seq s JOIN main.label l ON l.gate = s.gate WHERE s.run = %d AND s.gate IN (%d, %d)' % (r['run'], H, T))['rows'])
print('merge error path (same gate):', ask('q SELECT merge(%d, %d)' % (T, T))['rows'])
print('relabel:', ask('relabel'))
