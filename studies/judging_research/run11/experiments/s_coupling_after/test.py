"""s_coupling_after: Jason's S = 1 + g/pi with g read as a COUPLING between the song's two outer voices (run 11, after seeing results;
Jason's request of 28 Nov 2026: one more, novel attempt before the formula is dropped). Whole songs from the Lakh Pianoroll Dataset.

Usage:
  python3 test.py measure   -> /home/claude/dl/run11/s_coupling.json (notes only; no outcome is read)
  python3 test.py gates     -> gates.json (stability between two MIDI files of one song, overlap with run 07's measures)
  python3 test.py power     -> power.json (fake outcomes on the real design)
  python3 test.py run       -> result.json (refuses unless PREDICTION.md, this file and common11.py are pushed)

Series (LPD-5 cleansed: 4/4, 24 steps per beat; tracks 0 drums, 1 piano, 2 guitar, 3 bass, 4 strings):
  melody line x: at each eighth note (every 12th step), the highest sounding pitch over tracks 1, 2, 4 (the "skyline");
  bass line y:   the lowest sounding pitch of track 3.
  A step with no note in a line holds that line's last pitch; the series runs from the first step where both lines have sounded to
  the last step where either sounds. A file needs at least 128 eighths (32 bars) and two non-constant lines.
g (G_COUP): rho_DCCA (Zebende 2011) between x and y, the mean over box sizes n = 8, 16, 32 eighths (one, two and four bars):
  profiles X = cumsum(x - mean), Y likewise; overlapping boxes of n + 1 points (step n // 4 between box starts, to bound compute);
  each box detrended by a least-squares line; rho(n) = F2xy / sqrt(F2xx F2yy). S_C = 1 + G_COUP / pi.
Readings: G_ABS = |G_COUP|; S_MEL = the DFA-1 exponent of x (box sizes 8 to 128 eighths, log-spaced, least-squares slope);
  the formula's own claim, checked notes-only: is pi (S_MEL - 1) related to G_COUP across songs (Spearman), and how near.
Song value = mean over the song's MIDI files with a value. Songs: run 07's 5,901 within-artist Lakh songs
(studies/judging_research/data/lakh_songs_discogs_run07.json; SEEN: joined in run 07 to y_foreign and eight chord measures, never to
this measure). Credit: Lakh MIDI Dataset (Raffel 2016) / LPD (Dong et al. 2018), CC BY 4.0; Discogs-VI (Araz, Serra & Bogdanov 2024),
CC BY-SA 4.0.
"""
import os, sys, json, math, hashlib, subprocess
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE)
sys.path.insert(0, EXP)
LPD = os.environ.get("LPD_DIR", "/home/claude/dl/lpd/lpd_5/lpd_5_cleansed")
CACHE = "/home/claude/dl/run11/s_coupling.json"
TABLE = os.path.normpath(os.path.join(EXP, "..", "..", "data", "lakh_songs_discogs_run07.json"))
NS = (8, 16, 32)
OUTCOME_KEYS = ("y", "y_foreign", "clique", "n_foreign_sets")


def lines(path):
    z = np.load(path, allow_pickle=False); T = len(z["downbeat"])
    def track(k):
        shp = z[f"pianoroll_{k}_csc_shape"]
        if shp[0] == 0: return None
        ind, ptr = z[f"pianoroll_{k}_csc_indices"], z[f"pianoroll_{k}_csc_indptr"]
        hi = np.full(T, -1, np.int16); lo = np.full(T, 999, np.int16)
        for p in range(128):
            a, b = ptr[p], ptr[p + 1]
            if b > a:
                t = ind[a:b]; hi[t] = np.maximum(hi[t], p); lo[t] = np.minimum(lo[t], p)
        return hi, lo
    tops = [track(k) for k in (1, 2, 4)]; bass = track(3)
    if bass is None or all(t is None for t in tops): return None, None
    top = np.max(np.vstack([t[0] for t in tops if t is not None]), 0)
    bot = bass[1].astype(float); bot[bot == 999] = np.nan
    topf = top.astype(float); topf[top < 0] = np.nan
    s = np.arange(0, T, 12); x, y = topf[s], bot[s]
    ok = np.isfinite(x) | np.isfinite(y)
    if not ok.any(): return None, None
    first = max(np.argmax(np.isfinite(x)), np.argmax(np.isfinite(y))) if np.isfinite(x).any() and np.isfinite(y).any() else None
    if first is None: return None, None
    last = len(s) - np.argmax(ok[::-1])
    x, y = x[first:last], y[first:last]
    for v in (x, y):
        for i in range(1, len(v)):
            if not np.isfinite(v[i]): v[i] = v[i - 1]
    return x, y


