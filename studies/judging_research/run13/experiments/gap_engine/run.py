"""gap_engine: real 4/4 Hooktheory clips vs the metre engine's survivors (songs 50, 54, 55, 58, 60, 61, 62, 66). No outcome read.
Also writes the cross-fitted realness model inputs for realness_covers (models trained per artist half)."""
import os, sys, json, glob, random, hashlib, collections
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import features13 as F
SONGS = ["50", "54", "55", "58", "60", "61", "62", "66"]; CAP = 150
H = json.load(open("/home/claude/dl/run13/hook_feats.json")); names = sorted(next(iter(H.values()))["f"])
real = [(v["f"], "A:" + v["artist"], v["half"]) for v in H.values()]
eng, picks = [], []
for s in SONGS:
    d = json.load(open(f"/home/claude/dl/run13/b_{s}.json")); rnd = random.Random(int(s)); bl = d["builds"][:]; rnd.shuffle(bl)
    for b in bl[:CAP]:
        for sec, (ns, t) in F.from_engine_build(b, d["BEAT"]).items():
            f = F.base(ns, t)
            if f: eng.append((f, "E:" + s, -1))
    sj = json.load(open(d["song"] if os.path.isabs(d["song"]) else os.path.join("/home/claude/mainro", d["song"])))
    secs = collections.OrderedDict()
    for n in sj["melody"]["notes"]: secs.setdefault(n["sec"], []).append((n["on"] / 12, n["dur"] / 12, n["midi"]))
    for sec, ns in secs.items():
        f = F.base(ns, sj["key"]["tonic_midi"] % 12)
        if f: picks.append((f, "P:" + s, sec))
def mat(rows):
    X = np.array([[r[0][n] for n in names] for r in rows], float); return X
Xr, Xe, Xp = mat(real), mat(eng), mat(picks)
X = np.vstack([Xr, Xe]); y = np.r_[np.ones(len(Xr)), np.zeros(len(Xe))]; g = np.array([r[1] for r in real] + [r[1] for r in eng])
med = np.nanmedian(X, 0); X = np.where(np.isfinite(X), X, med); mu, sd = X.mean(0), X.std(0) + 1e-12; Z = (X - mu) / sd
w = np.where(y == 1, 0.5 / y.mean(), 0.5 / (1 - y.mean()))
oof = np.zeros(len(y)); gkf = GroupKFold(n_splits=8)
# make each engine song its own fold: assign groups so the 8 engine songs fall in 8 different folds
for tr, te in gkf.split(Z, y, g):
    m = LogisticRegression(C=1.0, max_iter=3000).fit(Z[tr], y[tr], sample_weight=w[tr]); oof[te] = m.decision_function(Z[te])
auc = roc_auc_score(y, oof)
eng_fold = {s: int(np.mean(oof[g == "E:" + s] > np.median(oof[y == 1]))) for s in SONGS}
full = LogisticRegression(C=1.0, max_iter=3000).fit(Z, y, sample_weight=w)
coef = dict(zip(names, full.coef_[0].tolist()))
per = {}
for j, n in enumerate(names):
    a = roc_auc_score(y, X[:, j]); sgn = []
    for s in SONGS:
        m_ = np.r_[np.ones(len(Xr), bool), (g[len(Xr):] == "E:" + s)]; sgn.append(np.sign(roc_auc_score(y[m_], X[m_, j]) - 0.5))
    per[n] = dict(auc=float(a), real_median=float(np.median(X[y == 1, j])), engine_median=float(np.median(X[y == 0, j])),
                  real_q10_q90=[float(np.quantile(X[y == 1, j], .1)), float(np.quantile(X[y == 1, j], .9))],
                  picks_median=float(np.nanmedian(Xp[:, j])) if len(Xp) else None, songs_same_sign=int(max(sum(x > 0 for x in sgn), sum(x < 0 for x in sgn))), coef=coef[n])
gap = sorted([n for n in names if abs(per[n]["auc"] - 0.5) >= 0.15 and per[n]["songs_same_sign"] >= 7], key=lambda n: -abs(per[n]["auc"] - 0.5))
pk = (Xp - mu) / sd; pk = np.where(np.isfinite(pk), pk, 0); pick_scores = full.decision_function(pk)
P = dict(P1_auc_at_least_0_90=bool(auc >= 0.90),
         P2_top_pc_share_engine_above_real=bool(per["top_pc_share"]["engine_median"] > per["top_pc_share"]["real_median"]),
         P3_rhythm_minus_pitch_rep_real_above_engine=bool(per["rhythm_minus_pitch_rep"]["real_median"] > per["rhythm_minus_pitch_rep"]["engine_median"]),
         P4_real_bar_rhythm_rep_above_bar_interval_rep=bool(per["bar_rhythm_rep"]["real_median"] > per["bar_interval_rep"]["real_median"]),
         P5_real_phrase_range_7_to_11=bool(7 <= per["phrase_range"]["real_median"] <= 11))
out = dict(real_clips=len(Xr), engine_sections=len(Xe), engine_songs=SONGS, picks_sections=len(Xp), oof_auc=float(auc),
           engine_song_share_above_real_median=eng_fold, predictions=P, gap_list=gap,
           per_feature=per, picks_realness_log_odds_median=float(np.median(pick_scores)), real_oof_median=float(np.median(oof[y == 1])), engine_oof_median=float(np.median(oof[y == 0])))
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1)
print("AUC", round(auc, 3), P); print("gap list:")
for n in gap: print(f"  {n}: AUC {per[n]['auc']:.3f} real {per[n]['real_median']:.3f} engine {per[n]['engine_median']:.3f} picks {per[n]['picks_median']:.3f} songs {per[n]['songs_same_sign']}/8")
# inputs for realness_covers: engine matrix and real matrix with halves (notes only)
np.savez("/home/claude/dl/run13/realness_inputs.npz", Xr=Xr, Xe=Xe, half=np.array([r[2] for r in real]), names=np.array(names))
