"""Run 03, fifths path (FP): mean step size of the chord path on the circle of fifths (phase of the 5th Fourier coefficient, Amiot),
against covers within each artist's own songs. The rule is PREDICTION.md in this folder (commit 09ce7bd), frozen before this script was
written. Rows, chord token, merging, wrap rule, data-pack measures, within() model, CR1 clustered SE and md5 halves are copied from
../bridge/test.py and ../curvature/test.py.

Order (printed as it goes):
  1. unit values of the step (must reproduce the card), and a worked example (I-V-vi-IV against I-IV-V);
  2. songs from the notes only (the song list is the key set of hooktheory_covers_discogs.json; nothing else in that file is read);
  3. FP per song;
  4. THE GATE, on those songs, before any outcome-side field (first_year included) is read:
       clip 1 vs clip 2 Spearman >= 0.20, and |Spearman| <= 0.7 with the 17 data-pack measures, distinct chords, links and clips.
     If it fails: result.json records "stopped", and the script exits without opening first_year, covers or versions.
  5. only if the gate passes: first_year, artists with 2+ songs, covers and versions; SE and power printed before beta; halves; extras.
python3 studies/judging_research/run03/experiments/fifths_path/test.py -> result.json in this folder
"""
import json, gzip, collections, re, hashlib, os, sys, time
import numpy as np, statsmodels.api as sm
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/home/claude/jdata"   # a read-only copy of origin/main:studies/judging_data (same files, not modified)
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF   # the 17 of study_covers_discogs.py
ALPHA = 0.05 / 6; ZC = 2.638; PRED = -0.02
OUT = dict(rule="PREDICTION.md, commit 09ce7bd", alpha=round(ALPHA, 5))
r4 = lambda x: round(float(x), 4)

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item())
    print("VERDICT:", verdict, flush=True); sys.exit(0)

# ---------------------------------------------------------------- measure
def qual(iv):   # copied from studies/surprise/surprise_hooktheory.py (origin/main)
    iv = tuple(iv)
    Q = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
    return Q.get(iv, 8)

def phase(S):
    """theta = angle of f5(S) = sum_k exp(-2 pi i 5k/12); None if |f5| < 1e-6"""
    f = sum(np.exp(-2j * np.pi * 5 * k / 12) for k in S)
    return None if abs(f) < 1e-6 else float(np.angle(f))

def arc(a, b): d = abs(a - b) % (2 * np.pi); return float(min(d, 2 * np.pi - d))

def runs_of(clip):
    """merged runs (consecutive equal bridge tokens); each run's tonic-relative pitch-class set from its first event"""
    tonic = clip["keys"][0]["tonic_pitch_class"] if clip.get("keys") else 0; R = []
    for ev in sorted(clip.get("harmony") or [], key=lambda c: c["onset"]):
        t = ((ev["root_pitch_class"] - tonic) % 12) * 9 + qual(ev["root_position_intervals"])
        if R and R[-1][0] == t: continue
        r = (ev["root_pitch_class"] - tonic) % 12
        S = {r} | {int((r + s) % 12) for s in np.cumsum(ev["root_position_intervals"] or [])}
        R.append((t, phase(S)))
    return R

def clip_steps(clip):
    """kept steps of one clip (moves of M: consecutive runs, plus the wrap when tokens differ), and the number of moves"""
    R = runs_of(clip); mv = list(zip(R, R[1:]))
    if len(R) > 1 and R[-1][0] != R[0][0]: mv.append((R[-1], R[0]))
    return [arc(x[1], y[1]) for x, y in mv if x[1] is not None and y[1] is not None], len(mv)

def fake_clip(chords):   # chords: list of (root relative to C, root_position_intervals), tonic C, one beat each
    return dict(keys=[dict(tonic_pitch_class=0)], harmony=[dict(root_pitch_class=r, root_position_intervals=iv, onset=i, offset=i + 1) for i, (r, iv) in enumerate(chords)])

# ---------------------------------------------------------------- 1. unit values and the worked example
MAJ, MIN, DOM7 = [4, 3], [3, 4], [4, 3, 3]
CH = dict(I=(0, MAJ), V=(7, MAJ), IV=(5, MAJ), vi=(9, MIN), ii=(2, MIN), iii=(4, MIN), bVII=(10, MAJ), i=(0, MIN), bVI=(8, MAJ), bII=(1, MAJ), V7=(7, DOM7))
def step2(x, y): s, _ = clip_steps(fake_clip([CH[x], CH[y]])); return s[0]
UNIT = [("I", "V", np.pi / 6), ("I", "IV", np.pi / 6), ("I", "vi", np.pi / 6), ("ii", "V", np.pi / 6), ("I", "iii", np.pi / 3), ("I", "bVII", np.pi / 3),
        ("I", "i", np.pi / 3), ("IV", "V", np.pi / 3), ("I", "bVI", 2 * np.pi / 3), ("I", "bII", 5 * np.pi / 6), ("V", "vi", 0.0), ("I", "ii", 0.0)]
