"""Run 04, info_rate (R04-I3): is a song far from the habitual surprise-per-beat (D) versioned less, within artist?
The rule is PREDICTION.md in this folder (frozen and committed in 00ab557 before this script was written). Rows, controls,
LPM, CR1, conditional logit and halves are as ../move_extensive/PREDICTION.md.

Order (printed as it goes):
  1. rows, measure and controls from the notes only;
  2. the GATE (clip-to-clip; overlap). If it fails: result.json says "stopped", no outcome is joined, the script ends;
     also the check that D is not an existing measure renamed, and the notes-side power;
  3. only then the KEY SET of origin/main:studies/judging_data/hooktheory_covers_discogs.json (nothing else in it is read);
  4. N and the y = 1 count;
  5. clustered SE and power, then beta, then the halves, then the conditional logit, then the verdict;
  6. reported, deciding nothing; result.json.
python3 test.py              -> full run, writes result.json in this folder
python3 test.py --notes-only -> steps 1-2 only, never touches the outcome, writes nothing

Data: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI (CC BY-SA 4.0)."""
import json, gzip, collections, re, hashlib, os, sys, time, subprocess, urllib.parse, warnings
import numpy as np
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/claude/zeneng-pipeline"
SURPRISE = "/home/claude/scratch/surprise.json.gz"   # byte-identical to origin/main studies/judging_data/hooktheory_surprise.json.gz
RHYTHM = "/home/claude/scratch/rhythm.json.gz"       # byte-identical to origin/main studies/judging_data/hooktheory_rhythm.json.gz
MD5 = {SURPRISE: "ff7b9d37a462c9ef78570b80db8a822e", RHYTHM: "1d6e04057519a864b62b7e8140971bb6"}
NOTES_ONLY = "--notes-only" in sys.argv
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF   # the 17 data-pack measures (run 03)
C_REF = 4.32           # fixed in the rule
PRED, ALPHA, ZC = -0.8, 0.01, N.ppf(1 - 0.01 / 2)
OUT = dict(rule="PREDICTION.md in this folder, commit 00ab557", hypothesis="R04-I3 information rate", prediction_pp_per_sd=PRED, alpha=ALPHA)
r4 = lambda x: None if x is None else round(float(x), 4)
def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    if not NOTES_ONLY:
        json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", verdict, flush=True); sys.exit(0)

import hashlib as _h
for f, m in MD5.items():
    got = _h.md5(open(f, "rb").read()).hexdigest(); assert got == m, f"{f}: md5 {got} != {m}"
print("data md5 checked (surprise ff7b9d37..., rhythm 1d6e0405...)", flush=True)

# ---------------------------------------------------------------- 1. rows from the notes
S = json.load(gzip.open(SURPRISE))
RH = {r["k"]: r for r in json.load(gzip.open(RHYTHM))}
print(f"surprise clips {len(S)}, rhythm rows {len(RH)}", flush=True)

def clip_rate(c, mel=True, ch=True):
    b = c["beats"]
    if b <= 0: return None
    r = ((c["n_mel"] * c["mel_ic_mean"]) if mel else 0.0) + ((c["n_ch"] * c["ch_ic_mean"]) if ch else 0.0)
    r /= b
    return r if r > 0 else None

rates = [clip_rate(c) for c in S]
r_all = np.array([x for x in rates if x is not None])
med = float(np.median(r_all))
print(f"clip r: {len(r_all)} of {len(S)} clips defined [chair: all]; median {med:.4f} [chair 4.323; the rule fixes 4.32]", flush=True)
OUT["clip_rate"] = dict(defined=len(r_all), clips=len(S), median=r4(med), fixed_ref=C_REF)
for c, r in zip(S, rates):
    c["r"] = r
    c["D"] = None if r is None else abs(np.log(r) - np.log(C_REF))
    c["Ds"] = None if r is None else float(np.log(r) - np.log(C_REF))
