"""Run 06: power from fake outcomes on the real designs (notes only; no outcome file is read). python3 power_fake.py -> power_fake.json
For each counted test (and the reported CH-on-fresh reading), on the test's own rows and columns:
  y ~ Bernoulli(p_i) x 100. 'homogeneous': p_i = 0.22 + beta/100 * z_i. 'calibrated': each artist draws p_a ~ Beta(0.22*phi, 0.78*phi),
  phi = 1.25, and p_i = p_a * (1 + beta/100 * z_i / 0.22); phi was chosen so that run 05's arrow_of_time design gives the clustered SE
  that run 05 actually observed (0.40 pp; the homogeneous world gives 0.54). z_i is the tested measure (fresh and seen rows alike).
  1,000 draws with beta = the prediction and 1,000 with beta = 0. Reported: the share of draws that pass (two-sided p < .05/6 with the
  predicted sign and the same sign in both artist halves; the conditional logit is not simulated), the share where the kill line fires,
  the share significant with the opposite sign, and the median clustered SE."""
import os, sys, json, numpy as np
from scipy.stats import norm as N
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

def demean(M, g):
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); c = np.bincount(gg)
    M = np.asarray(M, float).reshape(len(g), -1); s = np.zeros((len(codes), M.shape[1])); np.add.at(s, gg, M); return M - (s / c[:, None])[gg], gg

def prep(X, g):
    Xw, gg = demean(X, g); keep = np.where(np.abs(Xw).sum(0) > 1e-12)[0]; assert keep[0] == 0
    Xw = Xw[:, keep]; XtXi = np.linalg.pinv(Xw.T @ Xw); Nn, K = Xw.shape; Gn = gg.max() + 1
    return dict(Xw=Xw, P=XtXi @ Xw.T, h=Xw @ XtXi[0], gg=gg, c=Gn / (Gn - 1) * (Nn - 1) / (Nn - K), Gn=Gn)

def fit(pp, Y):
    Yw, _ = demean(Y, pp["gg"]); B = pp["P"] @ Yw; U = Yw - pp["Xw"] @ B
    sc = np.zeros((pp["Gn"], Y.shape[1])); np.add.at(sc, pp["gg"], pp["h"][:, None] * U)
    return B[0], np.sqrt(pp["c"] * (sc ** 2).sum(0))

def notes_bound(X, g):
    Xw, _ = demean(X, g); x = Xw[:, 0]; o = Xw[:, 1:]; o = o[:, np.abs(o).sum(0) > 1e-12]
    xt = x - o @ np.linalg.lstsq(o, x, rcond=None)[0]; return float(np.sqrt(0.22 * 0.78) * 100 / np.sqrt(xt @ xt))

def simulate(X, g, half, effcol, pred, kill, D=1000, phi=None, base=0.22, seed=0):
    rs = np.random.default_rng(seed); arts = sorted(set(g)); ai = {a: i for i, a in enumerate(arts)}; gi = np.array([ai[a] for a in g])
    pp = prep(X, g); ph = {h: prep(X[half == h], np.asarray(g)[half == h]) for h in (0, 1)}; out = {}
    for lab, beta in (("true", pred), ("zero", 0.0)):
        pa = np.full((len(arts), D), base) if phi is None else rs.beta(base * phi, (1 - base) * phi, size=(len(arts), D))
        p = pa[gi]
        p = np.clip(p + beta / 100 * effcol[:, None], 0, 1) if phi is None else np.clip(p * (1 + beta / 100 * effcol[:, None] / base), 0, 1)
        Y = 100.0 * (rs.random(p.shape) < p)
        b, se = fit(pp, Y); bh = [fit(ph[h], Y[half == h])[0] for h in (0, 1)]
        sig = np.abs(b / se) > N.isf(C.ALPHA / 2); s = np.sign(pred)
        passed = sig & (np.sign(b) == s) & (np.sign(bh[0]) == s) & (np.sign(bh[1]) == s)
        out[lab] = dict(pass_rate=round(float(passed.mean()), 3), kill_rate=round(float(kill(b).mean()), 3),
                        opposite_sign_significant=round(float((sig & (np.sign(b) == -s)).mean()), 3), se_median=round(float(np.median(se)), 3))
    return out

