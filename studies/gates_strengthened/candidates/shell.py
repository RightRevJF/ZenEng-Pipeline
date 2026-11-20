"""Gate 2, THE SHELL: how far a recording stands from the hits of its time.

Two measures, both kind "sound" (Essentia numbers, any number of stores):

  directional_shell (primary)  = family shell + lean.
  family_shell      (runner-up) = nothing fitted; pure geometry.

family shell: every trait is turned into a normal score by rank within its store. The traits are grouped into seven
families (level, spectral shape, rhythm, tonal, MFCC timbre, spectral contrast, frame-to-frame variances). For each
family and each recording the reference crowd is the hits of the five years BEFORE it in the same store (widened until
there are 150; the earliest years fall back to the years around them): a record can only be unlike what came before it.
In that crowd's own shrunk covariance we take the mean distance to the recording's 10 nearest hits of the crowd (far
from everybody, not only from the average). Each family's distance is ranked within the store and the seven are added
with equal weight, so a four-trait family (chords, key) counts as much as a 27-trait one.

lean: one fixed direction in the same era-relative coordinates (each trait minus the previous years' mean, over their
spread), a ridge fitted ONCE at import on the open half only. It says the shell is not equally thick all round: standing
apart toward a loose tempo, low frame-to-frame flux, energy gathered low, few chord changes counts for more than
standing apart toward the busy, bright side.

At scoring time only the sound columns, `year` and `store` of the collection handed in are read. No outcome column is
read: G, love, cover_rank, peak, pop, cov0 are used only at import, only on the open half, to fit the 127 lean weights.
"""
import numpy as np, pandas as pd, warnings
from scipy.stats import rankdata, norm
from sklearn.covariance import LedoitWolf
from sklearn.linear_model import Ridge

_OPEN = "/home/claude/arena/sound_open.pkl"
_SCALARS = ("average_loudness", "dynamic_complexity", "bpm", "danceability", "onset_rate", "chords_changes_rate", "key_strength")
_K, _WIN, _NMIN, _ALPHA = 10, 5, 150, 600.0


def _has(f, keys): return any(k in f for k in keys)


def _families(cols):
    means = [c for c in cols if c.endswith(".mean")] + [c for c in _SCALARS if c in cols]
    fam = dict(
        level=[f for f in means if _has(f, ("rms", "spectral_energy.", "energyband", "hfc", "flux", "average_loudness", "silence_rate", "spectral_decrease", "beats_loudness", "strongpeak"))],
        rhythm=[f for f in means if _has(f, ("bpm", "onset", "danceability"))],
        tonal=[f for f in means if _has(f, ("chords", "hpcp", "key_"))])
    used = set(sum(fam.values(), []))
    fam["shape"] = [f for f in means if f not in used]
    fam["mfcc"] = [c for c in cols if c.startswith("mfcc")]
    fam["contrast"] = [c for c in cols if c.startswith("spectral_contrast")]
    fam["vars"] = [c for c in cols if c.endswith(".var")]
    return {k: v for k, v in fam.items() if len(v) >= 2}


def _clean(D, F):
    A = D[F].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan)
    return np.nan_to_num(A.fillna(A.median()).values.astype(float))


def _nscore(X):
    return np.column_stack([norm.ppf((rankdata(X[:, j]) - .5) / len(X)) for j in range(X.shape[1])])


def _zs(v, groups):
    v = np.asarray(v, float); ok = np.isfinite(v); v = np.where(ok, v, np.median(v[ok]) if ok.any() else 0.0); o = np.zeros(len(v))
    for g in np.unique(groups):
        m = groups == g; o[m] = norm.ppf((rankdata(v[m]) - .5) / m.sum())
    return o


def _crowd(yg, y, nm):
    """the hits of the years before y (5 years, widened until nm records); failing that the years around y; failing that the nm nearest in time."""
    w = _WIN; m = (yg < y) & (yg >= y - w)
    while m.sum() < nm and w < 40: w += 1; m = (yg < y) & (yg >= y - w)
    if m.sum() >= nm: return m
    w = 3; m = np.abs(yg - y) <= w
    while m.sum() < nm and w < 40: w += 1; m = np.abs(yg - y) <= w
    if m.sum() < min(nm, len(yg)):
        m = np.zeros(len(yg), bool); m[np.argsort(np.abs(yg - y), kind="stable")[:nm]] = True
    return m


