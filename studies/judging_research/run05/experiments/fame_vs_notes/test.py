"""Run 05, fame_vs_notes: the Skeptic's fame-versus-notes test (card 2, Interiano et al. 2018), frozen in PREDICTION.md
(commit 1f6c36d) before any outcome was joined.

THE RULE (verbatim in substance from PREDICTION.md):
  Rows: run 04's 9,588 songs by 1,741 artists (common.load_rows()); songs with y_foreign = NaN dropped. Outcome y_foreign / 100.
  Blocks: (a) fame = ln(artist's songs among the 13,198 of the surprise file), ln(clips per song);
          (b) notes = the 17 data-pack measures (common.FE); (c) both.
  Folds: md5(artist) % 5. Per fold: standardise with mean / population SD of the other four folds, then NaN -> 0;
         LogisticRegression(C=1.0, max_iter=5000) on the other four folds; predict fold k. AUC on pooled out-of-fold predictions.
  D = AUC(a) - AUC(b); Delta = AUC(c) - AUC(a).
  Interval: artist bootstrap on the fixed out-of-fold predictions, rng = default_rng(0), 2,000 x rng.integers(0, G, G),
            0.357th to 99.643th percentile (level 1 - .05/7).
  PASS  : lower end of D's interval > 0 AND Delta < 0.01.
  KILL  : (Delta >= 0.01 AND lower end of Delta's interval > 0) OR D <= 0.
  Else UNSETTLED.
Reported, deciding nothing: AUCs with 95% intervals, log-loss, D and Delta per artist half, the same rule on y, the within-artist
partial R^2 of the clips dummies vs the 17 measures, the ch_rep x ln(artist songs) interaction, and a within-artist shuffle placebo.

Run as `python3 test.py` from this folder (`python3 test.py --fake` runs the whole pipeline on a random outcome and reads no outcome).
Single process: BLAS threads are pinned to 1. The bootstrap is vectorised (weighted Mann-Whitney AUC; checked against
sklearn's roc_auc_score on explicit resamples).

Data credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
             Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, hashlib, collections, warnings, time
import numpy as np
from scipy import sparse
from scipy.stats import spearmanr
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss
from sklearn.exceptions import ConvergenceWarning

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C

FAKE = "--fake" in sys.argv
NT = 7; ALPHA = 0.05 / NT
QLO, QHI = 0.357, 99.643          # percentiles as written in the rule (level 1 - .05/7)
B = 2000; NPLAC = 200; NFOLD = 5
FOLD_SIZES = [2069, 2072, 1739, 1772, 1936]
T0 = time.time()
r4 = C.r4
def say(*a): print(*a, flush=True)
OUT = dict(test="fame_vs_notes", rule_commit="1f6c36d", fake=FAKE, sklearn=sklearn.__version__, numpy=np.__version__)

# ------------------------------------------------------------------ 1. rows and predictor blocks (notes only)
D_ = C.load_rows(); rows, alls = D_["rows"], D_["allsongs"]
nart_all = collections.Counter(r["artist"] for r in alls)
art = np.array([r["artist"] for r in rows])
ln_art = np.log([nart_all[a] for a in art]); ln_clips = np.log([r["nclips"] for r in rows])
FAME = np.column_stack([ln_art, ln_clips]); FAME_NAMES = ["ln_artist_songs", "ln_clips_per_song"]
NOTES = np.array([[r[f] for f in C.FE] for r in rows], float)
nan_rows = int(np.isnan(NOTES).any(1).sum())
nan_cols = {f: int(n) for f, n in zip(C.FE, np.isnan(NOTES).sum(0))}
say(f"all songs {len(alls)} [13,198]; NaN rows in notes {nan_rows} [14]; NaN per column {nan_cols}")
assert len(alls) == 13198 and len(rows) == 9588 and len(set(art)) == 1741 and nan_rows == 14
assert all(nan_cols[f] == 14 for f in C.RF) and all(nan_cols[f] == 0 for f in C.FE[:8])
fold = np.array([int(hashlib.md5(a.encode()).hexdigest(), 16) % NFOLD for a in art])
fs = np.bincount(fold).tolist(); say(f"fold sizes {fs} [{FOLD_SIZES}]")
assert fs == FOLD_SIZES, "fold sizes do not reproduce the rule's unit values: stop"
half = np.array([r["half"] for r in rows])

# measure-side check (notes only): what the fame proxies overlap with among the notes. The rule sets no stop line here (no new
# measure is built), so this is printed for renaming awareness only.
ov = {}
for nm, x in zip(FAME_NAMES, FAME.T):
    ov[nm] = {f: r4(C.sp(x, NOTES[:, j])[0]) for j, f in enumerate(C.FE)}
    top = max(ov[nm], key=lambda k: abs(ov[nm][k]))
    say(f"  {nm}: largest |Spearman| with the 17 measures {top} {ov[nm][top]:+.3f}; with ch_rep {ov[nm]['ch_rep']:+.3f}")
rho_ff = r4(spearmanr(FAME[:, 0], FAME[:, 1])[0]); say(f"  ln_artist_songs vs ln_clips_per_song: {rho_ff:+.3f}")
OUT["notes_side"] = dict(rows=len(rows), artists=int(len(set(art))), all_songs=len(alls), notes_nan_rows=nan_rows,
                         fold_sizes=fs, fold_sizes_reproduced=True, fame_overlap_spearman=ov, fame_proxies_rho=rho_ff,
                         ln_artist_songs_range=[r4(ln_art.min()), r4(ln_art.max())])


# ------------------------------------------------------------------ machinery
def oof(X, y, fold_k):
    """out-of-fold probabilities, per the rule. Returns (p, n_convergence_warnings)."""
    p = np.zeros(len(y)); nw = 0
    for k in range(NFOLD):
        tr, te = fold_k != k, fold_k == k
        mu = np.nanmean(X[tr], 0); sd = np.nanstd(X[tr], 0)
        assert (sd > 0).all()
        Z = (X - mu) / sd; Z = np.where(np.isnan(Z), 0.0, Z)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", ConvergenceWarning)
            m = LogisticRegression(C=1.0, max_iter=5000).fit(Z[tr], y[tr])
            nw += sum(issubclass(x.category, ConvergenceWarning) for x in w)
        p[te] = m.predict_proba(Z[te])[:, 1]
    return p, nw

def draw_weights(g, seed=0):
    """the rule's artist bootstrap: rng = default_rng(seed); B times rng.integers(0, G, G). Returns (B x G counts, picks)."""
    G = int(g.max()) + 1; rng = np.random.default_rng(seed)
    picks = [rng.integers(0, G, G) for _ in range(B)]
    cnt = np.stack([np.bincount(pk, minlength=G) for pk in picks]).astype(np.float64)
    return cnt, picks

