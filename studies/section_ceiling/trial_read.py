"""PREDICTION_trial.md: the trial's records against v53's.  N=300 python3 studies/section_ceiling/trial_read.py ON_DIR OFF_DIR -> trial.json"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, song_from_lyric as SL, metre_engine as M, page_gate as PG, make_kept_commonest_pitch as CP
T = PG.table(); ON, OFF = sys.argv[1:3]; N = int(os.environ.get("N", "300")); out = {}
KM = dict(pitch_scaling=json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json"))), surprise=T["percentiles_10_25_50_75_90"]["surprise"][2])
def share(ns, kd): return CP.share([n["midi"] for n in ns if (CP.kind_b(n.get("sec")) if kd == "Bridge" else CP.kind(n.get("sec"))) == kd])
def builds(rec, L):
    spec = json.loads(json.dumps(rec["spec"])); E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"), clash=None, relocate=False)[0]
    rng = random.Random(L.get("seed", 1)); ps = []; su = []
    for _ in range(N):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        ps.append(E.readings(c["notes"]).get("pitch scaling", float("nan"))); s = sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]); on_ = [x["on"] for x in s]; su.append(PG.read([x["p"] for x in s], [(b_ - a_) / float(E.BEAT) for a_, b_ in zip(on_, on_[1:])] + [1.0], T)["surprise"])
    return round(float(np.nanmedian(ps)), 3), round(st.median(su), 3)
for tag, stem in (("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59"), ("61", "songs/p71/lyric61"), ("66", "songs/p76/lyric66")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); o = {}
    for lab, f in (("v53", os.path.join(OFF, f"lyric{tag}.song.json") if tag == "66" else os.path.join(ROOT, stem + ".song.json")), ("trial", os.path.join(ON, f"lyric{tag}.song.json"))):
        R = json.load(open(f)); j = R["judge7"]; ns = R["melody"]["notes"]; rc = j["range_choice"]; ps, su = builds(R, L)
        o[lab] = dict(living=j["builds"], pool=j["pitch_ceiling"]["passed"] if "the ceiling is waived" not in json.dumps(j["pitch_ceiling"]) else j["pitch_ceiling"]["read"], pool_line=j["pass_the_gate"], ceiling=j["pitch_ceiling"], waived="waived" in json.dumps(j["pitch_ceiling"]), builds_fit=j["words_gate"]["the_builds_median_fit"], pick_fit=j["pick_words_fit"]["all"], range=rc["the_pick_range"], floor=rc["floor"],
                      bridge=round(share(ns, "Bridge") or 0, 3), verse=round(share(ns, "Verse"), 3), chorus=round(share(ns, "Chorus"), 3), key=R["key"]["key"], pick=R["melody"]["pick"], pitch_scaling=ps, surprise=su)
    out[tag] = o; print(tag, json.dumps(o), flush=True)
out["kept_surprise_middle"] = KM["surprise"]; json.dump(out, open(os.path.join(HERE, "trial.json"), "w"), indent=1)
