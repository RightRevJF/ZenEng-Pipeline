"""Run 11 chair: notes-side measure gates (no outcome is read). python3 gates11.py -> measure_gates11.json
Standing Hooktheory gate (runs 05-06), applied to the RAW measure as frozen: clip-1 vs clip-2 Spearman >= 0.20, and no single
|Spearman| > 0.70 with one of the 13 baselines or 17 pack measures (REP is a baseline by design: exempt from the second part).
Reported beside it (decides nothing): the Skeptic's 'stability with extras held' = Spearman of clip-1 vs clip-2 residuals after an
OLS of the clip values on the frozen extras' clip values (pooled over both clips; a pack extra has no clip value, so the song
value is used for both clips), R^2 on the 13 baselines, coverage, and pairwise Spearman among the candidate measures."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy import stats
import common11 as C

# key: (idea, pred, frozen extras, role)
CAND = {
    "G_GAP":     ("R11-G1 GAP (= R10-I3; S = 1 + g/pi)", -0.03, ["range", "n_pitch", "ln_notes"], "candidate"),
    "G_TIE":     ("R11-G3 TIE (= R11-I1 HB)", +0.03, ["ln_notes", "density", "n_pc"], "candidate"),
    "ANT":       ("R11-I2 ANT", +0.03, ["density"], "candidate"),
    "TYP11":     ("R11-L2 TYP11", +0.03, ["mel_ic_mean"], "candidate"),
    "REP":       ("R11-L3 REP (= R10-S1)", -0.03, [], "candidate (baseline by design)"),
    "LOCKP":     ("R11-I3 LOCKP", +0.02, [], "candidate"),
    "LOCK":      ("R10-I2 LOCK (run 10 recipe, m00)", +0.03, [], "candidate"),
    "R_PE_H0":   ("R10-G1 pe_h0", +0.03, ["pc_entropy"], "candidate"),
    "R_IRR":     ("R10-G2 irr_skel", -0.03, ["n_pc"], "candidate"),
    "R_SGAP":    ("R10-G3 S_gap (skeleton, pitch classes)", -0.03, ["n_pc"], "candidate"),
    "R_CORE_IC": ("R10-L2 core_ic", -0.03, ["pc_entropy", "mel_ic_mean"], "candidate"),
    "R_TSG":     ("R10-L2b TSG", -0.03, ["pc_entropy"], "candidate"),
    "R_CUT_AB":  ("R10-L3 CUT_AB", +0.03, ["ln_notes"], "candidate"),
    "R_CHEEGER": ("R10-C1 Cheeger (sweep cut)", -0.03, ["range", "n_pitch", "ln_notes"], "candidate"),
    "R_ARCH":    ("R10-I1 ARCH_PE", -0.03, ["range", "n_pitch"], "candidate"),
    "R_SLG":     ("R10-L1 SLG", +0.03, ["bar_rep", "ln_notes"], "candidate"),
    # readings
    "G_ROOMS":   ("reading in GAP (R11-G2)", +0.03, ["range", "n_pitch", "ln_notes"], "reading"),
    "SETTLE":    ("reading in GAP (R11-L1)", +0.03, ["n_pitch", "range"], "reading"),
    "HB":        ("reading in TIE", +0.03, ["ln_notes", "density", "n_pc"], "reading"),
    "G_TIE_BC":  ("reading in TIE (Bergsma V^2)", +0.03, ["ln_notes", "density", "n_pc"], "reading"),
    "CT":        ("reading (chord-tone share)", None, [], "reading"),
    "TYP_KK11":  ("reading in TYP11", +0.03, ["mel_ic_mean"], "reading"),
    "TYP":       ("reading in TYP11", +0.03, ["mel_ic_mean"], "reading"),
    "R_SURF_IC": ("reading in core_ic", -0.03, ["pc_entropy"], "reading"),
    "R_SLGW":    ("reading in SLG", +0.03, ["bar_rep", "ln_notes"], "reading"),
    "R_PE_H0I":  ("reading in pe_h0", +0.03, ["pc_entropy"], "reading"),
    "R_H0MAX":   ("reading in GAP", None, [], "reading"),
}


def resid_stability(R, M, key, extra):
    rows = []
    for r in R:
        p = M[r["vid"]].get(key + "_c12")
        if not p or not all(np.isfinite(p)): continue
        e1, e2 = [], []
        ok = True
        for e in extra:
            q = M[r["vid"]].get(e + "_c12")
            if q is not None and all(np.isfinite(q)): e1.append(q[0]); e2.append(q[1])
            elif e in C.PACK and r.get(e) is not None and np.isfinite(r[e]): e1.append(r[e]); e2.append(r[e])
            else: ok = False; break
        if ok: rows.append((p[0], p[1], e1, e2))
    if len(rows) < 50: return dict(spearman=float("nan"), n=len(rows))
    x = np.array([a for a, _, _, _ in rows] + [b for _, b, _, _ in rows], float)
    if extra:
        X = np.array([e1 for _, _, e1, _ in rows] + [e2 for _, _, _, e2 in rows], float)
        X = np.column_stack([np.ones(len(x)), X]); bb, *_ = np.linalg.lstsq(X, x, rcond=None); x = x - X @ bb
    n = len(rows)
    return dict(spearman=float(stats.spearmanr(x[:n], x[n:]).correlation), n=n)


def main():
    M = C.load_cache(); out = {"rule": __doc__, "measures": {}, "pairwise_spearman": {}}
    designs = {}
    for k, (idea, pred, extra, role) in CAND.items():
        R = C.design(k, [])
        st = C.stability(R, k); rn = C.renaming(R, k)
        top = sorted(((c, v) for c, v in rn.items() if c != "R2_on_13_baselines" and c != k), key=lambda t: -abs(t[1]))
        exempt = k == "REP"
        top_check = [t for t in top if not (exempt and t[0] == "pc_entropy")]
        mx = top_check[0] if top_check else (None, 0.0)
        rs = resid_stability(R, M, k, extra)
        rs13 = resid_stability(R, M, k, [b for b in C.BASE if b != ("pc_entropy" if exempt else None)])
        passes = (st["spearman"] >= 0.20) and (exempt or abs(mx[1]) <= 0.70)
        out["measures"][k] = dict(idea=idea, role=role, pred=pred, extra=extra, songs=len(R), coverage=len(R) / 9588,
                                  stability=st["spearman"], pairs=st["n"], largest_overlap=[mx[0], mx[1]],
                                  top4=[[c, round(v, 3)] for c, v in top[:4]], R2_on_13=rn["R2_on_13_baselines"],
                                  stability_extras_held=rs["spearman"], pairs_extras_held=rs["n"],
                                  stability_13_held=rs13["spearman"], gate_raw="passes" if passes else "stopped",
                                  overlap_exempt=exempt)
        designs[k] = {r["vid"]: r[k] for r in R}
        print(k, round(st["spearman"], 3), st["n"], mx, round(rs["spearman"], 3), round(rs13["spearman"], 3), out["measures"][k]["gate_raw"], flush=True)
    keys = list(CAND)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            vs = [v for v in designs[a] if v in designs[b]]
            if len(vs) > 50:
                out["pairwise_spearman"][a + "|" + b] = round(float(stats.spearmanr([designs[a][v] for v in vs], [designs[b][v] for v in vs]).correlation), 3)
    json.dump(out, open(os.path.join(HERE, "measure_gates11.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
