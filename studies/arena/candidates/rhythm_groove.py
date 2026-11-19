"""Rhythm / phrasing / time candidates for the greatness arena. Plain arithmetic only; nothing is fitted."""
import numpy as np


def tempo_not_locked(df):
    """Share of the recording's beat intervals that sit at its single commonest tempo (Essentia bpm histogram,
    first peak weight). Low = the pulse breathes or shifts; high = one rigid, machine-steady tempo. Sign is -1."""
    return np.asarray(df["bpm_histogram_first_peak_weight.mean"], dtype=float)


def sparse_onsets(df):
    """Sound events (onsets) per second in the recording. Sign is -1: fewer events per second leans great."""
    return np.asarray(df["onset_rate"], dtype=float)


def long_short_contrast(song):
    """Within-phrase nPVI of the sung rhythm: mean of |a-b| / ((a+b)/2) over neighbouring note-to-note gaps a, b,
    skipping any pair that touches a rest of 2+ beats. High = long and short notes alternate (dotted, lilting);
    low = runs of even notes. Uses no bar lines, so it is valid in set 2 as well. Sign is +1."""
    vals, wts = [], []
    for clip in song["clips"]:
        o = np.array(sorted(set(round(float(x[0]) * 4) / 4 for x in clip)))
        if len(o) < 12:
            continue
        i = np.diff(o)
        a, b = i[:-1], i[1:]
        ok = (a < 2) & (b < 2)
        if ok.sum() < 5:
            continue
        vals.append(float(np.mean(np.abs(a - b)[ok] / ((a + b)[ok] / 2))))
        wts.append(len(o))
    if not vals:
        return float("nan")
    return float(np.average(vals, weights=wts))


CANDIDATES = [
    dict(name="tempo_not_locked", kind="sound", fn=tempo_not_locked, sign=-1,
         why="Recordings whose beat is not pinned to one rigid tempo (lower first tempo-histogram peak weight) scored higher on G in both sound stores."),
    dict(name="long_short_contrast", kind="tune", fn=long_short_contrast, sign=+1,
         why="Tunes whose neighbouring notes differ in length (high within-phrase nPVI) rather than running evenly lean great, mostly via being covered more."),
    dict(name="sparse_onsets", kind="sound", fn=sparse_onsets, sign=-1,
         why="Fewer sound events per second leaned great in both stores, but it is weak and mostly overlaps the tempo-lock measure."),
]
