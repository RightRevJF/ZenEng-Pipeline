"""The maintainer's request (1): the session's join and the maintainer's, song by song, to find why iyou_rate moves from p .002 to .30.
Reads numbers only: the session's covers_join.csv + covers_feat.csv, and the maintainer's check_repro.py output rebuilt here
(maint_feat.csv, from studies/covers/discogs_cliques.py run on the same Discogs-VI main.zip). Writes compare.json here."""
import json, os, hashlib, numpy as np, pandas as pd, statsmodels.api as sm
L = "/home/claude/lyr_dl/"; OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "compare.json")
mine = pd.read_csv(L + "covers_join.csv").merge(pd.read_csv(L + "covers_feat.csv"), on="id"); mine = mine[mine.matched == 1]
c = mine.groupby("writer").size(); mine = mine[mine.writer.isin(c[c >= 10].index)].copy()
th = pd.read_csv(L + "maint_feat.csv"); c = th.groupby("writer").size(); th = th[th.writer.isin(c[c >= 10].index)].copy()
for d in (mine, th): d["year"] = pd.to_numeric(d.year, errors="coerce")
def fit(x, m="iyou_rate", y="n_artists", yr="year"):
    x = x[x[m].notna() & x[yr].notna()].copy(); c = x.groupby("writer").writer.transform("size"); x = x[c >= 2]
    x["y"] = np.log(x[y]); x["logn"] = np.log(x.n_words); x["yr"] = (x[yr] - x[yr].mean()) / 10; x["z"] = (x[m] - x[m].mean()) / x[m].std()
    cols = ["y", "z", "logn", "yr"]; dm = x[cols] - x.groupby("writer")[cols].transform("mean")
    f = sm.OLS(dm.y, dm[["z", "logn", "yr"]]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.writer)[0]})
    return dict(coef=round(float(f.params["z"]), 4), p=round(float(f.pvalues["z"]), 4), n=int(len(x)), writers=int(x.writer.nunique()))
key = ["writer", "title"]
both = mine.merge(th, on=key, suffixes=("_s", "_m"))
res = {"session": dict(songs=len(mine), writers=int(mine.writer.nunique())), "maintainer": dict(songs=len(th), writers=int(th.writer.nunique())),
       "overlap": dict(songs=len(both), writers=int(both.writer.nunique()), same_wasabi_row=round(float((both.id_s == both.id_m).mean()), 3),
                       r_log_artists=round(float(np.corrcoef(np.log(both.n_artists_s), np.log(both.n_artists_m))[0, 1]), 3),
                       artists_equal=round(float((both.n_artists_s == both.n_artists_m).mean()), 3),
                       median_ratio_artists=round(float((both.n_artists_m / both.n_artists_s).median()), 3),
                       year_equal=round(float((both.year_s == both.year_m).mean()), 3),
                       iyou_equal=round(float(np.isclose(both.iyou_rate_s, both.iyou_rate_m).mean()), 3)),
       "only_session": int(len(mine) - len(both)), "only_maintainer": int(len(th) - len(both)), "fits": {}}
F = res["fits"]
F["session, all"] = fit(mine); F["maintainer, all"] = fit(th)
o = both.copy()
for side in ("s", "m"):                                   # the overlap, each side's own features, outcome and year
    x = o[["writer", "n_words_" + side, "iyou_rate_" + side, "n_artists_" + side, "year_" + side]].copy(); x.columns = ["writer", "n_words", "iyou_rate", "n_artists", "year"]
    F[f"overlap, {'session' if side == 's' else 'maintainer'}'s everything"] = fit(x)
x = o[["writer", "n_words_s", "iyou_rate_s", "n_artists_m", "year_s"]].copy(); x.columns = ["writer", "n_words", "iyou_rate", "n_artists", "year"]; F["overlap, session's features and year, maintainer's artists"] = fit(x)
x = o[["writer", "n_words_s", "iyou_rate_s", "n_artists_s", "year_m"]].copy(); x.columns = ["writer", "n_words", "iyou_rate", "n_artists", "year"]; F["overlap, session's, maintainer's year"] = fit(x)
os_ = mine.merge(th[key], on=key, how="left", indicator=True); os_ = os_[os_._merge == "left_only"]; F["session only"] = fit(os_)
om = th.merge(mine[key], on=key, how="left", indicator=True); om = om[om._merge == "left_only"]; F["maintainer only"] = fit(om)
for m in ("i_rate", "you_lines", "syl_line"):
    F[f"{m}: session, all"] = fit(mine, m); F[f"{m}: maintainer, all"] = fit(th, m)
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res, indent=1))
