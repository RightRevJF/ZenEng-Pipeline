"""Run 04, foreign_versions (sixth test, labelled 'after seeing results'): is move_extensive's +1.19 for chord repetition (ch_rep) on
"in Discogs-VI at all" carried by versions from OTHER performers (y_foreign), or by the original artist's own credit variants (y_self)?
The rule is PREDICTION.md in this folder (frozen and committed in 4410a0e before this outcome was built). It reuses
../move_extensive/test.py (rule 00ab557) with only the outcome changed: rows, columns, model, controls, halves and conditional logit are
the same code. Order:
  1. rows and measures from the notes;  2. move_extensive's gate (notes only, unchanged);
  3. the outcome: y (key set) and its split into own / foreign performer sets; drops printed (more than 25 -> "not run");
  4. counts of y_foreign = 100, y_self = 100 and the dropped count;  5. SE and power;  6. beta, p, 95% range; halves; conditional logit; verdict;
  7. result.json; then the items reported, deciding nothing (beta on y_self and the additivity check among them).
Data are read with `git show origin/main:studies/judging_data/...` from the repository this file sits in.
Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI (CC BY-SA 4.0).
python3 test.py -> result.json in this folder"""
import json, gzip, io, collections, re, hashlib, os, sys, time, subprocess, urllib.parse, warnings
import numpy as np
from scipy.stats import norm as N, spearmanr
from scipy.optimize import minimize

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
GIT = lambda path: subprocess.run(["git", "-C", HERE, "show", f"origin/main:studies/judging_data/{path}"], check=True, capture_output=True).stdout
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF   # run 03's 17 data-pack measures
MEAS = ["ch_rep", "ch_ic_mean"]
ALPHA = 0.05 / 6; ZC = float(N.isf(ALPHA / 2))   # .05/6 = .0083, two-sided, z 2.638
PRED, KILL = 0.9, 0.3
OUT = dict(rule="PREDICTION.md in this folder, commit 4410a0e (reuses ../move_extensive/test.py, rule 00ab557, outcome changed)",
           label="after seeing results", data="origin/main studies/judging_data (git show)",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)")
r4 = lambda x: None if x is None else round(float(x), 4)
def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", json.dumps(verdict), flush=True)

# ---------------------------------------------------------------- 1. rows and measures from the notes
raw_s, raw_r = GIT("hooktheory_surprise.json.gz"), GIT("hooktheory_rhythm.json.gz")
md5 = [hashlib.md5(raw_s).hexdigest(), hashlib.md5(raw_r).hexdigest()]
assert md5[0].startswith("ff7b9d37") and md5[1].startswith("1d6e0405"), md5
S = json.load(gzip.open(io.BytesIO(raw_s)))
RH = {r["k"]: r for r in json.load(gzip.open(io.BytesIO(raw_r)))}
print(f"surprise clips {len(S)}, rhythm rows {len(RH)}; md5 {md5}", flush=True)

by = collections.OrderedDict()   # vid -> clips in file order
for c in S: by.setdefault(c["vid"], []).append(c)

def toks(slug):
    u = urllib.parse.unquote(slug).lower(); b = re.sub(r"\([^)]*\)", " ", u)
    t = [x for x in re.split(r"[^a-z0-9]+", b) if x]
    return u, (t or [x for x in re.split(r"[^a-z0-9]+", u) if x])

