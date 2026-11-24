"""Run 04, thirds axis (D3 = |a3|/a0 of the duration-weighted chord profile, Amiot), against covers within each artist's own songs.
The rule is PREDICTION.md in this folder (commit 00ab557), frozen before this script was written. Rows, chord token, merging, wrap rule,
data-pack measures (weighted by n_mel), within() model, CR1 clustered SE and md5 artist halves are copied from
../../../run03/experiments/fifths_path/test.py; the song list is taken from the notes, as ../plr_share/PREDICTION.md says.

Order (printed as it goes):
  1. unit values of D3 (must reproduce the card), the worked example, and the invariance check (3 random clips, transposed by 5 and inverted);
  2. songs from the notes only: the `video` values of hooktheory_clips.json.gz; clips also present in the surprise and rhythm files;
  3. D3 per song (plus FP, PLR and TS, which are printed for the overlap check and decide nothing);
  4. THE GATE, before any outcome-side field is read: clip 1 vs clip 2 Spearman >= 0.20, and |Spearman| <= 0.7 with the 17 data-pack
     measures, distinct chords, links and clips. If it fails: result.json records "stopped" and the outcome file is never opened.
     Then the "not an existing measure renamed" check (largest overlap, R2 on the data pack) and the notes-side power;
  5. only if the gate passes: hooktheory_covers_discogs.json (covers, first_year), artists with 2+ songs; SE and power printed before beta;
     halves; the three-way rule; the items reported but deciding nothing.
Data are read from git (origin/main:studies/judging_data/), byte-identical to the files run 03 used.
python3 studies/judging_research/run04/experiments/thirds_axis/test.py -> result.json in this folder
"""
import json, gzip, collections, re, hashlib, os, sys, time, subprocess
import numpy as np, statsmodels.api as sm
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--show-toplevel"], text=True).strip()
def data(name):
    raw = subprocess.check_output(["git", "-C", REPO, "show", f"origin/main:studies/judging_data/{name}"])
    return json.loads(gzip.decompress(raw) if name.endswith(".gz") else raw)
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF   # the 17 of study_covers_discogs.py
ALPHA = 0.05 / 5; ZC = float(N.ppf(1 - ALPHA / 2)); PRED = 0.02; PRED_I1 = -0.025
OUT = dict(rule="PREDICTION.md, commit 00ab557", alpha=ALPHA, prediction_G3=PRED, prediction_I1=PRED_I1)
r4 = lambda x: round(float(x), 4)

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item())
    print("VERDICT:", verdict, flush=True); sys.exit(0)

# ---------------------------------------------------------------- the measure (frozen)
W3 = np.exp(-2j * np.pi * 3 * np.arange(12) / 12)
def pcs(ev, root=None):
    r = ev["root_pitch_class"] if root is None else root
    return {r % 12} | {int((r + s) % 12) for s in np.cumsum(ev["root_position_intervals"] or [])}
def profile(clip):
    """v[x] = sum of (offset - onset) over harmony events with positive duration, each pitch class counted once per event (absolute pcs)"""
    v = np.zeros(12)
    for ev in clip.get("harmony") or []:
        d = ev["offset"] - ev["onset"]
        if d > 0:
            for x in pcs(ev): v[x] += d
    return v
def d3_of(v): s = v.sum(); return None if s <= 0 else float(abs((v * W3).sum()) / s)
def d3_clip(clip): return d3_of(profile(clip))

# ---------------------------------------------------------------- run 03 token and runs (for the row rule, links, FP; copied)
def qual(iv):   # copied from studies/surprise/surprise_hooktheory.py (origin/main), via run 03
    iv = tuple(iv)
    Q = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
    return Q.get(iv, 8)
def ang(S, k):
    f = sum(np.exp(-2j * np.pi * k * x / 12) for x in S)
    return None if abs(f) < 1e-6 else float(np.angle(f))
