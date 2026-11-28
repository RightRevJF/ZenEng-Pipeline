"""formula_search, step 1: gates (notes only), then discovery on HALF 0 ONLY. Writes selected.json. Half-1 rows never reach the loader."""
import os, sys, json, itertools
import numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import common13 as C
R, names = C.song_table()
Z = {n: (lambda v: (v - np.nanmean(v)) / np.nanstd(v))(np.array([r[n] for r in R], float)) for n in names}
def zc(f, rows): v = np.array([f.get(n, np.nan) for f in rows], float); return v
cands = {n: ("base", n) for n in names}
for a, b in itertools.combinations(names, 2):
    cands[f"{a} - {b}"] = ("diff", a, b); cands[f"{a} * {b}"] = ("prod", a, b)
def value(spec, getz):
    if spec[0] == "base": return getz(spec[1])
    if spec[0] == "diff": return getz(spec[1]) - getz(spec[2])
    return getz(spec[1]) * getz(spec[2])
mu = {n: np.nanmean([r[n] for r in R]) for n in names}; sd = {n: np.nanstd([r[n] for r in R]) for n in names}
H0 = [i for i, r in enumerate(R) if r["half"] == 0]
P = [i for i in H0 if R[i]["_c12"] is not None]
z1 = {n: (np.array([R[i]["_c12"][0][n] for i in P], float) - mu[n]) / sd[n] for n in names}
z2 = {n: (np.array([R[i]["_c12"][1][n] for i in P], float) - mu[n]) / sd[n] for n in names}
ref = {k: np.array([R[i][k] if R[i][k] is not None else np.nan for i in H0], float) for k in ("REP", "ch_rep", "ln_notes")}
gated = {}; stops = {"stability": 0, "overlap": 0, "coverage": 0}
for k, spec in cands.items():
    v0 = value(spec, lambda n: Z[n][H0])
    if np.isfinite(v0).sum() < 2000: stops["coverage"] += 1; continue
    a = value(spec, lambda n: z1[n]); b = value(spec, lambda n: z2[n]); ok = np.isfinite(a) & np.isfinite(b)
    st = spearmanr(a[ok], b[ok])[0] if ok.sum() > 100 else np.nan
    if not (st >= 0.20): stops["stability"] += 1; continue
    ov = max(abs(spearmanr(v0[np.isfinite(v0) & np.isfinite(rv)], rv[np.isfinite(v0) & np.isfinite(rv)])[0]) for rv in ref.values())
    if ov >= 0.70: stops["overlap"] += 1; continue
    gated[k] = dict(spec=spec, stability=float(st), max_overlap=float(ov))
print(len(cands), "candidates;", len(gated), "pass the notes-side gates;", stops, flush=True)
json.dump(dict(n_candidates=len(cands), gated=len(gated), stops=stops), open(os.path.join(HERE, "gates.json"), "w"), indent=1)
if sys.argv[1:] != ["run"]: sys.exit(0)
# ---- outcome: half 0 only
R0 = [R[i] for i in H0]
info = C.load_y(R0, [os.path.join(HERE, "PREDICTION.md"), os.path.join(HERE, "discover.py"), os.path.join(os.path.dirname(HERE), "common13.py"), os.path.join(os.path.dirname(HERE), "features13.py")])
res = []
for k, g in gated.items():
    x = value(g["spec"], lambda n: Z[n][H0]); m, _, _ = C.within(R0, x, "y"); res.append((m["p"], k, m))
res.sort(key=lambda t: t[0])
sel = []
for p, k, m in res:
    x = value(gated[k]["spec"], lambda n: Z[n][H0])
    if any(abs(spearmanr(x[np.isfinite(x) & np.isfinite(s["_x"])], s["_x"][np.isfinite(x) & np.isfinite(s["_x"])])[0]) >= 0.70 for s in sel): continue
    sel.append(dict(name=k, spec=gated[k]["spec"], discovery=m, stability=gated[k]["stability"], max_overlap=gated[k]["max_overlap"], _x=x))
    if len(sel) == 3: break
top = [dict(name=k, beta=m["beta"], se=m["se"], p=m["p"]) for p, k, m in res[:25]]
out = dict(outcome_info=info, tested=len(res), half0_rows=len(R0), selected=[{a: b for a, b in s.items() if a != "_x"} for s in sel], top25=top,
           p_values_under_001=int(sum(p < 0.001 for p, _, _ in res)), expected_under_001_if_null=round(0.001 * len(res), 1),
           mu={n: float(mu[n]) for n in names}, sd={n: float(sd[n]) for n in names})
json.dump(out, open(os.path.join(HERE, "selected.json"), "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k not in ("mu", "sd")}, indent=1, default=float))
