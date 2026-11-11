"""Fixes 275 and 280 for song 38's rerun under v107: the pass rate of the gates the paper could not read on kept songs
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
    rows.append(g)
names = list(rows[0]); out = dict(corpus="POP909 (Wang et al. 2020), the 515 major-key songs with a labelled verse and chorus (Dai et al. 2020 labels): "
                                         "the engine's calibration pairs for Table B, read on the whole first verse and chorus runs as the calibration was",
                                  pairs=len(rows), alone={k: round(float(np.mean([g[k] for g in rows])), 3) for k in names},
                                  table_b_together=round(float(np.mean([all(g[k] for k in names[:5]) for g in rows])), 3),
                                  all_seven=round(float(np.mean([all(g.values()) for g in rows])), 3),
                                  breaks=dict(collections.Counter(sum(not v for v in g.values()) for g in rows)))
json.dump(out, open("/home/claude/p38/tableb_v2.json", "w"), indent=1); print(json.dumps(out, indent=1))
