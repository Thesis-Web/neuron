import sys; sys.path.insert(0,'/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad')
from hublib import *
s=82; c=q(f'SELECT call FROM sixth."{s}" WHERE before=6 AND trigger=68')[0][0]; t=text_of(c,'sixth').replace('6> ','',1)
a="UPDATE sixth.spawned SET shared = shared + 1 WHERE gate IN ( SELECT DISTINCT CAST ( j.value AS INTEGER ) FROM main.run_sheet s , json_each ( '[' || replace ( s.value , ' ' , ',' ) || ']' ) j WHERE s.run = what AND s.cell = ( SELECT gate FROM main.label WHERE symbol = 'unknown' ) AND s.value <> '' ) ; "
assert t.count(a)==1; n=t.replace(a,"")
j,dt=typ('6> '+n,'sixth'); r=(j.get('result') or {}).get('run'); print('hub line laid',r,round(dt,1),'s',j.get('error')); assert r
j,dt=typ(f'6> BUILD UPDATE sixth."{s}" SET call = {r} WHERE before = 6 AND trigger = 68 ; BUILD','sixth')
print('hub seen',q(f'SELECT call FROM sixth."{s}" WHERE before=6 AND trigger=68'),'was',c)
a0=q("SELECT count(*) FROM sixth.spawned WHERE sent=1")[0][0]; t0=time.time(); time.sleep(60); b0=q("SELECT count(*) FROM sixth.spawned WHERE sent=1")[0][0]; i=get('/api/info')
print('hub defines a minute',round((b0-a0)/(time.time()-t0)*60),'sent',b0,i['routers'])
j,dt=typ('define : know'); print('define : know',round(dt,2),'s refused',(j.get('result') or {}).get('refused'))
