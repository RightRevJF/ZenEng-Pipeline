import sys, os, json, pickle, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v26", "/home/claude/zeneng/corpus/v25"]
os.chdir("/home/claude/zeneng/corpus/v26"); import build as Bd; os.chdir("/home/claude/zeneng/corpus/v31")
from scipy.stats import rankdata, pearsonr, norm as N
def dfa(x):
    x = np.asarray(x, float); n = len(x)
    if n < 128 or x.std() == 0: return np.nan
    y = np.cumsum(x - x.mean()); sizes = np.unique(np.round(np.geomspace(4, n // 4, 12)).astype(int)); F = []
    for s in sizes:
        k = n // s; seg = y[:k * s].reshape(k, s); t = np.arange(s); t = t - t.mean(); b = (seg * t).sum(1) / (t ** 2).sum(); r = seg - seg.mean(1, keepdims=True) - b[:, None] * t; F.append(np.sqrt((r ** 2).mean()))
    return float(np.polyfit(np.log(sizes), np.log(F), 1)[0])
def both(t, p):
    t = np.asarray(t, float); p = np.asarray(p, float); return dfa(p), dfa(np.log2(np.clip(np.diff(t), .0625, 16)))
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb")); byid = {(s["src"], s["id"]): s for s in G}
s1 = pickle.load(open("/home/claude/zeneng/corpus/v25/shapes.pkl", "rb")); s2 = pickle.load(open("/home/claude/zeneng/corpus/v26/fresh_graded.pkl", "rb")); s3 = pd.read_pickle("/home/claude/zeneng/corpus/v30/set3.pkl")
r1 = []
for r in s1.itertuples():
    c = max(byid[(r.src, r.id)]["clips"], key=len); r1.append(both([n[0] for n in c], [n[1] for n in c]))
r2 = []
for r in s2.itertuples():
    t, p, tr, lines = Bd.read(Bd.D + "syllable_level_npy_39/" + r.file); r2.append(both(t, p))
L = {}
for ln in open("/home/claude/corpus/parsed_lakh.jsonl"):
    r = json.loads(ln); L[r["id"]] = r
r3 = []
for r in s3.itertuples():
    ns = sorted({(float(n["off"]), int(n["p"])) for s in L[r.id]["melody"]["sections"] for n in s["notes"] if "off" in n}); r3.append(both([n[0] for n in ns], [n[1] for n in ns]))
sets = []
for d, rr in ((s1, r1), (s2, r2), (s3, r3)):
    d = d.copy(); d["Sp"] = [a for a, b in rr]; d["Sr"] = [b for a, b in rr]; d["nearp"] = -(d.Sp - 1).abs(); d["nearr"] = -(d.Sr - 1).abs(); sets.append(d)
pickle.dump(sets, open("s_sets.pkl", "wb"))
def part(d, m, g):
    d = d.dropna(subset=[m, g]); C = [np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + ([(d.src == s).astype(float).values for s in ("CB", "RS", "BM")] if "src" in d and d.src.nunique() > 1 else []); C = np.c_[tuple(C)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(d[m])), res(rankdata(d[g]))); return float(r), float(p), len(d)
for i, d in enumerate(sets): print(f"set {i+1}: songs with S {int(d.Sp.notna().sum())}; Sp quartiles {d.Sp.quantile([.25,.5,.75]).round(3).tolist()}  g = pi(S-1) at the median {np.pi*(d.Sp.median()-1):+.2f}; Sr quartiles {d.Sr.quantile([.25,.5,.75]).round(3).tolist()}")
out = {}
for name, m in (("P1 Sp rises", "Sp"), ("P2 Sp near 1", "nearp"), ("P3 Sr near 1", "nearr"), ("(Sr rises)", "Sr")):
    R = [part(d, m, "G") for d in sets]; z = sum(np.sign(r) * N.isf(p / 2) * np.sqrt(n) for r, p, n in R) / np.sqrt(sum(n for _, _, n in R)); pp = 2 * N.sf(abs(z)); ok = all(r > 0 for r, _, _ in R) and sum(p < .05 for _, p, _ in R) >= 2 and pp < .017
    out[name] = dict(sets=[(round(r, 3), round(p, 4), n) for r, p, n in R], pooled_z=round(float(z), 2), pooled_p=round(float(pp), 4), love=[round(part(d, m, "love")[0], 3) for d in sets], covers=[round(part(d, m, "cover_rank")[0], 3) for d in sets], verdict="PASS" if ok else "fail"); print(name, out[name])
# the shape of the relation: G by fifths of Sp, sets pooled after ranking G within set
allr = pd.concat([d.assign(Gr=rankdata(d.G) / len(d)) for d in sets]).dropna(subset=["Sp"]); allr["bin"] = pd.qcut(allr.Sp, 5); print(allr.groupby("bin").agg(n=("Gr", "size"), Sp=("Sp", "median"), G=("Gr", "mean")).round(3).to_string())
json.dump(out, open("s_results.json", "w"), indent=1)
