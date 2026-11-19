import sys, os, json, pickle, re, collections, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v26", "/home/claude/zeneng/corpus/v25"]
os.chdir("/home/claude/zeneng/corpus/v26"); import build as Bd; os.chdir("/home/claude/zeneng/corpus/v34"); S = Bd.S
from sklearn.cluster import MiniBatchKMeans; from scipy.stats import rankdata, pearsonr, norm as Nm
norm = Bd.norm; rng = np.random.default_rng(0); W = 8
def wins(t, p):
    P = S.path(list(zip(t, p)))[:, [0, 1, 2, 5]]; return np.lib.stride_tricks.sliding_window_view(P, W, axis=0).reshape(len(P) - W + 1, -1)
pools = collections.defaultdict(list)   # source -> (title, artist, year, notes, windows)
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb"))
for s in G:
    if s["src"] == "HT" and s.get("year") and sum(len(c) for c in s["clips"]) >= 48:
        w = np.vstack([wins([n[0] for n in c], [n[1] for n in c]) for c in s["clips"] if len(c) >= W]); pools["HT"].append((s["title"], s["artist"], s["year"], sum(len(c) for c in s["clips"]), w))
seen = {}
for ln in open("/home/claude/corpus/parsed_lakh.jsonl"):
    r = json.loads(ln)
    if not r.get("bb"): continue
    ns = sorted({(float(n["off"]), int(n["p"])) for s in r["melody"]["sections"] for n in s["notes"] if "off" in n})
    if len(ns) < 48 or len({p for _, p in ns}) < 4: continue
    k = (norm(r["title"]), norm(r["bb"]["performer"]))
    if k in seen and seen[k][0] >= r["track_score"]: continue
    seen[k] = (r["track_score"], (k[0], k[1], int(r["bb"]["first"][:4]), len(ns), wins([n[0] for n in ns], [n[1] for n in ns])))
pools["LK"] = [v[1] for v in seen.values()]; seen = {}
for f in sorted(os.listdir(Bd.D + "syllable_level_npy_39")):
    m = Bd.match(Bd.J.get(f[:-4], f))
    if not m: continue
    try:
        a = np.load(Bd.D + "syllable_level_npy_39/" + f, allow_pickle=True, encoding="latin1"); notes = a[0][1]; t = []; now = 0.0
        for p, d, r in notes: now += float(r); t.append(now); now += float(d)
        p = [int(n[0]) for n in notes]
    except Exception: continue
    if len(p) < 48 or len(set(p)) < 4: continue
    k = (m[1].t, m[1].a)
    if k in seen and seen[k][3] >= len(p): continue
    seen[k] = (k[0], k[1], int(m[1].year), len(p), wins(t, p))
pools["LM"] = list(seen.values()); print({k: len(v) for k, v in pools.items()}, flush=True)
samp = np.vstack([v[4][rng.choice(len(v[4]), min(len(v[4]), 40), replace=False)] for src in pools for v in pools[src]]); km = MiniBatchKMeans(64, random_state=0, n_init=3, batch_size=4096).fit(samp)
Y = pickle.load(open("/home/claude/zeneng/corpus/v25/yardstick.pkl", "rb"))   # only for the love/cover reading of Hot 100 songs: rebuild per (title, artist)
import importlib.util
S3 = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx")[["Performer", "Song", "spotify_track_popularity"]].dropna(); S3["t"] = S3.Song.map(norm); S3["a"] = S3.Performer.map(norm); byS = collections.defaultdict(list)
for r in S3.itertuples(): byS[r.t].append(r)
Bb = Bd.B; pop = S3.groupby(["t", "a"]).spotify_track_popularity.max().to_dict(); PY = Bb.assign(pop=[pop.get((t, a)) for t, a in zip(Bb.t, Bb.a)]).dropna(subset=["pop"])
Wk = collections.defaultdict(lambda: dict(n=0, perf=set(), titles=collections.Counter()))
for ln in open("/tmp/claude-0/shs/list", encoding="utf8", errors="ignore"):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 4: w = Wk[p[0]]; w["n"] += 1; w["perf"].add(norm(p[3])); w["titles"][norm(p[2])] += 1
shsT = collections.defaultdict(list)
for k, w in Wk.items():
    for t, c in w["titles"].items():
        if c >= 2 or c == w["n"]: shsT[t].append(k)
