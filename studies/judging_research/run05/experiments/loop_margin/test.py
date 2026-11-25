"""Run 05, loop_margin: within an artist's songs, does a chord loop with a large certified H1 margin M (card 1, TopPT:
time-delay embedding of chord chroma, persistent homology, subsampling confidence radius) go with a higher chance that a
performer set sharing no name with the original artist released the song (y_foreign)?

The rule is PREDICTION.md in this folder (frozen and pushed in commit 1f6c36d, branch judging-research, before any outcome
was joined). Prediction: beta(M) = +0.8 pp per SD. Pass: beta > 0, p < .05/7 = .00714 two-sided, beta > 0 in both artist
halves, conditional logit > 0 and converged. Kill: beta < +0.3. Opposite sign (beta < 0, p < .00714): killed, reported as a
new hypothesis. Unsettled: anything else.

Order, as the rule says:
  1. unit values (must reproduce to 1e-6);  2. rows and M over every clip (multiprocessing Pool(2); per-clip values cached
  OUTSIDE the repo in /tmp/loop_margin_cache, keyed by a hash of this file's measure settings);  3. the gate (stops if it fails);
  4. notes-side power;  5. common.load_outcomes (refuses unless PREDICTION.md is committed);  6. counts;  7. clustered SE and
  power;  8. beta, p, 95% range, halves, conditional logit, verdict;  9. items reported, deciding nothing;  10. result.json.
FAKE_Y=1 python3 test.py runs steps 1-4 and then the model code on a random fake outcome (no outcome file read, nothing written).
GATE_ONLY=1 stops before the outcome.

Data credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
python3 test.py  ->  result.json in this folder
"""
import os, sys, json, time, hashlib
import multiprocessing as mp
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.stats import norm as N
from ripser import ripser

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C

ALPHA = 0.05 / 7; ZC = float(N.isf(ALPHA / 2)); PRED = 0.8; KILL = 0.3
CACHE_DIR = "/tmp/loop_margin_cache"
OUT = dict(rule="PREDICTION.md in this folder (commit 1f6c36d)", alpha=ALPHA, z_crit=round(ZC, 4), prediction_pp_per_sd=PRED, kill_below=KILL,
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)")
r4 = C.r4
def J(o): return o.item() if hasattr(o, "item") else (o.tolist() if hasattr(o, "tolist") else str(o))
def finish(verdict, write=True):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    if write: json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=J)
    print("VERDICT:", verdict, flush=True)

# ---------------------------------------------------------------- the measure M (every setting frozen by the rule)
H = 0.5; MM = 8; SIGMA = 2; PERIODS = (2, 4); CAP = 300; B = 200; COEFF = 11
SETTINGS = dict(H=H, m=MM, sigma=SIGMA, periods=PERIODS, cap=CAP, B=B, coeff=COEFF, b="min(ceil(0.99n), n-1)", c="2*q95", v=1)

def beats_per_bar(a):
    m = a.get("meters") or []
    v = m[0].get("beats_per_bar") if m else None
    return v if v else 4

def chroma(a):
    T = int(np.ceil(a["num_beats"] / H - 1e-9)); X = np.zeros((T, 12))
    for h in a.get("harmony") or []:
        i0 = max(int(np.floor(h["onset"] / H + 1e-9)), 0); i1 = min(int(np.ceil(h["offset"] / H - 1e-9)), T)
        if i1 > i0: X[i0:i1, list(C.chord_pcs(h))] = 1.0
    return X

