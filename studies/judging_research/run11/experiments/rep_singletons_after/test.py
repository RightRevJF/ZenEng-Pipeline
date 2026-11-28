"""rep_singletons_after (lead; after seeing results). Usage: python3 test.py power | run"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, collections, hashlib
from scipy import stats
import common11 as C
C5 = C.C5

def rows():
    A = C5.load_rows(verbose=False)["allsongs"]; n = collections.Counter(r["artist"] for r in A)
    S = [r for r in A if n[r["artist"]] == 1]
    C.song_values(S, lambda mel, a: C.baseline(mel), C.BASE)
    S = [r for r in S if np.isfinite(r["pc_entropy"]) and all(np.isfinite(r[k]) for k in ("n_pitch", "range", "ln_notes", "mel_ic_mean"))]
    for r in S: r["half"] = int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
    return S

def ols(S, x, y, extra=()):
    S = [r for r in S if np.isfinite(r[y])]
    _, X = C5.controls(S); X = np.hstack([np.ones((len(S), 1)), X] + [C._z([r[e] for r in S])[:, None] for e in extra])
    q, rr = np.linalg.qr(X); X = X[:, np.abs(np.diag(rr)) > 1e-8]; Q, _ = np.linalg.qr(X)
    xv = C._z([r[x] for r in S]); yv = C._z([r[y] for r in S])
    rx = xv - Q @ (Q.T @ xv); ry = yv - Q @ (Q.T @ yv)
    b = float(rx @ ry / (rx @ rx)); e = ry - b * rx; n, k = len(S), X.shape[1] + 1
    se = math.sqrt(n / (n - k) * float((rx ** 2 * e ** 2).sum())) / float(rx @ rx)
    return dict(beta=b, se=se, p=float(2 * stats.norm.sf(abs(b / se))), lo=b - 1.96 * se, hi=b + 1.96 * se, n=n), rx

if __name__ == "__main__":
    S = rows()
    if sys.argv[1] == "power":
        rng = np.random.default_rng(11); hit = 0; ses = []
        for r in S: r["_y"] = 0.0
        x = C._z([r["pc_entropy"] for r in S])
        for _ in range(300):
            y = -0.03 * x + rng.normal(0, math.sqrt(1 - 0.0009), len(x))
            for r, v in zip(S, y): r["_y"] = float(v)
            m, _ = ols(S, "pc_entropy", "_y"); ses.append(m["se"]); hit += (m["p"] < .05 and m["beta"] < 0)
        out = dict(power=hit / 300, median_fake_se=float(np.median(ses)), n=len(S), draws=300, seed=11, alpha=0.05)
        json.dump(out, open(os.path.join(HERE, "power.json"), "w"), indent=1); print(out)
    else:
        pw = json.load(open(os.path.join(HERE, "power.json"))); print("power (before the join):", pw)
        info = C.load_outcomes(S, HERE)
        main, _ = ols(S, "pc_entropy", "y_foreign")
        hv = [ols([r for r in S if r["half"] == h], "pc_entropy", "y_foreign")[0] for h in (0, 1)]
        import statsmodels.api as sm
        T = [r for r in S if np.isfinite(r["y_foreign"])]; _, X = C5.controls(T)
        X = np.hstack([C._z([r["pc_entropy"] for r in T])[:, None], np.ones((len(T), 1)), X]); X = X[:, X.std(0) > 0] if False else X
        try:
            lg = sm.Logit(np.array([r["y_foreign"] > 0 for r in T], float), X).fit(disp=0, method="bfgs", maxiter=500)
            sec = dict(beta=float(lg.params[0]), se=float(lg.bse[0]), p=float(lg.pvalues[0]))
        except Exception as ex: sec = dict(beta=float("nan"), error=str(ex))
        held = ols(S, "pc_entropy", "y_foreign", ("n_pitch", "range", "ln_notes", "mel_ic_mean"))[0]
        ok = main["p"] < .05 and main["beta"] < 0 and all(h["beta"] < 0 for h in hv) and sec.get("beta", 1) < 0
        v = "lead passed" if ok else ("killed" if not (main["lo"] <= -0.03 <= main["hi"]) else "unsettled")
        res = dict(main=main, halves=hv, second=sec, held_n_pitch_range_ln_notes_mel_ic=held, verdict=v, power=pw, outcome_info=info,
                   share_taken_up=float(np.mean([r["y_foreign"] > 0 for r in T])), after_seeing_results=True, counted=False)
        json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float); print(json.dumps(res, default=float)[:900])
