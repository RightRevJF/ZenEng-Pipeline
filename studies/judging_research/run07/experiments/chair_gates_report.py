"""Run 07 chair: the gate table (split-half Spearman, residual split-half, within-artist renaming overlaps). Notes only."""
import sys, json, numpy as np
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/judging_research/run07/experiments")
import common as C
from scipy import stats
R = json.load(open(sys.argv[1])); S = C.add_shapes(C.lakh_songs(verbose=False))
for s, r in zip(S, R): assert s["artist_key"] == r["artist"]; s["pmin"] = r["pmin_song"]; s["links"] = r["links_song"]
g = np.array([s["artist_key"] for s in S]); u, inv = np.unique(g, return_inverse=True)
def col(k): return np.array([s[k] for s in S], float)
def hc(p, k): return np.array([r[p][k] if r[p][k] is not None else np.nan for r in R], float)
def within(x):
    ok = np.isfinite(x); rk = np.full(len(x), np.nan); rk[ok] = stats.rankdata(x[ok])
    Sm = np.zeros(len(u)); Cn = np.zeros(len(u)); np.add.at(Sm, inv[ok], rk[ok]); np.add.at(Cn, inv[ok], 1)
    out = rk - (Sm / np.maximum(Cn, 1))[inv]; out[~ok | (Cn[inv] < 2)] = np.nan; return out
def wr(a, b):
    a, b = within(a), within(b); ok = np.isfinite(a) & np.isfinite(b); return float(np.corrcoef(a[ok], b[ok])[0, 1])
def sp(a, b):
    ok = np.isfinite(a) & np.isfinite(b); return float(stats.spearmanr(a[ok], b[ok])[0]), int(ok.sum())
def rk(x): o = np.full(len(x), np.nan); ok = np.isfinite(x); o[ok] = stats.rankdata(x[ok]); return o
def resid(y, Xs):
    X = np.column_stack(Xs + [np.ones(len(y))]); yy = rk(y); ok = np.isfinite(yy) & np.isfinite(X).all(1); e = np.full(len(y), np.nan)
    b = np.linalg.lstsq(X[ok], yy[ok], rcond=None)[0]; e[ok] = yy[ok] - X[ok] @ b; return e, 1 - np.var(e[ok]) / np.var(yy[ok])
REN = ["ch_rep", "V", "ln_chg", "ln_bars"]
out = {}
for m in ["ch_rep", "H4m", "cv_w", "g", "CH", "A", "lnP", "lnPsec", "F", "B", "pmin"]:
    sh, n = sp(hc("a", m if m != "pmin" else "pmin"), hc("b", m)) if m not in ("lnPsec",) else sp(hc("a", m), hc("b", m))
    if m == "pmin":
        def blk(p):
            V = hc(p, "nd"); return [((np.minimum(V, 20) == k).astype(float)) for k in range(4, 21)] + [hc(p, "links")]
        ea, _ = resid(hc("a", m), blk("a")); eb, _ = resid(hc("b", m), blk("b"))
        Vs = col("V"); _, r2 = resid(col("pmin"), [rk(Vs), rk(col("links"))])
    else:
        ea, _ = resid(hc("a", m), [rk(hc("a", c)) for c in REN]); eb, _ = resid(hc("b", m), [rk(hc("b", c)) for c in REN]); r2 = None
    rs, _ = sp(ea, eb)
    ov = {c: round(wr(col(m), col(c)), 3) for c in REN + ["CH", "A", "H4m", "cv_w", "g", "F", "B", "lnP", "ln_tempo"] if c != m}
    big = max(REN, key=lambda c: abs(ov[c]) if c in ov else 0)
    _, r2w = resid(col(m), [rk(col(c)) for c in REN])
    out[m] = dict(finite=int(np.isfinite(col(m)).sum()), split_half=round(sh, 3), pairs=n, resid_split_half=round(rs, 3), largest_renaming=[big, ov.get(big)],
                  r2_on_4=round(r2w, 3), r2_size_block=None if r2 is None else round(r2, 3), overlaps=ov,
                  median=float(np.nanmedian(col(m))), sd=float(np.nanstd(col(m))))
    print(m, json.dumps(out[m]))
pc = [s["Pcat"] for s in S]; import collections; print("Pcat", collections.Counter(pc))
print("year unknown", np.mean([not s["year"] for s in S]), "bb", sum(s["bb"] for s in S), "half sizes", collections.Counter(s["half"] for s in S),
      "artists per half", collections.Counter(C.half_of(a) for a in u))
json.dump(out, open(sys.argv[2], "w"), indent=1)
