"""After the result (a description, not a test): the chord's pull taken away altogether. -> pull_off.json"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
out = {}
for name, stem in (("50", "songs/p60/lyric50"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("55", "songs/p65/lyric55")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; spec["chord_pull"] = 0.0; E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    rng = random.Random(L.get("seed", 1)); sh = []; dist = []
    for _ in range(1000):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        ps = [n["p"] for n in E.as_sung(c["notes"]) if CP.kind(n["sec"]) == "Verse"]; sh.append(collections.Counter(ps).most_common(1)[0][1] / len(ps)); dist.append(len(set(ps)))
    out[name] = dict(living=len(sh), verses_over_the_ceiling_in_100=round(100 * sum(x > 0.44 for x in sh) / max(1, len(sh)), 1), middle_share=round(st.median(sh), 3) if sh else None, different_pitches=st.median(dist) if dist else None); print(name, out[name], flush=True)
json.dump(out, open(os.path.join(HERE, "pull_off.json"), "w"), indent=1)
