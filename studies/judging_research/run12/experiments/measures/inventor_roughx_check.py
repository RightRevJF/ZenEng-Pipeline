"""Notes-side, round 2: ROUGH_X = ROUGH with octave-multiple pairs (|p-q| % 12 == 0) removed from numerator and denominator.
Stability on non-duplicate two-file songs (pc-profile JSD >= 1e-4); Spearman with mean sounding pitch (register) and octave-pair share.
Writes /home/claude/dl/run12/inventor_roughx_check.json."""
import json, sys, numpy as np
from scipy.stats import spearmanr
from multiprocessing import Pool
sys.path.insert(0, "."); import inventor_rough_check as M
class Cn:
    @staticmethod
    def prof(path):
        z = np.load(path); T = len(z["downbeat"]); hm = np.zeros((T, 128), bool)
        for k in (1, 2, 4):
            r = M.roll(z, k, T)
            if r is not None: hm |= r
        w = np.array([hm[:, pc::12].sum() for pc in range(12)], float); return w / w.sum() if w.sum() else None
    @staticmethod
    def jsd(p, q):
        H = lambda v: -(v[v > 0] * np.log2(v[v > 0])).sum(); m = (p + q) / 2; return H(m) - (H(p) + H(q)) / 2
def mx(path):
    z = np.load(path); T = len(z["downbeat"]); allm = np.zeros((T, 128), bool)
    for k in (1, 2, 3, 4):
        r = M.roll(z, k, T)
        if r is not None: allm |= r
    num = pairs = octp = 0.0; reg = []
    for row in allm[::24]:
        ps = np.flatnonzero(row)
        if len(ps) == 0: continue
        reg.append(ps.mean())
        if len(ps) < 2: continue
        d = np.abs(ps[:, None] - ps[None, :]); keep = (d % 12 != 0); iu = np.triu(np.ones_like(d, bool), 1)
        num += M.R[np.ix_(ps, ps)][keep & iu].sum(); pairs += (keep & iu).sum(); octp += ((~keep) & iu).sum()
    return dict(RX=num / pairs if pairs else None, REG=float(np.mean(reg)), OCT=octp / (octp + pairs) if pairs else None)
def job(s):
    fs = M.files(s)[:2]
    if len(fs) < 2: return None
    p, q = Cn.prof(fs[0]), Cn.prof(fs[1])
    if p is None or q is None: return None
    if min(Cn.jsd(p, np.roll(q, k)) for k in range(12)) < 1e-4: return None
    a, b = mx(fs[0]), mx(fs[1]); return (a, b) if a["RX"] and b["RX"] else None
if __name__ == "__main__":
  S = json.load(open("/home/claude/dl/run12/lakh_notes_side.json")); pairs = [s for s in S if len(s["md5s"]) >= 2]
  with Pool(2) as P: R = [x for x in P.map(job, pairs) if x]
  m = lambda k: [(a[k] + b[k]) / 2 for a, b in R]
  out = dict(pairs=len(R), stab_RX=round(float(spearmanr([a["RX"] for a, _ in R], [b["RX"] for _, b in R])[0]), 3),
             stab_REG=round(float(spearmanr([a["REG"] for a, _ in R], [b["REG"] for _, b in R])[0]), 3),
             rho_RX_REG=round(float(spearmanr(m("RX"), m("REG"))[0]), 3), rho_RX_OCT=round(float(spearmanr(m("RX"), m("OCT"))[0]), 3))
  json.dump(out, open("/home/claude/dl/run12/inventor_roughx_check.json", "w"), indent=1); print(json.dumps(out, indent=1))
  