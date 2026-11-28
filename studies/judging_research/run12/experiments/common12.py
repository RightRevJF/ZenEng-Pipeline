"""Run 12 shared code (frozen with the predictions before any outcome is joined).

Two data sets, both SEEN (their outcomes were joined to other measures before; every measure tested here is new to them):
  Hooktheory : run 04's 9,588 within-artist songs (common11 / run 05's C5). Measures: run 11's frozen cache (REP = pc_entropy and
               the 13 baselines; /home/claude/dl/run11/measures_run11.json), the 17 pack measures (ch_rep, ...) and this pass's clip
               cache (build_hook12.py -> /home/claude/dl/run12/hook_measures12.json: G_E5, G_REST, PIC, ...).
  Lakh       : run 07's 5,901 within-artist songs (notes side: /home/claude/dl/run12/lakh_notes_side.json; measures:
               build_lakh12.py -> /home/claude/dl/run12/lakh_measures12.json; near-duplicate files counted once).
Outcomes (ONLY through the guarded loaders below; they refuse unless the folder's PREDICTION.md and spec.json, this file and
harness12.py are committed, unmodified AND pushed to origin/judging-research; run 11's guard, copied):
  load_hook(R, folder)  : C5.load_outcomes (y, y_foreign, lcov, first_year, versions) + /home/claude/dl/run12/fitness.json
                          (FIT, N, E, t0, clique; frozen fitness.py, commit b0c7824) + the window counts N_E (ages 0-3) and N_L (ages 8+)
                          recomputed from the versions by fitness.py's cover rule, with their exposures from fit.json's g and h.
  load_lakh(R, folder)  : y_foreign of studies/judging_research/data/lakh_songs_discogs_run07.json (run 07's rule).
Models: OLS on z-scores with ARTIST FIXED EFFECTS (Frisch-Waugh), CR1 SEs clustered by artist (common11's adjustment);
  conditional logit (C5.cond_logit) for the SIGN on binary outcomes; halves = md5(artist) mod 2; FE Poisson (conditional multinomial
  likelihood, cluster sandwich) for the window counts. Fake-outcome power WITH the within-artist variance share
  (/home/claude/dl/run12/outcome_side_shares.json; run 11's lesson).
Credit: Hooktheory via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0; Lakh MIDI (Raffel 2016) / LPD (Dong et al.
  2018), CC BY 4.0; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
"""
import os, sys, json, math, re, hashlib, subprocess, importlib.util
import numpy as np
from scipy import stats
from scipy.special import digamma

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "run11", "experiments")))
import common11 as C11
C5 = C11.C5
REPO = C11.REPO
SEED = 12
RUN11_CACHE = "/home/claude/dl/run11/measures_run11.json"
HOOK12 = os.environ.get("HOOK12_CACHE", "/home/claude/dl/run12/hook_measures12.json")
LAKH12 = os.environ.get("LAKH12_CACHE", "/home/claude/dl/run12/lakh_measures12.json")
LAKH_SIDE = "/home/claude/dl/run12/lakh_notes_side.json"
SHARES = "/home/claude/dl/run12/outcome_side_shares.json"
FITNESS_JSON = "/home/claude/dl/run12/fitness.json"          # OUTCOME: read only inside load_hook (guarded)
LAKH_TABLE = os.path.normpath(os.path.join(HERE, "..", "..", "data", "lakh_songs_discogs_run07.json"))   # OUTCOME: load_lakh only
FIT_SUMMARY = os.path.join(HERE, "fitness", "fit.json")    # aggregates only (r, A, g, h); no per-song value
_fs = importlib.util.spec_from_file_location("fitness12", os.path.join(HERE, "fitness", "fitness.py"))
F = importlib.util.module_from_spec(_fs); _fs.loader.exec_module(F)   # age_bin, era_bin, LAST (no data read at import)
LAKH_BASE = ["ln_chg", "V", "ln_bars"]                       # run 07's controls (plus 5-year year bins)
LAKH_SKEPTIC = ["LNEV", "NPB", "ACT", "NFILES"]              # Skeptic round 2: every Lakh test holds these
LAKH_EXISTING = ["ch_rep", "V", "ln_chg", "ln_bars", "CH", "A", "H4m", "cv_w", "g", "lnP", "F", "B", "ln_tempo"]
EARLY = (0, 3); LATE_FROM = 8                                 # window ages (WINDOWS)


