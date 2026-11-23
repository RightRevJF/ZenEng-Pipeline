"""Run 03, melody transport (MT): does the tune move less than the chords under it, and is such a song covered more within its artist?
The rule is PREDICTION.md in this folder (commit 09ce7bd), frozen before this script was written. Rows, chord token, merging, wrap rule,
data-pack measures, within() model, CR1 clustered SE and md5 halves are copied from ../bridge/test.py and ../curvature/test.py.

Order (printed as it goes):
  1. unit checks of the circular W1 (C -> F# = 6; C major -> G major = 1);
  2. songs from the notes only (the song list is the key set of hooktheory_covers_discogs.json; nothing else in that file is read);
  3. MT per song; songs with no usable change dropped;
  4. THE GATE, on those songs, before any outcome-side field (first_year included) is read:
       clip 1 vs clip 2 Spearman >= 0.20, and |Spearman| <= 0.7 with the 17 data-pack measures, distinct chords, links and clips.
     If it fails: result.json records "stopped", and the script exits without opening first_year, covers or versions.
  5. only if the gate passes: first_year, artists with 2+ songs, covers and versions; SE and power printed before beta; halves; extras.
python3 studies/judging_research/run03/experiments/melody_transport/test.py -> result.json in this folder
"""
import json, gzip, collections, re, hashlib, os, sys, time
import numpy as np, statsmodels.api as sm
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/home/claude/jdata"   # a read-only copy of origin/main:studies/judging_data (same files, not modified)
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF   # the 17 of study_covers_discogs.py
ALPHA = 0.05 / 6; ZC = 2.638; PRED = -0.03
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

def w1c(a, b):
    """W1 on the 12-pitch-class circle, ground distance min(|i-j|, 12-|i-j|): sum_k |F_k - median(F)|, F = cumsum(a - b)"""
    F = np.cumsum(np.asarray(a, float) - np.asarray(b, float)); return float(np.abs(F - np.median(F)).sum())

def pcset_abs(ev):
    r = ev["root_pitch_class"] % 12; return sorted({r} | {(r + s) % 12 for s in np.cumsum(ev["root_position_intervals"] or [])})

def runs_of(clip):
    """harmony sorted by onset; consecutive events with equal token merge into one run that keeps each event's [onset, offset)"""
    tonic = clip["keys"][0]["tonic_pitch_class"] if clip.get("keys") else 0; R = []
    for ev in sorted(clip.get("harmony") or [], key=lambda c: c["onset"]):
        t = ((ev["root_pitch_class"] - tonic) % 12) * 9 + qual(ev["root_position_intervals"])
        if R and R[-1]["tok"] == t: R[-1]["iv"].append((ev["onset"], ev["offset"]))
        else: R.append(dict(tok=t, first=ev, iv=[(ev["onset"], ev["offset"])]))
    for r in R:
        ch = np.zeros(12); S = pcset_abs(r["first"]); ch[S] = 1.0 / len(S); r["ch"] = ch; r["set"] = set(S)
        mel = np.zeros(12)
        for nt in clip.get("melody") or []:
            for on, off in r["iv"]:
                ov = min(nt["offset"], off) - max(nt["onset"], on)
                if ov > 0: mel[nt["pitch_class"] % 12] += ov
        r["mel"] = mel
    return R

def clip_changes(clip):
    """the kept changes of one clip: list of (delta, melody W1, chord W1); plus (all changes, melody duration total, on chord tones)"""
    R = runs_of(clip); pairs = list(zip(R, R[1:]))
    if len(R) > 1 and R[-1]["tok"] != R[0]["tok"]: pairs.append((R[-1], R[0]))
    kept = []
    for x, y in pairs:
        if x["mel"].sum() <= 0 or y["mel"].sum() <= 0: continue
        mw = w1c(x["mel"] / x["mel"].sum(), y["mel"] / y["mel"].sum()); cw = w1c(x["ch"], y["ch"]); kept.append((mw - cw, mw, cw))
    dur = sum(r["mel"].sum() for r in R); on = sum(r["mel"][sorted(r["set"])].sum() for r in R)
    return kept, len(pairs), dur, on

def toks(clip):   # the bridge chord sequence (merged tokens), for distinct chords and links
    return [r["tok"] for r in runs_of(clip)]

