"""THE PAGE GATE, strengthened.  One reader of which session tunes are kept, from the written notes alone.

What it is: (1) the note-to-note SURPRISE of the tune under a long-context (five-note), back-off-smoothed model of the tradition, kept separately for
pitch (interval, and scale degree) and rhythm, both for all tunes and for the tune's own type, with where the surprise falls (opening quarter, last quarter,
worst tenth); (2) plain page measures in families: scale use (pentatonic / six-note share, each degree's share), interval sizes, rhythm, repeated figures and
bars, how the strains relate, phrase length, contour, register; (3) two readers over them, a ridge and small boosted trees, averaged.
Everything is fitted here at import on the OPEN half only; the target is the kept-yardstick with tune type, mode, length and submission order taken out,
so the reader cannot earn its score from those.  Functions never read Gs, tunebooks, recordings or n_settings of the tunes they score."""
import sys, os, zlib, collections, re, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
sys.path.insert(0, "/home/claude/arena2"); sys.path.insert(0, "/home/claude/zeneng/corpus/v39")
import arena2, sabc
from scipy.stats import rankdata
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from threadpoolctl import threadpool_limits
BARLEN = {"4/4": 4, "6/8": 3, "3/4": 3, "2/4": 2, "9/8": 4.5, "12/8": 6, "3/2": 6}
DIA = dict(maj=(0, 2, 4, 5, 7, 9, 11), mix=(0, 2, 4, 5, 7, 9, 10), dor=(0, 2, 3, 5, 7, 9, 10), min=(0, 2, 3, 5, 7, 8, 10))
PEN = dict(maj=(0, 2, 4, 7, 9), mix=(0, 2, 4, 7, 9), dor=(0, 2, 5, 7, 10), min=(0, 3, 5, 7, 10))


def ent(v):
    c = np.array(list(collections.Counter(v).values()), float); p = c / c.sum(); return float(-(p * np.log2(p)).sum())


def boundaries(abc):
    """bar indices (in sabc.parse numbering) at which a new strain starts (after ||, :|, |:, ::)."""
    nb = 0; cur = False; out = set(); mark = False
    for m in sabc.TOK.finditer(abc.replace("\r", "")):
        s = m.group(0)
        if s[0] == "|" or s in (":|", "|:", "::") or s.startswith("[1") or s.startswith("[2"):
            if "|" in s or ":" in s:
                if cur: nb += 1; cur = False
                if ":" in s or "||" in s: mark = True
            continue
        isnote = False
        if m.group(1) is not None:
            isnote = bool(re.match(r"(\^\^|\^|__|_|=)?([A-Ga-gz])", m.group(1)))
        elif m.group(3): isnote = True
        if isnote:
            if mark and not cur and nb > 0: out.add(nb)
            mark = False; cur = True
    return sorted(out)


def seqs(t):
    """token sequences for the n-gram models."""
    ton = t["tonic_pc"]; P = []; D = []; POS = []
    for b in t["bars"]:
        pos = 0.0
        for p, d in b:
            if p is not None: P.append(p); D.append(min(round(d * 4) / 4, 4.0)); POS.append(round(pos * 4) / 4)
            pos += d
    P = np.array(P, int); iv = np.clip(np.diff(P), -12, 12)
    deg = np.clip(P - (60 + ton), -13, 30) if ton <= 6 else np.clip(P - (48 + ton), -13, 30)
    return dict(iv=[int(x) for x in iv], deg=[int(x) for x in deg], dur=[(d, p) for d, p in zip(D, POS)], dr=D,
                joint=[(int(i), d) for i, d in zip(iv, D[1:])])


