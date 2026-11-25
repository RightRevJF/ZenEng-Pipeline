"""Stream Discogs-VI cliques from stdin; write one row per clique: id, title, top writers, n versions, n distinct artists, first year, genre."""
import sys,json,csv,re,collections
out=csv.writer(open(sys.argv[1],'w',newline=''))
out.writerow(['clique_id','title','writers','writer_ids','n_versions','n_artists','first_year','genre'])
n=0
for line in sys.stdin:
    n+=1
    c=json.loads(line)
    T=collections.Counter();W=collections.Counter();WI=collections.Counter();A=set();yrs=[];G=collections.Counter()
    for v in c['versions']:
        for t in v['tracks'][:1]:
            T[(t.get('track_title_cleaned') or t['track_title']).lower()]+=1
            ws=t['track_writer_names'] or t['release_writer_names']; wi=t['track_writer_ids'] or t['release_writer_ids']
            for w in ws: W[w]+=1
            for w in wi: WI[w]+=1
            for a in (t['track_artist_names'] or t['release_artist_names']): A.add(re.sub(r'\s\(\d+\)$','',a).lower())
            y=str(t.get('released',''))[:4]
            if y.isdigit() and int(y)>1880: yrs.append(int(y))
            for g in t['release_genres']: G[g]+=1
    out.writerow([c['clique_id'],T.most_common(1)[0][0] if T else '','|'.join(w for w,_ in W.most_common(4)),'|'.join(w for w,_ in WI.most_common(4)),len(c['versions']),len(A),min(yrs) if yrs else '',G.most_common(1)[0][0] if G else ''])
    if n%50000==0: print(n,file=sys.stderr,flush=True)
print('done',n,file=sys.stderr)
