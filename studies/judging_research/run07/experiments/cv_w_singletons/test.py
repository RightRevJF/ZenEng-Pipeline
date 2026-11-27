"""Run 07, cv_w_singletons: WRITTEN AFTER SEEING RESULTS by the first-principles reviewer (a pass is only a lead).
The rule is PREDICTION.md in this folder: the night's 9th test, p < .05/9 two-sided. The eight earlier tests keep .05/8.
NOT RUN by its author. Run only after PREDICTION.md and ../common.py are committed (common.guard refuses otherwise):
    python3 -I test.py  ->  result.json in this folder
Songs: the Lakh songs of common.lakh_songs() whose artist has ONE song (dropped there by the within-artist step), less any song
that shares a MIDI file with a within-artist song. Across songs, not within artist: OLS with HC1 errors (= CR1 by artist here)."""
import os, sys, json, math, collections, hashlib, warnings
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from scipy import stats
import common as C

N_TESTS = 9; ALPHA = 0.05 / N_TESTS                       # the 9th test of run 07; the eight frozen tests keep .05/8
MEAS, EXTRA, PRED, SIGN = "cv_w", ("H4m", "ch_rep"), 1.5, 1  # the tree_h4m model in which cv_w was read (+3.11), across songs
SHAPE_CACHE = os.path.join(C.DL, "lakh", "shapes_run07_singletons.json")     # notes only
OUT_CACHE = os.path.join(C.DL, "lakh", "outcomes_run07_singletons.json")     # written by the guarded join; NOT the within-artist cache
WITHIN_CACHE = os.path.join(C.DL, "lakh", "outcomes_run07.json")             # the 5,901 seen songs (only their clique ids are read)


def all_songs():
    """common.lakh_songs() step for step (same exclusions, same per-song means), but returning every song BEFORE the
    within-artist step. singleton_songs() checks that its within-artist part equals common.lakh_songs() exactly."""
    notes = json.load(open(os.path.join(C.DL, "lakh", "notes.json")))
    HT, MG = C._hooktheory_keys(), C._mcgill_keys()
    owners = collections.defaultdict(set)
    for n in notes: owners[n["md5"]].add(C.nrm(C.clean(n["title"])))
    by = collections.OrderedDict(); used = set()
    for n in sorted(notes, key=lambda x: x["tid"]):
        if len(owners[n["md5"]]) > 1: continue
        if C.COVER_ARTISTS.search(n["artist"] or ""): continue
        a, tc, tx = C.nrm(n["artist"]), C.nrm(C.clean(n["title"])), C.nrm(n["title"])
        if not a or not tc: continue
        if (a, tc) in HT or (a, tx) in HT: continue
        if (a, tc) in MG or (a, tx) in MG: continue
        if n["n_bars"] < 8 or len(n["toks"]) < 5: continue
        if (a, tc, n["md5"]) in used: continue
        used.add((a, tc, n["md5"])); by.setdefault((a, tc), []).append(n)
    songs = []
    for (a, tc), tr in by.items():
        ms = [C.track_measures(x) for x in tr]
        s = dict(key=f"{a}|{tc}", artist_key=a, title_key=tc, artist=tr[0]["artist"], title=C.clean(tr[0]["title"]),
                 tids=[x["tid"] for x in tr], md5s=[x["md5"] for x in tr], n_tracks=len(tr),
                 year=min([x["year"] for x in tr if x["year"]], default=0),
                 bb=any(x["bb"] for x in tr), hot=max([x["hot"] for x in tr if x["hot"] is not None], default=None), half=C.half_of(a))
        for m in C.MEASURES:
            v = np.array([d[m] for d in ms], float); v = v[np.isfinite(v)]
            s[m] = float(v.mean()) if len(v) else np.nan
        songs.append(s)
    return songs