# reported-only variants: melody term alone, chord term alone, each about its own all-clip median (the rule names no reference; chosen here, before the outcome)
for tag, kw in (("mel", dict(mel=True, ch=False)), ("ch", dict(mel=False, ch=True))):
    rr = [clip_rate(c, **kw) for c in S]; m = float(np.median([x for x in rr if x is not None]))
    OUT.setdefault("variant_refs", {})[tag] = dict(median=r4(m), clips_defined=sum(x is not None for x in rr))
    for c, x in zip(S, rr): c["D_" + tag] = None if x is None else abs(np.log(x) - np.log(m))

by = collections.defaultdict(list)                      # a song's clips, in surprise-file order
for c in S: by[c["vid"]].append(c)
first = {v: cs[0] for v, cs in by.items()}
art_of = {v: c["artist"] for v, c in first.items()}
slug_of = {v: c["song"] for v, c in first.items()}
n_art = collections.Counter(art_of.values())
keep = [v for v in by if n_art[art_of[v]] >= 2]
print(f"songs {len(by)}, artists {len(n_art)}; artists with 2+ songs keep {len(keep)} songs [chair 9,588], "
      f"{len(set(art_of[v] for v in keep))} artists [chair 1,741]", flush=True)

def title_tokens(slug):
    u = urllib.parse.unquote(slug).lower(); b = re.sub(r"\([^)]*\)", " ", u)
    t = [x for x in re.split(r"[^a-z0-9]+", b) if x] or [x for x in re.split(r"[^a-z0-9]+", u) if x]
    return u, t
tkey = {}
for v in by: tkey[v] = "-".join(title_tokens(slug_of[v])[1])
arts_by_title = collections.defaultdict(set)
for v in by: arts_by_title[tkey[v]].add(art_of[v])

def wmean(vals, w):
    vals = np.asarray(vals, float); w = np.asarray(w, float)
    return float(np.average(vals, weights=w)) if w.sum() > 0 else float(vals.mean())

rows = []; no_rh = 0
for v in keep:
    cs = by[v]; w = [c["n_mel"] for c in cs]
    rc = [c for c in cs if c["k"] in RH]
    if not rc: no_rh += 1; continue
    r = {f: wmean([c[f] for c in cs], w) for f in FE if f not in RF}
    r["n_ch"] = wmean([c["n_ch"] for c in cs], w); r["beats"] = wmean([c["beats"] for c in cs], w)
    wr = [c["n_mel"] for c in rc]
    for f in RF + ["bpb"]:
        cc = [(RH[c["k"]][f], c["n_mel"]) for c in rc if RH[c["k"]][f] is not None]
        r[f] = wmean([a for a, _ in cc], [b for _, b in cc])
    def song_of(key):
        cc = [(c[key], c["n_mel"]) for c in cs if c[key] is not None]
        return wmean([a for a, _ in cc], [b for _, b in cc]) if cc else None
    r["D"] = song_of("D"); r["Ds"] = song_of("Ds"); r["D_mel"] = song_of("D_mel"); r["D_ch"] = song_of("D_ch")
    u, toks = title_tokens(slug_of[v])
    r.update(vid=v, artist=art_of[v], nclips=len(cs), ntok=len(toks), paren=float("(" in u),
             rep_title=float(len(arts_by_title[tkey[v]]) >= 2), clipD=[c["D"] for c in cs])
    rows.append(r)
assert all(r["D"] is not None for r in rows)
NR = len(rows); arts = sorted(set(r["artist"] for r in rows))
print(f"model rows: {NR} songs [chair 9,574], {len(arts)} artists [chair 1,741]; dropped for no rhythm clip: {no_rh} [chair 14]", flush=True)
OUT["rows"] = dict(songs=NR, artists=len(arts), dropped_no_rhythm_clip=no_rh, kept_before_rhythm_drop=len(keep))

def z(x): x = np.asarray(x, float); return (x - x.mean()) / x.std()
col = lambda k: np.array([r[k] for r in rows], float)
zD = z(col("D"))

