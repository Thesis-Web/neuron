import sys,re; sys.path.insert(0,'/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad')
from hublib import *
G=153; W=231
# 1. why: the guesser out. The hub's why was the guesser and nothing else.
j,dt=typ(f'BUILD UPDATE "{W}" SET call = NULL WHERE before = 5 AND trigger = 68 ; BUILD'); print('why unbound',round(dt,1),'s',str(j.get('error'))[:120], q(f'SELECT before,trigger,call FROM "{W}" WHERE before=5 AND trigger=68'))
# 2. define: known and unknown in one pass
c=q(f'SELECT call FROM "{G}" WHERE before=5 AND trigger=68')[0][0]; t=text_of(c)
i=t.index("BUILD INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , ( SELECT gate FROM label WHERE symbol = 'known' )"); e=t.rindex(" ; BUILD")
src="( r.arrival BETWEEN 7 AND 14 OR r.arrival = ( SELECT gate FROM label WHERE symbol = 'wikt' ) )"; srck=src.replace('r.arrival','k.arrival')
new=t[:i]+f"BUILD WITH x ( g , h ) AS MATERIALIZED ( SELECT DISTINCT s.gate , EXISTS ( SELECT 1 FROM run k WHERE k.kind = 3 AND k.about = s.gate AND {srck} ) FROM run r JOIN seq s ON s.run = r.id JOIN label l ON l.gate = s.gate WHERE r.kind = 3 AND {src} AND r.parent = above AND l.symbol GLOB '[A-Za-z]*' ORDER BY s.gate ) INSERT OR REPLACE INTO run_sheet ( run , cell , state , value ) SELECT above , k.gate , 1 , coalesce ( ( SELECT group_concat ( x.g , ' ' ) FROM x WHERE x.h = ( k.symbol = 'known' ) ) , '' ) FROM label k WHERE k.symbol IN ( 'known' , 'unknown' )"+t[e:]
j,dt=typ(new); run=(j.get('result') or {}).get('run'); print('define laid',run,round(dt,1),'s',str(j.get('error'))[:200]); assert run and text_of(run)==new
for b in (1,5): typ(f'BUILD UPDATE "{G}" SET call = {run} WHERE before = {b} AND trigger = 68 ; BUILD')
print('define rows',q(f'SELECT before,trigger,call FROM "{G}" WHERE trigger=68 AND before IN (1,5)'))
# 3. the sixth: no tree walks
s=82; cs=q(f'SELECT call FROM sixth."{s}" WHERE before=6 AND trigger=68')[0][0]; x=text_of(cs,'sixth')
a="s.run IN ( WITH RECURSIVE t ( id ) AS ( SELECT what UNION ALL SELECT k.id FROM main.run k JOIN t ON k.parent = t.id ) SELECT id FROM t )"
n=x.replace(a,"s.run = what")
pre="s.run IN ( WITH RECURSIVE t ( id ) AS ( SELECT ( SELECT CASE WHEN"; post=" END ) UNION ALL SELECT k.id FROM main.run k JOIN t ON k.parent = t.id ) SELECT id FROM t )"
n=n.replace(pre,"s.run = ( SELECT CASE WHEN").replace(post," END )")
assert 'RECURSIVE' not in n, n[n.index('RECURSIVE')-120:n.index('RECURSIVE')+200]
j,dt=typ('6> '+n,'sixth'); r6=(j.get('result') or {}).get('run'); print('sixth line laid',r6,round(dt,1),'s',str(j.get('error'))[:200])
if not r6: j,dt=typ(n,'sixth'); r6=(j.get('result') or {}).get('run'); print(' again without the prompt mark',r6)
assert r6 and text_of(r6,'sixth').replace('6> ','',1)==n
j,dt=typ(f'6> BUILD UPDATE sixth."{s}" SET call = {r6} WHERE before = 6 AND trigger = 68 ; BUILD','sixth'); print(str(j.get('result'))[:140])
print('seen row',q(f'SELECT before,trigger,call FROM sixth."{s}" WHERE before=6 AND trigger=68'),'was',cs)
# 4. the owner's line
for i in range(2):
    j,dt=typ('define : know'); res=j.get('result') or {}
    print('LIVE define : know',round(dt,2),'s runs',res.get('runs'),'hits',res.get('hits'),'refused',res.get('refused'),[str(o)[:80] for o in (res.get('out') or [])][:7])
print('mailbox',q("SELECT count(*) FROM hop"),'closed',q("SELECT count(*),sum(again) FROM closed"),'fire_ev',q("SELECT count(*) FROM fire_ev"),'refused rows',q("SELECT count(*) FROM refused"),q("SELECT count(*) FROM sixth.refused"))
