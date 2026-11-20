import sys, json, zlib, hashlib, collections, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path.insert(0, "."); import sabc
from scipy.stats import rankdata, pearsonr
from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler
J = "/home/claude/corpus/thesession/json/"; T = json.load(open(J + "tunes.json")); pop = {p["tune_id"]: int(p["tunebooks"]) for p in json.load(open(J + "tune_popularity.json"))}; rec = collections.defaultdict(set)
for r in json.load(open(J + "recordings.json")):
    if r.get("tune_id"): rec[r["tune_id"]].add(r["id"])
first = {}; nset = collections.Counter()
for t in T:
    nset[t["tune_id"]] += 1
    if t["tune_id"] not in first or int(t["setting_id"]) < int(first[t["tune_id"]]["setting_id"]): first[t["tune_id"]] = t
def ent(v):
    c = np.array(list(collections.Counter(v).values()), float); p = c / c.sum(); return float(-(p * np.log2(p)).sum())
def dfa(x):
    x = np.asarray(x, float); n = len(x)
    if n < 128 or x.std() == 0: return np.nan
    y = np.cumsum(x - x.mean()); sizes = np.unique(np.round(np.geomspace(4, n // 4, 12)).astype(int)); F = []
    for s in sizes:
        k = n // s; seg = y[:k * s].reshape(k, s); tt = np.arange(s) - (s - 1) / 2; b = (seg * tt).sum(1) / (tt ** 2).sum(); r = seg - seg.mean(1, keepdims=True) - b[:, None] * tt; F.append(np.sqrt((r ** 2).mean()))
    return float(np.polyfit(np.log(sizes), np.log(F), 1)[0])
def feats(t):
    bars, tonic, md = sabc.parse(t["abc"], t["mode"]); notes = [(p, d) for b in bars for p, d in b if p is not None]
    if len(notes) < 40 or len(bars) < 8: return None
    p = np.array([n[0] for n in notes], float); d = np.array([n[1] for n in notes]); iv = np.diff(p); a = np.abs(iv); sg = np.sign(iv[iv != 0]); pc = (p.astype(int) - tonic) % 12; bs = ["".join(f"{int(q) if q is not None else 'z'}:{dd}," for q, dd in b) for b in bars]; seen = set(); rep = 0
    for s in bs: rep += s in seen; seen.add(s)
    raw = "|".join(bs).encode(); half = len(p) // 2; penta = {0, 2, 4, 7, 9} if md in ("maj", "ion", "mix", "lyd") else {0, 3, 5, 7, 10} if md in ("min", "aeo", "phr") else {0, 2, 5, 7, 10} if md == "dor" else {0, 2, 4, 7, 9}
    return dict(range=p.max() - p.min(), step=a.mean(), leaps=(a > 4).mean(), stepwise=((a > 0) & (a <= 2)).mean(), same=(a == 0).mean(), turns=float((sg[1:] != sg[:-1]).mean()) if len(sg) > 2 else np.nan, pitch_ent=ent(p), iv_ent=ent(iv), rhythm_ent=ent(d), long=(d >= 2).mean(), per_bar=len(p) / len(bars), top_pos=float(np.argmax(p)) / len(p), tonic=(pc == 0).mean(), fifth=(pc == 7).mean(), ends_tonic=float(pc[-1] == 0), bars_repeated=rep / len(bars), compress=len(zlib.compress(raw)) / len(raw), part_lift=p[half:].mean() - p[:half].mean(), penta=np.isin(pc, list(penta)).mean(), thirds=((a == 3) | (a == 4)).mean(), S=dfa(p), n=len(p), nbars=len(bars), md=md)
rows = []
for tid, t in first.items():
    try: f = feats(t)
    except Exception: f = None
    if f: f.update(tune_id=int(tid), type=t["type"], tb=pop.get(tid, 0), rc=len(rec.get(tid, ())), settings=nset[tid], date=t["date"], name=t["name"]); rows.append(f)
D = pd.DataFrame(rows); D["Gs"] = (rankdata(D.tb) + rankdata(D.rc)) / (2 * len(D)); D["half"] = [int(hashlib.md5(str(i).encode()).hexdigest(), 16) % 2 for i in D.tune_id]; D.to_pickle("session.pkl")
F = ["range", "step", "leaps", "stepwise", "same", "turns", "pitch_ent", "iv_ent", "rhythm_ent", "long", "per_bar", "top_pos", "tonic", "fifth", "ends_tonic", "bars_repeated", "compress", "part_lift", "penta", "thirds"]
ty = pd.get_dummies(D.type).values[:, 1:].astype(float); mo = pd.get_dummies(D.md).values[:, 1:].astype(float)
def part(mask, v, tg, order=True):
    x = D[mask]; C = np.c_[tuple([np.ones(len(x)), ty[mask], mo[mask], rankdata(x.n)] + ([rankdata(x.tune_id)] if order else []))]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(x[tg]))); return round(float(r), 3), float(p)
print("tunes", len(D), "| with tunebooks 10+", int((D.tb > 0).sum()), "| recorded", int((D.rc > 0).sum()), "| neither", int(((D.tb == 0) & (D.rc == 0)).sum()), "| submission order vs Gs", part(np.ones(len(D), bool), D.tune_id.values, "Gs", False))
X = D[F].fillna(D[F].median()).values; Xs = np.c_[X, X ** 2]; pr = np.zeros(len(D)); A = np.ones(len(D), bool)
for h in (0, 1):
    a, b = (D.half != h).values, (D.half == h).values; sc = StandardScaler().fit(Xs[a]); pr[b] = RidgeCV(alphas=np.logspace(-1, 4, 16)).fit(sc.transform(Xs[a]), D.Gs.values[a]).predict(sc.transform(Xs[b]))
out = {"L1": dict(order_held=part(A, pr, "Gs"), order_not_held=part(A, pr, "Gs", False), half0=part((D.half == 0).values, pr[(D.half == 0).values], "Gs"), half1=part((D.half == 1).values, pr[(D.half == 1).values], "Gs"), tunebooks=part(A, pr, "tb"), recordings=part(A, pr, "rc"), after_2010=part((D.date > "2010").values, pr[(D.date > "2010").values], "Gs"))}; print("L1 page reader, out of fold:", out["L1"])
s = D.S.notna().values; x = D[s]; C = np.c_[np.ones(s.sum()), ty[s], mo[s], rankdata(x.n), rankdata(x.tune_id)]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; y = res(x.Gs.values); S1 = x.S.values; import numpy.polynomial.polynomial as P
Xq = np.c_[res(S1), res(S1 ** 2)]; co, *_ = np.linalg.lstsq(Xq, y, rcond=None); rs = y - Xq @ co; se = np.sqrt(np.diag(np.linalg.inv(Xq.T @ Xq)) * rs.var()); raw = np.polyfit(S1, x.Gs.values, 2)
out["L2"] = dict(n=int(s.sum()), S_quartiles=np.percentile(S1, [25, 50, 75]).round(3).tolist(), squared_term=float(co[1]), z=float(co[1] / se[1]), peak=float(-co[0] / (2 * co[1])), linear=part(s, S1, "Gs"), G_by_fifth_of_S=[round(float(v), 3) for v in x.groupby(pd.qcut(x.S, 5)).Gs.mean().values], S_fifth_medians=[round(float(v), 2) for v in x.groupby(pd.qcut(x.S, 5)).S.median().values]); print("L2 S:", out["L2"])
print("each measure alone (submission order held): half0, half1, all | without order held")
for f in F:
    v = D[f].fillna(D[f].median()).values; a, b, c, u = part((D.half == 0).values, v[(D.half == 0).values], "Gs"), part((D.half == 1).values, v[(D.half == 1).values], "Gs"), part(A, v, "Gs"), part(A, v, "Gs", False); out[f] = (a[0], b[0], c[0], u[0]); print(f"   {f:14} {a[0]:+.3f} {b[0]:+.3f} {c[0]:+.3f} | {u[0]:+.3f}")
json.dump(out, open("session_results.json", "w"), indent=1, default=float)
