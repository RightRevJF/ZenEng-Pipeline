"""Fix 860: the kept songs' readings one song a row, so a judge can read a candidate against the kept songs jointly and not one reading at a time.
4/4 pop from the 159 kept songs; 6/8 and 3/4 from the Essen tunes the metre atlas was built from."""
import sys, json, numpy as np
sys.path[:0] = ["/home/claude/rightrevjf/zeneng-pipeline/tables/metre_atlas", "/home/claude/zeneng/corpus/v20"]
import atlas_build as AB
sys.path.insert(0, "/home/claude/rightrevjf/zeneng-pipeline/lib/luthier"); import scaling as SC
def structure(ns, barlen):
    """864: how much of a song comes back: bars whose rhythm, and bars whose rhythm and pitch moves, were already sung"""
    bars = {}
    for on, d, p in ns: bars.setdefault(on // barlen, []).append((on % barlen, p))
    seen_r = set(); seen_f = set(); r = f = 0; keys = sorted(bars)
    for k in keys:
        v = bars[k]; rh = tuple(x for x, _ in v); fig = (rh, tuple(b[1] - a[1] for a, b in zip(v, v[1:])))
        r += rh in seen_r; f += fig in seen_f; seen_r.add(rh); seen_f.add(fig)
    return {"bars on a rhythm already sung": r / len(keys), "bars on a figure already sung": f / len(keys)}
out = {}
import bench as B
K = B.kept(); rows = []
for k in K:
    ns = [[t, 6, p] for t, p, _ in k["notes"] if t % 3 == 0]; sc = SC.series([(x[0], x[2]) for x in ns]); a_ = SC.dfa(sc["pitch"]); b_ = SC.dfa(sc["onsets on the grid"]); rows.append({**AB.readings(ns, 48, [0, 12, 24, 36], 12), **structure(ns, 48), "pitch scaling": a_["alpha"], "rhythm scaling": b_["alpha"]})
names = sorted(rows[0]); out["4-4_pop_sung"] = dict(names=names, rows=[[round(float(r[n]), 5) for n in names] for r in rows], songs=len(rows), source="the 159 kept CoCoPops Billboard songs")
for m in ("6/8", "3/4"):
    barlen, beats, beat, kind = AB.METRES[m]; rows = []
    for abc in AB.tunes(m, "sung"):
        try: ns = AB.notes_of(abc, barlen)
        except Exception: ns = None
        if ns: rows.append({**AB.readings(ns, barlen, beats, beat), **structure(ns, barlen)})
    names = sorted(rows[0]); out[m.replace("/", "-") + "_sung"] = dict(names=names, rows=[[round(float(r[n]), 5) for n in names] for r in rows], songs=len(rows), source="Essen folk-song collection (music21)"); print(m, len(rows), flush=True)
json.dump(out, open("/home/claude/rightrevjf/zeneng-pipeline/tables/metre_atlas/kept_readings.json", "w"))
for t, v in out.items():                                                                 # the two new readings' quartiles into each kept table
    pth = f"/home/claude/rightrevjf/zeneng-pipeline/tables/metre_atlas/{t}.json"; T = json.load(open(pth))
    for n in [x for x in ("bars on a rhythm already sung", "bars on a figure already sung", "pitch scaling", "rhythm scaling") if x in v["names"]]:
        j = v["names"].index(n); T["readings_quartiles"][n] = [float(x) for x in np.percentile([r[j] for r in v["rows"]], (25, 50, 75))]
    json.dump(T, open(pth, "w")); print({k: v["songs"] for k, v in out.items()})