unit = {}
for x, y, want in UNIT:
    got = step2(x, y); unit[f"{x}->{y}"] = dict(want=r4(want), got=r4(got)); print(f"unit {x}->{y}: {got:.3f} (want {want:.3f})")
    assert abs(got - want) < 1e-9, (x, y, got, want)
pI = runs_of(fake_clip([CH["I"]]))[0][1]; pV7 = runs_of(fake_clip([CH["V7"]]))[0][1]
print(f"unit: phase(V7) = {pV7:.4f}, phase(I) = {pI:.4f} (want equal)"); assert abs(pV7 - pI) < 1e-9
aug = runs_of(fake_clip([(0, [4, 4])]))[0][1]; dim7 = runs_of(fake_clip([(0, [3, 3, 3])]))[0][1]
assert aug is None and dim7 is None, "augmented triad and diminished seventh must have no phase"
unit["V7_phase_equals_I"] = True; unit["aug_and_dim7_no_phase"] = True
OUT["unit_values"] = unit
WORK = {}
for name, prog in (("I-V-vi-IV", ["I", "V", "vi", "IV"]), ("I-IV-V", ["I", "IV", "V"])):
    st, nm = clip_steps(fake_clip([CH[c] for c in prog]))
    labels = [f"{a}->{b}" for a, b in zip(prog, prog[1:] + prog[:1])]
    WORK[name] = dict(steps={l: r4(s) for l, s in zip(labels, st)}, FP=r4(np.mean(st)))
    print(f"worked example {name}: " + ", ".join(f"{l} {s:.3f}" for l, s in zip(labels, st)) + f" (the last is the wrap) -> FP = {np.mean(st):.3f} rad", flush=True)
OUT["worked_example"] = WORK