def runs_of(clip):
    """merged runs (consecutive equal tokens); each run's tonic-relative pitch-class set from its first event: (token, phi5, phi3)"""
    tonic = clip["keys"][0]["tonic_pitch_class"] if clip.get("keys") else 0; R = []
    for ev in sorted(clip.get("harmony") or [], key=lambda c: c["onset"]):
        t = ((ev["root_pitch_class"] - tonic) % 12) * 9 + qual(ev["root_position_intervals"])
        if R and R[-1][0] == t: continue
        S = pcs(ev, (ev["root_pitch_class"] - tonic) % 12)
        R.append((t, ang(S, 5), ang(S, 3)))
    return R
def moves(R):
    mv = list(zip(R, R[1:]))
    if len(R) > 1 and R[-1][0] != R[0][0]: mv.append((R[-1], R[0]))
    return mv
def arc(a, b): d = abs(a - b) % (2 * np.pi); return float(min(d, 2 * np.pi - d))
w = lambda x: ((x + np.pi) % (2 * np.pi)) - np.pi
def fp_steps(R): return [arc(x[1], y[1]) for x, y in moves(R) if x[1] is not None and y[1] is not None]   # run 03 FP
def torus_steps(R):   # plr_share: skip if any phase undefined, or s < 1e-9
    out, nund, nzero = [], 0, 0
    for x, y in moves(R):
        if None in (x[1], x[2], y[1], y[2]): nund += 1; continue
        s = float(np.hypot(w(x[2] - y[2]), w(x[1] - y[1])))
        if s < 1e-9: nzero += 1; continue
        out.append(s)
    return out, nund, nzero

def fake_clip(chords, durs=None):   # chords: list of (root, root_position_intervals), tonic C, one beat each unless durs given
    durs = durs or [1] * len(chords); on = np.concatenate([[0], np.cumsum(durs)])
    return dict(keys=[dict(tonic_pitch_class=0)], harmony=[dict(root_pitch_class=r, root_position_intervals=iv, onset=float(on[i]), offset=float(on[i + 1])) for i, (r, iv) in enumerate(chords)])

# ---------------------------------------------------------------- 1. unit values, worked example, invariance
MAJ, MIN, DOM7 = [4, 3], [3, 4], [4, 3, 3]
CH = dict(I=(0, MAJ), ii=(2, MIN), iii=(4, MIN), III=(4, MAJ), IV=(5, MAJ), V=(7, MAJ), vi=(9, MIN), bVII=(10, MAJ))
UNIT = [(["I"], 0.745), (["I", "vi"], 0.667), (["I", "V", "vi", "IV"], 0.333), (["I", "IV", "V"], 0.248), (["ii", "V", "I"], 0.111), (["IV", "V"], 0.0)]
unit = {}
for prog, want in UNIT:
    got = d3_clip(fake_clip([CH[c] for c in prog])); unit["-".join(prog)] = dict(want=want, got=r4(got))
    print(f"unit {'-'.join(prog)}: D3 = {got:.4f} (card {want:.3f})", flush=True)
    assert abs(got - want) < 5e-4, (prog, got, want)
OUT["unit_values"] = unit
def a3_of(name):
    r, iv = CH[name]; S = pcs(dict(root_pitch_class=r, root_position_intervals=iv)); return complex(sum(W3[x] for x in S))
WORK = dict(chord_a3={c: f"{a3_of(c).real:+.0f}{a3_of(c).imag:+.0f}i" for c in ["I", "IV", "V", "vi", "III", "bVII"]})
for prog in (["I", "IV", "V", "I"], ["I", "vi", "IV", "V"], ["I", "III"], ["IV", "V"], ["bVII", "I"]):
    sm_ = sum(a3_of(c) for c in prog); WORK["-".join(prog)] = dict(sum_a3=f"{sm_.real:+.0f}{sm_.imag:+.0f}i", abs_a3=r4(abs(sm_)), a0=3 * len(prog), D3=r4(d3_clip(fake_clip([CH[c] for c in prog]))))
    print(f"worked example {'-'.join(prog)}: sum of a3 = {sm_.real:+.0f}{sm_.imag:+.0f}i, |a3| = {abs(sm_):.3f}, a0 = {3 * len(prog)}, D3 = {WORK['-'.join(prog)]['D3']:.3f}", flush=True)
