"""Run 07, cv_w_singletons: notes-only checks and fake-outcome power, by the first-principles reviewer, BEFORE any outcome of
these songs is joined. Never calls common.load_outcomes, common.run_test or test.main.
Usage: python3 -I notes_check.py notes_check.json  (a few minutes; the first call writes the notes-only shape cache)"""
import os, sys, json, math, hashlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from scipy import stats
import common as C
spec = importlib.util.spec_from_file_location("cvw_test", os.path.join(HERE, "test.py")); T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)                                         # defines functions only; main() is not called

out = {}
S, n_shared = T.singleton_songs()
out["counts"] = dict(singletons_kept=len(S), dropped_shared_file=n_shared, artists=len({s["artist_key"] for s in S}))
# the outcome cache of the 5,901 seen songs must hold none of these keys (keys only; no value is read)
seen_keys = set(json.load(open(T.WITHIN_CACHE))["songs"].keys())
out["counts"]["singleton_keys_in_seen_outcome_cache"] = sum(s["key"] in seen_keys for s in S)
S = C.add_shapes(S, cache=T.SHAPE_CACHE)
X = T.design(S); ok = np.isfinite(X).all(1)
out["counts"]["model_rows"] = int(ok.sum()); out["counts"]["halves"] = [int(sum(s["half"] == h for s, k in zip(S, ok) if k)) for h in (0, 1)]
v = np.array([s["cv_w"] for s in S], float)
out["cv_w"] = dict(finite=int(np.isfinite(v).sum()), pct10_50_90=[float(x) for x in np.nanpercentile(v, [10, 50, 90])],
                   mean=float(np.nanmean(v)), sd=float(np.nanstd(v)))

# overlaps across songs (Spearman, pairwise complete)
def rho(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); m = np.isfinite(a) & np.isfinite(b)
    return round(float(stats.spearmanr(a[m], b[m])[0]), 3), int(m.sum())
cols = ["ch_rep", "V", "ln_chg", "ln_bars", "H4m", "g", "F", "B", "lnP", "CH", "A", "ln_tempo"]
out["overlaps"] = {k: rho(v, [s[k] for s in S]) for k in cols}
out["overlaps"]["hot"] = rho(v, [s["hot"] if s["hot"] is not None else np.nan for s in S])
out["overlaps"]["bb"] = rho(v, [float(s["bb"]) for s in S])
out["overlaps"]["year_known"] = rho(v, [float(s["year"] > 0) for s in S])
out["overlaps"]["year"] = rho(v, [s["year"] if s["year"] else np.nan for s in S])
out["overlaps"]["n_tracks"] = rho(v, [s["n_tracks"] for s in S])

# split-half: first and second half of the first file's bars and chord tokens (the chair's method), across songs
notes = {n["tid"]: n for n in json.load(open(os.path.join(C.DL, "lakh", "notes.json")))}
Z = np.load(os.path.join(C.DL, "lakh", "chroma.npz")); MI = json.load(open(os.path.join(C.DL, "lpd", "midi_info_v2.json")))
def part(Xb, t, sd, tm):
    d = C.song_shape(Xb, t, sd, tm)
    return dict(cv_w=d["cv_w"], ch_rep=C.repetition(t) if len(t) >= 3 else np.nan, V=len(set(t)), ln_chg=math.log(max(len(t), 1)),
                ln_bars=math.log(max(len(Xb), 1)))
A, B = [], []
for s in S:
    tid = s["tids"][0]; Xb = Z[tid].astype(float); t = notes[tid]["toks"]; tm = MI.get(notes[tid]["md5"], {}).get("tempo")
    sd = int(hashlib.md5(tid.encode()).hexdigest()[:8], 16); h = len(Xb) // 2; ht = len(t) // 2
    A.append(part(Xb[:h], t[:ht], sd, tm)); B.append(part(Xb[h:], t[ht:], sd, tm))
a = np.array([d["cv_w"] for d in A]); b = np.array([d["cv_w"] for d in B])
out["split_half"] = rho(a, b)
def resid(P):
    y = np.array([d["cv_w"] for d in P]); W = np.column_stack([[d[k] for d in P] for k in ("ch_rep", "V", "ln_chg", "ln_bars")] + [np.ones(len(P))])
    m = np.isfinite(y) & np.isfinite(W).all(1); r = np.full(len(y), np.nan)
    r[m] = y[m] - W[m] @ np.linalg.lstsq(W[m], y[m], rcond=None)[0]; return r
out["resid_split_half"] = rho(resid(A), resid(B))

# fake-outcome power on these rows and columns (no real outcome)
out["power"] = {}
for base in (0.40, 0.25):
    for beta in (1.5, 3.1, 0.0):
        for alpha in (T.ALPHA, 0.05):
            r = T.fake_power(S, beta, alpha, base=base, draws=300)
            out["power"][f"base{base}_beta{beta}_alpha{alpha:.5f}"] = r
            print(base, beta, alpha, r, flush=True)
se = out["power"][f"base0.4_beta1.5_alpha{T.ALPHA:.5f}"]["se"]
out["kill_fires"] = dict(se=se, if_true_1_5=float(stats.norm.cdf((0 - 1.5) / se)), if_zero=0.5)
json.dump(out, open(sys.argv[1], "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
