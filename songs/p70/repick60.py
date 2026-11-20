"""Song 60: the re-pick the songwrite method offers when the pick chants. The judge's own rule, unchanged, over the builds of the same run
that do not chant: a build whose longest run of one pitch, as sung across the song, is over 9 (the kept 90th percentile is 9.5) is set aside
before the judge reads the pool. Nothing else changes: same lyric, seed, fit and gates. Writes lyric60.nochant.song.json."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib", "luthier"))
import metre_engine as M, song_from_lyric as S
ON = {"on": False}; _gates = M.Engine.gates; _run = M.Engine.run
def longest(ps):
    best = cur = 1
    for a, b in zip(ps, ps[1:]): cur = cur + 1 if a == b else 1; best = max(best, cur)
    return best
def gates(self, c):
    f = _gates(self, c)
    if f or not ON["on"]: return f
    ns = (getattr(self, "as_sung", None) or (lambda x: x))(c["notes"])
    return "re-pick: a run of one pitch over 9, as sung" if longest([n["p"] for n in sorted(ns, key=lambda n: n["on"])]) > 9 else None
def run(self, N, seed):
    ON["on"] = True
    try: return _run(self, N, seed)
    finally: ON["on"] = False
M.Engine.gates = gates; M.Engine.run = run
L = json.load(open(sys.argv[1])); rec = S.write(L, int(sys.argv[2]), int(sys.argv[3]))
json.dump(rec, open(sys.argv[1].replace(".json", "") + ".nochant.song.json", "w"), indent=1, default=float)
m = rec["melody"]; print("survivors", m["survivors"], "of", m["made"], "pick", m["pick"], "deaths", m["deaths"])