# controls
nch_bin = np.digitize(col("n_ch"), [5, 7, 9, 11, 13, 16, 20, 25, 32])
ncl = col("nclips"); ntok = col("ntok"); bpb = col("bpb")
ctrl = {}
for k in range(1, 10): ctrl[f"nch_bin{k}"] = (nch_bin == k).astype(float)
ctrl["clips2"] = (ncl == 2).astype(float); ctrl["clips3"] = (ncl == 3).astype(float); ctrl["clips4p"] = (ncl >= 4).astype(float)
ctrl["ln_beats"] = np.log(col("beats"))
for k in (1, 2, 3, 4): ctrl[f"words{k}"] = (ntok == k).astype(float)
ctrl["paren"] = col("paren"); ctrl["rep_title"] = col("rep_title")
ctrl["density"] = col("density")
b3, b6 = np.isclose(bpb, 3), np.isclose(bpb, 6)
ctrl["bpb3"] = b3.astype(float); ctrl["bpb6"] = b6.astype(float); ctrl["bpb_other"] = (~b3 & ~b6 & ~np.isclose(bpb, 4)).astype(float)
cnt = dict(nch_bins=[int((nch_bin == k).sum()) for k in range(10)], clips=[int((ncl == 1).sum()), int(ctrl["clips2"].sum()), int(ctrl["clips3"].sum()), int(ctrl["clips4p"].sum())],
           words=[int((ntok == k).sum()) for k in (1, 2, 3, 4)] + [int((ntok >= 5).sum())], paren=int(ctrl["paren"].sum()), rep_title=int(ctrl["rep_title"].sum()),
           bpb3=int(b3.sum()), bpb6=int(b6.sum()), bpb_other=int(ctrl["bpb_other"].sum()))
print(f"control counts: {cnt}  [chair bpb 354 / 456 / 167]", flush=True)
OUT["control_counts"] = cnt
CN = list(ctrl)

# ---------------------------------------------------------------- 2. GATE (no outcome loaded)
art_arr = np.array([r["artist"] for r in rows])
ai = {a: i for i, a in enumerate(arts)}; gidx = np.array([ai[a] for a in art_arr])
def demean(M, g):
    M = np.asarray(M, float); M2 = M.reshape(len(M), -1)
    s = np.zeros((g.max() + 1, M2.shape[1])); np.add.at(s, g, M2); n = np.bincount(g).astype(float)
    return (M2 - s[g] / n[g, None]).reshape(M.shape)

# 2.1 clip-to-clip
pr = [(r["clipD"][0], r["clipD"][1]) for r in rows if r["nclips"] >= 2 and r["clipD"][0] is not None and r["clipD"][1] is not None]
rho_cc = float(spearmanr([a for a, _ in pr], [b for _, b in pr])[0])
print(f"GATE 1, clip-to-clip: Spearman clip D, clip 1 vs clip 2: {rho_cc:.4f} on {len(pr)} pairs (needs >= 0.20) [chair 0.279, 4,271 pairs]", flush=True)
# printed: clip-level D residualised on clip density, bpb, ln beats (fit on all clips with a rhythm row), same pairs where both clips have one
cr = [c for c in S if c["k"] in RH and c["D"] is not None]
Xc = np.column_stack([np.ones(len(cr)), [RH[c["k"]]["density"] for c in cr], [RH[c["k"]]["bpb"] for c in cr], np.log([c["beats"] for c in cr])])
res = np.array([c["D"] for c in cr]) - Xc @ np.linalg.lstsq(Xc, np.array([c["D"] for c in cr]), rcond=None)[0]
resk = {c["k"]: e for c, e in zip(cr, res)}
pr2 = []
for r in rows:
    if r["nclips"] < 2: continue
    k1, k2 = by[r["vid"]][0]["k"], by[r["vid"]][1]["k"]
    if k1 in resk and k2 in resk: pr2.append((resk[k1], resk[k2]))
