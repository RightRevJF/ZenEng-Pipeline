"""Design B, step 1: the join, from titles and credits only (no lyric is read here).
Inputs outside the repo: the data scout's WASABI metadata (songs_meta.csv) and Discogs-VI reduction (cliques.csv).
Writes /home/claude/lyr_dl/covers_join.csv: id, writer, title, matched, n_artists, year (clique's first year, else WASABI's).
The matching rule is the data scout's (scout_scripts/wasabi_match.py), unchanged."""
import csv, re, collections, sys
csv.field_size_limit(10**9)
W = "/home/claude/lyr_dl/scout/"; OUT = "/home/claude/lyr_dl/covers_join.csv"
def norm(s): s = s.lower().replace('&', 'and'); s = re.sub(r'\(.*?\)|\[.*?\]', '', s); s = re.sub(r'\s(feat|featuring|ft)\.?\s.*', '', s); s = re.sub(r'^the ', '', s.strip()); return re.sub(r'[^a-z0-9]', '', s)
def amatch(a, b): return a and b and (a[:6] in b or b[:6] in a)
key = {}
for r in csv.DictReader(open(W + "wasabi/songs_meta.csv")):
    if r["language"] not in ("english", "en", "eng") or int(r["n_lines"]) < 8: continue
    k = (norm(r["artist"]), norm(r["title"]))
    if k[0] and k[1] and (k not in key or int(r["n_lines"]) > int(key[k]["n_lines"])): key[k] = r
dvi = collections.defaultdict(list)
for r in csv.DictReader(open(W + "dvi_writers/cliques.csv")): dvi[norm(r["title"])].append(r)
byA = collections.defaultdict(list)
for (a, t), r in key.items(): byA[a].append((t, r))
rows = []; per = collections.Counter()
for a, v in byA.items():
    if len(v) < 10: continue
    for t, r in v:
        cands = [c for c in dvi.get(t, []) if any(amatch(a, norm(w)) or (len(a) > 5 and a[-6:] in norm(w)) for w in c["writers"].split("|"))]
        best = max(cands, key=lambda c: int(c["n_artists"])) if cands else None
        y = (best["first_year"] if best and best["first_year"] else r["year"]) or ""
        rows.append(dict(id=r["id"], writer=a, title=t, matched=int(best is not None), n_artists=int(best["n_artists"]) if best else 1, year=y))
        per[a] += best is not None
keep = {a for a, n in per.items() if n >= 10}
rows = [r for r in rows if r["writer"] in keep]
w = csv.DictWriter(open(OUT, "w", newline=""), list(rows[0])); w.writeheader(); w.writerows(rows)
print("writers", len(keep), "songs", len(rows), "matched", sum(r["matched"] for r in rows))
