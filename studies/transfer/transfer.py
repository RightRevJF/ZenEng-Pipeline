import sys, json, zlib, pickle, hashlib, collections, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/home/claude/zeneng/corpus/v39"); import sabc
from scipy.stats import rankdata, pearsonr, norm as Nm
from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler
MAJ = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]); MIN = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
def ent(v):
    c = np.array(list(collections.Counter(v).values()), float); p = c / c.sum(); return float(-(p * np.log2(p)).sum())
def toks(p, d): return [(int(np.clip(p[i] - p[i - 1], -12, 12)), min(round(d[i] * 4) / 4, 4.0)) for i in range(1, len(p))]
def feats(p, d):
    p = np.asarray(p, float); d = np.clip(np.asarray(d, float), .0625, 8); h = np.bincount(p.astype(int) % 12, d, 12); cm = [np.corrcoef(np.roll(MAJ, k), h)[0, 1] for k in range(12)]; cn = [np.corrcoef(np.roll(MIN, k), h)[0, 1] for k in range(12)]; minor = max(cn) > max(cm); ton = int(np.argmax(cn if minor else cm)); pc = (p.astype(int) - ton) % 12
    iv = np.diff(p); a = np.abs(iv); sg = np.sign(iv[iv != 0]); half = len(p) // 2; pen = [0, 3, 5, 7, 10] if minor else [0, 2, 4, 7, 9]; tk = toks(p, d); g4 = [tuple(tk[i:i + 4]) for i in range(len(tk) - 3)]; raw = ";".join(f"{x[0]}:{x[1]}" for x in tk).encode()
    return dict(range=p.max() - p.min(), step=a.mean(), leaps=(a > 4).mean(), stepwise=((a > 0) & (a <= 2)).mean(), same=(a == 0).mean(), turns=float((sg[1:] != sg[:-1]).mean()) if len(sg) > 2 else 0.5, pitch_ent=ent(p), iv_ent=ent(iv), rhythm_ent=ent(np.round(d * 4) / 4), long=(d >= 1).mean(), top_pos=float(np.argmax(p)) / len(p), tonic=(pc == 0).mean(), fifth=(pc == 7).mean(), ends_tonic=float(pc[-1] == 0), penta=np.isin(pc, pen).mean(), thirds=((a == 3) | (a == 4)).mean(), part_lift=p[half:].mean() - p[:half].mean(), compress=len(zlib.compress(raw)) / max(len(raw), 1), fig_rep=1 - len(set(g4)) / max(len(g4), 1))
def trigram(seqs):
    c1 = collections.Counter(); c2 = collections.Counter(); c3 = collections.Counter()
    for s in seqs:
        for k in range(len(s)):
            c1[s[k]] += 1
            if k >= 1: c2[(s[k - 1], s[k])] += 1
            if k >= 2: c3[(s[k - 2], s[k - 1], s[k])] += 1
    return c1, c2, c3, sum(c1.values()), len(c1)
def ic(s, M):
    c1, c2, c3, N, V = M; o = []
    for k in range(2, len(s)):
        p1 = (c1[s[k]] + 1) / (N + V); p2 = (c2[(s[k - 1], s[k])] + p1) / (c1[s[k - 1]] + 1); o.append(-np.log2(max((c3[(s[k - 2], s[k - 1], s[k])] + p2) / (c2[(s[k - 2], s[k - 1])] + 1), 1e-9)))
    return float(np.mean(o)) if o else np.nan
def crossfit_ic(seqs, halves):
    out = np.full(len(seqs), np.nan)
    for h in (0, 1):
        M = trigram([s for s, hh in zip(seqs, halves) if hh != h])
        for j, (s, hh) in enumerate(zip(seqs, halves)):
            if hh == h: out[j] = ic(s, M)
    return out
# session
S = pd.read_pickle("/home/claude/zeneng/corpus/v39/session.pkl"); T = json.load(open("/home/claude/corpus/thesession/json/tunes.json")); first = {}
for t in T:
    if t["tune_id"] not in first or int(t["setting_id"]) < int(first[t["tune_id"]]["setting_id"]): first[t["tune_id"]] = t
