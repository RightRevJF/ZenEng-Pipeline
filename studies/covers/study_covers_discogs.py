"""What predicts being covered: SHS100K version counts for the Hooktheory songs it lists (1,039 songs), against the same note measures
as the views study (melody, chord and rhythm surprise and uncertainty, the Cheung terms, repetition, syncopation, rests, phrases,
density, length variety). Controls: log YouTube views (the audience's channel), log channel subscribers, video age, duration,
music category, number of Hooktheory clips. Also: the same measures against views in the same 1,039 songs, to compare what
musicians re-record with what audiences watch. Only songs SHS100K sampled are here, so this compares songs that were covered more
with songs covered less, not covered with never covered."""
import json, collections, re, datetime
import numpy as np, statsmodels.api as sm
S = json.load(open("/home/claude/shape/hooktheory_surprise.json")); RH = {r["k"]: r for r in json.load(open("/home/claude/shape/hooktheory_rhythm.json"))}
Y = json.load(open("/home/claude/dl/shape/youtube/hooktheory_youtube.json")); V, C = Y["videos"], Y["channels"]
COV = json.load(open("/home/claude/shape/hooktheory_covers_discogs.json"))
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF
by = collections.defaultdict(list)
for c in S:
    if c["k"] in RH: by[c["vid"]].append(dict(c, **{f: RH[c["k"]][f] for f in RF}))
def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or ""); return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else np.nan
rows = []
for vid, cv in COV.items():
    cs = by.get(vid); v = V.get(vid)
    if not cs or not v or not v["views"]: continue
    sub = (C.get(v["channel"]) or {}).get("subscribers") or 1
    w = np.array([c["n_mel"] for c in cs], float); r = {f: float(np.average([c[f] for c in cs], weights=w)) for f in FE}
    pub = datetime.datetime.fromisoformat(v["published"].replace("Z", "+00:00"))
    r.update(vid=vid, artist=cs[0]["artist"], covers=cv["covers"], original=1.0, first_year=cv["first_year"], releases=cv["releases"], views=v["views"], subs=sub,
             age=max(31, (datetime.datetime(2026, 11, 15, tzinfo=datetime.timezone.utc) - pub).days), dur=dur_s(v["duration"]), music=1.0 if v["category"] == "10" else 0.0, nclips=len(cs))
    rows.append(r)
rows = [r for r in rows if np.isfinite(r["dur"]) and r["dur"] > 0 and r["first_year"]]
import sys
if "--originals" in sys.argv: rows = [r for r in rows if r["original"]]
print(len(rows), "songs with Discogs covers, notes, views and a first year")
def zc(M): M = np.asarray(M, float); s = M.std(0); s[s == 0] = 1; return (M - M.mean(0)) / s
X = zc(np.column_stack([[r[f] for r in rows] for f in FE]))
base_ctrl = np.column_stack([np.log([r["subs"] for r in rows]), np.log([r["age"] for r in rows]), np.log([r["dur"] for r in rows]), [r["music"] for r in rows], np.log([r["nclips"] for r in rows]), [r["first_year"] for r in rows]])
logv = np.log([r["views"] for r in rows]); logc = np.log1p([r["covers"] for r in rows]); logrel = np.log([r["releases"] for r in rows])
art = np.array([r["artist"] for r in rows]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
def fit(y, ctrl, P):
    yz = (y - y.mean()) / y.std(); A0 = sm.add_constant(zc(ctrl)); A1 = sm.add_constant(np.column_stack([zc(ctrl), P]))
    m0 = sm.OLS(yz, A0).fit(); m1 = sm.OLS(yz, A1).fit(); mr = sm.OLS(yz, A1).fit(cov_type="cluster", cov_kwds={"groups": g}); k = ctrl.shape[1]
    return dict(n=len(y), r2_controls=float(m0.rsquared), delta_r2=float(m1.rsquared - m0.rsquared), f_p=float(m1.compare_f_test(m0)[1]),
                terms={f: dict(beta=float(mr.params[1 + k + i]), p=float(mr.pvalues[1 + k + i])) for i, f in enumerate(FE)})
res = dict(n=len(rows), covers_median=float(np.median([r["covers"] for r in rows])), corr_covers_views=float(np.corrcoef(logc, logv)[0, 1]),
           covers=fit(logc, np.column_stack([base_ctrl, logv]), X), views=fit(logv, base_ctrl, X), releases=fit(logrel, np.column_stack([base_ctrl, logv]), X))
json.dump(res, open("/home/claude/shape/covers_discogs_results.json", "w"), indent=1)
print("log covers vs log views r = %.2f" % res["corr_covers_views"])
for k in ("covers", "views", "releases"):
    v = res[k]; print(k, "n", v["n"], "R2 controls %.3f, notes add %.4f (p %.3g)" % (v["r2_controls"], v["delta_r2"], v["f_p"]))
for f in FE:
    a, b, c2 = res["covers"]["terms"][f], res["views"]["terms"][f], res["releases"]["terms"][f]
    print("   %-20s covers %+.3f (p %.3f)   views %+.3f (p %.3f)   releases %+.3f (p %.3f)" % (f, a["beta"], a["p"], b["beta"], b["p"], c2["beta"], c2["p"]))