SF = ["n_ch", "beats", "ch_ic_sd"] + FE[:8]
allsongs = []
for vid, cs in by.items():
    w = np.array([c["n_mel"] for c in cs], float)
    avg = (lambda v: float(np.average(v, weights=w))) if w.sum() > 0 else (lambda v: float(np.mean(v)))
    r = {f: avg([c[f] for c in cs]) for f in SF}
    rc = [(c, RH[c["k"]]) for c in cs if c["k"] in RH]   # rhythm: weighted by n_mel over the clips that have a rhythm row
    for f in RF:
        if not rc: r[f] = np.nan; continue
        wr = np.array([c["n_mel"] for c, _ in rc], float); v = [h[f] for _, h in rc]
        r[f] = float(np.average(v, weights=wr)) if wr.sum() > 0 else float(np.mean(v))
    u, t = toks(cs[0]["song"])
    r.update(vid=vid, artist=cs[0]["artist"], slug=cs[0]["song"], nclips=len(cs), wzero=bool(w.sum() == 0), u=u, tokens=t, key="-".join(t),
             clip12=[(cs[0]["ch_rep"], cs[1]["ch_rep"]), (cs[0]["ch_ic_mean"], cs[1]["ch_ic_mean"])] if len(cs) >= 2 else None)
    allsongs.append(r)
keyart = collections.defaultdict(set)
for r in allsongs: keyart[r["key"]].add(r["artist"])
for r in allsongs: r["rep_title"] = len(keyart[r["key"]]) >= 2
nart = collections.Counter(r["artist"] for r in allsongs)
rows = [r for r in allsongs if nart[r["artist"]] >= 2]
arts = sorted(set(r["artist"] for r in rows)); half = lambda a: int(hashlib.md5(a.encode()).hexdigest(), 16) % 2
for r in rows: r["half"] = half(r["artist"])
n = len(rows)
print(f"songs {len(allsongs)} [chair 13,198], artists {len(nart)} [5,351]; kept {n} songs [9,588], {len(arts)} artists [1,741]; "
      f"songs with zero weight: {sum(r['wzero'] for r in rows)} [0]; halves {sum(half(a) == 0 for a in arts)} / {sum(half(a) == 1 for a in arts)} artists [886 / 855]", flush=True)

zs = lambda x: (np.asarray(x, float) - np.mean(x)) / np.std(x)
Z = {f: zs([r[f] for r in rows]) for f in MEAS}
nch = np.array([r["n_ch"] for r in rows]); binv = np.digitize(nch, [5, 7, 9, 11, 13, 16, 20, 25, 32])
ncl = np.array([r["nclips"] for r in rows]); ntk = np.array([len(r["tokens"]) for r in rows])
bins_c = np.bincount(binv, minlength=10); cl_c = [int((ncl == 1).sum()), int((ncl == 2).sum()), int((ncl == 3).sum()), int((ncl >= 4).sum())]
wc_c = [int((ntk == k).sum()) for k in (1, 2, 3, 4)] + [int((ntk >= 5).sum())]
par = np.array([("(" in r["u"]) for r in rows], float); rep = np.array([r["rep_title"] for r in rows], float)
print(f"n_ch bins {bins_c.tolist()} [341, 672, 1553, 1160, 1174, 1429, 1597, 811, 464, 387]", flush=True)
print(f"clips 1/2/3/4+ {cl_c} [5317, 2533, 1123, 615]; words 1/2/3/4/5+ {wc_c} [1931, 2454, 1907, 1396, 1900]; "
      f"parentheses {int(par.sum())} [109]; repeated title {int(rep.sum())} [960]", flush=True)
OUT["rows"] = dict(songs_all=len(allsongs), artists_all=len(nart), songs=n, artists=len(arts), nch_bins=bins_c.tolist(), clips_classes=cl_c,
                   word_counts=wc_c, parentheses=int(par.sum()), repeated_title=int(rep.sum()),
                   artists_per_half=[sum(half(a) == h for a in arts) for h in (0, 1)])

CB = {f"nch_bin{k}": (binv == k).astype(float) for k in range(1, 10)}
CC = {"clips2": (ncl == 2).astype(float), "clips3": (ncl == 3).astype(float), "clips4p": (ncl >= 4).astype(float)}
CL = {"ln_beats": np.log([r["beats"] for r in rows])}
CT = {**{f"words{k}": (ntk == k).astype(float) for k in (1, 2, 3, 4)}, "parens": par, "rep_title": rep}
def design(meas=MEAS, title=True, clips="dummies"):
    cols = {f"z_{f}": Z[f] for f in meas}; cols.update(CB)
    cols.update(CC if clips == "dummies" else {"ln_clips": np.log(ncl.astype(float))}); cols.update(CL)
    if title: cols.update(CT)
    return list(cols), np.column_stack(list(cols.values()))