OUT["worked_example"] = WORK

CL = data("hooktheory_clips.json.gz")["clips"]
rng = np.random.default_rng(20261124)
inv = []
for k in rng.choice(sorted(k for k in CL if d3_clip(CL[k]) is not None), 3, replace=False):
    c = CL[k]; t = dict(c, harmony=[])
    for ev in c.get("harmony") or []:   # transpose by 5, then invert x -> -x, as pitch-class sets (inversion reverses the interval order)
        S = sorted({(-(x + 5)) % 12 for x in pcs(ev)})
        r0 = (-(ev["root_pitch_class"] + 5)) % 12   # any member works as the root of the image; intervals rebuilt from it
        ring = sorted((x - r0) % 12 for x in S); iv = list(np.diff(ring).astype(int))
        t["harmony"].append(dict(ev, root_pitch_class=r0, root_position_intervals=iv))
    assert all(pcs(e2) == {(-(x + 5)) % 12 for x in pcs(e1)} for e1, e2 in zip(c["harmony"], t["harmony"]))
    a, b = d3_clip(c), d3_clip(t); inv.append(dict(clip=str(k), D3=r4(a), D3_transformed=r4(b), diff=abs(a - b)))
    print(f"invariance: clip {k}: D3 {a:.6f}, transposed by 5 and inverted {b:.6f}", flush=True)
    assert abs(a - b) < 1e-9
OUT["invariance_check"] = inv

# ---------------------------------------------------------------- 2. songs from the notes only
S_ = data("hooktheory_surprise.json.gz")
RH = {r["k"]: r for r in data("hooktheory_rhythm.json.gz")}
SONGS = {c["video"] for c in CL.values()}
by = collections.defaultdict(list)   # the song's clips, in surprise-file order
for c in S_:
    if c["vid"] in SONGS and c["k"] in RH and c["k"] in CL:
        assert CL[c["k"]]["video"] == c["vid"]
        by[c["vid"]].append(dict(c, **{f: RH[c["k"]][f] for f in RF}))

rows_all = []; undefined = 0
for vid, cs in by.items():
    Rs = [runs_of(CL[c["k"]]) for c in cs]
    seqs = [[t for t, *_ in R] for R in Rs]
    nodes = sorted({t for s in seqs for t in s})
    if len(nodes) < 3: continue
    links = set()
    for s in seqs:
        mv = list(zip(s, s[1:])) + ([(s[-1], s[0])] if len(s) > 1 and s[-1] != s[0] else [])
        links |= {frozenset(m) for m in mv if m[0] != m[1]}
    cd3 = [d3_clip(CL[c["k"]]) for c in cs]
    if all(x is None for x in cd3): undefined += 1; continue
    fps = [x for R in Rs for x in fp_steps(R)]
    tor = [torus_steps(R) for R in Rs]; ts = [x for t_, _, _ in tor for x in t_]
    wt = np.array([c["n_mel"] for c in cs], float)
    r = {f: float(np.average([c[f] for c in cs], weights=wt)) for f in FE}
    r.update(vid=vid, artist=cs[0]["artist"], nclips=len(cs), nchords=len(nodes), nlinks=len(links),
             D3=float(np.mean([x for x in cd3 if x is not None])), clip1=cd3[0], clip2=cd3[1] if len(cd3) > 1 else None,
             FP=float(np.mean(fps)) if fps else None, PLR=float(np.mean([x < 1.25 for x in ts])) if ts else None, TS=float(np.mean(ts)) if ts else None,
             tor_und=sum(u for _, u, _ in tor), tor_zero=sum(z for _, _, z in tor))
    rows_all.append(r)
