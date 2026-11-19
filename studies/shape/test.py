import pickle, numpy as np, pandas as pd, json
from scipy.stats import rankdata, pearsonr
x = pickle.load(open("shapes.pkl", "rb")); PRED = dict(M1=1, M2=1, M3=-1, M4=1, M5=-1, M6=1)
def partial(d, m, y, peak=False):
    d = d.dropna(subset=[m, y] + (["peak"] if peak else [])); C = [np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + [(d.src == s).astype(float).values for s in ("CB", "RS", "BM")] + ([rankdata(d.peak)] if peak else [])
    C = np.c_[tuple(C)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(d[m])), res(rankdata(d[y]))); return round(float(r), 3), float(p), len(d)
out = {}
print(f"{'':4}{'pred':>5} {'half A':>16} {'half B':>16} {'pooled':>18} {'+peak':>16} {'whole songs':>16} {'love':>8} {'covers':>8}  verdict")
for m, s in PRED.items():
    a = partial(x[x.half == 0], m, "G"); b = partial(x[x.half == 1], m, "G"); p = partial(x, m, "G"); k = partial(x, m, "G", True); w = partial(x[x.src != "HT"], m, "G"); lo = partial(x, m, "love"); co = partial(x, m, "cover_rank")
    ok = all(np.sign(v[0]) == s for v in (a, b, p, k, w)) and a[1] < .05 and b[1] < .05 and p[1] < .007
    f = lambda v: f"{v[0]:+.3f} p={v[1]:.3f}"; print(f"{m:4}{s:+5d} {f(a):>16} {f(b):>16} {f(p):>18} {f(k):>16} {f(w):>16} {lo[0]:+8.3f} {co[0]:+8.3f}  {'PASS' if ok else 'fail'}")
    out[m] = dict(pred=s, halfA=a, halfB=b, pooled=p, with_peak=k, whole=w, love=lo, covers=co, verdict="pass" if ok else "fail")
print("n", len(x), "whole", int((x.src != "HT").sum()), "G vs peak", partial(x, "peak", "G")); json.dump(out, open("shapes_results.json", "w"), indent=1)
