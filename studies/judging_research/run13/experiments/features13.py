"""Run 13 (supplemental trial of the new system, 28 Nov 2026): one notes-only feature grammar used by every test.
A melody section = notes (onset in beats, duration in beats, MIDI pitch), a tonic pitch class, 4 beats a bar.
The window is the first 8 bars from the bar of the first note (so clips and engine sections are compared at the same length).
base(notes, tonic_pc) -> dict of ~60 named features (no fitted settings). No outcome is read here.
Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); the Luthier engine (this repository)."""
import math, zlib, collections
import numpy as np

BPB = 4; BARS = 8; GRID = 4   # 16th-note grid

def _H(counts):
    c = np.array([v for v in counts if v > 0], float)
    if c.sum() <= 0: return 0.0
    p = c / c.sum(); return float(-(p * np.log2(p)).sum())

def _rep_share(seq, n):
    if len(seq) < n + 1: return np.nan
    seen = set(); rep = 0; tot = 0
    for i in range(len(seq) - n + 1):
        g = tuple(seq[i:i + n]); tot += 1
        if g in seen: rep += 1
        seen.add(g)
    return rep / tot

def _lz(s):
    """Lempel-Ziv (1976) phrase count of a token sequence, normalised by n / log2 n."""
    n = len(s)
    if n < 4: return np.nan
    i, c = 0, 0; d = set()
    w = ()
    for t in s:
        w = w + (t,)
        if w not in d: d.add(w); c += 1; w = ()
    if w: c += 1
    return c / (n / math.log2(n))

def window(notes):
    """notes: list of (on, dur, pitch) in beats. Keep the 8 bars from the first note's bar; re-zero to that bar."""
    notes = sorted([n for n in notes if n[1] > 0], key=lambda x: (x[0], x[2]))
    if not notes: return []
    b0 = math.floor(notes[0][0] / BPB) * BPB
    return [(on - b0, du, p) for on, du, p in notes if on - b0 < BPB * BARS]

