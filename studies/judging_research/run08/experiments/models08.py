"""Run 08 models, frozen by the chair before any outcome is joined (no outcome is read here).

poisson_fe    Poisson pseudo-likelihood (QMLE) with a fixed effect per group (composer), the group effects concentrated out
              (Hausman-Hall-Griliches / Wooldridge 1999); cluster-robust (by group) sandwich SEs with G/(G-1). The second model of
              every y_cov test (on n_sets) and the timeline test's primary model (on L).
rho_nb        R08-I2 heritability statistic: corr(r_i, mean of r over i's neighbours), and its permutation null within cells.
urn_ceiling   card 2 (c): the content-share ceiling from a Polya urn that keeps each song's K10 and each cohort's total of late sets.
timeline_counts  K10, L (and the second model's K15, L15) from a song's sorted artist-set years and its t0.
"""
import math, collections
import numpy as np
from scipy import stats

def poisson_fe(y, X, g, maxit=100, tol=1e-10):
    y = np.asarray(y, float); X = np.asarray(X, float); g = np.asarray(g)
    if X.ndim == 1: X = X[:, None]
    ug, inv = np.unique(g, return_inverse=True)
    ysum = np.bincount(inv, weights=y, minlength=len(ug))
    keep = ysum[inv] > 0                                      # groups with no events carry no information on beta
    y, X, inv = y[keep], X[keep], inv[keep]
    ug2, inv = np.unique(inv, return_inverse=True); G = len(ug2); ysum = np.bincount(inv, weights=y, minlength=G)
    var = X.std(0) > 1e-12
    for j in np.nonzero(var)[0]:                              # drop columns constant within every group
        m = np.bincount(inv, weights=X[:, j], minlength=G) / np.bincount(inv, minlength=G)
        if np.abs(X[:, j] - m[inv]).max() < 1e-12: var[j] = False
    Xk = X[:, var]; k = Xk.shape[1]; b = np.zeros(k)
    def parts(b):
        eta = Xk @ b; eta -= eta.max()
        e = np.exp(eta); esum = np.bincount(inv, weights=e, minlength=G)
        mu = e * (ysum / esum)[inv]
        musum = np.bincount(inv, weights=mu, minlength=G)
        xbar = np.column_stack([np.bincount(inv, weights=mu * Xk[:, j], minlength=G) for j in range(k)]) / musum[:, None]
        Xc = Xk - xbar[inv]
        return mu, Xc
    for it in range(maxit):
        mu, Xc = parts(b)
        s = Xc.T @ (y - mu); H = (Xc * mu[:, None]).T @ Xc
        step = np.linalg.solve(H + 1e-12 * np.eye(k), s); b = b + step
        if np.abs(step).max() < tol: break
    mu, Xc = parts(b); H = (Xc * mu[:, None]).T @ Xc; Hi = np.linalg.pinv(H)
    sc = Xc * (y - mu)[:, None]
    Sg = np.column_stack([np.bincount(inv, weights=sc[:, j], minlength=G) for j in range(k)])
    V = Hi @ (Sg.T @ Sg) @ Hi * (G / (G - 1))
    se = np.sqrt(np.diag(V))
    bb = np.full(X.shape[1], np.nan); ss = bb.copy(); bb[var] = b; ss[var] = se
    return bb, ss, int(len(y)), int(G), int(it + 1)

def p_two(b, se, null=0.0):
    return float(2 * stats.norm.sf(abs((b - null) / se)))

# ---------------------------------------------------------------- R08-I2
def nb_matrix(order, nb, K):
    """row-normalised neighbour-mean operator over the songs in `order` (neighbours outside `order` are ignored)."""
    from scipy import sparse
    ix = {q: i for i, q in enumerate(order)}; r, c = [], []
    for q in order:
        js = [ix[j] for j, _ in nb.get(q, [])[:K] if j in ix]
        for j in js: r.append(ix[q]); c.append(j)
    A = sparse.csr_matrix((np.ones(len(r)), (r, c)), shape=(len(order), len(order)))
    deg = np.asarray(A.sum(1)).ravel(); has = deg > 0
    A = sparse.diags(1 / np.maximum(deg, 1)) @ A
    return A.tocsr(), has

def rho_nb(r, A, has, mask=None):
    m = A @ r; ok = has if mask is None else (has & mask)
    return float(np.corrcoef(r[ok], m[ok])[0, 1])

