"""749.93: does taking an earlier line's rhythm (818's borrow, rhythm share 0.0 now; figure 0.6) bring rhythm scaling into the kept range?
For one 4/4 song, N builds a setting (same seed): the builds' quartiles of rhythm scaling (kept 25th, median, 75th 0.608, 0.656, 0.721), bars on a rhythm
already sung (0.454, 0.595, 0.687), distinct rhythms over bars (0.313, 0.405, 0.546), pitch scaling (0.792, 0.905, 1.023), stressed syllables on a beat.
    python3 studies/soundness/rhythm_borrow_sweep.py songs/p68/lyric58.json 300 0 0.2 0.4"""
import sys, os, json, random
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import metre_engine as M, song_from_lyric as SL
class Got(Exception): pass
CAP = {}; BR = {"v": 0.0}
def capture(self, N, seed):
    self.S["borrow"] = dict(self.S["borrow"], rhythm=BR["v"]); rng = random.Random(seed); A = []
    for k in range(N):
        c, err = self.build(rng)
        if err or self.gates(c): continue
        r = self.readings(c["notes"]); st = [n for n in c["notes"] if n["stress"]]; A.append(dict(r, sob=float(np.mean([self.on_beat(n["on"]) for n in st]))))
    CAP["A"] = A; raise Got()
M.Engine.run = capture
f, N = sys.argv[1], int(sys.argv[2]); L = json.load(open(f)); out = {}
KEYS = ["rhythm scaling", "bars on a rhythm already sung", "distinct rhythms over bars", "pitch scaling", "sob"]
for v in [float(x) for x in sys.argv[3:]]:
    BR["v"] = v
    try: SL.write(L, N, 12)
    except Got: pass
    A = CAP["A"]; out[v] = dict(survivors=len(A), **{k: [round(float(x), 3) for x in np.percentile([a[k] for a in A], (25, 50, 75))] for k in KEYS if k in A[0]})
    print(os.path.basename(f), "borrow rhythm", v, json.dumps(out[v]), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rhythm_borrow_sweep_" + os.path.basename(f).split(".")[0] + ".json"), "w"), indent=1)