d3 = np.array([r["D3"] for r in rows_all]); pct = np.percentile(d3, (10, 50, 90))
print(f"[{time.time() - T0:.0f}s] songs with >= 3 distinct tokens: {len(rows_all) + undefined} (chair 2,672); D3 undefined: {undefined} (chair none)", flush=True)
print(f"  D3 10th / 50th / 90th: {pct[0]:.3f} / {pct[1]:.3f} / {pct[2]:.3f} (chair 0.153 / 0.302 / 0.469); share below 0.05: {np.mean(d3 < 0.05):.4f}", flush=True)
print(f"  (PLR side, deciding nothing: torus moves skipped for an undefined phase {sum(r['tor_und'] for r in rows_all)} (plr chair 1,801), zero steps {sum(r['tor_zero'] for r in rows_all)} (plr chair 37))", flush=True)
OUT["shape"] = dict(songs=len(rows_all), undefined=undefined, D3_p10_p50_p90=[r4(x) for x in pct], share_D3_below_0_05_all_songs=r4(np.mean(d3 < 0.05)))

# ---------------------------------------------------------------- 4. THE GATE (no outcome-side field has been read)
pairs = [(r["clip1"], r["clip2"]) for r in rows_all if r["nclips"] >= 2 and r["clip1"] is not None and r["clip2"] is not None]
rho12 = float(spearmanr([p[0] for p in pairs], [p[1] for p in pairs])[0])
ALSO = [(f, f) for f in FE] + [("distinct chords", "nchords"), ("links", "nlinks"), ("clips", "nclips")]
ov = {lab: float(spearmanr(d3, [r[k] for r in rows_all])[0]) for lab, k in ALSO}
top = max(ov, key=lambda k: abs(ov[k]))
g1 = rho12 >= 0.20; g2 = abs(ov[top]) <= 0.7
print(f"GATE 1, clip 1 vs clip 2: Spearman {rho12:.4f} on {len(pairs)} pairs (needs >= 0.20; chair 0.318, 1,281 pairs) -> {'pass' if g1 else 'FAIL'}", flush=True)
print("GATE 2, overlap: " + "; ".join(f"{k} {v:+.3f}" for k, v in ov.items()), flush=True)
print(f"  largest |rho|: {top} {ov[top]:+.4f} (needs <= 0.7; chair -0.25, ch_ic_mean; distinct chords -0.23) -> {'pass' if g2 else 'FAIL'}", flush=True)
info = {}
for m in ("TS", "PLR", "FP"):
    ok = [r for r in rows_all if r[m] is not None]
    info[m] = r4(spearmanr([r["D3"] for r in ok], [r[m] for r in ok])[0])
print(f"  printed, deciding nothing: Spearman with TS {info['TS']:+.3f}, PLR {info['PLR']:+.3f}, FP {info['FP']:+.3f} (chair -0.34, +0.26, about 0)", flush=True)
OUT["gate"] = dict(clip_to_clip=dict(spearman=rho12, pairs=len(pairs), threshold=0.20, passed=bool(g1), chair=0.318, chair_pairs=1281),
                   overlap=dict(spearman={k: r4(v) for k, v in ov.items()}, largest=[top, r4(ov[top])], threshold=0.7, passed=bool(g2)),
                   deciding_nothing_spearman=info, passed=bool(g1 and g2))
if not (g1 and g2):
    OUT["outcome_joined"] = False
    finish("stopped (gate failed before any outcome was read: " + ", ".join(x for x, ok in (("clip-to-clip", g1), ("overlap", g2)) if not ok) + "); no outcome joined")

# not an existing measure renamed: how much of D3 the existing notes measures reproduce together (still notes-only)
nd_all = np.array([r["nchords"] for r in rows_all])
def blockX(R):
    nd = np.array([r["nchords"] for r in R])
    return np.column_stack([[r[f] for r in R] for f in FE] + [[r["nlinks"] for r in R], np.log([r["nclips"] for r in R])] + [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)])
