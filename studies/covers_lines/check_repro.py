import sys, re, csv, html, zipfile, ijson, json, collections
sys.path.insert(0, "/home/claude/rightrevjf/zeneng-pipeline/studies/covers_lines")
import linefeat as LF
def norm(s): s = s.lower().replace('&', 'and'); s = re.sub(r'\(.*?\)|\[.*?\]', '', s); s = re.sub(r'\s(feat|featuring|ft)\.?\s.*', '', s); s = re.sub(r'^the ', '', s.strip()); return re.sub(r'[^a-z0-9]', '', s)
def amatch(a, b): return a and b and (a[:6] in b or b[:6] in a)
dvi = collections.defaultdict(list)
for c in json.load(open("/home/claude/shape/discogs_cliques.json")): dvi[c["title"]].append((len(c["artists"]), c.get("first_year"), [norm(w) for w in c.get("writers") or []]))
best = {}; n = 0
for o in ijson.items(zipfile.ZipFile("/home/claude/lyr_dl/wasabi/json/json.zip").open("song.json"), "item"):
    n += 1
    if (o.get("language_detect") or "") != "english" or not o.get("lyrics"): continue
    a = norm(o.get("name") or ""); t = norm(o.get("title") or "")
    if not a or not t or t not in dvi: continue
    cands = [c for c in dvi[t] if any(amatch(a, w) or (len(a) > 5 and a[-6:] in w) for w in c[2])]
    if not cands: continue
    b = max(cands, key=lambda c: c[0]); tx = html.unescape(o["lyrics"]); st = [[re.sub(r"<.*?>", " ", l).strip() for l in re.split(r"<br\s*/?>", s)] for s in re.split(r"(?:<br\s*/?>\s*){2,}", tx)]
    f = LF.features(st)
    if f is None: continue
    m = re.match(r"(\d{4})", (o.get("publicationDate") or "") or (o.get("publicationDateAlbum") or "")); f.update(writer=a, title=t, n_artists=b[0], year=b[1] or (m.group(1) if m else ""))
    if (a, t) not in best or best[(a, t)]["n_lines"] < f["n_lines"]: best[(a, t)] = f
rows = list(best.values()); w = csv.DictWriter(open("feat.csv", "w", newline=""), list(rows[0])); w.writeheader(); w.writerows(rows); print(n, len(rows))
