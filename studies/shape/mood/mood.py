import sys, os, json, pickle, re, collections, hashlib, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v26", "/home/claude/zeneng/corpus/v25"]
os.chdir("/home/claude/zeneng/corpus/v26"); import build as Bd; os.chdir("/home/claude/zeneng/corpus/v35"); S = Bd.S
from sklearn.cluster import MiniBatchKMeans; from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler; from scipy.stats import rankdata, pearsonr, spearmanr, norm as Nm
norm = Bd.norm; rng = np.random.default_rng(0); W = 8
def wins(t, p):
    P = S.path(list(zip(t, p)))[:, [0, 1, 2, 5]]; return np.lib.stride_tricks.sliding_window_view(P, W, axis=0).reshape(len(P) - W + 1, -1)
def feats(clips, tempo=None):
    t = np.concatenate([np.asarray([n[0] for n in c], float) for c in clips]); p = np.concatenate([np.asarray([n[1] for n in c], float) for c in clips]); io = np.concatenate([np.diff([n[0] for n in c]) for c in clips]); iv = np.concatenate([np.diff([n[1] for n in c]) for c in clips]); iv = iv[io > 0]; io = io[io > 0]
    d = np.clip(np.r_[io, np.median(io)][:len(p)] if len(io) + 1 >= len(p) else np.ones(len(p)), .25, 4); h = np.bincount(p.astype(int) % 12, d[:len(p)], 12); cm = [np.corrcoef(np.roll(S.MAJ, k), h)[0, 1] for k in range(12)]; cn = [np.corrcoef(np.roll(S.MIN, k), h)[0, 1] for k in range(12)]; k = int(np.argmax(cm)) if max(cm) >= max(cn) else int(np.argmax(cn)); deg = np.roll(h, -k) / h.sum()
    fr = t % 1; slopes = [np.polyfit(np.arange(8), p[i:i + 8], 1)[0] for i in range(0, len(p) - 8, 4)]
    return [np.median(np.log2(io)), np.std(np.log2(io)), float((np.minimum(fr, 1 - fr) > .1).mean()), np.percentile(p, 90) - np.percentile(p, 10), np.abs(iv).mean(), float((np.abs(iv) > 4).mean()), float((iv == 0).mean()), float((iv < 0).sum() / max((iv != 0).sum(), 1)), float(np.mean(slopes)), float(np.mean(np.abs(slopes))), max(cn) - max(cm), deg[0], deg[3], deg[4], deg[7], deg[8], deg[9], deg[10], deg[11], float((io >= 2).mean()), float((io >= 4).mean()), np.log(len(p))] + ([np.log(tempo)] if tempo else [])
pools = collections.defaultdict(list)
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb"))
for s in G:
    if s["src"] == "HT" and s.get("year") and sum(len(c) for c in s["clips"]) >= 48: pools["HT"].append((s["title"], s["artist"], s["year"], s["peak"], [c for c in s["clips"] if len(c) >= 9], None))
seen = {}
for ln in open("/home/claude/corpus/parsed_lakh.jsonl"):
    r = json.loads(ln)
    if not r.get("bb"): continue
    ns = sorted({(float(n["off"]), int(n["p"])) for s in r["melody"]["sections"] for n in s["notes"] if "off" in n})
    if len(ns) < 48 or len({p for _, p in ns}) < 4: continue
    k = (norm(r["title"]), norm(r["bb"]["performer"]))
    if k in seen and seen[k][0] >= r["track_score"]: continue
    seen[k] = (r["track_score"], (k[0], k[1], int(r["bb"]["first"][:4]), r["bb"]["peak"], [ns], float(r.get("tempo") or 120)))
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
    if k in seen and len(seen[k][4][0]) >= len(p): continue
    seen[k] = (k[0], k[1], int(m[1].year), float(m[1].peak), [list(zip(t, p))], None)
pools["LM"] = list(seen.values())
SP = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx").dropna(subset=["spotify_track_popularity", "valence", "danceability"]); SP["t"] = SP.Song.map(norm); SP["a"] = SP.Performer.map(norm); byS = collections.defaultdict(list)
for r in SP.itertuples(): byS[r.t].append(r)
pop = SP.groupby(["t", "a"]).spotify_track_popularity.max().to_dict(); Bb = Bd.B; PY = Bb.assign(pop=[pop.get((t, a)) for t, a in zip(Bb.t, Bb.a)]).dropna(subset=["pop"])
Wk = collections.defaultdict(lambda: dict(n=0, perf=set(), titles=collections.Counter()))
for ln in open("/tmp/claude-0/shs/list", encoding="utf8", errors="ignore"):
    q = ln.rstrip("\n").split("\t")
    if len(q) >= 4: w = Wk[q[0]]; w["n"] += 1; w["perf"].add(norm(q[3])); w["titles"][norm(q[2])] += 1