ok3 = [r for r in rows_all if None not in (r["FP"], r["PLR"], r["TS"])]
R2pack = float(sm.OLS(d3, sm.add_constant(blockX(rows_all))).fit().rsquared)
R2plus = float(sm.OLS([r["D3"] for r in ok3], sm.add_constant(np.column_stack([blockX(ok3), [[r["FP"], r["PLR"], r["TS"]] for r in ok3]]))).fit().rsquared)
print(f"renamed-measure check: R2 of D3 on the 17 data-pack measures + size block {R2pack:.3f}; adding FP, PLR, TS {R2plus:.3f} (printed; the frozen check is gate 2)", flush=True)
OUT["renamed_check"] = dict(largest_single_overlap=[top, r4(ov[top])], r2_on_data_pack_and_size=r4(R2pack), r2_adding_FP_PLR_TS=r4(R2plus))

# notes-side power (first year is unavailable notes-side): residual share after the artist effect and the model columns, artists with 2+ songs
def zc(M): M = np.asarray(M, float); s = np.atleast_1d(M.std(0)).copy(); s[s == 0] = 1; return (M - M.mean(0)) / (s if M.ndim > 1 else s[0])
def dm_by(M, g):
    M = np.array(M, float).reshape(len(g), -1); out = M.copy()
    for k in np.unique(g): out[g == k] -= M[g == k].mean(0)
    return out
cnt0 = collections.Counter(r["artist"] for r in rows_all); sub0 = [r for r in rows_all if cnt0[r["artist"]] >= 2]
g0 = np.array([sorted(set(r["artist"] for r in sub0)).index(r["artist"]) for r in sub0])
def resid_share(m):
    nd = np.array([r["nchords"] for r in sub0])
    C = zc(np.column_stack([[r["ch_rep"] for r in sub0], [r["ch_ic_mean"] for r in sub0], np.log([r["nclips"] for r in sub0]), [r["nlinks"] for r in sub0]] + [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)]))
    x = dm_by(zc([r[m] for r in sub0]), g0).ravel(); Cd = dm_by(C, g0)
    e = x - Cd @ np.linalg.lstsq(Cd, x, rcond=None)[0]; return float(e.var())
rsD, rsF = resid_share("D3"), resid_share("FP")
se_pred = 0.018 * np.sqrt(rsF / rsD); pw = lambda se, b=PRED, z=ZC: float(N.cdf(b / se - z) + N.cdf(-b / se - z))
print(f"notes-side: {len(sub0)} songs in {len(set(g0))} artists with 2+ songs (chair 1,924 / 420); residual share D3 {rsD:.3f}, FP {rsF:.3f} (chair 0.643, 0.679)", flush=True)
print(f"  SE ~ 0.018 * sqrt(FP/D3) = {se_pred:.4f} (chair 0.0185); power at +0.02, p < .01 two-sided {pw(se_pred):.3f} (chair 0.068); at p < .05 {pw(se_pred, z=1.96):.3f} (chair 0.19)", flush=True)
print("  power floor: far below the proposed 0.5 floor (R03-4, undecided); printed, not blocking", flush=True)
OUT["notes_side_power"] = dict(songs=len(sub0), artists=int(len(set(g0))), residual_share_D3=r4(rsD), residual_share_FP=r4(rsF), se=r4(se_pred), power_p01=r4(pw(se_pred)), power_p05=r4(pw(se_pred, z=1.96)))

# ---------------------------------------------------------------- 5. outcome side (reached only if the gate passed)
if os.environ.get("NOTES_ONLY"): print("NOTES_ONLY set: stopping before the outcome file is opened"); sys.exit(0)
print(f"[{time.time() - T0:.0f}s] gate passed; opening hooktheory_covers_discogs.json now", flush=True)
COV = data("hooktheory_covers_discogs.json")
VM = data("discogs_versions_matched.json")["cliques"]
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
print(f"rows with a first year: {len(rows)}; artists with two or more songs: {len(set(r['artist'] for r in sub))} artists, {len(sub)} songs", flush=True)

