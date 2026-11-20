import sys, json, hashlib, importlib.util, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr, norm as Nm
from sklearn.covariance import LedoitWolf; from sklearn.decomposition import PCA; from sklearn.linear_model import RidgeCV; from sklearn.metrics import roc_auc_score
def era_coords(X, years, groups, win=3):
    """X: songs x features. Returns each song's coordinates in its own era's metric (per group)."""
    Z = np.zeros_like(X, float)
    for g in np.unique(groups):
        gm = groups == g; Xg = X[gm]; yg = years[gm]; Xn = np.zeros_like(Xg, float)
        for j in range(Xg.shape[1]): Xn[:, j] = Nm.ppf((rankdata(Xg[:, j]) - .5) / len(Xg))          # each trait to a normal scale within the store
        out = np.zeros_like(Xn)
        for y in np.unique(yg):
            w = win; m = np.abs(yg - y) <= w
            while m.sum() < max(150, 3 * Xn.shape[1]) and w < 25: w += 1; m = np.abs(yg - y) <= w
            lw = LedoitWolf().fit(Xn[m]); ev, V = np.linalg.eigh(lw.covariance_); ev = np.maximum(ev, 1e-3 * ev.max()); out[yg == y] = ((Xn[yg == y] - lw.location_) @ V) / np.sqrt(ev)
        Z[gm] = out
    return Z
def gauss(P):
    lw = LedoitWolf().fit(P); return lw.location_, np.linalg.pinv(lw.covariance_), np.linalg.slogdet(lw.covariance_)[1]
def maha(P, g): d = P - g[0]; return np.einsum("ij,jk,ik->i", d, g[1], d)
def run(d, F, label, hold=("year", "peak")):
    X = np.nan_to_num(d[F].replace([np.inf, -np.inf], np.nan).fillna(d[F].replace([np.inf, -np.inf], np.nan).median()).values.astype(float)); Z = np.nan_to_num(era_coords(X, d.year.values.astype(int), d.store.values)); define = (d.half == 0).values; test = ~define
    great = np.zeros(len(d), bool)
    for g in d.store.unique(): m = (d.store == g).values; great[m] = d.G.values[m] >= np.quantile(d.G.values[m], .8)
    k = min(12, Z.shape[1]); pca = PCA(k, random_state=0).fit(Z[define]); P = pca.transform(Z)
    Gg, Go = gauss(P[define & great]), gauss(P[define & ~great]); u = np.linalg.solve(LedoitWolf().fit(P[define]).covariance_, Gg[0] - Go[0])
    S = dict(S1_shell=np.sqrt((Z ** 2).sum(1)), S2_direction=P @ u, S3_region=(maha(P, Go) + Go[2]) - (maha(P, Gg) + Gg[2]), S4_great_alone=-maha(P, Gg))
    sc = lambda A: (A - A[define].mean(0)) / (A[define].std(0) + 1e-9); S["ridge reader"] = RidgeCV(alphas=np.logspace(0, 5, 16)).fit(sc(Z)[define], d.G.values[define]).predict(sc(Z)[test]); full = {}
    def part(m, v, tg="G"):
        x = d[m]; C = np.c_[tuple([np.ones(len(x))] + [rankdata(x[h]) for h in hold])]; res = lambda q: q - C @ np.linalg.lstsq(C, q, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(x[tg]))); return float(r), float(p), int(m.sum())
    print(f"\n{label}: {len(d)} songs, {len(F)} traits, {k} directions kept; defining half {int(define.sum())} ({int((define & great).sum())} great), test half {int(test.sum())} ({int((test & great).sum())} great)"); out = {}
    for name, v in S.items():
        vt = v if len(v) == test.sum() else v[test]; R = []
        for g in d.store.unique():
            m = test & (d.store == g).values; R.append(part(m, vt[(d.store == g).values[test]]))
        z = sum(np.sign(r) * Nm.isf(p / 2) * np.sqrt(n) for r, p, n in R) / np.sqrt(sum(n for _, _, n in R)); pooled = sum(r * n for r, _, n in R) / sum(n for _, _, n in R); auc = roc_auc_score(great[test], vt)
        out[name] = dict(stores=[round(r, 3) for r, _, _ in R], pooled=round(pooled, 3), p=float(2 * Nm.sf(abs(z))), auc=round(float(auc), 3), love=round(part(test, vt, "love")[0], 3), covers=round(part(test, vt, "cover_rank")[0], 3))
        print(f"   {name:16} per store {out[name]['stores']}  pooled {pooled:+.3f} (p {out[name]['p']:.1g})  tells great from the rest: {auc:.3f}  love {out[name]['love']:+.3f} covers {out[name]['covers']:+.3f}")
    r1 = np.sqrt((Z ** 2).sum(1)); q = pd.qcut(r1[test], 5, labels=False); print("   share of great songs by fifth of distance from the era's centre (near to far):", [round(float(great[test][q == i].mean()), 3) for i in range(5)])
    dg = np.sqrt(maha(P, Gg)); q = pd.qcut(dg[test], 5, labels=False); print("   share of great songs by fifth of distance from the great cloud's centre (near to far):", [round(float(great[test][q == i].mean()), 3) for i in range(5)])
    return out, dict(Z=Z, P=P, great=great, test=test)
if __name__ == "__main__":
    D = pd.concat([pd.read_pickle("/home/claude/arena/sound_open.pkl"), pd.read_pickle("/home/claude/arena_locked/sound_locked.pkl")], ignore_index=True)
    F = [c for c in D.columns if c.endswith(".mean") and D[c].notna().mean() > .98 and D[c].std() > 0] + [c for c in ("average_loudness", "dynamic_complexity", "bpm", "danceability", "onset_rate", "chords_changes_rate", "key_strength") if c in D.columns]
    res = {}; res["sound"], _ = run(D, F, "SOUND (Essentia measurements, two stores)")
    sp = importlib.util.spec_from_file_location("c", "/home/claude/arena/candidates/sound.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); cs = np.asarray({c["name"]: c["fn"] for c in m.CANDIDATES}["concentrated_spectrum"](D.copy()), float); t = (D.half == 1).values; R = []
    for g in D.store.unique():
        mm = t & (D.store == g).values; x = D[mm]; C = np.c_[np.ones(len(x)), rankdata(x.year), rankdata(x.peak)]; rs = lambda q: q - C @ np.linalg.lstsq(C, q, rcond=None)[0]; R.append((pearsonr(rs(rankdata(cs[mm])), rs(rankdata(x.G)))[0], len(x)))
    print(f"   benchmark: concentrated spectrum alone, same test half: {[round(r, 3) for r, _ in R]} pooled {sum(r * n for r, n in R) / sum(n for _, n in R):+.3f}")
    H = pd.concat([pd.read_pickle("/home/claude/arena/hot100_open.pkl"), pd.read_pickle("/home/claude/arena_locked/hot100_locked.pkl")], ignore_index=True); H["store"] = "hot100"; FH = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "spotify_track_duration_ms"]
    res["spotify"], _ = run(H, FH, "SPOTIFY'S TEN READINGS (18,024 hits)"); json.dump(res, open("shape_results.json", "w"), indent=1)
