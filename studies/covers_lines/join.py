"""Design B, step 1: the join, from titles and credits only (no lyric is read here).
Inputs (committed, no lyric text): data/wasabi_english_meta.csv.gz (the data scout's WASABI metadata, English songs of 8 lines or more)
and data/dvi_cliques_writers.csv.gz (the data scout's Discogs-VI reduction); see data/README.md.
Writes /home/claude/lyr_dl/covers_join.csv: id, writer, title, matched, n_artists, year (clique's first year, else WASABI's).
The matching rule is the data scout's (scout_scripts/wasabi_match.py), unchanged."""
import csv, re, collections, sys, gzip, os
csv.field_size_limit(10**9)
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"); OUT = "/home/claude/lyr_dl/covers_join.csv"
def norm(s): s = s.lower().replace('&', 'and'); s = re.sub(r'\(.*?\)|\[.*?\]', '', s); s = re.sub(r'\s(feat|featuring|ft)\.?\s.*', '', s); s = re.sub(r'^the ', '', s.strip()); return re.sub(r'[^a-z0-9]', '', s)
def amatch(a, b): return a and b and (a[:6] in b or b[:6] in a)
key = {}
for r in csv.DictReader(gzip.open(os.path.join(D, "wasabi_english_meta.csv.gz"), "rt", newline="")):
    if r["language"] not in ("english", "en", "eng") or int(r["n_lines"]) < 8: continue
    k = (norm(r["artist"]), norm(r["title"]))
    if k[0] and k[1] and (k not in key or int(r["n_lines"]) > int(key[k]["n_lines"])): key[k] = r
dvi = collections.defaultdict(list)
for r in csv.DictReader(gzip.open(os.path.join(D, "dvi_cliques_writers.csv.gz"), "rt", newline="")): dvi[norm(r["title"])].append(r)
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
