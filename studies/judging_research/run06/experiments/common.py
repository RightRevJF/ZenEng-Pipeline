"""Run 06 shared code, frozen by the chair before any outcome is joined. Builds on run05/experiments/common.py (imported as C5).

What is new tonight:
  1. Harmonic chirality CH (the Inventor's I1): signed area swept on the circle of fifths by the open chord-root walk.
  2. FRESH SONGS: the 1,946 Hooktheory songs in the raw file that are not in the data pack (rebuilt here from the notes, exactly as
     /tmp/claude-0/r6/fresh_build.py did). Their outcomes have never been joined to anything.
  3. The FRESH OUTCOME: Discogs-VI 20240701 reduced exactly as the maintainer's
     studies/judging_checks/within_artist/cliques_versions.py does (origin/main), into /home/claude/shape/discogs_cliques.json and
     /home/claude/shape/discogs_versions.jsonl, then matched by the maintainer's rule (studies/covers/covers_match_discogs.py on
     origin/main): norm(song slug) == clique title and norm(artist slug) among the clique's artists; among candidates, the clique with
     the most artist sets (first in file order on ties, as max() does). Fresh songs are keyed by (artist slug, song slug).
     y_foreign is run 05's rule (C5.load_outcomes) applied to the clique's version sets.
  4. A VALIDATION step (validate_match) that must pass before any fresh outcome is used: the rebuilt match must reproduce the data
     pack's hooktheory_covers_discogs.json (keys and cliques) and discogs_versions_matched.json (version sets) for >= 99%.

GUARD: every outcome loader here refuses unless the calling folder's PREDICTION.md AND this file are committed and unmodified.
NEVER use studies/judging_data/hooktheory_clips.json.gz for anything: its clip set is the set of matched videos (an outcome).
Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
"""
import os, sys, json, gzip, io, math, re, hashlib, collections, subprocess
import numpy as np
from scipy.sparse.csgraph import connected_components

HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util
_spec = importlib.util.spec_from_file_location("run05_common", os.path.normpath(os.path.join(HERE, "..", "..", "run05", "experiments", "common.py")))
C5 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(C5)   # run 05's shared code, unchanged
r4, zs, sp, lpm, summ, power, cond_logit, controls = C5.r4, C5.zs, C5.sp, C5.lpm, C5.summ, C5.power, C5.cond_logit, C5.controls
chord_pcs, melody_midi, raw_clips, song_measure, toks, FE, gate = C5.chord_pcs, C5.melody_midi, C5.raw_clips, C5.song_measure, C5.toks, C5.FE, C5.gate

N_TESTS = 6                              # counted tests tonight (chair.md); every one needs two-sided p < .05 / 6
ALPHA = 0.05 / N_TESTS                   # .008333, z = 2.638
SHAPE = os.environ.get("DISCOGS_SHAPE", "/home/claude/shape")
nrm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))   # the maintainer's norm(), identical to C5's nrm
half_of = lambda artist: int(hashlib.md5(artist.encode()).hexdigest(), 16) % 2