def margin_at(Xs, P, s):
    T = len(Xs); tau = P / (MM + 1); span = MM * tau
    anc = np.arange(0.0, T - 1 - span + 1e-9, 0.5)                       # every 1/4 beat
    if len(anc) > CAP: anc = anc[np.round(np.linspace(0, len(anc) - 1, CAP)).astype(int)]
    n_pre = len(anc); grid = np.arange(T)
    pts = np.concatenate([np.stack([np.interp(anc + k * tau, grid, Xs[:, j]) for j in range(12)], 1) for k in range(MM + 1)], 1)  # k-major
    pts = np.unique(np.round(pts, 6), axis=0); n = len(pts)
    if n < 10: return None
    D = np.sqrt(np.maximum(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1), 0.0))
    b = min(int(np.ceil(0.99 * n)), n - 1); rng = np.random.default_rng(0); hs = np.empty(B)
    for j in range(B):
        keep = np.zeros(n, bool); keep[rng.choice(n, b, replace=False)] = True
        hs[j] = D[~keep][:, keep].min(1).max()
    c = 2.0 * float(np.quantile(hs, 0.95))
    dg = ripser(D, distance_matrix=True, maxdim=1, coeff=COEFF)["dgms"][1] / 2.0
    if len(dg): dg = dg[np.isfinite(dg[:, 1])]
    mg = max([d - bb - 2 * c for bb, d in dg if bb <= c] + [0.0]) / s
    top = float(max([d - bb for bb, d in dg], default=0.0)) / s
    return dict(margin=float(mg), n_pre=int(n_pre), n_post=int(n), c=c / s, top_bar=top, bars=int(len(dg)))

def M_clip(a):
    X = chroma(a)
    if X.sum() == 0: return None
    Xs = gaussian_filter1d(X, SIGMA, axis=0, mode="nearest")
    s = np.sqrt(MM + 1) * np.sqrt(((Xs - Xs.mean(0)) ** 2).sum(1).mean())
    if s < 1e-9: return None
    T = len(Xs); per = {}
    for Pb in PERIODS:
        P = Pb * beats_per_bar(a) / H
        if 2 * P > T: continue
        r = margin_at(Xs, P, s)
        if r is not None: per[Pb] = r
    if not per: return None
    M = max(r["margin"] for r in per.values()); p2 = per.get(2)
    return dict(M=M, cert=float(M > 0), n_pre2=(p2["n_pre"] if p2 else None), n_post2=(p2["n_post"] if p2 else None),
                per={str(k): v for k, v in per.items()})

def _work(k):
    try: return k, M_clip(C.raw_clips()[k])
    except Exception as e: return k, {"err": repr(e)}

# ---------------------------------------------------------------- arrow of time A (printed in the gate, deciding nothing)
def _changes(a):
    seq = [C.chord_pcs(h) for h in sorted(a.get("harmony") or [], key=lambda h: h["onset"])]
    return [x for i, x in enumerate(seq) if i == 0 or x != seq[i - 1]]
def arrow(a):
    s = _changes(a); n = {}
    for x, y in zip(s, s[1:]): n[(x, y)] = n.get((x, y), 0) + 1
    tot = sum(n.values())
    return np.nan if tot < 6 else 1 - sum(min(v, n.get((y, x), 0)) for (x, y), v in n.items()) / tot


