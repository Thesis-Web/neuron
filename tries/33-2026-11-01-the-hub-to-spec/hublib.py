import json,urllib.request,time
B='http://127.0.0.1:8056'
def post(path,body,t=600):
    r=urllib.request.Request(B+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r,timeout=t))
def get(path,t=60): return json.load(urllib.request.urlopen(B+path,timeout=t))
def q(sql,t=120):
    r=post('/api/q',{'sql':sql},t); 
    if 'rows' not in r: raise Exception(str(r)[:300])
    return r['rows']
def typ(line,prompt='main'):
    t=time.time(); j=post('/api/type',{'line':line,'prompt':prompt})
    while not j.get('done'): time.sleep(0.2); j=get('/api/job?id=%d'%j['id'])
    return j,time.time()-t
def text_of(run,s='main'): return q(f"SELECT group_concat(symbol,'') FROM (SELECT l.symbol FROM {s}.seq x JOIN {s}.label l ON l.gate=x.gate WHERE x.run={run} ORDER BY x.pos)")[0][0]
