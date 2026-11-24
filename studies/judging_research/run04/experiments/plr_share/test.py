"""Run 04, PLR share: the share of a song's chord moves that are P, L or R moves (the three nearest triads on Amiot's flat torus of
phases (phi3, phi5)), against covers within each artist's own songs. The rule is PREDICTION.md in this folder (commit 00ab557), frozen
before this script was written. Rows, chord token, merging, wrap rule, data-pack measures, within() model, CR1 clustered SE and md5
halves are copied from ../../../run03/experiments/fifths_path/test.py (and its sources), except where PREDICTION.md says otherwise:
  - the song list is the set of `video` values of hooktheory_clips.json.gz (not the key set of the covers file);
  - the threshold is p < .05/5 = .01, two-sided (z 2.5758);
  - the clustered SE is the CR1 formula of run03/experiments/bridge/PREDICTION.md, computed by hand
    (statsmodels' cluster SE with df_correction is printed alongside as a check only).

Order (printed as it goes):
  1. unit values (must reproduce the card), the 36-pair check, the stretched-phi5 check, and the five loops;
  2. songs from the notes only; PLR, TS (and FP, D3 for printing) per song;
  3. THE GATE, before any outcome-side field: clip 1 vs clip 2 Spearman >= 0.20; |Spearman| <= 0.7 with the 17 data-pack measures,
     distinct chords, links and clips. If it fails: result.json records "stopped" and the covers file is never opened.
  4. only if the gate passes: hooktheory_covers_discogs.json (covers, first_year), artists with 2+ songs; SE and power printed
     before beta; halves; the verdict by the frozen rule; the items reported deciding nothing.

Data: origin/main:studies/judging_data/ read straight from git (read only; nothing written there).
python3 studies/judging_research/run04/experiments/plr_share/test.py -> result.json in this folder
(NOTES_ONLY=1 stops after the gate without opening the covers file; it was used once, before the full run, to check the notes side.)
"""
import json, gzip, collections, re, hashlib, os, sys, time, subprocess, itertools
import numpy as np
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
def data(name):
    """one file of origin/main:studies/judging_data/, read from git (bytes)"""
    return subprocess.run(["git", "-C", REPO, "show", f"origin/main:studies/judging_data/{name}"], capture_output=True, check=True).stdout
def jload(name): b = data(name); return json.loads(gzip.decompress(b) if name.endswith(".gz") else b)

RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF   # the 17 of study_covers_discogs.py
ALPHA = 0.05 / 5; ZC = float(N.ppf(1 - ALPHA / 2)); PRED = 0.02; CUT = 1.25
OUT = dict(rule="PREDICTION.md, commit 00ab557", alpha=ALPHA, z_crit=round(ZC, 4), prediction=PRED, plr_cut=CUT)
r4 = lambda x: round(float(x), 4)

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item())
    print("VERDICT:", verdict, flush=True); sys.exit(0)

# ---------------------------------------------------------------- measure
def qual(iv):   # copied from studies/surprise/surprise_hooktheory.py (origin/main), via run 03
    iv = tuple(iv)
    Q = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
    return Q.get(iv, 8)

def ph(S, n):
    """angle of a_n(S) = sum_k exp(-2 pi i n k / 12); None if |a_n| < 1e-6"""
    f = sum(np.exp(-2j * np.pi * n * k / 12) for k in S)
    return None if abs(f) < 1e-6 else float(np.angle(f))

def pcset(ev, tonic):
    r = (ev["root_pitch_class"] - tonic) % 12
    return {r} | {int((r + s) % 12) for s in np.cumsum(ev["root_position_intervals"] or [])}

def runs_of(clip):
    """merged runs (consecutive equal run-03 tokens); each run's tonic-relative pitch-class set from its first event -> (token, phi3, phi5)"""
    tonic = clip["keys"][0]["tonic_pitch_class"] if clip.get("keys") else 0; R = []
    for ev in sorted(clip.get("harmony") or [], key=lambda c: c["onset"]):
        t = ((ev["root_pitch_class"] - tonic) % 12) * 9 + qual(ev["root_position_intervals"])
        if R and R[-1][0] == t: continue
        S = pcset(ev, tonic)
        R.append((t, ph(S, 3), ph(S, 5)))
    return R

