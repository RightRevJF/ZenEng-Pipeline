"""The builds' middle scaling readings: v50 records and the whole-engine trial records (a directory of them). python3 scaling.py DIR -> scaling.json"""
import os, sys, json, random, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M
out = {}
for n, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("50", "songs/p60/lyric50"), ("59", "songs/p69/lyric59")):
    L = json.load(open(os.path.join(ROOT, p + ".json"))); o = {}
    for lab, f in (("v50", os.path.join(ROOT, p + ".song.json")), ("form", os.path.join(sys.argv[1], f"lyric{n}.song.json"))):
        spec = json.load(open(f))["spec"]; E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); ps = []; rs = []; fg = []
        for _ in range(int(os.environ.get("N", "300"))):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            r = E.readings(c["notes"]); ps.append(r["pitch scaling"]); rs.append(r["rhythm scaling"]); fg.append(r["bars on a figure already sung"])
        q = lambda v: [round(x, 3) for x in st.quantiles(v, n=4)]
        o[lab] = dict(builds=len(ps), pitch_scaling_25_50_75=q(ps), rhythm_scaling_25_50_75=q(rs), figure=round(st.median(fg), 3))
    out[n] = o; print(n, json.dumps(o), flush=True)
json.dump(out, open(os.path.join(HERE, "scaling.json"), "w"), indent=1)
