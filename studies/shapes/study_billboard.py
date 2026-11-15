"""Stage 2 (Billboard, CoCoPops): (a) which note-level measures track what listeners felt (100 songs rated moment by moment for
arousal, with the audio's RMS level); (b) an intensity curve per song from those measures (214 songs with melody); Q1 shared shape,
Q2 types; (c) does shape relate to chart peak or weeks on the chart, with year and length as controls; (d) the structure test on all
739 songs (time to the first chorus, number of choruses)."""
import json, sys, collections
import numpy as np, statsmodels.api as sm
sys.path.insert(0, "/home/claude/shape")
import shape_lib as SL
B = json.load(open("/home/claude/shape/billboard_bars.json"))
def z(a):
    a = np.asarray(a, float); s = np.nanstd(a); return (a - np.nanmean(a)) / s if s > 0 else a * 0
def bar_table(song):
    bs = [b for b in song["bars"] if b["bar"] > 0]
    pitch = np.array([b["pitch"] if b["pitch"] is not None else np.nan for b in bs])
    voice = (~np.isnan(pitch)).astype(float)
    pf = np.where(np.isnan(pitch), np.nanmean(pitch) if voice.any() else 0, pitch)
    return bs, dict(pitch=z(pf), onsets=z([b["onsets"] for b in bs]), chords=z([b["chords"] for b in bs]), voice=voice - voice.mean())
res = {}
# (a) validation on the rated songs
rows = []
for k, s in B.items():
    if s["kind"] != "varms": continue
    bs, T = bar_table(s)
    ar = np.array([b["arousal"] if b["arousal"] is not None else np.nan for b in bs]); rms = np.array([b["rms"] if b["rms"] is not None else np.nan for b in bs])
    ok = ~np.isnan(ar) & ~np.isnan(rms)
    if ok.sum() < 16: continue
    arz, rmsz = z(ar[ok]), z(rms[ok])
    for i in np.where(ok)[0]:
        j = int(np.sum(ok[:i]))
        rows.append([arz[j], T["pitch"][i], T["onsets"][i], T["chords"][i], T["voice"][i], rmsz[j], i / len(bs)])
R = np.array(rows)
names = ["pitch", "onsets", "chords", "voice"]
m_sym = sm.OLS(R[:, 0], sm.add_constant(R[:, 1:5])).fit(cov_type="HC3")
m_rms = sm.OLS(R[:, 0], sm.add_constant(R[:, [5]])).fit()
m_time = sm.OLS(R[:, 0], sm.add_constant(R[:, [6]])).fit()
m_all = sm.OLS(R[:, 0], sm.add_constant(R[:, [1, 2, 3, 4, 5, 6]])).fit(cov_type="HC3")
res["validation"] = dict(bars=len(R), songs=sum(1 for s in B.values() if s["kind"] == "varms"),
    symbolic=dict(r2=float(m_sym.rsquared), betas={n: float(b) for n, b in zip(names, m_sym.params[1:])}, p={n: float(p) for n, p in zip(names, m_sym.pvalues[1:])}),
    rms_only_r2=float(m_rms.rsquared), time_only_r2=float(m_time.rsquared), time_beta=float(m_time.params[1]), all_r2=float(m_all.rsquared))
W = {n: max(0.0, float(b)) for n, b in zip(names, m_sym.params[1:])}
print("validation:", json.dumps(res["validation"], indent=0)[:900])
# (b) intensity curves
songs = [(k, s) for k, s in B.items() if s["kind"] in ("hum", "varms") and s["meta"]]
curves, meta, raw = [], [], []
for k, s in songs:
    bs, T = bar_table(s)
    if len(bs) < 24: continue
    c = sum(W[n] * T[n] for n in names)
    curves.append(c); meta.append(s["meta"]); raw.append((k, bs))
N, K = 100, 10
Rm = SL.raw_matrix(curves, N, K); X = np.array([SL.standardise(x) for x in Rm])
q1 = SL.shared_shape(curves, N, K, reps=200); q2 = SL.types_test(Rm, dims=6, reps=40); sv = SL.svd_modes(X, 4)
peak = np.array([np.argmax(SL.dct_smooth(SL.resample(c, N), K)) / (N - 1) for c in curves])
thirds = np.array([x[67:].mean() - x[:33].mean() for x in X])
res["shape"] = dict(n=len(curves), q1=q1, q2=q2, mode_share=[float(v) for v in sv["share"]], mean_curve=[float(v) for v in sv["mean"]],
                    modes=[[float(v) for v in m] for m in sv["modes"]], peak_pos_median=float(np.median(peak)), peak_in_last_third=float(np.mean(peak >= 2 / 3)),
                    last_minus_first_third_mean=float(thirds.mean()))
