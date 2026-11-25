"""Tests 1-3 of PREDICTION.md. Reads numbers only (feat.csv, covers.csv)."""
import csv, json, math, sys, collections
import numpy as np, pandas as pd
import statsmodels.api as sm
from statsmodels.discrete.conditional_models import ConditionalLogit

FEAT = "/home/claude/lyr_dl/feat.csv"
COV = "/home/claude/lyr_dl/covers.csv"
OUT = "/home/claude/zeneng-pipeline/studies/lyric_research/result.json"

PRED = {"conc_noun": +1, "image_noun_rate": +1, "emo_rate": -1, "poetic_stock_rate": -1,
        "verb_share": +1, "you_rate": +1, "stock_rate": -1, "repetition": -1,
        "mattr": +1, "zipf_content": -1, "allit_rate": +1, "asson_rate": +1,
        "sem_dist": "U"}
DESC = ["adj_share", "i_rate", "we_rate", "compress", "archaic_rate"]


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i]); m = len(ps); adj = [0] * m; run = 0
    for k, i in enumerate(order):
        run = max(run, min(1, (m - k) * ps[i])); adj[i] = run
    return adj


def main():
    d = pd.read_csv(FEAT)
    d = d.dropna(subset=list(PRED) + DESC).copy()
    d["logn"] = np.log(d.n_words)
    d["year"] = d.year.astype(int); d["band"] = (d.year // 5) * 5
    d["yr_c"] = (d.year - d.year.mean()) / 10
    for m in list(PRED) + DESC:
        d["z_" + m] = (d[m] - d[m].mean()) / d[m].std()
    both = d.groupby("artist_key").rs.agg(["sum", "count"])
    keep = both[(both["sum"] >= 1) & (both["sum"] < both["count"])].index
    w = d[d.artist_key.isin(keep)].copy()
    res = {"n_songs": int(len(d)), "n_acclaimed": int(d.rs.sum()),
           "within": {"n_artists": int(len(keep)), "n_songs": int(len(w)), "n_acclaimed": int(w.rs.sum())},
           "measures": {}}
    cov = None
    try:
        cov = pd.read_csv(COV)
        d = d.merge(cov, on=["song_key", "artist_key"], how="left")
        res["covers_matched"] = int(d.n_cover_artists.notna().sum())
    except FileNotFoundError:
        pass
    raw_p = {}
    for m in list(PRED) + DESC:
        z = "z_" + m; quad = PRED.get(m) == "U"
        X1 = w[[z, "logn", "yr_c"]].copy()
        if quad:
            X1[z + "2"] = X1[z] ** 2
        f1 = ConditionalLogit(w.rs, X1, groups=w.artist_key).fit(disp=0)
        X2 = pd.get_dummies(d[["band"]].astype(str), drop_first=True, dtype=float)
        X2[z] = d[z]; X2["logn"] = d.logn; X2["rank"] = d["rank"] / 100
        if quad:
            X2[z + "2"] = d[z] ** 2
        X2 = sm.add_constant(X2)
        f2 = sm.Logit(d.rs, X2).fit(disp=0, cov_type="cluster", cov_kwds={"groups": pd.factorize(d.artist_key)[0]})
        key = z + "2" if quad else z
        r = {"within_coef": float(f1.params[key]), "within_p": float(f1.pvalues[key]),
             "across_coef": float(f2.params[key]), "across_p": float(f2.pvalues[key]),
             "mean_acclaimed": float(d.loc[d.rs == 1, m].mean()), "mean_other": float(d.loc[d.rs == 0, m].mean())}
        if quad:
            b1, b2 = f1.params[z], f1.params[z + "2"]
            peak_z = -b1 / (2 * b2) if b2 != 0 else float("nan")
            r["peak_raw"] = float(d[m].mean() + peak_z * d[m].std())
            r["peak_inside"] = bool(d[z].quantile(.05) < peak_z < d[z].quantile(.95))
            r["linear_within_coef"] = float(b1)
        if cov is not None:
            c = d[d.n_cover_artists.notna()].copy()
            c["y"] = np.log1p(c.n_cover_artists)
            cnt = c.artist_key.value_counts(); c = c[c.artist_key.isin(cnt[cnt >= 2].index)]
            X3 = pd.get_dummies(c[["artist_key"]], drop_first=True, dtype=float)
            X3[z] = c[z]; X3["logn"] = c.logn; X3["yr_c"] = c.yr_c
            if quad:
                X3[z + "2"] = c[z] ** 2
            X3 = sm.add_constant(X3)
            f3 = sm.OLS(c.y.values, X3.values).fit()
            ix = list(X3.columns).index(key)
            r["covers_coef"] = float(f3.params[ix]); r["covers_p"] = float(f3.pvalues[ix])
            r["covers_n"] = int(len(c))
        res["measures"][m] = r
        if m in PRED:
            raw_p[m] = r["within_p"]
    names = list(raw_p); adj = holm([raw_p[k] for k in names])
    for k, a in zip(names, adj):
        r = res["measures"][k]; r["within_p_holm"] = a
        sign = -1 if PRED[k] == "U" else PRED[k]
        ok1 = np.sign(r["within_coef"]) == sign and a < 0.05
        ok2 = np.sign(r["across_coef"]) == sign
        if PRED[k] == "U":
            ok1 = ok1 and r.get("peak_inside", False)
        rev = np.sign(r["within_coef"]) == -sign and r["within_p"] < 0.05
        verdict = "passes" if (ok1 and ok2) else ("reversed" if rev else "unsettled")
        if verdict == "passes" and "covers_coef" in r:
            one = r["covers_p"] / 2 if np.sign(r["covers_coef"]) == sign else 1
            if one < 0.05:
                verdict = "confirmed"
        r["verdict"] = verdict
    json.dump(res, open(OUT, "w"), indent=1)
    print(f"songs {res['n_songs']} acclaimed {res['n_acclaimed']} within: {res['within']}")
    for m, r in res["measures"].items():
        print(f"{m:18s} within {r['within_coef']:+.3f} p={r['within_p']:.4f} holm={r.get('within_p_holm', float('nan')):.3f}"
              f" | across {r['across_coef']:+.3f} p={r['across_p']:.4f}"
              + (f" | covers {r['covers_coef']:+.3f} p={r['covers_p']:.3f}" if 'covers_coef' in r else "")
              + f" | {r.get('verdict', 'desc')}  acc {r['mean_acclaimed']:.3f} oth {r['mean_other']:.3f}")


if __name__ == "__main__":
    main()
