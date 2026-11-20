"""Do the pools follow their aims? Pool and every-living-build medians on the aimed checks, against each song's aimed kept song."""
# Hold-out (song 59): studies/review19/aimpool.py as it stands at v34, run on song 59 alone. From the repo root, PYTHONHASHSEED=0.
import sys, os, json, random, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import song_from_lyric as SL, metre_engine as M, soundness as S, word_weight as WW
class Got(Exception): pass
CAP = {}
def row(sung):
    ns = [dict(n, midi=n["p"]) for n in sorted(sung, key=lambda n: n["on"])]
    return S.record_row(dict(melody=dict(notes=ns), checks={"the chorus's median over the verse's, semitones": 0, "rest share inside sung sections": 0}))
def capture(self, N, seed):
    rng = random.Random(seed); alive = []
    for k in range(N):
        c, err = self.build(rng)
        if err or self.gates(c): continue
        alive.append(c)
    for c in alive: c["row"] = row(self.as_sung(c["notes"]))
    CAP.update(alive=alive, target=self.S["target"]); raise Got()
M.Engine.run = capture
K = S.kept_rows(); full = [r for r in K.values()]; out = {}
CH = ["moves by step", "moves by leap", "repeated notes", "range", "bars on a figure already sung", "bars on a rhythm already sung", "distinct rhythms over bars", "pitch scaling", "rhythm scaling"]
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]
for f in ("songs/p69/lyric59.json",):
    try: SL.write(json.load(open(os.path.join(ROOT, f))), 1000, 12)
    except Got: pass
    t = CAP["target"]; kr = dict(zip(KR["names"], KR["rows"][t["kept_song_row"]])); o = {}
    for c in CH:
        v = [x["row"][c] for x in CAP["alive"] if c in x["row"] and x["row"][c] is not None]
        o[c] = dict(aim=round(float(kr[c]), 3) if c in kr else None, builds_median=round(float(np.median(v)), 3), kept_median=round(float(np.median([r[c] for r in full if r.get(c) is not None])), 3))
    out[os.path.basename(f)] = dict(aims_at=t.get("kept_song"), builds=len(CAP["alive"]), checks=o); print(f, json.dumps(out[os.path.basename(f)]), flush=True)
json.dump(out, open(os.path.join(ROOT, "studies", "holdout59", "aimpool59.json"), "w"), indent=1)
