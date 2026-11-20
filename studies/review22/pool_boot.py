"""Review 22 (Luthier v36): neighbour.py's pools, then a bootstrap of the random pick from the engine's pool: each pool resampled with replacement (its own size), 2,000 random triples a resample, 200 resamples. How much of the rate is the luck of which builds made each pool.
(Below, neighbour.py's own docstring.)
749.94: pick toward a kept song, not toward the middle. For each 4/4 song: the engine's 1,000 builds and its gates (as margin.py), then every pool build
read on the 21 checks soundness.py reads on kept songs (as sung). Two ways to choose from the pool:
  first      the engine's way (872): the first build in order
  neighbour  draw one kept song at random and take the pool build nearest it on the 21 checks (each check scaled by the kept middle half's width)
For the neighbour way, 400 draws of three kept targets: how many song-checks fall outside the kept middle half across the three songs (kept songs drawn at
random: median about 30, 5th percentile about 21), and how often the soundness rule fails.
Also: a random pick from every build that lived, from the engine's pool, and from a looser pool (the joint gate and the kept floor only), 4,000 times each.
    python3 studies/soundness/neighbour.py songs/p65/lyric55.json songs/p64/lyric54.json songs/p68/lyric58.json   (PYTHONHASHSEED=0; MARGIN_TURNS_OF_FOUR=dir to try 749.95 with it)"""
import sys, os, json, random
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
if os.environ.get("MARGIN_TURNS_OF_FOUR"): sys.path.insert(0, os.environ["MARGIN_TURNS_OF_FOUR"])
import song_from_lyric as SL; import metre_engine as M, word_weight as WW
import soundness as S
class Got(Exception): pass
CAP = {}; NAMES = [n for n, _ in S.CHECKS]
def row(sung):
    ns = [dict(n, midi=n["p"]) for n in sorted(sung, key=lambda n: n["on"])]
    R = dict(melody=dict(notes=ns), checks={"the chorus's median over the verse's, semitones": 0, "rest share inside sung sections": 0}); return S.record_row(R)
def capture(self, N, seed):
    rng = random.Random(seed); alive = []
    for k in range(N):
        c, err = self.build(rng)
        if err or self.gates(c): continue
        r = self.readings(c["notes"]); ch, dist = self.charge(r); c.update(readings=r, charge=ch, distance=dist, n=k); alive.append(c)
    import luthier_judge7 as J7; J = J7.Judge7(self.S.get("table") or self.S["metre"].replace("/", "-") + "_sung")
    for c in alive:
        c["d7"] = J.distance(c["readings"]); c["sung"] = self.as_sung(c["notes"]); f = WW.fit([x for x in c["sung"] if x.get("melisma") != "second"], self.BAR, self.BEAT, parts=True)
        c.update(f_all=f["all"], f_len=f["length"], f_ht=f["height"])
    half = float(np.median([c["charge"] for c in alive])); ok = [c for c in alive if c["charge"] <= half and c["d7"] <= J.gate]
    ml = float(np.median([c["f_len"] for c in alive])); mh = float(np.median([c["f_ht"] for c in alive]))
    pool = [c for c in ok if c["f_all"] >= self.WW["gate"] and c["f_len"] >= ml and c["f_ht"] >= mh] or ok
    for c in alive: c["row"] = row(c["sung"])
    loose = [c for c in alive if c["d7"] <= J.gate and c["f_all"] >= self.WW["gate"]]        # the joint gate and the kept floor only: no pull to the builds' better halves
    CAP.update(pool=pool, alive=alive, loose=loose, target=(self.S.get("target") or {}).get("readings")); raise Got()
M.Engine.run = capture
K = S.kept_rows(); full = [r for r in K.values() if all(n in r for n in NAMES)]
Q = {n: [float(x) for x in np.percentile([r[n] for r in full], (10, 25, 50, 75, 90))] for n in NAMES}; W_ = {n: max(1e-9, Q[n][3] - Q[n][1]) for n in NAMES}
pools = {}; ALIVE = {}; LOOSE = {}; TARGET = {}
for f in sys.argv[1:]:
    try: SL.write(json.load(open(f)), 1000, 12)
    except Got: pass
    TARGET[os.path.basename(f)] = CAP["target"]; pools[os.path.basename(f)] = CAP["pool"]; ALIVE[os.path.basename(f)] = CAP["alive"]; LOOSE[os.path.basename(f)] = CAP["loose"]; print(os.path.basename(f), "pool", len(CAP["pool"]), "loose", len(CAP["loose"]), flush=True)
def outside(r): return sum(S.side(Q[n], r[n], "half") != 0 for n in NAMES)
def judge(rows): w = S.same_side(Q, rows, NAMES, "wide"); h = S.same_side(Q, rows, NAMES, "half"); return (not w and len(h) <= 2), [x[0] for x in w], [x[0] for x in h]

def rate(P, n, rng):
    keys = list(P); fl = 0
    for _ in range(n):
        rows = [rng.choice(P[k])["row"] for k in keys]; ok_, _, _ = judge(rows); fl += not ok_
    return fl / n
rng = random.Random(23); out = {}
for name, P in (("pool", pools), ("every build that lived", ALIVE)):
    base = rate(P, 4000, random.Random(11)); boots = []
    for b in range(200):
        Pb = {k: [rng.choice(v) for _ in v] for k, v in P.items()}; boots.append(rate(Pb, 2000, rng))
    out[name] = dict(sizes={k: len(v) for k, v in P.items()}, rate_4000_draws=round(base, 4), bootstrap_5_25_50_75_95=[round(float(x), 4) for x in np.percentile(boots, (5, 25, 50, 75, 95))])
    print(name, out[name], flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pool_boot" + os.environ.get("OUT_SUFFIX", "") + ".json"), "w"), indent=1)
