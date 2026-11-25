import numpy as np, pandas as pd, statsmodels.api as sm, hashlib
d = pd.read_csv("feat.csv"); d["year"] = pd.to_numeric(d.year, errors="coerce"); c = d.groupby("writer").size(); d = d[d.writer.isin(c[c >= 10].index)].copy()
d["y"] = np.log(d.n_artists); d["logn"] = np.log(d.n_words); d["half"] = [int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 for a in d.writer]
print("writers", d.writer.nunique(), "songs", len(d), "median artists", d.n_artists.median())
def fit(x, m, extra=[]):
    x = x[x[m].notna() & x.year.notna()].copy(); x["yr"] = (x.year - x.year.mean()) / 10; x["z"] = (x[m] - x[m].mean()) / x[m].std()
    for e in extra: x[e] = (x[e] - x[e].mean()) / x[e].std()
    cols = ["y", "z", "logn", "yr"] + extra; dm = x[cols] - x.groupby("writer")[cols].transform("mean")
    f = sm.OLS(dm.y, dm[cols[1:]]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.writer)[0]}); return round(float(f.params["z"]), 4), round(float(f.pvalues["z"]), 5)
for m in ["iyou_rate", "syl_line", "rhyme_rate", "line_cv", "end_weight", "you_lines", "feel_late", "repeat_share", "i_rate", "emo_rate"]:
    print(f"{m:13s}", fit(d, m), "halves", [fit(d[d.half == i], m)[0] for i in (0, 1)], "| repeat held", fit(d, m, ["repeat_share"]) if m != "repeat_share" else "")
# a harder control: the song's fame at Deezer is not in feat; instead drop the top-covered tenth of each writer's songs
q = d.groupby("writer").n_artists.transform(lambda s: s.quantile(0.9)); e = d[d.n_artists <= q]
print("without each writer's most-covered tenth:", {m: fit(e, m) for m in ("iyou_rate", "syl_line")})
