import sys, pickle, json, numpy as np
sys.path[:0] = ["/home/claude/rightrevjf/zeneng-pipeline/lib/luthier", "/home/claude/zeneng/corpus/nine"]
import scaling as SC
from scipy.stats import rankdata, spearmanr, t as tdist, mannwhitneyu
def partial(x, y, Z):
    x, y = np.asarray(x, float), np.asarray(y, float); rx, ry = rankdata(x), rankdata(y); Zr = np.column_stack([rankdata(z) for z in Z] + [np.ones(len(x))])
    ex = rx - Zr @ np.linalg.lstsq(Zr, rx, rcond=None)[0]; ey = ry - Zr @ np.linalg.lstsq(Zr, ry, rcond=None)[0]; r = float(np.corrcoef(ex, ey)[0, 1]); df = len(x) - 2 - len(Z); tt = r * np.sqrt(df / (1 - r * r)); return [round(r, 3), round(float(2 * tdist.sf(abs(tt), df)), 4)]
G = pickle.load(open("../v23/graded.pkl", "rb")); import common as C
old = {str(s) for s in C.PT.SONGS}; rng = np.random.default_rng(1); rows = []
for s in G:
    if s["src"] not in ("CB", "RS"): continue
    ns = s["clips"][0]
    if len(ns) < 150: continue
    notes = [(int(round(t * 12)), p) for t, p in ns]; X = SC.series(notes); a = SC.dfa(X["pitch"]); b = SC.dfa(X["onsets on the grid"])
    if a is None or b is None: continue
    sh = SC.dfa(rng.permutation(X["pitch"])); rows.append(dict(src=s["src"], id=s["id"], title=s["title"], notes=len(ns), year=s.get("year"), peak=s.get("peak"), weeks=s.get("weeks"), rank=s.get("rank"), pitch=a["alpha"], rhythm=b["alpha"], shuffled=sh["alpha"] if sh else None, old=s["src"] == "CB" and s["id"] in old))
for r in rows: r["near_pitch"] = -abs(r["pitch"] - 0.90); r["near_rhythm"] = -abs(r["rhythm"] - 0.66)
cbt = {r["title"] for r in rows if r["src"] == "CB"}; M = ("pitch", "rhythm", "near_pitch", "near_rhythm"); out = {}
def grade(v):
    v = [r for r in v if r["peak"] is not None and r["year"]]; Z = [[r["year"] for r in v], [r["notes"] for r in v]]
    return dict(songs=len(v), **{m: dict(weeks=partial([r[m] for r in v], [r["weeks"] for r in v], Z), peak=partial([r[m] for r in v], [-r["peak"] for r in v], Z)) for m in M})
cb = [r for r in rows if r["src"] == "CB"]; rs = [r for r in rows if r["src"] == "RS"]
out["counts"] = dict(CB=len(cb), CB_old=sum(r["old"] for r in cb), RS=len(rs), pitch_medians=dict(CB=round(float(np.median([r["pitch"] for r in cb])), 3), RS=round(float(np.median([r["pitch"] for r in rs])), 3), shuffled=round(float(np.median([r["shuffled"] for r in rows if r["shuffled"]])), 3)), rhythm_medians=dict(CB=round(float(np.median([r["rhythm"] for r in cb])), 3), RS=round(float(np.median([r["rhythm"] for r in rs])), 3)))
out["the old songs (kept, with a record)"] = grade([r for r in cb if r["old"]])
out["NEW songs: CB not among the old, and RS with a record not in CB"] = grade([r for r in cb if not r["old"]] + [r for r in rs if r["title"] not in cbt])
out["all CoCoPops Billboard"] = grade(cb); out["Rolling Stone with a chart record"] = grade(rs)
both = cb + [r for r in rs if r["title"] not in cbt]; both = [r for r in both if r["year"]]; out["Rolling Stone against CoCoPops Billboard"] = dict(songs=len(both))
for m in M:
    a = [r[m] for r in both if r["src"] == "RS"]; b = [r[m] for r in both if r["src"] == "CB"]; u = mannwhitneyu(a, b); out["Rolling Stone against CoCoPops Billboard"][m] = dict(auc=round(float(u.statistic / (len(a) * len(b))), 3), p=round(float(u.pvalue), 4), holding_year_and_notes=partial([r[m] for r in both], [r["src"] == "RS" for r in both], [[r["year"] for r in both], [r["notes"] for r in both]]))
v = [r for r in rs if r["year"]]; out["inside the Rolling Stone list (higher = greater)"] = {m: partial([r[m] for r in v], [-r["rank"] for r in v], [[r["year"] for r in v], [r["notes"] for r in v]]) for m in M}; out["inside the Rolling Stone list (higher = greater)"]["songs"] = len(v)
json.dump(out, open("way2_again_results.json", "w"), indent=1); pickle.dump(rows, open("rows.pkl", "wb"))
for k, v in out.items():
    print("==", k)
    for a, b in v.items(): print("  ", a, b)