tabs = {}
for src, P in pools.items():
    H = np.array([np.sqrt(np.bincount(km.predict(v[4]), minlength=64) / len(v[4])) for v in P]); H = H / np.linalg.norm(H, axis=1, keepdims=True); yrs = np.array([v[2] for v in P]); tit = np.array([v[0] for v in P]); rows = []
    for i, (t, a, y, n, _) in enumerate(P):
        if y > 2005: continue
        h = [x for x in byS.get(t, []) if a and (a in x.a or x.a in a)]
        if not h: continue
        pp = max(x.spotify_track_popularity for x in h); other = tit != t; b = other & (yrs >= y - 10) & (yrs < y); f = other & (yrs > y) & (yrs <= y + 10); o = other & (np.abs(yrs - y) <= 2)
        if b.sum() < 30 or f.sum() < 30 or o.sum() < 30: continue
        cos = lambda m: float(H[i] @ (H[m].mean(0) / np.linalg.norm(H[m].mean(0)))); sb, sf = cos(b), cos(f)
        cov = max((Wk[k]["n"] for k in shsT.get(t, []) if any(a in q or (len(q) >= 4 and q in a) for q in Wk[k]["perf"])), default=0)
        rows.append(dict(src=src, title=t, artist=a, year=y, notes=n, N=1 - sb, F=sf - sb, T=cos(o), love=float((PY[(PY.year - y).abs() <= 3]["pop"].values < pp).mean()), cov0=cov))
    d = pd.DataFrame(rows); yr = d.year.values; d["cover_rank"] = [float((d.cov0.values[np.abs(yr - y) <= 5] < c).mean() + .5 * (d.cov0.values[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, d.cov0)]; d["G"] = (d.love + d.cover_rank) / 2; tabs[src] = d
pickle.dump(tabs, open("newness.pkl", "wb"))
def part(d, m, g):
    C = np.c_[np.ones(len(d)), rankdata(d.year), rankdata(d.notes)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(d[m])), res(rankdata(d[g]))); return float(r), float(p), len(d)
out = {}
for m in ("N", "F", "T"):
    R = [part(tabs[s], m, "G") for s in ("HT", "LK", "LM")]; z = sum(np.sign(r) * Nm.isf(p / 2) * np.sqrt(n) for r, p, n in R) / np.sqrt(sum(n for _, _, n in R)); pp = 2 * Nm.sf(abs(z)); ok = m != "T" and all(r > 0 for r, _, _ in R) and sum(p < .05 for _, p, _ in R) >= 2 and pp < .025
    out[m] = dict(HT_LK_LM=[(round(r, 3), round(p, 4), n) for r, p, n in R], pooled_z=round(float(z), 2), pooled_p=round(float(pp), 5), love=[round(part(tabs[s], m, "love")[0], 3) for s in ("HT", "LK", "LM")], covers=[round(part(tabs[s], m, "cover_rank")[0], 3) for s in ("HT", "LK", "LM")], verdict="PASS" if ok else ("-" if m == "T" else "fail")); print(m, out[m])
allr = pd.concat([d.assign(Gr=rankdata(d.G) / len(d), Nr=rankdata(d.N) / len(d)) for d in tabs.values()]); allr["fifth"] = np.ceil(allr.Nr * 5).clip(1, 5); print(allr.groupby("fifth").Gr.agg(["size", "mean"]).round(3).T.to_string()); json.dump(out, open("newness_results.json", "w"), indent=1)
