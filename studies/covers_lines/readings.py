"""Readings after the result (RESULT.md): the two passes on first-sung lines and with repeat_share held. Reads numbers only."""
import numpy as np, pandas as pd, statsmodels.api as sm, hashlib
d = pd.read_csv("/home/claude/lyr_dl/covers_join.csv").merge(pd.read_csv("/home/claude/lyr_dl/covers_feat_first.csv"), on="id"); d["year"] = pd.to_numeric(d.year, errors="coerce")
d["y"] = np.log(d.n_artists); d["logn"] = np.log(d.n_words); d["half"] = [int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 for a in d.writer]
p = d[d.matched == 1]; c = p.groupby("writer").size(); p = p[p.writer.isin(c[c >= 10].index)]; s = d[d.writer.isin(p.writer.unique())]
def fit(x, m, extra=[]):
    x = x[x[m].notna() & x.year.notna()].copy(); x["yr"] = (x.year - x.year.mean()) / 10; x["z"] = (x[m] - x[m].mean()) / x[m].std()
    for e in extra: x[e] = (x[e] - x[e].mean()) / x[e].std()
    cols = ["y", "z", "logn", "yr"] + extra; dm = x[cols] - x.groupby("writer")[cols].transform("mean")
    f = sm.OLS(dm.y, dm[cols[1:]]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.writer)[0]}); return float(round(f.params["z"], 4)), float(round(f.pvalues["z"], 5))
for m in ["syl_line", "syl_line_first", "iyou_rate", "iyou_first", "you_lines_first"]:
    print(m, fit(p, m), "halves", [fit(p[p.half == i], m)[0] for i in (0, 1)], "zeros", fit(s, m), "with repeat_share", fit(p, m, ["repeat_share"]))
print("r(syl_line, repeat_share)", round(p[["syl_line", "repeat_share"]].corr().iloc[0, 1], 3))