NAMES, X = design()
print(f"columns ({len(NAMES)}): {NAMES}", flush=True)

# ---------------------------------------------------------------- 2. GATE (no outcome loaded)
cc = {}
pr = [r["clip12"] for r in rows if r["clip12"]]
for i, f in enumerate(MEAS):
    cc[f] = float(spearmanr([p[i][0] for p in pr], [p[i][1] for p in pr])[0])
g1 = all(v >= 0.20 for v in cc.values())
print(f"GATE 1, clip-to-clip (clip 1 vs clip 2, {len(pr)} pairs [4,271]): ch_rep {cc['ch_rep']:.4f} [0.324], ch_ic_mean {cc['ch_ic_mean']:.4f} [0.496]; "
      f"needs >= 0.20 each -> {'pass' if g1 else 'FAIL'}", flush=True)

def sp(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float); ok = ~(np.isnan(a) | np.isnan(b))
    return float(spearmanr(a[ok], b[ok])[0]), int(ok.sum())
others = {f: [r[f] for r in rows] for f in FE}; others.update(n_ch=nch, beats=[r["beats"] for r in rows], clips_per_song=ncl)
ov = {}; norh = sum(np.isnan(r[RF[0]]) for r in rows)
for f in MEAS:
    ov[f] = {k: sp(Z[f], v) for k, v in others.items() if k != f}
g2 = True
for f in MEAS:
    top = max(ov[f], key=lambda k: abs(ov[f][k][0])); g2 &= abs(ov[f][top][0]) <= 0.7
    print(f"GATE 2, overlap of {f}: largest |Spearman| {top} {ov[f][top][0]:+.4f} (needs <= 0.7) "
          f"[chair {'ch_h_mean -0.44' if f == 'ch_rep' else 'ch_h_mean +0.48'}]; all: "
          + json.dumps({k: round(v[0], 3) for k, v in ov[f].items()}), flush=True)
print(f"  ch_rep vs ch_ic_mean {ov['ch_rep']['ch_ic_mean'][0]:+.4f} [chair -0.33]; songs without any rhythm row (left out of the rhythm correlations): {norh}", flush=True)
# extra, printed deciding nothing: the other model columns (dummies, ln beats, title flags)
extra = {f: {k: round(sp(Z[f], v)[0], 4) for k, v in {**CB, **CC, **CL, **CT}.items()} for f in MEAS}
ext_max = {f: max(extra[f].items(), key=lambda kv: abs(kv[1])) for f in MEAS}
print(f"  deciding nothing, largest |Spearman| with the model's other columns (dummies, ln beats, title flags): {ext_max}", flush=True)
icsd = sp([r["ch_ic_mean"] for r in rows], [r["ch_ic_sd"] for r in rows])[0]
print(f"  printed, deciding nothing: ch_ic_mean vs ch_ic_sd {icsd:+.4f} [chair +0.78] (outside the 17 and outside the model)", flush=True)
OUT["gate"] = dict(clip_to_clip=dict(pairs=len(pr), rho={k: r4(v) for k, v in cc.items()}, threshold=0.20, passed=bool(g1)),
                   overlap={f: dict(rho={k: [r4(v[0]), v[1]] for k, v in ov[f].items()}, threshold=0.7) for f in MEAS},
                   overlap_passed=bool(g2), songs_without_rhythm=int(norh),
                   deciding_nothing=dict(other_model_columns_largest=ext_max, ch_ic_mean_vs_ch_ic_sd=r4(icsd)), passed=bool(g1 and g2))
print(f"GATE: {'PASSED' if g1 and g2 else 'FAILED'}", flush=True)
if not (g1 and g2):
    finish("stopped (gate failed; no outcome joined)"); sys.exit(0)

