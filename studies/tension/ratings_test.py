"""Which score-only readings follow listeners? 100 CoCoPops songs, four listeners' continuous arousal (bar means), and the recording's RMS.
1) Within-song correlations of each reading with arousal (both demeaned within song), with a song-clustered bootstrap.
2) Models: features smoothed by an exponential memory of time constant tau (seconds, using each bar's length), fitted by ridge regression to
   within-song arousal, scored by R^2 on held-out songs (10-fold by song). Harmony and the other features get separate taus, after Farbood and
   Upham (2013). Score-only models (what the engine can plan) against the recording's loudness."""
import json, numpy as np, itertools
rng = np.random.default_rng(20261116)
F = json.load(open("cocopops_features.json"))
FEATS = ["tps_tonic", "tps_seq", "old", "diss", "pitch", "pmax", "onset_rate", "sung", "nct", "rms"]
songs = []
for k, s in F.items():
    if not s["varms"]: continue
    bars = [b for b in s["bars"] if b.get("arousal") is not None]
    if len(bars) < 20: continue
    sec = np.array([b["sec"] if b["sec"] and 0.5 < b["sec"] < 8 else np.nan for b in bars]); med = np.nanmedian(sec); sec = np.where(np.isnan(sec), med, sec)
    X = {}
    for f in FEATS:
        v = np.array([b.get(f) if b.get(f) is not None else np.nan for b in bars], float)
        if f in ("pitch", "pmax"):   # unsung bars: carry the last sung value forward, then the song mean
            last = np.nan
            for i in range(len(v)):
                if np.isnan(v[i]): v[i] = last
                else: last = v[i]
        m = np.nanmean(v) if np.isfinite(np.nanmean(v)) else 0.0
        X[f] = np.where(np.isnan(v), m, v)
    y = np.array([b["arousal"] for b in bars])
    songs.append(dict(name=k, X=X, y=y, sec=sec, labels=[b["label"] for b in bars]))
print(len(songs), "songs;", sum(len(s["y"]) for s in songs), "rated bars")
def dm(v): return v - v.mean()
# 1) within-song correlations, pooled
res = {}
for f in FEATS:
    def pooled(idx):
        a = np.concatenate([dm(songs[i]["X"][f]) for i in idx]); b = np.concatenate([dm(songs[i]["y"]) for i in idx])
        sa, sb = a.std(), b.std(); return float((a * b).mean() / (sa * sb)) if sa > 0 and sb > 0 else 0.0
    idx = np.arange(len(songs)); r = pooled(idx)
    boots = [pooled(rng.choice(idx, len(idx))) for _ in range(500)]
    per = [np.corrcoef(s["X"][f], s["y"])[0, 1] for s in songs if s["X"][f].std() > 0]
    res[f] = dict(r=round(r, 3), ci=[round(float(np.percentile(boots, 2.5)), 3), round(float(np.percentile(boots, 97.5)), 3)],
                  median_song_r=round(float(np.median(per)), 3), share_positive=round(float(np.mean(np.array(per) > 0)), 2))
    print(f"{f:11s} pooled r {res[f]['r']:+.3f} {res[f]['ci']}  median song r {res[f]['median_song_r']:+.3f}  positive in {res[f]['share_positive']:.0%}")
# 2) smoothed-feature models, CV by song
def ema(v, sec, tau):
    if tau <= 0: return v.copy()
    out = np.empty_like(v); acc = v[0]
    for i in range(len(v)):
        a = np.exp(-sec[i] / tau); acc = a * acc + (1 - a) * v[i]; out[i] = acc
    return out
def design(s, feats, tau_h, tau_o, lag_s=2.5):
    cols = []
    for f in feats:
        tau = tau_h if f in ("tps_tonic", "tps_seq", "old", "diss") else tau_o
        v = ema((s["X"][f] - s["X"][f].mean()) / (s["X"][f].std() or 1), s["sec"], tau)
        cols.append(v)
    M = np.column_stack(cols)
    # listeners answer late: shift the design forward by about lag_s seconds (whole bars)
    shift = int(round(lag_s / np.median(s["sec"])))
    if shift > 0: M = np.vstack([np.repeat(M[:1], shift, 0), M[:-shift]])
    return M
folds = np.array_split(rng.permutation(len(songs)), 10)
def cv(feats, tau_h, tau_o, lag_s=2.5, lam=10.0):
    ss_res = ss_tot = 0.0
    for k in range(10):
        test = set(folds[k].tolist()); tr = [i for i in range(len(songs)) if i not in test]
        A = np.vstack([design(songs[i], feats, tau_h, tau_o, lag_s) for i in tr]); b = np.concatenate([dm(songs[i]["y"]) for i in tr])
        w = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ b)
        for i in test:
            p = design(songs[i], feats, tau_h, tau_o, lag_s) @ w; yy = dm(songs[i]["y"])
            ss_res += ((yy - p) ** 2).sum(); ss_tot += (yy ** 2).sum()
    return 1 - ss_res / ss_tot
SCORE = ["tps_tonic", "tps_seq", "diss", "pitch", "pmax", "onset_rate", "sung", "nct"]
out = dict(correlations=res, models={})
for name, feats in [("old chord value alone", ["old"]), ("Lerdahl distance from tonic alone", ["tps_tonic"]), ("harmony (Lerdahl + dissonance)", ["tps_tonic", "tps_seq", "diss"]),
                    ("melody and texture only", ["pitch", "pmax", "onset_rate", "sung", "nct"]), ("score: all", SCORE), ("recording loudness alone", ["rms"]),
                    ("score + loudness", SCORE + ["rms"])]:
    grid = {}
    for th, to in itertools.product([0, 4, 8, 16, 24, 32], [0, 2, 4, 8]):
        grid[(th, to)] = cv(feats, th, to)
    best = max(grid, key=grid.get)
    out["models"][name] = dict(best_tau_harmony_s=best[0], best_tau_other_s=best[1], r2_cv=round(grid[best], 3), r2_no_memory=round(grid[(0, 0)], 3),
                               r2_short_memory_all=round(max(grid[(t, t2)] for t, t2 in grid if t == t2 or (t, t2) in [(4, 4), (8, 8)]), 3))
    print(f"{name:34s} best tau harmony {best[0]:2d}s other {best[1]}s  R2(cv) {grid[best]:.3f}  without memory {grid[(0,0)]:.3f}")
# 3) the harmony window: R^2 of the score model as harmony's tau grows, other tau fixed at its best
bo = out["models"]["score: all"]["best_tau_other_s"]
out["harmony_window_curve"] = {th: round(cv(SCORE, th, bo), 4) for th in [0, 2, 4, 8, 12, 16, 20, 24, 32, 48]}
print("harmony tau curve (score model):", out["harmony_window_curve"])
json.dump(out, open("ratings_results.json", "w"), indent=1)
