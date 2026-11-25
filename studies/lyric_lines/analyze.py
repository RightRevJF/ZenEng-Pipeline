"""Tests 1 and 2 of PREDICTION.md. Reads numbers only. Usage: python3 analyze.py feat.csv"""
import sys, json, os, hashlib, numpy as np, pandas as pd
from statsmodels.discrete.conditional_models import ConditionalLogit
PRED = {"rhyme_rate": +1, "perfect_share": -1, "iyou_rate": +1, "you_lines": +1, "end_weight": +1, "feel_late": +1}
DESC = ["line_cv", "syl_line", "repeat_share", "emo_rate", "i_rate", "stanzas"]
d = pd.read_csv(sys.argv[1]); d["logn"] = np.log(d.n_words); yr_ok = d.year.notna().mean()
use_year = yr_ok >= 0.8
if use_year: d = d[d.year.notna()].copy(); d["yr"] = (d.year - d.year.mean()) / 10
g = d.groupby("artist").rs.agg(["sum", "count"]); keep = g[(g["sum"] >= 1) & (g["count"] >= 5) & (g["sum"] < g["count"])].index; d = d[d.artist.isin(keep)].copy()
d["half"] = [int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 for a in d.artist]
def holm(ps):
    o = sorted(range(len(ps)), key=lambda i: ps[i]); m = len(ps); adj = [0] * m; run = 0
    for k, i in enumerate(o): run = max(run, min(1, (m - k) * ps[i])); adj[i] = run
    return adj
def fit(x, m):
    x = x[x[m].notna()].copy(); gg = x.groupby("artist").rs.agg(["sum", "count"]); x = x[x.artist.isin(gg[(gg["sum"] >= 1) & (gg["sum"] < gg["count"])].index)].copy()
    x["z"] = (x[m] - x[m].mean()) / x[m].std(); f = ConditionalLogit(x.rs, x[["z", "logn"] + (["yr"] if use_year else [])], groups=x.artist).fit(disp=0)
    return float(f.params["z"]), float(f.pvalues["z"]), int(len(x)), int(x.rs.sum()), float(x[x.rs == 1][m].mean()), float(x[x.rs == 0][m].mean())
res = {"year_known_share": round(float(yr_ok), 3), "year_used": bool(use_year), "artists": int(d.artist.nunique()), "songs": int(len(d)), "listed": int(d.rs.sum()), "measures": {}}
for m in list(PRED) + DESC:
    c, p, n, k, a, b = fit(d, m); h = [fit(d[d.half == i], m)[0] for i in (0, 1)]
    res["measures"][m] = dict(coef=round(c, 3), p=round(p, 4), n=n, listed=k, mean_listed=round(a, 4), mean_other=round(b, 4), halves=[round(x, 3) for x in h])
adj = holm([res["measures"][m]["p"] for m in PRED])
for m, pa in zip(PRED, adj):
    r = res["measures"][m]; r["p_holm"] = round(pa, 4); same = all(np.sign(x) == PRED[m] for x in r["halves"])
    r["predicted"] = PRED[m]; r["verdict"] = "passes" if np.sign(r["coef"]) == PRED[m] and pa < 0.05 and same else "reversed" if np.sign(r["coef"]) == -PRED[m] and r["p"] < 0.05 else "unsettled"
json.dump(res, open(os.path.dirname(os.path.abspath(__file__)) + "/result.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "measures"}))
for m, r in res["measures"].items(): print(f"{m:14s} {r['coef']:+.3f} p {r['p']:.4f} holm {r.get('p_holm', '')} halves {r['halves']} listed {r['mean_listed']} other {r['mean_other']} {r.get('verdict', '')}")
