"""Stage 2b (PDMX, public-domain MuseScore scores, CC0 / public domain): an intensity curve per score from its MIDI, per bar:
the top line's mean pitch, note onsets, notes struck together, and velocity, each standardised within the piece and averaged.
Sample: deduplicated scores with no licence conflict, 24 to 400 bars, at least one view; a random 12,000.
Q1 shared shape, Q2 types; Q3 log views (and rating among rated scores) against shape, controlling for genre, number of parts,
complexity, length, lyrics, official/pro/original flags, custom audio or video, and the song's fame (log number of PDMX scores
with the same song name)."""
import csv, json, sys, os, collections, random
import numpy as np, statsmodels.api as sm, mido
from multiprocessing import Pool
sys.path.insert(0, "/home/claude/shape")
import shape_lib as SL
P = "/home/claude/dl/shape/pdmx"; csv.field_size_limit(10 ** 9)
def bar_curve(path):
    try: mf = mido.MidiFile(path)
    except Exception: return None
    tpq = mf.ticks_per_beat; num, den = 4, 4; notes = []
    for tr in mf.tracks:
        t = 0
        for m in tr:
            t += m.time
            if m.type == "time_signature" and t == 0: num, den = m.numerator, m.denominator
            if m.type == "note_on" and m.velocity > 0 and getattr(m, "channel", 0) != 9: notes.append((t, m.note, m.velocity))
    if len(notes) < 32: return None
    bar = int(tpq * 4 * num / den)
    if bar <= 0: return None
    nb = max(n[0] for n in notes) // bar + 1
    if nb < 24 or nb > 400: return None
    by = collections.defaultdict(list)
    for t, p, v in notes: by[t // bar].append((t, p, v))
    top, ons, poly, vel = [], [], [], []
    for b in range(nb):
        ev = by.get(b, [])
        if not ev: top.append(np.nan); ons.append(0); poly.append(0); vel.append(np.nan); continue
        at = collections.defaultdict(list)
        for t, p, v in ev: at[t].append((p, v))
        top.append(np.mean([max(p for p, _ in g) for g in at.values()])); ons.append(len(at)); poly.append(np.mean([len(g) for g in at.values()])); vel.append(np.mean([v for _, _, v in ev]))
    def zf(a):
        a = np.array(a, float); m = np.nanmean(a) if np.isfinite(a).any() else 0; a = np.where(np.isnan(a), m, a); s = a.std(); return (a - a.mean()) / s if s > 0 else a * 0
    comps = [zf(top), zf(ons), zf(poly), zf(vel)]
    return dict(curve=list(np.mean(comps, 0)), comps=[list(c) for c in comps], bars=nb)
def work(row):
    c = bar_curve(os.path.join(P, "ext", row["mid"].lstrip("./")))
    return (row, c)
if __name__ == "__main__":
    rows = list(csv.DictReader(open(f"{P}/PDMX.csv", encoding="utf-8")))
    name_count = collections.Counter((r["song_name"] or "").strip().lower() for r in rows)
    pool_rows = [r for r in rows if r["subset:deduplicated"] == "True" and r["subset:no_license_conflict"] == "True" and r["n_views"] not in ("", "NA") and int(float(r["n_views"])) > 0
                 and r["song_length.bars"] not in ("", "NA") and 24 <= float(r["song_length.bars"]) <= 400 and r["mid"] not in ("", "NA")]
    SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 20261115; random.seed(SEED); sample = random.sample(pool_rows, min(12000, len(pool_rows)))
    print("pool", len(pool_rows), "sample", len(sample))
    with Pool(2) as pool: got = [x for x in pool.map(work, sample, chunksize=50) if x[1]]
    print("curves", len(got))
    curves = [c["curve"] for _, c in got]; meta = [r for r, _ in got]
    N, K = 100, 10
    R = SL.raw_matrix(curves, N, K); X = np.array([SL.standardise(x) for x in R])
    sub = np.random.default_rng(3).choice(len(curves), min(3000, len(curves)), replace=False)
    q1 = SL.shared_shape([curves[i] for i in sub], N, K, reps=100); q2 = SL.types_test(R[sub], dims=6, reps=30)
    sv = SL.svd_modes(X, 4)
    peak = np.array([np.argmax(x) / (N - 1) for x in R]); thirds = np.array([x[67:].mean() - x[:33].mean() for x in X])
    def fnum(r, k):
        try: return float(r[k])
        except (ValueError, TypeError): return 0.0
    genres = collections.Counter((r["genres"] or "NA").split(",")[0] for r in meta); topg = [g for g, _ in genres.most_common(12)]
    C = [[1.0 if (r["genres"] or "NA").split(",")[0] == g else 0.0 for r in meta] for g in topg[1:]]
    C += [[fnum(r, k) for r in meta] for k in ("n_tracks", "complexity", "song_length.bars", "notes_per_bar")]
    C += [[1.0 if r[k] == "True" else 0.0 for r in meta] for k in ("has_lyrics", "is_official", "is_user_pro", "is_original", "has_custom_audio", "has_custom_video")]
    C += [[np.log(name_count[(r["song_name"] or "").strip().lower()]) for r in meta]]
    S = [sv["scores"][:, j] for j in range(4)] + [peak, thirds]; labs = ["mode1", "mode2", "mode3", "mode4", "peak_pos", "last_minus_first_third"]
    def zc(M):
        M = np.asarray(M, float).T; s = M.std(0); keep = s > 0; M = M[:, keep]; return (M - M.mean(0)) / M.std(0)
    def model(y, idx):
        y = np.asarray(y, float)[idx]; y = (y - y.mean()) / y.std()
        A0 = sm.add_constant(zc([np.asarray(c)[idx] for c in C])); A1 = sm.add_constant(np.column_stack([A0[:, 1:], zc([np.asarray(s)[idx] for s in S])]))
        m0 = sm.OLS(y, A0).fit(); m1 = sm.OLS(y, A1).fit(); m1r = sm.OLS(y, A1).fit(cov_type="HC3"); nC = A0.shape[1] - 1
        return dict(n=int(len(y)), r2_controls=float(m0.rsquared), r2_with_shape=float(m1.rsquared), delta_r2=float(m1.rsquared - m0.rsquared), f_p=float(m1.compare_f_test(m0)[1]),
                    terms={lab: dict(beta=float(m1r.params[1 + nC + i]), p=float(m1r.pvalues[1 + nC + i])) for i, lab in enumerate(labs)})
    allidx = np.arange(len(meta)); rated = np.array([i for i, r in enumerate(meta) if fnum(r, "n_ratings") >= 3])
    res = dict(pool=len(pool_rows), n=len(curves), q1=q1, q2=q2, mode_share=[float(v) for v in sv["share"]], mean_curve=[float(v) for v in sv["mean"]],
               modes=[[float(v) for v in m] for m in sv["modes"]], peak_pos_median=float(np.median(peak)), peak_in_last_third=float(np.mean(peak >= 2 / 3)),
               views=model(np.log([fnum(r, "n_views") for r in meta]), allidx),
               favorites=model(np.log1p([fnum(r, "n_favorites") for r in meta]), allidx),
               rating=model([fnum(r, "rating") for r in meta], rated) if len(rated) > 200 else None)
    json.dump(res, open("/home/claude/shape/pdmx_results.json" if SEED == 20261115 else f"/home/claude/shape/pdmx_results_{SEED}.json", "w"), indent=1, default=float)
    print("Q1", {k: round(v, 3) for k, v in q1.items()}); print("Q2", q2["types_found"], q2["k_supported"], {k: (round(v["silhouette"], 3), round(v["null95"], 3), round(v["stability_ari"], 2)) for k, v in q2["by_k"].items()})
    print("modes", [round(v, 3) for v in sv["share"]], "peak median", round(res["peak_pos_median"], 2), "last third", round(res["peak_in_last_third"], 2))
    for k in ("views", "favorites", "rating"):
        v = res[k]
        if v: print(k, "n", v["n"], "R2 ctrl %.3f dR2 %.4f p %.3g" % (v["r2_controls"], v["delta_r2"], v["f_p"]), {t: (round(x["beta"], 3), round(x["p"], 4)) for t, x in v["terms"].items()})