def wauc(y, p, W, chunk=250):
    """AUC of p for each row of song weights W (B x N): weighted Mann-Whitney with ties counted 1/2. With integer weights equal
    to resample counts this is exactly roc_auc_score on the resample with repeats."""
    uq, inv = np.unique(p, return_inverse=True); U = len(uq); n = len(p)
    pos = y == 1
    Mp = sparse.csr_matrix((np.ones(pos.sum()), (np.nonzero(pos)[0], inv[pos])), shape=(n, U))
    Mn = sparse.csr_matrix((np.ones((~pos).sum()), (np.nonzero(~pos)[0], inv[~pos])), shape=(n, U))
    out = np.empty(W.shape[0])
    for s in range(0, W.shape[0], chunk):
        Wc = W[s:s + chunk]
        P = np.asarray((Mp.T @ Wc.T).T); Nn = np.asarray((Mn.T @ Wc.T).T)
        below = np.cumsum(Nn, 1) - Nn
        out[s:s + chunk] = (P * (below + 0.5 * Nn)).sum(1) / (P.sum(1) * Nn.sum(1))
    return out

def pct(x, q): return float(np.percentile(x, q))

def analyse(yv, keep, label, placebo=False):
    """the whole frozen rule on outcome yv (0/1) over rows `keep`. Prints counts, SEs and power before any estimate."""
    t = time.time()
    y = yv[keep].astype(int); ak = art[keep]; fk = fold[keep]; hk = half[keep]
    codes = {a: i for i, a in enumerate(sorted(set(ak)))}; g = np.array([codes[a] for a in ak]); G = len(codes)
    Fa, Nb = FAME[keep], NOTES[keep]; Xc = np.column_stack([Fa, Nb])
    pa, wa = oof(Fa, y, fk); pb, wb = oof(Nb, y, fk); pc, wc = oof(Xc, y, fk)
    A = {k: roc_auc_score(y, p) for k, p in (("a", pa), ("b", pb), ("c", pc))}
    LL = {k: log_loss(y, p) for k, p in (("a", pa), ("b", pb), ("c", pc))}
    Dv, Dl = A["a"] - A["b"], A["c"] - A["a"]
    cnt, picks = draw_weights(g, 0); W = cnt[:, g]
    BA = {k: wauc(y, p, W) for k, p in (("a", pa), ("b", pb), ("c", pc))}
    # exactness check of the vectorised AUC against sklearn on explicit resamples (with repeats)
    by = [np.nonzero(g == k)[0] for k in range(G)]; chk = 0.0
    for i in range(3):
        ix = np.concatenate([by[k] for k in picks[i]])
        for k, p in (("a", pa), ("b", pb), ("c", pc)): chk = max(chk, abs(roc_auc_score(y[ix], p[ix]) - BA[k][i]))
    assert chk < 1e-10, chk
    bD, bDl = BA["a"] - BA["b"], BA["c"] - BA["a"]
    # ---- counts, SEs, power first
    fsz = np.bincount(fk, minlength=NFOLD).tolist()
    say(f"\n[{label}] N {len(y)} songs, {G} artists, y = 1: {int(y.sum())} ({100 * y.mean():.1f}%); fold sizes {fsz}; "
        f"convergence warnings {wa + wb + wc}")
    say(f"[{label}] bootstrap SE: D {bD.std(ddof=1):.4f}, Delta {bDl.std(ddof=1):.4f}  (rule's synthetic: about 0.02 and 0.005)")
    say(f"[{label}] power (rule, synthetic outcomes): fame-only world pass 6/6; notes add ~0.045 AUC kill 6/6; "
        f"boundary ~0.01 pass 4 / kill 1 / unsettled 3 of 8")
    # ---- estimates
    lD, hD = pct(bD, QLO), pct(bD, QHI); lDl, hDl = pct(bDl, QLO), pct(bDl, QHI)
    say(f"[{label}] AUC(a) fame {A['a']:.4f}  AUC(b) notes {A['b']:.4f}  AUC(c) both {A['c']:.4f}")
    say(f"[{label}] D = {Dv:+.4f}  interval [{lD:+.4f}, {hD:+.4f}];  Delta = {Dl:+.4f}  interval [{lDl:+.4f}, {hDl:+.4f}]")
    passed = bool(lD > 0 and Dl < 0.01); killed = bool((Dl >= 0.01 and lDl > 0) or Dv <= 0)
    assert not (passed and killed)
    verdict = "pass" if passed else ("kill" if killed else "unsettled")
    say(f"[{label}] VERDICT by the rule: {verdict.upper()}")
    res = dict(N=len(y), artists=G, y1=int(y.sum()), base_rate=r4(y.mean()), fold_sizes=fsz, convergence_warnings=wa + wb + wc,
               auc=dict(fame=r4(A["a"]), notes=r4(A["b"]), both=r4(A["c"])),
               auc_ci95={k2: [r4(pct(BA[k], 2.5)), r4(pct(BA[k], 97.5))] for k, k2 in (("a", "fame"), ("b", "notes"), ("c", "both"))},
               log_loss=dict(fame=r4(LL["a"]), notes=r4(LL["b"]), both=r4(LL["c"]),
                             base_rate_only=r4(log_loss(y, np.full(len(y), y.mean())))),
               D=r4(Dv), D_interval=[r4(lD), r4(hD)], D_boot_se=r4(bD.std(ddof=1)), D_ci95=[r4(pct(bD, 2.5)), r4(pct(bD, 97.5))],
               Delta=r4(Dl), Delta_interval=[r4(lDl), r4(hDl)], Delta_boot_se=r4(bDl.std(ddof=1)),
               Delta_ci95=[r4(pct(bDl, 2.5)), r4(pct(bDl, 97.5))],
               interval_percentiles=[QLO, QHI], bootstrap_draws=B, bootstrap_check_max_abs_diff=float(chk),
               pass_clause=dict(D_lower_above_0=bool(lD > 0), Delta_below_001=bool(Dl < 0.01)),
               kill_clause=dict(Delta_ge_001_and_lower_above_0=bool(Dl >= 0.01 and lDl > 0), D_le_0=bool(Dv <= 0)),
               verdict=verdict)
    # halves (fixed out-of-fold predictions)
    hv = {}
    for h in (0, 1):
        m = hk == h
        aa, ab, ac = (roc_auc_score(y[m], p[m]) for p in (pa, pb, pc))
        hv[f"half{h}"] = dict(N=int(m.sum()), artists=int(len(set(ak[m]))), y1=int(y[m].sum()),
                              auc_fame=r4(aa), auc_notes=r4(ab), auc_both=r4(ac), D=r4(aa - ab), Delta=r4(ac - aa))
        say(f"[{label}] half {h}: N {m.sum()}, AUC fame {aa:.4f} notes {ab:.4f} both {ac:.4f}; D {aa - ab:+.4f}, Delta {ac - aa:+.4f}")
    res["halves"] = hv
    if placebo:
        # 17 notes columns permuted within artist (a song's 17 values move together), rng = default_rng(s), s = 0..199
        srt = np.argsort(g, kind="stable"); dl = []
        for s in range(NPLAC):
            rng = np.random.default_rng(s)
            order = np.lexsort((rng.random(len(g)), g))     # within each artist, a random ordering of its songs
            perm = np.empty(len(g), int); perm[srt] = order
            assert (g[perm] == g).all()
            pcs, _ = oof(np.column_stack([Fa, Nb[perm]]), y, fk)
            dl.append(roc_auc_score(y, pcs) - A["a"])
        dl = np.array(dl)
        res["placebo"] = dict(draws=NPLAC, Delta_mean=r4(dl.mean()), Delta_p95=r4(pct(dl, 95)), Delta_sd=r4(dl.std(ddof=1)),
                              Delta_min=r4(dl.min()), Delta_max=r4(dl.max()), share_ge_observed=r4((dl >= Dl).mean()),
                              artist_level_share_of_Delta=r4(dl.mean() / Dl) if Dl > 0 else None)
        say(f"[{label}] placebo (notes shuffled within artist, {NPLAC}): Delta mean {dl.mean():+.4f}, 95th pct {pct(dl, 95):+.4f}, "
            f"share >= observed {(dl >= Dl).mean():.3f}")
    say(f"[{label}] {time.time() - t:.0f} s")
    return res