def tune_feats(t):
    bars = t["bars"]; md = t["mode_family"] if t["mode_family"] in DIA else {"ion": "maj", "lyd": "maj", "aeo": "min", "phr": "min", "loc": "min"}.get(t["mode_family"], "maj"); ton = t["tonic_pc"]; bl = BARLEN.get(t["meter"], 4)
    notes = [(p, d) for b in bars for p, d in b if p is not None]
    p = np.array([n[0] for n in notes], float); d = np.array([n[1] for n in notes]); n = len(p); nb = len(bars)
    iv = np.diff(p); a = np.abs(iv); sg = np.sign(iv[iv != 0]); pc = (p.astype(int) - ton) % 12
    f = {}
    # ---- baseline twenty (b_)
    bs = ["".join(f"{int(q) if q is not None else 'z'}:{dd}," for q, dd in b) for b in bars]; seen = set(); rep = 0
    for s in bs: rep += s in seen; seen.add(s)
    raw = "|".join(bs).encode(); half = n // 2
    f.update(b_range=p.max() - p.min(), b_step=a.mean(), b_leaps=(a > 4).mean(), b_stepwise=((a > 0) & (a <= 2)).mean(), b_same=(a == 0).mean(),
             b_turns=float((sg[1:] != sg[:-1]).mean()) if len(sg) > 2 else np.nan, b_pitch_ent=ent(p), b_iv_ent=ent(iv), b_rhythm_ent=ent(d), b_long=(d >= 1).mean(),
             b_per_bar=n / nb, b_top_pos=float(np.argmax(p)) / n, b_tonic=(pc == 0).mean(), b_fifth=(pc == 7).mean(), b_ends_tonic=float(pc[-1] == 0),
             b_bars_repeated=rep / nb, b_compress=len(zlib.compress(raw)) / len(raw), b_part_lift=p[half:].mean() - p[:half].mean(),
             b_penta=np.isin(pc, PEN[md]).mean(), b_thirds=((a == 3) | (a == 4)).mean())
    # ---- intervals / attractors (i_)
    f.update(i_gt5=(a > 7).mean(), i_le5=(a <= 7).mean(), i_ndist=len(set(iv)), i_ndist_abs=len(set(a)), i_45=((a == 5) | (a == 7)).mean(), i_oct=(a == 12).mean(),
             i_p90=np.percentile(a, 90), i_up=(iv > 0).mean(), i_maxrun=0.0, i_tri=(a == 6).mean(), i_semi=(a == 1).mean(), i_whole=(a == 2).mean())
    # leap then return
    lp = np.where(a[:-1] > 4)[0]; f["i_leap_back"] = float(np.mean(np.sign(iv[lp + 1]) == -np.sign(iv[lp]))) if len(lp) else np.nan
    # scale runs: share of notes in runs of >=3 same-direction steps
    st = (a > 0) & (a <= 2); run = 0; inrun = 0
    for k in range(len(iv)):
        if st[k] and k > 0 and st[k - 1] and np.sign(iv[k]) == np.sign(iv[k - 1]): run += 1
        else: run = 0
        inrun += run >= 1
    f["i_scalerun"] = inrun / max(len(iv), 1)
    # arpeggio share: two successive thirds/fourths same direction
    th = (a >= 3) & (a <= 5); f["i_arp"] = float(np.mean(th[1:] & th[:-1] & (np.sign(iv[1:]) == np.sign(iv[:-1])))) if len(iv) > 1 else 0
    # ---- scale use (s_)
    h = np.bincount(pc, d, 12); h = h / h.sum()
    for k in range(12): f[f"s_deg{k}"] = h[k]
    dia = DIA[md]; f["s_off"] = 1 - h[list(dia)].sum(); f["s_npc"] = int((h > 0.02).sum()); f["s_pc_ent"] = float(-(h[h > 0] * np.log2(h[h > 0])).sum())
    f["s_deg4"] = h[dia[3]]; f["s_deg7"] = h[dia[6]]; f["s_deg3"] = h[dia[2]]; f["s_deg6"] = h[dia[5]]; f["s_deg2"] = h[dia[1]]; f["s_penta_dw"] = h[list(PEN[md])].sum()
    f["s_triad"] = h[0] + h[dia[2]] + h[7]; f["s_gap"] = float(min(h[dia[3]], h[dia[6]]))
    f["s_hexa"] = 1 - min(h[dia[k]] for k in range(7)) - f["s_off"]  # best six-note share
    # count-based penta of alternate pentatonics (best rotation)
    f["s_penta_best"] = max(np.roll(np.array([1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0.]), k) @ h for k in range(12))
    # tonic on bar starts, strong notes
    firsts = [b[0][0] for b in bars if b and b[0][0] is not None]; fpc = (np.array(firsts) - ton) % 12
    f["s_barstart_tonic"] = float((fpc == 0).mean()); f["s_barstart_triad"] = float(np.isin(fpc, (0, dia[2], 7)).mean()); f["s_barstart_penta"] = float(np.isin(fpc, PEN[md]).mean())
    f["s_first_tonic"] = float(pc[0] == 0); f["s_first_fifth"] = float(pc[0] == 7); f["s_last_fifth"] = float(pc[-1] == 7); f["s_last_second"] = float(pc[-1] == 2)
    f["s_last_triad"] = float(pc[-1] in (0, dia[2], 7)); f["s_longnote_tonic"] = float((pc[d >= np.percentile(d, 90)] == 0).mean())
    f["s_lead_back"] = abs(p[-1] - p[0]); f["s_lead_back_step"] = float(0 < abs(p[-1] - p[0]) <= 2); f["s_last_long"] = d[-1] / np.median(d)
    f["s_last_is_low"] = float(p[-1] == p.min()); f["s_last_rel"] = (p[-1] - p.min()) / max(p.max() - p.min(), 1)
    # ---- register / instrument (r_)
    f.update(r_low=p.min(), r_high=p.max(), r_mean=float(np.average(p, weights=d)), r_below_d=(p < 62).mean(), r_above_b=(p > 83).mean(), r_std=p.std(),
             r_gt_octave=float(p.max() - p.min() > 12), r_tonic_pc=ton, r_tess=np.percentile(p, 90) - np.percentile(p, 10))
    ap = p.astype(int) % 12; f["r_inD"] = float(np.isin(ap, (2, 4, 6, 7, 9, 11, 1)).mean()); f["r_inG"] = float(np.isin(ap, (7, 9, 11, 0, 2, 4, 6)).mean())
    f["r_whistle"] = float((np.isin(ap, (2, 4, 6, 7, 9, 11, 1, 0)) & (p >= 62) & (p <= 83)).mean())
    # ---- rhythm (h_)
    dq = np.round(d * 8) / 8; cnt = collections.Counter(dq); f["h_modal"] = cnt.most_common(1)[0][1] / n; f["h_ndur"] = len(cnt); modal = cnt.most_common(1)[0][0]
    f["h_modal_dur"] = modal; f["h_npvi"] = float(np.mean(np.abs(d[1:] - d[:-1]) / ((d[1:] + d[:-1]) / 2))) * 100; f["h_short"] = (d < modal).mean(); f["h_longer"] = (d > modal).mean()
    f["h_verylong"] = (d >= 3 * modal).mean(); f["h_rest"] = sum(1 for b in bars for q, _ in b if q is None) / (n + 1)
    bl_tot = np.array([sum(dd for _, dd in b) for b in bars]); f["h_pickup"] = float(bl_tot[0] < bl - 0.01)
    rp = [tuple(round(dd * 8) for _, dd in b) for b in bars]; rc = collections.Counter(rp); f["h_bar_modal"] = rc.most_common(1)[0][1] / nb; f["h_bar_ndist"] = len(rc) / nb; f["h_bar_ent"] = ent(rp)
    f["h_bar_ndist_abs"] = len(rc)
    # syncopation: notes that start off the beat and last across the next beat (beat = 1 quarter for simple, 1.5 for compound)
    beat = 1.5 if t["meter"] in ("6/8", "9/8", "12/8") else 1.0; syn = 0; onb = 0
    for b in bars:
        pos = 0.0
        for q, dd in b:
            if q is not None:
                r = pos % beat
                if r > 1e-6 and r + dd > beat + 1e-6: syn += 1
                if r < 1e-6: onb += 1
            pos += dd
    f["h_sync"] = syn / n; f["h_onbeat"] = onb / n
    f["h_dotted"] = float(np.mean(np.isclose(d[:-1] / d[1:], 3) | np.isclose(d[1:] / d[:-1], 3))) if n > 1 else 0
    f["h_dur_cv"] = d.std() / d.mean(); f["h_density"] = n / max(bl_tot.sum(), 1)
    # ---- repetition (p_)
    pb = [tuple(q for q, _ in b) for b in bars]; ib = [tuple(np.diff([q for q, _ in b if q is not None]).astype(int)) for b in bars]
    def repshare(L):
        s = set(); r = 0
        for x in L: r += x in s; s.add(x)
        return r / len(L)
    f["p_bar_pitch"] = repshare(pb); f["p_bar_iv"] = repshare(ib); f["p_bar_ndist"] = len(set(bs)); f["p_bar_distshare"] = len(set(bs)) / nb
    hb = []
    for b in bars:
        pos = 0.0; h1 = []; h2 = []
        for q, dd in b:
            (h1 if pos < bl / 2 - 1e-6 else h2).append((q, dd)); pos += dd
        hb += [tuple(h1), tuple(h2)]
    f["p_halfbar"] = repshare(hb)
    for lag in (1, 2, 4, 8):
        f[f"p_lag{lag}"] = float(np.mean([bs[k] == bs[k - lag] for k in range(lag, nb)])) if nb > lag else np.nan
    # near repeats: bar shares >=75% of onset-aligned pitches with an earlier bar
    def grid(b):
        g = {}; pos = 0.0
        for q, dd in b:
            g[round(pos * 4)] = q; pos += dd
        return g
    G = [grid(b) for b in bars]; near = 0; best = []
    for k in range(1, nb):
        bb = 0.0
        for j in range(max(0, k - 16), k):
            keys = set(G[k]) | set(G[j]); m = sum(1 for x in keys if G[k].get(x, -1) == G[j].get(x, -2)) / len(keys)
            if m > bb: bb = m
        best.append(bb); near += bb >= 0.74
    f["p_near"] = near / nb; f["p_bestsim"] = float(np.mean(best)) if best else np.nan
    # n-gram coverage (interval+duration tokens)
    tk = [(int(np.clip(iv[i], -12, 12)), float(dq[i + 1])) for i in range(len(iv))]; ivl = [int(x) for x in iv]
    for nn in (3, 5, 8):
        for nm, S in (("jt", tk), ("iv", ivl)):
            g = [tuple(S[i:i + nn]) for i in range(len(S) - nn + 1)]; c = collections.Counter(g); cov = np.zeros(len(S), bool)
            for i, x in enumerate(g):
                if c[x] > 1: cov[i:i + nn] = True
            f[f"p_cov{nn}{nm}"] = float(cov.mean()) if len(S) else np.nan
    g4 = [tuple(tk[i:i + 4]) for i in range(len(tk) - 3)]; f["p_figrep"] = 1 - len(set(g4)) / max(len(g4), 1)
    # predicted by its own past: context of 3 tokens seen before, most recent continuation the same
    last = {}; hit = 0; seenctx = 0
    for i in range(3, len(tk)):
        c = tuple(tk[i - 3:i])
        if c in last: seenctx += 1; hit += last[c] == tk[i]
        last[c] = tk[i]
    f["p_selfpred"] = hit / max(len(tk) - 3, 1); f["p_selfctx"] = seenctx / max(len(tk) - 3, 1)
    f["p_compress_pitch"] = len(zlib.compress(bytes(int(x) % 256 for x in p))) / n; f["p_compress_iv"] = len(zlib.compress(bytes(int(x) % 256 for x in iv))) / n
    f["p_compress_dur"] = len(zlib.compress(bytes(int(x * 8) % 256 for x in dq))) / n
    # ---- structure (t_)
    B = boundaries(t["abc"]); B = [x for x in B if 0 < x < nb]; starts = [0] + B; ends = B + [nb]; parts = [(s, e) for s, e in zip(starts, ends) if e - s >= 3]
    f["t_nparts"] = len(parts); f["t_nbars"] = nb; f["t_partlen"] = float(np.mean([e - s for s, e in parts])) if parts else nb
    f["t_std8"] = float(all((e - s) in (8, 9, 10, 16, 17, 18) for s, e in parts)) if parts else 0.0
    if len(parts) >= 2:
        (s0, e0), (s1, e1) = parts[0], parts[1]; A = set(bs[s0:e0]); f["t_BinA"] = float(np.mean([x in A for x in bs[s1:e1]]))
        f["t_end_shared"] = float(bs[e0 - 1] == bs[e1 - 1]) + float(bs[e0 - 2] == bs[e1 - 2]); f["t_end_shared_any"] = float(np.mean([bs[e - 1] == bs[e0 - 1] for s, e in parts[1:]]))
        pa = [q for b in bars[s0:e0] for q, _ in b if q is not None]; pbb = [q for b in bars[s1:e1] for q, _ in b if q is not None]
        f["t_lift"] = np.mean(pbb) - np.mean(pa); f["t_Bhigh"] = max(pbb) - max(pa); f["t_Arange"] = max(pa) - min(pa); f["t_Brange"] = max(pbb) - min(pbb)
        f["t_A_n"] = len(pa); f["t_AB_first"] = float(bs[s0] == bs[s1])
        # tail similarity: share of the last 4 bars of B that equal the bars at same position in A
        f["t_tail4"] = float(np.mean([bs[e1 - k] == bs[e0 - k] for k in range(1, 5)])) if min(e0 - s0, e1 - s1) >= 4 else np.nan
        # within-part repetition
        f["t_A_rep"] = repshare(bs[s0:e0]); f["t_B_rep"] = repshare(bs[s1:e1])
        f["t_A_15"] = float(np.mean([bs[s0 + k] == bs[s0 + k + 4] for k in range(0, min(4, e0 - s0 - 4))])) if e0 - s0 >= 6 else np.nan
        f["t_B_15"] = float(np.mean([bs[s1 + k] == bs[s1 + k + 4] for k in range(0, min(4, e1 - s1 - 4))])) if e1 - s1 >= 6 else np.nan
    else:
        for k in ("t_BinA", "t_end_shared", "t_end_shared_any", "t_lift", "t_Bhigh", "t_Arange", "t_Brange", "t_A_n", "t_AB_first", "t_tail4", "t_A_rep", "t_B_rep", "t_A_15", "t_B_15"): f[k] = np.nan
    # strain-end degrees
    pe = [[q for q, _ in bars[e - 1] if q is not None] for s, e in parts]; pe = [(x[-1] - ton) % 12 for x in pe if x]
    f["t_partend_tonic"] = float(np.mean([x == 0 for x in pe])) if pe else np.nan
    # phrase length: notes between long notes (>= 2x modal) or rests
    ph = []; cur = 0
    for b in bars:
        for q, dd in b:
            if q is None:
                if cur: ph.append(cur); cur = 0
                continue
            cur += 1
            if dd >= 2 * modal - 1e-6: ph.append(cur); cur = 0
    if cur: ph.append(cur)
    f["t_phr_len"] = float(np.mean(ph)); f["t_phr_med"] = float(np.median(ph)); f["t_phr_max"] = float(max(ph)); f["t_phr_n"] = len(ph) / nb
    # ---- contour (c_)
    barmean = np.array([np.mean([q for q, _ in b if q is not None]) if any(q is not None for q, _ in b) else np.nan for b in bars])
    arch = []; desc = []; peakmid = []
    for s, e in parts:
        for k in range(s, e - 3, 4):
            seg = [q for b in bars[k:k + 4] for q, _ in b if q is not None]
            if len(seg) >= 6:
                x = np.linspace(-1, 1, len(seg)); c2, c1, c0 = np.polyfit(x, seg, 2); arch.append(-c2); desc.append(-c1); pk = np.argmax(seg) / len(seg); peakmid.append(0.25 < pk < 0.75)
    f["c_arch"] = float(np.mean(arch)) if arch else np.nan; f["c_desc"] = float(np.mean(desc)) if desc else np.nan; f["c_peakmid"] = float(np.mean(peakmid)) if peakmid else np.nan
    x = np.linspace(-1, 1, n); c2, c1, c0 = np.polyfit(x, p, 2); f["c_arch_all"] = -c2; f["c_desc_all"] = -c1
    # bar-level arch: within a bar, first note vs. mean
    f["c_barfirst_high"] = float(np.mean([b[0][0] >= np.mean([q for q, _ in b if q is not None]) for b in bars if b[0][0] is not None]))
    f["c_barmean_sd"] = float(np.nanstd(barmean)); f["c_barmean_step"] = float(np.nanmean(np.abs(np.diff(barmean)))) if nb > 1 else np.nan
    f["c_first_note_rel"] = (p[0] - p.min()) / max(p.max() - p.min(), 1); f["c_start_end"] = p[-1] - p[0]
    f["n"] = n
    return f