def shares():
    return json.load(open(SHARES))


_FS = None
def fit_summary():
    global _FS
    if _FS is None:
        d = json.load(open(FIT_SUMMARY))["pa"]; _FS = dict(r=d["r"], A=d["A"], g=d["g"], h=d["h"])
    return _FS


def exposure(t0, a0, a1, P=None):
    """sum over calendar years t in [t0+a0, min(t0+a1, LAST)] of A g(age) h(era): the frozen model's expected covers at fitness 1
    (A -> infinity, so k(t-) + A = A). a1 = None means to LAST."""
    P = P or fit_summary(); hi = F.LAST if a1 is None else min(t0 + a1, F.LAST); s = 0.0
    for t in range(t0 + a0, hi + 1): s += P["A"] * P["g"][F.age_bin(t - t0)] * P["h"][F.era_bin(t)]
    return s


# ---------------------------------------------------------------- Hooktheory rows (notes side)
def hook_rows():
    """run 04's rows with run 11's cache, the pack measures and this pass's clip cache (keyed by video id). No outcome."""
    M11 = json.load(open(RUN11_CACHE)); M12 = json.load(open(HOOK12)); R = []
    for r in C11.rows():
        q = dict(vid=r["vid"], artist=r["artist"], half=r["half"], n_ch=r["n_ch"], beats=r["beats"], nclips=r["nclips"],
                 u=r["u"], tokens=r["tokens"], rep_title=r["rep_title"], clips=r["clips"])
        for f in C11.PACK: q[f] = r.get(f)
        for M in (M11, M12):
            for k, v in (M.get(r["vid"]) or {}).items():
                if k.endswith("_c12"): q[k] = v
                else: q[k] = np.nan if v is None else v
        R.append(q)
    return R


def hook_design(cols):
    return [r for r in hook_rows() if all(r.get(c) is not None and np.isfinite(r[c]) for c in cols)]