# ---------------------------------------------------------------- 1. unit checks
e = np.eye(12); u1 = w1c(e[0], e[6])
cmaj = np.zeros(12); cmaj[[0, 4, 7]] = 1 / 3; gmaj = np.zeros(12); gmaj[[7, 11, 2]] = 1 / 3; u2 = w1c(cmaj, gmaj)
print(f"unit checks: W1(C, F#) = {u1:.6f} (want 6); W1(C major, G major) = {u2:.6f} (want 1)", flush=True)
assert abs(u1 - 6) < 1e-9 and abs(u2 - 1) < 1e-9, "circular W1 is wrong"
# brute-force cross-check of w1c against an exact LP on random pairs
from scipy.optimize import linprog
D = np.array([[min(abs(i - j), 12 - abs(i - j)) for j in range(12)] for i in range(12)], float)
A = np.zeros((24, 144))
for i in range(12): A[i, i * 12:(i + 1) * 12] = 1; A[12 + i, i::12] = 1
rng = np.random.default_rng(0); worst = 0.0
for _ in range(200):
    a = rng.random(12) * (rng.random(12) < 0.5); b = rng.random(12) * (rng.random(12) < 0.5); a[0] += 1e-3; b[5] += 1e-3; a /= a.sum(); b /= b.sum()
    lp = linprog(D.ravel(), A_eq=A, b_eq=np.r_[a, b], bounds=(0, None), method="highs").fun; worst = max(worst, abs(lp - w1c(a, b)))
print(f"  circular W1 formula vs exact LP on 200 random pairs: largest difference {worst:.1e}", flush=True)
assert worst < 1e-7
OUT["unit_checks"] = dict(C_to_Fsharp=u1, Cmaj_to_Gmaj=u2, formula_vs_lp_max_diff=worst)

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

songs3 = 0; dropped = 0; rows_all = []; n_changes = n_kept = 0; dur_all = on_all = 0.0
for vid, cs in by.items():
    seqs = [toks(CL[c["k"]]) for c in cs]
    nodes = sorted({t for s in seqs for t in s})
    if len(nodes) < 3: continue
    songs3 += 1
    links = set()
    for s in seqs:
        mv = list(zip(s, s[1:])) + ([(s[-1], s[0])] if len(s) > 1 and s[-1] != s[0] else [])
        links |= {frozenset(m) for m in mv if m[0] != m[1]}
    per_clip = [clip_changes(CL[c["k"]]) for c in cs]
    allk = [k for pc in per_clip for k in pc[0]]
    n_changes += sum(pc[1] for pc in per_clip); n_kept += len(allk)
    dur_all += sum(pc[2] for pc in per_clip); on_all += sum(pc[3] for pc in per_clip)
    if not allk: dropped += 1; continue
    w = np.array([c["n_mel"] for c in cs], float)
    r = {f: float(np.average([c[f] for c in cs], weights=w)) for f in FE}
    clipmt = [float(np.mean([k[0] for k in pc[0]])) if pc[0] else None for pc in per_clip]
    r.update(vid=vid, artist=cs[0]["artist"], nclips=len(cs), nchords=len(nodes), nlinks=len(links),
             MT=float(np.mean([k[0] for k in allk])), mel_w1=float(np.mean([k[1] for k in allk])), ch_w1=float(np.mean([k[2] for k in allk])),
             clip1=clipmt[0], clip2=clipmt[1] if len(clipmt) > 1 else None, changes=sum(pc[1] for pc in per_clip), kept=len(allk))
    rows_all.append(r)

mt = np.array([r["MT"] for r in rows_all]); pct = np.percentile(mt, (10, 50, 90))
print(f"[{time.time() - T0:.0f}s] songs with >= 3 distinct chords (before the first-year filter): {songs3} (chair 2,672); "
      f"dropped for no usable change: {dropped} (chair 3); kept: {len(rows_all)}", flush=True)
print(f"  changes kept: {n_kept} of {n_changes} = {n_kept / n_changes:.3f} (chair 0.81); melody duration on absolute chord tones: {on_all / dur_all:.3f} (chair 0.705)", flush=True)
print(f"  MT 10th / median / 90th: {pct[0]:+.3f} / {pct[1]:+.3f} / {pct[2]:+.3f} semitones (chair 0.18 / 0.88 / 1.55)", flush=True)
nd = np.array([r["nchords"] for r in rows_all])
Xs = sm.add_constant(np.column_stack([(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float), [r["nlinks"] for r in rows_all], np.log([r["nclips"] for r in rows_all])]))
R2 = float(sm.OLS(mt, Xs).fit().rsquared)
print(f"  R2 of MT on the size block (distinct-chord dummies, links, log clips): {R2:.3f} (chair 0.02)", flush=True)
OUT["shape"] = dict(songs_3plus_chords=songs3, dropped_no_usable_change=dropped, songs=len(rows_all), changes=n_changes, changes_kept=n_kept,
                    share_changes_kept=r4(n_kept / n_changes), share_changes_skipped=r4(1 - n_kept / n_changes),
                    melody_on_chord_tones=r4(on_all / dur_all), MT_p10_p50_p90=[r4(x) for x in pct], r2_size_block=r4(R2))

