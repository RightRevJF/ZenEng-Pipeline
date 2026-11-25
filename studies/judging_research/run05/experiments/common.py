"""Run 05 shared code: rows, controls, raw notes, gate, outcomes and models for tonight's tests.

What is new tonight: the full Hooktheory annotations (Sheet Sage's Hooktheory.json.gz, 26,175 clips) were fetched from
raw.githubusercontent.com/chrisdonahue/sheetsage-data (the same file studies/judging_data/make.py reads). It is a raw download,
kept OUTSIDE the repo (default /home/claude/dl/hooktheory/Hooktheory.json.gz, or $HOOKTHEORY_RAW) and checked by sha256.
It gives the notes of every Hooktheory song, not only the 3,080 matched to Discogs-VI, so a measure computed from the notes can
now be tested on run 04's extensive-margin rows (9,588 songs by 1,741 artists with two or more songs).

Rows and controls are run 04's (../../run04/experiments/move_extensive/test.py, rule 00ab557), byte-for-byte in logic:
  artist fixed effect; chord-count bins; clips-per-song dummies; ln beats; title flags (word count, parentheses, shared title).
Outcomes (only via load_outcomes(), which refuses to run unless the caller's PREDICTION.md is committed in git):
  y        = 100 if the song's video id is a key of hooktheory_covers_discogs.json (in Discogs-VI at all), else 0
  y_foreign= 100 if its Discogs-VI group holds a performer set sharing no name with the original artist's own sets (run 04 rule 4410a0e)
  covers   = log(1 + covers) and first_year, for matched songs (intensive margin)
Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
"""
import json, gzip, io, collections, re, hashlib, os, sys, subprocess, urllib.parse, warnings
import numpy as np
from scipy.stats import norm as N, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("HOOKTHEORY_RAW", "/home/claude/dl/hooktheory/Hooktheory.json.gz")
RAW_SHA256 = "917b7cd58f5f4e07d6c36acf7bfad958c99ee05472dab3555399141094698e0c"
GIT = lambda path: subprocess.run(["git", "-C", HERE, "show", f"origin/main:studies/judging_data/{path}"], check=True, capture_output=True).stdout
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF   # the 17 data-pack measures
r4 = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)
zs = lambda x: (np.asarray(x, float) - np.nanmean(x)) / np.nanstd(x)


# ------------------------------------------------------------------ rows (run 04's), from the data pack's per-clip measures
def toks(slug):
    u = urllib.parse.unquote(slug).lower(); b = re.sub(r"\([^)]*\)", " ", u)
    t = [x for x in re.split(r"[^a-z0-9]+", b) if x]
    return u, (t or [x for x in re.split(r"[^a-z0-9]+", u) if x])

def load_rows(verbose=True):
    """Returns dict(rows, allsongs, clips_by_vid). rows = songs of artists with 2+ songs (9,588). Each row has the 17 measures
    (n_mel-weighted means over clips), n_ch, beats, nclips, title flags, artist, half (md5 of the artist slug mod 2), and 'clips'
    (the surprise-file clip records in file order, each with k = Hooktheory clip id and n_mel)."""
    raw_s, raw_r = GIT("hooktheory_surprise.json.gz"), GIT("hooktheory_rhythm.json.gz")
    md5 = [hashlib.md5(raw_s).hexdigest(), hashlib.md5(raw_r).hexdigest()]
    assert md5[0].startswith("ff7b9d37") and md5[1].startswith("1d6e0405"), md5
    S = json.load(gzip.open(io.BytesIO(raw_s))); RH = {r["k"]: r for r in json.load(gzip.open(io.BytesIO(raw_r)))}
    by = collections.OrderedDict()
    for c in S: by.setdefault(c["vid"], []).append(c)
    SF = ["n_ch", "beats", "ch_ic_sd"] + FE[:8]
    allsongs = []
    for vid, cs in by.items():
        w = np.array([c["n_mel"] for c in cs], float)
        avg = (lambda v: float(np.average(v, weights=w))) if w.sum() > 0 else (lambda v: float(np.mean(v)))
        r = {f: avg([c[f] for c in cs]) for f in SF}
        rc = [(c, RH[c["k"]]) for c in cs if c["k"] in RH]
        for f in RF:
            if not rc: r[f] = np.nan; continue
            wr = np.array([c["n_mel"] for c, _ in rc], float); v = [h[f] for _, h in rc]
            r[f] = float(np.average(v, weights=wr)) if wr.sum() > 0 else float(np.mean(v))
        u, t = toks(cs[0]["song"])
        r.update(vid=vid, artist=cs[0]["artist"], slug=cs[0]["song"], nclips=len(cs), u=u, tokens=t, key="-".join(t), clips=cs)
        allsongs.append(r)
    keyart = collections.defaultdict(set)
    for r in allsongs: keyart[r["key"]].add(r["artist"])
    for r in allsongs: r["rep_title"] = len(keyart[r["key"]]) >= 2
    nart = collections.Counter(r["artist"] for r in allsongs)
    rows = [r for r in allsongs if nart[r["artist"]] >= 2]
    for r in rows: r["half"] = int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
    if verbose:
        arts = sorted(set(r["artist"] for r in rows))
        print(f"rows: {len(rows)} songs [9,588], {len(arts)} artists [1,741] (of {len(allsongs)} songs, {len(nart)} artists); "
              f"halves {sum(1 for a in arts if int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 == 0)} / "
              f"{sum(1 for a in arts if int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 == 1)} artists [886 / 855]", flush=True)
    return dict(rows=rows, allsongs=allsongs)

