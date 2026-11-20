"""The same reading as where.py on many builds of each song (not only the pick): python3 studies/repeated_figures/pool.py [N]  ->  pool.json"""
import sys, os, json, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", ".."); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier")); sys.argv, N = sys.argv[:1], int(sys.argv[1]) if len(sys.argv) > 1 else 80
import metre_engine as M
sys.path.insert(0, HERE); import importlib.util
spec_ = importlib.util.spec_from_file_location("where", os.path.join(HERE, "where.py")); Wm = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(Wm)
Q = json.load(open(os.path.join(HERE, "where.json")))["kept_quartiles"]; out = {}
for tag, path in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json")):
    R = json.load(open(os.path.join(ROOT, path))); E = M.Engine(R["spec"]); rng = random.Random(11); rows = []
    for _ in range(N):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        ns = sorted(c["notes"], key=lambda n: n["on"]); r = Wm.read([n["p"] for n in ns], [n["on"] * 4.0 / R["bar"] for n in ns])
        if r: rows.append(r)
    out[tag] = dict(builds=len(rows), **{k: dict(median=round(float(np.median([r[k] for r in rows])), 3), under_kept_25th=round(float(np.mean([r[k] < Q[k][0] for r in rows])), 2), over_kept_75th=round(float(np.mean([r[k] > Q[k][2] for r in rows])), 2), kept=Q[k]) for k in Q})
    print(tag, len(rows)); [print(f"   {k:22} median {out[tag][k]['median']:<7} under kept 25th {out[tag][k]['under_kept_25th']:<5} over 75th {out[tag][k]['over_kept_75th']:<5} kept {Q[k]}") for k in Q]
json.dump(out, open(os.path.join(HERE, "pool.json"), "w"), indent=1)
