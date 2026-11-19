"""Gate 3, THE SOUND: a stronger single direction for the sound of a hit that lasts.

PRIMARY  lasting_sound   = z(concentrated spectrum, the old measure) + z(a learned reader of the same kind of sound)
RUNNER-UP spare_steady   = 2*z(concentrated spectrum) + z(harmony that holds still) + z(few events); nothing fitted.

Plain arithmetic on Essentia columns. Every reading is first turned into a normal score by rank WITHIN its
technical group (whole recordings; 30-second previews; 60-second previews), because the three kinds of file
put the same sound on different scales (the 30 s and 60 s previews differ by up to 1.2 SD on some columns).
The learned reader is one ridge regression (closed form, deterministic, well under a second) fitted at import
on the OPEN half only: 75 mean-value sound columns -> the yardstick G with year and chart peak taken out.
No variance columns, no tempo-histogram columns (tempo locked to one value failed the last lock), no tuning.
It is a direction (more of this kind of sound), not a distance from the era.

What the direction is, in words (correlation of each named part with the final score on the open half is in
the researcher's report): energy gathered low and low-middle with the top left open and dark; a lower, less
crowded spectrum (fewer simultaneous peaks, quieter floor between partials in the upper bands); harmony that
holds still (few chord changes, few different chords); fewer sound events per second.
"""
import numpy as np, pandas as pd
from scipy.stats import rankdata, norm

_OPEN = "/home/claude/arena/sound_open.pkl"
_POS = ['melbands_flatness_db.mean', 'barkbands_kurtosis.mean', 'barkbands_skewness.mean', 'melbands_crest.mean']
_NEG = ['melbands_spread.mean', 'spectral_centroid.mean']
_STEADY_NEG = ['chords_strength.var', 'chords_changes_rate', 'chords_number_rate']
_FEW_NEG = ['onset_rate', 'spectral_flux.mean']
_ALPHA = 200.0
_FIRST, _LAST = 'average_loudness', 'tuning_nontempered_energy_ratio'


def _reader_columns(cols):
    cols = list(cols); block = cols[cols.index(_FIRST):cols.index(_LAST) + 1]
    return [c for c in block if not c.endswith('.var') and not c.startswith('bpm') and not c.startswith('tuning')]


def _z(v):
    v = np.asarray(v, float); out = np.zeros(len(v)); ok = np.isfinite(v)
    if ok.sum() > 1: out[ok] = norm.ppf((rankdata(v[ok]) - 0.5) / ok.sum())
    return out


def _groups(df):
    """technical group of each row: store, with previews split into 30 s and 60 s clips (never by any outcome)."""
    g = df['store'].astype(str).values.astype(object) if 'store' in df.columns else np.array(['all'] * len(df), dtype=object)
    if 'length' in df.columns:
        L = pd.to_numeric(df['length'], errors='coerce').values; pv = np.array(['preview' in str(s) for s in g])
        short = pv & (L < 45); long_ = pv & ~(L < 45)
        if short.sum() >= 30 and long_.sum() >= 30:
            g = g.copy(); g[short] = 'preview30'; g[long_] = 'preview60'
    return g


def _zg(v, g):
    v = np.asarray(v, float); out = np.zeros(len(v))
    for k in pd.unique(g):
        m = g == k; out[m] = _z(v[m])
    return out


def _mean_block(df, g, pos=(), neg=()):
    parts = [_zg(df[c].values, g) for c in pos] + [-_zg(df[c].values, g) for c in neg]
    return _zg(np.mean(parts, axis=0), g)


def _concentrated(df, g): return _mean_block(df, g, _POS, _NEG)


def _matrix(df, g, cols): return np.column_stack([_zg(pd.to_numeric(df[c], errors='coerce').values, g) for c in cols])


def _target(df):
    """rank of G with rank of year and of chart peak taken out, per store (what the lock holds)."""
    y = np.zeros(len(df)); st = df['store'].astype(str).values
    for k in pd.unique(st):
        m = st == k; x = df[m]; C = np.c_[np.ones(m.sum()), rankdata(x['year']), rankdata(x['peak'])]
        r = rankdata(x['G']).astype(float); r = r - C @ np.linalg.lstsq(C, r, rcond=None)[0]; y[m] = r / r.std()
    return y


def _fit(train):
    train = train.reset_index(drop=True); cols = _reader_columns(train.columns); g = _groups(train)
    X = _matrix(train, g, cols); y = _target(train); y = y - y.mean()
    w = np.linalg.solve(X.T @ X + _ALPHA * np.eye(X.shape[1]), X.T @ y)          # ridge, closed form
    return dict(cols=cols, w=w)


def _apply(df, model):
    df = df.reset_index(drop=True); g = _groups(df)
    learned = _zg(_matrix(df, g, model['cols']) @ model['w'], g)
    return _zg(learned + _concentrated(df, g), g)


_MODEL = _fit(pd.read_pickle(_OPEN))


def lasting_sound(df):
    """Old concentrated-spectrum score plus the learned reader of the same kind of sound, equal weights."""
    return _apply(df, _MODEL)


def spare_steady(df):
    """Nothing fitted: 2 x concentrated spectrum + harmony that holds still + few sound events per second."""
    df = df.reset_index(drop=True); g = _groups(df)
    return _zg(2 * _concentrated(df, g) + _mean_block(df, g, neg=_STEADY_NEG) + _mean_block(df, g, neg=_FEW_NEG), g)


CANDIDATES = [
    dict(name="lasting_sound", kind="sound", fn=lasting_sound, sign=+1,
         why="The sound of a lasting hit as one direction: energy gathered low with the top left open and dark, an uncrowded spectrum, harmony that holds still and fewer events per second; the old concentrated-spectrum score plus a ridge reader of 75 sound means fitted on the open half, each reading ranked within its own kind of file.",
         baseline="concentrated_spectrum: open half +0.179 whole recordings, +0.107 previews (+0.119 pooled); locked half +0.248 / +0.090"),
    dict(name="spare_steady", kind="sound", fn=spare_steady, sign=+1,
         why="Runner-up with nothing fitted: twice the concentrated-spectrum score plus harmony that holds still (few chord changes, few different chords, steady chord strength) plus few sound events per second; three nearly uncorrelated readings.",
         baseline="concentrated_spectrum: open half +0.179 whole recordings, +0.107 previews (+0.119 pooled); locked half +0.248 / +0.090"),
]