# ------------------------------------------------------------------ 2. fake random outcome first (no outcome file read)
fr = np.random.default_rng(12345); yfake = (fr.random(len(rows)) < 0.21).astype(float)
OUT["fake_check"] = analyse(yfake, np.ones(len(rows), bool), "FAKE random outcome", placebo=FAKE)
if FAKE:
    say("--fake: stopping before any outcome is read."); sys.exit(0)

# ------------------------------------------------------------------ 3. outcomes (refuses unless PREDICTION.md is committed)
S = C.load_outcomes(rows, HERE)
yf = np.array([r["y_foreign"] for r in rows], float); keep = np.isfinite(yf)
y_any = np.array([r["y"] for r in rows], float)
drop = collections.Counter(r["drop_reason"] for r in rows if r["drop_reason"])
say(f"\noutcomes: md5 {S['md5']}; y = 1: {S['y1']}; y_foreign = 1: {S['y_foreign1']}; dropped (y_foreign NaN): {S['drops']} {dict(drop)}")
OUT["outcomes"] = dict(md5=S["md5"], y1=S["y1"], y_foreign1=S["y_foreign1"], drops=S["drops"], drop_reasons=dict(drop),
                       N_kept=int(keep.sum()), artists_kept=int(len(set(art[keep]))))

# ------------------------------------------------------------------ 4-5. the frozen test
OUT["primary_y_foreign"] = analyse(yf / 100.0, keep, "y_foreign (DECIDES)", placebo=True)
OUT["verdict"] = OUT["primary_y_foreign"]["verdict"]

