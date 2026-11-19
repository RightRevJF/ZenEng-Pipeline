"""908 and the question of place: what the words' gate does to the stressed syllables on a beat. For each 4/4 song, the engine's own 1,000 builds
(same seed and spec as song_from_lyric.py), the gates up to the words' gate as the engine applies them, then the words' gate four ways:
  none      the joint gate only (v26 floor at the kept 10th, no median)
  908       the whole fit and the fit by length at the builds' medians (v27)
  len+ht    the fit by length and by height at the builds' medians, place left out
  len       the fit by length at its median only
For each: builds passing, the pick (the first in order, as 872), and the pool's medians of stressed syllables on a beat, fit whole, by length, by place, by height.
python3 studies/kept_checks/place_in_gate.py songs/p68/lyric58.json ... (PYTHONHASHSEED=0; WORD_PLACE=0.75 to try another place weight)"""
import sys, os, json, math, random, collections
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import metre_engine as M, song_from_lyric as SL, word_weight as WW
class Got(Exception): pass
CAP = {}
def capture(self, N, seed):
    rng = random.Random(seed); alive = []
    for k in range(N):
        c, err = self.build(rng)
        if err: continue
        if self.gates(c): continue
        r = self.readings(c["notes"]); ch, dist = self.charge(r); c.update(readings=r, charge=ch, distance=dist, n=k); alive.append(c)
    import luthier_judge7 as J7; J = J7.Judge7(self.S.get("table") or self.S["metre"].replace("/", "-") + "_sung")
    for c in alive:
        c["d7"] = J.distance(c["readings"]); f = WW.fit(c["notes"], self.BAR, self.BEAT, parts=True); c.update(f_all=f["all"], f_len=f["length"], f_pl=f["place"], f_ht=f["height"])
        st = [n for n in c["notes"] if n["stress"]]; c["sob"] = float(np.mean([self.on_beat(n["on"]) for n in st]))
    half = float(np.median([c["charge"] for c in alive])); ok = [c for c in alive if c["charge"] <= half and c["d7"] <= J.gate]
    CAP.update(alive=alive, ok=ok, floor=self.WW["gate"]); raise Got()
M.Engine.run = capture
WP = os.environ.get("WORD_PLACE")                      # a trial value of 879's place weight (the engine's is 1.5)
if WP: SL.WORD_PLACE = float(WP)
KL = json.load(open(os.path.join(ROOT, "tables", "kept_line_ends.json")))["stressed_syllables_on_a_beat_by_song_5_10_25_50_75"]
KW = json.load(open(os.path.join(ROOT, "tables", "kept_word_weight.json")))
out = {}
for f in sys.argv[1:]:
    L = json.load(open(f))
    try: SL.write(L, 1000, 12)
    except Got: pass
    A, ok, fl = CAP["alive"], CAP["ok"], CAP["floor"]; md = {k: float(np.median([c[k] for c in A])) for k in ("f_all", "f_len", "f_pl", "f_ht")}
    G = {"none": lambda c: c["f_all"] >= fl, "908": lambda c: c["f_all"] >= max(fl, md["f_all"]) and c["f_len"] >= md["f_len"],
         "len+ht": lambda c: c["f_all"] >= fl and c["f_len"] >= md["f_len"] and c["f_ht"] >= md["f_ht"], "len": lambda c: c["f_all"] >= fl and c["f_len"] >= md["f_len"],
         "len+ht, on-beat in kept middle half": lambda c: c["f_all"] >= fl and c["f_len"] >= md["f_len"] and c["f_ht"] >= md["f_ht"] and KL[2] <= c["sob"] <= KL[4]}
    res = dict(builds=len(A), past_joint=len(ok), builds_medians={k: round(v, 3) for k, v in md.items()}, builds_sob_quartiles=[round(float(x), 3) for x in np.percentile([c["sob"] for c in A], (25, 50, 75))], builds_share_on_beat_in_kept_middle_half=round(float(np.mean([KL[2] <= c["sob"] <= KL[4] for c in A])), 3),
               corr_sob_with={k: round(float(np.corrcoef([c["sob"] for c in A], [c[k] for c in A])[0, 1]), 3) for k in ("f_all", "f_len", "f_pl", "f_ht")})
    for g, fn in G.items():
        P = [c for c in ok if fn(c)]
        if not P: res[g] = "none pass"; continue
        pk = min(P, key=lambda c: c["n"])
        res[g] = dict(pass_=len(P), pick=dict(n=pk["n"], fp=__import__('hashlib').sha1(json.dumps([(n_["on"], n_["p"]) for n_ in pk["notes"]]).encode()).hexdigest()[:12], sob=round(pk["sob"], 3), all=round(pk["f_all"], 3), length=round(pk["f_len"], 3), place=round(pk["f_pl"], 3), height=round(pk["f_ht"], 3)),
                      pool_medians={k: round(float(np.median([c[k] for c in P])), 3) for k in ("sob", "f_all", "f_len", "f_pl", "f_ht")},
                      pool_share_on_beat_in_kept_middle_half=round(float(np.mean([KL[2] <= c["sob"] <= KL[4] for c in P])), 3))
    out[os.path.basename(f)] = res; print(os.path.basename(f), json.dumps(res))
out["kept"] = dict(stressed_on_a_beat_by_song_5_10_25_50_75=KL)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "place_in_gate_" + (f"wp{WP}_" if WP else "") + "_".join(os.path.basename(f).split(".")[0] for f in sys.argv[1:]) + ".json"), "w"), indent=1)