def hook_controls(R, extra=(), year=None):
    """run 04's control block + z(extra) + year dummies (year='exact': one per first year t0; 'five': 5-year bins of t0)."""
    _, X = C5.controls(R); cols = [X] + [_z([r[e] for r in R])[:, None] for e in extra]
    if year:
        b = [r["t0"] if year == "exact" else r["t0"] // 5 * 5 for r in R]; lv = sorted(set(b))
        if len(lv) > 1: cols.append(np.column_stack([[float(x == l) for x in b] for l in lv[1:]]))
    return np.hstack(cols)


# ---------------------------------------------------------------- Lakh rows (notes side)
def lakh_rows():
    """one row per Lakh song with a value: notes-side fields, song means over kept (non-duplicate) files, 'pairs' (file 1, file 2
    of the kept files) for the two-file gate, NFILES = number of MIDI files listed, artist = key prefix, half = md5(artist) mod 2."""
    side = {s["key"]: s for s in json.load(open(LAKH_SIDE))}; M = json.load(open(LAKH12))["songs"]; R = []
    for key, s in side.items():
        m = M.get(key)
        if not m: continue
        r = {k: v for k, v in s.items()}; fs = m["files"]
        for k in fs[0].keys():
            if k in ("PROF", "j"): continue
            v = [f[k] for f in fs if f.get(k) is not None]; r[k] = float(np.mean(v)) if v else np.nan
        r["pairs"] = (fs[0], fs[1]) if len(fs) >= 2 else None
        r["NFILES"] = float(len(s["md5s"])); r["n_dup"] = m["n_dup"]
        r["artist"] = key.split("|")[0]; r["half"] = int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
        R.append(r)
    return R


def within_artist(R):
    from collections import Counter
    c = Counter(r["artist"] for r in R); return [r for r in R if c[r["artist"]] >= 2]


def lakh_design(cols, base=None):
    base = lakh_rows() if base is None else base
    return within_artist([r for r in base if all(r.get(c) is not None and np.isfinite(r[c]) for c in cols)])


def lakh_controls(R, extra=(), skeptic=True):
    b = [str(min(max(r["year"], 1950), 2010) // 5 * 5) if r.get("year") else "u" for r in R]; lv = sorted(set(b))
    cols = [_z([r[c] for r in R]) for c in LAKH_BASE + (LAKH_SKEPTIC if skeptic else [])] + [_z([r[e] for r in R]) for e in extra]
    X = np.column_stack(cols)
    if len(lv) > 1: X = np.column_stack([X] + [np.array([float(x == l) for x in b]) for l in lv[1:]])
    return X


# ---------------------------------------------------------------- the guard and the outcomes
def _pushed_clean(path):
    return C11._pushed_clean(path)


def guard(folder):
    for p in (os.path.join(folder, "PREDICTION.md"), os.path.join(folder, "spec.json"), os.path.join(HERE, "common12.py"),
              os.path.join(HERE, "harness12.py")):
        if not _pushed_clean(p):
            raise SystemExit(f"REFUSED: {p} is not committed, unmodified and pushed to origin/judging-research: outcome NOT joined")


_nrm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))


def window_counts(versions, artist, t0):
    """fitness.py's cover rule: a version is a cover iff its performer set is non-empty and shares no normalised name with the
    original artist's own sets; versions with no year or a year after LAST are dropped; a year before t0 counts at t0."""
    a = _nrm(artist); own = [s for s, y, _ in versions if any(_nrm(n) == a for n in s)]
    if not own: return None
    O = {_nrm(n) for s in own for n in s}; ages = []
    for s, y, _ in versions:
        if len(s) == 0 or any(_nrm(n) in O for n in s): continue
        if y is None or y > F.LAST: continue
        ages.append(max(int(y), t0) - t0)
    ages = np.array(ages, int)
    return dict(N_all=int(len(ages)), N_E=int(((ages >= EARLY[0]) & (ages <= EARLY[1])).sum()), N_L=int((ages >= LATE_FROM).sum()))


def load_hook(R, folder):
    guard(folder)
    info = C5.load_outcomes(R, folder)
    FJ = json.load(open(FITNESS_JSON)); VC = json.loads(C5.GIT("discogs_versions_matched.json"))["cliques"]; P = fit_summary()
    nfit = mism = 0
    for r in R:
        r.update(FIT=np.nan, N=np.nan, t0=None, N_E=np.nan, N_L=np.nan, X_E=np.nan, X_L=np.nan)
        f = FJ.get(r["vid"])
        if f is None: continue
        nfit += 1; r.update(FIT=float(f["FIT"]), N=float(f["N"]), t0=int(f["t0"]), lN=float(np.log1p(f["N"])))
        v = VC.get(f["clique"])
        if v is None: continue
        w = window_counts(v["versions"], r["artist"], r["t0"])
        if w is None: continue
        mism += int(w["N_all"] != int(f["N"]))
        r.update(N_E=float(w["N_E"]), N_L=float(w["N_L"]), X_E=exposure(r["t0"], EARLY[0], EARLY[1], P), X_L=exposure(r["t0"], LATE_FROM, None, P))
    info.update(rows_with_FIT=nfit, window_N_mismatch_vs_fitness_json=mism, fitness_sha256=hashlib.sha256(open(FITNESS_JSON, "rb").read()).hexdigest())
    return info


def load_lakh(R, folder):
    guard(folder)
    O = {s["key"]: s for s in json.load(open(LAKH_TABLE))["songs"]}
    for r in R:
        o = O.get(r["key"]); r["y_foreign"] = np.nan if (o is None or o.get("y_foreign") is None) else float(o["y_foreign"])
    return dict(rows=len(R), with_y_foreign=int(sum(np.isfinite(r["y_foreign"]) for r in R)),
                md5=hashlib.md5(open(LAKH_TABLE, "rb").read()).hexdigest())


# ---------------------------------------------------------------- OLS with artist FE (several x columns), CR1 by artist
def _z(v):
    v = np.asarray(v, float); s = v.std(); return (v - v.mean()) / s if s > 0 else v * 0


class Proj:
    def __init__(self, g, Cmat):
        self.g = list(g); Cw, self.G = C11._demean(Cmat, self.g); keep = np.abs(Cw).sum(0) > 1e-10
        q, rr = np.linalg.qr(Cw[:, keep]); ok = np.abs(np.diag(rr)) > 1e-8; self.Q = q[:, ok]; self.k = int(ok.sum()) + self.G
    def resid(self, v):
        vw, _ = C11._demean(v, self.g); vw = vw.reshape(len(self.g), -1)
        out = vw - self.Q @ (self.Q.T @ vw); return out[:, 0] if out.shape[1] == 1 else out


def ols_resid(RX, ry, g, k):
    """RX: n x p residualised regressors, ry residualised y. Returns b (p), V (p x p) CR1 by g (common11's adjustment)."""
    RX = RX.reshape(len(ry), -1); n, p = RX.shape; XtXi = np.linalg.inv(RX.T @ RX); b = XtXi @ RX.T @ ry; e = ry - RX @ b
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); G = len(codes)
    S = np.zeros((G, p)); np.add.at(S, gg, RX * e[:, None])
    adj = (G / (G - 1)) * ((n - 1) / max(n - k - p, 1)); V = adj * XtXi @ (S.T @ S) @ XtXi
    return b, V