shsT = collections.defaultdict(list)
for k, w in Wk.items():
    for t, c in w["titles"].items():
        if c >= 2 or c == w["n"]: shsT[t].append(k)
samp = np.vstack([np.vstack([wins([n[0] for n in c], [n[1] for n in c]) for c in v[4]])[::7] for src in pools for v in pools[src]]); km = MiniBatchKMeans(64, random_state=0, n_init=3, batch_size=4096).fit(samp)
def part(d, m, g, C0=("year", "notes", "peak")):
    d = d.dropna(subset=[m, g]); C = np.c_[tuple([np.ones(len(d))] + [rankdata(d[c]) for c in C0])]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(d[m])), res(rankdata(d[g]))); return float(r), float(p), len(d)
tabs = {}
for src, P in pools.items():
    rows = []; X = []
    for (t, a, y, pk, clips, tempo) in P:
        h = [x for x in byS.get(t, []) if a and (a in x.a or x.a in a)]
        if not h or not clips: continue
        b = max(h, key=lambda x: x.spotify_track_popularity)
        try: w = np.vstack([wins([n[0] for n in c], [n[1] for n in c]) for c in clips]); f = feats(clips, tempo)
        except Exception: continue
        cov = max((Wk[k]["n"] for k in shsT.get(t, []) if any(a in q or (len(q) >= 4 and q in a) for q in Wk[k]["perf"])), default=0)
        rows.append(dict(src=src, title=t, artist=a, year=y, peak=pk if pk == pk and pk is not None else 50., notes=sum(len(c) for c in clips), val=b.valence, dan=b.danceability, love=float((PY[(PY.year - y).abs() <= 3]["pop"].values < b.spotify_track_popularity).mean()), cov0=cov)); X.append(np.r_[f, np.sqrt(np.bincount(km.predict(w), minlength=64) / len(w))])
    d = pd.DataFrame(rows); X = np.nan_to_num(np.array(X)); d["h"] = [int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 for a in d.artist]
    for tgt, name in (("val", "Vw"), ("dan", "Dw")):
        pr = np.zeros(len(d))
        for hh in (0, 1):
            a_, b_ = (d.h != hh).values, (d.h == hh).values; sc = StandardScaler().fit(X[a_]); pr[b_] = RidgeCV(alphas=np.logspace(0, 4, 13)).fit(sc.transform(X[a_]), d[tgt].values[a_]).predict(sc.transform(X[b_]))
        d[name] = pr
    print(f"{src}: songs {len(d)}; written reading tracks Spotify's: cheerfulness {spearmanr(d.Vw, d.val)[0]:+.3f}, danceability {spearmanr(d.Dw, d.dan)[0]:+.3f}", flush=True)
    g = d[d.year <= 2005].copy(); yr = g.year.values; g["cover_rank"] = [float((g.cov0.values[np.abs(yr - y) <= 5] < c).mean() + .5 * (g.cov0.values[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, g.cov0)]; g["G"] = (g.love + g.cover_rank) / 2; tabs[src] = g
pickle.dump(tabs, open("mood.pkl", "wb")); out = {}
for m, pred in (("Vw", -1), ("Dw", -1), ("val", 0), ("dan", 0)):
    R = [part(tabs[s], m, "G") for s in ("HT", "LK", "LM")]; z = sum(np.sign(r) * Nm.isf(p / 2) * np.sqrt(n) for r, p, n in R) / np.sqrt(sum(n for _, _, n in R)); pp = 2 * Nm.sf(abs(z)); ok = pred and all(r < 0 for r, _, _ in R) and sum(p < .05 for _, p, _ in R) >= 2 and pp < .025
    out[m] = dict(HT_LK_LM=[(round(r, 3), round(p, 4), n) for r, p, n in R], pooled_z=round(float(z), 2), pooled_p=round(float(pp), 5), love=[round(part(tabs[s], m, "love")[0], 3) for s in ("HT", "LK", "LM")], covers=[round(part(tabs[s], m, "cover_rank")[0], 3) for s in ("HT", "LK", "LM")], verdict=("PASS" if ok else "fail") if pred else "mark"); print(m, out[m])
json.dump(out, open("mood_results.json", "w"), indent=1)