def _groups(D): return D["store"].astype(str).values if "store" in D.columns else np.zeros(len(D), dtype=int).astype(str)


def _era(D, F, want="knn"):
    """per recording: mean distance to its K nearest hits of the crowd (want='knn'), or its era-relative trait scores (want='z')."""
    X = _clean(D, F); years = pd.to_numeric(D["year"], errors="coerce"); years = years.fillna(years.median()).values.astype(int); groups = _groups(D); n, p = X.shape
    out = np.zeros(n) if want == "knn" else np.zeros((n, p))
    for g in np.unique(groups):
        gi = np.where(groups == g)[0]
        if len(gi) < 3: continue
        Xn = _nscore(X[gi]); yg = years[gi]; nm = min(max(_NMIN, 3 * p), len(gi))
        for y in np.unique(yg):
            m = _crowd(yg, y, nm); R = Xn[m]; me = yg == y; mu = R.mean(0)
            if want == "z":
                sd = R.std(0); out[gi[me]] = np.where(sd > 1e-9, (Xn[me] - mu) / np.where(sd > 1e-9, sd, 1.0), 0.0); continue
            cov = LedoitWolf().fit(R).covariance_; ev, V = np.linalg.eigh(cov); ev = np.maximum(ev, 1e-3 * ev.max()); W = V / np.sqrt(ev)
            Zr = (R - mu) @ W; Zm = (Xn[me] - mu) @ W
            d = np.sqrt(np.maximum((Zm ** 2).sum(1)[:, None] + (Zr ** 2).sum(1)[None, :] - 2 * Zm @ Zr.T, 0)); d.sort(1); k = max(1, min(_K, d.shape[1] - 1))
            out[gi[me]] = np.where(m[me], d[:, 1:k + 1].mean(1), d[:, :k].mean(1))      # a record in its own crowd skips itself
    return out


def _with_cols(D, cols):
    D = D.copy()
    for c in cols:
        if c not in D.columns: D[c] = np.nan
    return D


def family_shell(D):
    D = _with_cols(D.reset_index(drop=True), _ALL); groups = _groups(D)
    return _zs(sum(_zs(_era(D, F), groups) for F in _FAM.values()), groups)


def _lean(D):
    Z = _era(D, _ALL, "z"); return ((Z - _MU) / _SD) @ _W


def directional_shell(D):
    D = _with_cols(D.reset_index(drop=True), _ALL); groups = _groups(D)
    return family_shell(D) + _zs(_lean(D), groups)


def _fit(O):
    """the lean: ridge of the yardstick (year and peak taken out, within store) on era-relative trait scores. Open half only."""
    groups = _groups(O); y = np.zeros(len(O))
    for g in np.unique(groups):
        m = groups == g; x = O[m]; C = np.c_[np.ones(m.sum()), rankdata(x["year"]), rankdata(x["peak"])]; t = norm.ppf((rankdata(x["G"]) - .5) / m.sum()); y[m] = t - C @ np.linalg.lstsq(C, t, rcond=None)[0]
    Z = _era(O, _ALL, "z"); mu, sd = Z.mean(0), Z.std(0) + 1e-9
    return mu, sd, Ridge(alpha=_ALPHA).fit((Z - mu) / sd, y).coef_


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    _O = pd.read_pickle(_OPEN).reset_index(drop=True)
    _ALL = [c for c in _O.columns[3:_O.columns.get_loc("year")] if _O[c].notna().mean() > .98 and _O[c].std() > 0]
    _FAM = _families(_ALL)
    _MU, _SD, _W = _fit(_O)
    del _O

CANDIDATES = [
    dict(name="directional_shell", kind="sound", fn=directional_shell, sign=+1,
         why="Distance from the nearest hits of the previous five years, counted family by family, plus a fixed lean: standing apart toward loose tempo, low flux, low-gathered energy and few chord changes counts for more than standing apart toward the busy bright side.",
         baseline="Mahalanobis radius from the centre of the hits of its own years +-3 over 54 Essentia means (v45 S1_shell): +0.171 pooled on the open half when handed the open half alone (+0.144 on the locked half as published)"),
    dict(name="family_shell", kind="sound", fn=family_shell, sign=+1,
         why="Nothing fitted: mean distance to the 10 nearest hits of the previous five years in their own covariance, computed in seven trait families (level, shape, rhythm, tonal, MFCC, contrast, variances) and added with equal weight.",
         baseline="same v45 S1_shell radius: +0.171 pooled on the open half"),
]
