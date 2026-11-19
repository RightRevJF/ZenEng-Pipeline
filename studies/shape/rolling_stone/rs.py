import sys, os, re, glob, pickle, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v22", "/home/claude/zeneng/corpus/v25", "/home/claude/rightrevjf/zeneng-pipeline/lib/luthier", "/home/claude/rightrevjf/zeneng-pipeline/studies/ssm"]
os.chdir("/home/claude/zeneng/corpus/v22"); import fit as F; os.chdir("/home/claude/zeneng/corpus/v27"); import shapes as S, ssm_lib as L
from scipy.stats import rankdata, pearsonr
def read(path):
    R = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8", errors="ignore") if l.strip() and not l.startswith("!!")]; head = next(r for r in R if r[0].startswith("**"))
    if "**silbe" not in head: return None
    k, s, st = head.index("**kern"), head.index("**silbe"), head.index("**stress")
    t = 0.0; tb = None; bar = -1; t0 = 0.0; out = []
    for r in R[R.index(head) + 1:]:
        if len(r) <= max(k, s, st): continue
        a = r[k]
        if a.startswith("*"):
            for x in r:
                m = re.match(r"\*tb(\d+)", x)
                if m: tb = int(m.group(1))
            continue
        if a.startswith("!"): continue
        if a.startswith("="): bar += 1; t0 = t; continue
        if not tb: return None
        if a not in (".", "") and "r" not in a and L.kern_pitch(a) is not None and not a.startswith("]") and "_" not in a: out.append((4.0 * max(bar, 0) + (t - t0), L.kern_pitch(a), r[s], r[st]))
        t += 4.0 / tb
    return out
def cc1(A, B):
    A = A - A.mean(0); B = B - B.mean(0); return float(np.linalg.svd(np.linalg.qr(A)[0].T @ np.linalg.qr(B)[0], compute_uv=False)[0])
def coupled(w, P, ln, rng):
    Wd = np.c_[w, w == 0] if (w == 0).any() and not (w == 0).all() else w[:, None]; obs = cc1(Wd, P); sh = []
    for _ in range(200):
        o = np.arange(len(w))
        for l in set(ln.tolist()):
            q = np.where(ln == l)[0]; o[q] = rng.permutation(q)
        sh.append(cc1(Wd[o], P))
    return (obs - np.mean(sh)) / (np.std(sh) + 1e-9), obs
x = pickle.load(open("/home/claude/zeneng/corpus/v25/shapes.pkl", "rb")); x = x[x.src == "RS"]; rng = np.random.default_rng(0); rows = []
for r in x.itertuples():
    N = read(f"/home/claude/corpus/try2/CoCoPops/RollingStone/Data/{r.id}.hum")
    if not N: continue
    t = np.array([n[0] for n in N]); p = np.array([n[1] for n in N]); syl = [n[2] for n in N]; mark = [n[3] for n in N]
    words = []; cur = ""; n = 0
    for sx in syl:
        z = sx.strip(); cur += re.sub(r"[^A-Za-z']", "", z); n += 1
        if not z.endswith("-"): words.append((cur, n)); cur = ""; n = 0
    if n: words.append((cur, n))
    tr = []
    for w, n in words:
        info = F.word_info(w) if w else None
        tr += [None] * n if (info is None or len(info[0]) != n) else [0 if (fn and len(info[0]) == 1) else 2 if stt else 1 for stt, fn in info[0]]
    lines = np.cumsum([1 if (i and t[i] - t[i - 1] >= 2) else 0 for i in range(len(t))]); P = S.path(list(zip(t, p))); d = dict(src="RS", id=r.id, nsyl=len(t))
    idx = np.array([i for i in range(len(tr)) if tr[i] is not None])
    if len(idx) >= 60: d["M7"], d["M7r"] = coupled(np.array([(0, .4, 1)[tr[i]] for i in idx]), P[idx], lines[idx], rng); d["known"] = len(idx)
    ix = np.array([i for i in range(len(mark)) if mark[i].strip().isdigit()])
    if len(ix) >= 60 and len(set(mark[i] for i in ix)) > 1: d["M7s"], _ = coupled(np.array([float(mark[i]) for i in ix]), P[ix], lines[ix], rng)
    rows.append(d)
y = x.merge(pd.DataFrame(rows), on=["src", "id"]); pickle.dump(y, open("rs.pkl", "wb")); print("songs", len(y), "with M7", int(y.M7.notna().sum()), "with M7s", int(y.M7s.notna().sum()), "| share above their shuffles (z>2): M7", round((y.M7 > 2).mean(), 2), "M7s", round((y.M7s > 2).mean(), 2))
def partial(d, m, g):
    d = d.dropna(subset=[m, g]); C = np.c_[np.ones(len(d)), rankdata(d.year), rankdata(d.notes)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, pv = pearsonr(res(rankdata(d[m])), res(rankdata(d[g]))); return round(float(r), 3), round(float(pv), 4), len(d)
out = {}
for m in ("M7", "M7r", "M7s"):
    out[m] = dict(A=partial(y[y.half == 0], m, "G"), B=partial(y[y.half == 1], m, "G"), pooled=partial(y, m, "G"), love=partial(y, m, "love"), covers=partial(y, m, "cover_rank")); print(m, out[m])
json.dump(out, open("rs_results.json", "w"), indent=1)
