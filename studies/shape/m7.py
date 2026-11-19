import sys, pickle, numpy as np, pandas as pd, warnings, re, os; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v22", "/home/claude/zeneng/corpus/v25", "/home/claude/rightrevjf/zeneng-pipeline/lib/luthier"]
os.chdir("/home/claude/zeneng/corpus/v22")
import fit as F
os.chdir("/home/claude/zeneng/corpus/v25")
import shapes as S
from scipy.stats import rankdata, pearsonr
def tiers(words):
    out = []
    for w, n in words:
        info = F.word_info(w)
        if info is None or len(info[0]) != n: out += [None] * n
        else:
            sy, z = info
            for st, fn in sy: out.append(0 if (fn and len(sy) == 1) else 2 if st else 1)
    return out
def cc1(A, B):
    A = A - A.mean(0); B = B - B.mean(0); qa = np.linalg.qr(A)[0]; qb = np.linalg.qr(B)[0]; return float(np.linalg.svd(qa.T @ qb, compute_uv=False)[0])
x = pickle.load(open("shapes.pkl", "rb")); rng = np.random.default_rng(0); rows = []
for k in F.kept_songs():
    tr = tiers(k["words"])
    if len(tr) != len(k["t"]): continue
    idx = np.array([i for i in range(len(tr)) if tr[i] is not None])
    if len(idx) < 60: continue
    t = np.asarray(k["t"], float) / 12; p = np.asarray(k["p"]); lines = np.asarray(k["lines"]); P = S.path(list(zip(t, p)))[idx]; ln = lines[idx]
    w = np.array([(0, .4, 1)[tr[i]] for i in idx]); Wd = np.c_[w, w == 0]; obs = cc1(Wd, P); sh = []
    for _ in range(100):
        o = np.arange(len(idx))
        for l in set(ln.tolist()):
            m = np.where(ln == l)[0]; o[m] = rng.permutation(m)
        sh.append(cc1(Wd[o], P))
    rows.append(dict(id=k["song"], M7=(obs - np.mean(sh)) / np.std(sh), M7raw=obs, n=len(idx)))
m = pd.DataFrame(rows); y = x.merge(m, on="id"); print("kept with words", len(m), "on the yardstick", len(y)); pickle.dump(y, open("m7.pkl", "wb"))
def partial(d, a, b):
    C = np.c_[np.ones(len(d)), rankdata(d.year), rankdata(d.notes)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, pv = pearsonr(res(rankdata(d[a])), res(rankdata(d[b]))); return round(float(r), 3), round(float(pv), 3), len(d)
for c in ("M7", "M7raw"):
    print(c, "G", partial(y, c, "G"), "A", partial(y[y.half == 0], c, "G"), "B", partial(y[y.half == 1], c, "G"), "love", partial(y, c, "love"), "covers", partial(y, c, "cover_rank"))
print("M7 z median", y.M7.median(), "share z>2", (y.M7 > 2).mean())