# notes-side power bound (no outcome needed), as in the rule's table
art = np.array([r["artist"] for r in rows]); code = {a: i for i, a in enumerate(arts)}; g = np.array([code[a] for a in art]); G = len(arts)
cnt = np.bincount(g)
def dm(M):
    M = np.asarray(M, float); M2 = M.reshape(len(M), -1); s = np.zeros((G, M2.shape[1]))
    np.add.at(s, g, M2); out = M2 - (s / cnt[:, None])[g]
    return out.reshape(M.shape)
Xd = dm(X)
for i, f in enumerate(MEAS):
    o = np.delete(Xd, i, 1); x = Xd[:, i]; xt = x - o @ np.linalg.lstsq(o, x, rcond=None)[0]
    se_b = np.sqrt(0.21 * 0.79 / (xt @ xt)) * 100
    print(f"notes-side: {f} within-artist residual share {xt @ xt / n:.3f} [{'0.412' if i == 0 else '0.530'}], SE bound {se_b:.3f} pp", flush=True)
    OUT.setdefault("notes_side_power", {})[f] = dict(residual_share=r4(xt @ xt / n), se_bound_pp=r4(se_b))


# ---------------------------------------------------------------- 3. outcome: y (key set) and its split into own and foreign performer sets
if os.environ.get("GATE_ONLY"): print("GATE_ONLY: stopping before the outcome", flush=True); sys.exit(0)
nrm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))   # covers_match_discogs.py's rule, no unquoting
if os.environ.get("FAKE_Y"):   # code check on a random fake outcome (no outcome file read); writes nothing in this folder
    _rs = np.random.default_rng(1); HERE = os.environ["FAKE_Y"]; CV, VC = {}, {}
    for i_, r in enumerate(allsongs):
        if _rs.random() < 0.2:
            cq = f"c{i_}"; CV[r["vid"]] = {"clique": cq}
            if _rs.random() < 0.0005: continue                                        # clique missing from the versions file
            own = [r["artist"].replace("-", " ").title()] if _rs.random() > 0.0005 else ["Nobody Here"]   # no own set
            sets = [own]
            if _rs.random() < 0.4: sets.append(own + ["Some Guest"])
            if _rs.random() < 0.5 + 0.05 * Z["ch_rep"][0]: sets.append(["Other Band"])
            if _rs.random() < 0.05: sets.append(["Karaoke Kings"])
            if _rs.random() < 0.05: sets.append(["Some Guest"])
            VC[cq] = {"versions": [[s, 2000, [1]] for s in sets]}
    md5o = ["fake", "fake"]
else:
    _a, _b = GIT("hooktheory_covers_discogs.json"), GIT("discogs_versions_matched.json")
    md5o = [hashlib.md5(_a).hexdigest(), hashlib.md5(_b).hexdigest()]
    CV = json.loads(_a); VC = json.loads(_b)["cliques"]; del _a, _b
KEYS = set(CV)
KT = lambda s: any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in s)
y = np.zeros(n); yf = np.zeros(n); yloose = np.zeros(n); ykt = np.zeros(n); keepr = np.ones(n, bool); drops = []
empty_names = 0
for i_, r in enumerate(rows):
    if r["vid"] not in KEYS: continue
    y[i_] = 100.0
    cq = CV[r["vid"]].get("clique")
    if cq not in VC:
        keepr[i_] = False; drops.append(dict(vid=r["vid"], artist=r["artist"], slug=r["slug"], clique=cq, why="clique missing from the versions file")); continue
    sets = [e[0] for e in VC[cq]["versions"]]; a = nrm(r["artist"])
    empty_names += sum(1 for s in sets for nm in s if nrm(nm) == "")
    own = [s for s in sets if any(nrm(nm) == a for nm in s)]
    if not own:
        keepr[i_] = False; drops.append(dict(vid=r["vid"], artist=r["artist"], slug=r["slug"], clique=cq, why="no own set",
                                              sets=[list(s) for s in sets][:8])); continue
    O = {nrm(nm) for s in own for nm in s}
    foreign = [s for s in sets if len(s) > 0 and not any(nrm(nm) in O for nm in s)]
    yf[i_] = 100.0 if foreign else 0.0
    yloose[i_] = 100.0 if [s for s in sets if len(s) > 0 and a not in {nrm(nm) for nm in s}] else 0.0
    ykt[i_] = 100.0 if [s for s in foreign if not KT(s)] else 0.0
