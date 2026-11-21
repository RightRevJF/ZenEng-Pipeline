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
import make_kept_commonest_pitch as CPK
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
    def cp_(c, part):                                                                             # 749.134: the share of a part's sung notes on its commonest pitch
        import collections; ps = [n["p"] for n in c["sung"] if CPK.kind(n["sec"]) == part]; return max(collections.Counter(ps).values()) / len(ps) if len(ps) >= 20 else 0.0
    for c in alive: c["cp"] = (cp_(c, "Verse"), cp_(c, "Chorus"))
    ce_ = self.S.get("pitch_ceiling")                                                              # 956: the engine's pool is under the ceiling
    if ce_: pool = [c for c in pool if c["cp"][0] <= ce_["Verse"] and c["cp"][1] <= ce_["Chorus"]] or pool
    loose = [c for c in alive if c["d7"] <= J.gate and c["f_all"] >= self.WW["gate"]]        # the joint gate and the kept floor only: no pull to the builds' better halves
    CAP.update(floor=((self.S.get("target") or {}).get("choose_range") or {}).get("floor"), pool=pool, alive=alive, loose=loose, target=(self.S.get("target") or {}).get("readings")); raise Got()
M.Engine.run = capture
K = S.kept_rows(); full = [r for r in K.values() if all(n in r for n in NAMES)]
Q = {n: [float(x) for x in np.percentile([r[n] for r in full], (10, 25, 50, 75, 90))] for n in NAMES}; W_ = {n: max(1e-9, Q[n][3] - Q[n][1]) for n in NAMES}
pools = {}; ALIVE = {}; LOOSE = {}; TARGET = {}; FLOOR = {}
for f in sys.argv[1:]:
    try: SL.write(json.load(open(f)), 1000, 12)
    except Got: pass
    FLOOR[os.path.basename(f)] = CAP["floor"]
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
out["pool_spread_over_kept_spread_by_check"] = {n: round(float(np.subtract(*np.percentile([c["row"][n] for p in pools.values() for c in p], (75, 25)))) / W_[n], 3) for n in NAMES}      # the pools' middle half, as wide as the kept songs' middle half = 1
out["pool_spread_over_kept_spread_within_each_song_median"] = {s_: round(float(np.median([float(np.subtract(*np.percentile([c["row"][n] for c in p], (75, 25)))) / W_[n] for n in NAMES])), 3) for s_, p in pools.items()}
out["variety_two_sided"] = dict(sum_of_twice_the_smaller_side=round(sum(2 * min(v["low"], v["high"]) for v in out["pool_share_outside_middle_half_by_check"].values()), 2), kept=0.5 * len(NAMES),
                                median_spread_ratio_all_three_pooled=round(float(np.median(list(out["pool_spread_over_kept_spread_by_check"].values()))), 3))
# 940 (749.120): each pool figure with its spread. The pools are small (some 50 to 90 builds), and which builds land in a pool moves a rate more than a fix does.
# Each pool (and each song's living builds) is resampled with replacement at its own size, 200 times; the figure is read again on each resample; the 5th and 95th percentiles are its 90% range.
def boot_rate(P, n, rngb):
    fl = 0
    for _ in range(n):
        ok_, _, _ = judge([rngb.choice(p)["row"] for p in P.values()]); fl += not ok_
    return fl / n
def boot_neighbour(P, n, rngb):
    mats = {k: (np.array([[c["row"][x] / W_[x] for x in NAMES] for c in p]), p) for k, p in P.items()}; fl = 0
    for _ in range(n):
        rows = []
        for k, (mt, p) in mats.items():
            tt = rngb.choice(full); rows.append(p[int(np.argmin(((mt - np.array([tt[x] / W_[x] for x in NAMES])) ** 2).sum(1)))]["row"])
        ok_, _, _ = judge(rows); fl += not ok_
    return fl / n
rngb = random.Random(940); rs = lambda v: [round(float(x), 3) for x in np.percentile(v, (5, 95))]; res = lambda P: {k: [rngb.choice(v) for _ in v] for k, v in P.items()}
out["ranges_90"] = {"neighbour choice": rs([boot_neighbour(res(pools), 1000, rngb) for _ in range(200)]), "a random pick from the engine's pool": rs([boot_rate(res(pools), 1000, rngb) for _ in range(200)]),
                    "a random pick from every build that lived": rs([boot_rate(res(ALIVE), 1000, rngb) for _ in range(200)]), "pool_sizes": {k: len(v) for k, v in pools.items()},
                    "note": "940: each pool resampled with replacement at its own size, 200 times; the 5th and 95th percentiles of the figure read on the resamples. 949 (749.124): 1,000 inner draws a resample for every figure, so a range is the pools' and not the inner draws'"}
