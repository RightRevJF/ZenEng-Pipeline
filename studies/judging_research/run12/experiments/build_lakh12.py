"""Run 12: the notes-side Lakh cache (deterministic; reads NO outcome). Frozen by the chair before any outcome is joined.

Usage: python3 build_lakh12.py [max_songs]  -> /home/claude/dl/run12/lakh_measures12.json  (about 5-10 min on 2 cores)

Songs: /home/claude/dl/run12/lakh_notes_side.json (run 07's 5,901 within-artist Lakh songs, outcome keys removed by the orchestrator).
Files: LPD-5 cleansed npz (4/4, 24 steps per beat; tracks 0 drums, 1 piano, 2 guitar, 3 bass, 4 strings).

Per MIDI file (every recipe fixed here; nothing is fitted):
  Skyline s[e] = the highest pitch sounding on tracks 1, 2, 4 at eighth e (every 12th step; -1 = none), trimmed from the first to the
  last sounding eighth (run 11's s_coupling `lines`, the Listener's and the Geometer's skyline). A file needs >= 128 sounding eighths.
  Duration-weighted skyline pitch-class profile p (count of sounding eighths per pitch class; rests carry nothing):
    REP_L  = Shannon entropy (bits) of p                      (run 11's REP recipe, pc_entropy, on the skyline)
    C_L    = 12 sum p^2 - 1;  E5_L = 2|f5|^2;  REST_L = C_L - E5_L  (Geometer's Parseval split, m_geometer.fourier)
    TOP_L  = the largest pitch-class share max p              (Geometer round 2: held in FIFTHS)
  Events (Listener's recipe): sounding skyline eighths, consecutive equal pitches merged, mapped to pitch class.
    NEV, LNEV = ln NEV (needs >= 128 events for the event measures);  H1 = plug-in pc entropy of the events;
    PI3c = 2H(3) - H(6) on the pc events minus the mean of the same over 10 permutations (seed int(md5[:8], 16));
    EVLEN = sounding eighths / NEV (mean event length, Skeptic: G2's grid carries duration).
  REPBAR = share of non-empty skyline bars (8 eighths, absolute grid, exact pitches and rests) equal to an earlier bar of the file.
  Gaussian predictive information (Geometer R12-G2, a reading): x = skyline held through gaps (MIDI pitch), n >= 256 eighths,
    PI8 = -1/2 sum_{k<=32} k ln(1 - a_k^2) - 32*33/(4n), a_k by Levinson-Durbin; H8 = ln of the one-step innovation variance.
  Texture: NPB = mean distinct pitches per beat over tracks 1-4 (beats with a note; every 24th step); ACT = non-empty tracks of 0-4;
    PCE_ALL = entropy of the pitch-class profile of sounding steps over tracks 1, 2, 4 (PROF, 12 shares, kept for duplicates/CANAL).
  ROUGH_X (Inventor round 2): at every beat, the distinct sounding pitches of tracks 1-4; Sethares partials n = 1..6, amplitude 0.88^(n-1);
    the sum of note-pair roughness over pairs whose interval is not a multiple of 12, divided by the number of such pairs (all beats).
    REG = mean over beats of the mean sounding pitch; OCT = octave-multiple pairs / all pairs.
Near-duplicate rule (chair, frozen): within a song, a file whose PROF has min over 12 rotations of JSD (bits) < 1e-4 with an EARLIER
  kept file of the same song is a near-duplicate and is dropped (counted once). Song value = mean over kept files with a value;
  'pair' = values of the first two kept files (the two-file stability gate, on non-duplicate pairs only).
Credit: Lakh MIDI Dataset (Raffel 2016) / LPD (Dong et al. 2018), CC BY 4.0.
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

LPD = os.environ.get("LPD_DIR", "/home/claude/dl/lpd/lpd_5/lpd_5_cleansed")
SIDE = "/home/claude/dl/run12/lakh_notes_side.json"
OUT = os.environ.get("LAKH12_CACHE", "/home/claude/dl/run12/lakh_measures12.json")
NSH = 10
KEYS = ["REP_L", "C_L", "E5_L", "REST_L", "TOP_L", "NEV", "LNEV", "H1", "PI3c", "EVLEN", "REPBAR", "PI8", "H8",
        "NPB", "ACT", "PCE_ALL", "ROUGH_X", "REG", "OCT"]
_W = np.exp(-2j * np.pi * np.outer(np.arange(12), np.arange(12)) / 12)


def _rough_table():
    f0 = 440.0 * 2 ** ((np.arange(128) - 69) / 12.0); n = np.arange(1, 7); amp = 0.88 ** (n - 1)
    F = f0[:, None] * n[None, :]; R = np.zeros((128, 128)); am = np.minimum(amp[:, None], amp[None, :])
    for p in range(128):
        for q in range(p + 1, 128):
            fa, fb = F[p][:, None], F[q][None, :]; lo, hi = np.minimum(fa, fb), np.maximum(fa, fb)
            s = 0.24 / (0.0207 * lo + 18.96); x = hi - lo
            R[p, q] = R[q, p] = (am * 5 * (np.exp(-3.51 * s * x) - np.exp(-5.75 * s * x))).sum()
    return R
RT = None


def _ent(c):
    c = np.asarray(c, float); c = c[c > 0]
    if c.sum() == 0: return None
    p = c / c.sum(); return float(-(p * np.log2(p)).sum())


def _H(seq, L, base):
    n = len(seq) - L + 1
    if n < 2: return float("nan")
    code = np.zeros(n, np.int64)
    for j in range(L): code = code * base + seq[j:j + n]
    _, c = np.unique(code, return_counts=True); p = c / n
    return float(-(p * np.log2(p)).sum())


def _pi3(seq): return 2 * _H(seq, 3, 12) - _H(seq, 6, 12)


def _pacf(x, K):
    x = np.asarray(x, float) - np.mean(x); n = len(x)
    g = np.array([np.dot(x[:n - k], x[k:]) / n for k in range(K + 1)])
    if g[0] <= 0: return None
    a = np.zeros(K + 1); phi = np.zeros(K + 1); v = g[0]
    for k in range(1, K + 1):
        ak = (g[k] - np.dot(phi[1:k], g[1:k][::-1])) / v; a[k] = ak
        new = phi.copy(); new[k] = ak; new[1:k] = phi[1:k] - ak * phi[1:k][::-1]; phi = new; v = v * (1 - ak * ak)
        if v <= 0: return None
    return a[1:]


def rolls(z):
    T = len(z["downbeat"]); out = {}
    for k in range(5):
        shp = z[f"pianoroll_{k}_csc_shape"]
        if shp[0] == 0: out[k] = None; continue
        ind, ptr = z[f"pianoroll_{k}_csc_indices"], z[f"pianoroll_{k}_csc_indptr"]
        M = np.zeros((T, 128), bool)
        for p in range(128):
            a, b = ptr[p], ptr[p + 1]
            if b > a: M[ind[a:b], p] = True
        out[k] = M if M.any() else None
    return T, out


def file_measure(path, md5):
    global RT
    if RT is None: RT = _rough_table()
    try:
        z = np.load(path, allow_pickle=False); T, rs = rolls(z)
    except Exception:
        return None
    mel = np.zeros((T, 128), bool)
    for k in (1, 2, 4):
        if rs[k] is not None: mel |= rs[k]
    if not mel.any(): return None
    e8 = mel[::12]; has = e8.any(1); top = np.where(has, 127 - np.argmax(e8[:, ::-1], 1), -1)
    if has.sum() < 128: return None
    i0 = int(np.argmax(has)); i1 = len(has) - int(np.argmax(has[::-1])); sky = top[i0:i1]
    snd = sky[sky >= 0]
    out = {}
    p = np.bincount(snd % 12, minlength=12).astype(float); pn = p / p.sum(); f = _W @ pn
    C = 12 * float((pn * pn).sum()) - 1.0; e5 = 2 * abs(f[5]) ** 2
    out.update(REP_L=_ent(p), C_L=C, E5_L=e5, REST_L=C - e5, TOP_L=float(pn.max()))
    ev = snd[np.r_[True, snd[1:] != snd[:-1]]]; pc = (ev % 12).astype(np.int64)
    out["NEV"] = int(len(pc)); out["LNEV"] = float(math.log(len(pc)))
    if len(pc) >= 128:
        out["H1"] = _ent(np.bincount(pc, minlength=12))
        rng = np.random.default_rng(int(md5[:8], 16))
        out["PI3c"] = _pi3(pc) - float(np.mean([_pi3(rng.permutation(pc)) for _ in range(NSH)]))
    else:
        out["H1"] = out["PI3c"] = None
    out["EVLEN"] = float(len(snd) / len(ev))
    # repeated-bar share on the absolute eighth grid (bars of 8 eighths), exact pitches and rests
    nb = len(top) // 8; bars = top[:nb * 8].reshape(nb, 8); seen = set(); ne = rep = 0
    for b in bars:
        if (b < 0).all(): continue
        t = b.tobytes(); ne += 1; rep += t in seen; seen.add(t)
    out["REPBAR"] = rep / ne if ne else None
    # Gaussian predictive information (held skyline)
    x = sky.astype(float); x[x < 0] = np.nan
    for i in range(1, len(x)):
        if not np.isfinite(x[i]): x[i] = x[i - 1]
    out["PI8"] = out["H8"] = None
    if len(x) >= 256 and np.std(x) > 0:
        a = _pacf(x, 32)
        if a is not None:
            a = np.clip(a, -0.999999, 0.999999); k = np.arange(1, 33)
            out["PI8"] = float(-0.5 * np.sum(k * np.log(1 - a * a)) - 32 * 33 / (4.0 * len(x)))
            out["H8"] = float(math.log(np.var(x) * np.prod(1 - a * a)))
    # texture
    allm = np.zeros((T, 128), bool)
    for k in (1, 2, 3, 4):
        if rs[k] is not None: allm |= rs[k]
    beats = allm[::24]; nbt = beats.sum(1); act = nbt >= 1
    out["NPB"] = float(nbt[act].mean()) if act.any() else None
    out["ACT"] = int(sum(rs[k] is not None for k in range(5)))
    prof = np.array([mel[:, q::12].sum() for q in range(12)], float); out["PROF"] = (prof / prof.sum()).tolist()
    out["PCE_ALL"] = _ent(prof)
    num = pairs = octp = 0.0; reg = []
    for row in beats[act]:
        ps = np.flatnonzero(row); reg.append(ps.mean())
        if len(ps) < 2: continue
        d = np.abs(ps[:, None] - ps[None, :]); iu = np.triu(np.ones_like(d, bool), 1); keep = (d % 12 != 0) & iu
        num += RT[np.ix_(ps, ps)][keep].sum(); pairs += keep.sum(); octp += ((d % 12 == 0) & iu).sum()
    out["ROUGH_X"] = float(num / pairs) if pairs else None
    out["REG"] = float(np.mean(reg)) if reg else None
    out["OCT"] = float(octp / (octp + pairs)) if (octp + pairs) else None
    return out


def jsd_min(p, q):
    p, q = np.asarray(p), np.asarray(q)
    def H(v): v = v[v > 0]; return float(-(v * np.log2(v)).sum())
    return min(H((p + np.roll(q, k)) / 2) - (H(p) + H(np.roll(q, k))) / 2 for k in range(12))


def _path(tid, md5): return os.path.join(LPD, tid[2], tid[3], tid[4], tid, md5 + ".npz")


def _job(s):
    files = []
    for j, (tid, md5) in enumerate(zip(s["tids"], s["md5s"])):
        m = file_measure(_path(tid, md5), md5)
        if m is not None: m["j"] = j; files.append(m)
    kept, dups = [], 0
    for m in files:
        if any(jsd_min(m["PROF"], k["PROF"]) < 1e-4 for k in kept): dups += 1; continue
        kept.append(m)
    return s["key"], dict(files=kept, n_dup=dups, n_files_valued=len(files))


def main():
    mx = int(sys.argv[1]) if len(sys.argv) > 1 else None
    S = json.load(open(SIDE));
    if mx: S = S[:mx]
    t0 = time.time()
    with Pool(2) as P: res = P.map(_job, S, chunksize=8)
    out = {k: v for k, v in res if v["files"]}
    meta = dict(songs_listed=len(S), songs_with_value=len(out), files_kept=sum(len(v["files"]) for v in out.values()),
                near_duplicates_dropped=sum(v["n_dup"] for v in out.values()), seconds=round(time.time() - t0, 1), keys=KEYS)
    json.dump(dict(meta=meta, songs=out), open(OUT if not mx else OUT + ".test", "w"))
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