# ---------------------------------------------------------------- 2. songs from the notes only
CL = json.load(gzip.open(os.path.join(DATA, "hooktheory_clips.json.gz")))["clips"]
S = json.load(gzip.open(os.path.join(DATA, "hooktheory_surprise.json.gz")))
RH = {r["k"]: r for r in json.load(gzip.open(os.path.join(DATA, "hooktheory_rhythm.json.gz")))}
SONGS = set(json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json"))).keys())   # key set only; covers/first_year not kept here
by = collections.defaultdict(list)   # the song's clips, in surprise-file order
for c in S:
    if c["vid"] in SONGS and c["k"] in RH and c["k"] in CL:
        assert CL[c["k"]]["video"] == c["vid"]
        by[c["vid"]].append(dict(c, **{f: RH[c["k"]][f] for f in RF}))

rows_all = []; undefined = 0; n_moves = n_kept = n_zero = 0
for vid, cs in by.items():
    seqs = [[t for t, _ in runs_of(CL[c["k"]])] for c in cs]
    nodes = sorted({t for s in seqs for t in s})
    if len(nodes) < 3: continue
    links = set()
    for s in seqs:
        mv = list(zip(s, s[1:])) + ([(s[-1], s[0])] if len(s) > 1 and s[-1] != s[0] else [])
        links |= {frozenset(m) for m in mv if m[0] != m[1]}
    per_clip = [clip_steps(CL[c["k"]]) for c in cs]
    allst = [x for st, _ in per_clip for x in st]
    n_moves += sum(m for _, m in per_clip); n_kept += len(allst); n_zero += sum(1 for x in allst if x < 1e-9)
    if not allst: undefined += 1; continue
    w = np.array([c["n_mel"] for c in cs], float)
    r = {f: float(np.average([c[f] for c in cs], weights=w)) for f in FE}
    clipfp = [float(np.mean(st)) if st else None for st, _ in per_clip]
    r.update(vid=vid, artist=cs[0]["artist"], nclips=len(cs), nchords=len(nodes), nlinks=len(links), FP=float(np.mean(allst)),
             zero_share=float(np.mean([x < 1e-9 for x in allst])), clip1=clipfp[0], clip2=clipfp[1] if len(clipfp) > 1 else None)
    rows_all.append(r)
fp = np.array([r["FP"] for r in rows_all]); pct = np.percentile(fp, (10, 50, 90))
print(f"[{time.time() - T0:.0f}s] songs with >= 3 distinct chords (before the first-year filter): {len(rows_all) + undefined} (chair 2,672); FP undefined: {undefined} (chair 0)", flush=True)
print(f"  moves skipped for a chord with no phase: {n_moves - n_kept} of {n_moves} (chair 426 of 68,314); zero steps: {n_zero / n_kept:.3f} of kept moves", flush=True)
print(f"  FP 10th / median / 90th: {pct[0]:.3f} / {pct[1]:.3f} / {pct[2]:.3f} rad (chair 0.428 / 0.663 / 1.047)", flush=True)
nd = np.array([r["nchords"] for r in rows_all])
Xs = sm.add_constant(np.column_stack([(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float), [r["nlinks"] for r in rows_all], np.log([r["nclips"] for r in rows_all])]))
R2 = float(sm.OLS(fp, Xs).fit().rsquared)
print(f"  R2 of FP on the size block (distinct-chord dummies, links, log clips): {R2:.3f} (chair 0.02)", flush=True)
OUT["shape"] = dict(songs=len(rows_all), undefined=undefined, moves=n_moves, moves_kept=n_kept, moves_skipped_no_phase=n_moves - n_kept,
                    share_zero_steps=r4(n_zero / n_kept), FP_p10_p50_p90=[r4(x) for x in pct], r2_size_block=r4(R2))

# ---------------------------------------------------------------- 4. THE GATE (no outcome-side field has been read)
pairs = [(r["clip1"], r["clip2"]) for r in rows_all if r["nclips"] >= 2 and r["clip1"] is not None and r["clip2"] is not None]
rho12 = float(spearmanr([p[0] for p in pairs], [p[1] for p in pairs])[0])
ALSO = [(f, f) for f in FE] + [("distinct chords", "nchords"), ("links", "nlinks"), ("clips", "nclips")]
ov = {lab: float(spearmanr(fp, [r[k] for r in rows_all])[0]) for lab, k in ALSO}
top = max(ov, key=lambda k: abs(ov[k]))
g1 = rho12 >= 0.20; g2 = abs(ov[top]) <= 0.7
print(f"GATE 1, clip 1 vs clip 2: Spearman {rho12:.4f} on {len(pairs)} pairs (needs >= 0.20; chair 0.356, 1,281 pairs) -> {'pass' if g1 else 'FAIL'}", flush=True)
print("GATE 2, overlap: " + "; ".join(f"{k} {v:+.3f}" for k, v in ov.items()), flush=True)
print(f"  largest |rho|: {top} {ov[top]:+.4f} (needs <= 0.7; chair +0.22, ch_ic_mean) -> {'pass' if g2 else 'FAIL'}", flush=True)
OUT["gate"] = dict(clip_to_clip=dict(spearman=rho12, pairs=len(pairs), threshold=0.20, passed=bool(g1), chair=0.356, chair_pairs=1281),
                   overlap=dict(spearman={k: r4(v) for k, v in ov.items()}, largest=[top, r4(ov[top])], threshold=0.7, passed=bool(g2)),
                   passed=bool(g1 and g2))
if not (g1 and g2):
    OUT["outcome_joined"] = False
    finish("stopped (gate failed before any outcome was read: " + ", ".join(x for x, ok in (("clip-to-clip", g1), ("overlap", g2)) if not ok) + "); no outcome joined")

# ---------------------------------------------------------------- 5. outcome side (reached only if the gate passed)
COV = json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json")))
VM = json.load(open(os.path.join(DATA, "discogs_versions_matched.json")))["cliques"]
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))   # as in studies/judging_checks/within_artist/test.py
rows = []
for r in rows_all:
    cv = COV[r["vid"]]
    if not cv["first_year"]: continue
    r = dict(r); r.update(covers=cv["covers"], first_year=cv["first_year"], clique=cv["clique"]); rows.append(r)
cnt = collections.Counter(r["artist"] for r in rows); sub = [r for r in rows if cnt[r["artist"]] >= 2]
for r in sub:
    a = norm(r["artist"]); vm = VM[str(r["clique"])]
    oth = [y for names, y, _ in vm["versions"] if a not in [norm(x) for x in (names if isinstance(names, list) else [names])]]
    r["early"] = sum(1 for y in oth if y is not None and y <= r["first_year"] + 5); r["late"] = sum(1 for y in oth if y is not None and y > r["first_year"] + 10)
print(f"[{time.time() - T0:.0f}s] rows with a first year: {len(rows)}; artists with two or more songs: {len(set(r['artist'] for r in sub))} artists, {len(sub)} songs", flush=True)

