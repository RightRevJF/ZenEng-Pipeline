"""Run 10 shared code: TheSession.org tunes (melody only), design, baseline measures, frozen model, power, verdict.

Data (outside the repo, never committed): /home/claude/dl/thesession/ from github.com/adactio/TheSession-data (csv/, main
branch, fetched 27 Nov 2026 18:19 ET). tunes.csv (settings, ABC), tune_popularity.csv and recordings.csv (OUTCOMES).
Parsed melodies: /home/claude/dl/thesession/parsed.jsonl.gz (parser /home/claude/scripts/parser/abcparse.py, copied to
run10/experiments/abcparse.py; notes side only).

THE DESIGN (written by the orchestrator before any outcome was joined to any measure):
  unit = a tune (tune_id). Its melody = its FIRST ok setting (lowest setting_id; the original posting), 'expanded' order
  (repeats played). Tunes with no ok setting, or under 16 notes, are dropped. Settings count is NEVER a control (it is
  downstream of popularity).
  split (sha256 of 'thesession:<tune_id>', first hex digit): 0-9 -> 'A' (this pass's tests), a-c -> 'C' (this pass's
  confirmation of anything that passes on A, rule first), d-f -> 'H' (sealed for later passes; not to be joined this pass).
  controls (fixed effects): tune type; meter; mode (the 'mode' column, levels with < 20 tunes in the analysed rows pooled);
  first-posting year (min date over the tune's settings); composer (normalised; blank or containing 'trad' = none), as a fixed
  effect for composers with >= 2 analysed tunes, plus an indicator 'has a named composer'.
  clusters for SEs: composer key (named) or the tune itself.
  halves: md5 of the composer key (named) or of 'trad:<tune_id>'; first hex digit even -> half 0, odd -> half 1.
OUTCOMES (joined only through load_outcomes, after the test's PREDICTION.md is committed and pushed):
  y_cov  = log(1 + number of distinct recording artists of the tune in recordings.csv) -- covers by other artists;
  y_love = log(tunebooks) for tunes in tune_popularity.csv (the file lists only tunes with >= 10 tunebooks; others missing) --
           musicians choosing to learn the tune (a love reading, truncated sample).
  Both standardised over the analysed rows.
THE MODEL: OLS of z(y) on z(measure) plus the fixed effects above (and any extra frozen controls), by Frisch-Waugh: y and x are
  residualised on the control matrix, slope and cluster-robust SE (CR1) from the residuals. Second model: Poisson GLM of the
  artist count on z(measure) and the same dummies (HC0), sign only (y_cov tests); for y_love, OLS on the other half-split is the
  check (no count model; it is truncated).
POWER (before the outcome): fake y = beta*z(x)+N(0,1-beta^2) on the real rows, the same model, 300 draws, seed 10; power =
  share with p < alpha and the predicted sign; also kill_if_true and kill_if_zero (range kill firing).
VERDICT (rulings in force): counted only if power >= 0.2 (R06-5); pass = p < alpha, predicted sign, same sign in both halves,
  same sign in the second model; killed = the prediction lies outside the 95% range (R07-3); otherwise unsettled. Under the
  floor: estimate (passes nothing, kills nothing).
Licences: TheSession data (Jeremy Keith / thesession.org, published on GitHub for reuse); credit it in anything derived.
"""
import os, sys, json, gzip, hashlib, math, subprocess, re
import numpy as np
from scipy import stats

REPO = "/home/claude/zeneng-pipeline"
DL = "/home/claude/dl/thesession"
HERE = os.path.dirname(os.path.abspath(__file__))
PARSED = os.path.join(DL, "parsed.jsonl.gz")
SEED = 10

def split_of(tid):
    h = hashlib.sha256(f"thesession:{tid}".encode()).hexdigest()[0]
    return "A" if h in "0123456789" else ("C" if h in "abc" else "H")

def norm_composer(c):
    if c is None or (isinstance(c, float) and math.isnan(c)): return None
    c = re.sub(r"\s+", " ", str(c).strip().lower())
    if not c or "trad" in c or c in ("unknown", "anon", "anon.", "anonymous", "?"): return None
    return c

def half_of(ckey, tid):
    s = ckey if ckey else f"trad:{tid}"
    return int(hashlib.md5(s.encode()).hexdigest()[0], 16) % 2