ys = y - yf
allv = set(r["vid"] for r in allsongs)
print(f"\nOUTCOME FILES md5 {md5o}; keys {len(KEYS)}, keys not among the {len(allv)} surprise songs: {len(KEYS - allv)}; cliques in the versions file {len(VC)}", flush=True)
print(f"DROPS (matched model songs with no own set, or clique missing): {len(drops)}", flush=True)
for d_ in drops: print("  dropped:", json.dumps(d_, ensure_ascii=False), flush=True)
OUT["drops"] = dict(count=len(drops), limit=25, songs=drops)
if len(drops) > 25:
    finish("not run (more than 25 songs dropped)"); sys.exit(0)

# every model below runs on the same kept rows (columns and their z-scores are move_extensive's, over the 9,588)
k_ = keepr; Xk_, artk, HVk = X[k_], np.array([r["artist"] for r in rows])[k_], np.array([r["half"] for r in rows])[k_]
y, yf, ys, yloose, ykt = y[k_], yf[k_], ys[k_], yloose[k_], ykt[k_]
art = artk; X = Xk_; nk = len(y)
arts_k = sorted(set(art)); code = {a: i for i, a in enumerate(arts_k)}; g = np.array([code[a] for a in art]); G = len(arts_k); cnt = np.bincount(g)
def dm(M):
    M = np.asarray(M, float); M2 = M.reshape(len(M), -1); s = np.zeros((G, M2.shape[1]))
    np.add.at(s, g, M2); out = M2 - (s / cnt[:, None])[g]
    return out.reshape(M.shape)
print(f"\nCOUNTS (on the {nk} kept songs, {G} artists): y = 100 {int((y > 0).sum())}; y_foreign = 100 {int((yf > 0).sum())}; "
      f"y_self = 100 {int((ys > 0).sum())}; dropped {len(drops)}; names that normalise to '' {empty_names}", flush=True)
assert np.all((ys == 0) | (ys == 100)) and np.all(yf <= y)
OUT["outcome"] = dict(N=nk, artists=G, y1=int((y > 0).sum()), y_foreign1=int((yf > 0).sum()), y_self1=int((ys > 0).sum()), dropped=len(drops),
                      share_y_foreign=r4((yf > 0).mean()), share_y_self=r4((ys > 0).mean()), keys=len(KEYS), keys_not_in_surprise=len(KEYS - allv),
                      names_normalising_to_empty=empty_names, outcome_md5=md5o)

def lpm(Xm, yv, gv):
    """within-artist OLS of yv on Xm, CR1 by artist: G/(G-1) (N-1)/(N-K) (X'X)^-1 sum_g X_g'u_g u_g'X_g (X'X)^-1"""
    codes = {a: i for i, a in enumerate(sorted(set(gv)))}; gg = np.array([codes[a] for a in gv]); Gn = len(codes); c_ = np.bincount(gg)
    def d(M):
        M2 = np.asarray(M, float).reshape(len(M), -1); s = np.zeros((Gn, M2.shape[1])); np.add.at(s, gg, M2); return M2 - (s / c_[:, None])[gg]
    Xw, yw = d(Xm), d(yv).ravel(); Nn, K = Xw.shape
    XtXi = np.linalg.inv(Xw.T @ Xw); b = XtXi @ Xw.T @ yw; u = yw - Xw @ b
    sc = np.zeros((Gn, K)); np.add.at(sc, gg, Xw * u[:, None])
    V = Gn / (Gn - 1) * (Nn - 1) / (Nn - K) * XtXi @ (sc.T @ sc) @ XtXi
    se = np.sqrt(np.diag(V)); p = 2 * N.sf(np.abs(b / se))
    return dict(b=b, se=se, p=p, N=Nn, G=Gn, K=K, Xw=Xw, yw=yw, gg=gg)
