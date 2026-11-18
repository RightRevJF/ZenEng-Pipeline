"""Breath in sung melodies: phrase onsets and the time from one phrase onset to the next (the breath cycle), in seconds.
CoCoPops songs carry the McGill audio timestamps, so quarter-note time maps to clock time; Luthier records carry their tempo.
A phrase ends where the next note comes 1.5 beats or more after the last onset (a held note or a rest: where a singer breathes)."""
import re, os, json, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ssm")); import ssm_lib as L
def read_hum_timed(path):
    Lr = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8", errors="ignore") if l.strip() and not l.startswith("!!")]
    head = next(r for r in Lr if r[0].startswith("**")); kern = head.index("**kern"); ts = head.index("**timestamp") if "**timestamp" in head else None
    if ts is None: return None
    t = 0.0; tb = None; anchors = []; notes = []
    for r in Lr[Lr.index(head) + 1:]:
        if len(r) <= max(kern, ts): continue
        a = r[kern]
        if a.startswith("*"):
            for x in r:
                m = re.match(r"\*tb(\d+)", x)
                if m: tb = int(m.group(1))
            continue
        if a.startswith(("!", "=")): continue
        try:
            sec = float(r[ts]); anchors.append((t, sec))
        except ValueError: pass
        if tb:
            if a not in (".", "") and L.kern_pitch(a) is not None and not a.startswith("]") and "_" not in a and "r" not in a: notes.append((t, L.kern_pitch(a)))
            t += 4.0 / tb
        else:
            if a in (".", ""): continue
            d = L.kern_dur(a); p = L.kern_pitch(a)
            if p is not None and "]" not in a and "_" not in a: notes.append((t, p))
            if d: t += d
    if len(anchors) < 4 or len(notes) < 40: return None
    aq, asec = np.array([x for x, _ in anchors]), np.array([y for _, y in anchors]); o = np.argsort(aq)
    sec = np.interp([q for q, _ in notes], aq[o], asec[o]); return [(q, s, p) for (q, p), s in zip(notes, sec)], float(asec.max() - asec.min())
def read_record_timed(path):
    R = json.load(open(path)); spq = 60.0 / R["bpm"] * (1.5 if R["metre"] in ("6/8", "9/8", "12/8") else 1.0)
    ns = [(n["on"] / 12.0, n["on"] / 12.0 * spq, n["midi"]) for n in R["melody"]["notes"] if n.get("text")]
    return ns, ns[-1][1] - ns[0][1]
def breaths(notes, beat_q=1.0, gap_beats=1.5):
    """notes: (quarters, seconds, pitch). Returns phrase onsets (seconds), cycles (seconds), and the gap before each phrase (seconds)."""
    ons = [notes[0]]; gaps = [None]
    for a, b in zip(notes, notes[1:]):
        if b[0] - a[0] >= gap_beats * beat_q: ons.append(b); gaps.append(b[1] - a[1])
    starts = [s for _, s, _ in ons]; cyc = list(np.diff(starts)); return starts, cyc, gaps
def song_readings(notes, length_s):
    starts, cyc, gaps = breaths(notes); cyc = [c for c in cyc if 0.5 < c < 40]
    if len(cyc) < 6: return None
    c = np.array(cyc); return dict(cycle_median=float(np.median(c)), cycle_cv=float(np.std(c) / np.mean(c)), resonance=float(np.mean((c >= 8) & (c <= 12))),
        quick=float(np.mean(c < 4)), phrases=len(starts), per_min=60.0 * len(starts) / max(1, length_s))