_TUNES = None
def tunes():
    """{tune_id: dict(type, meter, mode, year, composer, split, half, setting_id, mel={pitch,dur,onset,bar,beatpos}, n_settings_ok,
    other=[second ok setting's melody or None])} -- notes side only."""
    global _TUNES
    if _TUNES is not None: return _TUNES
    import csv
    csv.field_size_limit(10**9)
    meta = {}
    with open(os.path.join(DL, "tunes.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = int(r["tune_id"]); y = int(r["date"][:4]) if r["date"][:4].isdigit() else None
            m = meta.setdefault(t, {"year": y, "composer": None, "name": r["name"]})
            if y is not None and (m["year"] is None or y < m["year"]): m["year"] = y
            nc = norm_composer(r["composer"])
            if nc and not m["composer"]: m["composer"] = nc
    by = {}
    with gzip.open(PARSED, "rt") as f:
        for line in f:
            s = json.loads(line)
            if not s["ok"]: continue
            by.setdefault(s["tune_id"], []).append(s)
    T = {}
    for tid, L in by.items():
        L.sort(key=lambda s: s["setting_id"])
        s0 = L[0]
        if len(s0["expanded"]["pitch"]) < 16: continue
        mt = meta.get(tid, {})
        ck = mt.get("composer")
        T[tid] = dict(tune_id=tid, name=mt.get("name"), type=s0["type"], meter=s0["meter"], mode=s0["mode"],
                      tonic_pc=s0["tonic_pc"], mode_name=s0["mode_name"], year=mt.get("year"), composer=ck,
                      split=split_of(tid), half=half_of(ck, tid), setting_id=s0["setting_id"], mel=s0["expanded"],
                      written=s0["written"], n_settings_ok=len(L),
                      other=(L[1]["expanded"] if len(L) > 1 and len(L[1]["expanded"]["pitch"]) >= 16 else None))
    _TUNES = T
    return T

# ---------------------------------------------------------------- baseline measures (renaming checks)
def _entropy(counts):
    c = np.array([v for v in counts if v > 0], float)
    if c.sum() == 0: return 0.0
    p = c / c.sum(); return float(-(p * np.log2(p)).sum())

def baseline(mel, tonic_pc):
    p = np.array(mel["pitch"], int); d = np.array(mel["dur"], float); b = np.array(mel["bar"], int)
    iv = np.diff(p)
    nb = len(set(b.tolist()))
    bars = {}
    for pi, di, bi in zip(p, d, b): bars.setdefault(int(bi), []).append((int(pi), round(float(di), 4)))
    seq = [tuple(bars[k]) for k in sorted(bars)]
    pcd = np.zeros(12)
    for pi, di in zip(p, d): pcd[pi % 12] += di
    return dict(
        ln_notes=math.log(len(p)), n_bars=nb, density=len(p) / max(nb, 1),
        n_pitch=len(set(p.tolist())), n_pc=len(set((p % 12).tolist())), range=int(p.max() - p.min()),
        int_entropy=_entropy(np.bincount(np.clip(iv + 24, 0, 48), minlength=49)),
        n_int=len(set(iv.tolist())), step_share=float(np.mean((np.abs(iv) >= 1) & (np.abs(iv) <= 2))),
        leap_share=float(np.mean(np.abs(iv) > 4)), unison_share=float(np.mean(iv == 0)),
        pc_entropy=_entropy(pcd), tonic_share=float(pcd[tonic_pc % 12] / pcd.sum()),
        bar_rep=1.0 - len(set(seq)) / max(len(seq), 1),
    )
BASE = ["ln_notes", "density", "n_pitch", "n_pc", "range", "int_entropy", "n_int", "step_share", "leap_share",
        "unison_share", "pc_entropy", "tonic_share", "bar_rep"]

# ---------------------------------------------------------------- outcomes (guarded)
def _committed_and_pushed(folder):
    pred = os.path.join(folder, "PREDICTION.md")
    if not os.path.exists(pred): return False
    rel = os.path.relpath(pred, REPO)
    out = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "origin/judging-research", "--", rel],
                         capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", REPO, "diff", "--name-only", "origin/judging-research", "--", rel],
                           capture_output=True, text=True).stdout.strip()
    return bool(out) and not dirty