def singleton_songs(verbose=True):
    songs = all_songs()
    cnt = collections.Counter(s["artist_key"] for s in songs)
    within = {s["key"] for s in C.lakh_songs(verbose=False)}
    assert {s["key"] for s in songs if cnt[s["artist_key"]] >= 2} == within, "all_songs() does not reproduce common.lakh_songs()"
    within_md5 = {m for s in songs if cnt[s["artist_key"]] >= 2 for m in s["md5s"]}
    single = [s for s in songs if cnt[s["artist_key"]] == 1]
    shared = [s for s in single if set(s["md5s"]) & within_md5]
    keep = [s for s in single if not (set(s["md5s"]) & within_md5)]
    if verbose:
        print(f"songs {len(songs)}; within-artist {len(within)}; single-song artists {len(single)}; "
              f"dropped for sharing a MIDI file with a within-artist song {len(shared)}; kept {len(keep)}", flush=True)
    return keep, len(shared)


# ====================================================================== across-song model
def design(songs, extra=EXTRA, add=None):
    cols = [C.zcol(songs, MEAS)] + [C.zcol(songs, e) for e in extra] + [C.zcol(songs, b) for b in C.BASE]
    X = np.column_stack(cols + [C.year_dummies(songs)])
    return X if add is None else np.column_stack([X, add])

def ols_hc1(X, y):
    """OLS with an intercept; HC1 errors (with one song per artist these equal CR1 by artist). Returns b, se, p, N for column 0."""
    X = np.asarray(X, float); y = np.asarray(y, float); ok = np.isfinite(y) & np.isfinite(X).all(1); X, y = X[ok], y[ok]
    keep = X.std(0) > 1e-12; keep[0] = True; X = np.column_stack([X[:, keep], np.ones(len(y))])
    XtX = np.linalg.pinv(X.T @ X); b = XtX @ X.T @ y; u = y - X @ b; N, K = X.shape
    V = XtX @ (X.T * u ** 2) @ X @ XtX * N / (N - K); se = math.sqrt(V[0, 0])
    return dict(b=float(b[0]), se=float(se), p=float(2 * stats.norm.sf(abs(b[0] / se))), N=int(N))

def logit_sign(X, y):
    """statsmodels Logit on y/100 with an intercept; Newton, then BFGS (maxiter 2000). Converged only if statsmodels says so and
    raises no ConvergenceWarning. Returns coef on column 0, p, converged."""
    import statsmodels.api as sm
    from statsmodels.tools.sm_exceptions import ConvergenceWarning
    X = np.asarray(X, float); ok = np.isfinite(y) & np.isfinite(X).all(1); X, yb = X[ok], (y[ok] > 0).astype(float)
    keep = X.std(0) > 1e-12; keep[0] = True; X = sm.add_constant(X[:, keep], prepend=False)
    last = (float("nan"), float("nan"), False)
    for kw in (dict(method="newton", maxiter=200), dict(method="bfgs", maxiter=2000)):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try: r = sm.Logit(yb, X).fit(disp=0, **kw)
            except Exception: continue
        conv = bool(r.mle_retvals.get("converged", False)) and not any(issubclass(x.category, ConvergenceWarning) for x in w)
        last = (float(r.params[0]), float(r.pvalues[0]), conv)
        if conv: return last
    return last