def controls(rows):
    """run 04's control block (names, matrix): n_ch bins, clips dummies, ln beats, title flags."""
    nch = np.array([r["n_ch"] for r in rows]); binv = np.digitize(nch, [5, 7, 9, 11, 13, 16, 20, 25, 32])
    ncl = np.array([r["nclips"] for r in rows]); ntk = np.array([len(r["tokens"]) for r in rows])
    par = np.array([("(" in r["u"]) for r in rows], float); rep = np.array([r["rep_title"] for r in rows], float)
    cols = {f"nch_bin{k}": (binv == k).astype(float) for k in range(1, 10)}
    cols.update({"clips2": (ncl == 2).astype(float), "clips3": (ncl == 3).astype(float), "clips4p": (ncl >= 4).astype(float)})
    cols["ln_beats"] = np.log([r["beats"] for r in rows])
    cols.update({f"words{k}": (ntk == k).astype(float) for k in (1, 2, 3, 4)}); cols.update(parens=par, rep_title=rep)
    return list(cols), np.column_stack(list(cols.values()))


# ------------------------------------------------------------------ raw notes
_RAWD = None
def raw_clips():
    """dict clip id -> annotations {num_beats, meters, keys, melody, harmony} from the full Hooktheory file (sha256 checked)."""
    global _RAWD
    if _RAWD is None:
        b = open(RAW, "rb").read(); h = hashlib.sha256(b).hexdigest()
        assert h == RAW_SHA256, f"raw Hooktheory file sha256 {h} != {RAW_SHA256}"
        D = json.load(gzip.open(io.BytesIO(b))); _RAWD = {k: c["annotations"] for k, c in D.items()}
    return _RAWD

def chord_pcs(h):
    """pitch-class set (sorted tuple, absolute pcs) of a Hooktheory harmony event: root_pitch_class + stacked root_position_intervals."""
    pcs = [h["root_pitch_class"] % 12]; acc = h["root_pitch_class"]
    for iv in h.get("root_position_intervals") or []:
        acc += iv; pcs.append(acc % 12)
    return tuple(sorted(set(pcs)))

def tonic_pc(a, beat=0.0):
    ks = a.get("keys") or []
    if not ks: return None
    cur = ks[0]
    for k in ks:
        if k["beat"] <= beat: cur = k
    return cur["tonic_pitch_class"] % 12

def melody_midi(a):
    """list of (onset, offset, pitch) with pitch = 12*octave + pitch_class (relative height; Hooktheory octave 0 is the reference)."""
    return [(n["onset"], n["offset"], 12 * n.get("octave", 0) + n["pitch_class"]) for n in (a.get("melody") or [])
            if n.get("pitch_class") is not None and n["offset"] > n["onset"]]