w = lambda x: ((x + np.pi) % (2 * np.pi)) - np.pi
def step(x, y, k5=1.0): return float(np.sqrt(w(y[1] - x[1]) ** 2 + (k5 * w(y[2] - x[2])) ** 2))
def arc(a, b): d = abs(a - b) % (2 * np.pi); return float(min(d, 2 * np.pi - d))   # run 03's FP step, for printing only

def clip_moves(clip):
    """run 03's moves: consecutive runs, plus the wrap last -> first when tokens differ.
    returns (kept steps, n moves, n skipped for an undefined phase, n skipped for s < 1e-9, FP steps (f5 defined))"""
    R = runs_of(clip); mv = list(zip(R, R[1:]))
    if len(R) > 1 and R[-1][0] != R[0][0]: mv.append((R[-1], R[0]))
    kept = []; und = zer = 0; fps = []
    for x, y in mv:
        if x[2] is not None and y[2] is not None: fps.append(arc(x[2], y[2]))
        if None in (x[1], x[2], y[1], y[2]): und += 1; continue
        s = step(x, y)
        if s < 1e-9: zer += 1; continue
        kept.append(s)
    return kept, len(mv), und, zer, fps

def plr_ts(steps): return (float(np.mean([s < CUT for s in steps])), float(np.mean(steps))) if steps else (None, None)

def d3_clip(clip):
    """thirds_axis D3 of one clip (../thirds_axis/PREDICTION.md), for printing only"""
    v = np.zeros(12)
    for ev in clip.get("harmony") or []:
        d = ev["offset"] - ev["onset"]
        if d > 0:
            for x in pcset(ev, 0): v[x] += d
    if v.sum() == 0: return None
    return float(abs(sum(v[x] * np.exp(-2j * np.pi * 3 * x / 12) for x in range(12))) / v.sum())

def fake_clip(chords):   # chords: list of (root relative to C, root_position_intervals), tonic C, one beat each
    return dict(keys=[dict(tonic_pitch_class=0)], harmony=[dict(root_pitch_class=r, root_position_intervals=iv, onset=i, offset=i + 1) for i, (r, iv) in enumerate(chords)])

# ---------------------------------------------------------------- 1. unit values, 36 pairs, stretch check, loops
MAJ, MIN = [4, 3], [3, 4]
NAME = {"C": (0, MAJ), "Am": (9, MIN), "Cm": (0, MIN), "Em": (4, MIN), "F": (5, MAJ), "G": (7, MAJ), "Fm": (5, MIN), "D": (2, MAJ)}
pt = lambda c: runs_of(fake_clip([c]))[0]
UNIT = [("C", "Am", 1.065), ("C", "Cm", 1.229), ("C", "Em", 1.229), ("C", "F", 1.656), ("C", "G", 1.656), ("C", "Fm", 1.824), ("Cm", "D", 3.26)]
unit = {}
for x, y, want in UNIT:
    got = step(pt(NAME[x]), pt(NAME[y])); unit[f"d({x},{y})"] = dict(want=want, got=r4(got))
    print(f"unit d({x},{y}) = {got:.4f} (want {want})"); assert abs(got - want) < 0.0051, (x, y, got)
TRI = [(r, q) for r in range(12) for q in (MAJ, MIN)]; P = [pt(c) for c in TRI]
def relatives(a, b):   # P, L or R: same / opposite quality sharing two tones
    (ra, qa), (rb, qb) = a, b
    if qa == qb: return False
    sa = pcset(dict(root_pitch_class=ra, root_position_intervals=qa), 0); sb = pcset(dict(root_pitch_class=rb, root_position_intervals=qb), 0)
    return len(sa & sb) == 2
