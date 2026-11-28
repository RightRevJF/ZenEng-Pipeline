"""Run 12, Inventor, round 1: NOTES-SIDE check only (reads no outcome; lakh_notes_side.json has its outcome keys removed).
ROUGH (P11-4): Sethares (1993; 2005 code) roughness of what sounds together, LPD-5 cleansed, tracks 1-4 (piano, guitar, bass, strings),
sampled at every beat (24 steps). Partials n = 1..6 at n*f0, amplitude 0.88**(n-1), f0 = 440*2**((p-69)/12).
Pair of partials (f<f', amplitudes a, a'): d = min(a,a') * 5 * (exp(-3.51 s (f'-f)) - exp(-5.75 s (f'-f))), s = 0.24/(0.0207 f + 18.96).
Note-pair roughness R[p,q] = sum of d over the 36 partial pairs (one partial from each note). A beat's set = distinct sounding pitches.
ROUGH = sum over beats of sum_{p<q} R[p,q] / sum over beats of C(n,2)   (roughness per sounding pair; density divided out).
Readings: ROUGH_BEAT (mean per beat, density kept), PCE_ALL (pitch-class entropy of sounding time, tracks 1,2,4),
PCE_SKY (pitch-class entropy of the skyline, highest of 1,2,4 at each eighth: a melody proxy), NPB (mean distinct pitches per beat).
Stability: Spearman between two MIDI files of one song (the 226 arrangement-pair songs). Overlap with run 07's ch_rep, ln_bars.
Writes only /home/claude/dl/run12/inventor_rough_check.json.
"""
import os, json, glob, math, random, sys
import numpy as np
from multiprocessing import Pool
from scipy.stats import spearmanr
LPD = "/home/claude/dl/lpd/lpd_5/lpd_5_cleansed"
OUT = "/home/claude/dl/run12/inventor_rough_check.json"

def note_pair_table():
    f0 = 440.0 * 2 ** ((np.arange(128) - 69) / 12.0); n = np.arange(1, 7); amp = 0.88 ** (n - 1)
    F = f0[:, None] * n[None, :]
    R = np.zeros((128, 128))
    for p in range(128):
        for q in range(p + 1, 128):
            fa, fb = F[p][:, None], F[q][None, :]
            lo, hi = np.minimum(fa, fb), np.maximum(fa, fb)
            s = 0.24 / (0.0207 * lo + 18.96); x = hi - lo
            d = np.minimum(amp[:, None], amp[None, :]) * 5 * (np.exp(-3.51 * s * x) - np.exp(-5.75 * s * x))
            R[p, q] = R[q, p] = d.sum()
    return R
R = note_pair_table()

def roll(z, k, T):
    shp = z[f"pianoroll_{k}_csc_shape"]
    if shp[0] == 0: return None
    ind, ptr = z[f"pianoroll_{k}_csc_indices"], z[f"pianoroll_{k}_csc_indptr"]
    M = np.zeros((T, 128), bool)
    for p in range(128):
        a, b = ptr[p], ptr[p + 1]
        if b > a: M[ind[a:b], p] = True
    return M

def ent(w):
    w = w[w > 0]; 
    if w.sum() == 0: return None
    p = w / w.sum(); return float(-(p * np.log2(p)).sum())

def measure(path):
    try: z = np.load(path, allow_pickle=False)
    except Exception: return None
    T = len(z["downbeat"]); rs = {k: roll(z, k, T) for k in (1, 2, 3, 4)}
    if all(v is None for v in rs.values()): return None
    allm = np.zeros((T, 128), bool)
    for v in rs.values():
        if v is not None: allm |= v
    beats = allm[::24]; nb = beats.sum(1); act = nb >= 1
    if act.sum() < 64: return None
    num = 0.0; pairs = 0.0
    for row in beats[nb >= 2]:
        ps = np.flatnonzero(row); sub = R[np.ix_(ps, ps)]; num += sub.sum() / 2; pairs += len(ps) * (len(ps) - 1) / 2
    hm = np.zeros((T, 128), bool)
    for k in (1, 2, 4):
        if rs[k] is not None: hm |= rs[k]
    pcw = np.array([hm[:, pc::12].sum() for pc in range(12)], float)
    e8 = hm[::12]; has = e8.any(1); top = 127 - np.argmax(e8[:, ::-1], 1)
    sky = np.bincount(top[has] % 12, minlength=12).astype(float)
    return dict(ROUGH=num / pairs if pairs else None, ROUGH_BEAT=num / act.sum(), NPB=float(nb[act].mean()),
                PCE_ALL=ent(pcw), PCE_SKY=ent(sky))

def files(s):
    out = []
    for tid in s["tids"]:
        for m in s["md5s"]:
            p = f"{LPD}/{tid[2]}/{tid[3]}/{tid[4]}/{tid}/{m}.npz"
            if os.path.exists(p) and p not in out: out.append(p)
    return out

def job(s):
    return s["key"], [measure(p) for p in files(s)[:2]]

if __name__ == "__main__":
    S = json.load(open("/home/claude/dl/run12/lakh_notes_side.json"))
    pairs = [s for s in S if len(s["md5s"]) >= 2]
    random.seed(12); others = random.sample([s for s in S if len(s["md5s"]) < 2], 900)
    with Pool(2) as P: res = dict(P.map(job, pairs + others, chunksize=8))
    keys = ["ROUGH", "ROUGH_BEAT", "NPB", "PCE_ALL", "PCE_SKY"]
    rep = {}
    # stability between two files of one song
    for k in keys:
        a = [(v[0][k], v[1][k]) for key, v in res.items() if len(v) == 2 and v[0] and v[1] and v[0][k] is not None and v[1][k] is not None]
        rep[f"stab_{k}"] = dict(n=len(a), spearman=float(spearmanr([x for x, _ in a], [y for _, y in a])[0]))
    # song values (mean of files) and overlaps
    meta = {s["key"]: s for s in pairs + others}
    rows = []
    for key, v in res.items():
        v = [x for x in v if x]
        if not v: continue
        d = {k: np.mean([x[k] for x in v if x[k] is not None]) if any(x[k] is not None for x in v) else None for k in keys}
        d.update(ch_rep=meta[key].get("ch_rep"), ln_bars=meta[key].get("ln_bars"), artist=meta[key]["artist"]); rows.append(d)
    ov = {}
    for k in keys:
        for j in keys + ["ch_rep", "ln_bars"]:
            if j <= k and j in keys: continue
            a = [(r[k], r[j]) for r in rows if r[k] is not None and r[j] is not None]
            ov[f"{k}~{j}"] = round(float(spearmanr(*zip(*a))[0]), 3)
    # within-artist share of variance (artists with 2+ songs in the sample)
    from collections import defaultdict
    wa = {}
    for k in keys:
        g = defaultdict(list)
        for r in rows:
            if r[k] is not None and np.isfinite(r[k]): g[r["artist"]].append(r[k])
        allv = np.array([x for v in g.values() for x in v]); g2 = {a: v for a, v in g.items() if len(v) >= 2}
        within = sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in g2.values()); tot = sum(((np.array(v) - allv.mean()) ** 2).sum() for v in g2.values())
        wa[k] = dict(artists=len(g2), within_share=round(float(within / tot), 3))
    rep.update(songs=len(rows), overlap=ov, within_artist=wa,
               quantiles={k: [round(float(x), 4) for x in np.nanpercentile([r[k] for r in rows if r[k] is not None], [10, 50, 90])] for k in keys})
    json.dump(rep, open(OUT, "w"), indent=1); print(json.dumps(rep, indent=1))