# ------------------------------------------------------------------ 6. reported, deciding nothing
OUT["reported_same_rule_on_y"] = analyse(y_any / 100.0, np.ones(len(rows), bool), "y, in Discogs-VI at all (reported)")

# within artist: partial R^2 of the clips dummies and of the 17-measure block (LPM, artist demeaning, y_foreign in points)
cn, CM = C.controls(rows)
def demean(M, g):
    M = np.asarray(M, float).reshape(len(M), -1); Gn = g.max() + 1; s = np.zeros((Gn, M.shape[1])); np.add.at(s, g, M)
    return M - (s / np.bincount(g, minlength=Gn)[:, None])[g]
def rss(X, y):
    b = np.linalg.lstsq(X, y, rcond=None)[0]; u = y - X @ b; return float(u @ u)
ak = art[keep]; codes = {a: i for i, a in enumerate(sorted(set(ak)))}; gk = np.array([codes[a] for a in ak])
Zn = np.column_stack([C.zs(NOTES[keep, j]) for j in range(NOTES.shape[1])]); nan_filled = int(np.isnan(Zn).sum()); Zn = np.nan_to_num(Zn)
Xw = demean(np.column_stack([Zn, CM[keep]]), gk); yw = demean(yf[keep], gk).ravel()
names = list(C.FE) + cn
iclip = [names.index(c) for c in ("clips2", "clips3", "clips4p")]; inotes = list(range(len(C.FE)))
full = rss(Xw, yw)
r_noclip = rss(np.delete(Xw, iclip, 1), yw); r_nonotes = rss(np.delete(Xw, inotes, 1), yw)
pr_clip = (r_noclip - full) / r_noclip; pr_notes = (r_nonotes - full) / r_nonotes
tss = float(yw @ yw)
say(f"\n[within artist] partial R^2: clips-per-song dummies {pr_clip:.5f}, 17 measures {pr_notes:.5f}; ratio fame/notes "
    f"{pr_clip / pr_notes:.2f} (Skeptic predicted >= 5); within R^2 full {1 - full / tss:.4f}")
