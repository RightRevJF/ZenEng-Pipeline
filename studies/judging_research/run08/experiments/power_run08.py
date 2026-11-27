"""Run 08 chair: power on FAKE outcomes on the real design, before any outcome is joined (no outcome is read).
Usage: python3 -I power_run08.py <part> ; part = scan_a | scan_b | other | final_a | final_b   (writes power_<part>.json here)

y_cov tests: common.fake_power's exact procedure (seed 11, 300 draws). The scan replicates its loop line for line, keeping every
draw's p and sign, so power can be read at every candidate alpha .05/K from one pass (the same draws common.fake_power makes);
'final' then calls common.fake_power itself at the frozen alpha, at comp_share 0.3 (the assumption) and 0.5 (sensitivity).
R08-I2 and the timeline test have their own fake-outcome simulations (below); their assumptions are stated in each PREDICTION.md.
"""
import sys, os, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import common as C, models08 as M8

HERE = C.HERE
SZ = ["ch_rep", "V", "ln_chg", "ln_bars"]
# name: (measure, frozen extra columns, predicted beta in SD of y_cov per SD of the measure)
TESTS = {
    "chrep_confirm":     ("ch_rep", [], -0.04),
    "key_travel":        ("TRAV5", ["TRAVL1"] + SZ, 0.05),
    "iiv_chunk":         ("IIV", ["w_chr"] + SZ, 0.04),
    "transport_economy": ("econ", ["w_chr"] + SZ, 0.03),
    "tonic_resistance":  ("H", SZ + ["H_links"], -0.03),
    "transposed_rep":    ("T_rep", SZ, 0.05),
    # qualified but waiting (ranked 9-11); power reported for the ranking only
    "obtuse_statue":     ("pmin", SZ + ["pmin_links"], -0.02),
    "loop_period":       ("lnP", SZ, 0.012),
    "burstiness":        ("B", SZ, 0.006),
}
KS = [1, 2, 3, 4, 5, 6, 7, 8]

def songs():
    info, S = C.load_design(); MS = json.load(open(os.path.join(C.DL, "choco", "measures_run08.json")))
    for s in S: s.update(MS["songs"][s["clique"]])
    return S, MS

def rows_for(S, meas, extra):
    return [s for s in S if all(s.get(c) is not None for c in [meas] + list(extra))]

def scan(S, meas, extra, beta, comp_share, draws=300, seed=11):
    """common.fake_power's loop, keeping each draw's (b, se, p)."""
    sign = np.sign(beta); rng = np.random.default_rng(seed); g = np.array([s["composer"] for s in S])
    X = np.column_stack([C.zs([s[meas] for s in S])] + [C.zs([s[e] for s in S]) for e in extra] + [C.dummies([s["genre"] for s in S])])
    ok = ~np.isnan(X).any(1); X, g2 = X[ok], g[ok]; z = X[:, 0]
    ug, inv = np.unique(g2, return_inverse=True); out = []
    for d in range(draws):
        u = rng.normal(0, math.sqrt(comp_share), len(ug))[inv]
        y = u + beta * z + rng.normal(0, math.sqrt(max(1 - comp_share - beta ** 2, 0.05)), len(z))
        b, se, p, N, G = C.ols_fe(y, X, g2); out.append((b[0], se[0], p[0]))
    a = np.array(out)
    return dict(power_at_K={K: float(np.mean((a[:, 2] < 0.05 / K) & (np.sign(a[:, 0]) == sign))) for K in KS},
                se_fake=float(np.median(a[:, 1])), N=int(ok.sum()), G=int(len(ug)), comp_share=comp_share, draws=draws)