pairs = list(itertools.combinations(range(24), 2))
near = {(i, j) for i, j in pairs if step(P[i], P[j]) < CUT}
near_s = {(i, j) for i, j in pairs if step(P[i], P[j], 0.7365) < CUT}
plr_pairs = {(i, j) for i, j in pairs if relatives(TRI[i], TRI[j])}
ds = sorted({round(step(P[i], P[j]), 4) for i, j in pairs})
print(f"unit: {len(near)} of 276 triad pairs below {CUT} (want 36); same set with phi5 x 0.7365: {near == near_s}; equal to the P/L/R pairs: {near == plr_pairs}; "
      f"smallest distances {ds[:4]}", flush=True)
assert len(near) == 36 and near == near_s and near == plr_pairs
unit.update(pairs_below_cut=len(near), same_pairs_with_phi5_stretched_0_7365=near == near_s, pairs_are_exactly_PLR=near == plr_pairs, smallest_distances=ds[:4])
RN = dict(I=(0, MAJ), V=(7, MAJ), vi=(9, MIN), IV=(5, MAJ), iii=(4, MIN))
LOOPS = [("I-V-vi-IV", 0.25, 1.760), ("I-IV-V", 0.0, 2.208), ("I-vi", 1.0, 1.065), ("IV-V", 0.0, 3.312), ("I-iii-vi-IV", 0.50, 1.442)]
loops = {}
for name, wp, wt in LOOPS:
    prog = name.split("-"); kept, nm, _, _, _ = clip_moves(fake_clip([RN[c] for c in prog])); p_, t_ = plr_ts(kept)
    labels = [f"{a}->{b}" for a, b in zip(prog, prog[1:] + prog[:1])][:nm]
    loops[name] = dict(steps={l: r4(s) for l, s in zip(labels, kept)}, PLR=r4(p_), TS=r4(t_))
    print(f"loop {name}: " + ", ".join(f"{l} {s:.3f}{'*' if s < CUT else ''}" for l, s in zip(labels, kept)) + f" -> PLR {p_:.2f} (want {wp}), TS {t_:.3f} (want {wt})")
    assert abs(p_ - wp) < 1e-9 and abs(t_ - wt) < 0.0006, name
OUT["unit_values"] = unit; OUT["loops"] = loops

# ---------------------------------------------------------------- 2. songs from the notes only (the covers file is not opened here)
CL = jload("hooktheory_clips.json.gz")["clips"]
S = jload("hooktheory_surprise.json.gz")
RH = {r["k"]: r for r in jload("hooktheory_rhythm.json.gz")}
SONGS = {c["video"] for c in CL.values()}   # PREDICTION: the `video` values of the clips file
by = collections.defaultdict(list)          # a song's clips, in surprise-file order
for c in S:
    if c["k"] in CL and c["k"] in RH and CL[c["k"]]["video"] in SONGS:
        assert CL[c["k"]]["video"] == c["vid"]
        by[c["vid"]].append(dict(c, **{f: RH[c["k"]][f] for f in RF}))

rows_all = []; undefined = 0; n_moves = n_und = n_zer = n_kept = 0
for vid, cs in by.items():
    seqs = [[t for t, _, _ in runs_of(CL[c["k"]])] for c in cs]
    nodes = sorted({t for s in seqs for t in s})
    if len(nodes) < 3: continue
    links = set()
    for s in seqs:
        mv = list(zip(s, s[1:])) + ([(s[-1], s[0])] if len(s) > 1 and s[-1] != s[0] else [])
        links |= {frozenset(m) for m in mv if m[0] != m[1]}
    per = [clip_moves(CL[c["k"]]) for c in cs]
    allst = [x for p in per for x in p[0]]
    n_moves += sum(p[1] for p in per); n_und += sum(p[2] for p in per); n_zer += sum(p[3] for p in per); n_kept += len(allst)
    if not allst: undefined += 1; continue
    wts = np.array([c["n_mel"] for c in cs], float)
    r = {f: float(np.average([c[f] for c in cs], weights=wts)) for f in FE}
    PLR, TS = plr_ts(allst)
    fps = [x for p in per for x in p[4]]
    d3s = [d for d in (d3_clip(CL[c["k"]]) for c in cs) if d is not None]
    cp = [plr_ts(p[0])[0] for p in per]
    r.update(vid=vid, artist=cs[0]["artist"], nclips=len(cs), nchords=len(nodes), nlinks=len(links), PLR=PLR, TS=TS,
             FP=float(np.mean(fps)) if fps else np.nan, D3=float(np.mean(d3s)) if d3s else np.nan,
             clip1=cp[0], clip2=cp[1] if len(cp) > 1 else None)
    rows_all.append(r)
