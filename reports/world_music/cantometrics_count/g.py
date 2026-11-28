import csv, sys, collections
D=sys.argv[1]
soc={}
with open(D+'/cldf/societies.csv',encoding='utf-8-sig') as f:
    for r in csv.DictReader(f): soc[r['society_id']]=r
songs={}
with open(D+'/cldf/songs.csv',encoding='utf-8-sig') as f:
    for r in csv.DictReader(f): songs[r['song_id']]=r
codes=collections.defaultdict(lambda: collections.defaultdict(set))
with open(D+'/cldf/data.csv',encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        try: v=int(float(r['code']))
        except: continue
        for k in range(0,20):
            if v>>k & 1: codes[r['var_id']][r['song_id']].add(k)
def group(sid):
    g=group0(sid)
    return 'SSA' if g.startswith('SSA') else g
def group0(sid):
    s=songs[sid]; so=soc.get(s['society_id'],{})
    reg=s['Region']
    if reg=='Africa': return 'N_Africa' if s['Division']=='Northern Africa' else 'SSA_'+s['Division'].split()[0]
    p=(so.get('People','')+'|'+so.get('People2','')+'|'+so.get('People3','')).lower()
    if reg in ('North America','Central America','South America') and so.get('society','')!='Indo-Trinidad' and ('african' in p or 'afro-c' in p or 'afro-i' in p or 'creole' in p) :
        return 'Dia_US' if reg=='North America' else 'Dia_CarSAm'
    if reg=='Europe': return 'Europe'
    return 'Other'
G={sid:group(sid) for sid in songs}
print(collections.Counter(G.values()))
nsoc=collections.defaultdict(set)
for sid in songs: nsoc[G[sid]].add(songs[sid]['society_id'])
print({k:len(v) for k,v in nsoc.items()})
dsoc=collections.Counter(soc[songs[s]['society_id']]['society'] for s in songs if G[s].startswith('Dia'))
print('diaspora societies',len(dsoc), sorted(dsoc.items(), key=lambda x:-x[1])[:60])
order=['SSA','Dia_US','Dia_CarSAm','Dia_all','N_Africa','Europe','Other']
def table(var, sets):
    print('\n==',var)
    hdr='set'.ljust(24)+''.join(g[:11].rjust(12) for g in order); print(hdr)
    n={g:sum(1 for s in codes[var] if G.get(s)==g or (g=='Dia_all' and G.get(s,'').startswith('Dia_'))) for g in order}
    print('n coded'.ljust(24)+''.join(str(n[g]).rjust(12) for g in order))
    for name,st in sets:
        row=name.ljust(24)
        for g in order:
            k=sum(1 for s,cs in codes[var].items() if (G.get(s)==g or (g=='Dia_all' and G.get(s,'').startswith('Dia_') and G.get(s)!='Dia_all')) and cs&st)
            row+=f"{k/n[g]:.3f}".rjust(12) if n[g] else 'na'.rjust(14)
        print(row)
table('line_1',[('solo 2-3',{2,3}),('solo alternating 4',{4}),('leader+unison 5',{5}),('unison 6',{6}),('diffuse 7',{7}),('leader-group alt 8',{8}),('group-group alt 9',{9}),('ldr overlap 10',{10}),('grp-ldr overlap 11',{11}),('grp-grp overlap 12',{12}),('interlock 13',{13}),('ANY alternation 8-12',{8,9,10,11,12}),('ANY overlap 10-12',{10,11,12}),('overlap or interlock',{10,11,12,13}),('leader-chorus 8,10,11',{8,10,11})])
table('line_16',[('through-composed 1',{1}),('complex strophe 2-3',{2,3}),('simple strophe 4-6',{4,5,6}),('complex litany 7-9',{7,8,9}),('simple litany 10-12',{10,11,12}),('simple litany exact 12',{12}),('canon/round 13',{13}),('any litany 7-12',{7,8,9,10,11,12})])
table('line_10',[('wordy 1',{1}),('some 4',{4}),('half 7',{7}),('quite 10',{10}),('extreme 13',{13}),('>=half 7-13',{7,10,13})])
table('line_18',[('>8 phrases 1',{1}),('5 or 7 :3',{3}),('4/8 asym 5',{5}),('4/8 sym 6',{6}),('3/6 asym 8',{8}),('3/6 sym 9',{9}),('2 asym 11',{11}),('1-2 sym 13',{13}),('<=2 phrases 11,13',{11,13})])
table('line_17',[('very long 1',{1}),('long 4',{4}),('medium 7',{7}),('short 10',{10}),('very short 13',{13})])
table('line_11',[('one-beat 3',{3}),('simple metre 6',{6}),('complex metre 9',{9}),('irregular 11',{11}),('parlando rubato 13',{13})])