rows = []; seqs = []
for tid in S.tune_id:
    bars, _, _ = sabc.parse(first[str(tid)]["abc"], first[str(tid)]["mode"]); n = [(p, d / 2) for b in bars for p, d in b if p is not None]; p = [x[0] for x in n]; d = [x[1] for x in n]; rows.append(feats(p, d)); seqs.append(toks(p, d))
FS = pd.DataFrame(rows); FS["ic"] = crossfit_ic(seqs, S.half.values); F = list(FS.columns); ty = pd.get_dummies(S.type).values[:, 1:].astype(float)
def partS(v):
    C = np.c_[np.ones(len(S)), ty, rankdata(S.n), rankdata(S.tune_id)]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(S.Gs))); return round(float(r), 3), float(p)
Z = StandardScaler().fit_transform(FS.fillna(FS.median()).values); Z2 = np.c_[Z, Z ** 2]; pr = np.zeros(len(S))
for h in (0, 1):
    a, b = (S.half != h).values, (S.half == h).values; pr[b] = RidgeCV(alphas=np.logspace(-1, 4, 16)).fit(Z2[a], S.Gs.values[a]).predict(Z2[b])
print("Step 0: portable reader on session tunes, half to half:", partS(pr)); R = RidgeCV(alphas=np.logspace(-1, 4, 16)).fit(Z2, S.Gs.values)
# hits
H = pickle.load(open("/home/claude/arena/tunes_open.pkl", "rb")) + pickle.load(open("/home/claude/arena_locked/tunes_locked.pkl", "rb")); out = {}; allr = []
def part(x, v, tg):
    C = np.c_[np.ones(len(x)), rankdata(x.year), rankdata(x.notes)]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(x[tg]))); return float(r), float(p), len(x)
res_sets = collections.defaultdict(list)
for st in (1, 2, 3):
    X = [s for s in H if s["set"] == st]; rows = []; seqs = []; meta = []
    for s in X:
        c = max(s["clips"], key=len); p = [n[1] for n in c]; t = [n[0] for n in c]; d = list(np.diff(t)) + [1.0]
        if len(p) < 40 or len(set(p)) < 4: continue
        rows.append(feats(p, d)); seqs.append(toks(p, d)); meta.append(dict(year=s["year"], notes=len(p), cover_rank=s["cover_rank"], love=s["love"], G=s["G"], h=int(hashlib.md5(s["artist"].encode()).hexdigest(), 16) % 2 if False else int(hashlib.sha1(s["artist"].encode()).hexdigest(), 16) % 2))
    f = pd.DataFrame(rows); m = pd.DataFrame(meta); f["ic"] = crossfit_ic(seqs, m.h.values); z = StandardScaler().fit_transform(f[F].fillna(f[F].median()).values); pred = R.predict(np.c_[z, z ** 2]); m["pred"] = pred
    for tg in ("cover_rank", "love", "G"): res_sets[tg].append(part(m, pred, tg))
    for c in F: res_sets["feat_" + c].append(part(m, f[c].fillna(f[c].median()).values, "cover_rank"))
def pool(Rs): z = sum(np.sign(r) * Nm.isf(p / 2) * np.sqrt(n) for r, p, n in Rs) / np.sqrt(sum(n for _, _, n in Rs)); return float(2 * Nm.sf(abs(z)))
for tg, lab in (("cover_rank", "P1 frozen reader against COVERED"), ("love", "P2 against still loved"), ("G", "   against the whole yardstick")):
    Rs = res_sets[tg]; print(f"{lab:34} sets " + " ".join(f"{r:+.3f} (n {n})" for r, _, n in Rs) + f"  pooled p {pool(Rs):.3g}"); out[tg] = Rs
print("parts against covered (sets 1, 2, 3):")
for c in F:
    Rs = res_sets["feat_" + c]; out[c] = Rs; print(f"   {c:11} " + " ".join(f"{r:+.3f}" for r, _, _ in Rs) + f"   pooled p {pool(Rs):.2g}   session sign {np.sign(R.coef_[F.index(c)]):+.0f}")
json.dump(out, open("transfer_results.json", "w"), indent=1)