def zc(M): M = np.asarray(M, float); s = np.atleast_1d(M.std(0)).copy(); s[s == 0] = 1; return (M - M.mean(0)) / (s if M.ndim > 1 else s[0])
def within(R, yname, feats, ctrl):   # copied from studies/judging_checks/within_artist/test.py (origin/main)
    art = np.array([r["artist"] for r in R]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
    y = zc(np.log1p([r[yname] for r in R])); X = zc(np.column_stack([[r[f] for r in R] for f in feats] + [ctrl(R)]))
    def dm(M):
        M = np.array(M, float).reshape(len(R), -1); out = M.copy()
        for k in range(len(codes)): out[g == k] -= M[g == k].mean(0)
        return out
    m = sm.OLS(dm(y).ravel(), dm(X)).fit(cov_type="cluster", cov_kwds={"groups": g, "df_correction": True})
    return {f: dict(beta=float(m.params[i]), se=float(m.bse[i]), p=float(m.pvalues[i])) for i, f in enumerate(feats)}, len(R), len(codes)
def ctrl(R):   # first_year, log(clips per song), distinct links, distinct-chord dummies 4..11 and 12+ (3 the reference)
    nd = np.array([r["nchords"] for r in R])
    return np.column_stack([[r["first_year"] for r in R], np.log([r["nclips"] for r in R]), [r["nlinks"] for r in R]] + [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)])
half = lambda r: int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
F = ["FP", "ch_rep", "ch_ic_mean"]; F0 = ["FP", "ch_rep"]
main, n, na = within(sub, "covers", F, ctrl); t = main["FP"]
power = float(N.cdf(-PRED / t["se"] - ZC) + N.cdf(PRED / t["se"] - ZC))
print(f"SE of beta: {t['se']:.4f} (chair ~0.016); power to see -0.02 at p < .0083 two-sided: {power:.3f} (chair ~0.08)", flush=True)
b, p = t["beta"], t["p"]
print(f"beta(FP) = {b:+.4f}, p = {p:.5f}, 95% range {b - 1.96 * t['se']:+.4f} to {b + 1.96 * t['se']:+.4f}", flush=True)
Hh = {h: within([r for r in sub if half(r) == h], "covers", F, ctrl) for h in (0, 1)}
hb = [Hh[h][0]["FP"]["beta"] for h in (0, 1)]
print(f"halves: {hb[0]:+.4f} (p {Hh[0][0]['FP']['p']:.3f}, {Hh[0][1]} songs, {Hh[0][2]} artists), {hb[1]:+.4f} (p {Hh[1][0]['FP']['p']:.3f}, {Hh[1][1]} songs, {Hh[1][2]} artists)", flush=True)
if b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0: verdict = "pass"
elif b > 0 and p < ALPHA: verdict = "opposite sign (p < .0083): a new hypothesis ('bold steps are what coverers take up'), not a pass"
elif b > -0.01: verdict = "kill"
else: verdict = "unsettled" + (" (the halves split)" if not (hb[0] < 0 and hb[1] < 0) else "")
OUT.update(outcome_joined=True, rows_with_first_year=len(rows), songs=n, artists=na, se=r4(t["se"]), power=r4(power), prediction=PRED,
           primary=dict(beta=r4(b), se=r4(t["se"]), p=round(p, 5), ci95=[r4(b - 1.96 * t["se"]), r4(b + 1.96 * t["se"])],
                        ch_rep={k: r4(v) for k, v in main["ch_rep"].items()}, ch_ic_mean={k: r4(v) for k, v in main["ch_ic_mean"].items()}),
           halves=[dict(half=h, songs=Hh[h][1], artists=Hh[h][2], beta=r4(hb[h]), se=r4(Hh[h][0]["FP"]["se"]), p=r4(Hh[h][0]["FP"]["p"])) for h in (0, 1)])
def one(R, yname, feats=F, key="FP"): r_, n_, a_ = within(R, yname, list(feats), ctrl); return dict(beta=r4(r_[key]["beta"]), se=r4(r_[key]["se"]), p=r4(r_[key]["p"]), songs=n_)
dn = dict(covers_within_5_years=one(sub, "early"), covers_after_10_years=one(sub, "late"), without_ch_ic_mean=one(sub, "covers", F0),
          share_zero_steps_all_kept_moves=OUT["shape"]["share_zero_steps"], share_zero_steps_mean_over_model_songs=r4(np.mean([r["zero_share"] for r in sub])),
          median_covers_early_late=[float(np.median([r[k] for r in sub])) for k in ("covers", "early", "late")])
print(json.dumps(dn, indent=1), flush=True)
OUT["deciding_nothing"] = dn
finish(verdict)