rho_cc_res = float(spearmanr([a for a, _ in pr2], [b for _, b in pr2])[0])
print(f"  printed: residualised on density, bpb, ln beats (clip level): {rho_cc_res:.4f} on {len(pr2)} pairs [chair 0.290]", flush=True)
g1 = rho_cc >= 0.20

# 2.2 overlap
others = {f: col(f) for f in FE}; others.update(n_ch=col("n_ch"), beats=col("beats"), clips_per_song=ncl, bpb=bpb)
ov = {k: float(spearmanr(zD, v)[0]) for k, v in others.items()}
big = max(ov, key=lambda k: abs(ov[k]))
print("GATE 2, overlap (|Spearman| of song D <= 0.7 with each):", flush=True)
for k in sorted(ov, key=lambda k: -abs(ov[k])): print(f"    {k:20s} {ov[k]:+.4f}", flush=True)
print(f"  largest {big} {ov[big]:+.4f} [chair +0.17 mel_ic_mean; ch_ic_mean +0.07, ch_rep -0.03, density +0.05]", flush=True)
g2 = all(abs(x) <= 0.7 for x in ov.values())
OUT["gate"] = dict(clip_to_clip=dict(rho=r4(rho_cc), pairs=len(pr), need=0.20, passed=g1, printed_residualised=r4(rho_cc_res), printed_pairs=len(pr2)),
                   overlap=dict(rho={k: r4(v) for k, v in ov.items()}, largest=big, need_abs_max=0.7, passed=g2))
if not (g1 and g2):
    OUT["gate"]["passed"] = False; print("GATE FAILED: no outcome is joined.", flush=True); finish("stopped")
OUT["gate"]["passed"] = True
print("GATE PASSED", flush=True)

# 2.3 not an existing measure renamed (printed): D is a new combination; its nearest neighbours among every numeric field on hand
extra = {f: col(f) for f in []}
for f in ("mel_ic_sd", "ch_ic_sd"):
    extra[f] = np.array([wmean([c[f] for c in by[r["vid"]]], [c["n_mel"] for c in by[r["vid"]]]) for r in rows])
for f in ("long_rests_per_bar", "phrase_cv", "sync_share"):
    extra[f] = np.array([wmean([RH[c["k"]][f] for c in by[r["vid"]] if c["k"] in RH], [c["n_mel"] for c in by[r["vid"]] if c["k"] in RH]) for r in rows])
extra["n_mel"] = np.array([wmean([c["n_mel"] for c in by[r["vid"]]], [c["n_mel"] for c in by[r["vid"]]]) for r in rows])
extra["signed_lnr_dev"] = col("Ds")
ex = {k: float(spearmanr(zD, v)[0]) for k, v in extra.items()}
# within-artist R2 of D on all 17 + size fields + bpb (how much of D the existing fields reproduce linearly)
Xall = demean(np.column_stack([z(v) for v in others.values()] + [z(v) for k, v in extra.items() if k != "signed_lnr_dev"]), gidx)
dD = demean(zD, gidx); bb = np.linalg.lstsq(Xall, dD, rcond=None)[0]
r2_within = 1 - ((dD - Xall @ bb) ** 2).sum() / (dD ** 2).sum()
print("RENAME CHECK (printed): Spearman of song D with fields outside the gate list: " + ", ".join(f"{k} {v:+.3f}" for k, v in ex.items()), flush=True)
print(f"  within-artist R2 of z(D) on all {Xall.shape[1]} existing song fields (linear): {r2_within:.3f} -> D is not an existing field renamed "
      f"(largest single |rho| with any data-pack field {abs(ov[big]):.2f})", flush=True)
OUT["rename_check"] = dict(rho_outside_gate=({k: r4(v) for k, v in ex.items()}), within_artist_R2_on_existing_fields=r4(r2_within),
                           note="signed ln r - ln 4.32 is a component of D (|.|), not an existing field; printed for reference")