# ---------------------------------------------------------------- 4. THE GATE (no outcome-side field has been read)
pairs = [(r["clip1"], r["clip2"]) for r in rows_all if r["nclips"] >= 2 and r["clip1"] is not None and r["clip2"] is not None]
rho12 = float(spearmanr([p[0] for p in pairs], [p[1] for p in pairs])[0])
ALSO = [(f, f) for f in FE] + [("distinct chords", "nchords"), ("links", "nlinks"), ("clips", "nclips")]
ov = {lab: float(spearmanr(mt, [r[k] for r in rows_all])[0]) for lab, k in ALSO}
top = max(ov, key=lambda k: abs(ov[k]))
g1 = rho12 >= 0.20; g2 = abs(ov[top]) <= 0.7
print(f"GATE 1, clip 1 vs clip 2: Spearman {rho12:.4f} on {len(pairs)} pairs (needs >= 0.20; chair 0.195, 1,277 pairs) -> {'pass' if g1 else 'FAIL'}", flush=True)
print("GATE 2, overlap: " + "; ".join(f"{k} {v:+.3f}" for k, v in ov.items()), flush=True)
print(f"  largest |rho|: {top} {ov[top]:+.4f} (needs <= 0.7; chair 0.175, length_variety) -> {'pass' if g2 else 'FAIL'}", flush=True)
OUT["gate"] = dict(clip_to_clip=dict(spearman=rho12, pairs=len(pairs), threshold=0.20, passed=bool(g1), chair=0.195, chair_pairs=1277),
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
F = ["MT", "ch_rep", "ch_ic_mean"]; F0 = ["MT", "ch_rep"]
main, n, na = within(sub, "covers", F, ctrl); t = main["MT"]
power = float(N.cdf(-PRED / t["se"] - ZC) + N.cdf(PRED / t["se"] - ZC))
print(f"SE of beta: {t['se']:.4f} (chair ~0.0155); power to see -0.03 at p < .0083 two-sided: {power:.3f} (chair ~0.24)", flush=True)
b, p = t["beta"], t["p"]
print(f"beta(MT) = {b:+.4f}, p = {p:.5f}, 95% range {b - 1.96 * t['se']:+.4f} to {b + 1.96 * t['se']:+.4f}", flush=True)
Hh = {h: within([r for r in sub if half(r) == h], "covers", F, ctrl) for h in (0, 1)}
hb = [Hh[h][0]["MT"]["beta"] for h in (0, 1)]
print(f"halves: {hb[0]:+.4f} (p {Hh[0][0]['MT']['p']:.3f}, {Hh[0][1]} songs), {hb[1]:+.4f} (p {Hh[1][0]['MT']['p']:.3f}, {Hh[1][1]} songs)", flush=True)
if b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0: verdict = "pass"
elif b > 0 and p < ALPHA: verdict = "opposite sign (p < .0083): a new hypothesis, not a pass"
elif b > -0.01: verdict = "kill"
else: verdict = "unsettled" + (" (the halves split)" if not (hb[0] < 0 and hb[1] < 0) else "")
OUT.update(outcome_joined=True, rows_with_first_year=len(rows), songs=n, artists=na, se=r4(t["se"]), power=r4(power), prediction=PRED,
           primary=dict(beta=r4(b), se=r4(t["se"]), p=round(p, 5), ci95=[r4(b - 1.96 * t["se"]), r4(b + 1.96 * t["se"])],
                        ch_rep={k: r4(v) for k, v in main["ch_rep"].items()}, ch_ic_mean={k: r4(v) for k, v in main["ch_ic_mean"].items()}),
           halves=[dict(half=h, songs=Hh[h][1], artists=Hh[h][2], beta=r4(hb[h]), se=r4(Hh[h][0]["MT"]["se"]), p=r4(Hh[h][0]["MT"]["p"])) for h in (0, 1)])
def one(R, yname, feats=F, key="MT"): r_, n_, a_ = within(R, yname, list(feats), ctrl); return dict(beta=r4(r_[key]["beta"]), se=r4(r_[key]["se"]), p=r4(r_[key]["p"]), songs=n_)
pm, _, _ = within(sub, "covers", ["mel_w1", "ch_w1", "ch_rep", "ch_ic_mean"], ctrl)
dn = dict(covers_within_5_years=one(sub, "early"), covers_after_10_years=one(sub, "late"), without_ch_ic_mean=one(sub, "covers", F0),
          parts_in_place_of_MT={k: {kk: r4(vv) for kk, vv in pm[k].items()} for k in ("mel_w1", "ch_w1")},
          share_changes_skipped=OUT["shape"]["share_changes_skipped"], median_covers_early_late=[float(np.median([r[k] for r in sub])) for k in ("covers", "early", "late")])
print(json.dumps(dn, indent=1), flush=True)
OUT["deciding_nothing"] = dn
finish(verdict)