def fe_fit(R, xcols, ycol, ctrl, zy=True):
    """OLS of z(y) (or raw y if zy=False) on z(x_1..x_p) with artist FE and the control matrix ctrl(R). Returns a dict per x and the
    covariance. beta of the FIRST x is 'beta' (with se, p, lo, hi)."""
    R = [r for r in R if r.get(ycol) is not None and np.isfinite(r[ycol])]
    X = np.column_stack([_z([r[c] for r in R]) for c in xcols]); y = np.array([r[ycol] for r in R], float); y = _z(y) if zy else y
    P = Proj([r["artist"] for r in R], ctrl(R)); RX = P.resid(X).reshape(len(R), -1); ry = P.resid(y)
    b, V = ols_resid(RX, ry, P.g, P.k); se = np.sqrt(np.diag(V)); pv = 2 * stats.norm.sf(np.abs(b / se))
    out = dict(beta=float(b[0]), se=float(se[0]), p=float(pv[0]), lo=float(b[0] - 1.96 * se[0]), hi=float(b[0] + 1.96 * se[0]),
               n=len(R), artists=P.G, coefs={c: dict(beta=float(b[i]), se=float(se[i]), p=float(pv[i])) for i, c in enumerate(xcols)},
               cov=V.tolist())
    return out


def fe_fit_raw(R, xcols, ycol, ctrl):
    """as fe_fit but x on its RAW scale (Geometer's Wald test b_E5 = b_REST); y z-scored."""
    R = [r for r in R if r.get(ycol) is not None and np.isfinite(r[ycol])]
    X = np.column_stack([np.array([r[c] for r in R], float) for c in xcols]); y = _z([r[ycol] for r in R])
    P = Proj([r["artist"] for r in R], ctrl(R)); RX = P.resid(X).reshape(len(R), -1); ry = P.resid(y)
    b, V = ols_resid(RX, ry, P.g, P.k); return b, V, len(R)


def halves_fit(R, xcols, ycol, ctrl, zy=True):
    return [fe_fit([r for r in R if r["half"] == h], xcols, ycol, ctrl, zy) for h in (0, 1)]


def second_logit(R, xcols, ycol, ctrl):
    R = [r for r in R if r.get(ycol) is not None and np.isfinite(r[ycol])]
    X = np.hstack([np.column_stack([_z([r[c] for r in R]) for c in xcols]), ctrl(R)])
    keep = X.std(0) > 1e-12; keep[:len(xcols)] = True; X = X[:, keep]
    try:
        pa, bse, pv, conv, ns, ng = C5.cond_logit(X, np.array([r[ycol] > 0 for r in R], float), [r["artist"] for r in R])
        return dict(beta=float(pa[0]), se=float(bse[0]), p=float(pv[0]), converged=bool(conv), songs=ns, groups=ng)
    except Exception as ex:
        return dict(beta=float("nan"), se=float("nan"), p=float("nan"), error=str(ex))


def verdict(main, pred, alpha, counted, hv, sec=None, second_applies=True, kill="range"):
    """run 10-11's rules. kill='range': killed iff pred outside beta +- 1.96 SE (R07-3). kill='range_and_wrong_side' (V1, Jason's
    words): killed iff pred outside beta +- 1.96 SE AND beta is on the wrong side of 0 (sign(beta) != sign(pred) or beta == 0)."""
    sign_ok = np.sign(main["beta"]) == np.sign(pred)
    halves_ok = all(np.sign(h["beta"]) == np.sign(pred) for h in hv)
    second_ok = (not second_applies) or (sec is not None and np.isfinite(sec.get("beta", np.nan)) and np.sign(sec["beta"]) == np.sign(pred))
    outside = not (main["lo"] <= pred <= main["hi"])
    killed = outside if kill == "range" else (outside and not sign_ok)
    if not counted: v = "estimate"
    elif main["p"] < alpha and sign_ok and halves_ok and second_ok: v = "passed"
    elif killed: v = "killed"
    else: v = "unsettled"
    return dict(verdict=v, counted=bool(counted), sign_ok=bool(sign_ok), halves_ok=bool(halves_ok), second_ok=bool(second_ok),
                second_applies=bool(second_applies), prediction_outside_range=bool(outside), kill_rule=kill,
                would_be_killed=bool(killed))


