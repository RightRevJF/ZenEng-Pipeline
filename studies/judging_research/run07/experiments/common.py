"""Run 07 shared code, frozen by the chair before any outcome is joined.

THE NEW DATA: whole songs from the Lakh Pianoroll Dataset (LPD-5 cleansed, 21,425 songs; Dong et al. 2018, from Raffel's Lakh MIDI
Dataset; Zenodo 5646574, CC BY 4.0), named by the Gold-Caps LMD-matched metadata (Zenodo 10178563, CC BY 4.0; artist, title, year and
song_hotttnesss are the Million Song Dataset's), with Billboard Hot 100 flags from the Hit Song Prediction set (Zenodo 3258042).
The notes are read by lakh_notes.py (bar chroma, half-bar triad chords). NO Lakh song has ever been joined to an outcome.

Songs. A Lakh SONG is (nrm(artist_name), nrm(clean(title))). clean() removes every (...) and [...] segment, then cuts at the first
" - ". Tracks of one song are averaged (measures) and share one outcome. Excluded before anything else:
  - SEEN: any song whose artist and title (clean or exact) equal a Hooktheory song in Sheet Sage's Hooktheory.json.gz (all 26,175
    clips, every song: the pack's and run 06's fresh songs alike), under nrm() of the slugs;
  - HOLD-OUT: any song whose artist and title (clean or exact) equal a McGill Billboard chart in studies/harmony/billboard_sections.json;
  - songs with fewer than 8 bars or fewer than 5 chord runs;
  - AMBIGUOUS FILES: the Lakh match is audio-based, and one MIDI file (md5) is often the chosen file for several MSD tracks, many of
    them unrelated songs (one file serves 12 different titles). A track is kept only if its md5 carries ONE clean title over all
    21,425 tracks (the Skeptic's fix: a file under one title and several artists is a song and its covers, and it is given to each
    of those artists). Within a song, a file is counted once;
  - COVER-ONLY ARTISTS: artist names matching COVER_ARTISTS (karaoke, tribute, panpipe and similar acts, frozen below), whose songs'
    outcomes belong to other performers.
The design is within artist: artists with at least two songs left.

THE OUTCOME (post-commit only): Discogs-VI 20240701 reduced by the maintainer's cliques_versions.py (origin/main, unchanged) into
$DISCOGS_SHAPE/discogs_cliques.json and discogs_versions.jsonl; matched by the maintainer's rule (covers_match_discogs.py): the clique
whose title == the song's clean nrm title and whose artists include nrm(artist); among several, the one with most artist sets (first
on ties). y = 100 if matched. y_foreign = run 05's rule: 100 if some version's performer set shares no name with the artist's own
sets; nan if matched but no own set (dropped). Unmatched songs: y = y_foreign = 0.

GUARD: every outcome loader refuses unless the calling folder's PREDICTION.md AND this file are committed and unmodified.
Credit: Lakh MIDI Dataset (Raffel 2016) and LPD (Dong et al. 2018), CC BY 4.0; Million Song Dataset (Bertin-Mahieux et al. 2011) via
Gold-Caps (Jonason, Casini & Sturm 2023), CC BY 4.0; Hit Song Prediction (Zangerle et al. 2019); Hooktheory (via Sheet Sage),
CC BY-NC-SA 3.0, used only to exclude seen songs; Discogs-VI (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
"""
import os, re, json, gzip, math, hashlib, collections, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.environ.get("LAKH_DL", "/home/claude/dl")
SHAPE = os.environ.get("DISCOGS_SHAPE", "/home/claude/shape")
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
nrm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))      # the maintainer's norm()
COVER_ARTISTS = re.compile(r"karaoke|tribute|pan ?pipe|orchestra|hit ?crew|top of the poppers|in the style of|lullab|string quartet|"
                           r"piano players|ameritz|studio musicians|cover band|countdown (singers|kids)|sound.?alike|backing track|"
                           r"made famous|the hit makers|party hits|the starlite|starlight singers|chartbusters|twinkle", re.I)
half_of = lambda artist: int(hashlib.md5(artist.encode()).hexdigest(), 16) % 2         # artist halves (md5 of the artist key)

def clean(t):
    t = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", t or "")
    return t.split(" - ")[0].strip()


