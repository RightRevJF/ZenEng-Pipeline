"""Gate 4, DEVOTION: which recordings listeners come back to (last.fm plays per listener, reach, year and genre held).

The reader: every Essentia sound statistic in the file (not only the means the baseline used: also how much each reading
varies over the track and how much it changes from one frame to the next), plus Essentia's mood/timbre/voice classifiers
(but NOT its genre guesses, which added nothing), each turned into normal scores by rank within the collection being read,
then two readers averaged: a ridge (straight-line) reader and a boosted-tree reader (which can use bends and interactions).
Fitted at import on half 0 of the last.fm tracks only (md5(uuid) % 2 == 0). Uses no play or listener counts of scored rows,
no year, no track length, no file metadata.

Runner-up (kind "sound"): the same reader rebuilt from only the mean columns that the Hot 100 sound table also has, fitted on
last.fm half 0 only, and read off the Hot 100 recordings (normal scores taken within each store).
Set DEVOTION_GATE_FIT_SUB=0 or 1 to fit on one half of half 0 only (used for the honest open-half check).
"""
import os, re, hashlib, warnings, numpy as np, pandas as pd, pyarrow.parquet as pq
from scipy.stats import rankdata, norm
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import HistGradientBoostingRegressor
from threadpoolctl import threadpool_limits
warnings.filterwarnings("ignore")
_P = "/tmp/claude-0/hspd/"
_strip = lambda c: re.sub(r"^(lowlevel|rhythm|tonal)\.", "", c)
_MOOD = re.compile(r"highlevel\.(mood_\w+|danceability|voice_instrumental|gender|timbre|tonal_atonal)\.all\.")
_HGB = dict(max_iter=300, learning_rate=0.04, max_leaf_nodes=31, min_samples_leaf=100, l2_regularization=5.0, random_state=0)

def _gauss(X):
    X = np.asarray(X, float); out = np.zeros_like(X)
    for j in range(X.shape[1]):
        v = X[:, j]; ok = np.isfinite(v)
        if ok.sum() > 1 and np.nanstd(v[ok]) > 0: out[ok, j] = norm.ppf((rankdata(v[ok]) - .5) / ok.sum())
    return out

def _col(df, c):
    """a reading by its parquet name, or by the name with the lowlevel./rhythm./tonal. prefix removed; missing -> NaN"""
    if c.endswith("_scale_minor"):
        b = c[:-6]; s = df[b] if b in df.columns else (df[_strip(b)] if _strip(b) in df.columns else None)
        if s is not None: return (s.astype(str) == "minor").astype(float).values
        c2 = _strip(c); return pd.to_numeric(df[c2], errors="coerce").values.astype(float) if c2 in df.columns else np.full(len(df), np.nan)
    for k in (c, _strip(c)):
        if k in df.columns:
            s = df[k]; s = s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s; return pd.to_numeric(s, errors="coerce").values.astype(float)
    return np.full(len(df), np.nan)

def _matrix(df, cols): return _gauss(np.c_[tuple(_col(df, c) for c in cols)])

