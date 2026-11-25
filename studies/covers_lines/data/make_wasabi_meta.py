"""Read raw-deflate WASABI song.json (local-file-entry bytes) from argv[1]; write per-song metadata (no lyric text) to argv[2].
Top-level objects are separated by '\n},{\n'."""
import sys,zlib,struct,json,csv,re
f=open(sys.argv[1],'rb'); h=f.read(30); nl,el=struct.unpack('<HH',h[26:30]); f.read(nl+el)
d=zlib.decompressobj(-15)
out=csv.writer(open(sys.argv[2],'w',newline=''))
out.writerow(['id','artist','title','year','rank','isClassic','language','has_wiki','n_lines','n_stanzas','n_unique_lines','n_words','explicit'])
BR=re.compile(r'<br\s*/?>'); BR2=re.compile(r'(?:<br\s*/?>\s*){2,}'); TAG=re.compile(r'<[^>]+>|&\w+;'); W=re.compile(r"[A-Za-z']+")
n=bad=0
def emit(txt):
    global n,bad
    try: o=json.loads(txt)
    except Exception: bad+=1; return
    ly=o.get('lyrics') or ''
    st=[s for s in BR2.split(ly) if s.strip()]
    lines=[' '.join(l.split()).lower() for l in BR.split(ly) if l.strip()]
    out.writerow([o.get('_id',{}).get('$oid',''),o.get('name',''),o.get('title',''),str(o.get('publicationDate') or o.get('publicationDateAlbum') or '')[:4],o.get('rank',''),o.get('isClassic',''),o.get('language_detect') or o.get('language',''),1 if o.get('urlWikipedia') else 0,len(lines),len(st),len(set(lines)),len(W.findall(TAG.sub(' ',ly))),o.get('explicitLyrics','')])
    n+=1
    if n%200000==0: print(n,bad,file=sys.stderr,flush=True)
buf=''; first=True
while True:
    chunk=f.read(1<<24)
    if not chunk: break
    buf+=d.decompress(chunk).decode('utf-8','ignore')
    if first: buf=buf[buf.find('[')+1:]; first=False
    parts=buf.split('\n},{\n')
    buf=parts.pop()
    for i,p in enumerate(parts):
        if not p.startswith('{'): p='{'+p
        emit(p+'\n}')
buf=buf.strip().rstrip(']').strip()
if buf:
    if not buf.startswith('{'): buf='{'+buf
    emit(buf)
print('done',n,'bad',bad,file=sys.stderr)
