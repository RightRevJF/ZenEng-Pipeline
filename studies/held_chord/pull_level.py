"""After the result (a description, not a test): the share of on-beat notes that are chord tones in the builds, at the pull as it is, halved, and gone; the clash rule on and off. -> pull_level.json"""
import os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M
out = {}
for name, stem in (("50", "songs/p60/lyric50"), ("55", "songs/p65/lyric55")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); out[name] = {}
    for label, pull, clash in (("as it is", None, True), ("pull halved", 0.5, True), ("pull gone", 0.0, True), ("pull gone, clash rule off", 0.0, False), ("pull as it is, clash rule off", None, False)):
        spec = json.loads(json.dumps(rec["spec"])); spec["clash_rule"] = clash
        if pull is not None: spec["chord_pull"] = pull
        E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); a = b = c = d = 0; nb = 0
        for _ in range(400):
            cc, err = E.build(rng)
            if err or E.gates(cc): continue
            nb += 1
            for n in E.as_sung(cc["notes"]):
                ct = n["p"] % 12 in E.chord_at(n["on"])
                if E.on_beat(n["on"]): a += ct; b += 1
                else: c += ct; d += 1
        out[name][label] = dict(living=nb, on_beat_chord_tones=round(a / max(1, b), 3), off_beat_chord_tones=round(c / max(1, d), 3)); print(name, label, out[name][label], flush=True)
json.dump(out, open(os.path.join(HERE, "pull_level.json"), "w"), indent=1)
