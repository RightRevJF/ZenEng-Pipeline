"""Every living build's median against the song's own targets (from its words and the engine's theory). After studies/review19/aimpool.py. PYTHONHASHSEED=0 python3 studies/shape_from_the_song/own.py -> own[SUFFIX].json"""
import sys, os, json, random, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import song_from_lyric as SL, metre_engine as M, soundness as S
class Got(Exception): pass
CAP = {}
def row(sung): return S.record_row(dict(melody=dict(notes=[dict(n, midi=n["p"]) for n in sorted(sung, key=lambda n: n["on"])]), checks={"the chorus's median over the verse's, semitones": 0, "rest share inside sung sections": 0}))
def capture(self, N, seed):
    rng = random.Random(seed); alive = []
    for k in range(N):
        c, err = self.build(rng)
        if err or self.gates(c): continue
        alive.append(c)
    CAP.update(rows=[row(self.as_sung(c["notes"])) for c in alive], target=self.S["target"], borrow=self.S.get("borrow")); raise Got()
M.Engine.run = capture
K = S.kept_rows(); full = list(K.values()); out = {}
CH = ["moves by step", "moves by leap", "repeated notes", "range", "bars on a figure already sung", "bars on a rhythm already sung", "rhythm scaling", "pitch scaling"]
for f in ("songs/p65/lyric55.json", "songs/p64/lyric54.json", "songs/p68/lyric58.json", "songs/p69/lyric59.json"):
    try: SL.write(json.load(open(os.path.join(ROOT, f))), 1000, 12)
    except Got: pass
    t = CAP["target"]; o = {}
    for c in CH:
        kv = [r[c] for r in full if r.get(c) is not None]; v = [r[c] for r in CAP["rows"] if r.get(c) is not None]
        o[c] = dict(asked=round(float(t["readings"][c]), 3) if c in t["readings"] else None, builds_median=round(float(np.median(v)), 3), kept_quartiles=[round(float(x), 3) for x in np.percentile(kv, (25, 50, 75))])
    out[os.path.basename(f)] = dict(builds=len(CAP["rows"]), borrow=CAP["borrow"], from_its_words=t.get("from_its_words"), movement=t.get("movement"), checks=o); print(f, json.dumps(out[os.path.basename(f)]), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "own" + os.environ.get("OUT_SUFFIX", "") + ".json"), "w"), indent=1)
