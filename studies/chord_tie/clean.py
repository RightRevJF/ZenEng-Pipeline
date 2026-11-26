"""The clean reading (PREDICTION.md, marks 1 and 2): each v50 record's fitted spec, the form off and on. OUT=x.json python3 clean.py stem ..."""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
W = json.load(open(os.path.join(ROOT, "tables", "kept_chord_tie.json")))["weights"]; out = {}
for stem in sys.argv[1:]:
    L = json.load(open(stem + ".json")); rec = json.load(open(stem + ".song.json")); o = {}
    for form in (False, True):
        spec = json.loads(json.dumps(rec["spec"]))
        if form: spec["chord_tie"] = W
        E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); sh = []; a = b = c = d = la = lb = 0
        for _ in range(1000):
            cc, err = E.build(rng)
            if err or E.gates(cc): continue
            s = sorted(E.as_sung(cc["notes"]), key=lambda n: n["on"]); ps = [n["p"] for n in s if CP.kind(n["sec"]) == "Verse"]; sh.append(collections.Counter(ps).most_common(1)[0][1] / len(ps))
            for n in s:
                ct = n["p"] % 12 in E.chord_at(n["on"])
                if E.on_beat(n["on"]):
                    a += ct; b += 1
                    if n["dur"] >= E.BEAT: la += ct; lb += 1
                else: c += ct; d += 1
        o["the form" if form else "v50"] = dict(living=len(sh), verses_over_the_ceiling_in_100=round(100 * sum(x > 0.44 for x in sh) / max(1, len(sh)), 1), middle_share_on_the_commonest_pitch=round(st.median(sh), 3), on_beat_chord_tones=round(a / max(1, b), 3), off_beat_chord_tones=round(c / max(1, d), 3), long_on_beat_chord_tones=round(la / max(1, lb), 3))
    out[os.path.basename(stem)] = o; print(os.path.basename(stem), json.dumps(o), flush=True)
json.dump(out, open(os.path.join(HERE, os.environ.get("OUT", "clean.json")), "w"), indent=1)
