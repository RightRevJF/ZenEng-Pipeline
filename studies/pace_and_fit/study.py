"""Pace and the words' fit (749.154), by the rule in PREDICTION.md.  python3 studies/pace_and_fit/study.py -> result.json"""
import os, sys, json, collections, numpy as np, statsmodels.api as sm
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol")]
import word_weight as W, kept_corpus as KC, make_kept_word_weight as MK
rows = []
for k in KC.kept_songs():
    tr, wid = MK.tiers(k["words"])
    if len(tr) != len(k["t"]): continue
    t, p, lines, dur = np.asarray(k["t"]), np.asarray(k["p"]), np.asarray(k["lines"]), np.asarray(k["dur"])
    idx = np.array([i for i in range(len(tr)) if tr[i] is not None])
    if len(idx) < 40: continue
    S = W.salience(t, dur, p, lines); w = np.array([W.WEIGHT[tr[i]] for i in idx])
    whole = W.spearman(w, S["all"][idx]); nolen = W.spearman(w, ((S["place"] + S["height"]) / 2)[idx])
    lf = []
    for l in sorted(set(lines[idx].tolist())):
        m = lines[idx] == l
        if m.sum() >= 4 and np.std(w[m]) > 0 and np.std(S["all"][idx][m]) > 0: lf.append(W.spearman(w[m], S["all"][idx][m]))
    if len(lf) < 4: continue
    sec = k["sec"]; bars = collections.defaultdict(set); cnt = collections.Counter()
    for i in range(len(t)): s_ = sec[i] if i < len(sec) else ""; bars[s_].add(int(t[i]) // 48); cnt[s_] += 1
    dens = [(np.log(cnt[s_] / len(bars[s_])), len(bars[s_])) for s_ in bars if len(bars[s_]) >= 2]
    if len(dens) < 2: continue
    v = np.array([d for d, _ in dens]); wb = np.array([b for _, b in dens], float); mu = (v * wb).sum() / wb.sum(); pace = float(np.sqrt(((v - mu) ** 2 * wb).sum() / wb.sum()))
    rows.append(dict(song=str(k["song"]), whole=float(whole), line=float(np.mean(lf)), pace=pace, nolen=float(nolen), sections=len(dens)))
z = lambda a: (np.asarray(a, float) - np.mean(a)) / np.std(a)
def ols(y, cols):
    m = sm.OLS(z(y), sm.add_constant(np.column_stack([z(c) for c in cols]))).fit(cov_type="HC1"); return m
y = [r["whole"] for r in rows]; L = [r["line"] for r in rows]; P = [r["pace"] for r in rows]
m = ols(y, [L, P]); b, se, pv = float(m.params[2]), float(m.bse[2]), float(m.pvalues[2])
verdict = "the reading holds" if (b <= -0.15 and pv < .05) else "it does not hold" if b > -0.05 else "unsettled"
m2 = ols([r["nolen"] for r in rows], [L, P]); m3 = ols(y, [L])
res = dict(songs=len(rows), pace_coefficient=dict(b=round(b, 3), se=round(se, 3), p=round(pv, 4)), line_fit_coefficient=round(float(m.params[1]), 3), r2=round(float(m.rsquared), 3), verdict=verdict,
           deciding_nothing=dict(without_length=dict(b=round(float(m2.params[2]), 3), p=round(float(m2.pvalues[2]), 4)), whole_on_line_alone=dict(b=round(float(m3.params[1]), 3), r2=round(float(m3.rsquared), 3))),
           quantiles={c: [round(float(x), 3) for x in np.percentile([r[c] for r in rows], (10, 25, 50, 75, 90))] for c in ("whole", "line", "pace", "nolen")})
json.dump(dict(res, rows=rows), open(os.path.join(HERE, "result.json"), "w"), indent=1); print(json.dumps(res, indent=1))
