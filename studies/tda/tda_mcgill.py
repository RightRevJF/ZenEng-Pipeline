"""A rough test of 'topological data analysis of harmonic space' as a greatness vector, on McGill Billboard (studies/harmony/billboard_sections.json).
Each chord is a point: its pitch-class set's Fourier magnitudes and phases (coefficients 1-6, the standard pc-set DFT; nearness = harmonic relatedness).
  V  vocabulary cloud: the song's distinct chords. H1 = loops among the chords it uses (e.g. a cycle of fifths), H0 = clusters.
  W  journey cloud: the song's bar-by-bar chord sequence in sliding windows of 4 bars (time-delay embedding). H1 = cycles in the progression.
Readings: count of H1 features with persistence over 0.25, total H1 persistence, the longest H1 bar; and H0 clusters persisting over 0.5.
Compared with plain readings (distinct chords, share of bars outside the key, bars, loop share) and with chart peak (1 is best).
    python3 studies/tda/tda_mcgill.py      # writes studies/tda/tda_mcgill.json"""
import json, sys, os, re, math, collections
import numpy as np
from ripser import ripser
from scipy.stats import spearmanr
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "..", "lib", "luthier")); import chord_writer as C
S = json.load(open(os.path.join(H, "..", "harmony", "billboard_sections.json")))
def vec(pcs):
    x = np.zeros(12); x[list(pcs)] = 1; F = np.fft.fft(x)[1:7]; return np.concatenate([F.real, F.imag]) / max(1, len(pcs))
def tones(rn):
    try: return frozenset(C.tones(C.norm(rn)))
    except Exception: return None
def h1(P, thr):
    if len(P) < 4: return 0, 0.0, 0.0, 1
    D = ripser(P, maxdim=1)["dgms"]; h0, h1_ = D[0], D[1]
    pers = h1_[:, 1] - h1_[:, 0] if len(h1_) else np.array([])
    p0 = h0[:, 1] - h0[:, 0]; clusters = int(np.sum(np.isinf(p0)) + np.sum(p0[np.isfinite(p0)] > 0.5))
    return int(np.sum(pers > thr)), float(pers.sum()), float(pers.max()) if len(pers) else 0.0, clusters
rows = []
for s in S:
    bars = []; out = 0; IN = C.IN.get(s["mode"], C.IN["major"])
    for sec in s["sections"]:
        if C.KIND.get(sec["label"]) not in ("verse", "chorus", "bridge", "pre"): continue
        for b in sec["bars"]:
            t = [x for x in (C.norm(r) for r in b["rn"]) if x and tones(x) is not None]
            if t: bars.append(t[0]); out += t[0] not in IN
    if len(bars) < 16: continue
    try: peak = int(s["peak"])
    except Exception: continue
    voc = sorted(set(bars)); V = np.array([vec(tones(x)) for x in voc])
    seq = np.array([vec(tones(x)) for x in bars]); W = np.array([seq[i:i + 4].ravel() for i in range(len(seq) - 3)])
    if len(W) > 300: W = W[np.linspace(0, len(W) - 1, 300).astype(int)]
    v = h1(V, 0.25); w = h1(W, 0.25)
    per = sum(1 for i in range(len(bars) - 8) if bars[i:i + 4] == bars[i + 4:i + 8]) / max(1, len(bars) - 8)
    rows.append(dict(id=s["id"], title=s["title"], artist=s["artist"], peak=peak, bars=len(bars), distinct=len(voc), out=out / len(bars), loop_share=per,
                     V_loops=v[0], V_total=v[1], V_max=v[2], V_clusters=v[3], W_loops=w[0], W_total=w[1], W_max=w[2]))
R = {k: np.array([r[k] for r in rows], float) for k in rows[0] if k not in ("id", "title", "artist")}
good = -R["peak"]                                                                                     # higher is better
TDA = ("V_loops", "V_total", "V_max", "V_clusters", "W_loops", "W_total", "W_max"); PLAIN = ("distinct", "out", "bars", "loop_share")
res = dict(songs=len(rows), spread={k: [round(float(x), 3) for x in np.quantile(R[k], (0.1, 0.25, 0.5, 0.75, 0.9))] + [round(float(np.mean(R[k] == 0)), 3)] for k in TDA + PLAIN},
           against_peak={k: [round(float(x), 3) for x in spearmanr(R[k], good)] for k in TDA + PLAIN},
           against_plain={t: {p: round(float(spearmanr(R[t], R[p])[0]), 3) for p in PLAIN} for t in TDA})
# what TDA adds beyond the plain readings: rank residuals of each TDA reading on the plain ones, against peak
from scipy.stats import rankdata
Xp = np.column_stack([rankdata(R[p]) for p in PLAIN] + [np.ones(len(rows))])
def resid(y): y = rankdata(y); b = np.linalg.lstsq(Xp, y, rcond=None)[0]; return y - Xp @ b
res["beyond_plain_against_peak"] = {t: [round(float(x), 3) for x in spearmanr(resid(R[t]), good)] for t in TDA}
top = sorted(rows, key=lambda r: -r["W_total"])[:5]; low = sorted(rows, key=lambda r: r["W_total"])[:5]
res["most_journey_persistence"] = [(r["title"], r["artist"], r["peak"], round(r["W_total"], 2), r["distinct"]) for r in top]
res["least"] = [(r["title"], r["artist"], r["peak"], round(r["W_total"], 2), r["distinct"]) for r in low]
json.dump(res, open(os.path.join(H, "tda_mcgill.json"), "w"), indent=1); print(json.dumps(res, indent=1))