def summ(m, i): return dict(beta=r4(m["b"][i]), se=r4(m["se"][i]), p=float(f"{m['p'][i]:.4g}"), ci95=[r4(m["b"][i] - 1.96 * m["se"][i]), r4(m["b"][i] + 1.96 * m["se"][i])])

M = lpm(X, yf, art)
try:
    import statsmodels.api as sm
    smf = sm.OLS(M["yw"], M["Xw"]).fit(cov_type="cluster", cov_kwds={"groups": M["gg"], "df_correction": True})
    xchk = dict(max_abs_beta_diff=float(np.max(np.abs(smf.params - M["b"]))), max_abs_se_diff=float(np.max(np.abs(smf.bse - M["se"]))))
except Exception as e:
    xchk = dict(error=repr(e))
OUT["statsmodels_crosscheck_lpm"] = xchk

# ---------------------------------------------------------------- 5. SE and power first (y_foreign)
se = M["se"][0]
power = dict(se=r4(se), power_at_pred=r4(N.cdf(PRED / se - ZC) + N.cdf(-PRED / se - ZC)),
             power_at_pred_p05=r4(N.cdf(PRED / se - 1.96) + N.cdf(-PRED / se - 1.96)),
             kill_fires_if_true_is_pred=r4(N.cdf((KILL - PRED) / se)), kill_fires_if_true_is_zero=r4(N.cdf(KILL / se)),
             se_ch_ic_mean=r4(M["se"][1]))
print(f"POWER ch_rep on y_foreign: clustered SE {se:.4f} pp [rule: <= 0.50]; power at +{PRED} pp, p < .0083: {power['power_at_pred']:.3f} [about 0.20]; "
      f"at p < .05: {power['power_at_pred_p05']:.3f}; kill line (beta < +0.3) fires {power['kill_fires_if_true_is_pred']:.3f} if +0.9 is true [about 0.12], "
      f"{power['kill_fires_if_true_is_zero']:.3f} if the true effect is 0 [about 0.73]", flush=True)
print(f"  (SE for ch_ic_mean on y_foreign {M['se'][1]:.4f}; CR1 by hand vs statsmodels cluster SE: {xchk})", flush=True)
OUT["power"] = power

# ---------------------------------------------------------------- 6. beta, halves, conditional logit, verdict
OUT["primary_y_foreign"] = {f: summ(M, i) for i, f in enumerate(MEAS)}
i = 0
print(f"PRIMARY LPM ch_rep on y_foreign: beta {M['b'][i]:+.4f} pp per SD (predicted +{PRED}; artefact story < +{KILL}), SE {M['se'][i]:.4f}, "
      f"p {M['p'][i]:.4g}, 95% range {M['b'][i] - 1.96 * M['se'][i]:+.4f} to {M['b'][i] + 1.96 * M['se'][i]:+.4f}", flush=True)
print(f"  N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = HVk == h; HM[h] = lpm(X[s], yf[s], art[s])
    d = dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], y_foreign1=int((yf[s] > 0).sum()), ch_rep=summ(HM[h], 0))
    OUT["halves"].append(d)
    print(f"HALF {h}: {HM[h]['N']} songs, {HM[h]['G']} artists, y_foreign=1 {d['y_foreign1']}; ch_rep beta {HM[h]['b'][0]:+.4f} "
          f"(SE {HM[h]['se'][0]:.4f}, p {HM[h]['p'][0]:.3g})", flush=True)

