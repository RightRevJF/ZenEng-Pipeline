import sys, json, collections, hashlib, re, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/home/claude/zeneng/corpus/v39"); import sabc
from scipy.stats import rankdata, pearsonr
from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler
D = pd.read_pickle("/home/claude/zeneng/corpus/v39/session.pkl"); T = json.load(open("/home/claude/corpus/thesession/json/tunes.json")); first = {}
for t in T:
    if t["tune_id"] not in first or int(t["setting_id"]) < int(first[t["tune_id"]]["setting_id"]): first[t["tune_id"]] = t
tok = {}
for tid in D.tune_id:
    bars, _, _ = sabc.parse(first[str(tid)]["abc"], first[str(tid)]["mode"]); notes = [(p, d) for b in bars for p, d in b if p is not None]; s = [(int(np.clip(notes[i][0] - notes[i - 1][0], -12, 12)), min(round(notes[i][1] * 2) / 2, 4.0)) for i in range(1, len(notes))]; tok[tid] = (s, len(notes) // 2)
def model(ids):
    c3 = collections.Counter(); c2 = collections.Counter(); c1 = collections.Counter()
    for i in ids:
        s = tok[i][0]
        for k in range(len(s)):
            c1[s[k]] += 1
            if k >= 1: c2[(s[k - 1], s[k])] += 1
            if k >= 2: c3[(s[k - 2], s[k - 1], s[k])] += 1
    return c1, c2, c3, sum(c1.values()), len(c1)
def ic(s, M):
    c1, c2, c3, N, V = M; out = []
    for k in range(2, len(s)):
        p1 = (c1[s[k]] + 1) / (N + V); p2 = (c2[(s[k - 1], s[k])] + 1 * p1 * 1) / (c1[s[k - 1]] + 1); p3 = (c3[(s[k - 2], s[k - 1], s[k])] + 1 * p2) / (c2[(s[k - 2], s[k - 1])] + 1); out.append(-np.log2(max(p3, 1e-9)))
    return np.array(out)
D["ic"] = np.nan; D["ic_first"] = np.nan
for h in (0, 1):
    M = model(D.tune_id[D.half != h]); 
    for j in np.where((D.half == h).values)[0]:
        s, half = tok[D.tune_id.iat[j]]; v = ic(s, M); D.iat[j, D.columns.get_loc("ic")] = v.mean(); D.iat[j, D.columns.get_loc("ic_first")] = v[:max(half - 2, 4)].mean()
ty = pd.get_dummies(D.type).values[:, 1:].astype(float); mo = pd.get_dummies(D.md).values[:, 1:].astype(float); A = np.ones(len(D), bool)
def part(mask, v, tg="Gs"):
    x = D[mask]; C = np.c_[np.ones(len(x)), ty[mask], mo[mask], rankdata(x.n), rankdata(x.tune_id)]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(x[tg]))); return round(float(r), 3), float(p)
print("session tunes", len(D)); out = {}
for c in ("ic", "ic_first", "per_bar", "nbars"): out[c] = (part((D.half == 0).values, D[c][D.half == 0].values), part((D.half == 1).values, D[c][D.half == 1].values), part(A, D[c].values)); print(f"   {c:9} halves {out[c][0][0]:+.3f} {out[c][1][0]:+.3f}  all {out[c][2][0]:+.3f} (p {out[c][2][1]:.1g})")
F = ["range", "step", "leaps", "stepwise", "same", "turns", "pitch_ent", "iv_ent", "rhythm_ent", "long", "per_bar", "top_pos", "tonic", "fifth", "ends_tonic", "bars_repeated", "compress", "part_lift", "penta", "thirds"]
def reader(F):
    X = D[F].fillna(D[F].median()).values; X = np.c_[X, X ** 2]; pr = np.zeros(len(D))
    for h in (0, 1):
        a, b = (D.half != h).values, (D.half == h).values; sc = StandardScaler().fit(X[a]); pr[b] = RidgeCV(alphas=np.logspace(-1, 4, 16)).fit(sc.transform(X[a]), D.Gs.values[a]).predict(sc.transform(X[b]))
    return part(A, pr)
out["reader_before"] = reader(F); out["reader_after"] = reader(F + ["ic", "ic_first", "nbars"]); print("reader before", out["reader_before"][0], "after adding surprise, first-strain surprise, bar count", out["reader_after"][0])
# is plainness more than low surprise?  penta etc with ic held
x = D; C = np.c_[np.ones(len(x)), ty, mo, rankdata(x.n), rankdata(x.tune_id), rankdata(x.ic)]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]
for c in ("penta", "bars_repeated", "tonic", "pitch_ent"): print(f"   {c:14} with surprise held {pearsonr(res(rankdata(x[c])), res(rankdata(x.Gs)))[0]:+.3f}")
# hymns
H = pd.read_pickle("/home/claude/zeneng/corpus/v40/hymn.pkl"); H["half"] = [int(hashlib.md5(str(a).encode()).hexdigest(), 16) % 2 for a in H.tuneAuthNumber]; seq = [re.sub(r"[()]", "", s) for s in H.incipit]; H["ic"] = np.nan
for h in (0, 1):
    c2 = collections.Counter(); c1 = collections.Counter()
    for s in np.array(seq, dtype=object)[(H.half != h).values]:
        for k in range(len(s)):
            c1[s[k]] += 1
            if k: c2[(s[k - 1], s[k])] += 1
    N = sum(c1.values()); V = len(c1)
    for j in np.where((H.half == h).values)[0]:
        s = seq[j]; H.iat[j, H.columns.get_loc("ic")] = float(np.mean([-np.log2((c2[(s[k - 1], s[k])] + (c1[s[k]] + 1) / (N + V)) / (c1[s[k - 1]] + 1)) for k in range(1, len(s))]))
me = pd.get_dummies(H.meter).values[:, 1:].astype(float)
def hp(col, extra=None):
    C = np.c_[tuple([np.ones(len(H)), me, H.minor.values.astype(float), rankdata(H.length)] + ([rankdata(H[extra])] if extra else []))]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(H[col])), res(rankdata(H.y))); return round(float(r), 3), float(p)
out["hymn_ic"] = hp("ic"); out["hymn_plain_ic_held"] = hp("plain", "ic"); out["hymn_ic_plain_held"] = hp("ic", "plain"); print("hymns", len(H), "surprise", out["hymn_ic"], "| plainness with surprise held", out["hymn_plain_ic_held"], "| surprise with plainness held", out["hymn_ic_plain_held"])
q = pd.qcut(H.ic, 5, labels=False); print("   share in 20+ hymnals by fifth of surprise (least to most):", H.groupby(q).n.apply(lambda v: round(float((v >= 20).mean()), 3)).tolist()); json.dump(out, open("t4_results.json", "w"), indent=1, default=float)
