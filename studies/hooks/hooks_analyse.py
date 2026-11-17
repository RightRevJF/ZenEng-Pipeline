"""Chorus against verse inside the same song (Hooktheory clips from hooks_hooktheory.py): for every song with at least one chorus
clip and one verse clip, each feature's chorus mean minus its verse mean. Reports the median difference, the share of songs where
the chorus is higher, a sign test, and the chorus bands (25th, 50th, 75th percentiles) a v8 hook can be held to. Intro and
pre-chorus against verse the same way."""
import gzip, json, collections, math
import numpy as np
from scipy import stats
D = json.load(gzip.open("/home/claude/zeneng-pipeline/studies/hooks/hooks_clips.json.gz", "rt"))
F = ["density", "range", "mean_pitch", "i_entropy", "recurrence", "convention", "ic_mean", "h_mean", "top_cell_n", "top_cell_cover", "top_cell_pos", "up_rhythm", "up_pitch", "opens_down", "n", "beats"]
by = collections.defaultdict(lambda: collections.defaultdict(list))
for r in D: by[r["song"]][r["section"]].append(r)
def mean_of(rs, f):
    v = [r[f] for r in rs if r[f] is not None]; return float(np.mean(v)) if v else None
def paired(a, b):
    out = {}
    pairs = [(by[s][a], by[s][b]) for s in by if by[s][a] and by[s][b]]
    out["songs"] = len(pairs)
    for f in F:
        d = [mean_of(x, f) - mean_of(y, f) for x, y in pairs if mean_of(x, f) is not None and mean_of(y, f) is not None]
        d = np.array(d); pos = (d > 0).sum(); neg = (d < 0).sum()
        p = stats.binomtest(int(pos), int(pos + neg)).pvalue if pos + neg else None
        allv = np.array([r[f] for r in D if r[f] is not None and r["section"] in (a, b)]); iqr = np.subtract(*np.percentile(allv, [75, 25])) or 1
        out[f] = dict(median_diff=round(float(np.median(d)), 4), mean_diff=round(float(np.mean(d)), 4), higher_pct=round(100 * pos / max(1, pos + neg), 1),
                      ties_pct=round(100 * (len(d) - pos - neg) / max(1, len(d)), 1), p=p, effect_iqr=round(float(np.median(d) / iqr), 3), n=int(len(d)))
    return out
res = dict(clips=len(D), songs=len(by), sections=dict(collections.Counter(r["section"] for r in D)))
res["chorus_vs_verse"] = paired("chorus", "verse"); res["prechorus_vs_verse"] = paired("pre-chorus", "verse"); res["intro_vs_verse"] = paired("intro", "verse")
res["chorus_vs_prechorus"] = paired("chorus", "pre-chorus"); res["bridge_vs_chorus"] = paired("bridge", "chorus")
def bands(sec):
    out = {}
    for f in F:
        v = np.array([r[f] for r in D if r["section"] == sec and r[f] is not None], float)
        out[f] = [round(float(x), 3) for x in np.percentile(v, [10, 25, 50, 75, 90])]
    return out
res["bands"] = {s: bands(s) for s in ("chorus", "verse", "pre-chorus", "intro", "bridge")}
# uniqueness: censoring (no unique point by 17 notes)
for s in ("chorus", "verse", "intro"):
    v = [r["up_rhythm"] for r in D if r["section"] == s]; vp = [r["up_pitch"] for r in D if r["section"] == s]
    res.setdefault("unique_by", {})[s] = dict(rhythm_none=round(100 * np.mean([x is None for x in v]), 1), pitch_none=round(100 * np.mean([x is None for x in vp]), 1),
        rhythm_by6=round(100 * np.mean([x is not None and x <= 6 for x in v]), 1), rhythm_by8=round(100 * np.mean([x is not None and x <= 8 for x in v]), 1),
        pitch_by6=round(100 * np.mean([x is not None and x <= 6 for x in vp]), 1), pitch_by8=round(100 * np.mean([x is not None and x <= 8 for x in vp]), 1))
# the hook cell inside choruses
ch = [r for r in D if r["section"] == "chorus"]
res["chorus_cell"] = dict(returns_median=float(np.median([r["top_cell_n"] for r in ch])), returns_p25=float(np.percentile([r["top_cell_n"] for r in ch], 25)), returns_p75=float(np.percentile([r["top_cell_n"] for r in ch], 75)),
    first_in_first_quarter=round(100 * np.mean([r["top_cell_pos"] is not None and r["top_cell_pos"] < 0.25 for r in ch]), 1), cover_median=float(np.median([r["top_cell_cover"] for r in ch])))
json.dump(res, open("/home/claude/zeneng-pipeline/studies/hooks/hooks_hooktheory_results.json", "w"), indent=1)
for k in ("chorus_vs_verse", "prechorus_vs_verse", "intro_vs_verse", "bridge_vs_chorus"):
    print("==", k, res[k]["songs"])
    for f in F: x = res[k][f]; print("  %-14s med %+.3f  higher %5.1f%%  ties %4.1f%%  p %.2g  eff %+.2f" % (f, x["median_diff"], x["higher_pct"], x["ties_pct"], x["p"] if x["p"] is not None else 1, x["effect_iqr"]))
print(res["unique_by"]); print(res["chorus_cell"]); print(res["sections"])