def _load():
    f = pq.ParquetFile(_P + "hsp-l_acousticbrainz.parquet"); n = f.schema.names
    num = lambda c: str(f.schema_arrow.field(c).type) in ("double", "float", "int64", "int32")
    raw = [c for c in dict.fromkeys(n) if n.count(c) == 1 and re.match(r"(lowlevel|rhythm|tonal)\.", c) and num(c) and c != "rhythm.beats_count"]
    mood = [c for c in dict.fromkeys(n) if n.count(c) == 1 and _MOOD.match(c) and num(c)]
    ex = ["tonal.key_scale", "tonal.chords_scale", "highlevel.genre_dortmund.value", "highlevel.genre_rosamerica.value", "uuid", "lastfm_listener_count", "lastfm_playcount"]
    d = f.read(columns=raw + mood + ex).to_pandas()
    h = np.array([int(hashlib.md5(u.encode()).hexdigest(), 16) for u in d.uuid], dtype=object)
    d = d[np.array([x % 2 == 0 for x in h])].copy()                      # the open half only
    y = pd.read_csv(_P + "hsp-l_uuid_year.csv")[["uuid", "year"]]; d = d.merge(y, on="uuid").drop_duplicates("uuid")
    d = d[(d.lastfm_listener_count >= 50) & (d.lastfm_playcount > 0) & (d.year > 1900)].reset_index(drop=True)
    sub = os.environ.get("DEVOTION_GATE_FIT_SUB")
    if sub is not None: d = d[np.array([(int(hashlib.md5(u.encode()).hexdigest(), 16) // 2) % 2 == int(sub) for u in d.uuid])].reset_index(drop=True)
    raw = [c for c in raw if d[c].std() > 0]
    return d, raw + ["tonal.key_scale_minor", "tonal.chords_scale_minor"], mood

def _target(d):
    """log plays per listener with reach, year and Essentia genre classes taken out, as normal scores"""
    ppl = (np.log(d.lastfm_playcount) - np.log(d.lastfm_listener_count)).values
    C = np.c_[np.ones(len(d)), rankdata(d.year), rankdata(d.lastfm_listener_count), pd.get_dummies(d["highlevel.genre_dortmund.value"]).values[:, 1:].astype(float), pd.get_dummies(d["highlevel.genre_rosamerica.value"]).values[:, 1:].astype(float)]
    r = ppl - C @ np.linalg.lstsq(C, ppl, rcond=None)[0]; return norm.ppf((rankdata(r) - .5) / len(r))

class _Reader:
    def __init__(s, cols): s.cols = cols
    def fit(s, d, y):
        X = _matrix(d, s.cols); s.ridge = RidgeCV(alphas=np.logspace(0, 5, 16)).fit(X, y); 
        with threadpool_limits(limits=1): s.tree = HistGradientBoostingRegressor(**_HGB).fit(X, y)     # one thread: steady timing on a shared machine, same result
        return s
    def read(s, df):
        X = _matrix(df, s.cols); z = lambda v: (v - v.mean()) / (v.std() + 1e-12); return (z(s.ridge.predict(X)) + z(s.tree.predict(X))) / 2

_d, _RAW, _MOODS = _load(); _y = _target(_d)
_FULL = _Reader(_RAW + _MOODS).fit(_d, _y)
try:
    import sys; sys.path.insert(0, "/home/claude/arena2"); import arena2 as _a2; _SC = set(_a2.sound().columns)
    _SHARED = [c for c in _RAW if _strip(c) in _SC and not c.endswith(".var")]      # means and whole-track readings only: previews are 60 s, so variances do not carry
except Exception: _SHARED = [c for c in _RAW if c.endswith(".mean") or c.count(".") == 1 or c.endswith("_scale_minor")]
_CARRY = _Reader(_SHARED).fit(_d, _y)
del _d

def devotion_reader(df): return _FULL.read(df)

def devotion_carried_to_hot100(df):
    out = np.zeros(len(df)); groups = df["store"].values if "store" in df.columns else np.zeros(len(df))
    for g in pd.unique(groups):
        k = groups == g; out[k] = _CARRY.read(df[k])
    return out

CANDIDATES = [
    dict(name="devotion_reader", kind="devotion", fn=devotion_reader, sign=+1,
         why="Plays per listener is read better from how the sound moves over the track (variances and frame-to-frame changes of every Essentia reading, plus the mood/timbre classifiers) by a ridge and a boosted-tree reader averaged on rank-normal scores than from the 53 means alone; the smallest honest description is unhurried (few onsets, few chord changes, low danceability) and full (a complex spectrum with no single dominant peak), with dark a small third.",
         baseline="ridge reader over the 53 Essentia sound means: +0.212 on the open half (fit on one half of half 0, scored on the other; +0.219 the other way round); this reader +0.329 and +0.323"),
    dict(name="devotion_carried_to_hot100", kind="sound", fn=devotion_carried_to_hot100, sign=+1,
         why="The last.fm devotion reader, rebuilt from only the mean columns the Hot 100 sound table shares and never shown a Hot 100 outcome: recordings whose sound predicts being replayed are, modestly, the hits still loved decades later (it goes with love, not with covers).",
         baseline="a cross-check, not a challenger: concentrated_spectrum scores +0.107 (previews) and +0.179 (whole recordings) on the open half; this scores +0.07 and +0.13"),
]
