"""Fresh songs (J6b), the join and the test, as PREDICTION.md fixes them. Discogs-VI main.zip (Zenodo 13983028, CC BY-SA 4.0) streamed from
the path given; cliques reduced as studies/covers/discogs_cliques.py does; McGill songs matched as studies/covers/covers_match_discogs.py
matches (cleaned title, artist among the clique's performing artists, the clique with the most artist sets); songs whose clique is among the
version groups already matched to Hooktheory are dropped, as are songs in Hooktheory. Power printed before the estimate.
    python3 -I studies/fresh_songs/join_and_test.py /path/to/main.zip -> result.json"""
import zipfile, json, re, collections, sys, os
import numpy as np, statsmodels.api as sm
from scipy.stats import norm as N
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))
M = json.load(open(os.path.join(HERE, "measures.json"))); want = {r["t"] for r in M}
by = collections.defaultdict(list)
with zipfile.ZipFile(sys.argv[1]).open("main/Discogs-VI-20240701.jsonl") as f:
    for line in f:
        d = json.loads(line); titles = collections.Counter(); artists = set()
        for v in d["versions"]:
            for t in v["tracks"]: titles[t.get("track_title_cleaned") or ""] += 1
        title = norm(titles.most_common(1)[0][0]) if titles else ""
        if title not in want: continue
        for v in d["versions"]:
            for t in v["tracks"]:
                a = tuple(sorted(norm(x) for x in (t.get("track_artist_names") or t.get("release_artist_names") or [])))
                if a: artists.add(a)
        by[title].append(dict(id=d["clique_id"], artists={x for a in artists for x in a}, n_artist_sets=len(artists)))
SEEN = set(json.load(open(os.path.join(ROOT, "studies/judging_checks/within_artist/discogs_versions_matched.json")))["cliques"])
rows = []; drop = collections.Counter()
for r in M:
    cands = [q for q in by.get(r["t"], []) if r["a"] in q["artists"]]
    if not cands: drop["no version group"] += 1; continue
    q = max(cands, key=lambda q: q["n_artist_sets"])
    if r["in_hooktheory"]: drop["in Hooktheory"] += 1; continue
    if q["id"] in SEEN: drop["group already matched to Hooktheory"] += 1; continue
    rows.append(dict(r, covers=q["n_artist_sets"] - 1, clique=q["id"]))
print(len(M), "measured;", dict(drop), "->", len(rows), "fresh matched songs")
res = dict(n=len(rows), dropped=dict(drop))
z = lambda x: (np.asarray(x, float) - np.mean(x)) / np.std(x)
n = len(rows); res["power_for_minus_0.04"] = float(N.cdf(0.04 * np.sqrt(n) - 1.96)); print("power to see -0.04 at p<.05 (two-sided): %.2f" % res["power_for_minus_0.04"])
if n < 300: res["verdict"] = "too small: decides nothing"
y = z(np.log1p([r["covers"] for r in rows])); x = z([r["ch_rep"] for r in rows])
yr = z([r["year"] for r in rows]); mc = z(np.log([r["merged_chords"] for r in rows]))
lw = z(np.log([r["weeks"] for r in rows])); pk = z([r["peak"] for r in rows])
def fit(cols, yy=y, groups=None):
    A = sm.add_constant(np.column_stack(cols)); m = sm.OLS(yy, A).fit(cov_type="HC1") if groups is None else sm.OLS(yy, A).fit(cov_type="cluster", cov_kwds={"groups": groups})
    return dict(b=float(m.params[1]), se=float(m.bse[1]), p=float(m.pvalues[1]), lo=float(m.conf_int()[1][0]), hi=float(m.conf_int()[1][1]))
res["primary"] = fit([x, yr, mc]); res["sensitivity_weeks_peak"] = fit([x, yr, mc, lw, pk])
b, p = res["primary"]["b"], res["primary"]["p"]
if n >= 300: res["verdict"] = "holds on fresh songs" if (b <= -0.04 and p < .05) else "does not travel" if b > -0.02 else "unsettled"
# deciding nothing
art = collections.Counter(r["a"] for r in rows); keep = [i for i, r in enumerate(rows) if art[r["a"]] >= 2]
if len(keep) > 30:
    ids = sorted({rows[i]["a"] for i in keep}); D = np.array([[rows[i]["a"] == a for a in ids[1:]] for i in keep], float)
    yy = z(y[keep]); xx = z(x[keep]); A = sm.add_constant(np.column_stack([xx, yr[keep], mc[keep], D])); m = sm.OLS(yy, A).fit(cov_type="HC1")
    res["artist_fixed_effects"] = dict(n=len(keep), artists=len(ids), b=float(m.params[1]), se=float(m.bse[1]), p=float(m.pvalues[1]))
res["weeks_on_ch_rep"] = fit([x, yr], yy=lw)
t40 = [i for i, r in enumerate(rows) if r["peak"] <= 40]
res["top40_only"] = dict(n=len(t40), **fit([z(x[t40]), yr[t40], mc[t40]], yy=z(y[t40])))
res["covers_median"] = float(np.median([r["covers"] for r in rows])); res["share_no_cover"] = float(np.mean([r["covers"] == 0 for r in rows]))
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1); print(json.dumps(res, indent=1))