def within(R, yname, feats, ctrl):   # copied from studies/judging_checks/within_artist/test.py (origin/main), via run 03
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
F = ["D3", "ch_rep", "ch_ic_mean"]
main, n, na = within(sub, "covers", F, ctrl); t = main["D3"]
power = pw(t["se"])
print(f"SE of beta: {t['se']:.4f} (chair 0.0185); power to see +0.02 at p < .01 two-sided: {power:.3f} (chair 0.068); power to see -0.025 (I1): {pw(t['se'], PRED_I1):.3f}", flush=True)
b, p = t["beta"], t["p"]
print(f"beta(D3) = {b:+.4f}, SE {t['se']:.4f}, p = {p:.5f}, 95% range {b - 1.96 * t['se']:+.4f} to {b + 1.96 * t['se']:+.4f}", flush=True)
Hh = {h: within([r for r in sub if half(r) == h], "covers", F, ctrl) for h in (0, 1)}
hb = [Hh[h][0]["D3"]["beta"] for h in (0, 1)]
print(f"halves: {hb[0]:+.4f} (p {Hh[0][0]['D3']['p']:.3f}, {Hh[0][1]} songs, {Hh[0][2]} artists), {hb[1]:+.4f} (p {Hh[1][0]['D3']['p']:.3f}, {Hh[1][1]} songs, {Hh[1][2]} artists)", flush=True)
# the three-way rule, exactly as frozen
if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0: verdict = "G3 passes, I1 killed"
elif b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0: verdict = "I1 passes, G3 killed"
elif -0.01 < b < 0.01: verdict = "both killed"
elif b >= 0.01: verdict = "G3 unsettled, I1 killed" + (" (the halves split)" if not (hb[0] > 0 and hb[1] > 0) else "")
elif b <= -0.01: verdict = "I1 unsettled, G3 killed" + (" (the halves split)" if not (hb[0] < 0 and hb[1] < 0) else "")
else: verdict = "no rule applies"
OUT.update(outcome_joined=True, rows_with_first_year=len(rows), songs=n, artists=na, se=r4(t["se"]), power=r4(power), power_I1=r4(pw(t["se"], PRED_I1)),
           primary=dict(beta=r4(b), se=r4(t["se"]), p=round(p, 5), ci95=[r4(b - 1.96 * t["se"]), r4(b + 1.96 * t["se"])],
                        ch_rep={k: r4(v) for k, v in main["ch_rep"].items()}, ch_ic_mean={k: r4(v) for k, v in main["ch_ic_mean"].items()}),
           halves=[dict(half=h, songs=Hh[h][1], artists=Hh[h][2], beta=r4(hb[h]), se=r4(Hh[h][0]["D3"]["se"]), p=r4(Hh[h][0]["D3"]["p"])) for h in (0, 1)])
def one(R, yname, feats=F, key="D3"): r_, n_, a_ = within(R, yname, list(feats), ctrl); return dict(beta=r4(r_[key]["beta"]), se=r4(r_[key]["se"]), p=r4(r_[key]["p"]), songs=n_)
subP = [r for r in sub if r["PLR"] is not None]
dn = dict(covers_within_5_years=one(sub, "early"), covers_after_10_years=one(sub, "late"), without_ch_ic_mean=one(sub, "covers", ["D3", "ch_rep"]),
          with_PLR_added=one(subP, "covers", F + ["PLR"]),   # D3's beta only; PLR's own coefficient belongs to ../plr_share and is not printed here
          share_D3_below_0_05_model_songs=r4(np.mean([r["D3"] < 0.05 for r in sub])), share_D3_below_0_05_all_songs=OUT["shape"]["share_D3_below_0_05_all_songs"],
          median_covers_early_late=[float(np.median([r[k] for r in sub])) for k in ("covers", "early", "late")])
print("reported, deciding nothing:", json.dumps(dn, indent=1), flush=True)
OUT["deciding_nothing"] = dn
finish(verdict)
