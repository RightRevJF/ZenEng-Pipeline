"""Sound candidates (arena angle: deepen the low-end finding). Plain arithmetic on Essentia columns, nothing fitted.
Each reading is turned into a normal score by rank WITHIN its store (whole recordings and 22 kHz previews are on
different scales), then the parts are averaged with equal weights. No weights were learned from G."""
import numpy as np
from scipy.stats import rankdata, norm

_POS = ['melbands_flatness_db.mean', 'barkbands_kurtosis.mean', 'barkbands_skewness.mean', 'melbands_crest.mean']
_NEG = ['melbands_spread.mean', 'spectral_centroid.mean']
_PW = 'bpm_histogram_first_peak_weight.mean'


def _z(v):
    v = np.asarray(v, float); out = np.full(len(v), np.nan); ok = np.isfinite(v)
    if ok.sum() > 1: out[ok] = norm.ppf((rankdata(v[ok]) - 0.5) / ok.sum())
    elif ok.sum() == 1: out[ok] = 0.0
    return out


def _by_store(df, f):
    out = np.full(len(df), np.nan)
    groups = df['store'].astype(str).values if 'store' in df.columns else np.zeros(len(df), dtype=int).astype(str)
    for g in np.unique(groups):
        m = groups == g; out[m] = f(df[m])
    return out


def _conc(d):
    parts = [_z(d[c]) for c in _POS] + [-_z(d[c]) for c in _NEG]
    return _z(np.nanmean(parts, axis=0))


def concentrated_spectrum(df):
    """Energy gathered into a few low bands (peaked, skewed low, narrow, low centre) rather than spread evenly."""
    return _by_store(df, _conc)


def loose_tempo(df):
    """Minus the share of the recording sitting at one exact tempo: higher = the tempo breathes."""
    return _by_store(df, lambda d: -_z(d[_PW]))


def concentrated_and_loose(df):
    """Equal-weight sum of the two above."""
    return _by_store(df, lambda d: _conc(d) - _z(d[_PW]))


CANDIDATES = [
    dict(name="concentrated_spectrum", kind="sound", fn=concentrated_spectrum, sign=+1,
         why="Great hits put their energy in a few low bands (peaked, low-skewed, narrow spectrum) instead of filling every band; this is what the low-end finding reduces to and it survives 5-year bands, genre and same-artist comparison in both stores."),
    dict(name="loose_tempo", kind="sound", fn=loose_tempo, sign=+1,
         why="Less of the recording locked to one exact tempo (lower first tempo-histogram peak weight); the only rhythmic reading that agreed in both stores and added to the spectral one."),
    dict(name="concentrated_and_loose", kind="sound", fn=concentrated_and_loose, sign=+1,
         why="Equal-weight sum of the two nearly independent readings above, nothing fitted."),
]
