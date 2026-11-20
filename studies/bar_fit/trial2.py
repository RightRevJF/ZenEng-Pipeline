"""Melismas carried with a line sung again, tried outside the engine. See PREDICTION2.md. python3 studies/bar_fit/trial2.py [N] -> trial2.json  (PYTHONHASHSEED=0)"""
import sys, os, json, random, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import song_from_lyric as SL, metre_engine as M, soundness as S
N = int(sys.argv[1]) if len(sys.argv) > 1 else 150; FIG, RHY, FIT = "bars on a figure already sung", "bars on a rhythm already sung", "the words' fit, whole"
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]
def row(ns): return S.record_row(dict(melody=dict(notes=[dict(n, midi=n["p"]) for n in sorted(ns, key=lambda n: n["on"])]), checks={"the chorus's median over the verse's, semitones": 0, "rest share inside sung sections": 0}))
out = {}
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    spec = json.load(open(os.path.join(ROOT, p + ".song.json")))["spec"]; L = json.load(open(os.path.join(ROOT, p + ".json"))); tg = spec["target"]; aim = dict(zip(KR["names"], KR["rows"][tg["kept_song_row"]]))
    how = spec.get("how") or {}; how2 = {k: (["copy", v[1], v[2]] if v and v[0] == "again" else v) for k, v in how.items()}; E = M.Engine(spec); rng = random.Random(17); rows = {"as the engine places them": [], "carried with a line sung again": []}
    kw = dict(key="p", cap=tg.get("run"), share=tg.get("melisma_share"))
    for _ in range(N):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        for nm, h in (("as the engine places them", how), ("carried with a line sung again", how2)):
            r = row(SL.melisma_notes(c["notes"], L, set(spec["scale"]), how=h, **kw)[0]); rows[nm].append({k: r[k] for k in (FIG, RHY, FIT)})
    res = {nm: dict(builds=len(v), **{k: round(float(np.median([x[k] for x in v])), 3) for k in (FIG, RHY, FIT)}) for nm, v in rows.items()}
    out[tag] = dict(aims_at=tg["kept_song"], aim={c: round(float(aim[c]), 3) for c in (FIG, RHY)}, lines_sung_again=sum(1 for v in how.values() if v and v[0] == "again"), lines_copied=sum(1 for v in how.values() if v and v[0] == "copy"), forms=res); print(tag, out[tag], flush=True)
T3 = ("55", "54", "58"); d = lambda t, c: out[t]["forms"]["carried with a line sung again"][c] - out[t]["forms"]["as the engine places them"][c]
c1 = all(sum(d(t, c) > 0 for t in T3) >= 2 and all(d(t, c) >= -0.01 for t in T3) for c in (FIG, RHY)); c2 = all(d(t, FIT) >= -0.01 for t in T3)
out["checks"] = {"1 bars return as sung": bool(c1), "2 the words' fit holds": bool(c2), "passes": bool(c1 and c2)}; print(out["checks"])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trial2.json"), "w"), indent=1)
