"""Luthier v7, fix 730: the judge of 715 with repeated notes read by window. Needs luthier_judge4.py and luthier_judge4_data.json beside it.
A window is the first eight bars of each section as it comes round (a section begins where the label changes or after four silent bars); windows of
under twelve notes or four sung bars are not read. A window's reading is the share of its moves that repeat the note, placed among kept windows
of its density (notes a sung bar: under 3.5, 3.5 to 4.5, 4.5 to 5.5, 5.5 and over). A song's reading is the place of its most-repeating window.
Eligible for the pick: eligible under 715, and that reading inside the kept songs' middle half. The charge, the place and the distance are 715's.
Labels: 'Last Chorus' is read as a chorus (fix 737), as kept songs label it.
score(notes) and pick(builds) take what luthier_judge4 takes: notes as (onset in twelfths of a beat from the song's first bar line, pitch, section label)."""
import re, numpy as np
import luthier_judge4 as J
BANDS = [3.5, 4.5, 5.5]
def _band(d): return int(np.searchsorted(BANDS, d, side="right"))
def _lab(x): return re.sub(r"(?i)^\s*(last|final)\s+", "", str(x))
def windows(s):
    t, p = np.asarray(s["t"]), np.asarray(s["p"]); insts = {}; out = []
    for b in J.song_bars(s): insts.setdefault(b["inst"], []).append(b)
    for i, bs in insts.items():
        b0 = bs[0]["b"]; m = (t >= b0 * 48) & (t < (b0 + 8) * 48) & np.isin(t // 48, [b["b"] for b in bs]); q = p[m]; nb = len(set((t[m] // 48).tolist()))
        if len(q) < 12 or nb < 4: continue
        out.append((bs[0]["sec"], len(q) / nb, float(np.mean(np.diff(q) == 0))))
    return out
_T = {k: np.sort([r for s in J._KEPT for _, d, r in windows(s) if _band(d) == k]) for k in range(4)}
def _place(d, r): T = _T[_band(d)]; return float(np.searchsorted(T, r, side="right") / len(T))
def window_reading(s):
    W = windows(s); pl = [_place(d, r) for _, d, r in W]
    return (max(pl) if len(W) >= 2 else float("nan")), [(sec, round(d, 2), round(r, 3), round(c, 3)) for (sec, d, r), c in zip(W, pl)]
_K = np.array([window_reading(s)[0] for s in J._KEPT]); LO, HI = (float(x) for x in np.nanpercentile(_K, (25, 75)))
def score(notes):
    notes = [(n[0], n[1], _lab(n[2])) for n in notes]; r = J.score(notes); ns = sorted(notes, key=lambda n: n[0])
    s = dict(t=np.array([int(n[0]) for n in ns]), p=np.array([int(n[1]) for n in ns]), sec=np.array([str(n[2]) for n in ns])); m, W = window_reading(s)
    r["most-repeating window, place for its density"] = m; r["windows: label, notes a bar, repeats, place"] = W; r["kept middle half of that place"] = [round(LO, 3), round(HI, 3)]
    r["eligible under 715"] = r["eligible for the pick"]; r["eligible for the pick"] = bool(r["eligible under 715"] and LO <= m <= HI); return r
def pick(builds):
    """builds: list of (id, notes). Returns (id of the pick, list of results)."""
    R = [(i, score(n)) for i, n in builds]; el = [(i, r) for i, r in R if r["eligible for the pick"]]
    if not el: return None, R
    least = min(r["charge"] for _, r in el); near = [(i, r) for i, r in el if r["charge"] <= least + 0.02]; return min(near, key=lambda x: x[1]["distance from the kept medians"])[0], R
