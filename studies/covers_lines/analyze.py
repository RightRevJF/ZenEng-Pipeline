"""Design B, step 3: tests 1 to 3 of PREDICTION.md. Reads numbers only; writes result.json here."""
import json, os, hashlib, numpy as np, pandas as pd, statsmodels.api as sm
J = "/home/claude/lyr_dl/covers_join.csv"; F = "/home/claude/lyr_dl/covers_feat.csv"; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json")
PRED = {"rhyme_rate": +1, "iyou_rate": +1, "you_lines": +1, "end_weight": +1, "feel_late": +1, "syl_line": -1, "line_cv": -1}
DESC = ["perfect_share", "repeat_share", "stanzas", "emo_rate", "i_rate"]
d = pd.read_csv(J).merge(pd.read_csv(F), on="id"); d["year"] = pd.to_numeric(d.year, errors="coerce")
d["y"] = np.log(d.n_artists); d["logn"] = np.log(d.n_words)
d["half"] = [int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 for a in d.writer]
def holm(ps):
    o = sorted(range(len(ps)), key=lambda i: ps[i]); m = len(ps); adj = [0] * m; run = 0
    for k, i in enumerate(o): run = max(run, min(1, (m - k) * ps[i])); adj[i] = run
    return adj
def fit(x, m):
    x = x[x[m].notna() & x.year.notna()].copy(); x["yr"] = (x.year - x.year.mean()) / 10; x["z"] = (x[m] - x[m].mean()) / x[m].std()
    c = x.groupby("writer").writer.transform("size"); x = x[c >= 2]
    cols = ["y", "z", "logn", "yr"]; dm = x[cols] - x.groupby("writer")[cols].transform("mean")
    f = sm.OLS(dm.y, dm[["z", "logn", "yr"]]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.writer)[0]})
    return float(f.params["z"]), float(f.pvalues["z"]), int(len(x))
prim = d[d.matched == 1].copy(); cnt = prim.groupby("writer").size(); prim = prim[prim.writer.isin(cnt[cnt >= 10].index)]
sec = d[d.writer.isin(prim.writer.unique())].copy()
res = {"primary": {"writers": int(prim.writer.nunique()), "songs": int(len(prim)), "median_artists": float(prim.n_artists.median())},
       "secondary": {"writers": int(sec.writer.nunique()), "songs": int(len(sec)), "matched_share": round(float(sec.matched.mean()), 3)}, "measures": {}}
for m in list(PRED) + DESC:
    c, p, n = fit(prim, m); h = [fit(prim[prim.half == i], m)[0] for i in (0, 1)]; c3, p3, n3 = fit(sec, m)
    res["measures"][m] = dict(coef=round(c, 4), p=round(p, 5), n=n, halves=[round(x, 4) for x in h], with_zeros=round(c3, 4), with_zeros_p=round(p3, 5))
adj = holm([res["measures"][m]["p"] for m in PRED])
for m, a in zip(PRED, adj):
    r = res["measures"][m]; s = PRED[m]; r["p_holm"] = round(a, 5); r["predicted"] = s
    ok = np.sign(r["coef"]) == s and a < 0.05 and all(np.sign(x) == s for x in r["halves"]) and np.sign(r["with_zeros"]) == s
    r["verdict"] = "passes" if ok else "reversed" if (np.sign(r["coef"]) == -s and r["p"] < 0.05) else "unsettled"
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "measures"}))
for m, r in res["measures"].items():
    print(f"{m:14s} {r['coef']:+.4f} p {r['p']:.5f} holm {r.get('p_holm', '')} halves {r['halves']} zeros {r['with_zeros']:+.4f} (p {r['with_zeros_p']:.4f}) {r.get('verdict', 'desc')}")
