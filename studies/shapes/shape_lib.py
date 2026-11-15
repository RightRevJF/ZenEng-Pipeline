"""Shapes of songs: the shared method (Stage 0 of the study in "Shapes of music like story arcs").

Every piece becomes one curve (a value per bar or per note). The steps:
  1. resample to relative time (n points, linear interpolation over the piece's span)
  2. smooth by keeping the first k coefficients of a discrete cosine transform (no wrap-around, unlike a Fourier filter)
  3. standardise each curve (mean 0, sd 1) so only its shape counts
  4. SVD of the matrix of curves: how much of the variation a few modes carry
  5. two separate questions, each against null models:
     Q1  do pieces share a shape at all?  the mean curve's strength and mode 1's share, against the same pieces with their
         bars shuffled (order destroyed, values kept)
     Q2  do the shapes fall into types?  k-means quality (silhouette) on the real curves against curves drawn from a
         Gaussian with exactly the real covariance (a continuum with the same modes and no types), plus bootstrap
         stability of the clusters (adjusted Rand index)
  6. link to an outcome: regress the outcome on the mode scores with controls (statsmodels), report effect sizes
"""
import numpy as np
from scipy.fft import dct, idct
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score

def resample(y, n=100):
    y = np.asarray(y, float)
    if len(y) == 1: return np.repeat(y, n)
    x = np.linspace(0, 1, len(y)); return np.interp(np.linspace(0, 1, n), x, y)

def dct_smooth(y, k=8):
    c = dct(np.asarray(y, float), norm="ortho"); c[k:] = 0; return idct(c, norm="ortho")

def standardise(y):
    y = np.asarray(y, float); s = y.std()
    return (y - y.mean()) / s if s > 1e-9 else y - y.mean()

def prepare(curves, n=100, k=8):
    return np.array([standardise(dct_smooth(resample(c, n), k)) for c in curves])

def svd_modes(X, m=4):
    Xc = X - X.mean(0); U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    share = S ** 2 / (S ** 2).sum()
    return dict(modes=Vt[:m], scores=Xc @ Vt[:m].T, share=share[:m], mean=X.mean(0))

def shared_shape(curves, n=100, k=8, reps=200, rng=None):
    """Q1: the mean curve's root-mean-square and mode 1's share, real against bar-shuffled nulls"""
    rng = rng or np.random.default_rng(0)
    X = prepare(curves, n, k); real_mean = np.sqrt((X.mean(0) ** 2).mean()); real_m1 = svd_modes(X, 1)["share"][0]
    null_mean, null_m1 = [], []
    for _ in range(reps):
        Xs = prepare([rng.permutation(np.asarray(c, float)) for c in curves], n, k)
        null_mean.append(np.sqrt((Xs.mean(0) ** 2).mean())); null_m1.append(svd_modes(Xs, 1)["share"][0])
    null_mean, null_m1 = np.array(null_mean), np.array(null_m1)
    return dict(mean_rms=real_mean, mean_rms_null95=float(np.percentile(null_mean, 95)), p_mean=float((null_mean >= real_mean).mean()),
                mode1_share=real_m1, mode1_null95=float(np.percentile(null_m1, 95)), p_mode1=float((null_m1 >= real_m1).mean()))

def _sil(X, k, seed=0):
    lab = KMeans(k, n_init=10, random_state=seed).fit_predict(X); return silhouette_score(X, lab), lab

def raw_matrix(curves, n=100, k=8):
    """resampled and smoothed, not yet standardised (the null models are drawn here, then standardised the same way)"""
    return np.array([dct_smooth(resample(c, n), k) for c in curves])

def _scores(R, dims):
    X = np.array([standardise(r) for r in R]); return svd_modes(X, dims)

def types_test(R, ks=(2, 3, 4, 5, 6), dims=6, reps=50, rng=None):
    """Q2: silhouette of k-means in the leading SVD dimensions of the standardised curves, real against null sets drawn from a
    Gaussian with the real curves' mean and covariance before standardisation, then standardised the same way (so the null
    shares the real data's modes and the distortion standardising brings, and has no types). Plus bootstrap stability.
    Types are real only if the real silhouette beats the null at some k (p < .05) and the clusters are stable (ARI >= .6)."""
    rng = rng or np.random.default_rng(1)
    R = np.asarray(R, float); sv = _scores(R, dims); Z = sv["scores"]; mu = R.mean(0); cov = np.cov(R.T)
    nulls = [_scores(rng.multivariate_normal(mu, cov, size=len(R)), dims)["scores"] for _ in range(reps)]
    out = {}
    for k in ks:
        s_real, lab = _sil(Z, k)
        s_null = [_sil(N, k, seed=r)[0] for r, N in enumerate(nulls)]
        aris = []
        for r in range(20):
            idx = rng.choice(len(Z), len(Z), replace=True)
            lab_b = KMeans(k, n_init=10, random_state=r).fit(Z[idx]).predict(Z)
            aris.append(adjusted_rand_score(lab, lab_b))
        out[k] = dict(silhouette=float(s_real), null95=float(np.percentile(s_null, 95)), null_mean=float(np.mean(s_null)),
                      p=float((np.array(s_null) >= s_real).mean()), stability_ari=float(np.median(aris)))
    beats = [k for k, v in out.items() if v["p"] < 0.05 and v["stability_ari"] >= 0.6]
    return dict(by_k=out, types_found=bool(beats), k_supported=beats, mode_share=[float(x) for x in sv["share"]])

def synthetic_check(seed=7):
    """Stage 0: the method must find types where there are types, and none in a continuum, and a shared shape where one exists"""
    rng = np.random.default_rng(seed); t = np.linspace(0, 1, 40)
    protos = [np.sin(np.pi * t), t, 1 - t]                                              # arch, rise, fall
    typed = [protos[i % 3] * 2 + rng.normal(0, 0.6, 40) for i in range(300)]
    cont = [rng.normal() * np.sin(np.pi * t) + rng.normal() * (t - 0.5) * 2 + rng.normal(0, 0.6, 40) for _ in range(300)]
    common = [np.sin(np.pi * t) + rng.normal(0, 1.0, 40) for _ in range(300)]
    noise = [rng.normal(0, 1, 40) for _ in range(300)]
    res = {}
    res["typed"] = types_test(raw_matrix(typed, 40, 8))
    res["continuum"] = types_test(raw_matrix(cont, 40, 8))
    res["common_shape"] = shared_shape(common, 40, 8, reps=100)
    res["pure_noise"] = shared_shape(noise, 40, 8, reps=100)
    return res

if __name__ == "__main__":
    import json
    r = synthetic_check()
    print("typed: types_found", r["typed"]["types_found"], r["typed"]["k_supported"])
    print("continuum: types_found", r["continuum"]["types_found"], r["continuum"]["k_supported"])
    print("common shape:", {k: round(v, 3) for k, v in r["common_shape"].items()})
    print("pure noise:", {k: round(v, 3) for k, v in r["pure_noise"].items()})
    json.dump(r, open("/home/claude/shape/stage0_synthetic.json", "w"), indent=1, default=float)