def load_outcomes(folder, splits=("A",)):
    """{tune_id: dict(n_art, y_cov_raw, tunebooks)} for tunes in the given splits. Refuses unless PREDICTION.md is pushed.
    Split 'H' is sealed this pass."""
    if not _committed_and_pushed(folder):
        raise SystemExit(f"REFUSED: {folder}/PREDICTION.md is not committed and pushed to origin/judging-research")
    if "H" in splits: raise SystemExit("REFUSED: split H is sealed this pass")
    import csv
    T = tunes(); keep = {t for t, v in T.items() if v["split"] in splits}
    art = {}
    with open(os.path.join(DL, "recordings.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try: t = int(r["tune_id"])
            except Exception: continue
            if t in keep: art.setdefault(t, set()).add(r["artist"])
    tb = {}
    with open(os.path.join(DL, "tune_popularity.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = int(r["tune_id"])
            if t in keep: tb[t] = int(r["tunebooks"])
    return {t: dict(n_art=len(art.get(t, ())), y_cov_raw=math.log1p(len(art.get(t, ()))), tunebooks=tb.get(t)) for t in keep}

# ---------------------------------------------------------------- model
def _dummies(vals, min_n=1, prefix=""):
    vals = [str(v) for v in vals]
    from collections import Counter
    c = Counter(vals)
    vals = [v if c[v] >= min_n else "__other__" for v in vals]
    lv = sorted(set(vals))
    if len(lv) <= 1: return np.zeros((len(vals), 0))
    idx = {v: i for i, v in enumerate(lv[1:])}
    M = np.zeros((len(vals), len(lv) - 1))
    for i, v in enumerate(vals):
        if v in idx: M[i, idx[v]] = 1
    return M

def control_matrix(R, extra=()):
    """intercept + type, meter, mode (pooled < 20), year, composer FE (>= 2 tunes), has-composer, extra z-columns."""
    from collections import Counter
    n = len(R)
    cc = Counter(r["composer"] for r in R if r["composer"])
    comp = [r["composer"] if (r["composer"] and cc[r["composer"]] >= 2) else "__none__" for r in R]
    cols = [np.ones((n, 1)), _dummies([r["type"] for r in R]), _dummies([r["meter"] for r in R]),
            _dummies([r["mode"] for r in R], min_n=20), _dummies([r["year"] for r in R]),
            _dummies(comp), np.array([[1.0 if r["composer"] else 0.0] for r in R])]
    for e in extra:
        v = np.array([r[e] for r in R], float); sd = v.std()
        cols.append(((v - v.mean()) / sd)[:, None] if sd > 1e-12 else np.zeros((n, 0)))
    M = np.hstack([c for c in cols if c.shape[1]])
    # drop exactly collinear columns via QR
    q, rr = np.linalg.qr(M)
    keep = np.abs(np.diag(rr)) > 1e-8
    return M[:, keep]

def clusters(R):
    return [r["composer"] if r["composer"] else f"t{r['tune_id']}" for r in R]

class Projector:
    def __init__(self, Ctrl):
        self.Q, _ = np.linalg.qr(Ctrl); self.k = Ctrl.shape[1]
    def resid(self, v):
        return v - self.Q @ (self.Q.T @ v)

def _z(v):
    v = np.asarray(v, float); return (v - v.mean()) / v.std()

def fwl_fit(rx, ry, cl, k):
    """slope and CR1 cluster SE of ry on rx (both residualised); k = number of control columns."""
    n = len(rx); sxx = float(rx @ rx)
    b = float(rx @ ry) / sxx; e = ry - b * rx
    g = {}
    for i, c in enumerate(cl): g[c] = g.get(c, 0.0) + rx[i] * e[i]
    G = len(g); meat = sum(v * v for v in g.values())
    adj = (G / (G - 1)) * ((n - 1) / (n - k - 1))
    se = math.sqrt(adj * meat) / sxx
    p = 2 * stats.norm.sf(abs(b / se))
    return b, se, p

def fit(R, xcol, ycol, extra=()):
    x = _z([r[xcol] for r in R]); y = _z([r[ycol] for r in R])
    P = Projector(control_matrix(R, extra)); cl = clusters(R)
    b, se, p = fwl_fit(P.resid(x), P.resid(y), cl, P.k)
    return dict(beta=b, se=se, p=p, lo=b - 1.96 * se, hi=b + 1.96 * se, n=len(R))

def power(R, xcol, beta, alpha, extra=(), draws=300, seed=SEED):
    rng = np.random.default_rng(seed)
    x = _z([r[xcol] for r in R]); P = Projector(control_matrix(R, extra)); cl = clusters(R); rx = P.resid(x)
    hit = kt = kz = 0; ses = []
    for _ in range(draws):
        for which in ("true", "zero"):
            bb = beta if which == "true" else 0.0
            y = _z(bb * x + rng.normal(0, math.sqrt(max(1 - bb * bb, 1e-9)), len(x)))
            b, se, p = fwl_fit(rx, P.resid(y), cl, P.k)
            killed = not (b - 1.96 * se <= beta <= b + 1.96 * se)
            if which == "true":
                ses.append(se); kt += killed
                if p < alpha and np.sign(b) == np.sign(beta): hit += 1
            else:
                kz += killed
    return dict(power=hit / draws, kill_if_true=kt / draws, kill_if_zero=kz / draws, median_fake_se=float(np.median(ses)),
                draws=draws, seed=seed, n=len(R))

def halves(R, xcol, ycol, extra=()):
    out = []
    for h in (0, 1):
        S = [r for r in R if r["half"] == h]
        out.append(fit(S, xcol, ycol, extra))
    return out

def poisson_sign(R, xcol, count_col="n_art", extra=()):
    import statsmodels.api as sm
    x = _z([r[xcol] for r in R])
    C = control_matrix(R, extra)
    X = np.hstack([x[:, None], C])
    y = np.array([r[count_col] for r in R], float)
    try:
        m = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC0", maxiter=200)
        return dict(beta=float(m.params[0]), se=float(m.bse[0]), p=float(m.pvalues[0]))
    except Exception as ex:
        return dict(beta=float("nan"), se=float("nan"), p=float("nan"), error=str(ex))

def verdict(res, pred_beta, alpha, pw, halves_res, second):
    counted = pw >= 0.2
    sign_ok = np.sign(res["beta"]) == np.sign(pred_beta)
    halves_ok = all(np.sign(h["beta"]) == np.sign(pred_beta) for h in halves_res)
    second_ok = (second is not None) and np.sign(second["beta"]) == np.sign(pred_beta)
    killed = not (res["lo"] <= pred_beta <= res["hi"])
    if not counted: v = "estimate"
    elif res["p"] < alpha and sign_ok and halves_ok and second_ok: v = "passed"
    elif killed: v = "killed"
    else: v = "unsettled"
    return dict(verdict=v, counted=counted, sign_ok=bool(sign_ok), halves_ok=bool(halves_ok), second_ok=bool(second_ok),
                prediction_outside_range=bool(killed))

def rows(split="A", measure_fn=None, need=()):
    """design rows for a split, with baseline measures and (optionally) a measure computed by measure_fn(tune) -> dict."""
    T = tunes(); R = []
    for tid, t in T.items():
        if t["split"] != split: continue
        r = {k: t[k] for k in ("tune_id", "type", "meter", "mode", "tonic_pc", "mode_name", "year", "composer", "half")}
        r.update(baseline(t["mel"], t["tonic_pc"]))
        if measure_fn is not None:
            m = measure_fn(t)
            if m is None: continue
            r.update(m)
        if all(r.get(c) is not None and np.isfinite(r.get(c)) for c in need): R.append(r)
    return R

def renaming(R, xcol, cols=BASE):
    x = np.array([r[xcol] for r in R], float); out = {}
    for c in cols:
        v = np.array([r[c] for r in R], float)
        if v.std() > 0: out[c] = float(stats.spearmanr(x, v).correlation)
    # R^2 of x on all baseline columns (linear)
    X = np.column_stack([np.ones(len(R))] + [_z([r[c] for r in R]) for c in cols if np.std([r[c] for r in R]) > 0])
    beta, *_ = np.linalg.lstsq(X, x, rcond=None); res = x - X @ beta
    out["R2_on_baseline"] = float(1 - res.var() / x.var())
    return out

def stability(measure_fn, split="A", key=None, max_n=4000):
    """Spearman correlation of the measure between a tune's first and second ok settings (notes side)."""
    T = tunes(); a = []; b = []
    for tid, t in T.items():
        if t["split"] != split or t["other"] is None: continue
        t2 = dict(t); t2["mel"] = t["other"]
        m1 = measure_fn(t); m2 = measure_fn(t2)
        if m1 is None or m2 is None: continue
        v1 = m1[key]; v2 = m2[key]
        if np.isfinite(v1) and np.isfinite(v2): a.append(v1); b.append(v2)
        if len(a) >= max_n: break
    return dict(spearman=float(stats.spearmanr(a, b).correlation), n=len(a))
