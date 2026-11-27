import json,csv,sys,os,statistics as st
R=sys.argv[1]
PC={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def parse(c):
    c=c.strip()
    if c in('N','X',''): return None
    r,q=c.split(':',1) if ':' in c else (c,'maj')
    p=PC[r[0]]+sum({'#':1,'b':-1}[x] for x in r[1:])
    q=q.split('/')[0]
    base=q.split('(')[0]
    return p%12,base
def isii(b): return b=='min7'
def isV(b): return b in('7','9','13')
def share(seq,wrap=False):
    s=[x for x in seq]
    # collapse repeats
    out=[]
    for x in s:
        if not out or x!=out[-1]: out.append(x)
    pairs=list(zip(out,out[1:]))
    if wrap and len(out)>1 and out[0]!=out[-1]: pairs.append((out[-1],out[0]))
    pairs=[(a,b) for a,b in pairs if a and b]
    n=len(pairs); k=sum(1 for a,b in pairs if isii(a[1]) and isV(b[1]) and (b[0]-a[0])%12==5)
    return k,n
L=json.load(open(f'{R}/lead_sheets.json')); M=json.load(open(f'{R}/metadata.json'))
lead={}
for l in L:
    seq=[];prev=None
    for bar in l['chord_changes']:
        for t in bar.split():
            if t!='%': prev=t
            seq.append(parse(prev))
    lead[l['title']]=share(seq,wrap=True)
def rows(p): return list(csv.DictReader(open(p)))
res={}
for m in M:
    ch=[(float(r['time']),r['chord']) for r in rows(f"{R}/{m['files']['chords']}")]
    stc=[(float(r['time']),r['name'].split(':')[0]) for r in rows(f"{R}/{m['files']['structure']}")]
    sg=[(float(r['start']),float(r['end'])) for r in rows(f"{R}/{m['files']['segments']}")]
    end=m['audio_length']
    secs=[(t,(stc[i+1][0] if i+1<len(stc) else end),n) for i,(t,n) in enumerate(stc)]
    for kind in('head','solo'):
        K=N=0
        for a,b,n in secs:
            if n!=kind: continue
            for s0,s1 in sg:
                lo,hi=max(a,s0),min(b,s1)
                if hi<=lo: continue
                seq=[parse(c) for t,c in ch if lo-1e-6<=t<hi]
                # chord sounding at lo
                before=[c for t,c in ch if t<lo-1e-6]
                if before and (not seq or True): seq=[parse(before[-1])]+seq
                k,n2=share(seq); K+=k;N+=n2
        res.setdefault(m['standard'],{}).setdefault(kind,[]).append((K,N))
H=[];S=[];LS=[]
diffs=[]
for t,(k,n) in lead.items():
    ls=k/n
    hs=[a/b for a,b in res[t].get('head',[]) if b]; ss=[a/b for a,b in res[t].get('solo',[]) if b]
    hm=st.mean(hs) if hs else float('nan'); sm=st.mean(ss) if ss else float('nan')
    LS.append(ls);H.append(hm);S.append(sm);diffs.append((t,round(ls,3),round(hm,3),round(sm,3),len(hs),len(ss)))
import math
ok=[(l,h,s) for l,h,s in zip(LS,H,S) if not math.isnan(h) and not math.isnan(s)]
print('n',len(ok),'mean lead',round(st.mean(x[0] for x in ok),3),'head',round(st.mean(x[1] for x in ok),3),'solo',round(st.mean(x[2] for x in ok),3))
print('tunes solo>lead',sum(1 for l,h,s in ok if s>l),'head>lead',sum(1 for l,h,s in ok if h>l))
from statistics import correlation
print('corr lead-head',round(correlation([x[0] for x in ok],[x[1] for x in ok]),2),'lead-solo',round(correlation([x[0] for x in ok],[x[2] for x in ok]),2))
for d in sorted(diffs,key=lambda d:(d[3]-d[1]) if not math.isnan(d[3]) else 0): print(d)
