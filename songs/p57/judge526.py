"""526: song 47 read first by a judge that has not seen it (v131, the other AI's specification): the judge of record's 37 measures; median
fill (the fitting set's), z-scored, L2 logistic, C = 0.3, kept and build sides weighted alike; windows: the first verse's and first chorus's
first eight bars, the engine's own reading (519: the run's stored window readings, and cand() for the four stream measures on the same
notes); kept side: CoCoPops and BiMMuDa 1958-1991 (zeneng_v131_kept_windows.json), split in half by piece, fitted on one half and tested on
the other, eight splits, mean and spread; the songs before it: 40, 42, 43, 44, 45 (v129) and 46 (v130) at their code of record. Song 47 is
scored by a judge fitted on all six; each of the six by a judge refitted on the other five. Main and control apart. First 400 complete builds.
Usage: python3 judge526.py OUT.json"""
import sys, json, pickle, collections
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
OUT = sys.argv[1]
KW = json.load(open("/home/claude/p57/tables/zeneng_v131_kept_windows.json")); MS = KW["measures"]; assert len(MS) == 37
assert MS == json.load(open("/home/claude/p55/tables/zeneng_v129_judge.json"))["content_judge"]["measures"]
ns_ = {"np": np, "collections": collections}
exec([v for k, v in json.load(open("/home/claude/p55/tables/zeneng_v121_blind_spots.json")).items() if k.startswith("code: cand")][0], ns_); cand = ns_["cand"]
KX = np.array([[np.nan if w[m] is None else w[m] for m in MS] for w in KW["windows"]], float); PIECE = [w["piece"] for w in KW["windows"]]; PIECES = sorted(set(PIECE))
RUNS = {"40": "/home/claude/p55/part1/melody_v129_p40", "42": "/home/claude/p55/part1/melody_v129_p42", "43": "/home/claude/p55/part1/melody_v129_p43",
        "44": "/home/claude/p55/part1/melody_v129_p44", "45": "/home/claude/p55/part1/melody_v129_p45", "46": "/home/claude/p56/run/melody_v130_p56", "47": "/home/claude/p57/run/melody_v131_p57"}
EARLIER = ["40", "42", "43", "44", "45", "46"]
def builds(pre, mode):
    D = pickle.load(open(f"{pre}_{mode}.pkl", "rb")); st = {}; b = 0
    for nm, kind, nb in D["form"]: st[nm] = b; b += nb
    Al = [x for x in D["all"] if x["read"]["v"] and x["read"]["c"]][:400]; rows = []
    for x in Al:
        for w, sec in (("v", "Verse 1"), ("c", "Chorus 1")):
            f = dict(x["read"][w]); b0 = st[sec]
            N = sorted(((t[0] - b0 * 48) / 12, t[1] / 12, t[2]) for t in x["notes"] if b0 * 48 <= t[0] < (b0 + 8) * 48)
            c = cand(N) or {}
            rows.append([(f.get(m) if m in f else c.get(m)) for m in MS])
    return np.array([[np.nan if v is None else v for v in r] for r in rows], float), len(Al)
def fit_auc(Ktr, Btr, Kte, Bte):
    X = np.vstack([Ktr, Btr]); med = np.nanmedian(X, 0); med = np.where(np.isfinite(med), med, 0.0)
    fill = lambda A: np.where(np.isfinite(A), A, med)
    X = fill(X); mu, sd = X.mean(0), X.std(0) + 1e-9; y = np.r_[np.ones(len(Ktr)), np.zeros(len(Btr))]
    lr = LogisticRegression(C=0.3, max_iter=5000, class_weight="balanced").fit((X - mu) / sd, y)
    Xt = fill(np.vstack([Kte, Bte])); yt = np.r_[np.ones(len(Kte)), np.zeros(len(Bte))]
    return float(roc_auc_score(yt, lr.decision_function((Xt - mu) / sd)))
res = {"about": __doc__.split("Usage")[0].strip(), "measures": MS, "kept": dict(windows=len(KX), pieces=len(PIECES)), "draws": {}}
for mode in ("main", "ctl"):
    B = {s: builds(p, mode) for s, p in RUNS.items()}
    out = {"builds read": {s: n for s, (_, n) in B.items()}, "splits": []}
    rs = np.random.RandomState(20261113)
    for k in range(8):
        perm = rs.permutation(len(PIECES)); A = {PIECES[j] for j in perm[: len(PIECES) // 2]}; ka = np.array([p in A for p in PIECE])
        row = {}
        row["47 (fitted on 40-46)"] = fit_auc(KX[ka], np.vstack([B[s][0] for s in EARLIER]), KX[~ka], B["47"][0])
        for h in EARLIER:
            row[f"{h} (fitted on the other five)"] = fit_auc(KX[ka], np.vstack([B[s][0] for s in EARLIER if s != h]), KX[~ka], B[h][0])
        out["splits"].append(row)
    out["mean and spread"] = {k: (round(float(np.mean([r[k] for r in out["splits"]])), 3), round(float(np.std([r[k] for r in out["splits"]])), 3)) for k in out["splits"][0]}
    res["draws"][mode] = out
    print(mode, out["mean and spread"])
json.dump(res, open(OUT, "w"), indent=1)
