import os, sys
sys.path.insert(0, os.path.expanduser('~/nk-c27'))
from client import ask
r = ask('type main from abligurriō (“to lick away; to spend or waste indulgently, squander”) + -tiō and ab‧lig‧u‧rit‧ion and *h₂epó and naïve café – dash … end')
print('typed run %s born %s' % (r.get('run'), r.get('born')))
syms = [s[0] for s in ask('q SELECT l.symbol FROM main.seq s JOIN main.label l ON l.gate = s.gate WHERE s.run = %d ORDER BY s.pos' % r['run'])['rows']]
print('symbols:', ' | '.join(s for s in syms if s != ' '))
