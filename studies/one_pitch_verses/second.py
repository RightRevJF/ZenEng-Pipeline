"""The second pass (PREDICTION.md): the clash rule off; the verse's chords replaced by song 55's; the clash rule and the pull off.  python3 second.py songs/p60/lyric50 -> second_lyricNN.json"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
stem = sys.argv[1]; L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); ref = json.load(open(os.path.join(ROOT, "songs/p65/lyric55.song.json")))["spec"]; out = {}
refv = next(b for n, b in ref["form"] if n == "Verse 1")
for name in ("the clash rule off", "song 55's verse chords", "the clash rule and the pull off"):
    spec = json.loads(json.dumps(rec["spec"]))
    if "clash" in name: spec["clash_rule"] = False
    if "pull off" in name: spec["chord_pull"] = 0.0
    if "55" in name:
        spec["chords"].update(ref["chords"])
        for e in spec["form"]:
            if CP.kind(e[0]) == "Verse": e[1] = [refv[i % len(refv)] for i in range(len(e[1]))]
    E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    rng = random.Random(L.get("seed", 1)); sh = []; dist = []
    for _ in range(1000):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        ps = [n["p"] for n in E.as_sung(c["notes"]) if CP.kind(n["sec"]) == "Verse"]; sh.append(collections.Counter(ps).most_common(1)[0][1] / len(ps)); dist.append(len(set(ps)))
    out[name] = dict(living=len(sh), verses_over_the_ceiling_in_100=round(100 * sum(x > spec["pitch_ceiling"]["Verse"] for x in sh) / max(1, len(sh)), 1), middle_share_on_the_commonest_pitch=round(st.median(sh), 3) if sh else None, different_pitches=st.median(dist) if dist else None); print(os.path.basename(stem), name, out[name], flush=True)
json.dump(out, open(os.path.join(HERE, f"second_{os.path.basename(stem)}.json"), "w"), indent=1)