# 2.4 notes-side power
X = np.column_stack([zD] + [ctrl[k] for k in CN]); NAMES = ["zD"] + CN
Xd = demean(X, gidx)
keepcol = np.abs(Xd).sum(0) > 1e-9
assert keepcol.all(), f"columns constant within artist: {[n for n, k in zip(NAMES, keepcol) if not k]}"
assert np.linalg.matrix_rank(Xd) == Xd.shape[1], "demeaned design is rank deficient"
xt = Xd[:, 0] - Xd[:, 1:] @ np.linalg.lstsq(Xd[:, 1:], Xd[:, 0], rcond=None)[0]
share = float((xt ** 2).sum() / NR)
se_bound = 100 * np.sqrt(0.21 * 0.79 / (xt ** 2).sum())
power = lambda se: float(N.cdf(abs(PRED) / se - ZC) + N.cdf(-abs(PRED) / se - ZC))
print(f"POWER (notes side): within-artist residual share of z(D) after controls {share:.3f} [chair 0.646]; SE bound {se_bound:.3f} pp [chair 0.52]; "
      f"power at {PRED} pp, p < .01: {power(se_bound):.3f} [chair 0.15]", flush=True)
OUT["power_notes"] = dict(residual_share=r4(share), se_bound_pp=r4(se_bound), power=r4(power(se_bound)))
if NOTES_ONLY:
    print("--notes-only: stopping before the outcome.", flush=True); sys.exit(0)

# ---------------------------------------------------------------- 3. the outcome: the key set only
raw = subprocess.run(["git", "-C", REPO, "show", "origin/main:studies/judging_data/hooktheory_covers_discogs.json"], capture_output=True, check=True).stdout
KEYS = set(json.loads(raw).keys()); del raw
y = np.array([100.0 if r["vid"] in KEYS else 0.0 for r in rows])
n1 = int((y > 0).sum())
print(f"OUTCOME: keys {len(KEYS)}; not among the {len(by)} surprise songs: {len(KEYS - set(by))} (diagnostic)", flush=True)
print(f"N = {NR} songs, {len(arts)} artists; y = 1: {n1} ({n1 / NR:.3f})", flush=True)
OUT["outcome"] = dict(keys=len(KEYS), keys_not_in_surprise=len(KEYS - set(by)), N=NR, artists=len(arts), y1=n1, share_y1=r4(n1 / NR))

# ---------------------------------------------------------------- 4. model
def lpm(Xm, yv, g):
    """within-artist OLS, no constant; CR1 by artist: G/(G-1) (N-1)/(N-K) (X'X)^-1 sum_g X_g'u_g u_g'X_g (X'X)^-1"""
    Xd = demean(Xm, g); yd = demean(yv, g)
    XtX_inv = np.linalg.inv(Xd.T @ Xd); b = XtX_inv @ Xd.T @ yd; u = yd - Xd @ b
    nobs, K = Xd.shape; G = len(np.unique(g))
    sc = np.zeros((g.max() + 1, K)); np.add.at(sc, g, Xd * u[:, None])
    V = G / (G - 1) * (nobs - 1) / (nobs - K) * XtX_inv @ (sc.T @ sc) @ XtX_inv
    se = np.sqrt(np.diag(V)); p = 2 * N.sf(np.abs(b / se))
    return b, se, p, Xd, yd, G

