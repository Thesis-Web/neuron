import sys; sys.path.insert(0,'/tmp/claude-1000/-home-exnulla-neuron-v3/6e671b3d-5812-4b8a-be01-22485eca8de9/scratchpad')
from hublib import *
j,dt=typ('6> BUILD CREATE INDEX IF NOT EXISTS sixth.asked_unsent ON asked ( sent ) WHERE sent = 0 ; BUILD','sixth'); print('hub index',round(dt,1),'s',str((j.get('result') or {}).get('out'))[:110],j.get('error'))
a=q("SELECT count(*) FROM sixth.spawned WHERE sent=1")[0][0]; g0=get('/api/info')['routers']; t0=time.time(); time.sleep(50); b=q("SELECT count(*) FROM sixth.spawned WHERE sent=1")[0][0]; g1=get('/api/info')['routers']; dt=time.time()-t0
print('hub defines a minute',round((b-a)/dt*60),'sent',b,'refused',g1['main']['refused'],g1['sixth']['refused'],'hops',g1['main']['hops']-g0['main']['hops'],g1['sixth']['hops']-g0['sixth']['hops'])
p=get('/api/prof')
for k,v in list(p.items())[:5]: print(f"{v[1]:8.2f} s  n {v[0]:6d}  {1000*v[1]/max(1,v[0]):9.1f} ms  {k}")
j,dt=typ('define : know'); print('LIVE define : know',round(dt,2),'s refused',(j.get('result') or {}).get('refused'))