def song_measure(rows, fn, name):
    """Applies fn(annotations, clip_record) -> float or nan to every clip of every row; song value = n_mel-weighted mean over clips
    with a finite value (plain mean if weights are all zero). Also stores clip-1 / clip-2 values for the stability gate.
    Sets r[name] and r[name + '_c12']."""
    R = raw_clips(); missing = 0
    for r in rows:
        vals, ws = [], []
        for c in r["clips"]:
            a = R.get(c["k"])
            if a is None: missing += 1; v = np.nan
            else:
                try: v = fn(a, c)
                except Exception: v = np.nan
            vals.append(v); ws.append(c["n_mel"])
        vals, ws = np.array(vals, float), np.array(ws, float); ok = np.isfinite(vals)
        if ok.any():
            r[name] = float(np.average(vals[ok], weights=ws[ok])) if ws[ok].sum() > 0 else float(np.mean(vals[ok]))
        else: r[name] = np.nan
        r[name + "_c12"] = (vals[0], vals[1]) if len(vals) >= 2 and np.isfinite(vals[:2]).all() else None
    return missing


# ------------------------------------------------------------------ gate (notes only)
def sp(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float); ok = ~(np.isnan(a) | np.isnan(b))
    return float(spearmanr(a[ok], b[ok])[0]), int(ok.sum())

def gate(rows, name, stab=0.20, overlap=0.70, extra=None):
    """Stability: Spearman of clip 1 vs clip 2 >= stab. Renaming: no |Spearman| > overlap with the 17 data-pack measures, n_ch,
    beats or clips per song (plus any arrays in `extra`, a dict name -> per-row values). Returns dict with 'passed'."""
    pr = [r[name + "_c12"] for r in rows if r.get(name + "_c12")]
    st = float(spearmanr([p[0] for p in pr], [p[1] for p in pr])[0]) if len(pr) > 10 else float("nan")
    x = [r[name] for r in rows]
    others = {f: [r[f] for r in rows] for f in FE}
    others.update(n_ch=[r["n_ch"] for r in rows], beats=[r["beats"] for r in rows], clips_per_song=[r["nclips"] for r in rows])
    if extra: others.update(extra)
    ov = {k: sp(x, v)[0] for k, v in others.items()}
    top = max(ov, key=lambda k: abs(ov[k]) if np.isfinite(ov[k]) else -1)
    n_ok = int(np.isfinite(np.asarray(x, float)).sum())
    passed = bool(st >= stab and abs(ov[top]) <= overlap)
    return dict(measure=name, songs_with_value=n_ok, clip_pairs=len(pr), clip_to_clip=r4(st), stab_threshold=stab,
                overlap_largest=[top, r4(ov[top])], overlap_threshold=overlap, overlap_all={k: r4(v) for k, v in ov.items()}, passed=passed)


# ------------------------------------------------------------------ outcomes (guarded)
def _prediction_committed(folder):
    p = os.path.join(folder, "PREDICTION.md")
    if not os.path.exists(p): return False
    out = subprocess.run(["git", "-C", folder, "log", "--oneline", "-1", "--", "PREDICTION.md"], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", folder, "status", "--porcelain", "--", "PREDICTION.md"], capture_output=True, text=True).stdout.strip()
    return bool(out) and not dirty

def load_outcomes(rows, folder):
    """Refuses unless folder/PREDICTION.md is committed and unmodified. Sets on each row: y, y_foreign (nan if dropped),
    covers (raw), lcov = log(1+covers), first_year (None for unmatched), drop_reason. Returns a summary dict."""
    if not _prediction_committed(folder):
        raise SystemExit(f"PREDICTION.md in {folder} is not committed (or has uncommitted edits): outcome NOT joined")
    a_, b_ = GIT("hooktheory_covers_discogs.json"), GIT("discogs_versions_matched.json")
    md5o = [hashlib.md5(a_).hexdigest(), hashlib.md5(b_).hexdigest()]
    CV = json.loads(a_); VC = json.loads(b_)["cliques"]
    nrm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))
    drops = 0
    for r in rows:
        r.update(y=0.0, y_foreign=0.0, covers=None, lcov=None, first_year=None, drop_reason=None, versions=None)
        if r["vid"] not in CV: continue
        cv = CV[r["vid"]]; r["y"] = 100.0
        r["covers"] = cv.get("covers"); r["lcov"] = float(np.log1p(cv["covers"])) if cv.get("covers") is not None else None
        r["first_year"] = cv.get("first_year")
        cq = cv.get("clique")
        if cq not in VC: r["y_foreign"] = np.nan; r["drop_reason"] = "clique missing"; drops += 1; continue
        r["versions"] = VC[cq]["versions"]
        sets = [e[0] for e in VC[cq]["versions"]]; a = nrm(r["artist"])
        own = [s for s in sets if any(nrm(nm) == a for nm in s)]
        if not own: r["y_foreign"] = np.nan; r["drop_reason"] = "no own set"; drops += 1; continue
        O = {nrm(nm) for s in own for nm in s}
        r["y_foreign"] = 100.0 if [s for s in sets if len(s) > 0 and not any(nrm(nm) in O for nm in s)] else 0.0
    return dict(md5=md5o, drops=drops, y1=int(sum(r["y"] > 0 for r in rows)),
                y_foreign1=int(sum((r["y_foreign"] or 0) > 0 for r in rows if np.isfinite(r["y_foreign"]))))


