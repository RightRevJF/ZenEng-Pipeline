"""PREDICTION_deduce.md: pop 3/4 = standard 3/4 x pop 4/4 / standard 4/4, checked on four countable figures.  python3 studies/other_metres/deduce_check.py -> deduce_check.json"""
import os, sys, json, gzip, glob, collections
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "lib", "luthier")]
import numpy as np, atlas_build as AB, tables_3_4 as T34, make_leadsheet_table as MK, hooktheory_tables as HT
FIG = ("notes a bar", "onsets on the beat", "onsets on the bar's first beat", "bars on a rhythm already sung")
def lead(path): x = T34.one(path); return None if x is None else {**AB.readings(x["ns"], T34.BL, T34.BEATS, 12), **MK.structure(x["ns"], T34.BL)}
def leadsheets(M, BL, BEATS):
    T34.M = M; T34.BL = BL; T34.BEATS = BEATS
    with Pool(2) as pool: return [x for x in pool.map(lead, sorted(glob.glob("/home/claude/corpus/choco/partitions/wikifonia/raw/*.mxl")), chunksize=20) if x]
def hook(D, want, BL, BEATS):
    songs = collections.defaultdict(list)
    for k, x in D.items():
        m = x["annotations"]["meters"]
        if len(m) != 1 or (m[0]["beats_per_bar"], m[0]["beat_unit"]) != want or "MELODY" not in x["tags"] or HT.left_out(x["hooktheory"]): continue
        ns = HT.clip_notes(x, 12)
        if ns: songs[(x["hooktheory"]["artist"], x["hooktheory"]["song"])].append(ns)
    rows = []
    for key, clips in songs.items():
        allns = []; shift = 0
        for ns in clips:
            b0 = ns[0][0] // BL; ns = [[on - b0 * BL + shift, d, p] for on, d, p in ns]; shift = (ns[-1][0] // BL + 2) * BL; allns += ns
        if len(allns) >= 24: rows.append({**AB.readings(allns, BL, BEATS, 12), **MK.structure(allns, BL)})
    return rows
def med(rows): return {f: float(np.median([r[f] for r in rows])) for f in FIG}
def quart(rows): return {f: [float(q) for q in np.percentile([r[f] for r in rows], (25, 50, 75))] for f in FIG}
if __name__ == "__main__":
    D = json.load(gzip.open(HT.SRC)); B4 = [0, 12, 24, 36]; B3 = [0, 12, 24]
    std34 = leadsheets("3/4", 36, B3); std44 = leadsheets("4/4", 48, B4); pop44 = hook(D, (4, 4), 48, B4); pop34 = hook(D, (3, 4), 36, B3)
    KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]; bb = {f: float(np.median([r[KR["names"].index(f)] for r in KR["rows"]])) for f in FIG}
    a, b, c = med(std34), med(pop44), med(std44); cq = quart(pop34); out = dict(songs=dict(standard_3_4=len(std34), standard_4_4=len(std44), pop_4_4=len(pop44), pop_3_4=len(pop34)), medians=dict(standard_3_4=a, pop_4_4=b, standard_4_4=c, pop_4_4_Billboard=bb), counted_pop_3_4=cq, figures={})
    errs = []
    for f in FIG:
        pred = a[f] * b[f] / c[f]; lo, md, hi = cq[f]; e = abs(pred - md) / (hi - lo); errs.append(e); predbb = a[f] * bb[f] / c[f]
        out["figures"][f] = dict(predicted=round(pred, 3), counted_median=round(md, 3), counted_middle_half=[round(lo, 3), round(hi, 3)], inside=bool(lo <= pred <= hi), style_factor_in_4_4=round(b[f] / c[f], 3), sign_right=bool((pred - a[f]) * (md - a[f]) > 0), error_over_width=round(e, 3), predicted_with_Billboard_pop=round(predbb, 3))
        print(f, out["figures"][f])
    out["median_error_over_width"] = round(float(np.median(errs)), 3); out["passes"] = bool(all(v["inside"] and v["sign_right"] for v in out["figures"].values()) and out["median_error_over_width"] < 0.5)
    print(out["songs"], out["median_error_over_width"], out["passes"]); json.dump(out, open(os.path.join(HERE, "deduce_check.json"), "w"), indent=1)
