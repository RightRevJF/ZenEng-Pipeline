"""Scarcity / localised surprise / memory density: three candidates. Plain arithmetic on the sung notes, nothing fitted.
Honest note: on the open half NONE of ~250 measures in this family beat what luck alone gives for the best of that many tries.
These three are the least-bad survivors (same sign in all three sets, or in the two clean ones), not confident bets."""
import math
from collections import Counter
import numpy as np


def _mono(clip):
    """one note per onset (the highest), sorted by time"""
    d = {}
    for o, p in clip:
        o = round(float(o) * 24) / 24
        if o not in d or p > d[o]: d[o] = p
    k = sorted(d)
    return np.array(k, float), np.array([d[x] for x in k], int)


def _wmean(song, f, minn=16):
    """note-weighted mean of f(onsets, pitches) over the song's clips of at least minn notes"""
    vs, ws = [], []
    for c in song["clips"]:
        if len(c) < minn: continue
        o, p = _mono(c)
        if len(p) < minn: continue
        try: v = f(o, p)
        except Exception: v = None
        if v is not None and np.isfinite(v): vs.append(float(v)); ws.append(len(p))
    return float(np.average(vs, weights=ws)) if vs else float("nan")


def top_note_isolation(song):
    """semitones between the highest pitch of the tune and the next-highest pitch it uses (the 'lonely peak')"""
    def f(o, p):
        u = np.unique(p)
        return float(u[-1] - u[-2]) if len(u) > 1 else None
    return _wmean(song, f)


def phrase_top_plateau(song):
    """split into phrases at silences (gap >= 2 beats and >= 3x the median gap); in each phrase of 4+ notes,
    the share of its notes that sit on that phrase's highest pitch; averaged over phrases. NaN if under 2 phrases."""
    def f(o, p):
        io = np.diff(o)
        b = [0] + list(np.where(io >= max(2.0, 3 * np.median(io)))[0] + 1) + [len(p)]
        v = [np.mean(p[a:c] == p[a:c].max()) for a, c in zip(b[:-1], b[1:]) if c - a >= 4]
        return np.mean(v) if len(v) >= 2 else None
    return _wmean(song, f)


def onbeat_rhythm_surprise(song):
    """each note's rhythmic surprise = -log2(how often its gap-from-the-previous-note occurs in this same tune),
    gaps binned in half-octaves of duration. Returns mean surprise of notes landing ON a quarter-note beat
    minus mean surprise of notes landing off it: is the tune's rhythmic novelty placed on the beat?"""
    def f(o, p):
        b = [int(np.clip(round(2 * math.log2(max(x, 1e-3))), -6, 6)) for x in np.diff(o)]
        c = Counter(b); n = len(b)
        x = np.array([-math.log2(c[t] / n) for t in b])
        on = np.abs(o[1:] - np.round(o[1:])) < 0.02
        return x[on].mean() - x[~on].mean() if on.sum() > 3 and (~on).sum() > 3 else None
    return _wmean(song, f)


CANDIDATES = [
    dict(name="top_note_isolation", kind="tune", fn=top_note_isolation, sign=-1,
         why="Against the scarcity idea: greater songs have a top note that is NOT a lonely outlier but sits a step above the next pitch used."),
    dict(name="phrase_top_plateau", kind="tune", fn=phrase_top_plateau, sign=+1,
         why="Greater songs return to each phrase's highest pitch several times within the phrase instead of touching it once."),
    dict(name="onbeat_rhythm_surprise", kind="tune", fn=onbeat_rhythm_surprise, sign=+1,
         why="Localised surprise: the tune's unusual rhythm values land on the beat rather than off it."),
]
