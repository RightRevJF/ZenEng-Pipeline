"""Does 926's gate pass over the builds that repeat most? Figures sung again, dead by 926 against alive."""
# Review 19 (Luthier v32). Run from the repo root with PYTHONHASHSEED=0.
import sys, os, json, random, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import song_from_lyric as SL, metre_engine as M, page_gate as PG
out = {}
for tag, lp in (("54", "songs/p64/lyric54.json"), ("55", "songs/p65/lyric55.json"), ("58", "songs/p68/lyric58.json")):
    R = json.load(open(os.path.join(ROOT, {"54": "songs/p64", "55": "songs/p65", "58": "songs/p68"}[tag], f"lyric{tag}.song.json"))); L = json.load(open(os.path.join(ROOT, lp))); spec = R["spec"]
    E = M.Engine(spec); E.as_sung = lambda ns_, L=L, spec=spec: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"))[0]
    rng = random.Random(9); dead = []; alive = []
    for _ in range(200):
        c, err = E.build(rng)
        if err: continue
        g = E.gates(c); fa = PG.figures_again([n["p"] for n in sorted(c["notes"], key=lambda n: n["on"])])
        (dead if g and g.startswith("926") else alive if not g else []).append(fa)
    out[tag] = dict(dead=len(dead), alive=len(alive), dead_median=round(float(np.median(dead)), 3), alive_median=round(float(np.median(alive)), 3))
    print(tag, out[tag], flush=True)
json.dump(out, open(os.path.join(ROOT, "studies", "review19", "runs2.json"), "w"), indent=1)
