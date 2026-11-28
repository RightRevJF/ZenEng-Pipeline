import csv, sys, collections, runpy
D=sys.argv[1]
ns=runpy.run_path('/tmp/scripts_canto/g.py', run_name='lib') if False else None
soc={}; songs={}
for r in csv.DictReader(open(D+'/cldf/societies.csv',encoding='utf-8-sig')): soc[r['society_id']]=r
for r in csv.DictReader(open(D+'/cldf/songs.csv',encoding='utf-8-sig')): songs[r['song_id']]=r
codes=collections.defaultdict(lambda: collections.defaultdict(set))
for r in csv.DictReader(open(D+'/cldf/data.csv',encoding='utf-8-sig')):
    try: v=int(float(r['code']))
    except: continue
    for k in range(20):
        if v>>k&1: codes[r['var_id']][r['song_id']].add(k)
def grp(sid):
    s=songs[sid]; so=soc.get(s['society_id'],{}); reg=s['Region']
    if reg=='Africa': return None if s['Division']=='Northern Africa' else 'SSA'
    p=(so.get('People','')+'|'+so.get('People2','')+'|'+so.get('People3','')).lower()
    if reg in ('North America','Central America','South America') and so.get('society','')!='Indo-Trinidad' and ('african' in p or 'afro-c' in p or 'afro-i' in p or 'creole' in p): return 'Diaspora'
    if reg=='Europe': return 'Europe'
    return 'Other'
G={s:grp(s) for s in songs}
CR={8,9,10,11,12}
print('Among call-and-response songs (line_1 in 8-12): line_16 and line_18')
for g in ['SSA','Diaspora','Europe','Other']:
    ids=[s for s,c in codes['line_1'].items() if G.get(s)==g and c&CR]
    n=len(ids)
    l16=codes['line_16']; l18=codes['line_18']
    def sh(var,st): return sum(1 for s in ids if codes[var].get(s,set())&st)/n
    print(g,'n',n,'simple litany any(10-12) %.3f exact(12) %.3f; complex litany(7-9) %.3f; strophe(2-6) %.3f; through(1) %.3f; <=2 phrases %.3f'%(sh('line_16',{10,11,12}),sh('line_16',{12}),sh('line_16',{7,8,9}),sh('line_16',{2,3,4,5,6}),sh('line_16',{1}),sh('line_18',{11,13})))
print('\nSociety-weighted (mean of per-society shares) line_1')
for g in ['SSA','Diaspora','Europe','Other']:
    per=collections.defaultdict(list)
    for s,c in codes['line_1'].items():
        if G.get(s)==g: per[songs[s]['society_id']].append(c)
    def w(st): return sum(sum(1 for c in L if c&st)/len(L) for L in per.values())/len(per)
    print(g,'societies',len(per),'alternation %.3f overlap %.3f interlock %.3f solo %.3f'%(w(CR),w({10,11,12}),w({13}),w({2,3})))
print('\nmulticoded line_1 share', {g: round(sum(1 for s,c in codes['line_1'].items() if G.get(s)==g and len(c)>1)/max(1,sum(1 for s in codes['line_1'] if G.get(s)==g)),3) for g in ['SSA','Diaspora','Europe','Other']})