yb = (yf > 0).astype(int); ga = np.bincount(g, weights=yb); keep_g = (ga > 0) & (ga < cnt); keep = keep_g[g]
drop_art, drop_songs = int(G - keep_g.sum()), int((~keep).sum())
print(f"CONDITIONAL LOGIT (y_foreign): drops {drop_art} artists and {drop_songs} songs (all 0 or all 1); keeps {int(keep_g.sum())} artists, {int(keep.sum())} songs", flush=True)
sys.setrecursionlimit(max(10000, 4 * int(cnt.max())))
from statsmodels.discrete.conditional_models import ConditionalLogit
Xk, yk, gk = X[keep], yb[keep], g[keep]
const_cols = [NAMES[j] for j in range(X.shape[1]) if np.all(dm(X)[keep][:, j] == 0)]
cl = dict(dropped_artists=drop_art, dropped_songs=drop_songs, kept_artists=int(keep_g.sum()), kept_songs=int(keep.sum()), columns_without_within_variation=const_cols)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    mod = ConditionalLogit(yk, Xk, groups=gk)
    # statsmodels' ConditionalResults drops the optimiser's flag, so convergence is judged by the score on the scale statsmodels
    # optimises (-loglike/nobs): max |score|/nobs < 1e-5. If BFGS fails it, Newton from the BFGS point.
    fit = mod.fit(method="bfgs", maxiter=2000, disp=False); how = "bfgs"
    conv = bool(np.max(np.abs(mod.score(fit.params))) / mod.nobs < 1e-5)
    if not conv:
        fit = mod.fit(start_params=fit.params, method="newton", maxiter=100, disp=False); how = "bfgs then newton"
        conv = bool(np.max(np.abs(mod.score(fit.params))) / mod.nobs < 1e-5)
grad = float(np.max(np.abs(mod.score(fit.params))))
cl.update(converged=conv, optimiser=how, max_abs_score=grad, convergence_test="max|score|/nobs < 1e-5", llf=float(fit.llf))
for i, f in enumerate(MEAS):
    cl[f] = dict(coef=r4(fit.params[i]), se=r4(fit.bse[i]), p=float(f"{fit.pvalues[i]:.4g}"))
    print(f"  {f}: coef {fit.params[i]:+.4f} (log-odds per SD), SE {fit.bse[i]:.4f}, p {fit.pvalues[i]:.4g}", flush=True)
print(f"  converged: {conv}; max |score| {grad:.2e}; columns with no within-artist variation in its sample: {const_cols}", flush=True)

# cross-check: the same likelihood by the subset recursion (elementary symmetric sums), Newton
def cl_own(Xk, yk, gk):
    grp = [np.nonzero(gk == a)[0] for a in np.unique(gk)]
    def f_g_h(b):
        ll = 0.0; gr = np.zeros(len(b)); H = np.zeros((len(b), len(b)))
        for ix in grp:
            x = Xk[ix]; k = int(yk[ix].sum()); eta = x @ b; c = eta.max(); w = np.exp(eta - c); p_ = len(b)
            E = np.zeros(k + 1); E[0] = 1; D = np.zeros((k + 1, p_)); Hh = np.zeros((k + 1, p_, p_))
            for t in range(len(ix)):
                xt = x[t]; wt = w[t]
                Hh[1:] = Hh[1:] + wt * (Hh[:-1] + np.outer(xt, xt)[None] * E[:-1, None, None] + xt[None, :, None] * D[:-1, None, :] + D[:-1, :, None] * xt[None, None, :])
                D[1:] = D[1:] + wt * (D[:-1] + E[:-1, None] * xt[None])
                E[1:] = E[1:] + wt * E[:-1]
            e, dd, hh = E[k], D[k], Hh[k]
            ll += yk[ix] @ eta - (np.log(e) + k * c); m = dd / e
            gr += yk[ix] @ x - m; H -= hh / e - np.outer(m, m)
        return ll, gr, H
    b = np.zeros(Xk.shape[1])
    for it in range(50):
        ll, gr, H = f_g_h(b); step = np.linalg.solve(H, gr)
        while True:
            nb = b - step
            if f_g_h(nb)[0] >= ll - 1e-10: break
            step /= 2
        b = nb
        if np.max(np.abs(step)) < 1e-9: break
    ll, gr, H = f_g_h(b)
    return b, np.sqrt(np.diag(np.linalg.inv(-H))), float(np.max(np.abs(gr))), it + 1