def rho_dcca(x, y, n):
    X = np.cumsum(x - x.mean()); Y = np.cumsum(y - y.mean()); N = len(X)
    if N < 4 * n: return None
    t = np.arange(n + 1); A = np.vstack([t, np.ones_like(t)]).T; P = np.eye(n + 1) - A @ np.linalg.pinv(A)
    starts = np.arange(0, N - n, max(n // 4, 1))
    BX = np.stack([X[i:i + n + 1] for i in starts]) @ P.T; BY = np.stack([Y[i:i + n + 1] for i in starts]) @ P.T
    fxy = (BX * BY).mean(); fxx = (BX * BX).mean(); fyy = (BY * BY).mean()
    if fxx <= 0 or fyy <= 0: return None
    return float(fxy / math.sqrt(fxx * fyy))


def dfa(x):
    X = np.cumsum(x - x.mean()); N = len(X); ns = [n for n in (8, 11, 16, 23, 32, 45, 64, 91, 128) if 4 * n <= N]
    if len(ns) < 4: return None
    F = []
    for n in ns:
        t = np.arange(n); A = np.vstack([t, np.ones_like(t)]).T; P = np.eye(n) - A @ np.linalg.pinv(A)
        B = np.stack([X[i:i + n] for i in range(0, N - n + 1, n)]) @ P.T
        F.append(math.sqrt((B * B).mean()))
    F = np.array(F)
    if (F <= 0).any(): return None
    return float(np.polyfit(np.log(ns), np.log(F), 1)[0])


def file_measure(path):
    try:
        x, y = lines(path)
    except Exception:
        return None
    if x is None or len(x) < 128 or np.std(x) == 0 or np.std(y) == 0: return None
    r = [rho_dcca(x, y, n) for n in NS]
    if any(v is None for v in r): return None
    g = float(np.mean(r)); s = dfa(x)
    return dict(G_COUP=g, S_C=1 + g / math.pi, G_ABS=abs(g), G_1BAR=r[0], G_2BAR=r[1], G_4BAR=r[2], S_MEL=s, n8=len(x))


def _path(tid, md5): return os.path.join(LPD, tid[2], tid[3], tid[4], tid, md5 + ".npz")


def _job(a): return a[0], file_measure(_path(a[1], a[2]))


def notes_side():
    """songs from the committed table, with ONLY the notes-side fields (outcome keys are not kept)."""
    T = json.load(open(TABLE))["songs"]
    return [{k: v for k, v in s.items() if k not in OUTCOME_KEYS} for s in T]


def do_measure():
    S = notes_side(); jobs = []
    for s in S:
        for tid, md5 in zip(s["tids"], s["md5s"]): jobs.append((s["key"], tid, md5))
    with Pool(2) as p: res = p.map(_job, jobs, chunksize=16)
    out = {}
    for k, m in res:
        if m is not None: out.setdefault(k, []).append(m)
    os.makedirs(os.path.dirname(CACHE), exist_ok=True); json.dump(out, open(CACHE, "w"))
    print("files", len(jobs), "with a value", sum(len(v) for v in out.values()), "songs with a value", len(out), "of", len(S))


def song_rows():
    M = json.load(open(CACHE)); R = []
    for s in notes_side():
        ms = M.get(s["key"])
        if not ms: continue
        r = dict(s)
        for k in ("G_COUP", "S_C", "G_ABS", "G_1BAR", "G_2BAR", "G_4BAR", "S_MEL"):
            v = [m[k] for m in ms if m.get(k) is not None]; r[k] = float(np.mean(v)) if v else float("nan")
        r["CRIT"] = -abs(r["S_MEL"] - 1) if np.isfinite(r["S_MEL"]) else float("nan")   # nearness of the melody's exponent to 1
        r["pair"] = (ms[0]["G_COUP"], ms[1]["G_COUP"]) if len(ms) >= 2 else None
        r["half"] = int(hashlib.md5(s["key"].split("|")[0].encode()).hexdigest(), 16) % 2
        R.append(r)
    from collections import Counter
    c = Counter(r["key"].split("|")[0] for r in R)
    for r in R: r["artist"] = r["key"].split("|")[0]
    return [r for r in R if c[r["artist"]] >= 2 and np.isfinite(r["G_COUP"])]
# note: the within-artist filter counts songs WITH a value (artists left with one valued song drop out)


def do_gates():
    from scipy import stats
    R = song_rows(); pr = [r["pair"] for r in R if r["pair"]]
    st = stats.spearmanr([p[0] for p in pr], [p[1] for p in pr]).correlation if len(pr) > 10 else float("nan")
    ov = {}
    for c in ("ch_rep", "V", "ln_chg", "ln_bars", "CH", "A", "H4m", "cv_w", "g", "lnP", "F", "B", "ln_tempo", "S_MEL"):
        v = np.array([r.get(c, np.nan) for r in R], float); x = np.array([r["G_COUP"] for r in R]); ok = np.isfinite(v)
        if ok.sum() > 50: ov[c] = float(stats.spearmanr(x[ok], v[ok]).correlation)
    sm = np.array([r["S_MEL"] for r in R], float); gc = np.array([r["G_COUP"] for r in R]); ok = np.isfinite(sm)
    formula = dict(spearman_pi_Smel_minus1_vs_g=float(stats.spearmanr(math.pi * (sm[ok] - 1), gc[ok]).correlation),
                   median_S_MEL=float(np.median(sm[ok])), median_pi_Smel_minus1=float(np.median(math.pi * (sm[ok] - 1))),
                   median_G_COUP=float(np.median(gc)), mean_G_COUP=float(gc.mean()), share_G_negative=float((gc < 0).mean()))
    out = dict(songs=len(R), artists=len({r["artist"] for r in R}), stability_two_files=float(st), pairs=len(pr),
               overlap_spearman=ov, gate_stability_min=0.20, gate_overlap_max=0.70,
               passed=bool(st >= 0.20 and max(abs(v) for v in ov.values()) <= 0.70), formula_notes_side=formula)
    json.dump(out, open(os.path.join(HERE, "gates.json"), "w"), indent=1); print(json.dumps(out, indent=1))


# ---------------------------------------------------------------- model: z(y_foreign) on z(x), artist FE, run 07's BASE + year bins
def _z(v): v = np.asarray(v, float); return (v - v.mean()) / v.std()

def controls(R, extra=()):
    b = [("u" if not r["year"] else str(min(max(r["year"], 1950), 2010) // 5 * 5)) for r in R]; lv = sorted(set(b))
    Y = np.column_stack([[float(x == l) for x in b] for l in lv[1:]])
    return np.column_stack([_z([r[c] for r in R]) for c in ("ln_chg", "V", "ln_bars")] + [_z([r[e] for r in R]) for e in extra] + [Y])

def fit(R, x, ycol="y_foreign", extra=()):
    import common11 as C
    R = [r for r in R if r.get(ycol) is not None and np.isfinite(r[ycol]) and all(np.isfinite(r[e]) for e in extra)]
    g = [r["artist"] for r in R]; Cw, G = C._demean(controls(R, extra), g)
    keep = np.abs(Cw).sum(0) > 1e-10; q, rr = np.linalg.qr(Cw[:, keep]); Q = q[:, np.abs(np.diag(rr)) > 1e-8]
    def res(v): vw, _ = C._demean(v, g); vw = vw.ravel(); return vw - Q @ (Q.T @ vw)
    b, se, p = C.fwl_fit(res(_z([r[x] for r in R])), res(_z([r[ycol] for r in R])), g, Q.shape[1] + G)
    return dict(beta=b, se=se, p=p, lo=b - 1.96 * se, hi=b + 1.96 * se, n=len(R), artists=G), (R, g, Q, res)

def do_power():
    import common11 as C
    spec = json.load(open(os.path.join(HERE, "spec.json"))); R = song_rows()
    for r in R: r["_y"] = 0.0
    _, (R2, g, Q, res) = fit(R, spec["measure"], "_y")
    x = _z([r[spec["measure"]] for r in R2]); rx = res(x); rng = np.random.default_rng(11); hit = 0; ses = []; kz = 0
    for _ in range(300):
        y = _z(spec["pred"] * x + rng.normal(0, math.sqrt(1 - spec["pred"] ** 2), len(x)))
        b, se, p = C.fwl_fit(rx, res(y), g, Q.shape[1] + len(set(g))); ses.append(se)
        hit += (p < spec["alpha"] and np.sign(b) == np.sign(spec["pred"]))
        y0 = _z(rng.normal(0, 1, len(x))); b0, se0, _ = C.fwl_fit(rx, res(y0), g, Q.shape[1] + len(set(g)))
        kz += not (b0 - 1.96 * se0 <= spec["pred"] <= b0 + 1.96 * se0)
    out = dict(power=hit / 300, kill_if_zero=kz / 300, median_fake_se=float(np.median(ses)), n=len(R2), artists=len(set(g)),
               draws=300, seed=11, alpha=spec["alpha"], note="iid fake noise (no artist share): conservative, as R11-4 says")
    json.dump(out, open(os.path.join(HERE, "power.json"), "w"), indent=1); print(out)

def do_run():
    import common11 as C
    for p in (os.path.join(HERE, "PREDICTION.md"), os.path.join(HERE, "test.py"), os.path.join(EXP, "common11.py"), os.path.join(HERE, "spec.json")):
        if not C._pushed_clean(p): raise SystemExit(f"REFUSED: {p} is not committed, unmodified and pushed: outcome NOT joined")
    spec = json.load(open(os.path.join(HERE, "spec.json"))); pw = json.load(open(os.path.join(HERE, "power.json")))
    print("power (before the join):", pw, flush=True)
    R = song_rows(); O = {s["key"]: s for s in json.load(open(TABLE))["songs"]}
    for r in R:
        o = O[r["key"]]; r["y_foreign"] = np.nan if o["y_foreign"] is None else float(o["y_foreign"]); r["y"] = float(o["y"])
    x, pred, alpha = spec["measure"], spec["pred"], spec["alpha"]
    main, _ = fit(R, x)
    hv = [fit([r for r in R if r["half"] == h], x)[0] for h in (0, 1)]
    from statsmodels.discrete.conditional_models import ConditionalLogit
    T = [r for r in R if np.isfinite(r["y_foreign"])]
    try:
        X = np.column_stack([_z([r[x] for r in T]), controls(T)]); X = X[:, X.std(0) > 1e-12]
        cl = ConditionalLogit(np.array([r["y_foreign"] > 0 for r in T], float), X, groups=[r["artist"] for r in T]).fit(disp=0, method="bfgs", maxiter=2000)
        sec = dict(beta=float(cl.params[0]), se=float(cl.bse[0]), p=float(cl.pvalues[0]))
    except Exception as ex: sec = dict(beta=float("nan"), error=str(ex))
    killed = not (main["lo"] <= pred <= main["hi"])
    ok = main["p"] < alpha and np.sign(main["beta"]) == np.sign(pred) and all(np.sign(h["beta"]) == np.sign(pred) for h in hv) and np.sign(sec.get("beta", 0)) == np.sign(pred)
    verdict = "lead passed" if ok else ("killed" if killed else "unsettled")
    rd = {}
    for name, meas, ex, sign in spec["readings"]:
        try: rd[name] = dict(fit(R, meas, extra=tuple(ex))[0], pred_sign=sign)
        except Exception as e: rd[name] = dict(error=str(e))
    res = dict(spec=spec, power=pw, main=main, halves=hv, second=sec, verdict=verdict, readings=rd,
               share_taken_up=float(np.mean([r["y_foreign"] > 0 for r in T])), after_seeing_results=True, counted_in_K=False)
    json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float)
    print(json.dumps(dict(main=main, verdict=verdict, halves=[h["beta"] for h in hv], second=sec.get("beta")), default=float))

if __name__ == "__main__":
    {"measure": do_measure, "gates": do_gates, "power": do_power, "run": do_run}[sys.argv[1]]()
