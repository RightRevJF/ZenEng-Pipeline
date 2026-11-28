"""Run 12, the Listener: predictive information of the melody skyline on whole Lakh songs (notes only; no outcome is read).

Usage: python3 lakh_listener_pi.py [max_files]   -> /home/claude/dl/run12/listener_pi_lakh.json, then prints notes-side checks.

Melody: at each eighth note (every 12th step of LPD-5 cleansed, 4/4, 24 steps per beat) the highest sounding pitch over tracks
1 piano, 2 guitar, 4 strings (the skyline, as run 11's s_coupling). Rests dropped; consecutive equal pitches merged -> note events.
Alphabet: pitch class (12 symbols). Block entropies are invariant to relabelling, so no key or tonic is needed.
H(L): plug-in Shannon entropy (bits) of the overlapping L-blocks. PI_L = 2 H(L) - H(2L) = I(past L ; future L) (Bialek,
Nemenman & Tishby 2001, eq. for I_pred at finite window). Bias correction: subtract the mean PI_L of 10 shuffles of the same
events (shuffle = zero predictive information with the same pitch-class counts; seeds from the md5). Corrected values: PIc_L.
E3 = H(3) - 3 (H(3) - H(2)) (finite-L excess entropy), corrected the same way. H1 = event pitch-class entropy (REP's twin here).
Grid reading: the eighth-note skyline with holds (pc or rest = 13 symbols), PIg_L for L = 4, 8 eighths (half bar, bar).
KEFF = PI4c - PI1c = 2 dI_pred/dlog2 L over L = 1..4: the BNT log-growth coefficient, read as an effective parameter count.
A file needs >= 128 note events. Song value = mean over its files; two-file songs give the arrangement stability check.
"""
import os, sys, json, hashlib, time
import numpy as np
from scipy import stats

LPD = "/home/claude/dl/lpd/lpd_5/lpd_5_cleansed"
SIDE = "/home/claude/dl/run12/lakh_notes_side.json"
OUT = "/home/claude/dl/run12/listener_pi_lakh.json"
NSH = 10


def skyline(path):
    z = np.load(path, allow_pickle=False); T = len(z["downbeat"])
    hi = np.full(T, -1, np.int16)
    for k in (1, 2, 4):
        shp = z[f"pianoroll_{k}_csc_shape"]
        if shp[0] == 0: continue
        ind, ptr = z[f"pianoroll_{k}_csc_indices"], z[f"pianoroll_{k}_csc_indptr"]
        for p in range(128):
            a, b = ptr[p], ptr[p + 1]
            if b > a:
                t = ind[a:b]; hi[t] = np.maximum(hi[t], p)
    return hi[::12]


def H(seq, L, base):
    n = len(seq) - L + 1
    if n < 2: return np.nan
    code = np.zeros(n, np.int64)
    for j in range(L): code = code * base + seq[j:j + n]
    _, c = np.unique(code, return_counts=True); p = c / n
    return float(-(p * np.log2(p)).sum())


def pis(seq, base, Ls):
    Hs = {L: H(seq, L, base) for L in set(Ls) | {2 * L for L in Ls} | {1, 2, 3}}
    out = {f"PI{L}": 2 * Hs[L] - Hs[2 * L] for L in Ls}
    out["E3"] = Hs[3] - 3 * (Hs[3] - Hs[2])
    return out


def corrected(seq, base, Ls, seed):
    raw = pis(seq, base, Ls); rng = np.random.default_rng(seed); acc = {k: 0.0 for k in raw}
    for _ in range(NSH):
        s = rng.permutation(seq); r = pis(s, base, Ls)
        for k in r: acc[k] += r[k] / NSH
    return {k + "c": raw[k] - acc[k] for k in raw}, raw