# ---------------------------------------------------------------- FE Poisson (conditional multinomial likelihood), cluster sandwich
def pois_fe(y, X, off, g, iters=60):
    """Poisson with group (artist) fixed effects, by the conditional (multinomial) likelihood, which gives the same beta as the
    FE Poisson MLE. Groups with zero total drop out. Columns with no within-group variation (among kept rows) are dropped.
    Returns dict(b, V (cluster sandwich, G/(G-1)), cols kept, n, groups, scores per group (for joint covariances))."""
    y = np.asarray(y, float); X = np.asarray(X, float).reshape(len(y), -1); off = np.asarray(off, float)
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g])
    tot = np.bincount(gg, weights=y, minlength=len(codes)); keep = tot[gg] > 0
    y, X, off, gg = y[keep], X[keep], off[keep], gg[keep]
    u, gg = np.unique(gg, return_inverse=True); G = len(u)
    cnt = np.bincount(gg, minlength=G); Xm = np.zeros((G, X.shape[1])); np.add.at(Xm, gg, X); Xw = X - (Xm / cnt[:, None])[gg]
    q, rr = np.linalg.qr(Xw); okc = np.abs(np.diag(rr)) > 1e-8 * max(1.0, np.abs(np.diag(rr)).max()); okc[0] = True
    X = X[:, okc]; p = X.shape[1]; b = np.zeros(p); ng = np.bincount(gg, weights=y, minlength=G)
    def parts(b):
        eta = X @ b + off; mx = np.full(G, -np.inf); np.maximum.at(mx, gg, eta); w = np.exp(eta - mx[gg])
        sw = np.bincount(gg, weights=w, minlength=G); pi = w / sw[gg]
        ll = float((y * (eta - mx[gg])).sum() - (ng * np.log(sw)).sum())
        mxp = np.zeros((G, p)); np.add.at(mxp, gg, pi[:, None] * X)
        S = np.zeros((G, p)); np.add.at(S, gg, y[:, None] * X); S -= ng[:, None] * mxp
        # Hessian: -sum_g n_g [ sum_i pi x x' - m m' ]
        XX = np.einsum("i,ij,ik->jk", pi * ng[gg], X, X)
        MM = np.einsum("g,gj,gk->jk", ng, mxp, mxp); H = -(XX - MM)
        return ll, S, H
    ll = -np.inf
    for _ in range(iters):
        ll1, S, H = parts(b); step = np.linalg.solve(H, S.sum(0)); b_new = b - step
        t = 1.0
        while parts(b_new)[0] < ll1 - 1e-10 and t > 1e-4: t /= 2; b_new = b - t * step
        b = b_new
        if np.max(np.abs(t * step)) < 1e-9: break
    ll, S, H = parts(b); Hi = np.linalg.inv(H); V = (G / (G - 1)) * Hi @ (S.T @ S) @ Hi
    return dict(b=b, V=V, Hi=Hi, S=S, groups_kept=u, n=int(len(y)), G=G, cols=np.flatnonzero(okc).tolist(), ll=ll)


# ---------------------------------------------------------------- power by fake outcomes WITH the within-artist share
def fake_y(x, g, beta, w, rng):
    """y = beta z(x) + sqrt(1 - w) a_artist + sqrt(w - beta^2) e : total variance 1, within-artist share about w."""
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g])
    a = rng.normal(0, 1, len(codes))[gg]
    return beta * x + math.sqrt(max(1 - w, 0)) * a + math.sqrt(max(w - beta * beta, 1e-9)) * rng.normal(0, 1, len(x))