# Window 201 (749.140): rhythm scaling read per build, in each pool and among every living build; and what a trial must not lose (builds, the words' fit).
RS = "rhythm scaling"
out["749.140"] = dict(kept_10th_25th_75th=[Q[RS][0], Q[RS][1], Q[RS][3]], pools={k: [round(c["row"][RS], 4) for c in p] for k, p in pools.items()}, living={k: [round(c["row"][RS], 4) for c in a] for k, a in ALIVE.items()},
                      living_builds={k: len(a) for k, a in ALIVE.items()}, living_median_rhythm_scaling={k: round(float(np.median([c["row"][RS] for c in a])), 3) for k, a in ALIVE.items()},
                      living_median_words_fit={k: round(float(np.median([c["f_all"] for c in a])), 3) for k, a in ALIVE.items()}, pool_median_words_fit={k: round(float(np.median([c["f_all"] for c in p])), 3) for k, p in pools.items()},
                      pool_spread_over_kept_spread=out["pool_spread_over_kept_spread_by_check"][RS])
# Window 200. 749.137: the pool figures with range left out of the rule. 749.134: the pools under a ceiling on the commonest pitch's share. Each with its own seeded draws, so the figures above are untouched.
def judge_on(rows, names): w = S.same_side(Q, rows, names, "wide"); h = S.same_side(Q, rows, names, "half"); return (not w and len(h) <= 2), [x[0] for x in w], [x[0] for x in h]
def rates(P, names, seed):
    r_ = random.Random(seed); fl = 0; hl = {}
    for _ in range(4000):
        ok_, _, h_ = judge_on([r_.choice(p)["row"] for p in P.values()], names); fl += not ok_
        for x in h_: hl[x] = hl.get(x, 0) + 1
    nf = 0
    for _ in range(1000):
        rows = []
        for p in P.values(): t_ = r_.choice(full); rows.append(min(p, key=lambda c: sum(((c["row"][n] - t_[n]) / W_[n]) ** 2 for n in names))["row"])
        nf += not judge_on(rows, names)[0]
    return dict(a_random_pick_from_the_pool_fails=round(fl / 4000, 3), neighbour_choice_fails=round(nf / 1000, 3), lean_past_25_75_share_by_check={k: round(v / 4000, 3) for k, v in sorted(hl.items(), key=lambda x: -x[1])[:5]})
NR = [n for n in NAMES if n != "range"]
out["749.137"] = dict(with_range=rates(pools, NAMES, 137), range_left_out=rates(pools, NR, 137), pool_range_quartiles={k: [float(x) for x in np.percentile([c["row"]["range"] for c in p], (25, 50, 75))] for k, p in pools.items()})
CE = json.load(open(os.path.join(ROOT, "studies", "commonest_pitch", "result.json")))["kept"]; cv, cc = CE["Verse"]["p10_25_50_75_90"][4], CE["Chorus"]["p10_25_50_75_90"][4]
under = {k: [c for c in p if c["cp"][0] <= cv and c["cp"][1] <= cc] for k, p in pools.items()}
def chosen(p, fl):
    if not p: return None
    nr = [c for c in p if fl is None or c["readings"]["range"] >= fl]; c = min(nr, key=lambda c: c["n"]) if nr else min(p, key=lambda c: (-c["readings"]["range"], c["n"]))
    return c
def tell(c): return None if c is None else dict(n=c["n"], range=int(c["readings"]["range"]), words_fit=round(c["f_all"], 3), commonest_pitch_verse=round(c["cp"][0], 3), commonest_pitch_chorus=round(c["cp"][1], 3), outside_middle_half=outside(c["row"]))
pk0 = {k: chosen(p, FLOOR[k]) for k, p in pools.items()}; pk1 = {k: chosen(p, FLOOR[k]) for k, p in under.items()}
out["749.134"] = dict(ceiling=dict(verse=cv, chorus=cc), pool_sizes={k: len(p) for k, p in pools.items()}, pool_sizes_under_the_ceiling={k: len(p) for k, p in under.items()},
                      living_builds_under_the_ceiling={k: round(float(np.mean([c["cp"][0] <= cv and c["cp"][1] <= cc for c in a])), 3) for k, a in ALIVE.items()},
                      chosen_without_the_ceiling={k: tell(c) for k, c in pk0.items()}, chosen_under_the_ceiling={k: tell(c) for k, c in pk1.items()},
                      chosen_without_sound=judge([c["row"] for c in pk0.values()])[0], chosen_under_sound=(judge([c["row"] for c in pk1.values()])[0] if all(pk1.values()) else None),
                      rates_under_the_ceiling=(rates(under, NAMES, 134) if all(under.values()) else None), rates_without=rates(pools, NAMES, 134))
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "neighbour" + ("_" + os.environ.get("TRIAL_NAME", "trial") if os.environ.get("MARGIN_TURNS_OF_FOUR") else os.environ.get("OUT_SUFFIX", "")) + ".json"), "w"), indent=1)