plr = np.array([r["PLR"] for r in rows_all]); pct = np.percentile(plr, (10, 50, 90))
print(f"[{time.time() - T0:.0f}s] songs (clips-file videos) with >= 3 distinct tokens: {len(rows_all) + undefined} (chair 2,672); PLR undefined: {undefined} (chair 0)", flush=True)
print(f"  moves: {n_moves}; skipped for an undefined phase: {n_und} (chair 1,801 of 60,579); skipped for s < 1e-9: {n_zer} (chair 37); kept {n_kept}", flush=True)
print(f"  PLR 10th / 50th / 90th: {pct[0]:.2f} / {pct[1]:.2f} / {pct[2]:.2f} (chair 0.00 / 0.22 / 0.50); share of songs with PLR = 0: {np.mean(plr == 0):.3f}", flush=True)
OUT["shape"] = dict(songs=len(rows_all), plr_undefined=undefined, moves=n_moves, moves_skipped_undefined_phase=n_und, moves_skipped_zero_step=n_zer,
                    moves_kept=n_kept, PLR_p10_p50_p90=[r4(x) for x in pct], share_zero_PLR_songs_all=r4(np.mean(plr == 0)))

# ---------------------------------------------------------------- 3. THE GATE (no outcome-side field has been read)
cpairs = [(r["clip1"], r["clip2"]) for r in rows_all if r["nclips"] >= 2 and r["clip1"] is not None and r["clip2"] is not None]
rho12 = float(spearmanr([p[0] for p in cpairs], [p[1] for p in cpairs])[0])
ALSO = [(f, f) for f in FE] + [("distinct chords", "nchords"), ("links", "nlinks"), ("clips", "nclips")]
ov = {lab: float(spearmanr(plr, [r[k] for r in rows_all])[0]) for lab, k in ALSO}
top = max(ov, key=lambda k: abs(ov[k]))
info = {k: float(spearmanr(plr, [r[k] for r in rows_all], nan_policy="omit")[0]) for k in ("TS", "FP", "D3")}
g1 = rho12 >= 0.20; g2 = abs(ov[top]) <= 0.7
print(f"GATE 1, clip 1 vs clip 2: Spearman {rho12:.4f} on {len(cpairs)} pairs (needs >= 0.20; chair 0.349, 1,279 pairs) -> {'pass' if g1 else 'FAIL'}", flush=True)
print("GATE 2, overlap: " + "; ".join(f"{k} {v:+.3f}" for k, v in ov.items()), flush=True)
print(f"  largest |rho|: {top} {ov[top]:+.4f} (needs <= 0.7; chair +0.14, links) -> {'pass' if g2 else 'FAIL'}", flush=True)
print(f"  printed, deciding nothing: TS {info['TS']:+.3f} (chair -0.70), FP {info['FP']:+.3f} (chair -0.19), D3 {info['D3']:+.3f} (chair +0.26)", flush=True)
OUT["gate"] = dict(clip_to_clip=dict(spearman=r4(rho12), pairs=len(cpairs), threshold=0.20, passed=bool(g1), chair=0.349, chair_pairs=1279),
                   overlap=dict(spearman={k: r4(v) for k, v in ov.items()}, largest=[top, r4(ov[top])], threshold=0.7, passed=bool(g2)),
                   printed_deciding_nothing={k: r4(v) for k, v in info.items()}, passed=bool(g1 and g2))
if not (g1 and g2):
    OUT["outcome_joined"] = False
    finish("stopped (gate failed before any outcome was read: " + ", ".join(x for x, ok in (("clip-to-clip", g1), ("overlap", g2)) if not ok) + "); no outcome joined")

