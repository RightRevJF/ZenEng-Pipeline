import re, json, collections, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
d = pd.read_pickle("metered.pkl"); d = d[d.incipit.notna()].copy(); MAJ = [0, 2, 4, 5, 7, 9, 11]; MIN = [0, 2, 3, 5, 7, 8, 10]
def ent(v):
    c = np.array(list(collections.Counter(v).values()), float); p = c / c.sum(); return float(-(p * np.log2(p)).sum())
def read(inc, minor):
    s = re.sub(r"[()]", "", str(inc))
    if re.search(r"[^1-7UD]", s): return None
    sc = MIN if minor else MAJ; o = 0; p = []; deg = []
    for ch in s:
        if ch == "U": o += 12
        elif ch == "D": o -= 12
        else: p.append(sc[int(ch) - 1] + o); deg.append(int(ch))
    if len(p) < 10: return None
    p = np.array(p, float); iv = np.diff(p); a = np.abs(iv); pen = {1, 3, 4, 5, 7} if minor else {1, 2, 3, 5, 6}
    return dict(penta=float(np.mean([x in pen for x in deg])), same=float((a == 0).mean()), tonic=float(np.mean([x == 1 for x in deg])), iv_ent=ent(iv), pitch_ent=ent(p), leaps=float((a > 4).mean()), length=len(p), range=float(p.max() - p.min()), step=float(a.mean()), starts_tonic=float(deg[0] == 1), fifth=float(np.mean([x == 5 for x in deg])), third=float(np.mean([x == 3 for x in deg])))
d["minor"] = d.tuneKey.fillna("").str.contains("minor"); rows = [read(i, m) for i, m in zip(d.incipit, d.minor)]; ok = [r is not None for r in rows]; d = d[ok].reset_index(drop=True); d = pd.concat([d, pd.DataFrame([r for r in rows if r])], axis=1); d["y"] = np.log1p(d.n)
by = d.composers.fillna("").str.extract(r"(1[4-9]\d\d)")[0].astype(float); d["born"] = by
SIGN = dict(penta=1, same=1, tonic=1, iv_ent=-1, pitch_ent=-1, leaps=-1); z = lambda v: (v - v.mean()) / v.std(); d["plain"] = sum(s * z(d[k]) for k, s in SIGN.items()) / 6
me = pd.get_dummies(d.meter).values[:, 1:].astype(float)
def part(mask, col, born=False):
    x = d[mask]; C = np.c_[tuple([np.ones(len(x)), me[mask], x.minor.values.astype(float), rankdata(x.length)] + ([rankdata(x.born)] if born else []))]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(x[col])), res(rankdata(x.y))); return round(float(r), 3), float(p), int(mask.sum())
A = np.ones(len(d), bool); B = d.born.notna().values; print("tunes", len(d), "| printed in one hymnal only", int((d.n <= 1).sum()), "| in 50+", int((d.n >= 50).sum()), "| composer birth year known", int(B.sum()), "| birth year vs hymnals", part(B, "born")[:2]); out = {}
out["H1 plainness"] = dict(all=part(A, "plain"), born_held=part(B, "plain", True), major=part(~d.minor.values, "plain"), minor=part(d.minor.values, "plain"), CM=part((d.meter == "8.6.8.6").values, "plain"), LM=part((d.meter == "8.8.8.8").values, "plain"), SM=part((d.meter == "6.6.8.6").values, "plain"), other=part(~d.meter.isin(["8.6.8.6", "8.8.8.8", "6.6.8.6"]).values, "plain")); print("H1", out["H1 plainness"])
for k, s in SIGN.items(): out[k] = dict(session_sign=s, all=part(A, k), born_held=part(B, k, True)); print(f"   {k:10} session sign {s:+d}  here {out[k]['all'][0]:+.3f} (p {out[k]['all'][1]:.1g})  with birth year held {out[k]['born_held'][0]:+.3f}")
print("other readings, no prediction:"); 
for k in ("range", "step", "starts_tonic", "fifth", "third"): out[k] = part(A, k); print(f"   {k:12} {out[k][0]:+.3f} (p {out[k][1]:.1g})")
q = pd.qcut(d.plain, 5, labels=False); print("median hymnals by fifth of plainness:", d.groupby(q).n.median().tolist(), "| share in 20+ hymnals:", d.groupby(q).n.apply(lambda v: round(float((v >= 20).mean()), 3)).tolist()); json.dump(out, open("hymn_results.json", "w"), indent=1, default=float); d.to_pickle("hymn.pkl")