# ---------------------------------------------------------------- R08-I2 heritability
def heritability_sim(S, MS, comp_share=0.3, draws=100, perms=200, target=0.06, seed=3, pseudo_decade=False):
    """fake y = composer effect (comp_share) + a * f + noise, f = z(x + mean of x over i's 10 neighbours), x iid N(0,1);
    a calibrated so the mean rho_nb is the predicted +0.06 (calibrated on raw rho_nb; the test reads the excess over the null mean). r = residual of y on composer FE + genre dummies (first year is not
    known before the outcome, so no decade bins here). Null SD from `perms` permutations within composer x genre cells;
    p = two-sided normal on excess / null SD (excess = rho_nb - null mean). Power = share of draws with p < alpha and excess > 0 (as common.fake_power: halves and the
    second model are not simulated; their rates are reported)."""
    NB = MS["neighbours"]; sd = {s["clique"]: s for s in S}
    order = [s["clique"] for s in S if NB.get(s["clique"])]
    A10, has = M8.nb_matrix(order, NB, 10); A5, has5 = M8.nb_matrix(order, NB, 5)
    comp = np.array([sd[q]["composer"] for q in order]); D = C.dummies([sd[q]["genre"] for q in order])
    cells = np.array([sd[q]["composer"] + "|" + sd[q]["genre"] for q in order]); half = np.array([C.halves(c) for c in comp])
    if pseudo_decade:   # sensitivity: the real cells add the decade (unknown now); each composer gets a base decade, each song
        rd = np.random.default_rng(77); uc = sorted(set(comp)); base = dict(zip(uc, rd.integers(0, 8, len(uc))))  # base +- N(0, 1)
        cells = np.array([c + "|" + str(base[sd[q]["composer"]] + int(round(rd.normal()))) for c, q in zip(cells, order)])
    Dw = C.within(D, comp); ug, inv = np.unique(comp, return_inverse=True); N = len(order)
    def resid(y):
        yw = C.within(y[:, None], comp)[:, 0]; b, *_ = np.linalg.lstsq(Dw, yw, rcond=None); return yw - Dw @ b
    rng = np.random.default_rng(seed)
    def fake(a):
        x = rng.normal(size=N); f = x + A10 @ x; f = (f - f.mean()) / f.std()
        return rng.normal(0, math.sqrt(comp_share), len(ug))[inv] + a * f + rng.normal(0, math.sqrt(max(1 - comp_share - a * a, 0.05)), N)
    grid = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55]; cal = {}
    for a in grid: cal[a] = float(np.mean([M8.rho_nb(resid(fake(a)), A10, has) for _ in range(20)]))
    a = min(grid, key=lambda v: abs(cal[v] - target))
    specs = [(A10, has, None), (A10, has, half == 0), (A10, has, half == 1), (A5, has5, None)]
    res = []
    for d in range(draws):
        T = M8.excess_test(resid(fake(a)), specs, cells, perms, seed=d)
        res.append([T[0]["excess"], T[0]["null_sd"], T[1]["excess"], T[2]["excess"], T[3]["excess"], T[0]["p"]])
    res = np.array(res); from scipy import stats
    p = 2 * stats.norm.sf(np.abs(res[:, 0] / res[:, 1]))          # normal approximation (200 permutations cannot resolve .01)
    pw = {K: float(np.mean((p < 0.05 / K) & (res[:, 0] > 0))) for K in KS}
    pw_full = {K: float(np.mean((p < 0.05 / K) & (res[:, 0] > 0) & (res[:, 2] > 0) & (res[:, 3] > 0) & (res[:, 4] > 0))) for K in KS}
    kill = float(np.mean(np.abs(target - res[:, 0]) > 1.96 * res[:, 1]))
    res0 = []
    for d in range(40):
        T = M8.excess_test(resid(fake(0.0)), specs[:1], cells, perms, seed=1000 + d); res0.append((T[0]["excess"], T[0]["null_sd"]))
    res0 = np.array(res0)
    return dict(power_at_K=pw, power_at_K_with_halves_and_K5=pw_full, kill_rate_if_true=kill,
                kill_rate_if_zero=float(np.mean(np.abs(target - res0[:, 0]) > 1.96 * res0[:, 1])),
                a=a, calibration=cal, mean_excess=float(res[:, 0].mean()), null_sd=float(res[:, 1].mean()), N=N, comp_share=comp_share,
                draws=draws, perms=perms)