b, se, p, Xd, yd, G = lpm(X, y, gidx)
# cross-check with statsmodels cov_type="cluster" (df_correction=True)
import statsmodels.api as sm
smf = sm.OLS(yd, Xd).fit(cov_type="cluster", cov_kwds=dict(groups=gidx, df_correction=True))
print(f"cross-check statsmodels: beta {smf.params[0]:+.6f} vs {b[0]:+.6f}; SE {smf.bse[0]:.6f} vs {se[0]:.6f}", flush=True)
assert abs(smf.params[0] - b[0]) < 1e-8 and abs(smf.bse[0] - se[0]) < 1e-8
pw = power(se[0])
print(f"SE (clustered, CR1) of z(D): {se[0]:.4f} pp; power at {PRED} pp, p < .01 two-sided: {pw:.3f}", flush=True)
beta, ci = b[0], (b[0] - 1.959964 * se[0], b[0] + 1.959964 * se[0])
print(f"BETA z(D): {beta:+.4f} pp per SD (SE {se[0]:.4f}, p {p[0]:.4f}, 95% {ci[0]:+.3f} to {ci[1]:+.3f}); N {NR}, clusters {G}", flush=True)
OUT["primary"] = dict(beta_pp=r4(beta), se_pp=r4(se[0]), p=r4(p[0]), ci95=[r4(ci[0]), r4(ci[1])], N=NR, clusters=G, K=Xd.shape[1],
                      power_at_prediction=r4(pw), statsmodels_crosscheck=dict(beta=r4(smf.params[0]), se=r4(smf.bse[0])),
                      controls={n: dict(b=r4(bb_), se=r4(ss), p=r4(pp)) for n, bb_, ss, pp in zip(NAMES[1:], b[1:], se[1:], p[1:])})

half = lambda a: int(hashlib.md5(a.encode()).hexdigest(), 16) % 2
hv = np.array([half(a) for a in art_arr]); halves = []
for h in (0, 1):
    m = hv == h; gh = np.unique(gidx[m], return_inverse=True)[1]
    bh, sh, ph, _, _, Gh = lpm(X[m], y[m], gh)
    halves.append(dict(half=h, songs=int(m.sum()), artists=int(Gh), y1=int((y[m] > 0).sum()), beta=r4(bh[0]), se=r4(sh[0]), p=r4(ph[0])))
    print(f"  half {h}: {m.sum()} songs, {Gh} artists, y=1 {int((y[m] > 0).sum())}: beta {bh[0]:+.4f} (SE {sh[0]:.4f}, p {ph[0]:.4f})", flush=True)
OUT["halves"] = halves

# conditional logit: same columns, not demeaned, grouped by artist; artists all 0 or all 1 drop out
from statsmodels.discrete.conditional_models import ConditionalLogit
yb = (y > 0).astype(int)
gs = np.bincount(gidx, weights=yb); gn = np.bincount(gidx)
ok_g = (gs > 0) & (gs < gn); m = ok_g[gidx]
drop_a, drop_s = int((~ok_g).sum()), int((~m).sum())
print(f"CONDITIONAL LOGIT: drops {drop_a} artists and {drop_s} songs (all 0 or all 1; all-1: {int((gs == gn).sum())} artists); "
      f"keeps {int(ok_g.sum())} artists, {int(m.sum())} songs", flush=True)
Xm = X[m]; assert np.linalg.matrix_rank(demean(Xm, np.unique(gidx[m], return_inverse=True)[1])) == Xm.shape[1]
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    cl = ConditionalLogit(yb[m], Xm, groups=gidx[m])
    # ConditionalLogit.fit discards the optimiser's return values, so call the base LikelihoodModel.fit on the same model to read "converged"
    from statsmodels.base.model import LikelihoodModel
    fit = LikelihoodModel.fit(cl, start_params=np.zeros(Xm.shape[1]), method="bfgs", maxiter=2000, disp=False, full_output=True)
    conv = bool(fit.mle_retvals.get("converged", False)); meth = "bfgs"
    if not conv:
        fit = LikelihoodModel.fit(cl, start_params=fit.params, method="newton", maxiter=200, disp=False, full_output=True)
        conv = bool(fit.mle_retvals.get("converged", False)); meth = "bfgs+newton"
    fit_sm = cl.fit(method="bfgs", maxiter=2000, disp=False)   # the ConditionalLogit wrapper itself, as a cross-check of the coefficient
