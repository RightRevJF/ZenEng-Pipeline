"""PREDICTION_6_8.md: why song 52's builds die and where the living stand off.  python3 studies/other_metres/read_6_8.py -> read_6_8.json"""
import os, sys, json, glob, random, collections
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, luthier_judge7 as J7, atlas_build as AB, tables_3_4 as T34, make_leadsheet_table as MK
def engine(stem):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); spec = json.loads(json.dumps(rec["spec"])); E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"), clash=None, relocate=False)[0]; return L, spec, E
def land(E, spec):
    """840: for each title line, the kept two-bar windows of its syllable count (and with one or two pickups): the share, by kept count, in which half or more of its stressed syllables fall on a beat, and in which all do"""
    out = {}; W = E.ALLW[0] if getattr(E, "ALLW", None) else E.WIN
    for h in spec.get("hooks", ()):
        sec, i = h.rsplit(":", 1); sy = E.LINES[sec][int(i)]; n = len(sy); st = [k for k, x in enumerate(sy) if x[1]]; lead = next((k for k, x in enumerate(sy) if x[1]), n); tot = half = full = 0.0; nw = 0
        for p in sorted({0, min(1, lead), min(2, lead)}):
            for w, c in W.get(n - p, []):
                if w[0] != 0 and p > 0: continue
                ons = [-6 * (p - j) for j in range(p)] + list(w); ob = [E.on_beat(ons[k]) for k in st]; tot += c; nw += 1; half += c * (np.mean(ob) >= 0.5); full += c * all(ob)
        out[h] = dict(line=" ".join(dict.fromkeys(x[0] for x in sy)), syllables=n, stressed=len(st), slot_bars=E.SLOTS[sec][int(i)], windows=nw, half_or_more_on_a_beat=round(half / tot, 3) if tot else None, all_on_a_beat=round(full / tot, 3) if tot else None)
    return out
def wiki68(path):
    x = T34.one(path); return None if x is None else {**AB.readings(x["ns"], 36, [0, 18], 18), **MK.structure(x["ns"], 36)}
if __name__ == "__main__":
    out = {}; L, spec, E = engine("songs/p62/lyric52"); rng = random.Random(L.get("seed", 1)); deaths = collections.Counter(); hook_share = collections.defaultdict(list); lifts = []; onb = []; living = []; hooks = set(spec.get("hooks", ()))
    for _ in range(1000):
        c, err = E.build(rng)
        if err: deaths["build: " + str(err[0])] += 1; continue
        ns = c["notes"]; g = E.gates(c); v_ = [n["p"] for n in ns if E.KIND[n["sec"]] == "Verse"]; c_ = [n["p"] for n in ns if E.KIND[n["sec"]] == "Chorus"]; lifts.append(float(np.median(c_) - np.median(v_))); st = [n for n in ns if n["stress"]]; onb.append(float(np.mean([E.on_beat(n["on"]) for n in st])))
        for h in hooks:
            s_, i_ = h.rsplit(":", 1); hs = [n for n in ns if n["stress"] and n["sec"] == s_ and n["line"] == int(i_)]
            if hs: hook_share[h].append(float(np.mean([E.on_beat(n["on"]) for n in hs])))
        if g: deaths[g] += 1; continue
        living.append(E.readings(sorted(E.as_sung(ns), key=lambda n: n["on"])))
    out["song 52"] = dict(builds=1000, living=len(living), deaths=dict(deaths), title_lines_stressed_on_a_beat_quartiles={h: [round(float(q), 3) for q in np.percentile(v, (25, 50, 75))] for h, v in hook_share.items()}, title_lines_under_half_share={h: round(float(np.mean(np.array(v) < 0.5)), 3) for h, v in hook_share.items()},
                           lift_quartiles=[round(float(q), 2) for q in np.percentile(lifts, (10, 25, 50, 75, 90))], plan_lift=spec["plan"]["lift"], lift_within_two_share=round(float(np.mean(np.abs(np.array(lifts) - spec["plan"]["lift"]) <= 2)), 3), stressed_on_a_beat_quartiles=[round(float(q), 3) for q in np.percentile(onb, (25, 50, 75))], floor_731=spec.get("stressed on the beat, at least", 0.4), a_place_to_land=land(E, spec))
    print(json.dumps(out["song 52"], indent=0)[:3000], flush=True)
    L5, spec5, E5 = engine("songs/p65/lyric55"); out["song 55 (4/4)"] = dict(a_place_to_land=land(E5, spec5)); print(json.dumps(out["song 55 (4/4)"]), flush=True)
    T34.M = "6/8"; T34.BL = 36; T34.BEATS = [0, 18]
    with Pool(2) as pool: W = [x for x in pool.map(wiki68, sorted(glob.glob("/home/claude/corpus/choco/partitions/wikifonia/raw/*.mxl")), chunksize=20) if x]
    KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["6-8_sung"]; J = J7.Judge7("6-8_sung"); rd = {}
    for nm in J.names:
        es = [r[KR["names"].index(nm)] for r in KR["rows"]]; wk = [w[nm] for w in W]; lv = [x[nm] for x in living]; e = [float(q) for q in np.percentile(es, (25, 50, 75))]; w = [float(q) for q in np.percentile(wk, (25, 50, 75))]; m = float(np.median(lv))
        rd[nm] = dict(living_median=round(m, 3), Essen_25_50_75=[round(q, 3) for q in e], lead_sheets_25_50_75=[round(q, 3) for q in w], outside_Essen=bool(not e[0] <= m <= e[2]), outside_lead_sheets=bool(not w[0] <= m <= w[2]))
    out["where the living stand"] = dict(living=len(living), Essen_tunes=len(KR["rows"]), lead_sheets=len(W), readings=rd)
    for k, v in rd.items(): print(f"{k:34} {v}")
    json.dump(out, open(os.path.join(HERE, "read_6_8.json"), "w"), indent=1)