def main():
    fake = bool(os.environ.get("FAKE_Y"))
    # ------------------------------------------------------------ 1. unit values
    def toy(chords, n_bars=16):
        return dict(num_beats=4 * n_bars, meters=[dict(beat=1, beats_per_bar=4)],
                    harmony=[dict(onset=4.0 * i, offset=4.0 * (i + 1), root_pitch_class=r, root_position_intervals=iv)
                             for i, (r, iv) in enumerate((chords * n_bars)[:n_bars])])
        # one chord per 4/4 bar
    I, IV, V, vi = (0, [4, 3]), (5, [4, 3]), (7, [4, 3]), (9, [3, 4])
    u1, u2, u3 = M_clip(toy([I, V, vi, IV])), M_clip(toy([I, IV])), M_clip(toy([I]))
    print(f"UNIT I-V-vi-IV x4: M {u1['M']:.6f} [0.242192], n_pre {u1['n_pre2']} [226], n {u1['n_post2']} [96]; per P: "
          + json.dumps({k: {kk: round(vv, 6) for kk, vv in v.items()} for k, v in u1['per'].items()}), flush=True)
    print(f"UNIT I-IV x8: M {u2['M']:.6f} [0.015590]; per P: " + json.dumps({k: {kk: round(vv, 6) for kk, vv in v.items()} for k, v in u2['per'].items()}), flush=True)
    print(f"UNIT I x16: {u3} [None: s = 0]", flush=True)
    ok = abs(u1["M"] - 0.242192) < 1e-6 and u1["n_pre2"] == 226 and u1["n_post2"] == 96 and abs(u2["M"] - 0.015590) < 1e-6 and u3 is None
    OUT["unit_values"] = dict(I_V_vi_IV=dict(M=u1["M"], n_pre=u1["n_pre2"], n_post=u1["n_post2"], per_P=u1["per"]),
                              I_IV=dict(M=u2["M"], per_P=u2["per"]), I_only=u3, reproduced=bool(ok))
    if not ok: finish("stopped (unit values not reproduced)", write=not fake); sys.exit(1)

    # ------------------------------------------------------------ 2. rows, M on every clip (Pool(2), cached outside the repo)
    rows = C.load_rows()["rows"]; R = C.raw_clips()
    ks = [c["k"] for r in rows for c in r["clips"]]
    os.makedirs(CACHE_DIR, exist_ok=True)
    tag = hashlib.md5((json.dumps(SETTINGS, sort_keys=True) + C.RAW_SHA256).encode()).hexdigest()[:10]
    cpath = os.path.join(CACHE_DIR, f"M_clips_{tag}.json")
    cache = json.load(open(cpath)) if os.path.exists(cpath) else {}
    todo = [k for k in dict.fromkeys(ks) if k not in cache and k in R]
    t1 = time.time()
    if todo:
        print(f"computing M on {len(todo)} clips with Pool(2) (cache {cpath} has {len(cache)})", flush=True)
        with mp.get_context("fork").Pool(2) as pool:
            for i, (k, v) in enumerate(pool.imap_unordered(_work, todo, chunksize=25), 1):
                cache[k] = v
                if i % 2000 == 0: print(f"  {i}/{len(todo)} clips, {time.time() - t1:.0f}s", flush=True)
        json.dump(cache, open(cpath, "w"))
    MC = {k: cache.get(k) for k in ks}
    errs = sum(1 for v in MC.values() if v and "err" in v); none = sum(v is None for v in MC.values()); miss = sum(k not in R for k in ks)
    vals = [v for v in MC.values() if v and "err" not in v]
    print(f"clips {len(ks)} [16,563]; computed now {len(todo)} in {time.time() - t1:.0f}s; no value {none} [44]; errors {errs}; missing from raw {miss}; "
          f"clips certifying (M > 0) {np.mean([v['cert'] for v in vals]):.3f} [0.41]", flush=True)
    OUT["clips"] = dict(n=len(ks), computed_this_run=len(todo), compute_s=round(time.time() - t1), no_value=none, errors=errs, missing_raw=miss,
                        share_certified=r4(np.mean([v['cert'] for v in vals])), cache=cpath)
    if errs: print("ERRORS:", [(k, v) for k, v in MC.items() if v and "err" in v][:5], flush=True)

    def put(name, f):
        def fn(a, c):
            o = MC.get(c["k"])
            if not o or "err" in o: return np.nan
            v = f(o); return np.nan if v is None else float(v)
        C.song_measure(rows, fn, name)
    put("M", lambda o: o["M"]); put("cert", lambda o: o["cert"])
    put("ln_anchors", lambda o: np.log(o["n_pre2"]) if o["n_pre2"] else None)
    put("ln_anchors_post", lambda o: np.log(o["n_post2"]) if o["n_post2"] else None)
    Mv = np.array([r["M"] for r in rows]); hasM = np.isfinite(Mv)
    pct = np.nanpercentile(Mv, [10, 50, 75, 90])
    crep = np.array([r["ch_rep"] for r in rows]); q = np.percentile(crep, [100 / 3, 200 / 3]); terc = np.digitize(crep, q)
    tshare = [float(np.mean(Mv[hasM & (terc == t)] > 0)) for t in range(3)]
    print(f"songs with M {hasM.sum()} [9,576]; share scoring 0 {np.mean(Mv[hasM] == 0):.3f} [0.48]; pct 10/50/75/90 {np.round(pct, 3).tolist()} "
          f"[0 / 0.006 / 0.124 / 0.242]; share M > 0 by ch_rep tercile {np.round(tshare, 3).tolist()} [0.36 / 0.65 / 0.54]", flush=True)
    OUT["songs_measure"] = dict(with_M=int(hasM.sum()), share_zero=r4(np.mean(Mv[hasM] == 0)), pct_10_50_75_90=[r4(x) for x in pct],
                                share_pos_by_ch_rep_tercile=[r4(x) for x in tshare])

    # ------------------------------------------------------------ 3. gate (notes only)
    z_crep = C.zs(crep); z_crep2 = z_crep ** 2; z_icm = C.zs([r["ch_ic_mean"] for r in rows])
    lnA = np.array([r["ln_anchors"] for r in rows]); lnA_post = np.array([r["ln_anchors_post"] for r in rows])
    g = C.gate(rows, "M", extra={"ch_rep_sq": list(z_crep2), "ln_anchors": list(lnA)})
    top6 = sorted(g["overlap_all"].items(), key=lambda kv: -abs(kv[1] or 0))[:6]
    print(f"GATE 1 clip-to-clip: {g['clip_to_clip']} on {g['clip_pairs']} pairs [0.369 on 4,247]; needs >= 0.20", flush=True)
    print(f"GATE 2 largest overlap: {g['overlap_largest']} [n_ch -0.254]; top 6 {top6}; needs |rho| <= 0.7", flush=True)
    for r in rows:   # A, deciding nothing (arrow_of_time's measure, weighted by changes)
        vs, ws = [], []
        for c in r["clips"]:
            a = R.get(c["k"]); vs.append(arrow(a) if a else np.nan); ws.append(max(len(_changes(a)) - 1, 0) if a else 0)
        vs, ws = np.array(vs, float), np.array(ws, float); okA = np.isfinite(vs)
        r["A"] = float(np.average(vs[okA], weights=ws[okA])) if okA.any() and ws[okA].sum() > 0 else np.nan
    rhoA = C.sp(Mv, [r["A"] for r in rows]); rho_pre = C.sp(Mv, lnA); rho_post = C.sp(Mv, lnA_post)
    print(f"  deciding nothing: rho(M, A) {rhoA[0]:+.3f} on {rhoA[1]} songs [+0.19]; rho(M, ln anchors before dedup) {rho_pre[0]:+.3f} [+0.25], after {rho_post[0]:+.3f} [+0.12]", flush=True)
    OUT["gate"] = dict(g, top6=top6, rho_M_A=[r4(rhoA[0]), rhoA[1]], rho_M_lnanchors_pre=r4(rho_pre[0]), rho_M_lnanchors_post=r4(rho_post[0]))
    print(f"GATE: {'PASSED' if g['passed'] else 'FAILED'}", flush=True)
    if not g["passed"]: finish("stopped (gate failed; no outcome joined)", write=not fake); sys.exit(0)

    # ------------------------------------------------------------ 4. design and notes-side power
    art_all = np.array([r["artist"] for r in rows]); half_all = np.array([r["half"] for r in rows])
    cnames, Xc = C.controls(rows)
    zM = np.full(len(rows), np.nan); zM[hasM] = (Mv[hasM] - Mv[hasM].mean()) / Mv[hasM].std()
    certv = np.array([r["cert"] for r in rows]); zcert = np.full(len(rows), np.nan); zcert[hasM] = (certv[hasM] - certv[hasM].mean()) / certv[hasM].std()
    def design(x=zM, sq=True, anchors=lnA):
        cols = {"z_M": x, "z_ch_rep": z_crep}
        if sq: cols["z_ch_rep_sq"] = z_crep2
        cols.update(z_ch_ic_mean=z_icm, ln_anchors=anchors)
        cols.update({n: Xc[:, j] for j, n in enumerate(cnames)})
        return list(cols), np.column_stack(list(cols.values()))
    NAMES, X = design()
    base_ok = np.isfinite(X).all(1)
    print(f"columns ({len(NAMES)}): {NAMES}; rows with every column {base_ok.sum()}", flush=True)
    OUT["columns"] = NAMES

    def demean(Mx, gv):
        codes = {a: i for i, a in enumerate(sorted(set(gv)))}; gg = np.array([codes[a] for a in gv]); cnt = np.bincount(gg)
        M2 = np.asarray(Mx, float).reshape(len(gv), -1); s = np.zeros((len(codes), M2.shape[1])); np.add.at(s, gg, M2); return M2 - (s / cnt[:, None])[gg]
    Xd = demean(X[base_ok], art_all[base_ok]); Xd = Xd[:, np.abs(Xd).sum(0) > 1e-12]
    xt = Xd[:, 0] - Xd[:, 1:] @ np.linalg.lstsq(Xd[:, 1:], Xd[:, 0], rcond=None)[0]
    se_n = np.sqrt(0.22 * 0.78 / (xt @ xt)) * 100
    pw_n = C.power(PRED, se_n, ALPHA)
    print(f"NOTES-SIDE POWER: residual share {xt @ xt / base_ok.sum():.3f} [0.459] on {base_ok.sum()} songs; SE bound {se_n:.3f} pp [0.63]; "
          f"power at +0.8, p < .00714: {pw_n:.3f} [0.08]; at p < .05: {C.power(PRED, se_n, 0.05):.3f} [0.25]; "
          f"P(kill | +0.8) {N.cdf((KILL - PRED) / se_n):.2f} [0.21], P(kill | 0) {N.cdf(KILL / se_n):.2f} [0.68]", flush=True)
    OUT["notes_side_power"] = dict(songs=int(base_ok.sum()), residual_share=r4(xt @ xt / base_ok.sum()), se_bound_pp=r4(se_n), power_p00714=r4(pw_n),
                                   power_p05=r4(C.power(PRED, se_n, 0.05)), p_kill_if_pred=r4(N.cdf((KILL - PRED) / se_n)), p_kill_if_zero=r4(N.cdf(KILL / se_n)))
    if os.environ.get("GATE_ONLY"): print("GATE_ONLY: stopping before the outcome", flush=True); sys.exit(0)

    # ------------------------------------------------------------ 5. outcome
    if fake:
        rs = np.random.default_rng(7)
        for r in rows:
            r["y"] = 100.0 if rs.random() < 0.23 else 0.0
            r["y_foreign"] = (np.nan if rs.random() < 0.02 else (100.0 if rs.random() < 0.6 else 0.0)) if r["y"] > 0 else 0.0
            r["versions"] = None; r["lcov"] = float(rs.exponential(1.0)) if r["y"] > 0 else None; r["first_year"] = int(rs.integers(1960, 2020)) if r["y"] > 0 else None
        osum = dict(fake=True)
        print("\n*** FAKE random outcome (no outcome file read; nothing written) ***", flush=True)
    else:
        osum = C.load_outcomes(rows, HERE)
    yf = np.array([r["y_foreign"] for r in rows], float); yv = np.array([r["y"] for r in rows], float)
    smp = base_ok & np.isfinite(yf)
    nart = len(set(art_all[smp])); y1 = int((yf[smp] > 0).sum())
    print(f"\nOUTCOME: {osum}", flush=True)
    print(f"COUNTS: N {smp.sum()} songs, {nart} artists; y_foreign = 100: {y1} ({y1 / smp.sum():.4f}); dropped: no M {int((~hasM).sum())}, "
          f"y_foreign NaN {int((hasM & ~np.isfinite(yf)).sum())} (of all rows {int((~np.isfinite(yf)).sum())}); y = 100 among N {int((yv[smp] > 0).sum())}", flush=True)
    OUT["outcome"] = dict(summary=osum, N=int(smp.sum()), artists=nart, y_foreign1=y1, share=r4(y1 / smp.sum()), dropped_no_M=int((~hasM).sum()),
                          dropped_yforeign_nan=int((hasM & ~np.isfinite(yf)).sum()))

    # ------------------------------------------------------------ 6-7. LPM; SE and power first
    m = C.lpm(X[smp], yf[smp], art_all[smp]); se = float(m["se"][0])
    pw = C.power(PRED, se, ALPHA)
    print(f"POWER: clustered SE {se:.4f} pp [notes bound {se_n:.3f}]; power at +0.8, p < .00714: {pw:.3f}; at p < .05: {C.power(PRED, se, 0.05):.3f}; "
          f"P(kill | +0.8) {N.cdf((KILL - PRED) / se):.2f}, P(kill | 0) {N.cdf(KILL / se):.2f}", flush=True)
    OUT["power"] = dict(se=r4(se), power_p00714=r4(pw), power_p05=r4(C.power(PRED, se, 0.05)), p_kill_if_pred=r4(N.cdf((KILL - PRED) / se)),
                        p_kill_if_zero=r4(N.cdf(KILL / se)))

    # ------------------------------------------------------------ 8. estimate, halves, conditional logit, verdict
    b, p = float(m["b"][0]), float(m["p"][0])
    OUT["primary"] = dict(summ=C.summ(m, 0), N=m["N"], artists=m["G"], K=m["K"], other={n: C.summ(m, j) for j, n in enumerate(NAMES[:5])})
    print(f"PRIMARY LPM z(M): beta {b:+.4f} pp per SD (predicted +0.8), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; "
          f"N {m['N']}, artists {m['G']}, K {m['K']}", flush=True)
    print("  other columns: " + "; ".join(f"{n} {m['b'][j]:+.3f} ({m['se'][j]:.3f})" for j, n in enumerate(NAMES[1:5], 1)), flush=True)
    halves = []
    for h in (0, 1):
        s = smp & (half_all == h); mh = C.lpm(X[s], yf[s], art_all[s])
        halves.append(dict(half=h, songs=mh["N"], artists=mh["G"], y_foreign1=int((yf[s] > 0).sum()), **C.summ(mh, 0)))
        print(f"HALF {h}: {mh['N']} songs, {mh['G']} artists, y_foreign=100 {halves[-1]['y_foreign1']}; beta {mh['b'][0]:+.4f} (SE {mh['se'][0]:.4f}, p {mh['p'][0]:.3g})", flush=True)
    OUT["halves"] = halves
    dh = halves[0]["beta"] - halves[1]["beta"]; sdh = float(np.hypot(halves[0]["se"], halves[1]["se"]))
    OUT["halves_difference"] = dict(diff=r4(dh), se=r4(sdh), z=r4(dh / sdh), p=float(f"{2 * N.sf(abs(dh / sdh)):.4g}"), note="printed, deciding nothing")
    print(f"  halves differ by {dh:+.3f} (SE {sdh:.3f}, z {dh / sdh:+.2f}, p {2 * N.sf(abs(dh / sdh)):.3g}); printed, deciding nothing", flush=True)
    yb = (yf[smp] > 0).astype(float); ga = art_all[smp]
    codes = {a: i for i, a in enumerate(sorted(set(ga)))}; gi = np.array([codes[a] for a in ga]); cnt = np.bincount(gi); sy = np.bincount(gi, weights=yb)
    kg = (sy > 0) & (sy < cnt)
    print(f"CONDITIONAL LOGIT: drops {int((~kg).sum())} artists and {int((~kg[gi]).sum())} songs (all 0 or all 1)", flush=True)
    t2 = time.time()
    params, bse, pv, conv, ksongs, kgroups = C.cond_logit(X[smp], yb, list(ga))
    clr = dict(coef=r4(params[0]), se=r4(bse[0]), p=float(f"{pv[0]:.4g}"), converged=conv, kept_songs=ksongs, kept_artists=kgroups,
               dropped_artists=int((~kg).sum()), dropped_songs=int((~kg[gi]).sum()), secs=round(time.time() - t2))
    print(f"  z(M): coef {params[0]:+.4f} log-odds per SD, SE {bse[0]:.4f}, p {pv[0]:.4g}; converged {conv}; kept {ksongs} songs, {kgroups} artists", flush=True)
    OUT["conditional_logit"] = clr
    if b < 0 and p < ALPHA: verdict = "killed (opposite sign: beta < 0 with p < .00714; reported as a new hypothesis, not a pass)"
    elif b < KILL: verdict = "kill (beta below +0.3)"
    elif b > 0 and p < ALPHA and all(hh["beta"] > 0 for hh in halves) and params[0] > 0 and conv: verdict = "pass"
    else: verdict = "unsettled"
    print(f"VERDICT BY THE RULE: {verdict}", flush=True)

    # ------------------------------------------------------------ 9. reported, deciding nothing
    rep = {}
    def alt(lab, Xa, ya, sa, idx=0):
        ok = sa & np.isfinite(Xa).all(1) & np.isfinite(ya)
        mm = C.lpm(Xa[ok], ya[ok], art_all[ok]); rep[lab] = dict(N=mm["N"], artists=mm["G"], **C.summ(mm, idx))
        print(f"  [{lab}] beta {mm['b'][idx]:+.4f} (SE {mm['se'][idx]:.4f}, p {mm['p'][idx]:.3g}), N {mm['N']}", flush=True)
    print("REPORTED, deciding nothing:", flush=True)
    alt("cert (z of the song's certified share) in place of M", design(x=zcert)[1], yf, smp)
    alt("ln_anchors after dedup in place of before", design(anchors=lnA_post)[1], yf, smp)
    alt("without ch_rep^2", design(sq=False)[1], yf, smp)
    if not fake:
        nrm = lambda s: __import__("re").sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))
        bad = lambda st: any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in st)
        yk = yf.copy(); changed = 0; removed_sets = 0
        for i, r in enumerate(rows):
            if not np.isfinite(yf[i]) or r.get("versions") is None: continue
            sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"])
            O = {nrm(nm) for s_ in sets if any(nrm(nm) == a for nm in s_) for nm in s_}   # the artist's own names, from all sets
            kept = [s_ for s_ in sets if not bad(s_)]; removed_sets += len(sets) - len(kept)
            v = 100.0 if [s_ for s_ in kept if len(s_) > 0 and not any(nrm(nm) in O for nm in s_)] else 0.0
            changed += int(v != yf[i]); yk[i] = v
        print(f"  karaoke/tribute: {removed_sets} performer sets removed; {changed} songs change y_foreign; y_foreign=100 in N now {int((yk[smp] > 0).sum())}", flush=True)
        alt("y_foreign without karaoke/tribute sets", X, yk, smp); rep["y_foreign without karaoke/tribute sets"].update(sets_removed=removed_sets, songs_changed=changed)
    alt("beta(M) on y", X, yv, base_ok)
    # intensive margin: among y = 100 with covers and first_year; z(log(1+covers)) on the same columns + first_year; SD per SD
    lc = np.array([np.nan if r.get("lcov") is None else r["lcov"] for r in rows], float)
    fy = np.array([np.nan if r.get("first_year") is None else r["first_year"] for r in rows], float)
    si = base_ok & (yv > 0) & np.isfinite(lc) & np.isfinite(fy)
    zl = np.full(len(rows), np.nan); zl[si] = (lc[si] - lc[si].mean()) / lc[si].std()
    zMi = np.full(len(rows), np.nan); zMi[si] = (Mv[si] - Mv[si].mean()) / Mv[si].std()
    Xi = np.column_stack([design(x=zMi)[1], fy])
    alt("intensive: z(log(1+covers)) per SD of M, among versioned songs (+first_year)", Xi, zl, si)
    OUT["reported"] = rep
    finish(verdict, write=not fake)


if __name__ == "__main__":
    main()