# ====================================================================== the guard
def _committed_clean(path):
    d, f = os.path.dirname(path), os.path.basename(path)
    if not os.path.exists(path): return False
    out = subprocess.run(["git", "-C", d, "log", "--oneline", "-1", "--", f], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", d, "status", "--porcelain", "--", f], capture_output=True, text=True).stdout.strip()
    return bool(out) and not dirty

def guard(folder, fresh=False):
    need = [os.path.join(folder, "PREDICTION.md"), os.path.join(HERE, "common.py")]
    if fresh: need.append(os.path.join(HERE, "fresh_repetition", "PREDICTION.md"))   # the battery's shared rules live there
    for p in need:
        if not _committed_clean(p):
            raise SystemExit(f"{p} is not committed (or has uncommitted edits): outcome NOT joined")


# ====================================================================== chord walk and tonight's measures (notes only)
def chord_runs(a):
    """harmony events sorted by onset (stable), mapped to C5.chord_pcs; runs of consecutive equal sets collapsed; each run keeps
    the root_pitch_class of its first event. Returns [(pcs, root)], length K + 1."""
    out = []
    for h in sorted(a.get("harmony") or [], key=lambda h: h["onset"]):
        S = chord_pcs(h)
        if not out or out[-1][0] != S: out.append((S, h["root_pitch_class"] % 12))
    return out

def K_of(a): return max(len(chord_runs(a)) - 1, 0)

def theta(root): return 2 * math.pi * ((7 * root) % 12) / 12         # position on the circle of fifths

def CH_clip(a, wrap=False):
    """Harmonic chirality (frozen): CH = (1/K) * sum_{t<K} 1/2 sin(theta_{t+1} - theta_t), open walk (no wrap). nan if K < 6.
    wrap=True adds the move from the last run back to the first (the sensitivity form; reported only)."""
    R = chord_runs(a); K = len(R) - 1
    if K < 6: return np.nan
    th = [theta(r) for _, r in R]
    W = 0.5 * sum(math.sin(th[t + 1] - th[t]) for t in range(K))
    if wrap: W += 0.5 * math.sin(th[0] - th[-1])
    return W / K

def A_clip(a):
    """run 05's arrow of time A (frozen in run05/experiments/arrow_of_time/PREDICTION.md). nan if K < 6."""
    s = [S for S, _ in chord_runs(a)]; K = len(s) - 1
    if K < 6: return np.nan
    n = collections.Counter(zip(s, s[1:]))
    return 1.0 - sum(min(v, n.get((y, x), 0)) for (x, y), v in n.items()) / sum(n.values())

def V_clip(a): return len(set(S for S, _ in chord_runs(a)))           # distinct chord pitch-class sets in the clip

def L2_clip(a, c=None, fold=True):
    """run 05's folded melody range (run05/experiments/melody_range/PREDICTION.md), semitones; nan if fewer than 4 notes."""
    p = sorted(melody_midi(a))
    if len(p) < 4: return np.nan
    q = [p[0][2]]
    for k in range(1, len(p)):
        i = p[k][2] - p[k - 1][2]
        if fold:
            while abs(i) > 12: i -= 12 * int(np.sign(i))
        q.append(q[-1] + i)
    q = np.array(q, float); w = np.array([x[1] - x[0] for x in p], float)
    o = np.argsort(q, kind="stable"); cw = np.cumsum(w[o]) / w.sum()
    return float(q[o][np.searchsorted(cw, 0.95)] - q[o][np.searchsorted(cw, 0.05)])

def D5_clip(a, c=None):
    """R04-G1 diatonicity |a5|/a0 of the duration-weighted chord pc profile (run05/experiments/fifths_path/PREDICTION.md)."""
    v = np.zeros(12)
    for h in a.get("harmony") or []:
        d = h["offset"] - h["onset"]
        if d > 0:
            for p in chord_pcs(h): v[p] += d
    if v.sum() == 0: return np.nan
    return float(abs((v * np.exp(-2j * np.pi * 5 * np.arange(12) / 12)).sum()) / v.sum())

def NT_clip(a, c=None):
    """non-triad share (frozen tonight for fresh_diatonic): share of harmony duration (offset - onset > 0) on events whose
    root_position_intervals are neither (4, 3) nor (3, 4). nan if no duration."""
    tot = non = 0.0
    for h in a.get("harmony") or []:
        d = h["offset"] - h["onset"]
        if d > 0:
            tot += d; non += d * (tuple(h.get("root_position_intervals") or []) not in ((4, 3), (3, 4)))
    return non / tot if tot > 0 else np.nan

# ---- run 03's key-relative tokens (fifths path FP, tonic resistance H); copied from run05's test.py files, unchanged
QUAL = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
def qual(iv): return QUAL.get(tuple(iv or []), 8)

def tokens_rel(a):
    tonic = a["keys"][0]["tonic_pitch_class"] if a.get("keys") else 0; ch = []
    for h in sorted(a.get("harmony") or [], key=lambda h: h["onset"]):
        t = ((h["root_pitch_class"] - tonic) % 12) * 9 + qual(h["root_position_intervals"])
        if not ch or ch[-1] != t: ch.append(t)
    return ch

def _phase(S):
    f = sum(np.exp(-2j * np.pi * 5 * k / 12) for k in S)
    return None if abs(f) < 1e-6 else float(np.angle(f))

def _arc(x, y): d = abs(x - y) % (2 * np.pi); return float(min(d, 2 * np.pi - d))

def fp_runs(a):
    tonic = a["keys"][0]["tonic_pitch_class"] if a.get("keys") else 0; R = []
    for ev in sorted(a.get("harmony") or [], key=lambda c: c["onset"]):
        r = (ev["root_pitch_class"] - tonic) % 12; t = r * 9 + qual(ev["root_position_intervals"])
        if R and R[-1][0] == t: continue
        S = {r} | {int((r + s) % 12) for s in np.cumsum(ev["root_position_intervals"] or [])}
        R.append((t, _phase(S)))
    return R

def fp_steps(a):
    R = fp_runs(a); mv = list(zip(R, R[1:]))
    if len(R) > 1 and R[-1][0] != R[0][0]: mv.append((R[-1], R[0]))
    return [_arc(x[1], y[1]) for x, y in mv if x[1] is not None and y[1] is not None]

def FP_song(annots):
    """run 05's fifths path: plain mean of the kept steps of all the song's clips pooled; nan if none."""
    st = [s for a in annots for s in fp_steps(a)]
    return float(np.mean(st)) if st else np.nan

def _resist(W):
    Qd = np.linalg.pinv(np.diag(W.sum(1)) - W); d = np.diag(Qd)
    return d[:, None] + d[None, :] - 2 * Qd

def H_song(seqs):
    """run 05's tonic resistance (run05/experiments/tonic_resistance/PREDICTION.md). Returns (H or nan, distinct tokens n, links)."""
    names = sorted(set(t for s in seqs for t in s)); ix = {t: i for i, t in enumerate(names)}; M = np.zeros((len(names), len(names)))
    for s in seqs:
        for x, y in zip(s, s[1:]): M[ix[x], ix[y]] += 1
        if len(s) > 1 and s[-1] != s[0]: M[ix[s[-1]], ix[s[0]]] += 1
    n = len(names); Cm = M + M.T; np.fill_diagonal(Cm, 0); links = int((np.triu(Cm, 1) > 0).sum())
    if n < 3: return np.nan, n, links
    cand = [i for i, t in enumerate(names) if t // 9 == 0]
    if not cand: return np.nan, n, links
    rs = Cm.sum(1); T = min(cand, key=lambda i: (-rs[i], names[i]))
    _, lab = connected_components(Cm > 0, directed=False); idx = np.nonzero(lab == lab[T])[0]
    if len(idx) < 3: return np.nan, n, links
    Cs = Cm[np.ix_(idx, idx)]; t = int(np.nonzero(idx == T)[0][0]); om = _resist(Cs); pi = Cs.sum(1) / Cs.sum()
    return float(pi @ om[:, t] / (pi @ om @ pi)), n, links

# ---- the data pack's chord and melody tokens (studies/surprise; reproduced exactly by /tmp/claude-0/r6/surp.py, copied here)
IB = [(-99, -5), (-4, -3), (-2, -1), (0, 0), (1, 2), (3, 4), (5, 99)]
def _ib(i): return next(k for k, (x, y) in enumerate(IB) if x <= i <= y)
def pack_tokens(a):
    tonic = a["keys"][0]["tonic_pitch_class"] if a.get("keys") else 0
    mel = []; prev = None
    for n in sorted(a.get("melody") or [], key=lambda n: n["onset"]):
        p = 12 * n["octave"] + n["pitch_class"]; sd = (n["pitch_class"] - tonic) % 12
        mel.append(sd * 7 + (_ib(p - prev) if prev is not None else 3)); prev = p
    ch = []
    for c in sorted(a.get("harmony") or [], key=lambda c: c["onset"]):
        t = ((c["root_pitch_class"] - tonic) % 12) * 9 + qual(c["root_position_intervals"])
        if not ch or ch[-1] != t: ch.append(t)
    return mel, ch

def repetition(s, n=3):
    seen = set(); rep = 0; tot = 0
    for i in range(len(s) - n + 1):
        g = tuple(s[i:i + n]); tot += 1
        if g in seen: rep += 1
        seen.add(g)
    return rep / tot if tot else 0.0


# ====================================================================== song values
def k_weighted(r, fn):
    """mean of fn(annotations) over the song's clips with a finite value, weighted by each clip's K; also the clip-1 / clip-2 pair."""
    R = raw_clips(); vals, ws = [], []
    for c in r["clips"]:
        a = R[c["k"]]; vals.append(fn(a)); ws.append(K_of(a))
    vals, ws = np.array(vals, float), np.array(ws, float); ok = np.isfinite(vals)
    v = float(np.average(vals[ok], weights=ws[ok])) if ok.any() and ws[ok].sum() > 0 else (float(np.mean(vals[ok])) if ok.any() else np.nan)
    return v, ((vals[0], vals[1]) if len(vals) >= 2 and np.isfinite(vals[:2]).all() else None)

def add_measures(rows, which=("CH", "A", "V", "ln_chg", "L2", "D5", "NT", "FP", "H")):
    """Adds tonight's song values to each row (seen or fresh, by the same code). r['clips'] = clip records with 'k' and 'n_mel'."""
    R = raw_clips()
    for r in rows:
        an = [R[c["k"]] for c in r["clips"]]; Ks = [K_of(a) for a in an]
        if "CH" in which:
            r["CH"], r["CH_c12"] = k_weighted(r, CH_clip); r["CH_wrap"], r["CH_wrap_c12"] = k_weighted(r, lambda a: CH_clip(a, True))
        if "A" in which: r["A"], r["A_c12"] = k_weighted(r, A_clip)
        if "V" in which:
            v = np.array([V_clip(a) for a in an], float); w = np.array(Ks, float)
            r["V"] = float(np.average(v, weights=w)) if w.sum() > 0 else float(np.mean(v))
        if "ln_chg" in which: r["ln_chg"] = float(np.log(max(sum(Ks), 1)))
        if "FP" in which: r["FP"] = FP_song(an)
        if "H" in which: r["H"], r["n_tok"], r["links"] = H_song([tokens_rel(a) for a in an])
    for nm, fn in (("L2", L2_clip), ("D5", D5_clip), ("NT", NT_clip)):
        if nm in which: song_measure(rows, fn, nm)                          # n_mel-weighted, plain mean if all weights are zero
    if "L2" in which:   # fresh_range only: a 5th-95th percentile range above 36 semitones (three octaves) is a transcription artefact, not a sung range
        for r in rows: r["L2c"] = r["L2"] if np.isfinite(r["L2"]) and r["L2"] <= L2_CAP else np.nan
    return rows

L2_CAP = 36


# ====================================================================== fresh songs (notes only)
def fresh_songs(verbose=True):
    """The fresh songs, rebuilt as /tmp/claude-0/r6/fresh_build.py built them: raw clips (file order) whose clip id is not a data-pack
    clip, whose YouTube id is not a pack video and whose (artist, song) slug pair is not a pack pair; grouped by (artist, song).
    Asserts 1,946 songs and 2,570 clips."""
    S = json.load(gzip.open(io.BytesIO(C5.GIT("hooktheory_surprise.json.gz"))))
    pv = {c["vid"] for c in S}; pk = {c["k"] for c in S}; pas = {(c["artist"], c["song"]) for c in S}
    b = open(C5.RAW, "rb").read(); assert hashlib.sha256(b).hexdigest() == C5.RAW_SHA256
    D = json.load(gzip.open(io.BytesIO(b))); fresh = collections.OrderedDict()
    for k, c in D.items():
        if k in pk: continue
        yt = (c.get("youtube") or {}).get("id"); key = (c["hooktheory"]["artist"], c["hooktheory"]["song"])
        if yt in pv or key in pas: continue
        f = fresh.setdefault(key, dict(artist=key[0], song=key[1], vids=set(), clip_ids=[]))
        if yt: f["vids"].add(yt)
        f["clip_ids"].append(k)
    out = [dict(f, vids=sorted(f["vids"])) for f in fresh.values()]
    assert len(out) == 1946 and sum(len(f["clip_ids"]) for f in out) == 2570, (len(out), sum(len(f["clip_ids"]) for f in out))
    if verbose: print(f"fresh songs: {len(out)} [1,946], clips {sum(len(f['clip_ids']) for f in out)} [2,570], with a video id {sum(1 for f in out if f['vids'])} [1,765]", flush=True)
    return out

def fresh_rows(seen_allsongs, verbose=True):
    """Fresh songs as rows built like run 04's rows. A fresh clip counts only if it has at least one harmony event (every data-pack
    clip has one); songs with no such clip are dropped. Songs whose (norm artist, norm song) equals a seen song's are dropped
    (duplicates under another slug). Per clip: n_mel = number of melody notes, n_ch = number of pack chord tokens, beats = num_beats,
    ch_rep = repetition(pack chord tokens, 3): the pack's own definitions, checked to reproduce the pack on every seen clip.
    Song values: n_mel-weighted means (plain mean if all n_mel are 0), as C5.load_rows does."""
    R = raw_clips(); seen_pairs = {(nrm(r["artist"]), nrm(r["slug"])) for r in seen_allsongs}
    rows, drop = [], collections.Counter()
    for f in fresh_songs(verbose):
        cl = []
        for k in f["clip_ids"]:
            a = R[k]
            if not (a.get("harmony") or []): continue
            mel, ch = pack_tokens(a)
            cl.append(dict(k=k, n_mel=len(mel), n_ch=len(ch), beats=a.get("num_beats"), ch_rep=repetition(ch, 3)))
        if not cl: drop["no clip with harmony"] += 1; continue
        if (nrm(f["artist"]), nrm(f["song"])) in seen_pairs: drop["same normalised artist and title as a seen song"] += 1; continue
        w = np.array([c["n_mel"] for c in cl], float)
        avg = (lambda v: float(np.average(v, weights=w))) if w.sum() > 0 else (lambda v: float(np.mean(v)))
        u, t = toks(f["song"])
        r = dict(n_ch=avg([c["n_ch"] for c in cl]), beats=avg([c["beats"] for c in cl]), ch_rep=avg([c["ch_rep"] for c in cl]),
                 vid=None, vids=f["vids"], artist=f["artist"], slug=f["song"], nclips=len(cl), u=u, tokens=t, key="-".join(t), clips=cl,
                 has_mel=float(w.sum() > 0), fresh=1)
        rows.append(r)
    if verbose: print(f"fresh rows: {len(rows)}; dropped {dict(drop)}", flush=True)
    return rows, dict(drop)

def battery(verbose=True):
    """Seen + fresh rows for the fresh tests: every song (seen: the data pack's 13,198; fresh: fresh_rows) by an artist with at least
    one fresh row and at least two rows in total. Title flag rep_title is recomputed over all seen + fresh songs. Returns dict."""
    L = C5.load_rows(verbose=verbose); seen_all = L["allsongs"]
    for r in seen_all: r.update(fresh=0, has_mel=1.0, vids=[r["vid"]])
    fr, fdrop = fresh_rows(seen_all, verbose)
    keyart = collections.defaultdict(set)
    for r in seen_all + fr: keyart[r["key"]].add(r["artist"])
    for r in seen_all + fr: r["rep_title_all"] = len(keyart[r["key"]]) >= 2
    nf = collections.Counter(r["artist"] for r in fr); nall = collections.Counter(r["artist"] for r in seen_all + fr)
    rows = [r for r in seen_all + fr if nf[r["artist"]] >= 1 and nall[r["artist"]] >= 2]
    for r in rows: r["half"] = half_of(r["artist"])
    if verbose:
        f_ = [r for r in rows if r["fresh"]]
        print(f"battery: {len(rows)} rows = {len(rows) - len(f_)} seen + {len(f_)} fresh, {len(set(r['artist'] for r in rows))} artists", flush=True)
    return dict(rows=rows, seen_rows=L["rows"], seen_all=seen_all, fresh_rows=fr, fresh_drops=fdrop)

def battery_controls(rows):
    """Run 04's block computed identically for seen and fresh rows (rep_title over seen + fresh), plus ln_chg, V, has_mel and the fresh
    main effect. ch_ic_mean / mel_ic_mean are NOT used: they come from the pack's corpus models and cannot be computed identically."""
    saved = [r.get("rep_title") for r in rows]
    for r in rows: r["rep_title"] = r["rep_title_all"]
    names, X = controls(rows)
    for r, s in zip(rows, saved): r["rep_title"] = s
    extra = dict(ln_chg=[r["ln_chg"] for r in rows], V=[r["V"] for r in rows], has_mel=[r["has_mel"] for r in rows], fresh=[float(r["fresh"]) for r in rows])
    return names + list(extra), np.column_stack([X] + [np.asarray(v, float) for v in extra.values()])

def seen_sd(seen_rows, name):
    """mean and population SD of a measure over run 04's 9,588 within-artist seen rows that have a value (tonight's per-SD scale)."""
    v = np.array([r[name] for r in seen_rows], float); v = v[np.isfinite(v)]
    return float(v.mean()), float(v.std())


# ====================================================================== the outcome (post-commit only)
def _cliques():
    Q = json.load(open(os.path.join(SHAPE, "discogs_cliques.json"))); by = collections.defaultdict(list)
    for q in Q: by[q["title"]].append(q)
    return Q, by

def match(a_norm, s_norm, by):
    """the maintainer's rule: candidates with title == s and a among artists; the one with the most artist sets (first on ties)."""
    cands = [q for q in by.get(s_norm, []) if a_norm in q["artists"]]
    return max(cands, key=lambda q: q["n_artist_sets"]) if cands else None

def _sets(ids):
    want = {str(i) for i in ids}; VS = {}
    for line in open(os.path.join(SHAPE, "discogs_versions.jsonl")):
        d = json.loads(line)
        if str(d["id"]) in want: VS[str(d["id"])] = d["sets"]
    return VS

def y_foreign_of(artist, sets):
    """run 05's rule (C5.load_outcomes): own sets = those holding a name equal to norm(artist); y_foreign = 100 if some non-empty set
    shares no name with the own sets. Returns (value or nan, drop reason)."""
    names = [e[0] for e in sets]; a = nrm(artist)
    own = [s for s in names if any(nrm(nm) == a for nm in s)]
    if not own: return np.nan, "no own set"
    O = {nrm(nm) for s in own for nm in s}
    return (100.0 if [s for s in names if len(s) > 0 and not any(nrm(nm) in O for nm in s)] else 0.0), None

VALID_FILE = os.path.join(HERE, "match_validation.json")

def validate_match(folder):
    """MUST pass before any fresh outcome is used. Rebuilds the vid-keyed match over the raw Hooktheory file exactly as
    covers_match_discogs.py does (one entry per YouTube id; the last clip's slugs win), and compares with the data pack:
      (1) keys: |pack & rebuilt| / |pack | rebuilt| >= 0.99;  (2) cliques equal on >= 99% of the common keys;
      (3) version sets: for >= 99% of the pack's matched cliques, the set of normalised performer sets equals the rebuilt one;
      (4) y_foreign of the 13,198 seen songs, pack route (C5.load_outcomes) vs rebuilt route: equal for >= 99%.
    Writes match_validation.json (with up to 50 listed differences each). Returns the dict; 'passed' decides."""
    guard(folder, fresh=True)
    if os.path.exists(VALID_FILE):
        v = json.load(open(VALID_FILE))
        if v.get("cliques_sha256") == _sha(os.path.join(SHAPE, "discogs_cliques.json")): return v
    Q, by = _cliques()
    D = json.load(gzip.open(io.BytesIO(open(C5.RAW, "rb").read()))); songs = {}
    for c in D.values():
        yt = (c.get("youtube") or {}).get("id")
        if yt: songs[yt] = (nrm(c["hooktheory"]["artist"]), nrm(c["hooktheory"]["song"]))
    reb = {}
    for vid, (a, s) in songs.items():
        q = match(a, s, by)
        if q: reb[vid] = dict(clique=str(q["id"]), covers=q["n_artist_sets"] - 1, first_year=q["first_year"])
    CV = json.loads(C5.GIT("hooktheory_covers_discogs.json")); VC = json.loads(C5.GIT("discogs_versions_matched.json"))["cliques"]
    kp, kr = set(CV), set(reb); inter = kp & kr
    jac = len(inter) / max(len(kp | kr), 1)
    same_cq = [v for v in inter if str(CV[v]["clique"]) == reb[v]["clique"]]
    VS = _sets(set(VC) | {reb[v]["clique"] for v in reb})
    norm_sets = lambda L: sorted({tuple(sorted(nrm(n) for n in e[0])) for e in L})
    vs_same = [cq for cq in VC if str(cq) in VS and norm_sets(VC[cq]["versions"]) == norm_sets(VS[str(cq)])]
    L = C5.load_rows(verbose=False); seen = L["allsongs"]
    C5.load_outcomes(seen, folder); agree = 0; ydiff = []
    for r in seen:
        q = reb.get(r["vid"])
        yr, _ = (y_foreign_of(r["artist"], VS.get(q["clique"], [])) if q else (0.0, None))
        yp = r["y_foreign"]
        if (np.isnan(yp) and np.isnan(yr)) or yp == yr: agree += 1
        else: ydiff.append([r["vid"], r["artist"], r["slug"], yp, yr])
    v = dict(cliques_sha256=_sha(os.path.join(SHAPE, "discogs_cliques.json")), versions_sha256=_sha(os.path.join(SHAPE, "discogs_versions.jsonl")),
             n_cliques=len(Q), pack_keys=len(kp), rebuilt_keys=len(kr), common_keys=len(inter), key_jaccard=r4(jac),
             only_pack=sorted(kp - kr)[:50], only_rebuilt=sorted(kr - kp)[:50], clique_agree=r4(len(same_cq) / max(len(inter), 1)),
             clique_diff=[[x, CV[x]["clique"], reb[x]["clique"]] for x in sorted(inter) if str(CV[x]["clique"]) != reb[x]["clique"]][:50],
             covers_agree=r4(np.mean([CV[x].get("covers") == reb[x]["covers"] for x in inter])) if inter else None,
             version_sets_agree=r4(len(vs_same) / max(len(VC), 1)), version_sets_diff=sorted(set(VC) - set(vs_same))[:50],
             seen_y_foreign_agree=r4(agree / len(seen)), seen_y_foreign_diff=ydiff[:50], seen_songs=len(seen))
    v["passed"] = bool(jac >= 0.99 and v["clique_agree"] >= 0.99 and v["version_sets_agree"] >= 0.99 and v["seen_y_foreign_agree"] >= 0.99)
    json.dump(v, open(VALID_FILE, "w"), indent=1, default=str)
    print("MATCH VALIDATION:", json.dumps({k: v[k] for k in v if not isinstance(v[k], list)}), flush=True)
    return v

def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def load_battery_outcomes(rows, folder):
    """Refuses unless PREDICTION.md and this file are committed, and unless validate_match passed. Seen rows: y, y_foreign, versions,
    first_year from the data pack via C5.load_outcomes. Fresh rows: the maintainer's match keyed by (norm artist slug, norm song slug)
    on the rebuilt cliques, y = 100 if matched, y_foreign by run 05's rule on the clique's version sets (nan if no own set).
    Each fresh row also gets 'clique', 'versions' (sets) and 'first_year'; 'clique_seen' = its clique is also matched by a seen song."""
    guard(folder, fresh=True)
    v = validate_match(folder)
    if not v["passed"]: raise SystemExit("match validation FAILED: the fresh tests stop; no fresh outcome is used")
    seen = [r for r in rows if not r["fresh"]]; fresh = [r for r in rows if r["fresh"]]
    LO = C5.load_outcomes(seen, folder)
    CV = json.loads(C5.GIT("hooktheory_covers_discogs.json")); seen_cq = {str(x["clique"]) for x in CV.values()}
    Q, by = _cliques(); hit = {}
    for r in fresh:
        q = match(nrm(r["artist"]), nrm(r["slug"]), by); hit[id(r)] = q
    VS = _sets({q["id"] for q in hit.values() if q})
    for r in fresh:
        q = hit[id(r)]
        r.update(y=0.0, y_foreign=0.0, clique=None, versions=None, first_year=None, drop_reason=None, clique_seen=False)
        if q is None: continue
        cq = str(q["id"]); r.update(y=100.0, clique=cq, first_year=q["first_year"], versions=VS.get(cq, []), clique_seen=cq in seen_cq)
        r["y_foreign"], r["drop_reason"] = y_foreign_of(r["artist"], r["versions"])
    yf = [r["y_foreign"] for r in fresh]
    wv = [r for r in fresh if r["vids"]]   # printed, deciding nothing: the slug-keyed match against the pack's vid-keyed file
    vid_in = [any(v in CV for v in r["vids"]) for r in wv]
    return dict(seen=LO, validation_passed=True, fresh_rows=len(fresh), fresh_y1=int(sum(r["y"] > 0 for r in fresh)),
                fresh_with_vid=len(wv), fresh_vid_in_pack_covers_file=int(sum(vid_in)),
                fresh_slug_vs_vid_agree=r4(np.mean([(r["y"] > 0) == b for r, b in zip(wv, vid_in)])) if wv else None,
                fresh_y_foreign1=int(np.nansum([x > 0 for x in yf if np.isfinite(x)])), fresh_nan=int(sum(1 for x in yf if not np.isfinite(x))),
                fresh_clique_seen=int(sum(r["clique_seen"] for r in fresh)))

def early_late(r):
    """W01-J6a (reported only): foreign performer sets dated within 5 years of the clique's first year, and after 10 years.
    Versions: pack entries [names, year, ...] or rebuilt sets [names, year, releases]; same layout."""
    if not r.get("versions") or r.get("first_year") is None: return (0.0, 0.0) if not r.get("y") else (np.nan, np.nan)
    a = nrm(r["artist"]); names = [e[0] for e in r["versions"]]
    own = [s for s in names if any(nrm(n) == a for n in s)]
    if not own: return np.nan, np.nan
    O = {nrm(n) for s in own for n in s}; fy = r["first_year"]
    fo = [e for e in r["versions"] if len(e[0]) > 0 and not any(nrm(n) in O for n in e[0])]
    return (100.0 * any(e[1] is not None and e[1] <= fy + 5 for e in fo), 100.0 * any(e[1] is not None and e[1] > fy + 10 for e in fo))


# ====================================================================== the fresh model
def fresh_design(rows, meas, seen_rows, extra_cols=None):
    """Columns: z_fresh = z(x) * fresh, z_seen = z(x) * (1 - fresh), z scaled by the mean and SD over the 9,588 seen rows; then any
    measure-specific extra columns (dict name -> array); then battery_controls (which include the fresh main effect).
    Coefficient 0 (z_fresh) is the tested slope: it is identified by fresh outcomes only."""
    mu, sd = seen_sd(seen_rows, meas)
    x = (np.array([r[meas] for r in rows], float) - mu) / sd; f = np.array([float(r["fresh"]) for r in rows])
    cols = {"z_fresh": x * f, "z_seen": x * (1 - f)}
    if extra_cols: cols.update(extra_cols)
    cn, cx = battery_controls(rows)
    return list(cols) + cn, np.column_stack([np.asarray(v, float) for v in cols.values()] + [cx]), (mu, sd)
