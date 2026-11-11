"""v109 fixes 300 and 301 (on 286): realness leaves the family (a reading only, printed); the remaining six are read jointly on
the 515 POP909 pairs and, if the family passes under nine pairs in ten, its hard limits are refitted outward (the 1st/99th, then the
0.5th/99.5th, the 0.25th/99.75th, the 0.1st/99.9th) until it passes nine in ten. Writes limits_v109.json and the per-pair readings.
From song 40's:
v108 fix 286 for song 40: the soft (5th/95th) and hard (1st/99th) limits of six of the seven gates of fix 280, read on the
engine's calibration pairs (the spectral limits are the v108 file's, read on kept chart songs). Adapted from song 38's tableb_v2_p38.py.
Fixes 275 and 280 for song 38's rerun under v107: the pass rate of the gates the paper could not read on kept songs
(the five Table B readings, the rhythm band of 163 and the sequence-legs gate of 148), run with the engine's own functions on its
calibration pairs: the 515 major-key POP909 songs with a labelled verse and chorus (Dai et al. 2020 labels; Wang et al. 2020 corpus),
the pairs Table B's floors were set on (pop/calib_pop.py). Each gate as song 38's search applies it; then the share that pass all seven.
Usage: python3 tableb_v2_p38.py   (writes tableb_v2.json)"""
import sys, os, json, math, random, collections
import numpy as np
sys.path[:0] = ["/home/claude/pop", "/home/claude/carol"]
import calib_pop as CP
from measures import beta_pitch, cmp_score, m_horizon, PPM, ic_profile, feature_vec
CAL = json.load(open("/home/claude/pop/pop_calibration.json")); C = CAL["cal"]
T = json.load(open("/home/claude/p36/tables/zeneng_v88_tables.json"))
RT = T["rhythm_tables"]["pop_rock_country"]["4/4"]["table"]; RT = json.loads(RT) if isinstance(RT, str) else RT
RBAND = T["surprise_bands_rhythm"]["pop_hooktheory"]["4/4"]["rhythm_bits_per_note"]
BEAT, BAR = 12, 48

refs = [r for r in (CP.load(s) for s in sorted(os.listdir(CP.ROOT)) if s.isdigit()) if r]
random.seed(9); idx = list(range(len(refs))); random.shuffle(idx); folds = [idx[i::5] for i in range(5)]
for f in folds:                                                       # as calib_pop: each chorus read by a model that never saw its song
    model = PPM(3); model.train([PPM.symbols(refs[i]["all"], refs[i]["tonic"]) for i in idx if i not in f])
    for i in f:
        r = refs[i]; tune = r["V"] + [(on + 4 * r["vbars"], d, p) for on, d, p in r["C"]]
        bits = model.bits(PPM.symbols(tune, r["tonic"])); ps = [p for *_, p in r["C"]]
        r["ic"], _ = ic_profile(bits[len(r["V"]):], ps.index(max(ps)))
F = np.array([feature_vec(r["C"], r["tonic"], 4) for r in refs]); Z = (F - np.array(CAL["mu"])) / np.array(CAL["sd"])
D = np.sqrt(((Z[:, None, :] - Z[None, :, :]) ** 2).sum(-1)); np.fill_diagonal(D, np.inf); knn = np.sort(D, 1)[:, :10].mean(1)
def rhythm_bits(ns, end):
    ons = [int(round(on * BEAT)) for on, _, _ in ns] + [end]; out = []
    for a, b2 in zip(ons, ons[1:]): out.append(-math.log2(max(1e-9, RT[a % BAR][min(96, b2 - a)])))
    return float(np.mean(out))
def sequences(ns, nbars):
    by = collections.OrderedDict((b, []) for b in range(nbars))
    for on, _, p in ns:
        t = int(round(on * BEAT)); b = t // BAR
        if b in by: by[b].append((t - b * BAR, p))
    legs = []; run = 1; ks = list(by)
    for a, b2 in zip(ks, ks[1:]):
        A_, B_ = by[a], by[b2]
        same = b2 == a + 1 and len(A_) == len(B_) >= 2 and [t for t, _ in A_] == [t for t, _ in B_] and len({y - x for (_, x), (_, y) in zip(A_, B_)}) == 1 and A_ != B_
        if same: run += 1
        else:
            if run >= 2: legs.append(run)
            run = 1
    if run >= 2: legs.append(run)
    return legs
rows = []
for i, r in enumerate(refs):
    t = r["tonic"]; tune = r["V"] + [(on + 4 * r["vbars"], d, p) for on, d, p in r["C"]]
    beta = beta_pitch(tune); cmp_, _ = cmp_score(tune, 4, t); mh = m_horizon(r["C"], r["V"])[0]
    real = sum(1 for x in CAL["real_knn"] if x >= knn[i]) / len(CAL["real_knn"])
    nb = r["vbars"] + r["cbars"]; rb = rhythm_bits(tune, nb * BAR)
    g = {"spectral": beta is not None and C["beta"]["p05"] <= beta <= C["beta"]["p95"], "cmp": cmp_ >= C["cmp"]["p05"], "memory": mh >= C["mh"]["p05"],
         "surprisal": r["ic"] >= C["ic"]["p05"], "realness": real >= C["realness"]["p05"], "rhythm band (163)": RBAND["p05"] <= rb <= RBAND["p95"],
         "sequence legs (148)": not any(l >= 3 for l in sequences(tune, nb))}
    g["_vals"] = dict(cmp=cmp_, mh=mh, ic=r["ic"], real=real, rbits=rb, seq_max=max(sequences(tune, nb) or [1]), beta=beta)
    rows.append(g)
