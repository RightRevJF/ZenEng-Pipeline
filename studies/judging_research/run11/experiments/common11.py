"""Run 11 shared code (Hooktheory melodies; frozen with the predictions before any outcome is joined).

Why this source. Run 10's corpus (TheSession.org) is withdrawn: its licence forbids processing with large language models (the
songwriting session's post of 27 Nov 2026 20:22 ET, corroborated by tables/metre_atlas/research_report.md on main). Jason's word
(20:33 ET, via the maintainer): keep the deductions, not the data. So run 10's ideas are tested FRESH here, on an allowed source:
the melodies of the Hooktheory clips (CC BY-NC-SA 3.0, via Sheet Sage), with the within-artist outcome of runs 04 to 06.
NOTHING here reads TheSession data, and no run 10 figure is used as evidence.

SEEN SONGS, said plainly: the 9,588 within-artist songs (1,741 artists) are run 04's rows; their outcome has been joined to chord
measures (runs 04, 05) and to a few melody measures (run 05/06: e.g. tonic resistance). No melody measure built here (pitch-class
entropy of the melody, spectral measures of the melody's pitch graph, ...) has been joined to this outcome before. The songs are
re-spent; the measures are new to them.

Rows      : C5.load_rows()['rows'] (run 05 common): songs of artists with 2+ songs, 17 data-pack measures, run 04 controls.
Melody    : raw Hooktheory clip annotations (C5.raw_clips; sha256 checked). Per clip: notes sorted by onset, rests ignored,
            pitch = 12*octave + pitch_class; clips with fewer than MIN_NOTES notes give no value. Song value = n_mel-weighted mean
            over clips with a value (C5.song_measure); clip 1 vs clip 2 kept for the stability gate.
Outcome   : y_foreign (run 04's rule 4410a0e via C5.load_outcomes): 100 if the song's Discogs-VI group holds a performer set
            sharing no name with the original artist's sets, else 0; nan rows dropped. Guarded: refuses unless the folder's
            PREDICTION.md and this file are committed, unmodified AND pushed to origin/judging-research.
Model     : OLS of z(y_foreign) on z(x) with ARTIST FIXED EFFECTS, run 04's control block (C5.controls), and frozen extra
            z-columns; Frisch-Waugh; CR1 SEs clustered by artist. beta = SD of y per SD of x (within artist).
Second    : conditional logit (artist groups) of the binary y on z(x) + the same columns: SIGN only.
Halves    : md5(artist slug) mod 2 (row['half'], run 04's).
Verdict   : run 10's rules: counted only at power >= 0.2 (R06-5); pass = p < alpha, predicted sign, both halves, second model;
            killed = prediction outside beta +- 1.96 SE (R07-3); else unsettled.
Credit    : Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
            Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
"""
import os, sys, json, math, subprocess, hashlib, importlib.util
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
_spec = importlib.util.spec_from_file_location("run05_common", os.path.normpath(os.path.join(HERE, "..", "..", "run05", "experiments", "common.py")))
C5 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(C5)
SEED = 11
MIN_NOTES = 12
CACHE = os.environ.get("RUN11_CACHE", "/home/claude/dl/run11/measures_run11.json")
BASE = ["ln_notes", "density", "n_pitch", "n_pc", "range", "int_entropy", "n_int", "step_share", "leap_share",
        "unison_share", "pc_entropy", "tonic_share", "bar_rep"]
PACK = C5.FE   # the 17 data-pack measures (mel_ic_mean, ..., ch_rep, rhythm)