print(f"  ConditionalLogit.fit cross-check: coef z(D) {fit_sm.params[0]:+.4f}", flush=True)
grad = cl.score(fit.params); gmax = float(np.abs(grad).max())
print(f"  converged: {conv} ({meth}); max |score| {gmax:.2e}; coef z(D) {fit.params[0]:+.4f} (SE {fit.bse[0]:.4f}, p {fit.pvalues[0]:.4f})", flush=True)
OUT["conditional_logit"] = dict(coef=r4(fit.params[0]), se=r4(fit.bse[0]), p=r4(fit.pvalues[0]), converged=conv, method=meth, max_abs_score=gmax,
                                artists_dropped=drop_a, songs_dropped=drop_s, artists_kept=int(ok_g.sum()), songs_kept=int(m.sum()))

# verdict, by the rule as written
both_neg = all(h["beta"] < 0 for h in halves)
if beta < 0 and p[0] < ALPHA and both_neg and conv and fit.params[0] < 0: verdict = "pass"
elif beta > 0 and p[0] < ALPHA: verdict = "opposite sign (prediction killed; new hypothesis)"
elif beta > -0.3: verdict = "kill"
else: verdict = "unsettled"
print(f"VERDICT BY THE RULE: {verdict}", flush=True)
OUT["verdict_inputs"] = dict(beta_negative=bool(beta < 0), p_below_01=bool(p[0] < ALPHA), both_halves_negative=both_neg,
                             clogit_converged=conv, clogit_negative=bool(fit.params[0] < 0), beta_above_minus_0_3=bool(beta > -0.3))

# ---------------------------------------------------------------- 5. reported, deciding nothing
print("REPORTED, DECIDING NOTHING:", flush=True)
rep = {}
X2 = np.column_stack([X, z(col("ch_rep")), z(col("ch_ic_mean"))])
b2, s2, p2, *_ = lpm(X2, y, gidx)
rep["with_ch_rep_and_ch_ic_mean"] = dict(beta_zD=r4(b2[0]), se=r4(s2[0]), p=r4(p2[0]), ch_rep=r4(b2[-2]), ch_ic_mean=r4(b2[-1]))
print(f"  z(D) with ch_rep and ch_ic_mean added: {b2[0]:+.4f} (SE {s2[0]:.4f}, p {p2[0]:.4f}); ch_rep {b2[-2]:+.4f}, ch_ic_mean {b2[-1]:+.4f}", flush=True)
Xs = X.copy(); Xs[:, 0] = z(col("Ds")); b3_, s3, p3, *_ = lpm(Xs, y, gidx)
rep["signed_lnr_minus_ln432"] = dict(beta=r4(b3_[0]), se=r4(s3[0]), p=r4(p3[0]), note="positive = faster-than-habitual songs versioned more")
print(f"  signed ln r - ln 4.32 (z) in place of D: {b3_[0]:+.4f} (SE {s3[0]:.4f}, p {p3[0]:.4f})", flush=True)
for tag in ("mel", "ch"):
    v = np.array([np.nan if r["D_" + tag] is None else r["D_" + tag] for r in rows]); mm = ~np.isnan(v)
    Xv = X[mm].copy(); Xv[:, 0] = z(v[mm]); gv = np.unique(gidx[mm], return_inverse=True)[1]
    bv, sv, pv, *_ = lpm(Xv, y[mm], gv)
    rep[f"D_{tag}_term_alone"] = dict(beta=r4(bv[0]), se=r4(sv[0]), p=r4(pv[0]), songs=int(mm.sum()), ref_median=OUT["variant_refs"][tag]["median"])
    print(f"  D from the {tag} term alone (about its own clip median {OUT['variant_refs'][tag]['median']}): {bv[0]:+.4f} (SE {sv[0]:.4f}, p {pv[0]:.4f}), {mm.sum()} songs", flush=True)
OUT["reported_deciding_nothing"] = rep
finish(verdict)