vals = [g.pop("_vals") for g in rows]; names = list(rows[0]); out = dict(corpus="POP909 (Wang et al. 2020), the 515 major-key songs with a labelled verse and chorus (Dai et al. 2020 labels): "
                                         "the engine's calibration pairs for Table B, read on the whole first verse and chorus runs as the calibration was",
                                  pairs=len(rows), alone={k: round(float(np.mean([g[k] for g in rows])), 3) for k in names},
                                  table_b_together=round(float(np.mean([all(g[k] for k in names[:5]) for g in rows])), 3),
                                  all_seven=round(float(np.mean([all(g.values()) for g in rows])), 3),
                                  breaks=dict(collections.Counter(sum(not v for v in g.values()) for g in rows)))
P = lambda k, q: round(float(np.percentile([v[k] for v in vals if v[k] is not None], q)), 4)
out["limits"] = {"cmp": dict(direction="at least", soft=P("cmp", 5), hard=P("cmp", 1)), "memory": dict(direction="at least", soft=P("mh", 5), hard=P("mh", 1)),
                 "surprisal": dict(direction="at least", soft=P("ic", 5), hard=P("ic", 1)), "realness": dict(direction="at least", soft=P("real", 5), hard=P("real", 1)),
                 "rhythm band": dict(direction="between", soft=[P("rbits", 5), P("rbits", 95)], hard=[P("rbits", 1), P("rbits", 99)]),
                 "sequence legs": dict(direction="at most", soft=P("seq_max", 95), hard=P("seq_max", 99))}
out["table_b_floors_as_coded"] = dict(cmp=C["cmp"]["p05"], mh=C["mh"]["p05"], ic=C["ic"]["p05"], realness=C["realness"]["p05"], rhythm_hooktheory=[RBAND["p05"], RBAND["p95"]])


SR = json.load(open("/home/claude/p40/tables/zeneng_v108_spectral_and_registers.json"))
SPx = SR["spectral reading (the engine's beta_pitch on Verse 1 then the first 8 bars of Chorus 1)"]
import numpy as _np
def pc(k, q): return float(_np.percentile([v[k] for v in vals if v[k] is not None], q))
KEYS = {"spectral": "beta", "cmp": "cmp", "memory": "mh", "surprisal": "ic", "rhythm band": "rbits", "sequence legs": "seq_max"}
DIR = {"spectral": "between", "cmp": "at least", "memory": "at least", "surprisal": "at least", "rhythm band": "between", "sequence legs": "at most"}
def limits(hq):
    L = {}
    for k, key in KEYS.items():
        if k == "spectral": L[k] = (DIR[k], SPx["soft limits (kept 5th, 95th)"], SPx["hard limits (kept 1st, 99th)"] if hq == 1 else [round(pc(key, hq), 4), round(pc(key, 100 - hq), 4)] if hq < 1 else SPx["hard limits (kept 1st, 99th)"])
        elif DIR[k] == "between": L[k] = (DIR[k], [round(pc(key, 5), 4), round(pc(key, 95), 4)], [round(pc(key, hq), 4), round(pc(key, 100 - hq), 4)])
        elif DIR[k] == "at least": L[k] = (DIR[k], round(pc(key, 5), 4), round(pc(key, hq), 4))
        else: L[k] = (DIR[k], round(pc(key, 95), 4), round(pc(key, 100 - hq), 4))
    if hq < 1:                                                                        # the spectral hard limits widen with the rest, on the pairs
        L["spectral"] = (DIR["spectral"], SPx["soft limits (kept 5th, 95th)"], [min(SPx["hard limits (kept 1st, 99th)"][0], round(pc("beta", hq), 4)), max(SPx["hard limits (kept 1st, 99th)"][1], round(pc("beta", 100 - hq), 4))])
    return L
def breaks(v, L):
    soft, hard = [], []
    for k, (d, sl, hl) in L.items():
        x = v[KEYS[k]]
        if x is None: hard.append(k); continue
        if d == "between": s_, h_ = not (sl[0] <= x <= sl[1]), not (hl[0] <= x <= hl[1])
        elif d == "at least": s_, h_ = x < sl - 1e-9, x < hl - 1e-9
        else: s_, h_ = x > sl + 1e-9, x > hl + 1e-9
        (hard if h_ else soft if s_ else []).append(k)
    return soft, hard
steps = []
for hq in (1, 0.5, 0.25, 0.1):
    L = limits(hq); per = [breaks(v, L) for v in vals]
    joint = float(_np.mean([not h and len(s) < 3 for s, h in per]))
    steps.append(dict(hard_percentile=hq, joint=round(joint, 4), hard_any=sum(bool(h) for s, h in per), limits=L))
    if joint >= 0.9: break
real = [v["real"] for v in vals]
OUT = dict(corpus=out["corpus"], pairs=len(vals), family="the six of 286 without realness (300)", steps=steps, chosen=steps[-1],
           realness=dict(reading_only=True, pairs_percentiles=[round(pc("real", q), 4) for q in (5, 25, 50, 75, 95)], kept_chart=[0.004, 0.029, 0.088, 0.303, 0.636]))
json.dump(OUT, open("/home/claude/p41/limits_v109.json", "w"), indent=1)
json.dump(vals, open("/home/claude/p41/limits_v109_pairs.json", "w"))
print(json.dumps({k: OUT[k] for k in ("steps",)}, indent=1)[:3000])
