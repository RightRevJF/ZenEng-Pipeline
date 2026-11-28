"""Notes-side: CANAL (canalization) on the 226 two-file Lakh songs. Per file, duration-weighted pitch-class profile over tracks 1,2,4;
CANAL = 1 - min over 12 rotations of JSD (bits) between the two files' profiles. Near-duplicate pairs (JSD < 1e-4) flagged.
Readings: rotation chosen (0 = same key), Spearman with the pair's mean PCE_ALL and NPB. Writes /home/claude/dl/run12/inventor_canal_check.json."""
import json, sys, numpy as np
from scipy.stats import spearmanr
from multiprocessing import Pool
sys.path.insert(0, "."); import inventor_rough_check as M
def prof(path):
    z = np.load(path); T = len(z["downbeat"]); hm = np.zeros((T, 128), bool)
    for k in (1, 2, 4):
        r = M.roll(z, k, T)
        if r is not None: hm |= r
    w = np.array([hm[:, pc::12].sum() for pc in range(12)], float); return w / w.sum() if w.sum() else None
def H(p): p = p[p > 0]; return -(p * np.log2(p)).sum()
def jsd(p, q): m = (p + q) / 2; return H(m) - (H(p) + H(q)) / 2
def job(s):
    fs = M.files(s)[:2]
    if len(fs) < 2: return None
    p, q = prof(fs[0]), prof(fs[1]); a, b = M.measure(fs[0]), M.measure(fs[1])
    if p is None or q is None or not a or not b: return None
    js = [jsd(p, np.roll(q, k)) for k in range(12)]; k = int(np.argmin(js))
    return dict(CANAL=1 - js[k], rot=k, PCE=(a["PCE_ALL"] + b["PCE_ALL"]) / 2, NPB=(a["NPB"] + b["NPB"]) / 2)
S = json.load(open("/home/claude/dl/run12/lakh_notes_side.json")); pairs = [s for s in S if len(s["md5s"]) >= 2]
with Pool(2) as P: R = [x for x in P.map(job, pairs) if x]
nd = [x for x in R if x["CANAL"] < 1 - 1e-4]
c = np.array([x["CANAL"] for x in nd])
out = dict(pairs=len(R), non_dup=len(nd), same_key_share=round(float(np.mean([x["rot"] == 0 for x in nd])), 3),
           CANAL_q10_50_90=[round(float(v), 4) for v in np.percentile(c, [10, 50, 90])],
           rho_CANAL_PCE=round(float(spearmanr(c, [x["PCE"] for x in nd])[0]), 3), rho_CANAL_NPB=round(float(spearmanr(c, [x["NPB"] for x in nd])[0]), 3))
json.dump(out, open("/home/claude/dl/run12/inventor_canal_check.json", "w"), indent=1); print(json.dumps(out, indent=1))
