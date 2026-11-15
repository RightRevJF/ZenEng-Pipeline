"""Surprise against expectation and YouTube views (Hooktheory, 10,855 songs). Unit: the song's video. Clip measures are averaged
over a song's clips (weighted by events). Outcome: log views. Controls: log channel subscribers, video age (log days), duration,
music category, number of Hooktheory clips (a popularity proxy), and, in the strictest model, the artist (comparing songs by the
same artist). Measures: melody and chord surprise (mean IC), uncertainty (mean H), the Cheung term, their squares (inverted U),
within-clip repetition."""
import json, collections, re, datetime
import numpy as np, statsmodels.api as sm
S = json.load(open("/home/claude/shape/hooktheory_surprise.json"))
RH = {r["k"]: r for r in json.load(open("/home/claude/shape/hooktheory_rhythm.json"))}
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "long_rests_per_bar", "phrase_mean", "phrase_cv", "phrase_on_downbeat", "density", "length_variety"]
S = [dict(c, **{f: RH[c["k"]][f] for f in RF}) for c in S if c["k"] in RH]; Y = json.load(open("/home/claude/dl/shape/youtube/hooktheory_youtube.json"))
V, C = Y["videos"], Y["channels"]
by = collections.defaultdict(list)
for c in S: by[c["vid"]].append(c)
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF
def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or ""); return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else np.nan
rows = []
for vid, cs in by.items():
    v = V.get(vid)
    if not v or not v["views"]: continue
    sub = (C.get(v["channel"]) or {}).get("subscribers")
    if not sub: continue
    w = np.array([c["n_mel"] for c in cs], float)
    r = {f: float(np.average([c[f] for c in cs], weights=w)) for f in FE}
    pub = datetime.datetime.fromisoformat(v["published"].replace("Z", "+00:00"))
    r.update(vid=vid, artist=cs[0]["artist"], views=v["views"], subs=sub, age=(datetime.datetime(2026, 11, 15, tzinfo=datetime.timezone.utc) - pub).days, year=pub.year,
             dur=dur_s(v["duration"]), music=1.0 if v["category"] == "10" else 0.0, nclips=len(cs), nev=float(w.sum()))
    rows.append(r)
rows = [r for r in rows if r["age"] > 30 and np.isfinite(r["dur"]) and r["dur"] > 0]
print(len(rows), "songs with views and a public subscriber count")
y = np.log(np.array([r["views"] for r in rows], float))
ctrl = np.column_stack([np.log([r["subs"] for r in rows]), np.log([r["age"] for r in rows]), np.log([r["dur"] for r in rows]), [r["music"] for r in rows],
                        np.log([r["nclips"] for r in rows]), np.log([r["nev"] for r in rows])])
X = np.column_stack([[r[f] for r in rows] for f in FE])
def zc(M): M = np.asarray(M, float); s = M.std(0); s[s == 0] = 1; return (M - M.mean(0)) / s
Xz = zc(X); quad = np.column_stack([Xz[:, [0, 3]] ** 2, Xz[:, [FE.index("rhy_ic_mean"), FE.index("sync_per_note")]] ** 2]); names = FE + ["mel_ic^2", "ch_ic^2", "rhy_ic^2", "sync^2"]
def fit(yv, C_, P_, groups=None):
    yz = (yv - yv.mean()) / yv.std(); A0 = sm.add_constant(zc(C_)); A1 = sm.add_constant(np.column_stack([zc(C_), P_]))
    m0 = sm.OLS(yz, A0).fit(); m1 = sm.OLS(yz, A1).fit()
    mr = sm.OLS(yz, A1).fit(cov_type="cluster", cov_kwds={"groups": groups}) if groups is not None else sm.OLS(yz, A1).fit(cov_type="HC3")
    k = C_.shape[1]
    return dict(n=len(yz), r2_controls=float(m0.rsquared), r2_with=float(m1.rsquared), delta_r2=float(m1.rsquared - m0.rsquared), f_p=float(m1.compare_f_test(m0)[1]),
                terms={nm: dict(beta=float(mr.params[1 + k + i]), p=float(mr.pvalues[1 + k + i])) for i, nm in enumerate(names)})
art = np.array([r["artist"] for r in rows]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
res = {}
res["across_songs"] = fit(y, ctrl, np.column_stack([Xz, quad]), groups=g)
# within artist: demean everything by artist, artists with 2+ songs
cnt = collections.Counter(art); keep = np.array([cnt[a] >= 2 for a in art])
def demean(M, idx):
    M = np.asarray(M, float)[idx]; out = M.copy(); gg = g[idx]
    for a in np.unique(gg):
        s = gg == a; out[s] = M[s] - M[s].mean(0)
    return out
P = np.column_stack([Xz, quad])
res["within_artist"] = fit(demean(y, keep), demean(ctrl, keep), demean(P, keep), groups=g[keep])
res["within_artist"]["artists"] = int(len(set(art[keep])))
def block_gain(yv, C_, P_all, idx_r):
    yz = (yv - yv.mean()) / yv.std(); base = np.column_stack([zc(C_), np.delete(P_all, idx_r, axis=1)]); full = np.column_stack([zc(C_), P_all])
    m0 = sm.OLS(yz, sm.add_constant(base)).fit(); m1 = sm.OLS(yz, sm.add_constant(full)).fit(); return float(m1.rsquared - m0.rsquared), float(m1.compare_f_test(m0)[1])
ridx = [names.index(n) for n in RF + ["rhy_ic^2", "sync^2"]]
res["rhythm_block_across"] = block_gain(y, ctrl, P, ridx)
res["rhythm_block_within"] = block_gain(demean(y, keep), demean(ctrl, keep), demean(P, keep), ridx)
res["descr"] = dict(songs=len(rows), median_views=float(np.median([r["views"] for r in rows])), median_subs=float(np.median([r["subs"] for r in rows])))
json.dump(res, open("/home/claude/shape/rhythm_views_results.json", "w"), indent=1)
print("rhythm block adds: across %.4f (p %.3g), within artist %.4f (p %.3g)" % (*res["rhythm_block_across"], *res["rhythm_block_within"]))
for k in ("across_songs", "within_artist"):
    v = res[k]; print(k, "n", v["n"], "R2 controls %.3f, added by the note measures %.4f (F p %.3g)" % (v["r2_controls"], v["delta_r2"], v["f_p"]))
    for t, x in v["terms"].items(): print("   %-12s beta %+.3f  p %.4f" % (t, x["beta"], x["p"]))
