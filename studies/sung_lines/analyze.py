"""Questions 1 to 4 of PREDICTION.md. Numbers only; writes result.json here. Question 3's power is reckoned and printed before its coefficient is read."""
import json, os, numpy as np, pandas as pd, statsmodels.api as sm
from scipy.stats import spearmanr
D = "/home/claude/lyr_dl/sung/"; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json")
s = pd.read_csv(D + "sung.csv"); w = pd.read_csv(D + "wasabi.csv"); c = pd.read_csv(D + "covers.csv")
both = s.merge(w, on="key", suffixes=("_s", "_w")).merge(c, on="key", how="left")
res = {"sung_songs": int(len(s)), "in_wasabi": int(len(both)), "with_covers": int(both.n_artists.notna().sum())}
# 1. typing habit
ex = both.repeat_share_w - both.repeat_share_s; res["q1_mean_excess"] = round(float(ex.mean()), 4); res["q1_median_excess"] = round(float(ex.median()), 4)
cv = both[both.n_artists.notna()]; r1, p1 = spearmanr(cv.repeat_share_w - cv.repeat_share_s, np.log(cv.n_artists))
res["q1_excess_vs_covers"] = dict(rho=round(float(r1), 3), p_one_sided=round(float(p1 / 2 if r1 > 0 else 1 - p1 / 2), 4), n=int(len(cv)))
res["q1_named"] = bool(res["q1_mean_excess"] >= 0.05 and r1 > 0 and p1 / 2 < 0.05)
# 2. agreement
for m in ("repeat_share", "syl_line"):
    r, p = spearmanr(both[m + "_s"], both[m + "_w"]); res[f"q2_{m}"] = dict(rho=round(float(r), 3), p=float(p), mean_sung=round(float(both[m + "_s"].mean()), 3), mean_wasabi=round(float(both[m + "_w"].mean()), 3))
# 3. shorter lines on their own, sung, across songs
x = s.merge(c, on="key"); x["y"] = np.log(x.n_artists); x["logn"] = np.log(x.n_words); x["yr"] = (x.year - x.year.mean()) / 10
x["z"] = (x.syl_line - x.syl_line.mean()) / x.syl_line.std(); x["rep"] = (x.repeat_share - x.repeat_share.mean()) / x.repeat_share.std()
X = sm.add_constant(x[["z", "logn", "yr", "rep"]])
rng = np.random.default_rng(749); hits = 0
for _ in range(1000):
    yf = rng.permutation(x.y.values) - 0.029 * x.z.values
    f = sm.OLS(yf, X).fit(); hits += f.params["z"] < 0 and f.pvalues["z"] / 2 < 0.05
res["q3_power"] = round(hits / 1000, 3); print("question 3 power", res["q3_power"], "n", len(x), flush=True)
f = sm.OLS(x.y, X).fit(cov_type="HC1"); b, p = float(f.params["z"]), float(f.pvalues["z"])
res["q3"] = dict(n=int(len(x)), coef=round(b, 4), p_one_sided=round(p / 2 if b < 0 else 1 - p / 2, 4), counts=bool(res["q3_power"] >= 0.2),
                 verdict=("estimate only (under the power floor)" if res["q3_power"] < 0.2 else ("passes" if b < 0 and p / 2 < 0.05 else "unsettled")))
# 4. described
r4, p4 = spearmanr(s.syl_line, s.repeat_share); res["q4_syl_vs_repeat_sung"] = dict(rho=round(float(r4), 3), p=float(p4), n=int(len(s)))
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res, indent=1))