class VLM:
    def __init__(self, order=5): self.K = order
    def _codes(self, seqs, groups, fit):
        if fit:
            vocab = {}
            for s in seqs:
                for x in s:
                    if x not in vocab: vocab[x] = len(vocab)
            self.vocab = vocab; self.B = len(vocab) + 2; self.gv = {g: i for i, g in enumerate(sorted(set(groups)))} if groups is not None else None
        unk = self.B - 1; code = np.array([self.vocab.get(x, unk) for s in seqs for x in s], np.int64); L = np.array([len(s) for s in seqs]); tune = np.repeat(np.arange(len(seqs)), L)
        start = np.repeat(np.cumsum(L) - L, L); pos = np.arange(len(code)) - start
        off = np.repeat(np.array([self.gv.get(g, len(self.gv)) for g in groups], np.int64), L) * self.B ** self.K if groups is not None else 0
        return code, tune, pos, off, L
    def _keys(self, code, pos, off):
        out = []; g = code.copy()
        for k in range(1, self.K + 1):
            if k > 1:
                sh = np.zeros_like(code); sh[k - 1:] = code[:-(k - 1)]; g = g + sh * self.B ** (k - 1)
            out.append((g + off, pos >= k - 1))
        return out
    def fit_score(self, seqs, groups=None):
        """fit on seqs; return leave-one-out information content, array (K, total tokens), and lengths."""
        code, tune, pos, off, L = self._codes(seqs, groups, True); self.tab = []; n = len(code); p = np.full(n, 1.0 / self.B); out = []
        for g, valid in self._keys(code, pos, off):
            gv = g[valid]; tv = tune[valid]; ug, cg = np.unique(gv, return_counts=True); uh, inv = np.unique(ug // self.B, return_inverse=True); ch = np.bincount(inv, cg).astype(np.int64); th = np.bincount(inv).astype(np.int64); self.tab.append((ug, cg, uh, ch, th))
            o = np.lexsort((gv, tv)); gs = gv[o]; ts = tv[o]; hs = gs // self.B; newg = np.r_[True, (gs[1:] != gs[:-1]) | (ts[1:] != ts[:-1])]; rid = np.cumsum(newg) - 1; own = np.bincount(rid)[rid]
            c = cg[np.searchsorted(ug, gs)]; newh = np.r_[True, (hs[1:] != hs[:-1]) | (ts[1:] != ts[:-1])]; hid = np.cumsum(newh) - 1; dC = np.bincount(hid)[hid]; dT = np.bincount(hid[newg], (own == c)[newg].astype(float))[hid]
            hi = np.searchsorted(uh, hs); c1 = c - own; ch1 = ch[hi] - dC; th1 = th[hi] - dT; pv = p[valid]; ps = pv[o]; new = np.where(ch1 > 0, (c1 + th1 * ps) / np.maximum(ch1 + th1, 1e-9), ps); pv2 = np.empty_like(pv); pv2[o] = new; p = p.copy(); p[valid] = pv2; out.append(-np.log2(np.maximum(p, 1e-12)))
        return np.array(out), L
    def score(self, seqs, groups=None):
        code, tune, pos, off, L = self._codes(seqs, groups, False); p = np.full(len(code), 1.0 / self.B); out = []
        for (g, valid), (ug, cg, uh, ch, th) in zip(self._keys(code, pos, off), self.tab):
            gv = g[valid]; i = np.minimum(np.searchsorted(ug, gv), len(ug) - 1); c = np.where(ug[i] == gv, cg[i], 0); hv = gv // self.B; j = np.minimum(np.searchsorted(uh, hv), len(uh) - 1); ok = uh[j] == hv; c_h = np.where(ok, ch[j], 0); t_h = np.where(ok, th[j], 0)
            pv = p[valid]; p = p.copy(); p[valid] = np.where(c_h > 0, (c + t_h * pv) / np.maximum(c_h + t_h, 1e-9), pv); out.append(-np.log2(np.maximum(p, 1e-12)))
        return np.array(out), L


LM_KEYS = ("iv", "deg", "dur", "dr", "joint")


def _ic_feats(tunes, lms=None):
    """surprise features. lms=None: fit the models on these tunes and score each tune with its own counts removed (leave-one-out)."""
    SQ = [seqs(t) for t in tunes]; types = [t["type"] for t in tunes]; fit = lms is None; lms = {} if fit else lms; cols = {}
    for key in LM_KEYS:
        S_ = [q[key] for q in SQ]
        if fit: lms[key] = (VLM(5), VLM(5)); A, L = lms[key][0].fit_score(S_); Bt, _ = lms[key][1].fit_score(S_, types)
        else: A, L = lms[key][0].score(S_); Bt, _ = lms[key][1].score(S_, types)
        st = np.cumsum(L) - L; n = len(tunes); o = {k: np.full(n, np.nan) for k in ("", "_p90", "_sd", "_first", "_last", "_max", "_hi", "t", "t_p90", "t_first", "t_sd", "2", "3")}
        for j in range(n):
            if L[j] == 0: continue
            a = A[4, st[j]:st[j] + L[j]]; b = Bt[4, st[j]:st[j] + L[j]]; k4 = max(L[j] // 4, 1)
            o[""][j] = a.mean(); o["_p90"][j] = np.percentile(a, 90); o["_sd"][j] = a.std(); o["_first"][j] = a[:k4].mean(); o["_last"][j] = a[-k4:].mean(); o["_max"][j] = a.max(); o["_hi"][j] = (a > 6).mean()
            o["t"][j] = b.mean(); o["t_p90"][j] = np.percentile(b, 90); o["t_first"][j] = b[:k4].mean(); o["t_sd"][j] = b.std(); o["2"][j] = A[1, st[j]:st[j] + L[j]].mean(); o["3"][j] = A[2, st[j]:st[j] + L[j]].mean()
        for k, v in o.items():
            nm = f"ict_{key}{k[1:]}" if k.startswith("t") else f"ic{k}_{key}" if k in ("2", "3") else f"ic_{key}{k}"
            if k in ("2", "3") and key in ("dur", "dr"): continue
            cols[nm] = v
    return pd.DataFrame(cols), lms


def _safe(t):
    try: return tune_feats(t)
    except Exception: return {}


def _features(tunes, lms=None):
    F = pd.DataFrame([_safe(t) for t in tunes]).drop(columns=["n"], errors="ignore"); I, lms = _ic_feats(tunes, lms); return F.join(I), lms


def _controls(tunes, ref=None):
    ty = pd.get_dummies([t["type"] for t in tunes]).values[:, 1:].astype(float); md = pd.get_dummies([t["mode_family"] for t in tunes]).values[:, 1:].astype(float)
    return np.c_[np.ones(len(tunes)), ty, md, rankdata([t["n"] for t in tunes]), rankdata([t["tune_id"] for t in tunes])]


def _z(v): return (v - v.mean()) / (v.std() + 1e-12)


def fit(train, parts=False):
    """fit the whole reader on a list of tunes (reads their Gs); returns predict(list of tunes) -> array."""
    F, lms = _features(train); cols = list(F.columns); X = F.values.astype(float); med = np.nanmedian(X, 0); X = np.where(np.isnan(X), med, X)
    C = _controls(train); g = rankdata([t["Gs"] for t in train]) / len(train); y = g - C @ np.linalg.lstsq(C, g, rcond=None)[0]
    lo, hi = np.percentile(X, [0.5, 99.5], 0); sc = StandardScaler().fit(np.clip(X, lo, hi)); tr = lambda X_: (lambda Z: np.c_[Z, Z ** 2])(sc.transform(np.clip(X_, lo, hi)))
    R = Ridge(alpha=1000.0).fit(tr(X), y)
    with threadpool_limits(limits=1): G = HistGradientBoostingRegressor(**GB).fit(X, y)

    def predict(tunes):
        F2, _ = _features(tunes, lms); F2 = F2.reindex(columns=cols); X2 = F2.values.astype(float); X2 = np.where(np.isnan(X2), med, X2); a = R.predict(tr(X2))
        with threadpool_limits(limits=1): b = G.predict(X2)
        return (a, b, F2) if parts else _z(a) + _z(b)
    return predict



# ---------------------------------------------------------------- runner-up: the same idea on hymn incipits
HMAJ = [0, 2, 4, 5, 7, 9, 11]; HMIN = [0, 2, 3, 5, 7, 8, 10]
def read(inc, minor):
    s = re.sub(r"[()]", "", str(inc)); sc = HMIN if minor else HMAJ; o = 0; p = []; deg = []
    for ch in s:
        if ch == "U": o += 12
        elif ch == "D": o -= 12
        elif ch in "1234567": p.append(sc[int(ch) - 1] + o); deg.append(int(ch))
    return p, deg
def hfeats(H):
    rows = []; SQ = []
    for inc, minor, meter in zip(H.incipit, H.minor, H.meter):
        p, deg = read(inc, minor); p = np.array(p, float); iv = np.diff(p); a = np.abs(iv); pen = {1, 3, 4, 5, 7} if minor else {1, 2, 3, 5, 6}; n = len(p); sg = np.sign(iv[iv != 0])
        try: l1 = int(str(meter).split(".")[0])
        except Exception: l1 = 8
        l1 = min(max(l1, 4), n); f = dict(penta=np.mean([x in pen for x in deg]), same=(a == 0).mean(), tonic=np.mean([x == 1 for x in deg]), iv_ent=ent(iv), pitch_ent=ent(p), leaps=(a > 4).mean(), range=p.max() - p.min(), step=a.mean(), starts_tonic=float(deg[0] == 1),
                 starts_fifth=float(deg[0] == 5), starts_third=float(deg[0] == 3), stepwise=((a > 0) & (a <= 2)).mean(), gt5=(a > 7).mean(), ndist=len(set(iv)), npitch=len(set(p)), ndeg=len(set(deg)), turns=float((sg[1:] != sg[:-1]).mean()) if len(sg) > 2 else 0.5, thirds=((a == 3) | (a == 4)).mean(),
                 up=(iv > 0).mean(), top_pos=np.argmax(p) / n, low=p.min(), high=p.max(), mean=p.mean(), line1_end_tonic=float(deg[l1 - 1] == 1), line1_end_fifth=float(deg[l1 - 1] == 5), line1_end_triad=float(deg[l1 - 1] in (1, 3, 5)), line1_range=p[:l1].max() - p[:l1].min(),
                 line1_arch=-np.polyfit(np.linspace(-1, 1, l1), p[:l1], 2)[0], line1_desc=p[0] - p[l1 - 1], arch=-np.polyfit(np.linspace(-1, 1, n), p, 2)[0], maxleap=a.max(), orn=str(inc).count("("), below=float(p.min() < 0), first_iv=iv[0], first_abs=a[0],
                 line2_same_start=float(n > l1 and p[l1] == p[0]), triad=np.mean([x in (1, 3, 5) for x in deg]))
        for k in range(1, 8): f[f"d{k}"] = np.mean([x == k for x in deg])
        g3 = [tuple(iv[i:i + 3]) for i in range(len(iv) - 2)]; f["figrep"] = 1 - len(set(g3)) / max(len(g3), 1); g2 = [tuple(p[i:i + 2]) for i in range(n - 1)]; f["pairrep"] = 1 - len(set(g2)) / max(len(g2), 1)
        rows.append(f); SQ.append(dict(deg=[int(x) for x in p], iv=[int(x) for x in iv], d7=deg, minor=bool(minor), meter=meter))
    return pd.DataFrame(rows), SQ
def hic(SQ, lms=None):
    fit = lms is None; lms = {} if fit else lms; out = {}
    for key in ("deg", "iv", "d7"):
        for grp in (None, "minor"):
            S_ = [q[key] for q in SQ]; g = [q[grp] for q in SQ] if grp else None; nm = f"{key}_{grp}"
            if fit: lms[nm] = VLM(5); A, L = lms[nm].fit_score(S_, g)
            else: A, L = lms[nm].score(S_, g)
            st = np.cumsum(L) - L
            for k in ((1, 2, 3, 5) if grp is None else (2, 5)): out[f"ic{k}_{nm}"] = np.array([A[k - 1, s:s + l].mean() for s, l in zip(st, L)])
            if grp is None:
                out[f"icmax_{nm}"] = np.array([A[4, s:s + l].max() for s, l in zip(st, L)]); out[f"icfirst_{nm}"] = np.array([A[4, s:s + min(l, 8)].mean() for s, l in zip(st, L)]); out[f"icsd_{nm}"] = np.array([A[4, s:s + l].std() for s, l in zip(st, L)])
    return pd.DataFrame(out), lms


def fit_hymns(H):
    """fit on a hymn dataframe (reads its y); returns predict(dataframe) -> array."""
    H = H.reset_index(drop=True); F, SQ = hfeats(H); I, lms = hic(SQ); FI = F.join(I); cols = list(FI.columns); X = FI.values.astype(float); n = len(H)
    C = np.c_[np.ones(n), pd.get_dummies(H.meter).values[:, 1:].astype(float), H.minor.values.astype(float), rankdata(H.length)]; y = rankdata(H.y) / n; y = y - C @ np.linalg.lstsq(C, y, rcond=None)[0]
    with threadpool_limits(limits=1): G = HistGradientBoostingRegressor(**HGB).fit(X, y)

    def predict(D):
        D = D.reset_index(drop=True); F2, SQ2 = hfeats(D); I2, _ = hic(SQ2, lms); X2 = F2.join(I2).reindex(columns=cols).values.astype(float)
        with threadpool_limits(limits=1): return G.predict(X2)
    return predict


HGB = dict(max_iter=300, learning_rate=0.03, max_leaf_nodes=6, min_samples_leaf=60, max_features=0.3, random_state=0)
GB = dict(max_iter=600, learning_rate=0.03, max_leaf_nodes=6, min_samples_leaf=80, max_features=0.3, l2_regularization=1.0, random_state=0)
if not os.environ.get("PAGE_GATE_DEV"):
    _predict = fit(arena2.session()); _predict_h = fit_hymns(arena2.hymns())


def page_reader(tunes): return _predict(tunes)


def hymn_reader(H): return _predict_h(H)


CANDIDATES = [
    dict(name="page_reader_long_surprise", kind="session", fn=page_reader, sign=+1,
         why="Kept tunes are the ones whose next pitch is easiest to foresee from the last five notes: long-context pitch surprise plus scale, repeated-figure, strain and rhythm measures, read by a ridge and small boosted trees averaged.",
         baseline="ridge over ~20 plain page measures + trigram surprise (v43/transfer.py recipe): +0.137 on the open half cross-fitted in halves, +0.143 five-fold; this reader +0.224 in halves, +0.24 five-fold"),
    dict(name="hymn_incipit_reader", kind="hymn", fn=hymn_reader, sign=+1,
         why="The same idea on hymn incipits: plain measures of the opening (pentatonic share, direction, degree use, first-line shape) plus five-note scale-degree surprise, read by small boosted trees instead of an equal-weight index.",
         baseline="low bigram surprise -0.06 to -0.07 and plainness index +0.049 on the open half; this reader +0.116 held out in halves, +0.139 five-fold"),
]
