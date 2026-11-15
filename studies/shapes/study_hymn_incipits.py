"""Stage 1a: the opening line of 5,000 hymn tunes (Hymnary.org export, top 5,000 tunes by published text-tune pairings).
Each incipit is a string of scale degrees (1-7, no octave, no rhythm). The octave of each note is taken as the nearest to the note
before (a leap of a fifth or more is read as the smaller step the other way), giving a diatonic contour. Questions:
  Q1 do opening lines share a shape (against the same notes shuffled)?
  Q2 do they fall into types (against a Gaussian continuum with the same covariance)?
  Q3 does the shape relate to how often the tune is printed (log Total Instances), beyond meter, length and range?"""
import csv, json, collections, sys
import numpy as np, statsmodels.api as sm
sys.path.insert(0, "/home/claude/shape")
import shape_lib as SL
SRC = "/home/claude/dl/shape/hymnary/tunes_top5000.csv"
def contour(inc):
    ds = [int(c) for c in inc if c in "1234567"]
    if len(ds) < 8: return None
    out = [0]
    for a, b in zip(ds, ds[1:]):
        step = (b - a) % 7
        if step > 3: step -= 7                                   # nearest: up to a fourth either way
        out.append(out[-1] + step)
    return out
rows = []
for r in csv.DictReader(open(SRC, encoding="utf-8")):
    c = contour(r["incipit"] or "")
    if c is None: continue
    rows.append(dict(n=int(r["totalInstances"]), c=c, meter=r["meter"] or "", key=r["tuneKey"] or "", title=r["tuneTitle"]))
print(len(rows), "tunes with an incipit of 8+ notes")
N, K = 16, 6
curves = [r["c"] for r in rows]
R = SL.raw_matrix(curves, N, K); X = np.array([SL.standardise(x) for x in R])
q1 = SL.shared_shape(curves, N, K, reps=200)
q2 = SL.types_test(R, dims=5, reps=40)
sv = SL.svd_modes(X, 4)
# simple shape features (relative time of the highest note, range, ending against start, turns)
def feats(c):
    c = np.array(c); top = np.argmax(c) / (len(c) - 1)
    turns = int(np.sum(np.diff(np.sign(np.diff(c))[np.diff(c) != 0]) != 0)) if len(c) > 2 else 0
    return dict(peak_pos=top, rng=c.max() - c.min(), end_minus_start=c[-1] - c[0], turns=turns / len(c), length=len(c))
F = [feats(r["c"]) for r in rows]
y = np.log([r["n"] for r in rows])
meters = collections.Counter(r["meter"] for r in rows); top_m = [m for m, _ in meters.most_common(15)]
def design(with_shape):
    cols = []; names = []
    for m in top_m[1:]: cols.append([1.0 if r["meter"] == m else 0.0 for r in rows]); names.append("meter=" + m)
    cols.append([1.0 if "Minor" in r["key"] else 0.0 for r in rows]); names.append("minor key")
    for f in ("length", "rng"): cols.append([x[f] for x in F]); names.append(f)
    if with_shape:
        for j in range(4): cols.append(list(sv["scores"][:, j])); names.append(f"mode{j+1}")
        for f in ("peak_pos", "end_minus_start", "turns"): cols.append([x[f] for x in F]); names.append(f)
    A = np.array(cols).T; keep = A.std(0) > 0                      # drop constant columns (e.g. a key mode never named)
    A = A[:, keep]; names = [n for n, k_ in zip(names, keep) if k_]; A = (A - A.mean(0)) / A.std(0)
    return sm.add_constant(A), names
yz = (y - y.mean()) / y.std()
A0, n0 = design(False); m0 = sm.OLS(yz, A0).fit(cov_type="HC3")
A1, n1 = design(True); m1 = sm.OLS(yz, A1).fit(cov_type="HC3")
shape_terms = {nm: dict(beta=float(m1.params[i + 1]), p=float(m1.pvalues[i + 1])) for i, nm in enumerate(n1) if nm.startswith("mode") or nm in ("peak_pos", "end_minus_start", "turns")}
ftest = sm.OLS(yz, A1).fit().compare_f_test(sm.OLS(yz, A0).fit())
res = dict(n=len(rows), N=N, K=K, q1=q1, q2=q2, mode_share=[float(x) for x in sv["share"]], mean_curve=[float(x) for x in sv["mean"]],
           modes=[[float(v) for v in m] for m in sv["modes"]],
           outcome=dict(r2_controls=float(m0.rsquared), r2_with_shape=float(m1.rsquared), delta_r2=float(m1.rsquared - m0.rsquared),
                        f_test_p=float(ftest[1]), shape_terms=shape_terms),
           peak_pos_mean=float(np.mean([x["peak_pos"] for x in F])), instances_median=float(np.median([r["n"] for r in rows])))
json.dump(res, open("/home/claude/shape/hymn_incipits.json", "w"), indent=1)
print("Q1 shared shape:", {k: round(v, 3) for k, v in q1.items()})
print("Q2 types:", q2["types_found"], q2["k_supported"], {k: (round(v["silhouette"], 3), round(v["null95"], 3), round(v["stability_ari"], 2)) for k, v in q2["by_k"].items()})
print("mode shares", [round(x, 3) for x in sv["share"]])
print("R2 controls %.4f  with shape %.4f  delta %.4f  F p %.3g" % (m0.rsquared, m1.rsquared, m1.rsquared - m0.rsquared, ftest[1]))
for k, v in shape_terms.items(): print("  ", k, round(v["beta"], 3), "p", round(v["p"], 4))
print("mean curve", [round(x, 2) for x in sv["mean"]])