def file_measure(path, md5):
    try:
        g = skyline(path)
    except Exception:
        return None
    seed = int(md5[:8], 16)
    sound = g >= 0
    if sound.sum() < 128: return None
    first, last = np.argmax(sound), len(g) - np.argmax(sound[::-1])
    g = g[first:last]
    ev = g[g >= 0]; ev = ev[np.r_[True, ev[1:] != ev[:-1]]]
    if len(ev) < 128: return None
    pc = (ev % 12).astype(np.int64)
    c, raw = corrected(pc, 12, (1, 2, 3, 4), seed)
    grid = np.where(g >= 0, g % 12, 12).astype(np.int64)
    cg, _ = corrected(grid, 13, (4, 8), seed + 1)
    p = np.bincount(pc, minlength=12) / len(pc); p = p[p > 0]
    out = dict(N=len(pc), lnN=float(np.log(len(pc))), H1=float(-(p * np.log2(p)).sum()), n_pc=int(len(p)),
               PI1=raw["PI1"], PI3=raw["PI3"])
    out.update(c); out.update({"PIg4c": cg["PI4c"], "PIg8c": cg["PI8c"], "KEFF": c["PI4c"] - c["PI1c"]})
    return out


def path_of(tid, md5):
    return os.path.join(LPD, tid[2], tid[3], tid[4], tid, md5 + ".npz")


def main():
    mx = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9
    S = json.load(open(SIDE)); t0 = time.time(); res = {}; nf = 0
    multi = [s for s in S if len(s["md5s"]) > 1]; single = [s for s in S if len(s["md5s"]) == 1]
    for s in multi + single:  # two-file songs first, so a capped run still gives the arrangement check
        if nf >= mx: break
        vals = []
        for tid, md5 in zip(s["tids"], s["md5s"]):
            v = file_measure(path_of(tid, md5), md5); nf += 1
            if v is not None: vals.append(v)
        if vals: res[s["key"]] = dict(artist=s["artist"], files=vals, ch_rep=s.get("ch_rep"))
    json.dump(res, open(OUT, "w"))
    print(f"files {nf}, songs with a value {len(res)}, {time.time() - t0:.0f} s", file=sys.stderr)
    checks(res)


def checks(res):
    K = ["PI1c", "PI2c", "PI3c", "PI4c", "KEFF", "E3c", "PIg4c", "PIg8c"]
    pairs = {k: [] for k in K + ["H1", "lnN"]}
    for r in res.values():
        if len(r["files"]) >= 2:
            for k in pairs: pairs[k].append((r["files"][0][k], r["files"][1][k]))
    print("stability between two MIDI files of one song (Spearman, songs):")
    for k, v in pairs.items():
        v = np.array(v); print(f"  {k:6s} {stats.spearmanr(v[:, 0], v[:, 1]).correlation:+.3f} ({len(v)})")
    rows = []
    for key, r in res.items():
        m = {k: float(np.mean([f[k] for f in r["files"]])) for k in K + ["H1", "lnN", "n_pc"]}
        m["artist"] = r["artist"]; m["ch_rep"] = r["ch_rep"]; rows.append(m)
    A = {}
    for i, m in enumerate(rows): A.setdefault(m["artist"], []).append(i)
    def col(k): return np.array([np.nan if m[k] is None else m[k] for m in rows], float)
    def within(x):
        y = x.copy()
        for ix in A.values(): y[ix] = x[ix] - np.nanmean(x[ix])
        return y
    multi_art = np.array([len(A[m["artist"]]) > 1 for m in rows])
    print(f"songs {len(rows)}; overlaps (Spearman, all songs | within artist, Pearson on demeaned):")
    base = ["H1", "n_pc", "lnN", "ch_rep"]
    for k in K:
        x = col(k); s = " ".join(f"{b} {stats.spearmanr(x, col(b), nan_policy='omit').correlation:+.2f}" for b in base)
        w = " ".join(f"{b} {np.corrcoef(*[within(v)[multi_art & np.isfinite(col(b))] for v in (x, col(b))])[0, 1]:+.2f}" for b in base)
        X = np.column_stack([np.ones(len(rows)), col("H1"), col("lnN")]); ok = np.isfinite(x)
        beta = np.linalg.lstsq(X[ok], x[ok], rcond=None)[0]; r2 = 1 - np.var(x[ok] - X[ok] @ beta) / np.var(x[ok])
        print(f"  {k:6s} | {s} | within: {w} | R2 on H1+lnN {r2:.2f}")
    # does PI subsume REP? share of H1's within-artist variance carried by PI3c (and the reverse)
    for k in ("PI3c", "PI4c", "KEFF", "E3c", "PIg8c"):
        x, h = within(col(k))[multi_art], within(col("H1"))[multi_art]
        print(f"  within-artist r({k}, H1) = {np.corrcoef(x, h)[0, 1]:+.3f}")


if __name__ == "__main__":
    main()
