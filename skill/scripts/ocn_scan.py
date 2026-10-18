"""Scan full-council meetings on opencouncil.network for wealth tax terms.
Usage: python scripts/ocn_scan.py OUT.json slug [slug:committee1,committee2 ...]
Env: OCN_OUT (output and cache dir, default data/ocn), OCN_MIN_YEAR (default 2022).
Rate-limited to one request per 0.9 s; retries on 429. Text on that site is AI-generated from council records and
many councils have no summaries (only document titles and attendees), so hits are leads and silence is weak evidence."""
import re,sys,json,os,html,time,urllib.request,csv
from concurrent.futures import ThreadPoolExecutor
S=os.environ.get('OCN_OUT','data/ocn')
os.makedirs(S,exist_ok=True)
CACHE=S+'/ocn_cache'; os.makedirs(CACHE,exist_ok=True)
H={"User-Agent":"Mozilla/5.0"}
PAT=re.compile(r'(?i)wealth tax|wealth levy|tax on wealth|taxing wealth|wealth taxation|taxes on wealth|billionaire|millionaire|super-?rich|tax the rich|extreme wealth|net wealth')
import threading
_lk=threading.Lock(); _last=[0.0]
def get(u,tries=7):
    for k in range(tries):
        with _lk:
            wait=0.9-(time.time()-_last[0])
            if wait>0: time.sleep(wait)
            _last[0]=time.time()
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=40).read().decode('utf-8','replace')
        except urllib.error.HTTPError as e:
            if e.code==404: return ''
            time.sleep(20*(k+1) if e.code==429 else 3*(k+1))
        except Exception as e:
            time.sleep(3*(k+1))
    return None
def clean(t):
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t)))
def meeting(mid):
    p=f'{CACHE}/{mid}.txt'
    if os.path.exists(p): return open(p,encoding='utf-8').read()
    t=get(f'https://opencouncil.network/meetings/{mid}')
    if t is None: return None
    c=clean(t); open(p,'w',encoding='utf-8').write(c); return c
def council_committees(slug):
    t=get(f'https://opencouncil.network/councils/{slug}/committees')
    if t is None: return None
    cs=sorted(set(re.findall(r'href="/councils/%s/committees/([^"?]*)"'%re.escape(slug),t)))
    return [c for c in cs if re.match(r'^(full-|annual-|extraordinary-|ordinary-)?council(-meeting)?(-\d+)?$|^(full-)?council-meetings?$|^extraordinary-council(-\d+)?$|^annual-council(-\d+)?$|^council-and-annual',c)]
MIN_YEAR=int(os.environ.get('OCN_MIN_YEAR','2022'))
def list_meetings(slug,com):
    ids=[];page=1
    while True:
        u=f'https://opencouncil.network/councils/{slug}/committees/{com}'+(f'?page={page}' if page>1 else '')
        t=get(u)
        if not t: break
        items=re.findall(r'href="/meetings/(\d+)">[^<]*?(\d{1,2} \w+ (\d{4}))[^<]*<',t)
        if not items:
            items=[(i,'',str(MIN_YEAR)) for i in dict.fromkeys(re.findall(r'/meetings/(\d+)',t))]
        new=[i for i,_,y in items if i not in ids and int(y)>=MIN_YEAR]
        ids+=new
        if not items or all(int(y)<MIN_YEAR for _,_,y in items): break
        if f'page={page+1}' not in t: break
        page+=1
    return ids
def scan(spec):
    slug,_,extra=spec.partition(':')
    out=dict(slug=slug,committees=[],meetings=0,hits=[],errors=0)
    cs=extra.split(',') if extra else council_committees(slug)
    if cs is None: out['error']='no council page'; return out
    out['committees']=cs
    ids=[]
    for c in cs: ids+=list_meetings(slug,c)
    ids=list(dict.fromkeys(ids)); out['meetings']=len(ids)
    for mid in ids:
        t=meeting(mid)
        if t is None: out['errors']+=1; continue
        m=re.search(r'Open Council Network - [^-]+ - [^-]+ - ([\d/]+)',t)
        date=m.group(1) if m else ''
        for mm in PAT.finditer(t):
            ctx=t[max(0,mm.start()-200):mm.start()+300]
            if re.search(r'(?i)community wealth building',ctx) and not re.search(r'(?i)wealth tax|billionaire|millionaire',ctx): continue
            out['hits'].append(dict(mid=mid,date=date,kw=mm.group(0),ctx=ctx)); break
    return out
if __name__=='__main__':
    slugs=sys.argv[2:]
    res={}
    with ThreadPoolExecutor(2) as ex:
        for r in ex.map(scan,slugs):
            res[r['slug']]=r; print(r['slug'],r['committees'],'meetings',r['meetings'],'hits',len(r['hits']),'err',r['errors'],flush=True); json.dump(res,open(S+'/'+sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    json.dump(res,open(S+'/'+sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