OUT["reported_within_artist_partial_r2"] = dict(N=int(keep.sum()), artists=int(gk.max() + 1), clips_dummies=float(f"{pr_clip:.4g}"), notes17=float(f"{pr_notes:.4g}"),
                                                ratio_fame_over_notes=float(f"{pr_clip / pr_notes:.4g}"), within_r2_full=float(f"{1 - full / tss:.4g}"),
                                                rhythm_nan_cells_set_to_0=nan_filled, skeptic_predicted_ratio_at_least=5)

# interaction: run 04's model + z(ch_rep) x z(ln artist songs), z over the 9,588 rows; CR1 by artist
zr = C.zs([r["ch_rep"] for r in rows]); zi = C.zs([r["ch_ic_mean"] for r in rows]); zl = C.zs(ln_art)
Xi = np.column_stack([zr, zi, zr * zl, CM])
mi = C.lpm(Xi[keep], yf[keep], art[keep])
inter = dict(ch_rep=C.summ(mi, 0), ch_ic_mean=C.summ(mi, 1), ch_rep_x_ln_artist_songs=C.summ(mi, 2), N=mi["N"], G=mi["G"])
say(f"[interaction] ch_rep {inter['ch_rep']}; ch_rep x z(ln artist songs) {inter['ch_rep_x_ln_artist_songs']} (Skeptic predicted > 0)")
# ch_rep's slope (run 04's model, no interaction term) among songs of artists at or below the artist-level median of ln artist songs
arts_u = sorted(set(art)); med = float(np.median([np.log(nart_all[a]) for a in arts_u]))
low = keep & (ln_art <= med)
X4 = np.column_stack([zr, zi, CM]); ml = C.lpm(X4[low], yf[low], art[low])
m4 = C.lpm(X4[keep], yf[keep], art[keep])
inter.update(artist_median_ln_songs=r4(med), artist_median_songs=r4(np.exp(med)),
             low_fame_subset=dict(N=ml["N"], G=ml["G"], ch_rep=C.summ(ml, 0), ch_ic_mean=C.summ(ml, 1)),
             run04_model_all=dict(N=m4["N"], G=m4["G"], ch_rep=C.summ(m4, 0), ch_ic_mean=C.summ(m4, 1)))