if os.environ.get("NOTES_ONLY"): print("NOTES_ONLY set: stopping before the outcome (no result.json written)"); sys.exit(0)

# ---------------------------------------------------------------- 4. outcome side (reached only if the gate passed)
print(f"[{time.time() - T0:.0f}s] gate passed; now opening hooktheory_covers_discogs.json", flush=True)
COV = jload("hooktheory_covers_discogs.json")
rows = []
for r in rows_all:
    cv = COV.get(r["vid"])
    if not cv or not cv["first_year"]: continue
    r = dict(r); r.update(covers=cv["covers"], first_year=cv["first_year"], clique=cv["clique"]); rows.append(r)
cnt = collections.Counter(r["artist"] for r in rows); sub = [r for r in rows if cnt[r["artist"]] >= 2]
print(f"rows with a first year: {len(rows)}; artists with two or more songs: {len(set(r['artist'] for r in sub))} artists, {len(sub)} songs (run 03: 420, 1,924)", flush=True)

def zc(M): M = np.asarray(M, float); s = np.atleast_1d(M.std(0)).copy(); s[s == 0] = 1; return (M - M.mean(0)) / (s if M.ndim > 1 else s[0])
CHECK = []
def within(R, yname, feats, ctrl):
    """run 03's within(): y and every column standardised over R, demeaned within artist, OLS without a constant; SE by the CR1 formula
    of run03/experiments/bridge/PREDICTION.md: G/(G-1) (N-1)/(N-K) (X'X)^-1 sum_g X_g'u_g u_g'X_g (X'X)^-1, normal p-values"""
    art = np.array([r["artist"] for r in R]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
    y = zc(np.log1p([r[yname] for r in R])); X = zc(np.column_stack([[r[f] for r in R] for f in feats] + [ctrl(R)]))
    def dm(M):
        M = np.array(M, float).reshape(len(R), -1); out = M.copy()
        for k in range(len(codes)): out[g == k] -= M[g == k].mean(0)
        return out
    Y = dm(y).ravel(); Xd = dm(X); n, K = Xd.shape; G = len(codes)
    XtXi = np.linalg.pinv(Xd.T @ Xd); b = XtXi @ Xd.T @ Y; u = Y - Xd @ b
    meat = np.zeros((K, K))
    for k in range(G):
        sg = Xd[g == k].T @ u[g == k]; meat += np.outer(sg, sg)
    V = G / (G - 1) * (n - 1) / (n - K) * XtXi @ meat @ XtXi; se = np.sqrt(np.diag(V)); p = 2 * N.sf(np.abs(b / se))
    try:   # check only: statsmodels' clustered SE with its small-sample correction (run 03's call)
        import statsmodels.api as sm
        m = sm.OLS(Y, Xd).fit(cov_type="cluster", cov_kwds={"groups": g, "df_correction": True})
        CHECK.append(float(np.max(np.abs(m.bse - se) / se)))
    except ImportError: pass
    return {f: dict(beta=float(b[i]), se=float(se[i]), p=float(p[i])) for i, f in enumerate(feats)}, n, G
def ctrl(R):   # first_year, log(clips per song), distinct links, distinct-chord dummies 4..11 and 12+ (3 the reference)
    nd = np.array([r["nchords"] for r in R])
    return np.column_stack([[r["first_year"] for r in R], np.log([r["nclips"] for r in R]), [r["nlinks"] for r in R]] + [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)])