def perm_null(r, specs, cells, n, seed=8):
    """r permuted within cells (an array of cell labels). specs = list of (A, has, mask); returns an (n, len(specs)) array of null
    values of rho_nb, one column per spec, all from the same permutations. The permutation keeps each cell's values (the scene
    held by the cells), so the null is centred on the cell-level part of rho_nb, not on 0: the test reads the EXCESS
    rho_nb - mean(null), and its 95% range is excess +- 1.96 SD(null)."""
    rng = np.random.default_rng(seed); idx = collections.defaultdict(list)
    for i, c in enumerate(cells): idx[c].append(i)
    groups = [np.array(v) for v in idx.values() if len(v) > 1]
    out = np.empty((n, len(specs)))
    for t in range(n):
        rp = r.copy()
        for gi in groups: rp[gi] = r[rng.permutation(gi)]
        for k, (A, has, mask) in enumerate(specs): out[t, k] = rho_nb(rp, A, has, mask)
    return out

def excess_test(r, specs, cells, n, seed=8):
    """for each spec: observed rho_nb, null mean, null SD, excess = observed - null mean, two-sided p about the null mean
    = (1 + #{|null - mean| >= |excess|}) / (n + 1)."""
    nul = perm_null(r, specs, cells, n, seed); out = []
    for k, (A, has, mask) in enumerate(specs):
        obs = rho_nb(r, A, has, mask); m = float(nul[:, k].mean()); sd = float(nul[:, k].std()); ex = obs - m
        p = float((1 + np.sum(np.abs(nul[:, k] - m) >= abs(ex))) / (n + 1))
        out.append(dict(rho_nb=obs, null_mean=m, null_sd=sd, excess=ex, p=p))
    return out

# ---------------------------------------------------------------- the timeline test (card 2)
def timeline_counts(years, t0):
    """years: sorted earliest years of the clique's artist sets (None dropped); t0 = first year.
    K10 = sets with earliest year <= t0 + 9; L = sets with earliest year in t0+10 .. t0+29.
    Second model: K15 = sets <= t0 + 14; L15 = sets in t0+15 .. t0+34."""
    y = np.asarray(years, float)
    return dict(K10=int((y <= t0 + 9).sum()), L=int(((y >= t0 + 10) & (y <= t0 + 29)).sum()),
                K15=int((y <= t0 + 14).sum()), L15=int(((y >= t0 + 15) & (y <= t0 + 34)).sum()))

def urn_ceiling(K10, L, cohort, c0=1.0, reps=200, seed=5):
    """card 2 (c). Observed: residual variance of log(L+1) after OLS on cohort dummies and K10 dummies (1..14, 15+). Urn: within each
    cohort, the cohort's observed total of late sets is dealt one by one to its songs with probability proportional to (K + c0),
    K starting at K10 and growing by each set dealt (a Polya urn; the shared aging curve is absorbed by the fixed cohort totals).
    ceiling = (observed residual variance - mean urn residual variance) / observed residual variance."""
    K10 = np.asarray(K10, int); L = np.asarray(L, int); cohort = np.asarray(cohort)
    kd = np.minimum(K10, 15)
    D = np.column_stack([np.ones(len(L))] + [(cohort == c).astype(float) for c in sorted(set(cohort))[1:]] +
                        [(kd == k).astype(float) for k in sorted(set(kd))[1:]])
    def rv(Lv):
        y = np.log(Lv + 1.0); b, *_ = np.linalg.lstsq(D, y, rcond=None); return float((y - D @ b).var())
    obs = rv(L); rng = np.random.default_rng(seed); sims = []
    cells = {c: np.nonzero(cohort == c)[0] for c in set(cohort.tolist())}
    for t in range(reps):
        Ls = np.zeros(len(L), int)
        for c in sorted(cells):
            ix = cells[c]; w = K10[ix].astype(float) + c0; tot = int(L[ix].sum())
            # a Polya urn (each dealt set adds one to its song's weight) ends Dirichlet-multinomial(tot, w): drawn exactly that way
            Ls[ix] = rng.multinomial(tot, rng.dirichlet(w))
        sims.append(rv(Ls))
    u = float(np.mean(sims))
    return dict(obs_resid_var=obs, urn_resid_var=u, urn_resid_var_sd=float(np.std(sims)), ceiling=(obs - u) / obs, reps=reps, c0=c0)
