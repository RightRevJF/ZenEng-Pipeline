"""A reading after the result (not a test): the octave forms on the same fitted engine. The record's own spec (its fits already made) is run again, a thousand builds,
under the ban and under one leap allowed, so the two differ in the gate and in nothing else.   python3 studies/v48_trials/held_fit.py songs/p65/lyric55 ..."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [os.path.normpath(os.path.join(HERE, "..", "..", "lib", "luthier")), os.path.normpath(os.path.join(HERE, "..", "..", "tables", "metre_atlas"))]
import song_from_lyric as SL, metre_engine as M
out = {}
for stem in sys.argv[1:]:
    L = json.load(open(stem + ".json")); rec = json.load(open(stem + ".song.json")); o = {}
    for form in (True, "one", False):
        spec = json.loads(json.dumps(rec["spec"])); spec["no_leap_past_an_octave"] = form; E = M.Engine(spec)
        E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        r = E.run(1000, L.get("seed", 1)); o[{True: "ban", "one": "one", False: "off"}[form]] = dict(live=r["survivors"], octave_deaths=sum(v for k, v in r["deaths"].items() if k.startswith(("959", "trial 749.176"))))
    out[os.path.basename(stem)] = o; print(os.path.basename(stem), o, "record:", rec["melody"]["survivors"])
json.dump(out, open(os.path.join(HERE, "held_fit.json"), "w"), indent=1)
