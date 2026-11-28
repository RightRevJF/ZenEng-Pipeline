"""Run 12 notes-side gates (reads NO outcome): python3 gates12.py -> measure_gates12.json
Lakh: two-file stability (Spearman, file 1 vs file 2 of the kept, non-duplicate files) >= 0.20; largest |Spearman| (within-artist
  rows) with an existing measure <= 0.70. Existing = run 07's 13 chord/structure measures, the Skeptic's Lakh controls (LNEV, NPB,
  ACT, NFILES) and REP's twins on the skyline (REP_L, H1: the baseline of this pass, as pc_entropy is on Hooktheory; REP_L itself and
  H1 are exempt from the overlap part, as REP was in run 11). ROUGH_X's own gate (Inventor round 2): stability with register held =
  Spearman of the two files' residuals of ROUGH_X on REG (OLS over all kept files) >= 0.20.
Hooktheory (readings): clip-1 vs clip-2 stability and largest overlap with the 13 baselines and 17 pack measures (run 05-06 gate)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy import stats
import common12 as C

LAKH_KEYS = ["REP_L", "H1", "PI3c", "E5_L", "REST_L", "C_L", "TOP_L", "PI8", "H8", "EVLEN", "REPBAR", "ROUGH_X", "REG", "OCT",
             "PCE_ALL", "LNEV", "NPB", "ACT"]
EXIST = C.LAKH_EXISTING + C.LAKH_SKEPTIC + ["REP_L", "H1"]


def sp(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float); ok = np.isfinite(a) & np.isfinite(b)
    return float(stats.spearmanr(a[ok], b[ok]).correlation) if ok.sum() > 10 else float("nan"), int(ok.sum())


def within_share(R, k):
    from collections import defaultdict
    g = defaultdict(list)
    for r in R:
        if np.isfinite(r.get(k, np.nan)): g[r["artist"]].append(r[k])
    g = {a: v for a, v in g.items() if len(v) >= 2}; allv = np.array([x for v in g.values() for x in v])
    return float(sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in g.values()) / ((allv - allv.mean()) ** 2).sum())


def main():
    base = C.lakh_rows(); W = C.within_artist(base); out = {"lakh": {}, "hook": {}}
    pairs = [r["pairs"] for r in base if r["pairs"]]
    # ROUGH_X residual on register, over all kept files
    allf = [f for r in base for f in ([r["pairs"][0], r["pairs"][1]] if r["pairs"] else [])]
    M = json.load(open(C.LAKH12))["songs"]; files = [f for v in M.values() for f in v["files"] if f.get("ROUGH_X") is not None and f.get("REG") is not None]
    A = np.column_stack([np.ones(len(files)), [f["REG"] for f in files]]); bb = np.linalg.lstsq(A, np.array([f["ROUGH_X"] for f in files]), rcond=None)[0]
    res = lambda f: (f["ROUGH_X"] - bb[0] - bb[1] * f["REG"]) if f.get("ROUGH_X") is not None and f.get("REG") is not None else np.nan
    for k in LAKH_KEYS:
        a = [p[0].get(k) for p in pairs]; b = [p[1].get(k) for p in pairs]
        st, n = sp([np.nan if v is None else v for v in a], [np.nan if v is None else v for v in b])
        x = [r.get(k, np.nan) for r in W]
        ov = {e: sp(x, [r.get(e, np.nan) for r in W])[0] for e in EXIST if e != k}
        gate_ov = {e: v for e, v in ov.items() if e not in ("REP_L", "H1")} if k in ("REP_L", "H1") else ov
        top = max(gate_ov.items(), key=lambda t: abs(t[1]) if np.isfinite(t[1]) else -1)
        d = dict(stability_two_files=round(st, 3), pairs=n, largest_overlap=[top[0], round(top[1], 3)],
                 overlaps={e: round(v, 3) for e, v in ov.items()}, songs_within_artist=int(np.isfinite(np.array(x, float)).sum()),
                 within_artist_share=round(within_share(W, k), 3))
        d["gate"] = "passes" if (st >= 0.20 and abs(top[1]) <= 0.70) else "fails"
        out["lakh"][k] = d
    st, n = sp([res(p[0]) for p in pairs], [res(p[1]) for p in pairs])
    out["lakh"]["ROUGH_X"]["stability_register_held"] = round(st, 3); out["lakh"]["ROUGH_X"]["register_slope"] = [float(bb[0]), float(bb[1])]
    out["lakh"]["ROUGH_X"]["gate_inventor"] = "passes" if st >= 0.20 else "fails (stopped)"
    out["lakh"]["meta"] = dict(songs=len(base), within_artist_songs=len(W), artists=len({r["artist"] for r in W}),
                               nonduplicate_pairs=len(pairs), near_duplicate_files_dropped=int(sum(r["n_dup"] for r in base)),
                               songs_with_a_dropped_duplicate=int(sum(r["n_dup"] > 0 for r in base)))
    # Hooktheory readings
    R = C.hook_rows()
    for k in ["G_E5", "G_REST", "G_C", "G_S5", "PIC", "PIC_REL", "pc_entropy", "REP"]:
        S = [r for r in R if np.isfinite(r.get(k, np.nan))]
        pr = [r.get(k + "_c12") for r in S if r.get(k + "_c12")]
        st = float(stats.spearmanr([p[0] for p in pr], [p[1] for p in pr]).correlation) if len(pr) > 10 else float("nan")
        ov = {c: sp([r[k] for r in S], [r.get(c, np.nan) for r in S])[0] for c in C.C11.BASE + C.C11.PACK if c != k}
        top = sorted(ov.items(), key=lambda t: -abs(t[1]))[:4]
        out["hook"][k] = dict(n=len(S), clip_stability=round(st, 3), clip_pairs=len(pr), top_overlap=[(c, round(v, 3)) for c, v in top])
    json.dump(out, open(os.path.join(HERE, "measure_gates12.json"), "w"), indent=1)
    for k, d in out["lakh"].items():
        if k != "meta": print(k, d["stability_two_files"], d["pairs"], d["largest_overlap"], d["within_artist_share"], d["gate"], d.get("stability_register_held", ""))
    print(out["lakh"]["meta"])
    for k, d in out["hook"].items(): print(k, d)


if __name__ == "__main__":
    main()
