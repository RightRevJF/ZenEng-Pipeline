"""Run 12, the Geometer: notes-side checks on Lakh whole songs (no outcome read). Writes only /home/claude/dl/run12/geometer_lakh_check.json.
Per MIDI file (LPD-5 cleansed): skyline melody x = highest pitch of tracks 1, 2, 4 at each eighth (run 11's `lines`, held through gaps).
  L_H   : pitch-class entropy (bits) of x (REP on the skyline).     L_C, L_E5, L_REST: Parseval split (m_geometer) of x's pc profile.
  T_E5, T_C : the same on the whole texture (tracks 1-4, every sounding pitch-step counted).
  PI8   : Gaussian predictive information of x per eighth, K = 32 (4 bars);  PI4: per beat, K = 16 (4 bars); bias K(K+1)/4n removed.
  H8    : log one-step innovation variance of x per eighth after K = 32 (Kolmogorov-Szego; local unpredictability).
Songs: the 226 with 2+ files (pair stability = Spearman file 1 vs file 2) plus 500 others (seed 12) for overlap with run 07's ch_rep, ln_bars."""
import os, sys, json, math, random
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m_geometer import fourier, pacf, pred_info
LPD = "/home/claude/dl/lpd/lpd_5/lpd_5_cleansed"; OUT = "/home/claude/dl/run12/geometer_lakh_check.json"

def load(path):
    z = np.load(path, allow_pickle=False); T = len(z["downbeat"])
    hi = np.full(T, -1, np.int16); pcs = np.zeros(12)
    for k in (1, 2, 3, 4):
        shp = z[f"pianoroll_{k}_csc_shape"]
        if shp[0] == 0: continue
        ind, ptr = z[f"pianoroll_{k}_csc_indices"], z[f"pianoroll_{k}_csc_indptr"]
        for p in range(128):
            a, b = ptr[p], ptr[p + 1]
            if b > a:
                pcs[p % 12] += b - a
                if k != 3: t = ind[a:b]; hi[t] = np.maximum(hi[t], p)
    return hi, pcs

def ent(c):
    c = c[c > 0]; p = c / c.sum(); return float(-(p * np.log2(p)).sum())

def file_measure(path):
    try: hi, pcs = load(path)
    except Exception: return None
    s = hi[::12].astype(float); s[s < 0] = np.nan
    if np.isfinite(s).sum() < 128: return None
    i0 = int(np.argmax(np.isfinite(s))); i1 = len(s) - int(np.argmax(np.isfinite(s[::-1]))); x = s[i0:i1].copy()
    for i in range(1, len(x)):
        if not np.isfinite(x[i]): x[i] = x[i - 1]
    if np.std(x) == 0 or len(x) < 256: return None
    pc = np.bincount((x.astype(int) % 12), minlength=12).astype(float)
    C, e5 = fourier(pc); TC, te5 = fourier(pcs)
    a = pacf(x, 32); v = np.var(x) * np.prod(1 - np.clip(a, -.999999, .999999) ** 2)
    return dict(L_H=ent(pc), L_C=C, L_E5=e5, L_REST=C - e5, T_C=TC, T_E5=te5, PI8=pred_info(x, 32), PI4=pred_info(x[::2], 16),
                H8=float(math.log(v)), ln_n=math.log(len(x)))

def _p(tid, md5): return os.path.join(LPD, tid[2], tid[3], tid[4], tid, md5 + ".npz")
def _job(a): return a[0], a[3], file_measure(_p(a[1], a[2]))

if __name__ == "__main__":
    S = json.load(open("/home/claude/dl/run12/lakh_notes_side.json"))
    multi = [s for s in S if len(s["md5s"]) >= 2]; rest = [s for s in S if len(s["md5s"]) < 2]
    random.seed(12); sing = random.sample(rest, 500)
    jobs = [(s["key"], s["tids"][j], s["md5s"][j], j) for s in multi for j in (0, 1)] + [(s["key"], s["tids"][0], s["md5s"][0], 0) for s in sing]
    with Pool(2) as p: res = p.map(_job, jobs, chunksize=8)
    out = {}
    for k, j, m in res:
        if m: out.setdefault(k, {})[str(j)] = m
    json.dump(out, open(OUT, "w")); print("files", len(jobs), "with value", sum(len(v) for v in out.values()))
