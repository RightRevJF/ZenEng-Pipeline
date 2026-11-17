"""Greatest-list songs (RS: chosen by artists, musicians and critics for Rolling Stone's 500 Greatest Songs) against ordinary Hot 100
songs (BB, CoCoPops Billboard sample), both transcribed by the same project, years 1958-1991. Per feature: medians, AUC (RS higher =
above 0.5) with a bootstrap interval, and a permutation p inside decades (labels shuffled within each decade, 5,000 times). Bands
(25th, 50th, 75th percentiles) are given for both groups."""
import json, collections
import numpy as np
R = json.load(open("/home/claude/zeneng-pipeline/studies/lyrics/lyrics_rows.json"))
R = [r for r in R if r["year"] and 1958 <= r["year"] <= 1991]
F = ["words", "lines", "words_per_line", "mattr", "repeated_lines", "zipf", "rare", "you", "i", "we", "third", "conc", "past", "time", "place", "propn", "nums",
     "valence", "valence_sd", "ending", "sad_end", "absolutes", "rhyme", "title_n", "narrativity"]
def z(v): v = np.array(v, float); return (v - np.nanmean(v)) / (np.nanstd(v) or 1)
for k in ("past", "time", "place", "propn", "third"):
    zz = z([r[k] for r in R])
    for r, x in zip(R, zz): r.setdefault("_z", []).append(x)
for r in R: r["narrativity"] = float(np.mean(r.pop("_z")))
def auc(a, b):
    a = np.array(a); b = np.array(b); gt = (a[:, None] > b[None, :]).mean(); eq = (a[:, None] == b[None, :]).mean(); return gt + 0.5 * eq
rng = np.random.default_rng(3); out = {}
dec = np.array([r["year"] // 10 for r in R]); grp = np.array([r["group"] == "RS" for r in R])
print("RS", grp.sum(), "BB", (~grp).sum())
for f in F:
    v = np.array([np.nan if r.get(f) is None else r[f] for r in R], float); ok = ~np.isnan(v)
    a, b = v[ok & grp], v[ok & ~grp]; A = auc(a, b)
    boots = [auc(rng.choice(a, len(a)), rng.choice(b, len(b))) for _ in range(1000)]
    # permutation within decade
    perm = []
    vv, gg, dd = v[ok], grp[ok], dec[ok]
    for _ in range(2000):
        g2 = gg.copy()
        for d in np.unique(dd):
            idx = np.where(dd == d)[0]; g2[idx] = rng.permutation(g2[idx])
        perm.append(auc(vv[g2], vv[~g2]))
    p = float((np.abs(np.array(perm) - 0.5) >= abs(A - 0.5)).mean())
    out[f] = dict(rs_median=float(np.median(a)), bb_median=float(np.median(b)), rs_band=[float(x) for x in np.percentile(a, [25, 50, 75])], bb_band=[float(x) for x in np.percentile(b, [25, 50, 75])],
                  auc=round(float(A), 3), ci=[round(float(x), 3) for x in np.percentile(boots, [2.5, 97.5])], p_within_decade=p, n=[int(len(a)), int(len(b))])
    print("%-15s RS %8.3f  BB %8.3f  AUC %.3f [%.3f, %.3f]  p %.3f" % (f, out[f]["rs_median"], out[f]["bb_median"], A, *out[f]["ci"], p))
json.dump(dict(n_rs=int(grp.sum()), n_bb=int((~grp).sum()), features=out), open("/home/claude/zeneng-pipeline/studies/lyrics/lyrics_results.json", "w"), indent=1)
json.dump(R, open("/home/claude/zeneng-pipeline/studies/lyrics/lyrics_rows_scored.json", "w"))