# ---------------------------------------------------------------- melody of a clip
def melody(a):
    """dict(pitch, dur, onset, beatpos, bar, bpb, tonic_pc) for a raw clip, or None if fewer than MIN_NOTES notes.
    beatpos = onset mod beats_per_bar (first meter), in beats; on a beat iff beatpos is an integer."""
    notes = sorted(((n["onset"], n["offset"], 12 * n.get("octave", 0) + n["pitch_class"]) for n in (a.get("melody") or [])
                    if n.get("pitch_class") is not None and n["offset"] > n["onset"]), key=lambda x: (x[0], x[2]))
    if len(notes) < MIN_NOTES: return None
    ms = a.get("meters") or [{"beats_per_bar": 4}]
    bpb = ms[0].get("beats_per_bar") or 4
    on = np.array([x[0] for x in notes], float)
    tp = C5.tonic_pc(a)
    return dict(pitch=[int(x[2]) for x in notes], dur=[float(x[1] - x[0]) for x in notes], onset=on.tolist(),
                beatpos=(on % bpb).tolist(), bar=(on // bpb).astype(int).tolist(), bpb=bpb, tonic_pc=0 if tp is None else tp)

def _entropy(counts):
    c = np.array([v for v in counts if v > 0], float)
    if c.sum() == 0: return 0.0
    p = c / c.sum(); return float(-(p * np.log2(p)).sum())

def baseline(mel):
    """run 10's 13 renaming baselines, the same recipes, on a Hooktheory clip melody."""
    p = np.array(mel["pitch"], int); d = np.array(mel["dur"], float); b = np.array(mel["bar"], int)
    iv = np.diff(p); nb = len(set(b.tolist()))
    bars = {}
    for pi, di, bi in zip(p, d, b): bars.setdefault(int(bi), []).append((int(pi), round(float(di), 4)))
    seq = [tuple(bars[k]) for k in sorted(bars)]
    pcd = np.zeros(12)
    for pi, di in zip(p, d): pcd[pi % 12] += di
    return dict(
        ln_notes=math.log(len(p)), density=len(p) / max(nb, 1),
        n_pitch=len(set(p.tolist())), n_pc=len(set((p % 12).tolist())), range=int(p.max() - p.min()),
        int_entropy=_entropy(np.bincount(np.clip(iv + 24, 0, 48), minlength=49)),
        n_int=len(set(iv.tolist())), step_share=float(np.mean((np.abs(iv) >= 1) & (np.abs(iv) <= 2))),
        leap_share=float(np.mean(np.abs(iv) > 4)), unison_share=float(np.mean(iv == 0)),
        pc_entropy=_entropy(pcd), tonic_share=float(pcd[mel["tonic_pc"] % 12] / pcd.sum()),
        bar_rep=1.0 - len(set(seq)) / max(len(seq), 1))


# ---------------------------------------------------------------- rows and the cache
def rows(verbose=False):
    return C5.load_rows(verbose=verbose)["rows"]

def song_values(R, clip_fn, keys, prefix=""):
    """clip_fn(mel, a) -> dict over keys (or None). Sets r[prefix+key] (n_mel-weighted mean over clips with a finite value)
    and r[prefix+key+'_c12'] (clip 1, clip 2 values) for each key."""
    RAW = C5.raw_clips()
    for r in R:
        per = {k: ([], []) for k in keys}
        for c in r["clips"]:
            a = RAW.get(c["k"]); out = None
            if a is not None:
                mel = melody(a)
                if mel is not None:
                    try: out = clip_fn(mel, a)
                    except Exception: out = None
            for k in keys:
                v = float(out[k]) if (out and out.get(k) is not None) else float("nan")
                per[k][0].append(v); per[k][1].append(c["n_mel"])
        for k in keys:
            v, w = np.array(per[k][0], float), np.array(per[k][1], float); ok = np.isfinite(v)
            r[prefix + k] = (float(np.average(v[ok], weights=w[ok])) if w[ok].sum() > 0 else float(np.mean(v[ok]))) if ok.any() else float("nan")
            r[prefix + k + "_c12"] = (v[0], v[1]) if len(v) >= 2 and np.isfinite(v[:2]).all() else None
    return R

def load_cache():
    return json.load(open(CACHE))

def design(measure, extra=(), need_pack=()):
    """rows with the measure and every extra finite (values from the cache, keyed by video id)."""
    M = load_cache(); R = []
    for r in rows():
        m = M.get(r["vid"])
        if m is None: continue
        q = dict(vid=r["vid"], artist=r["artist"], half=r["half"], n_ch=r["n_ch"], beats=r["beats"], nclips=r["nclips"],
                 u=r["u"], tokens=r["tokens"], rep_title=r["rep_title"], clips=r["clips"])
        for f in PACK: q[f] = r.get(f)
        q.update({k: v for k, v in m.items() if not k.endswith("_c12")})
        need = [measure] + list(extra) + list(need_pack)
        if all(q.get(c) is not None and np.isfinite(q[c]) for c in need): R.append(q)
    return R


# ---------------------------------------------------------------- the guard and the outcome
def _pushed_clean(path):
    rel = os.path.relpath(path, REPO)
    if not os.path.exists(path): return False
    out = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "origin/judging-research", "--", rel], capture_output=True, text=True).stdout.strip()
    diff = subprocess.run(["git", "-C", REPO, "diff", "--name-only", "origin/judging-research", "--", rel], capture_output=True, text=True).stdout.strip()
    return bool(out) and not diff