# ------------------------------------------------------------------ models
def lpm(Xm, yv, gv):
    """within-group OLS of yv on Xm (group = artist), CR1 clustered by group. Returns b, se, p (arrays), N, G, K."""
    codes = {a: i for i, a in enumerate(sorted(set(gv)))}; gg = np.array([codes[a] for a in gv]); Gn = len(codes); c_ = np.bincount(gg)
    def d(M):
        M2 = np.asarray(M, float).reshape(len(M), -1); s = np.zeros((Gn, M2.shape[1])); np.add.at(s, gg, M2); return M2 - (s / c_[:, None])[gg]
    Xw, yw = d(Xm), d(yv).ravel()
    keepc = np.where(np.abs(Xw).sum(0) > 1e-12)[0]   # columns with no within-group variation are dropped (reported as nan)
    Xw2 = Xw[:, keepc]; Nn, K = Xw2.shape
    XtXi = np.linalg.pinv(Xw2.T @ Xw2); b2 = XtXi @ Xw2.T @ yw; u = yw - Xw2 @ b2
    sc = np.zeros((Gn, K)); np.add.at(sc, gg, Xw2 * u[:, None])
    V = Gn / (Gn - 1) * (Nn - 1) / (Nn - K) * XtXi @ (sc.T @ sc) @ XtXi
    b = np.full(Xw.shape[1], np.nan); se = np.full(Xw.shape[1], np.nan); b[keepc] = b2; se[keepc] = np.sqrt(np.diag(V))
    p = 2 * N.sf(np.abs(b / se))
    return dict(b=b, se=se, p=p, N=Nn, G=Gn, K=K)

def summ(m, i):
    return dict(beta=r4(m["b"][i]), se=r4(m["se"][i]), p=float(f"{m['p'][i]:.4g}"),
                ci95=[r4(m["b"][i] - 1.96 * m["se"][i]), r4(m["b"][i] + 1.96 * m["se"][i])])

def power(pred, se, alpha):
    z = float(N.isf(alpha / 2)); return float(N.cdf(abs(pred) / se - z) + N.cdf(-abs(pred) / se - z))

def cond_logit(X, yb, groups):
    """statsmodels ConditionalLogit on groups with variation; returns (params, bse, pvalues, converged, kept_songs, kept_groups)."""
    from statsmodels.discrete.conditional_models import ConditionalLogit
    codes = {a: i for i, a in enumerate(sorted(set(groups)))}; g = np.array([codes[a] for a in groups]); cnt = np.bincount(g)
    ga = np.bincount(g, weights=yb); keep_g = (ga > 0) & (ga < cnt); keep = keep_g[g]
    sys.setrecursionlimit(max(10000, 4 * int(cnt.max())))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mod = ConditionalLogit(yb[keep].astype(int), X[keep], groups=g[keep])
        fit = mod.fit(method="bfgs", maxiter=2000, disp=False)
        conv = bool(np.max(np.abs(mod.score(fit.params))) / mod.nobs < 1e-5)
        if not conv:
            fit = mod.fit(start_params=fit.params, method="newton", maxiter=100, disp=False)
            conv = bool(np.max(np.abs(mod.score(fit.params))) / mod.nobs < 1e-5)
    return fit.params, fit.bse, fit.pvalues, conv, int(keep.sum()), int(keep_g.sum())
