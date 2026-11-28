"""Run 13 shared code: Hooktheory song values of features13, the guarded outcome join, the within-artist model (run 11/12's)."""
import os, sys, json, hashlib, subprocess, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "run12", "experiments")))
import common12 as C12
C5 = C12.C5; C11 = C12.C11
FEATS = "/home/claude/dl/run13/hook_feats.json"

def pushed_clean(p): return C12._pushed_clean(p)

def guard(paths):
    for p in paths:
        if not pushed_clean(p): raise SystemExit(f"REFUSED: {p} not committed, unmodified and pushed: outcome NOT joined")

def song_table():
    """rows (run 04's within-artist songs with a 4/4 clip) with song-mean features, clip-1/clip-2 pairs, ln_notes, ch_rep, REP."""
    H = json.load(open(FEATS)); R = C11.rows(verbose=False); cache = json.load(open(C12.RUN11_CACHE))
    byv = collections.defaultdict(list)
    for k, v in H.items(): byv[v["vid"]].append(v)
    names = sorted(next(iter(H.values()))["f"])
    out = []
    for r in R:
        cs = byv.get(r["vid"])
        if not cs: continue
        w = np.array([c["n"] for c in cs], float); row = dict(vid=r["vid"], artist=r["artist"], half=r["half"], r=r)
        for n in names:
            v = np.array([c["f"][n] for c in cs], float); ok = np.isfinite(v)
            row[n] = float(np.average(v[ok], weights=w[ok])) if ok.any() else np.nan
        row["_c12"] = (cs[0]["f"], cs[1]["f"]) if len(cs) >= 2 else None
        cc = cache.get(r["vid"], {}); row["ln_notes"] = cc.get("ln_notes"); row["REP"] = cc.get("REP"); row["ch_rep"] = r.get("ch_rep")
        out.append(row)
    return out, names

def within(R, x, ycol, extra=("ln_notes",)):
    """z(y) on z(x) with artist FE, run 04 controls + extras; CR1 by artist. Returns beta, se, p, n."""
    import numpy as np
    keep = [i for i, r in enumerate(R) if np.isfinite(x[i]) and np.isfinite(r[ycol]) and all(r[e] is not None and np.isfinite(r[e]) for e in extra)]
    Rk = [R[i] for i in keep]; xk = np.asarray(x, float)[keep]
    cnt = collections.Counter(r["artist"] for r in Rk); idx = [i for i, r in enumerate(Rk) if cnt[r["artist"]] >= 2]
    Rk = [Rk[i] for i in idx]; xk = xk[idx]
    names, Cm = C5.controls([r["r"] for r in Rk])
    X = np.column_stack([(xk - xk.mean()) / xk.std()] + [Cm] + [C5.zs([r[e] for r in Rk]) for e in extra])
    y = np.array([r[ycol] for r in Rk], float); y = (y - y.mean()) / y.std()
    m = C5.lpm(X, y, [r["artist"] for r in Rk])
    return dict(beta=float(m["b"][0]), se=float(m["se"][0]), p=float(m["p"][0]), n=int(m["N"]), artists=int(m["G"])), Rk, X

def cond_logit_sign(Rk, X, ycol):
    yb = (np.array([r[ycol] for r in Rk]) > 0).astype(float)
    try:
        pr, bse, pv, conv, ks, kg = C5.cond_logit(X, yb, [r["artist"] for r in Rk]); return dict(beta=float(pr[0]), se=float(bse[0]), converged=bool(conv))
    except Exception as e: return dict(error=str(e)[:200])

def load_y(R, folder_paths):
    guard(folder_paths)
    rows = [r["r"] for r in R]; info = C5.load_outcomes(rows, os.path.dirname(folder_paths[0]))
    for r in R: r["y"] = r["r"]["y_foreign"]
    return info
