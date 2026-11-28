import csv, sys, collections
D=sys.argv[1]
soc={}
with open(D+'/cldf/societies.csv',encoding='utf-8-sig') as f:
    for r in csv.DictReader(f): soc[r['society_id']]=r
c=collections.Counter()
for s in soc.values():
    if s['Region'] in ('North America','Central America','South America'):
        c[(s['People3'],s['People2'])]+=1
for k,v in c.most_common(60): print(v,k)
afro=[s['society'] for s in soc.values() if 'afro' in (s['People']+s['People2']+s['People3']+s['society']).lower() or 'african' in (s['People2']+s['People3']+s['society']).lower() and s['Region']!='Africa']
print(len(afro), afro[:80])
