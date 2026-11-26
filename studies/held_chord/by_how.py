"""After the result (a description): on-beat chord tones in the builds by how the line was made (fresh; sung again from an earlier line). -> by_how.json"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M
out = {}
for name, stem in (("50", "songs/p60/lyric50"), ("58", "songs/p68/lyric58"), ("49", "songs/p59/lyric49"), ("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54")):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    rng = random.Random(L.get("seed", 1)); C = collections.defaultdict(lambda: [0, 0]); nb = 0; lines = collections.Counter(E.HOW.get(k, ["fresh"])[0] for k in E.KEYS)
    for _ in range(400):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        nb += 1
        for n in E.as_sung(c["notes"]):
            if E.on_beat(n["on"]): h = E.HOW.get((n["sec"], n["line"]), ["fresh"])[0]; C[h][0] += n["p"] % 12 in E.chord_at(n["on"]); C[h][1] += 1
    tot = [sum(v[0] for v in C.values()), sum(v[1] for v in C.values())]
    out[name] = dict(living=nb, lines_by_how=dict(lines), on_beat_chord_tones={h: round(a / b, 3) for h, (a, b) in C.items()}, on_beat_notes_share={h: round(b / tot[1], 3) for h, (a, b) in C.items()}, all=round(tot[0] / tot[1], 3)); print(name, json.dumps(out[name]), flush=True)
json.dump(out, open(os.path.join(HERE, "by_how.json"), "w"), indent=1)
