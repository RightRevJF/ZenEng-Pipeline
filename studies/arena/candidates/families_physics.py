"""families_physics: the song judged against its FAMILY rather than alone.
All three are plain arithmetic on the supplied tables; nothing is fitted, so nothing is carried over from the open half."""
import numpy as np, pandas as pd


def _year_family_distance(X, year, window, robust, clip=4.0):
    """mean absolute standardised distance of each row from the centre of the rows released within +-window years"""
    X = np.asarray(X, float); year = np.asarray(year, float); Z = np.full(X.shape, np.nan)
    for y in np.unique(year[np.isfinite(year)]):
        fam = np.abs(year - y) <= window; a = X[fam]; me = year == y
        if robust:
            mu = np.nanmedian(a, 0); sd = (np.nanpercentile(a, 75, 0) - np.nanpercentile(a, 25, 0)) / 1.349 + 1e-12
        else:
            mu = np.nanmean(a, 0); sd = np.nanstd(a, 0) + 1e-9
        Z[me] = (X[me] - mu) / sd
    return np.nanmean(np.clip(np.abs(Z), 0, clip), 1)


def sound_unlike_its_years(df):
    """Essentia sound numbers (the .mean columns): how far the recording sits from the typical hit of its own years (+-3), within its store"""
    cols = [c for c in df.columns if c.endswith(".mean") and df[c].dtype.kind == "f"]
    out = np.full(len(df), np.nan); store = df["store"].values if "store" in df.columns else np.zeros(len(df))
    for s in pd.unique(store):
        m = store == s
        out[m] = _year_family_distance(df.loc[m, cols].values, df["year"].values[m], 3, robust=True)
    return out


_SPOTIFY = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "spotify_track_duration_ms"]


def spotify_unlike_its_years(df):
    """Spotify's ten readings: mean |z| of the song against the hits released within +-2 years"""
    return _year_family_distance(df[_SPOTIFY].values, df["year"].values, 2, robust=False, clip=np.inf)


def hits_still_to_come(df):
    """years between this song and the same performer's LAST Hot 100 hit in the table (0 if it was the last or the only one)"""
    return (df.groupby("a")["year"].transform("max") - df["year"]).values.astype(float)


CANDIDATES = [
    dict(name="sound_unlike_its_years", kind="sound", fn=sound_unlike_its_years, sign=+1,
         why="A great song's recording sits far from the centre of the hits of its own years, in any direction, across nearly all 47 sound numbers at once."),
    dict(name="spotify_unlike_its_years", kind="hot100", fn=spotify_unlike_its_years, sign=+1,
         why="Same law with a second measurer: distance from the year's typical hit in Spotify's ten readings, beyond what valence and danceability already say."),
    dict(name="hits_still_to_come", kind="hot100", fn=hits_still_to_come, sign=+1,
         why="Family over time: a great song is followed by years of further hits from the same performer; hits that came BEFORE it tell nothing."),
]