def base(notes, tonic_pc):
    w = window(notes)
    if len(w) < 12: return None
    on = np.array([x[0] for x in w]); du = np.array([x[1] for x in w]); p = np.array([x[2] for x in w], int)
    deg = (p - tonic_pc) % 12; iv = np.diff(p); aiv = np.abs(iv); ioi = np.diff(on)
    span = BPB * BARS; f = {}
    f["density"] = len(w) / span
    pcd = np.zeros(12)
    for d_, u_ in zip(deg, du): pcd[d_] += u_
    q = pcd / pcd.sum()
    f["pc_entropy"] = _H(pcd); f["top_pc_share"] = float(q.max()); f["tonic_share"] = float(q[0]); f["fifth_share"] = float(q[7])
    f["triad_share"] = float(q[0] + q[7] + max(q[3], q[4])); f["n_pc"] = int((pcd > 0).sum())
    F = np.fft.fft(q)
    for k in range(1, 7): f[f"dft{k}"] = float(abs(F[k]))
    f["range"] = int(p.max() - p.min()); f["pitch_sd"] = float(p.std())
    f["int_entropy"] = _H(collections.Counter(np.clip(iv, -12, 12).tolist()).values())
    f["step_share"] = float(np.mean((aiv >= 1) & (aiv <= 2))); f["leap_share"] = float(np.mean(aiv > 4)); f["unison_share"] = float(np.mean(aiv == 0))
    f["mean_abs_int"] = float(aiv.mean()); f["third_share"] = float(np.mean((aiv == 3) | (aiv == 4)))
    sg = np.sign(iv[iv != 0]); f["turn_share"] = float(np.mean(sg[1:] != sg[:-1])) if len(sg) > 2 else np.nan
    up = iv[iv > 0]; dn = iv[iv < 0]; f["up_minus_down_size"] = float((up.mean() if len(up) else 0) - (-dn.mean() if len(dn) else 0))
    lr = [i for i in range(len(iv) - 1) if aiv[i] > 4]
    f["leap_recovery"] = float(np.mean([np.sign(iv[i + 1]) == -np.sign(iv[i]) and 1 <= aiv[i + 1] <= 2 for i in lr])) if lr else np.nan
    dq = np.round(du * 12).astype(int); f["dur_entropy"] = _H(collections.Counter(dq.tolist()).values()); f["n_dur"] = len(set(dq.tolist()))
    f["dur_cv"] = float(du.std() / du.mean()); f["ioi_cv"] = float(ioi.std() / ioi.mean()) if len(ioi) and ioi.mean() > 0 else np.nan
    pos = np.round((on % BPB) * GRID).astype(int) % (BPB * GRID)
    f["pos_entropy"] = _H(collections.Counter(pos.tolist()).values())
    f["on_beat"] = float(np.mean(pos % GRID == 0)); f["downbeat"] = float(np.mean(pos == 0)); f["offbeat16"] = float(np.mean(pos % 2 == 1))
    f["on_and"] = float(np.mean(pos % GRID == 2))
    sounding = float(np.minimum(du, np.concatenate([ioi, [du[-1]]])).sum()); f["rest_share"] = 1 - sounding / (on[-1] + du[-1] - on[0])
    long_ = du >= np.quantile(du, 0.75); f["long_on_beat"] = float(np.mean(pos[long_] % GRID == 0)); f["long_on_triad"] = float(np.mean(np.isin(deg[long_], [0, 3, 4, 7])))
    f["ends_tonic"] = float(deg[-1] == 0); f["ends_triad"] = float(deg[-1] in (0, 3, 4, 7))
    t = (on - on[0]) / max(on[-1] - on[0], 1e-9); f["peak_time"] = float(t[int(np.argmax(p))])
    th = np.digitize(t, [1 / 3, 2 / 3]); mids = p[th == 1]; outs = p[th != 1]
    f["arch"] = float(mids.mean() - outs.mean()) if len(mids) and len(outs) else np.nan
    bars = collections.defaultdict(list)
    for o_, p_ in zip(on, p): bars[int(o_ // BPB)].append((round(float(o_ % BPB) * 12), int(p_)))
    bl = [bars[k] for k in sorted(bars)]
    rh = [tuple(x[0] for x in b) for b in bl]; ivb = [tuple(np.diff([x[1] for x in b]).tolist()) for b in bl]; full = [tuple(b) for b in bl]
    def bar_rep(L): return float(np.mean([L[i] in L[:i] for i in range(1, len(L))])) if len(L) > 1 else np.nan
    f["bar_rhythm_rep"] = bar_rep(rh); f["bar_interval_rep"] = bar_rep(ivb); f["bar_exact_rep"] = bar_rep(full)
    f["rhythm_minus_pitch_rep"] = f["bar_rhythm_rep"] - f["bar_interval_rep"] if np.isfinite(f["bar_rhythm_rep"]) else np.nan
    f["n_bar_rhythms"] = len(set(rh)) / max(len(rh), 1)
    iq = np.round(ioi * 12).astype(int).tolist()
    for n in (2, 3, 4):
        f[f"pitch_rep{n}"] = _rep_share(iv.tolist(), n); f[f"rhythm_rep{n}"] = _rep_share(iq, n)
        f[f"joint_rep{n}"] = _rep_share(list(zip(iv.tolist(), iq)), n)
    tok = [f"{a}:{b}" for a, b in zip(deg.tolist(), dq.tolist())]
    s = " ".join(tok).encode(); f["zlib_ratio"] = len(zlib.compress(s, 9)) / len(s); f["lz_complexity"] = _lz(tok)
    grid = np.full(span * GRID, np.nan)
    for o_, d_, p_ in w:
        a = int(round(o_ * GRID)); b = int(round((o_ + d_) * GRID)); grid[a:max(b, a + 1)] = p_
    g = grid.copy(); last = np.nan
    for i in range(len(g)):
        if np.isfinite(g[i]): last = g[i]
        else: g[i] = last
    g = g[np.isfinite(g)]
    def ac(lag):
        if len(g) <= lag + 8: return np.nan
        a, b = g[:-lag] - g.mean(), g[lag:] - g.mean(); den = math.sqrt((a * a).sum() * (b * b).sum())
        return float((a * b).sum() / den) if den > 0 else np.nan
    f["ac_1bar"] = ac(BPB * GRID); f["ac_2bar"] = ac(2 * BPB * GRID); f["ac_beat"] = ac(GRID)
    gaps = np.concatenate([[0], ioi - du[:-1]]); bnd = np.where(gaps >= 1.0)[0]
    edges = [0] + bnd.tolist() + [len(w)]; ph = [p[a:b] for a, b in zip(edges, edges[1:]) if b > a]
    f["n_phrases"] = len(ph); f["phrase_notes"] = float(np.mean([len(x) for x in ph])); f["phrase_range"] = float(np.mean([x.max() - x.min() for x in ph]))
    f["phrase_range_over_range"] = f["phrase_range"] / max(f["range"], 1)
    return {k: (float(v) if v is not None and np.isfinite(v) else np.nan) for k, v in f.items()}

def from_hooktheory(a):
    """raw Hooktheory annotation -> (notes, tonic_pc) for 4/4 clips, else None."""
    ms = a.get("meters") or [{"beats_per_bar": 4}]
    if (ms[0].get("beats_per_bar") or 4) != 4: return None
    ks = a.get("keys") or []
    if not ks: return None
    tp = ks[0].get("tonic_pitch_class")
    if tp is None: return None
    ns = [(float(n["onset"]), float(n["offset"] - n["onset"]), 12 * (n.get("octave", 0) + 5) + n["pitch_class"]) for n in (a.get("melody") or [])
          if n.get("pitch_class") is not None and n["offset"] > n["onset"]]
    return ns, int(tp) % 12

def from_engine_build(build, beat=12):
    """engine survivor notes [[on, p, dur, sec, line, stress], ...] -> {section name: (notes, tonic_pc)}.
    The metre engine writes in C (spec scale relative to pitch class 0; the record transposes afterwards), so the tonic is 0."""
    secs = collections.OrderedDict()
    for on, p, dur, sec, line, st in build:
        secs.setdefault(sec, []).append((on / beat, (dur or 0) / beat, int(p)))
    return {s: (v, 0) for s, v in secs.items()}
