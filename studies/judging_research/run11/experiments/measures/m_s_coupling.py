"""Jason's S = 1 + g/pi, read with g as a COUPLING (run 11, after seeing results; Jason's request, 28 Nov 2026).
g = the detrended cross-correlation coefficient rho_DCCA (Zebende 2011) between the melody's height and the bass line's height,
at the phrase scale (box sizes of one bar and two bars, averaged). S_C = 1 + G_COUP/pi.
Series, on an eighth-note grid over the span where both melody and harmony are defined:
  melody: the MIDI-like pitch (12*octave + pc) of the note sounding at each grid point; through a rest, the last pitch held.
  bass:   each chord's bass pitch class (root + its inversion's stacked interval), unwrapped by minimal motion (each new bass at
          the octave nearest the previous bass; the first at 36 + pc), held through the chord.
rho_DCCA(n): profiles X = cumsum(x - mean x), Y likewise; overlapping boxes of n+1 points; each box's X and Y detrended by a
least-squares line; F2xy = mean over boxes of mean(rx*ry); rho = F2xy / sqrt(F2xx * F2yy). n = 2*bpb and 4*bpb grid steps.
A clip needs at least 8*bpb grid points (four bars) and a non-constant melody and bass. No fitted settings.
G_ABS = |G_COUP| (the criticality reading: |S_C - 1| = |g|/pi). G_1BAR, G_2BAR: each scale alone."""
import numpy as np
from math import pi
KEYS = ["G_COUP", "S_C", "G_ABS", "G_1BAR", "G_2BAR"]

def _bass_pc(h):
    iv = list(h.get("root_position_intervals") or []); inv = int(h.get("inversion") or 0)
    acc = [0]
    for x in iv: acc.append(acc[-1] + x)
    return (h["root_pitch_class"] + (acc[inv] if inv < len(acc) else 0)) % 12

def _rho(x, y, n):
    X = np.cumsum(x - x.mean()); Y = np.cumsum(y - y.mean()); N = len(X)
    if N < n + 1: return None
    t = np.arange(n + 1); A = np.vstack([t, np.ones_like(t)]).T; P = A @ np.linalg.pinv(A)
    fxy = fxx = fyy = 0.0; k = 0
    for i in range(0, N - n):
        bx = X[i:i + n + 1]; by = Y[i:i + n + 1]
        rx = bx - P @ bx; ry = by - P @ by
        fxy += (rx * ry).mean(); fxx += (rx * rx).mean(); fyy += (ry * ry).mean(); k += 1
    if fxx <= 0 or fyy <= 0: return None
    return float(fxy / np.sqrt(fxx * fyy))

def clip_measure(mel, a):
    H = sorted([h for h in (a.get("harmony") or []) if h.get("root_pitch_class") is not None and h["offset"] > h["onset"]],
               key=lambda h: h["onset"])
    if len(H) < 2: return None
    bpb = mel["bpb"]; on = np.array(mel["onset"]); p = np.array(mel["pitch"], float)
    t0 = max(on[0], H[0]["onset"]); t1 = min(on[-1] + mel["dur"][-1], H[-1]["offset"])
    grid = np.arange(t0, t1, 0.5)
    if len(grid) < 8 * bpb: return None
    mi = np.searchsorted(on, grid, side="right") - 1; x = p[np.clip(mi, 0, None)]
    # bass, unwrapped by minimal motion
    hb = []; prev = None
    for h in H:
        pc = _bass_pc(h)
        v = 36 + pc if prev is None else min((prev + d for d in range(-6, 7) if (prev + d) % 12 == pc), key=lambda q: abs(q - prev))
        hb.append(v); prev = v
    hon = np.array([h["onset"] for h in H]); hi = np.clip(np.searchsorted(hon, grid, side="right") - 1, 0, None)
    y = np.array(hb, float)[hi]
    if x.std() == 0 or y.std() == 0: return None
    r1 = _rho(x, y, int(2 * bpb)); r2 = _rho(x, y, int(4 * bpb))
    if r1 is None or r2 is None: return None
    g = (r1 + r2) / 2
    return dict(G_COUP=g, S_C=1 + g / pi, G_ABS=abs(g), G_1BAR=r1, G_2BAR=r2)
