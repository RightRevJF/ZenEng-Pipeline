"""Candidates from the layers / form / arrangement researcher. Plain arithmetic only; nothing is fitted.
Candidates 1 and 2 read the full multi-track MIDI (set 3 only; NaN elsewhere). Candidate 3 is one column of the sound table."""
import warnings
import numpy as np

_CACHE = {}

def _arrangement(song):
    """Parse the song's multi-track MIDI once; return the few plain facts the candidates use (or None)."""
    path = song.get("midi_path") if isinstance(song, dict) else None
    if not path:
        return None
    if path in _CACHE:
        return _CACHE[path]
    out = None
    try:
        import pretty_midi
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pm = pretty_midi.PrettyMIDI(path)
        pitched = [i for i in pm.instruments if not i.is_drum and len(i.notes) > 0]
        drums = [i for i in pm.instruments if i.is_drum and len(i.notes) > 0]
        end = pm.get_end_time()
        if pitched and end > 0:
            P = np.array([n.pitch for i in pitched for n in i.notes], float)
            D = np.array([n.end - n.start for i in pitched for n in i.notes], float)
            nbeats = max(len(pm.get_beats()), 1)
            out = dict(
                low43=float(D[P < 43].sum() / D.sum()),          # share of all sounding note-time below G2 (bass register)
                low55=float(D[P < 55].sum() / D.sum()),          # ... below G3 (bass plus low guitar / left hand)
                n_prog=len(set(i.program for i in pitched)),     # number of different instrument sounds written
                drum_per_beat=sum(len(i.notes) for i in drums) / nbeats)  # drum hits per beat
    except Exception:
        out = None
    if len(_CACHE) > 5000:
        _CACHE.clear()
    _CACHE[path] = out
    return out

def low_register_weight(song):
    """Share of the arrangement's sounding note-time that lies in the low register (mean of the below-G2 and below-G3 shares)."""
    a = _arrangement(song)
    return float("nan") if a is None else (a["low43"] + a["low55"]) / 2

def spare_arrangement(song):
    """Few different instrument sounds and few drum hits per beat (higher = sparer)."""
    a = _arrangement(song)
    return float("nan") if a is None else -(np.log1p(a["n_prog"]) + np.log1p(a["drum_per_beat"]))

def tempo_lock(df):
    """How much of the recording's beat-interval histogram sits on its single main tempo (Essentia bpm histogram, first peak weight)."""
    return np.asarray(df["bpm_histogram_first_peak_weight.mean"], float)

CANDIDATES = [
    dict(name="low_register_weight", kind="tune", fn=low_register_weight, sign=+1,
         why="The written arrangement spends more of its sounding time in the low register: the page-level twin of the low-band energy finding in the sound."),
    dict(name="spare_arrangement", kind="tune", fn=spare_arrangement, sign=+1,
         why="Great songs are written for fewer instrument sounds with a less busy drum part; agrees with lower spectral complexity and onset rate in the recordings."),
    dict(name="tempo_lock", kind="sound", fn=tempo_lock, sign=-1,
         why="Great recordings are less rigidly locked to one machine-steady tempo; held at about -0.13 in both sound stores and inside each decade."),
]