def load_outcomes(R, folder):
    for p in (os.path.join(folder, "PREDICTION.md"), os.path.join(HERE, "common11.py")):
        if not _pushed_clean(p):
            raise SystemExit(f"REFUSED: {p} is not committed, unmodified and pushed to origin/judging-research: outcome NOT joined")
    info = C5.load_outcomes(R, folder)
    return info


# ---------------------------------------------------------------- model (within artist)
def _z(v):
    v = np.asarray(v, float); s = v.std(); return (v - v.mean()) / s if s > 0 else v * 0

def _demean(M, g):
    M = np.asarray(M, float).reshape(len(g), -1); codes = {a: i for i, a in enumerate(sorted(set(g)))}
    gg = np.array([codes[a] for a in g]); s = np.zeros((len(codes), M.shape[1])); np.add.at(s, gg, M)
    cnt = np.bincount(gg, minlength=len(codes)); return M - (s / cnt[:, None])[gg], len(codes)

def control_matrix(R, extra=()):
    _, X = C5.controls(R)
    cols = [X] + [_z([r[e] for r in R])[:, None] for e in extra]
    return np.hstack(cols)

class Projector:
    def __init__(self, R, extra=()):
        self.g = [r["artist"] for r in R]
        Cw, self.G = _demean(control_matrix(R, extra), self.g)
        keep = np.abs(Cw).sum(0) > 1e-10; Cw = Cw[:, keep]
        q, rr = np.linalg.qr(Cw); ok = np.abs(np.diag(rr)) > 1e-8
        self.Q = q[:, ok]; self.k = int(ok.sum()) + self.G
    def resid(self, v):
        vw, _ = _demean(v, self.g); vw = vw.ravel(); return vw - self.Q @ (self.Q.T @ vw)

def fwl_fit(rx, ry, cl, k):
    n = len(rx); sxx = float(rx @ rx); b = float(rx @ ry) / sxx; e = ry - b * rx
    g = {}
    for i, c in enumerate(cl): g[c] = g.get(c, 0.0) + rx[i] * e[i]
    G = len(g); meat = sum(v * v for v in g.values())
    adj = (G / (G - 1)) * ((n - 1) / max(n - k - 1, 1))
    se = math.sqrt(adj * meat) / sxx; p = 2 * stats.norm.sf(abs(b / se))
    return b, se, p

def fit(R, xcol, ycol="y_foreign", extra=()):
    R = [r for r in R if r.get(ycol) is not None and np.isfinite(r[ycol])]
    x = _z([r[xcol] for r in R]); y = _z([r[ycol] for r in R]); P = Projector(R, extra)
    b, se, p = fwl_fit(P.resid(x), P.resid(y), P.g, P.k)
    return dict(beta=b, se=se, p=p, lo=b - 1.96 * se, hi=b + 1.96 * se, n=len(R), artists=P.G)