print("Q1", {k: round(v, 3) for k, v in q1.items()}); print("Q2", q2["types_found"], q2["k_supported"], {k: (round(v["silhouette"], 3), round(v["null95"], 3), round(v["stability_ari"], 2)) for k, v in q2["by_k"].items()})
print("modes", [round(v, 3) for v in sv["share"]], "peak median", round(float(np.median(peak)), 2), "in last third", round(float(np.mean(peak >= 2/3)), 2))
# (c) outcome
def outcome_models(y, shape_cols, ctrl_cols, labels):
    yz = z(y); C = np.column_stack(ctrl_cols); S = np.column_stack(shape_cols)
    A0 = sm.add_constant(z_cols(C)); A1 = sm.add_constant(np.column_stack([z_cols(C), z_cols(S)]))
    m0 = sm.OLS(yz, A0).fit(); m1 = sm.OLS(yz, A1).fit(); m1r = sm.OLS(yz, A1).fit(cov_type="HC3")
    nC = C.shape[1]
    return dict(r2_controls=float(m0.rsquared), r2_with_shape=float(m1.rsquared), delta_r2=float(m1.rsquared - m0.rsquared), f_p=float(m1.compare_f_test(m0)[1]),
                terms={lab: dict(beta=float(m1r.params[1 + nC + i]), p=float(m1r.pvalues[1 + nC + i])) for i, lab in enumerate(labels)})
def z_cols(M):
    M = np.asarray(M, float); s = M.std(0); s[s == 0] = 1; return (M - M.mean(0)) / s
yr = np.array([m["year"] for m in meta], float); ln = np.array([len(c) for c in curves], float)
shape_cols = [sv["scores"][:, j] for j in range(4)] + [peak, thirds]; labs = ["mode1", "mode2", "mode3", "mode4", "peak_pos", "last_minus_first_third"]
res["outcome_shape"] = dict(
    peak_position=outcome_models(-np.log([m["peak"] for m in meta]), shape_cols, [yr, ln], labs),
    weeks=outcome_models(np.log([m["weeks"] for m in meta]), shape_cols, [yr, ln], labs))
for k, v in res["outcome_shape"].items(): print(k, "dR2 %.3f p %.3f" % (v["delta_r2"], v["f_p"]), {t: (round(x["beta"], 3), round(x["p"], 3)) for t, x in v["terms"].items()})
# (d) structure on all 739: time to the first chorus (share of the song), number of chorus sections, number of distinct section labels
st_rows = []
for k, s in B.items():
    if not s["meta"]: continue
    bs = [b for b in s["bars"] if b["bar"] > 0]
    if len(bs) < 16: continue
    labs_ = [str(b["label"] or "").lower() for b in bs]
    ch = [i for i, l in enumerate(labs_) if "chorus" in l and "pre" not in l]
    first_ch = ch[0] / len(bs) if ch else np.nan
    n_ch = sum(1 for i in range(len(labs_)) if "chorus" in labs_[i] and "pre" not in labs_[i] and (i == 0 or labs_[i - 1] != labs_[i]))
    ts = [b["t"] for b in bs if b["t"] is not None]
    secs_to_ch = (bs[ch[0]]["t"] - (ts[0] if ts else 0)) if ch and bs[ch[0]]["t"] is not None else np.nan
    st_rows.append(dict(k=k, first=first_ch, secs=secs_to_ch, n_ch=n_ch, has_ch=bool(ch), bars=len(bs), year=s["meta"]["year"], peak=s["meta"]["peak"], weeks=s["meta"]["weeks"]))
H = [r for r in st_rows if r["has_ch"] and not np.isnan(r["secs"])]
def st_model(yname, tr):
    y = np.array([tr(r[yname]) for r in H]); C = [np.array([r["year"] for r in H], float), np.array([r["bars"] for r in H], float)]
    S = [np.array([r["first"] for r in H]), np.array([r["secs"] for r in H]), np.array([r["n_ch"] for r in H], float)]
    return outcome_models(y, S, C, ["first_chorus_share", "seconds_to_first_chorus", "chorus_count"])
res["structure"] = dict(n_songs=len(st_rows), with_chorus=len(H), chorus_share=float(np.mean([r["has_ch"] for r in st_rows])),
                        median_seconds_to_chorus=float(np.median([r["secs"] for r in H])), median_chorus_count=float(np.median([r["n_ch"] for r in H])),
                        peak_position=st_model("peak", lambda v: -np.log(v)), weeks=st_model("weeks", np.log))
for k in ("peak_position", "weeks"):
    v = res["structure"][k]; print("structure", k, "dR2 %.3f p %.3f" % (v["delta_r2"], v["f_p"]), {t: (round(x["beta"], 3), round(x["p"], 3)) for t, x in v["terms"].items()})
print("songs", len(st_rows), "with chorus", len(H), "median s to chorus", res["structure"]["median_seconds_to_chorus"])
json.dump(res, open("/home/claude/shape/billboard_results.json", "w"), indent=1, default=float)