if __name__ == "__main__":
    B = C.battery(); seen9, rows = B["seen_rows"], B["rows"]
    seen9_vids = {r["vid"] for r in seen9}; seen9 = [r for r in B["seen_all"] if r["vid"] in seen9_vids]
    C.add_measures(B["seen_all"] + B["fresh_rows"])
    for r in seen9: r["half"] = C.half_of(r["artist"])
    z = lambda Rb, nm: (np.array([r[nm] for r in Rb], float) - C.seen_sd(seen9, nm)[0]) / C.seen_sd(seen9, nm)[1]
    RES = {}
    def run(name, X, Rb, effcol, pred, kill):
        g = [r["artist"] for r in Rb]; half = np.array([r["half"] for r in Rb])
        h = simulate(X, g, half, effcol, pred, kill, phi=None, seed=1); c = simulate(X, g, half, effcol, pred, kill, phi=1.25, seed=2)
        f = sum(r.get("fresh", 0) for r in Rb)
        RES[name] = dict(rows=len(Rb), fresh_rows=f, artists=len(set(g)), prediction=pred, notes_bound_se=round(notes_bound(X, g), 3), homogeneous=h, calibrated=c,
                         power_at_threshold_calibrated=round(C.power(pred, c["zero"]["se_median"], C.ALPHA), 3),
                         power_at_05_calibrated=round(C.power(pred, c["zero"]["se_median"], 0.05), 3))
        print(name, json.dumps(RES[name]), flush=True)
    # chirality: seen within-artist rows with CH
    R9 = [r for r in seen9 if np.isfinite(r["CH"])]; cn, cx = C.controls(R9)
    X = np.column_stack([z(R9, "CH"), z(R9, "A"), z(R9, "ch_rep"), z(R9, "ch_ic_mean"), [r["V"] for r in R9], [r["ln_chg"] for r in R9], cx])
    run("chirality", X, R9, X[:, 0], -0.6, lambda b: b > -0.2)
    def fresh(name, meas, pred, extra=None, need=()):
        Rb = [r for r in rows if np.isfinite(r[meas]) and all(np.isfinite(r[k]) for k in need)]
        names, X, _ = C.fresh_design(Rb, meas, seen9, extra(Rb) if extra else None)
        run(name, X, Rb, X[:, 0] + X[:, 1], pred, (lambda b: b <= 0) if pred > 0 else (lambda b: b >= 0))
    rep = lambda Rb: {"z_ch_rep": z(Rb, "ch_rep")}
    def ton(Rb):
        e = rep(Rb); nd = np.array([r["n_tok"] for r in Rb])
        e.update({f"ntok{k}": (nd == k).astype(float) for k in range(4, 12)}); e["ntok12p"] = (nd >= 12).astype(float)
        e["links"] = np.array([r["links"] for r in Rb], float); return e
    fresh("fresh_repetition", "ch_rep", +1.0)
    fresh("fresh_arrow", "A", +0.6, rep)
    fresh("fresh_range", "L2c", -0.7, rep)
    fresh("fresh_tonic", "H", -0.6, ton)
    fresh("fresh_diatonic", "D5", +0.5, lambda Rb: dict(rep(Rb), z_FP=z(Rb, "FP"), z_NT=z(Rb, "NT")), need=("FP", "NT"))
    fresh("chirality_on_fresh_reported", "CH", -0.6, lambda Rb: dict(rep(Rb), z_A=z(Rb, "A")), need=("A",))
    json.dump(RES, open(os.path.join(C.HERE, "power_fake.json"), "w"), indent=1)
