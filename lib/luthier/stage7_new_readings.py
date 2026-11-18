import sys, json, math, collections, numpy as np, pickle
sys.path[:0] = ["/home/claude/zeneng/corpus/v20"]; import bench as B
from scipy.stats import spearmanr
T = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/tables/metre_atlas/4-4_pop_sung.json")); IV = {int(k): v for k, v in T["intervals"].items()}; IVT = sum(IV.values()); IV2 = {int(k): {int(j): c for j, c in v.items()} for k, v in T["interval_pairs"].items()}
def ic(d, last):
    d = max(-12, min(12, d)); row = IV2.get(max(-12, min(12, last))) if last is not None else None
    p = (row.get(d, 0) + 12.5 * (IV.get(d, 0) + 0.5) / IVT) / (sum(row.values()) + 12.5) if row and sum(row.values()) >= 50 else (IV.get(d, 0) + 0.5) / IVT
    return -math.log2(p)
def readings(notes):
    t = [x[0] for x in notes]; p = [x[1] for x in notes]; I = [None]; last = None
    for i in range(1, len(p)): d = p[i] - p[i - 1]; I.append(ic(d, last)); last = d
    final = [i for i in range(1, len(p)) if i + 1 == len(p) or t[i + 1] - t[i] >= 24]; fs = set(final); inner = [I[i] for i in range(1, len(p)) if i not in fs]
    return {"mean surprise": float(np.mean(I[1:])), "ending gap": float(np.mean(inner) - np.mean([I[i] for i in final])) if final else 0.0, "line endings": len(final)}
if __name__ == "__main__":
    K = [k for k in B.kept() if k["weeks"] == k["weeks"]]; R = [readings(k["notes"]) for k in K]; good_peak = -np.array([k["peak"] for k in K]); weeks = np.array([k["weeks"] for k in K]); out = {"songs": len(K)}
    for name in ("ending gap", "mean surprise"):
        v = np.array([r[name] for r in R]); a = spearmanr(v, good_peak); b = spearmanr(v, weeks); out[name] = dict(peak=[round(float(a.correlation), 3), round(float(a.pvalue), 3)], weeks=[round(float(b.correlation), 3), round(float(b.pvalue), 3)], median=round(float(np.median(v)), 3), quartiles=[round(float(x), 3) for x in np.percentile(v, (25, 75))])
    # N4: joint distance from the kept centre on the judge's readings
    rows = [r for r in pickle.load(open("feats.pkl", "rb")) if r["weeks"] == r["weeks"]]; names = sorted(rows[0]["f"]); X = np.nan_to_num(np.array([[float(r["f"][n]) for n in names] for r in rows])); X = (X - X.mean(0)) / (X.std(0) + 1e-9)
    S = np.cov(X.T); S = 0.7 * S + 0.3 * np.eye(len(names)); Si = np.linalg.inv(S); dist = np.sqrt(np.einsum("ij,jk,ik->i", X, Si, X)); pk = np.array([r["peak"] for r in rows]); th = np.percentile(dist, (33.3, 66.7))
    out["N4: median peak by third of joint distance (near, middle, far)"] = [float(np.median(pk[dist <= th[0]])), float(np.median(pk[(dist > th[0]) & (dist <= th[1])])), float(np.median(pk[dist > th[1]]))]; a = spearmanr(dist, -pk); out["N4: distance against goodness (Spearman, p)"] = [round(float(a.correlation), 3), round(float(a.pvalue), 3)]
    # N3: McGill chords
    S_ = json.load(open("/home/claude/rightrevjf/zeneng-pipeline/studies/harmony/billboard_sections.json")); sys.path.insert(0, "/home/claude/rightrevjf/zeneng-pipeline/lib/luthier"); import chord_writer as C
    cnt = {m: collections.Counter() for m in ("major", "minor")}
    for so in S_:
        for k, b, _, _ in C.sections([so]):
            for tok in b:
                for x in tok: cnt[so["mode"]][x] += 1 / len(tok)
    rar = lambda x, m: -math.log2((cnt[m][x] + 0.5) / (sum(cnt[m].values()) + 0.5 * len(cnt[m]))); rows3 = []
    for so in S_:
        try: peak = float(so["peak"])
        except Exception: continue
        by = collections.defaultdict(list)
        for k, b, _, _ in C.sections([so]):
            for tok in b: by[k].append(float(np.mean([rar(x, so["mode"]) for x in tok])))
        allb = [x for v in by.values() for x in v]
        if len(allb) < 16: continue
        rows3.append(dict(peak=peak, rarity=float(np.mean(allb)), verse=float(np.mean(by["verse"])) if by["verse"] else None, chorus=float(np.mean(by["chorus"])) if by["chorus"] else None))
    g = -np.array([r["peak"] for r in rows3]); a = spearmanr([r["rarity"] for r in rows3], g); vc = [r for r in rows3 if r["verse"] is not None and r["chorus"] is not None]; b = spearmanr([r["verse"] - r["chorus"] for r in vc], [-r["peak"] for r in vc]); c = spearmanr([r["verse"] for r in vc], [-r["peak"] for r in vc])
    pkq = np.percentile([r["peak"] for r in rows3], (25, 75)); top = [r["rarity"] for r in rows3 if r["peak"] <= pkq[0]]; bot = [r["rarity"] for r in rows3 if r["peak"] >= pkq[1]]; dd = (np.mean(top) - np.mean(bot)) / np.sqrt((np.var(top) + np.var(bot)) / 2)
    out["N3"] = dict(songs=len(rows3), rarity_vs_goodness=[round(float(a.correlation), 3), round(float(a.pvalue), 4)], verse_rarity=[round(float(c.correlation), 3), round(float(c.pvalue), 4)], verse_minus_chorus=[round(float(b.correlation), 3), round(float(b.pvalue), 4)], songs_with_both=len(vc), top_against_bottom_quartile_d=round(float(dd), 3), peak_quartiles=[float(x) for x in pkq])
    json.dump(out, open("newread.json", "w"), indent=1); print(json.dumps(out, indent=1))