def power(R, xcol, beta, alpha, extra=(), draws=300, seed=SEED):
    """fake outcomes on the real design: y = beta z(x) + N(0, 1 - beta^2); no outcome is read."""
    rng = np.random.default_rng(seed); x = _z([r[xcol] for r in R]); P = Projector(R, extra); rx = P.resid(x)
    hit = kt = kz = 0; ses = []
    for _ in range(draws):
        for which in ("true", "zero"):
            bb = beta if which == "true" else 0.0
            y = _z(bb * x + rng.normal(0, math.sqrt(max(1 - bb * bb, 1e-9)), len(x)))
            b, se, p = fwl_fit(rx, P.resid(y), P.g, P.k)
            killed = not (b - 1.96 * se <= beta <= b + 1.96 * se)
            if which == "true":
                ses.append(se); kt += killed
                if p < alpha and np.sign(b) == np.sign(beta): hit += 1
            else: kz += killed
    return dict(power=hit / draws, kill_if_true=kt / draws, kill_if_zero=kz / draws, median_fake_se=float(np.median(ses)),
                draws=draws, seed=seed, n=len(R), artists=P.G)

def halves(R, xcol, ycol="y_foreign", extra=()):
    return [fit([r for r in R if r["half"] == h], xcol, ycol, extra) for h in (0, 1)]

def second(R, xcol, ycol="y_foreign", extra=()):
    R = [r for r in R if r.get(ycol) is not None and np.isfinite(r[ycol])]
    X = np.hstack([_z([r[xcol] for r in R])[:, None], control_matrix(R, extra)])
    keep = X.std(0) > 1e-12; keep[0] = True; X = X[:, keep]
    try:
        pa, bse, pv, conv, ns, ng = C5.cond_logit(X, np.array([r[ycol] > 0 for r in R], float), [r["artist"] for r in R])
        return dict(beta=float(pa[0]), se=float(bse[0]), p=float(pv[0]), converged=bool(conv), songs=ns, groups=ng)
    except Exception as ex:
        return dict(beta=float("nan"), se=float("nan"), p=float("nan"), error=str(ex))

def verdict(res, pred, alpha, pw, hv, sec):
    counted = pw >= 0.2
    sign_ok = np.sign(res["beta"]) == np.sign(pred)
    halves_ok = all(np.sign(h["beta"]) == np.sign(pred) for h in hv)
    second_ok = sec is not None and np.isfinite(sec.get("beta", np.nan)) and np.sign(sec["beta"]) == np.sign(pred)
    killed = not (res["lo"] <= pred <= res["hi"])
    if not counted: v = "estimate"
    elif res["p"] < alpha and sign_ok and halves_ok and second_ok: v = "passed"
    elif killed: v = "killed"
    else: v = "unsettled"
    return dict(verdict=v, counted=bool(counted), sign_ok=bool(sign_ok), halves_ok=bool(halves_ok), second_ok=bool(second_ok),
                prediction_outside_range=bool(killed))


# ---------------------------------------------------------------- notes-side gates
def renaming(R, xcol, cols=None):
    cols = cols or (BASE + PACK)
    x = np.array([r[xcol] for r in R], float); out = {}
    for c in cols:
        v = np.array([r.get(c, np.nan) for r in R], float); ok = np.isfinite(v) & np.isfinite(x)
        if ok.sum() > 50 and v[ok].std() > 0: out[c] = float(stats.spearmanr(x[ok], v[ok]).correlation)
    B = [c for c in BASE if np.std([r[c] for r in R]) > 0]
    X = np.column_stack([np.ones(len(R))] + [_z([r[c] for r in R]) for c in B])
    bb, *_ = np.linalg.lstsq(X, x, rcond=None); res = x - X @ bb
    out["R2_on_13_baselines"] = float(1 - res.var() / x.var())
    return out

def stability(R, xcol):
    """Spearman of the measure between a song's first two clips (different sections of the song)."""
    M = load_cache(); a, b = [], []
    for r in R:
        p = M.get(r["vid"], {}).get(xcol + "_c12")
        if p and np.isfinite(p[0]) and np.isfinite(p[1]): a.append(p[0]); b.append(p[1])
    return dict(spearman=float(stats.spearmanr(a, b).correlation) if len(a) > 10 else float("nan"), n=len(a))