def fake_power(songs, beta, alpha, base=0.40, draws=400, seed=7):
    """fake outcomes on the real rows and columns: y ~ Bernoulli(base + beta/100 * z). Pass = two-sided p < alpha, the predicted
    sign, and the same sign in both artist halves (the logit is not simulated). base 0.40 = the realised rate on the 5,901 seen songs."""
    rng = np.random.default_rng(seed); X = design(songs); ok = np.isfinite(X).all(1); X = X[ok]
    hv = np.array([s["half"] for s in songs])[ok]; z = X[:, 0]
    def one(bb):
        y = 100.0 * (rng.random(len(z)) < np.clip(base + bb / 100 * z, 0, 1)); r = ols_hc1(X, y)
        good = r["p"] < alpha and np.sign(r["b"]) == SIGN
        for h in (0, 1):
            if good: good &= np.sign(ols_hc1(X[hv == h], y[hv == h])["b"]) == SIGN
        return good, r["se"]
    A = [one(beta) for _ in range(draws)]; Z0 = [one(0.0) for _ in range(draws // 2)]
    return dict(power=float(np.mean([a[0] for a in A])), false_pass=float(np.mean([a[0] for a in Z0])),
                se=float(np.mean([a[1] for a in A])), base=base, draws=draws)


# ====================================================================== the test
def main():
    C.guard(HERE)                                   # PREDICTION.md and ../common.py committed and unmodified, or no outcome
    S, n_shared_file = singleton_songs()
    S = C.add_shapes(S, cache=SHAPE_CACHE)
    pw = fake_power(S, PRED, ALPHA)
    print("POWER (before the estimate):", pw, flush=True)
    C.OUT_CACHE = OUT_CACHE                         # a separate cache: the within-artist cache holds only the 5,901 seen songs
    info = C.load_outcomes(S, HERE)
    seen_cliques = {v["clique"] for v in json.load(open(WITHIN_CACHE))["songs"].values() if v.get("clique") is not None}
    shared_clique = np.array([s.get("clique") is not None and s["clique"] in seen_cliques for s in S])
    Sall = S; S = [s for s, f in zip(Sall, shared_clique) if not f]
    y = lambda songs, k="y_foreign": np.array([s[k] for s in songs], float)
    X = design(S)
    main_ = ols_hc1(X, y(S))
    halves = [ols_hc1(X[np.array([s["half"] == h for s in S])], y(S)[np.array([s["half"] == h for s in S])]) for h in (0, 1)]
    lg = logit_sign(X, y(S))
    hot = np.array([s["hot"] if s["hot"] is not None else np.nan for s in S], float)
    fame = np.column_stack([[float(s["bb"]) for s in S], np.nan_to_num(hot, nan=np.nanmean(hot)), np.isnan(hot).astype(float)])
    style = np.column_stack([C.zcol(S, "F"), np.nan_to_num(C.zcol(S, "ln_tempo"), nan=0.0), np.isnan(C.zcol(S, "ln_tempo")).astype(float)])
    fpm = C.first_performer_mask(S)
    readings = dict(
        on_y=ols_hc1(X, y(S, "y")),
        fame_held=ols_hc1(design(S, add=fame), y(S)),
        style_held_F_tempo=ols_hc1(design(S, add=style), y(S)),
        first_performers=ols_hc1(X[fpm], y(S)[fpm]),
        bare_no_extras=ols_hc1(design(S, extra=()), y(S)),
        shared_cliques_kept=ols_hc1(design(Sall), y(Sall)))
    passed = (main_["p"] < ALPHA and np.sign(main_["b"]) == SIGN and all(np.sign(h["b"]) == SIGN for h in halves)
              and np.sign(lg[0]) == SIGN and lg[2])
    killed = main_["b"] <= 0
    verdict = "PASS (a lead only: written after seeing results)" if passed else ("KILLED" if killed else "UNSETTLED")
    if killed and main_["p"] < ALPHA: verdict += " (opposite sign at p < alpha: reported as a new hypothesis, not a finding)"
    R = dict(test="cv_w_singletons", written_after_seeing_results=True, measure=MEAS, extra=list(EXTRA), prediction=PRED, sign=SIGN,
             alpha=ALPHA, n_tests=N_TESTS, power=pw, outcome_info=info, dropped_shared_file=n_shared_file,
             dropped_shared_clique=int(shared_clique.sum()), rows=len(S), main=main_, halves=halves,
             logit=dict(coef=lg[0], p=lg[1], converged=lg[2]), readings=readings, verdict=verdict,
             base_rate=float(np.nanmean(y(S))))
    json.dump(R, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float)
    print(json.dumps(R, indent=1, default=float)); print("VERDICT:", verdict)


if __name__ == "__main__":
    main()
