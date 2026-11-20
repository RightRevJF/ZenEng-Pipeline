"""What can the borrows reach? Each song built with five settings of the two borrows (a fresh line sings an earlier line of its section again; or takes its rhythm with new notes),
read as sung: bars on a rhythm already sung, bars on a figure already sung, the words' fit. A look, not a trial: no rule, nothing decided. python3 studies/verse_match/reach.py [N] -> reach.json (PYTHONHASHSEED=0)"""
import sys, os, json, random, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import song_from_lyric as SL, metre_engine as M, soundness as S
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100; FIG, RHY, FIT = "bars on a figure already sung", "bars on a rhythm already sung", "the words' fit, whole"
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]
def row(ns): return S.record_row(dict(melody=dict(notes=[dict(n, midi=n["p"]) for n in sorted(ns, key=lambda n: n["on"])]), checks={"the chorus's median over the verse's, semitones": 0, "rest share inside sung sections": 0}))
out = {}
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    R = json.load(open(os.path.join(ROOT, p + ".song.json"))); spec = R["spec"]; L = json.load(open(os.path.join(ROOT, p + ".json"))); tg = spec["target"]; aim = dict(zip(KR["names"], KR["rows"][tg["kept_song_row"]])); res = {}
    for f, r in ((0.0, 0.0), (0.8, 0.0), (1.0, 0.0), (0.5, 0.5), (0.0, 1.0)):
        s2 = json.loads(json.dumps(spec)); s2["borrow"] = dict(figure=f, rhythm=r); E = M.Engine(s2); rng = random.Random(21); rows = []
        for _ in range(N):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            x = row(SL.melisma_notes(c["notes"], L, set(spec["scale"]), key="p", how=spec.get("how"), cap=tg.get("run"), share=tg.get("melisma_share"))[0]); rows.append({k: x[k] for k in (FIG, RHY, FIT, "rhythm scaling")})
        res[f"figure {f}, rhythm {r}"] = dict(builds=len(rows), **{k: round(float(np.median([x[k] for x in rows])), 3) for k in rows[0]})
    out[tag] = dict(aims_at=tg["kept_song"], aim={c: round(float(aim[c]), 3) for c in (FIG, RHY, "rhythm scaling")}, settings=res); print(tag, json.dumps(out[tag]), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reach.json"), "w"), indent=1)