half = lambda r: int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
F = ["PLR", "ch_rep", "ch_ic_mean"]
main, n, na = within(sub, "covers", F, ctrl); t = main["PLR"]
power = float(N.cdf(PRED / t["se"] - ZC) + N.cdf(-PRED / t["se"] - ZC))
print(f"SE of beta: {t['se']:.4f} (chair ~0.0176); power to see +0.02 at p < .01 two-sided: {power:.3f} (chair 0.075)", flush=True)
b, p = t["beta"], t["p"]
print(f"beta(PLR) = {b:+.4f}, SE {t['se']:.4f}, p = {p:.5f}, 95% range {b - 1.96 * t['se']:+.4f} to {b + 1.96 * t['se']:+.4f} ({n} songs, {na} artists)", flush=True)
Hh = {h: within([r for r in sub if half(r) == h], "covers", F, ctrl) for h in (0, 1)}
hb = [Hh[h][0]["PLR"]["beta"] for h in (0, 1)]
print(f"halves: {hb[0]:+.4f} (p {Hh[0][0]['PLR']['p']:.3f}, {Hh[0][1]} songs, {Hh[0][2]} artists), {hb[1]:+.4f} (p {Hh[1][0]['PLR']['p']:.3f}, {Hh[1][1]} songs, {Hh[1][2]} artists)", flush=True)
if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0: verdict = "pass"
elif b < 0 and p < ALPHA: verdict = "opposite sign (p < .01): the prediction is killed; reported as a new hypothesis ('long, every-voice-moves steps are what coverers take up'), not a pass"
elif b < 0.01: verdict = "kill"
else: verdict = "unsettled" + (" (the halves split)" if not (hb[0] > 0 and hb[1] > 0) else "")
OUT.update(outcome_joined=True, rows_with_first_year=len(rows), songs=n, artists=na, se=r4(t["se"]), power=r4(power),
           primary=dict(beta=r4(b), se=r4(t["se"]), p=round(p, 5), ci95=[r4(b - 1.96 * t["se"]), r4(b + 1.96 * t["se"])],
                        ch_rep={k: r4(v) for k, v in main["ch_rep"].items()}, ch_ic_mean={k: r4(v) for k, v in main["ch_ic_mean"].items()}),
           halves=[dict(half=h, songs=Hh[h][1], artists=Hh[h][2], beta=r4(hb[h]), se=r4(Hh[h][0]["PLR"]["se"]), p=r4(Hh[h][0]["PLR"]["p"])) for h in (0, 1)])

# reported, deciding nothing
VM = jload("discogs_versions_matched.json")["cliques"]
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))   # as in studies/judging_checks/within_artist/test.py
for r in sub:
    a = norm(r["artist"]); vm = VM[str(r["clique"])]
    oth = [y for names, y, _ in vm["versions"] if a not in [norm(x) for x in (names if isinstance(names, list) else [names])]]
    r["early"] = sum(1 for y in oth if y is not None and y <= r["first_year"] + 5); r["late"] = sum(1 for y in oth if y is not None and y > r["first_year"] + 10)
def one(yname, feats, key): r_, n_, a_ = within(sub, yname, list(feats), ctrl); return dict(beta=r4(r_[key]["beta"]), se=r4(r_[key]["se"]), p=r4(r_[key]["p"]), songs=n_)
dn = dict(TS_in_place_of_PLR=one("covers", ["TS", "ch_rep", "ch_ic_mean"], "TS"),
          covers_within_5_years=one("early", F, "PLR"), covers_after_10_years=one("late", F, "PLR"),
          without_ch_ic_mean=one("covers", ["PLR", "ch_rep"], "PLR"),
          skipped_moves=dict(undefined_phase=n_und, zero_step=n_zer, of_moves=n_moves),
          share_zero_PLR_songs=dict(all_songs=OUT["shape"]["share_zero_PLR_songs_all"], model_songs=r4(np.mean([r["PLR"] == 0 for r in sub]))),
          median_covers_all_early_late=[float(np.median([r[k] for r in sub])) for k in ("covers", "early", "late")],
          spearman_PLR_TS_model_songs=r4(spearmanr([r["PLR"] for r in sub], [r["TS"] for r in sub])[0]))
print(json.dumps(dn, indent=1), flush=True)
if CHECK: print(f"check: largest relative gap between the hand CR1 SE and statsmodels' clustered SE over all fits: {max(CHECK):.2e}", flush=True)
OUT["deciding_nothing"] = dn; OUT["cr1_vs_statsmodels_max_rel_gap"] = max(CHECK) if CHECK else None
finish(verdict)