try:
    bo, so, go, ito = cl_own(Xk, yk, gk)
    cl["own_recursion_crosscheck"] = dict(ch_rep=r4(bo[0]), ch_ic_mean=r4(bo[1]), se=[r4(so[0]), r4(so[1])], max_abs_score=go, newton_iters=ito,
                                          max_abs_diff_vs_statsmodels=float(np.max(np.abs(bo - fit.params))),
                                          all_coefs={nm_: [r4(a_), r4(b_)] for nm_, a_, b_ in zip(NAMES, fit.params, bo)},
                                          all_coefs_note="[statsmodels BFGS, own recursion Newton] per column")
    big = [(nm_, r4(a_), r4(b_)) for nm_, a_, b_ in zip(NAMES, fit.params, bo) if abs(a_ - b_) > 0.01]
    print(f"  columns where the two fits differ by > 0.01: {big}", flush=True)
    print(f"  cross-check (own recursion, Newton {ito} steps, max |score| {go:.1e}): ch_rep {bo[0]:+.4f}, ch_ic_mean {bo[1]:+.4f}; "
          f"max |diff| vs statsmodels {np.max(np.abs(bo - fit.params)):.2e}", flush=True)
except Exception as e:
    cl["own_recursion_crosscheck"] = dict(error=repr(e))
OUT["conditional_logit_y_foreign"] = cl

b, p = M["b"][0], M["p"][0]; hb = [HM[h]["b"][0] for h in (0, 1)]; cb = fit.params[0]
if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0 and conv and cb > 0: v = "pass (a lead needing fresh songs; the artefact story dies)"
elif b < KILL: v = "kill (beta < +0.3 pp): the sign was the original artist's own credit variants"
else:
    why = []
    if not p < ALPHA: why.append("p >= .0083")
    if not (hb[0] > 0 and hb[1] > 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb > 0: why.append("conditional logit sign disagrees")
    v = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (ch_rep on y_foreign): {v}", flush=True)
OUT["prediction_pp_per_sd"] = PRED; OUT["kill_below_pp"] = KILL; OUT["threshold_p"] = ALPHA; OUT["threshold_z"] = ZC

# ---------------------------------------------------------------- 7. result.json; then reported, deciding nothing
dn = {}
MS, MY = lpm(X, ys, art), lpm(X, y, art)
add = float(np.max(np.abs(M["b"] + MS["b"] - MY["b"])))
dn["y_self"] = dict(count1=int((ys > 0).sum()), **{f: summ(MS, i) for i, f in enumerate(MEAS)})
dn["y_on_the_same_rows"] = dict(count1=int((y > 0).sum()), **{f: summ(MY, i) for i, f in enumerate(MEAS)})
dn["additivity_check"] = dict(max_abs_diff_all_columns=add, tolerance=1e-9, holds=bool(add < 1e-9),
                              ch_rep=[r4(M["b"][0]), r4(MS["b"][0]), r4(MY["b"][0])], note="[beta_foreign, beta_self, beta_y]")
ML = lpm(X, yloose, art); dn["foreign_looser_a_not_in_set"] = dict(count1=int((yloose > 0).sum()), **{f: summ(ML, i) for i, f in enumerate(MEAS)})
MK = lpm(X, ykt, art); dn["foreign_without_karaoke_tribute_sets"] = dict(count1=int((ykt > 0).sum()), **{f: summ(MK, i) for i, f in enumerate(MEAS)})
dn["ch_ic_mean_on_y_foreign"] = summ(M, 1)
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k, v_ in dn.items(): print(f"  {k}: {json.dumps(v_)}", flush=True)
OUT["reported_deciding_nothing"] = dn
finish(v)