# ---------------------------------------------------------------- the timeline test (card 2)
SCEN = {"low": (1.5, 3.0), "middle": (3.0, 6.0), "high": (4.0, 10.0)}
def timeline_sim(S, beta, mK, mL, draws=200, share=0.5, seed=4):
    """A fake urn on the real design. ASSUMPTIONS (the outcome is not open): a random half of the design songs have t0 in
    1950-1994 (the primary window), each kept only if its composer keeps two; 9 five-year cohorts, cohort effect 0.1 per bin;
    composer effect N(0, 0.5) on both K10 and (x0.3) L; K10 = 1 + Poisson(Gamma(shape 0.8, mean mK x composer)); L =
    Poisson(Gamma(shape 1.0, mean proportional to (K10+1)^beta x composer x cohort)), scaled so mean L = mL.
    Model: models08.poisson_fe(L, [log(K10+1), cohort dummies], composer). Pass: two-sided p of beta = 1 below alpha with beta > 1
    (and, reported, both halves > 1). Kill: 1.10 outside beta +- 1.96 se."""
    rng = np.random.default_rng(seed); out = []
    for d in range(draws):
        pick = [s for s in S if rng.random() < share]
        comp = np.array([s["composer"] for s in pick]); ug, inv = np.unique(comp, return_inverse=True)
        keep = np.bincount(inv)[inv] >= 2; comp = comp[keep]; ug, inv = np.unique(comp, return_inverse=True); n = len(comp)
        coh = rng.integers(0, 9, n); ce = rng.normal(0, .5, len(ug))[inv]
        K10 = 1 + rng.poisson(rng.gamma(0.8, mK * np.exp(ce - .125) / 0.8))
        base = (K10 + 1.0) ** beta; lam = base * np.exp(.3 * ce) * np.exp(.1 * coh); lam *= mL / lam.mean()
        L = rng.poisson(rng.gamma(1.0, lam))
        X = np.column_stack([np.log(K10 + 1.0), C.dummies(coh.astype(str).tolist())])
        b, se, N, G, it = M8.poisson_fe(L, X, comp)
        h = np.array([C.halves(x) for x in comp])
        hb = [M8.poisson_fe(L[h == k], X[h == k], comp[h == k])[0][0] for k in (0, 1)]
        out.append((b[0], se[0], M8.p_two(b[0], se[0], 1.0), min(hb), n))
    a = np.array(out)
    return dict(power_at_K={K: float(np.mean((a[:, 2] < 0.05 / K) & (a[:, 0] > 1))) for K in KS},
                power_at_K_with_halves={K: float(np.mean((a[:, 2] < 0.05 / K) & (a[:, 0] > 1) & (a[:, 3] > 1))) for K in KS},
                kill_rate=float(np.mean(np.abs(1.10 - a[:, 0]) > 1.96 * a[:, 1])), se_median=float(np.median(a[:, 1])),
                N_median=int(np.median(a[:, 4])), beta=beta, mean_K10_minus_1=mK, mean_L=mL, draws=draws)

if __name__ == "__main__":
    part = sys.argv[1]; S, MS = songs(); t0 = time.time(); res = {}
    if part in ("scan_a", "scan_b"):
        names = list(TESTS)[:5] if part == "scan_a" else list(TESTS)[5:]
        for k in names:
            m, ex, b = TESTS[k]; R = rows_for(S, m, ex)
            res[k] = {str(cs): scan(R, m, ex, b, cs) for cs in (0.3, 0.5)}
            print(k, res[k]["0.3"]["power_at_K"], round(time.time() - t0), flush=True)
    elif part == "herit_decade":
        res["heritability_pseudo_decade"] = heritability_sim(S, MS, 0.3, pseudo_decade=True)
        print(res["heritability_pseudo_decade"]["power_at_K"], round(time.time() - t0), flush=True)
    elif part == "other":
        res["heritability"] = {str(cs): heritability_sim(S, MS, cs) for cs in (0.3, 0.5)}
        res["heritability"]["0.3_pseudo_decade"] = heritability_sim(S, MS, 0.3, pseudo_decade=True)
        print("heritability", res["heritability"]["0.3"]["power_at_K"], round(time.time() - t0), flush=True)
        res["timeline"] = {sc: dict(fitness=timeline_sim(S, 1.10, *v), neutral=timeline_sim(S, 1.0, *v)) for sc, v in SCEN.items()}
        for sc in SCEN: print("timeline", sc, res["timeline"][sc]["fitness"]["power_at_K"], res["timeline"][sc]["neutral"]["kill_rate"], flush=True)
    elif part in ("final_a", "final_b"):
        K = int(sys.argv[2]); alpha = 0.05 / K
        names = list(TESTS)[:3] if part == "final_a" else list(TESTS)[3:6]
        for k in names:
            m, ex, b = TESTS[k]; R = rows_for(S, m, ex)
            res[k] = {str(cs): {kk: (float(v) if not isinstance(v, (int, str)) else v) for kk, v in
                                C.fake_power(R, m, ex, b, alpha, sign=np.sign(b), comp_share=cs).items()} for cs in (0.3, 0.5)}
            res[k]["alpha"] = alpha; res[k]["K"] = K
            print(k, res[k], round(time.time() - t0), flush=True)
    json.dump(res, open(os.path.join(HERE, f"power_{part}.json"), "w"), indent=1)
    print("done", part, round(time.time() - t0))
