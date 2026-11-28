import csv, sys, collections
D=sys.argv[1]
songs={}
with open(D+'/cldf/songs.csv',encoding='utf-8-sig') as f:
    for r in csv.DictReader(f): songs[r['song_id']]=r
codes=collections.defaultdict(lambda: collections.defaultdict(set))
with open(D+'/cldf/data.csv',encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        try: c=int(float(r['code']))
        except: continue
        codes[r['var_id']][r['song_id']].add(c)
print('songs',len(songs))
# region list
reg=collections.Counter(s['Region'] for s in songs.values()); print(reg)
div=collections.Counter((s['Region'],s['Division']) for s in songs.values() if s['Region'] in('Africa','North America','South America','Central America','Caribbean')); 
for k,v in sorted(div.items()): print(k,v)