def power_ols(R, xcols, beta, alphas, ctrl, w, draws=300, seed=SEED):
    """fake y on the real rows and design; power at each alpha = share with p < alpha and the predicted sign (first x); kill rates."""
    rng = np.random.default_rng(seed); X = np.column_stack([_z([r[c] for r in R]) for c in xcols]); g = [r["artist"] for r in R]
    P = Proj(g, ctrl(R)); RX = P.resid(X).reshape(len(R), -1); hits = {a: 0 for a in alphas}; kt = kz = 0; ses = []
    for _ in range(draws):
        for which in ("true", "zero"):
            bb = beta if which == "true" else 0.0
            y = _z(fake_y(X[:, 0], g, bb, w, rng)); b, V = ols_resid(RX, P.resid(y), P.g, P.k); se = math.sqrt(V[0, 0])
            pv = 2 * stats.norm.sf(abs(b[0] / se)); outside = not (b[0] - 1.96 * se <= beta <= b[0] + 1.96 * se)
            if which == "true":
                ses.append(se); kt += outside
                for a in alphas: hits[a] += (pv < a and np.sign(b[0]) == np.sign(beta))
            else: kz += outside
    return dict(power={str(round(a, 6)): hits[a] / draws for a in alphas}, kill_if_true=kt / draws, kill_if_zero=kz / draws,
                median_fake_se=float(np.median(ses)), within_share_used=w, draws=draws, seed=seed, n=len(R), artists=P.G)


# ---------------------------------------------------------------- model-based fake outcomes for the FIT tests (no outcome read)
def calibrate_selection(g, mean, within, rng, grid=np.linspace(0.0, 3.0, 61)):
    """probit selection y* = tau a_artist + e > c, tuned so the share selected is `mean` and the within-artist share of the binary
    selection's variance (sum of within-artist squares / total squares, as outcome_side_shares.json) is `within`."""
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); best = None
    for tau in grid:
        ws = []
        for _ in range(3):
            s = tau * rng.normal(0, 1, len(codes))[gg] + rng.normal(0, 1, len(gg)); c = np.quantile(s, 1 - mean); y = (s > c).astype(float)
            ws.append(_within_share(y, gg))
        d = abs(np.mean(ws) - within)
        if best is None or d < best[0]: best = (d, tau, float(np.mean(ws)))
    return dict(tau=float(best[1]), within_achieved=best[2])


def _within_share(v, gg):
    v = np.asarray(v, float); cnt = np.bincount(gg); m = np.bincount(gg, weights=v) / np.maximum(cnt, 1)
    ok = cnt[gg] >= 2; tot = ((v[ok] - v[ok].mean()) ** 2).sum()
    return float(((v[ok] - m[gg][ok]) ** 2).sum() / tot) if tot > 0 else float("nan")


def sim_matched(R, rng, tau, mean, rho_a, era="artist", P=None):
    """one fake world on the real Hooktheory rows: which songs are matched (artist-clustered), a first year per song (artist era),
    fitness eta ~ Gamma(r, r) with artist correlation rho_a (Gaussian copula), exposures from fit.json. Returns the matched rows
    (copies) with t0, eta, Ezf (full exposure)."""
    P = P or fit_summary(); g = [r["artist"] for r in R]; codes = {a: i for i, a in enumerate(sorted(set(g)))}
    gg = np.array([codes[a] for a in g]); G = len(codes)
    s = tau * rng.normal(0, 1, G)[gg] + rng.normal(0, 1, len(R)); sel = s > np.quantile(s, 1 - mean)
    if era == "artist": c = rng.integers(1960, 2013, G)[gg]; t0 = np.minimum(c + rng.integers(0, 9, len(R)), 2015)
    else: c = rng.integers(1985, 2013, G)[gg]; t0 = np.minimum(c + rng.integers(0, 4, len(R)), 2015)
    zc = math.sqrt(rho_a) * rng.normal(0, 1, G)[gg] + math.sqrt(1 - rho_a) * rng.normal(0, 1, len(R))
    eta = stats.gamma.ppf(stats.norm.cdf(zc), P["r"], scale=1 / P["r"])
    out = []
    for i in np.flatnonzero(sel):
        q = dict(R[i]); q["t0"] = int(t0[i]); q["eta"] = float(eta[i]); out.append(q)
    return out


_EXP = {}
def exp_cached(t0, a0, a1):
    k = (t0, a0, a1)
    if k not in _EXP: _EXP[k] = exposure(t0, a0, a1)
    return _EXP[k]