say(f"[interaction] low-fame artists (ln songs <= {med:.3f}, i.e. <= {np.exp(med):.0f} songs): N {ml['N']}, ch_rep {inter['low_fame_subset']['ch_rep']}")
say(f"[interaction] run 04 model on all kept rows: ch_rep {inter['run04_model_all']['ch_rep']}")
OUT["reported_interaction"] = inter

# ------------------------------------------------------------------ 7. POST-HOC DIAGNOSTICS (added after the outcome was seen; decide nothing)
# Why AUC(fame) fell below 0.5 and where the notes' AUC comes from. Aggregates only; no per-song table.
yk = (yf[keep] > 0).astype(int); nk = np.round(np.exp(ln_art[keep])).astype(int); fk = fold[keep]
dg = dict(note="added after the outcome was seen; decides nothing")
dg["univariate_auc_fame_raw"] = dict(ln_artist_songs=r4(roc_auc_score(yk, ln_art[keep])), ln_clips_per_song=r4(roc_auc_score(yk, ln_clips[keep])))
bins = [(2, 2), (3, 3), (4, 5), (6, 9), (10, 19), (20, 49), (50, 10 ** 6)]
dg["rate_by_artist_song_count"] = [dict(songs_by_artist=f"{lo}-{hi}" if hi < 10 ** 6 else f"{lo}+", songs=int(((nk >= lo) & (nk <= hi)).sum()),
                                        artists=int(len(set(ak[(nk >= lo) & (nk <= hi)]))), y_foreign_share=r4(yk[(nk >= lo) & (nk <= hi)].mean()))
                                   for lo, hi in bins]
bigA = sorted({a for a in ak if nart_all[a] >= 50})
dg["artists_50plus_songs"] = dict(artists=len(bigA), songs=int(np.isin(ak, bigA).sum()),
                                  artists_with_zero_y_foreign=int(sum(yk[ak == a].sum() == 0 for a in bigA)))
pa_k, _ = oof(FAME[keep], yk, fk)
dg["fame_block_auc_by_test_fold"] = [r4(roc_auc_score(yk[fk == f], pa_k[fk == f])) for f in range(NFOLD)]
gm = np.array([codes[a] for a in ak]); cntg = np.bincount(gm)
uni = {}
for j, f in enumerate(C.FE):
    x = NOTES[keep, j]; ok = np.isfinite(x); xx = np.where(ok, x, np.nanmean(x)); am = (np.bincount(gm, weights=xx) / cntg)[gm]
    uni[f] = dict(raw=r4(roc_auc_score(yk[ok], x[ok])), within_artist=r4(roc_auc_score(yk, xx - am)), artist_mean=r4(roc_auc_score(yk, am)))
dg["univariate_auc_notes"] = uni
say("\n[post-hoc diagnostics, deciding nothing]")
say(f"  univariate AUC of raw fame proxies: {dg['univariate_auc_fame_raw']}")
for b_ in dg["rate_by_artist_song_count"]: say(f"  {b_}")
say(f"  artists with 50+ songs: {dg['artists_50plus_songs']}; fame-block AUC by test fold {dg['fame_block_auc_by_test_fold']}")
for f in sorted(uni, key=lambda f: -abs(uni[f]['raw'] - 0.5))[:6]: say(f"  {f}: {uni[f]}")
OUT["post_hoc_diagnostics"] = dg

OUT["runtime_s"] = round(time.time() - T0, 1)
json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1)
say(f"\nwrote result.json; verdict {OUT['verdict'].upper()}; {OUT['runtime_s']} s")
