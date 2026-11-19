"""After 912: how square are the builds as WORD_PLACE (879) is turned down? For one 4/4 song, N builds a setting (same seed), the builds' stressed
syllables on a beat (kept by song 10/25/50/75: 0.35, 0.446, 0.542, 0.661), onsets on the beat, and the words' fit whole and by part (kept medians:
0.318; length 0.209, place 0.242, height 0.106). python3 studies/kept_checks/place_weight_sweep.py songs/p68/lyric58.json 300 1.5 1.0 0.7"""
import sys, os, json, random
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import metre_engine as M, song_from_lyric as SL, word_weight as WW
class Got(Exception): pass
CAP = {}
def capture(self, N, seed):
    rng = random.Random(seed); A = []
    for k in range(N):
        c, err = self.build(rng)
        if err or self.gates(c): continue
        f = WW.fit(c["notes"], self.BAR, self.BEAT, parts=True); st = [n for n in c["notes"] if n["stress"]]
        A.append(dict(sob=float(np.mean([self.on_beat(n["on"]) for n in st])), ob=float(np.mean([self.on_beat(n["on"]) for n in c["notes"]])), **f))
    CAP["A"] = A; raise Got()
M.Engine.run = capture
f, N = sys.argv[1], int(sys.argv[2]); L = json.load(open(f)); out = {}
for wp in [float(x) for x in sys.argv[3:]]:
    SL.WORD_PLACE = wp
    try: SL.write(L, N, 12)
    except Got: pass
    A = CAP["A"]; q = lambda k: [round(float(x), 3) for x in np.percentile([a[k] for a in A], (25, 50, 75))]
    out[wp] = dict(survivors=len(A), stressed_on_beat=q("sob"), onsets_on_beat=q("ob"), fit=q("all"), by_length=q("length"), by_place=q("place"), by_height=q("height"))
    print(os.path.basename(f), "WORD_PLACE", wp, json.dumps(out[wp]), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "place_weight_sweep_" + os.path.basename(f).split(".")[0] + ".json"), "w"), indent=1)
