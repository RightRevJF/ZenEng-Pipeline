"""The clean reading for the peak climbed to (PREDICTION_climb.md, 6 and 7): each record's fitted spec, the form off and on, the octave gate off and on.
    python3 studies/the_draw/climb_held.py songs/p65/lyric55 ... -> climb_held.json"""
import os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [os.path.normpath(os.path.join(HERE, "..", "..", "lib", "luthier")), os.path.normpath(os.path.join(HERE, "..", "..", "tables", "metre_atlas"))]
import song_from_lyric as SL, metre_engine as M
out = {}
for stem in sys.argv[1:]:
    L = json.load(open(stem + ".json")); rec = json.load(open(stem + ".song.json")); o = {}
    for climb in (False, True):
        for gate in (True, False):
            spec = json.loads(json.dumps(rec["spec"])); spec["no_leap_past_an_octave"] = gate
            if climb: spec["target"]["peak"]["climb"] = True
            E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
            rng = random.Random(L.get("seed", 1)); live = 0; withleap = 0; rg = []
            for _ in range(1000):
                c, err = E.build(rng)
                if err or E.gates(c): continue
                s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]); live += 1; rg.append(max(n["p"] for n in s) - min(n["p"] for n in s))
                withleap += any(a["sec"] == b["sec"] and a["line"] == b["line"] and abs(b["p"] - a["p"]) > 12 for a, b in zip(s, s[1:]))
            o[("climb" if climb else "v47") + (", gate on" if gate else ", gate off")] = dict(living=live, builds_with_a_leap=round(withleap / max(1, live), 3), median_range=sorted(rg)[len(rg) // 2], planted=E.stats.get("950: the peak planted in a chorus line", 0))
    out[os.path.basename(stem)] = o; print(os.path.basename(stem), json.dumps(o), flush=True)
json.dump(out, open(os.path.join(HERE, "climb_held.json"), "w"), indent=1)