# ====================================================================== the guard
def _committed_clean(path):
    d, f = os.path.dirname(path), os.path.basename(path)
    if not os.path.exists(path): return False
    out = subprocess.run(["git", "-C", d, "log", "--oneline", "-1", "--", f], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", d, "status", "--porcelain", "--", f], capture_output=True, text=True).stdout.strip()
    return bool(out) and not dirty

def guard(folder):
    for p in (os.path.join(folder, "PREDICTION.md"), os.path.join(HERE, "common.py")):
        if not _committed_clean(p):
            raise SystemExit(f"{p} is not committed (or has uncommitted edits): outcome NOT joined")


# ====================================================================== notes-side measures (per track)
def repetition(s, n=3):
    """the pack's ch_rep: share of n-grams already heard earlier in the sequence."""
    seen = set(); rep = tot = 0
    for i in range(len(s) - n + 1):
        g = tuple(s[i:i + n]); tot += 1; rep += g in seen; seen.add(g)
    return rep / tot if tot else np.nan

def theta(tok): return 2 * math.pi * ((7 * (tok % 12)) % 12) / 12        # chord root on the circle of fifths

def CH(toks):
    """run 06's harmonic chirality on the open walk of chord roots (signed area per move on the circle of fifths)."""
    K = len(toks) - 1
    if K < 6: return np.nan
    th = [theta(t) for t in toks]
    return 0.5 * sum(math.sin(th[i + 1] - th[i]) for i in range(K)) / K

def A_arrow(toks):
    """run 05's arrow of time on chord tokens: 1 - (two-way moves)/(all moves)."""
    K = len(toks) - 1
    if K < 6: return np.nan
    n = collections.Counter(zip(toks, toks[1:]))
    return 1.0 - sum(min(v, n.get((y, x), 0)) for (x, y), v in n.items()) / sum(n.values())

def track_measures(n):
    t = n["toks"]
    return dict(ch_rep=repetition(t), ln_chg=math.log(max(len(t), 1)), V=len(set(t)), ln_bars=math.log(max(n["n_bars"], 1)),
                CH=CH(t), A=A_arrow(t))

MEASURES = ["ch_rep", "ln_chg", "V", "ln_bars", "CH", "A"]


# ====================================================================== exclusions and songs
def _hooktheory_keys():
    H = json.load(gzip.open(os.path.join(DL, "ht", "Hooktheory.json.gz")))
    return {(nrm(v["hooktheory"]["artist"]), nrm(v["hooktheory"]["song"])) for v in H.values()}

def _mcgill_keys():
    M = json.load(open(os.path.join(REPO, "studies", "harmony", "billboard_sections.json")))
    return {(nrm(m["artist"]), nrm(m["title"])) for m in M} | {(nrm(m["artist"]), nrm(clean(m["title"]))) for m in M}

def lakh_songs(verbose=True):
    """Returns the song list (dicts) after exclusions, within-artist only, with per-song mean measures and extra fields:
    key, artist_key, title_key, tids, year (max over tracks, 0 = unknown), bb (any track on the Hot 100), hot (max hotttnesss),
    n_tracks, half. Deterministic; reads no outcome."""
    notes = json.load(open(os.path.join(DL, "lakh", "notes.json")))
    HT, MG = _hooktheory_keys(), _mcgill_keys()
    owners = collections.defaultdict(set)
    for n in notes: owners[n["md5"]].add(nrm(clean(n["title"])))
    by = collections.OrderedDict(); n_seen = n_hold = n_short = n_amb = n_cov = 0; used = set()
    for n in sorted(notes, key=lambda x: x["tid"]):
        if len(owners[n["md5"]]) > 1: n_amb += 1; continue
        if COVER_ARTISTS.search(n["artist"] or ""): n_cov += 1; continue
        a, tc, tx = nrm(n["artist"]), nrm(clean(n["title"])), nrm(n["title"])
        if not a or not tc: n_short += 1; continue
        if (a, tc) in HT or (a, tx) in HT: n_seen += 1; continue
        if (a, tc) in MG or (a, tx) in MG: n_hold += 1; continue
        if n["n_bars"] < 8 or len(n["toks"]) < 5: n_short += 1; continue
        if (a, tc, n["md5"]) in used: continue
        used.add((a, tc, n["md5"])); by.setdefault((a, tc), []).append(n)
    songs = []
    for (a, tc), tr in by.items():
        ms = [track_measures(x) for x in tr]
        s = dict(key=f"{a}|{tc}", artist_key=a, title_key=tc, artist=tr[0]["artist"], title=clean(tr[0]["title"]),
                 tids=[x["tid"] for x in tr], md5s=[x["md5"] for x in tr], n_tracks=len(tr),
                 year=min([x["year"] for x in tr if x["year"]], default=0),
                 bb=any(x["bb"] for x in tr), hot=max([x["hot"] for x in tr if x["hot"] is not None], default=None), half=half_of(a))
        for m in MEASURES:
            v = np.array([d[m] for d in ms], float); v = v[np.isfinite(v)]
            s[m] = float(v.mean()) if len(v) else np.nan
        songs.append(s)
    cnt = collections.Counter(s["artist_key"] for s in songs)
    within = [s for s in songs if cnt[s["artist_key"]] >= 2]
    if verbose:
        print(f"Lakh tracks {len(notes)}; ambiguous files {n_amb}; cover-only artists {n_cov}; excluded seen (Hooktheory) {n_seen}, hold-out (McGill) {n_hold}, short/blank {n_short}; "
              f"songs {len(songs)}; within-artist songs {len(within)} by {len({s['artist_key'] for s in within})} artists")
    return within


# ====================================================================== whole-song measures (frozen; the Skeptic's code, notes only)
TRI = []
for _r in range(12):
    for _iv in ((0, 4, 7), (0, 3, 7)):
        _v = np.zeros(12); _v[[(_r + i) % 12 for i in _iv]] = 1; TRI.append(_v / 3)
TRI = np.array(TRI)

def fp_stats(P, seed, K=4000):
    """mean four-point fp / mean pairwise distance, and the CV of pairwise distances (Gilbert & Yim's concentration pitfall)."""
    import itertools
    m = len(P)
    if m < 4: return None
    D = np.sqrt(np.maximum(((P[:, None] - P[None]) ** 2).sum(-1), 0)); d = D[np.triu_indices(m, 1)]
    if d.mean() < 1e-9: return None
    if math.comb(m, 4) <= K: Q = np.array(list(itertools.combinations(range(m), 4)))
    else:
        r = np.random.default_rng(seed); Q = np.argsort(r.random((K, m)), 1)[:, :4] if m <= 200 else np.array([r.choice(m, 4, replace=False) for _ in range(K)])
    a, b, c, e = Q.T
    S = np.sort(np.stack([D[a, b] + D[c, e], D[a, c] + D[b, e], D[a, e] + D[b, c]]), 0)
    return (S[2] - S[1]).mean() / 2 / d.mean(), d.std() / d.mean()

def song_shape(X, t, seed, tempo):
    """X: bar chroma (L1 per bar), t: chord tokens. Returns H4m, cv_w (R07-L1 merged), g (R07-G3 = R02-gap on whole songs),
    lnP, Pcat, lnPsec (R07-L2), F (R07-I2), B (R07-I3)."""
    out = {}
    X = np.asarray(X, float); S = X[X.sum(1) > 0]
    n = np.linalg.norm(S, axis=1); U = S[n > 1e-9] / n[n > 1e-9, None]; nb = len(U)
    out["H4m"] = out["cv_w"] = np.nan
    if nb >= 8:
        W = np.array([U[i:i + 4].ravel() / 2 for i in range(nb - 3)]); W = np.unique(np.round(W, 6), axis=0)
        r = fp_stats(W, seed)
        if r: out["H4m"], out["cv_w"] = 2 * r[0], r[1]
    tt = list(t) + [t[0]]; idx = {c: i for i, c in enumerate(sorted(set(t)))}; k = len(idx); out["g"] = np.nan
    if k >= 2:
        M = np.zeros((k, k))
        for x, y in zip(tt, tt[1:]): M[idx[x], idx[y]] += 1
        M = M / np.maximum(M.sum(1, keepdims=True), 1)
        ev = np.sort(np.abs(np.linalg.eigvals(M)))[::-1]; out["g"] = float(1 - ev[1])
    L1 = S / S.sum(1, keepdims=True) if len(S) else S
    out["lnP"] = out["Pcat"] = out["lnPsec"] = np.nan
    if len(L1) >= 34:
        Dl = [((L1[l:] - L1[:-l]) ** 2).sum(1).mean() for l in range(2, 17)]; P = 2 + int(np.argmin(Dl))
        out["lnP"] = math.log(P); out["Pcat"] = P if P in (2, 4, 8, 16) else 0
        if tempo: out["lnPsec"] = math.log(P * 4 * 60 / tempo)
    out["F"] = float((L1 @ TRI.T).max(1).mean() * 3) if len(L1) >= 4 else np.nan
    pos = collections.defaultdict(list)
    for i, c in enumerate(t): pos[c].append(i)
    rr = []
    for c, p in pos.items():
        if len(p) >= 3: g = np.diff(p).astype(float); rr.extend(g / g.mean())
    out["B"] = float((np.std(rr) - 1) / (np.std(rr) + 1)) if len(rr) >= 6 else np.nan
    return out

SHAPES = ["H4m", "cv_w", "g", "lnP", "lnPsec", "F", "B", "ln_tempo"]

def add_shapes(songs, cache=os.path.join(DL, "lakh", "shapes_run07.json")):
    """per-song means over the song's files of song_shape(); seed = int(md5(tid)[:8], 16); tempo from LPD midi_info_v2.json.
    Pcat is taken from the song's first file. Cached (notes only)."""
    if os.path.exists(cache): C = json.load(open(cache))
    else:
        notes = {n["tid"]: n for n in json.load(open(os.path.join(DL, "lakh", "notes.json")))}
        Z = np.load(os.path.join(DL, "lakh", "chroma.npz")); MI = json.load(open(os.path.join(DL, "lpd", "midi_info_v2.json")))
        C = {}
        for s in songs:
            per = []
            for tid in s["tids"]:
                tm = MI.get(notes[tid]["md5"], {}).get("tempo")
                d = song_shape(Z[tid], notes[tid]["toks"], int(hashlib.md5(tid.encode()).hexdigest()[:8], 16), tm)
                d["ln_tempo"] = math.log(tm) if tm else np.nan; per.append(d)
            row = {}
            for k in SHAPES:
                v = np.array([p[k] for p in per], float); v = v[np.isfinite(v)]; row[k] = float(v.mean()) if len(v) else None
            row["Pcat"] = None if not np.isfinite(per[0]["Pcat"]) else int(per[0]["Pcat"])
            C[s["key"]] = row
        json.dump(C, open(cache, "w"))
    for s in songs:
        for k, v in C[s["key"]].items(): s[k] = np.nan if v is None else v
    return songs


# ====================================================================== the outcome (post-commit only)
OUT_CACHE = os.path.join(DL, "lakh", "outcomes_run07.json")    # written by the first guarded call, after every PREDICTION.md is pushed

def load_outcomes(songs, folder):
    guard(folder)
    if os.path.exists(OUT_CACHE):
        C = json.load(open(OUT_CACHE))
        for s in songs:
            s.update(C["songs"].get(s["key"], dict(y=0.0, y_foreign=0.0, clique=None, n_sets=None, first_year=None, _sets=[])))
            if s["y_foreign"] is None: s["y_foreign"] = np.nan
        return C["info"]
    Q = json.load(open(os.path.join(SHAPE, "discogs_cliques.json"))); by = collections.defaultdict(list)
    for q in Q: by[q["title"]].append(q)
    hit = {}
    for s in songs:
        c = [q for q in by.get(s["title_key"], []) if s["artist_key"] in q["artists"]]
        if c: hit[s["key"]] = max(c, key=lambda q: q["n_artist_sets"])
    want = {str(q["id"]) for q in hit.values()}; VS = {}
    for line in open(os.path.join(SHAPE, "discogs_versions.jsonl")):
        d = json.loads(line)
        if str(d["id"]) in want: VS[str(d["id"])] = d["sets"]
    drops = 0
    for s in songs:
        s.update(y=0.0, y_foreign=0.0, clique=None, n_sets=None, first_year=None)
        q = hit.get(s["key"])
        if q is None: continue
        s["y"] = 100.0; s["clique"] = q["id"]; s["first_year"] = q["first_year"]
        s["_sets"] = VS.get(str(q["id"]), []); sets = [e[0] for e in s["_sets"]]
        own = [x for x in sets if any(nrm(nm) == s["artist_key"] for nm in x)]
        if not own: s["y_foreign"] = np.nan; drops += 1; continue
        O = {nrm(nm) for x in own for nm in x}
        others = [x for x in sets if len(x) > 0 and not any(nrm(nm) in O for nm in x)]
        s["y_foreign"] = 100.0 if others else 0.0; s["n_sets"] = len(others)
    info = dict(matched=len(hit), dropped=drops, y_foreign1=int(sum((s["y_foreign"] or 0) > 0 for s in songs if np.isfinite(s["y_foreign"]))))
    keep = ("y", "y_foreign", "clique", "n_sets", "first_year", "_sets")
    json.dump(dict(info=info, songs={s["key"]: {k: (None if (k == "y_foreign" and not np.isfinite(s[k])) else s.get(k)) for k in keep} for s in songs}),
              open(OUT_CACHE, "w"))
    return info


# ====================================================================== models
def year_dummies(songs):
    """first-year control: the MSD year in five-year bins (unknown = its own bin); bins as dummies, the first dropped."""
    b = [("u" if not s["year"] else str(min(max(s["year"], 1950), 2010) // 5 * 5)) for s in songs]
    lv = sorted(set(b)); return np.column_stack([[float(x == l) for x in b] for l in lv[1:]]) if len(lv) > 1 else np.zeros((len(b), 0))

def lpm(X, y, g):
    """within-group OLS (group = artist) of y on X, CR1 standard errors clustered by group. Returns b, se, p, N, G."""
    from scipy import stats
    X = np.asarray(X, float); y = np.asarray(y, float); g = np.asarray(g)
    ok = np.isfinite(y) & np.isfinite(X).all(1); X, y, g = X[ok], y[ok], g[ok]
    u, inv = np.unique(g, return_inverse=True); G = len(u)
    def dm(M):
        M = np.atleast_2d(M.T).T.astype(float); S = np.zeros((G, M.shape[1])); np.add.at(S, inv, M)
        c = np.bincount(inv); return M - (S / c[:, None])[inv]
    Xd, yd = dm(X), dm(y[:, None])[:, 0]
    keep = Xd.std(0) > 1e-12; Xd = Xd[:, keep]
    XtX = np.linalg.pinv(Xd.T @ Xd); b = XtX @ Xd.T @ yd; e = yd - Xd @ b
    N, K = Xd.shape; S = np.zeros((G, K)); np.add.at(S, inv, Xd * e[:, None])
    V = XtX @ (S.T @ S) @ XtX * (G / (G - 1)) * ((N - 1) / (N - K - G))
    se = np.sqrt(np.diag(V)); p = 2 * stats.norm.sf(np.abs(b / se))
    bb = np.full(len(keep), np.nan); ss = bb.copy(); pp = bb.copy(); bb[keep], ss[keep], pp[keep] = b, se, p
    return bb, ss, pp, int(N), int(G)

def cond_logit(x, yb, g, Z=None):
    """conditional (fixed-effects) logit sign check via statsmodels; returns (coef on x, p, converged).
    Fixed after the first test ran (run 07, 19:25 ET; the sign-check column only, no rule changed): the frozen version read
    r.mle_retvals, which ConditionalResults does not have, so every call fell into the except branch and returned nan. Now
    convergence is read from statsmodels' ConvergenceWarning; if Newton does not converge, BFGS (maxiter 2000) is tried and used."""
    import warnings
    from statsmodels.discrete.conditional_models import ConditionalLogit
    from statsmodels.tools.sm_exceptions import ConvergenceWarning
    X = np.column_stack([x] + ([Z] if Z is not None and Z.shape[1] else []))
    ok = np.isfinite(yb) & np.isfinite(X).all(1)
    keep = X[ok].std(0) > 1e-12; keep[0] = True
    m = ConditionalLogit(yb[ok], X[ok][:, keep], groups=np.asarray(g)[ok])
    for kw in (dict(), dict(method="bfgs", maxiter=2000)):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try: r = m.fit(disp=0, **kw)
            except Exception: continue
        conv = not any(issubclass(x.category, ConvergenceWarning) for x in w)
        if conv: return float(r.params[0]), float(r.pvalues[0]), True
    try: return float(r.params[0]), float(r.pvalues[0]), False
    except Exception: return float("nan"), float("nan"), False


# ====================================================================== the battery (one design for every test)
BASE = ["ln_chg", "V", "ln_bars"]           # notes-side controls in every model, plus year bins

def zcol(songs, k):
    v = np.array([s[k] for s in songs], float); m, sd = np.nanmean(v), np.nanstd(v)
    return (v - m) / sd

def design(songs, meas, extra=()):
    """columns: z(meas), then z of each extra measure, then BASE (z), then year-bin dummies. Rows with a missing column are dropped
    by lpm(). Returns names, X."""
    cols = [zcol(songs, meas)] + [zcol(songs, e) for e in extra] + [zcol(songs, b) for b in BASE]
    Y = year_dummies(songs)
    return [meas] + list(extra) + BASE + [f"yr{i}" for i in range(Y.shape[1])], np.column_stack(cols + [Y])

def fit(songs, meas, extra=(), outcome="y_foreign", mask=None, add=None):
    names, X = design(songs, meas, extra)
    if add is not None: X = np.column_stack([X, add])
    y = np.array([s[outcome] for s in songs], float); g = np.array([s["artist_key"] for s in songs])
    if mask is not None: X, y, g = X[mask], y[mask], g[mask]
    b, se, p, N, G = lpm(X, y, g)
    return dict(b=float(b[0]), se=float(se[0]), p=float(p[0]), N=N, G=G)

def fake_power(songs, meas, extra, beta, alpha, sign, draws=400, base=0.20, prec=1.25, seed=7):
    """fake outcomes on the real design: artist baselines ~ Beta(base*prec, (1-base)*prec), y ~ Bernoulli(baseline + beta/100 * z).
    Pass = two-sided p < alpha, right sign, right sign in both artist halves. Returns pass rate under beta and under 0, and mean SE."""
    rng = np.random.default_rng(seed); names, X = design(songs, meas, extra)
    g = np.array([s["artist_key"] for s in songs]); hv = np.array([s["half"] for s in songs])
    ok = np.isfinite(X).all(1); X, g, hv = X[ok], g[ok], hv[ok]
    u, inv = np.unique(g, return_inverse=True); z = X[:, 0]
    def one(bb):
        a = rng.beta(base * prec, (1 - base) * prec, len(u))[inv]
        y = 100.0 * (rng.random(len(z)) < np.clip(a + bb / 100 * z, 0, 1))
        r = lpm(X, y, g); good = (r[2][0] < alpha) and np.sign(r[0][0]) == sign
        if good:
            for h in (0, 1):
                m = hv == h; rr = lpm(X[m], y[m], g[m]); good &= np.sign(rr[0][0]) == sign
        return good, r[1][0]
    A = [one(beta) for _ in range(draws)]; Z0 = [one(0.0) for _ in range(draws // 2)]
    return dict(power=float(np.mean([a[0] for a in A])), false_pass=float(np.mean([a[0] for a in Z0])), se=float(np.mean([a[1] for a in A])))

def first_performer_mask(songs):
    """True where the song is unmatched, or matched and the artist is among the performer sets of the clique's earliest dated year
    (R02-3's rule on main). Needs load_outcomes() to have run with versions kept (s['_sets'])."""
    out = []
    for s in songs:
        sets = s.get("_sets")
        if not s.get("clique") or not sets: out.append(True); continue
        ys = [e[1] for e in sets if e[1] is not None]
        if not ys: out.append(True); continue
        y0 = min(ys); out.append(any(e[1] == y0 and any(nrm(nm) == s["artist_key"] for nm in e[0]) for e in sets))
    return np.array(out)

def run_test(folder, songs, meas, extra, pred, sign, alpha, kill, power_beta=None):
    """the one test runner. Order: guard, power (fake outcomes, printed first), outcome, estimate, halves, logit, readings."""
    guard(folder)
    pw = fake_power(songs, meas, extra, power_beta if power_beta is not None else pred, alpha, sign)
    print("POWER (before the estimate):", pw, flush=True)
    info = load_outcomes(songs, folder)
    main = fit(songs, meas, extra)
    halves = [fit(songs, meas, extra, mask=np.array([s["half"] == h for s in songs])) for h in (0, 1)]
    names, X = design(songs, meas, extra)
    yb = np.array([(s["y_foreign"] > 0) if np.isfinite(s["y_foreign"]) else np.nan for s in songs], float)
    cl = cond_logit(X[:, 0], yb, np.array([s["artist_key"] for s in songs]), X[:, 1:])
    hot = np.array([s["hot"] if s["hot"] is not None else np.nan for s in songs], float)
    fame = np.column_stack([[float(s["bb"]) for s in songs], np.nan_to_num(hot, nan=np.nanmean(hot)), np.isnan(hot).astype(float)])
    readings = dict(on_y=fit(songs, meas, extra, outcome="y"), fame_held=fit(songs, meas, extra, add=fame),
                    first_performers=fit(songs, meas, extra, mask=first_performer_mask(songs)))
    passed = main["p"] < alpha and np.sign(main["b"]) == sign and all(np.sign(h["b"]) == sign for h in halves) and np.sign(cl[0]) == sign
    killed = kill(main["b"])
    verdict = "PASS" if passed else ("KILLED" if killed else "UNSETTLED")
    return dict(measure=meas, extra=list(extra), prediction=pred, alpha=alpha, power=pw, outcome_info=info, main=main, halves=halves,
                cond_logit=dict(coef=cl[0], p=cl[1], converged=cl[2]), readings=readings, verdict=verdict,
                base_rate=float(np.nanmean([s["y_foreign"] for s in songs])))
