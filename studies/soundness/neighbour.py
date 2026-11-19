"""749.94: pick toward a kept song, not toward the middle. For each 4/4 song: the engine's 1,000 builds and its gates (as margin.py), then every pool build
read on the 21 checks soundness.py reads on kept songs (as sung). Two ways to choose from the pool:
  first      the engine's way (872): the first build in order
  neighbour  draw one kept song at random and take the pool build nearest it on the 21 checks (each check scaled by the kept middle half's width)
For the neighbour way, 400 draws of three kept targets: how many song-checks fall outside the kept middle half across the three songs (kept songs drawn at
random: median about 30, 5th percentile about 21), and how often the soundness rule fails.
Also: a random pick from every build that lived, from the engine's pool, and from a looser pool (the joint gate and the kept floor only), 4,000 times each.
    python3 studies/soundness/neighbour.py songs/p65/lyric55.json songs/p64/lyric54.json songs/p68/lyric58.json   (PYTHONHASHSEED=0; MARGIN_TURNS_OF_FOUR=dir to try 749.95 with it)"""
import sys, os, json, random
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.dirname(os.path.abspath(__file__))]
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
first = [min(p, key=lambda c: c["n"])["row"] for p in pools.values()]; ok_f, w_f, h_f = judge(first)
rng = random.Random(7); tot = []; fails = 0; wl = {}
for _ in range(400):
    rows = []
    for p in pools.values():
        t = rng.choice(full); rows.append(min(p, key=lambda c: sum(((c["row"][n] - t[n]) / W_[n]) ** 2 for n in NAMES))["row"])
    tot.append(sum(outside(r) for r in rows)); ok, w, h = judge(rows); fails += not ok
    for x in w: wl[x] = wl.get(x, 0) + 1
out = dict(first=dict(outside_middle_half=[outside(r) for r in first], total=sum(outside(r) for r in first), sound=ok_f, leans_10_90=w_f, leans_25_75=h_f),
           neighbour=dict(total_outside_middle_half_5_25_50_75_95=[float(x) for x in np.percentile(tot, (5, 25, 50, 75, 95))], rule_fails_share=round(fails / 400, 3), leans_past_10_90_by_check={k: round(v / 400, 3) for k, v in wl.items()}),
           pool_share_outside_middle_half_median=[float(np.median([outside(c["row"]) for c in p])) for p in pools.values()])
def random_picks(P, n=4000):
    rng2 = random.Random(11); t = []; fl = 0; hl = {}; wl2 = {}
    for _ in range(n):
        rows = [rng2.choice(p)["row"] for p in P.values()]; t.append(sum(outside(r) for r in rows)); ok_, w_, h_ = judge(rows); fl += not ok_
        for x in h_: hl[x] = hl.get(x, 0) + 1
        for x in w_: wl2[x] = wl2.get(x, 0) + 1
    return dict(total_outside_middle_half_5_50_95=[float(x) for x in np.percentile(t, (5, 50, 95))], rule_fails_share=round(fl / n, 3),
                lean_past_25_75_share_by_check={k: round(v / n, 3) for k, v in sorted(hl.items(), key=lambda x: -x[1])}, lean_past_10_90_share_by_check={k: round(v / n, 3) for k, v in wl2.items()})
out["a_random_pick_from"] = {"every build that lived": random_picks(ALIVE), "the engine's pool (old charge's better half, joint gate, words' better halves)": random_picks(pools), "the joint gate and the kept floor only": random_picks(LOOSE)}
if all(TARGET.values()):                                                                        # 920's aim, carried into the choice: the pool builds nearest each song's own kept song on the aimed readings
    def near_aim(p, t, k=None):
        ks = [n for n in t if n in Q]; d = sorted(p, key=lambda c: sum(((c["row"][n] - t[n]) / W_[n]) ** 2 for n in ks))
        return d if k is None else d[:k]
    rows = [near_aim(pools[s_], TARGET[s_])[0]["row"] for s_ in pools]; ok_a, w_a, h_a = judge(rows)
    out["nearest_the_songs_own_aim"] = dict(outside_middle_half=[outside(r) for r in rows], total=sum(outside(r) for r in rows), sound=ok_a, leans_10_90=w_a, leans_25_75=h_a,
        random_pick_among_the_ten_nearest=random_picks({s_: near_aim(pools[s_], TARGET[s_], 10) for s_ in pools}))
    out["aim_reached"] = {s_: {n: dict(target=round(TARGET[s_][n], 3), first=round(min(pools[s_], key=lambda c: c["n"])["row"][n], 3), nearest=round(near_aim(pools[s_], TARGET[s_])[0]["row"][n], 3), kept_median=round(Q[n][2], 3)) for n in TARGET[s_] if n in Q} for s_ in pools}
out["pool_share_outside_middle_half_by_check"] = {n: dict(low=round(float(np.mean([S.side(Q[n], c["row"][n], "half") < 0 for p in pools.values() for c in p])), 3), high=round(float(np.mean([S.side(Q[n], c["row"][n], "half") > 0 for p in pools.values() for c in p])), 3)) for n in NAMES}      # a kept song: 0.25 and 0.25
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "neighbour" + ("_" + os.environ.get("TRIAL_NAME", "trial") if os.environ.get("MARGIN_TURNS_OF_FOUR") else "") + ".json"), "w"), indent=1)
