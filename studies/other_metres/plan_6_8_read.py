"""PREDICTION_plan_6_8.md: the plan-form record of song 52 read.  python3 studies/other_metres/plan_6_8_read.py RECORD.song.json -> plan_6_8.json"""
import os, sys, json, glob, random, collections
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, atlas_build as AB, tables_3_4 as T34, read_6_8 as R68
if __name__ == "__main__":
    R = json.load(open(sys.argv[1])); L = json.load(open(os.path.join(ROOT, "songs", "p62", "lyric52.json"))); sp = R["spec"]; m = R["melody"]; j = R["judge7"]; ns = sorted([[n["on"], n["dur"], n["midi"]] for n in m["notes"]]); r = AB.readings(ns, 36, [0, 18], 18); phr = sum(sum(v) for v in sp["slots"].values())
    out = dict(sung_bars=sp.get("sung_bars"), slots=sp["slots"], held_bar_share=sp.get("held_bar_share"), made=m["made"], living=m["survivors"], deaths=m["deaths"], pool=j.get("pass_the_gate"), pick_distance=j.get("pick_distance"), joint_gate=j.get("gate"), notes=len(ns), bars_of_sung_phrases=phr, notes_over_bars_of_sung_phrases=round(len(ns) / phr, 3), notes_a_bar_as_the_table_counts=round(r["notes a bar"], 3),
               onsets_on_the_beat=round(r["onsets on the beat"], 3), onsets_on_the_first_beat=round(r["onsets on the bar's first beat"], 3), range=r["range"], distinct_pitches=r["distinct pitches"], key=R["key"]["key"], seconds=[f for f in R.get("flags", []) if "seconds" in f])
    spec = json.loads(json.dumps(sp)); E = M.Engine(spec); rng = random.Random(L.get("seed", 1)); onb = []; errs = collections.Counter(); hook = []
    for _ in range(1000):
        c, err = E.build(rng)
        if err: errs[str(err[0])] += 1; continue
        st = [n for n in c["notes"] if n["stress"]]; onb.append(float(np.mean([E.on_beat(n["on"]) for n in st]))); hs = [n for n in st if n["sec"] == "Chorus 1" and n["line"] == 2]; hook.append(float(np.mean([E.on_beat(n["on"]) for n in hs])))
    out["every_build_made"] = dict(made=len(onb), not_made=dict(errs), stressed_on_a_beat_quartiles=[round(float(q), 3) for q in np.percentile(onb, (25, 50, 75))], chorus_title_line_under_half=round(float(np.mean(np.array(hook) < 0.5)), 3)); out["a_place_to_land"] = R68.land(E, spec)
    T34.M = "6/8"; T34.BL = 36; T34.BEATS = [0, 18]
    with Pool(2) as pool: W = [x for x in pool.map(R68.wiki68, sorted(glob.glob("/home/claude/corpus/choco/partitions/wikifonia/raw/*.mxl")), chunksize=20) if x]
    KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["6-8_sung"]; out["kept_10_25_50_75_90"] = {}
    for nm in ("notes a bar", "onsets on the beat", "onsets on the bar's first beat", "range", "distinct pitches"):
        out["kept_10_25_50_75_90"][nm] = dict(Essen=[round(float(q), 3) for q in np.percentile([x[KR["names"].index(nm)] for x in KR["rows"]], (10, 25, 50, 75, 90))], lead_sheets=[round(float(q), 3) for q in np.percentile([w[nm] for w in W], (10, 25, 50, 75, 90))])
    out["lead_sheets"] = len(W); print(json.dumps(out, indent=0)[:4000]); json.dump(out, open(os.path.join(HERE, "plan_6_8.json"), "w"), indent=1)
