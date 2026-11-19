import pickle, json, numpy as np
from scipy.stats import rankdata, spearmanr, t as tdist, mannwhitneyu
R = pickle.load(open("listeners.pkl", "rb"))
def partial(x, y, Z):
    x, y = np.asarray(x, float), np.asarray(y, float); rx, ry = rankdata(x), rankdata(y); Zr = np.column_stack([rankdata(z) for z in Z] + [np.ones(len(x))])
    ex = rx - Zr @ np.linalg.lstsq(Zr, rx, rcond=None)[0]; ey = ry - Zr @ np.linalg.lstsq(Zr, ry, rcond=None)[0]; r = float(np.corrcoef(ex, ey)[0, 1]); df = len(x) - 2 - len(Z); tt = r * np.sqrt(df / (1 - r * r)); return round(r, 3), round(float(2 * tdist.sf(abs(tt), df)), 4)
out = {}
for src in ("HT", "CB", "RS", "BM"):
    v = [r for r in R if r["src"] == src]; o = dict(songs=len(v)); medS = float(np.median([r["S"] for r in v]))
    for r in v: r["U"] = -abs(r["S"] - medS)
    o["medians"] = {k: round(float(np.median([r[k] for r in v if r[k] is not None])), 3) for k in ("notes", "S", "L", "GAIN", "SHARE", "LATE", "END")}; o["END under zero, share"] = round(float(np.mean([r["END"] < 0 for r in v if r["END"] is not None])), 3)
    g = [r for r in v if r.get("peak") is not None and r.get("year")]; o["graded"] = len(g)
    if len(g) > 40:
        for k in ("S", "SHARE", "GAIN", "U", "LATE", "END"):
            gg = [r for r in g if r[k] is not None]; Z = [[r["year"] for r in gg], [r["notes"] for r in gg]]
            o[k] = dict(peak=partial([r[k] for r in gg], [-r["peak"] for r in gg], Z), weeks=partial([r[k] for r in gg], [r["weeks"] for r in gg], Z), raw_peak=round(float(spearmanr([r[k] for r in gg], [-r["peak"] for r in gg])[0]), 3))
    if src == "RS":
        for k in ("S", "SHARE", "U", "LATE", "END"):
            gg = [r for r in v if r[k] is not None and r.get("year")]; o[k + " vs list rank (higher = greater)"] = partial([r[k] for r in gg], [-r["rank"] for r in gg], [[r["year"] for r in gg], [r["notes"] for r in gg]])
    if src == "BM":
        for k in ("S", "SHARE", "U", "LATE"):
            o[k + " vs year-end position (higher = better)"] = partial([r[k] for r in v], [-r["position"] for r in v], [[r["year"] for r in v], [r["notes"] for r in v]])
    out[src] = o
both = [r for r in R if r["src"] in ("RS", "CB") and r.get("year")]; cbt = {r["title"] for r in R if r["src"] == "RS"}; both = [r for r in both if not (r["src"] == "CB" and r["title"] in cbt)]
out["Rolling Stone against CoCoPops Billboard"] = dict(songs=len(both))
for k in ("S", "SHARE", "GAIN", "LATE", "END"):
    a = [r[k] for r in both if r["src"] == "RS" and r[k] is not None]; b = [r[k] for r in both if r["src"] == "CB" and r[k] is not None]; u = mannwhitneyu(a, b); bb = [r for r in both if r[k] is not None]
    out["Rolling Stone against CoCoPops Billboard"][k] = dict(auc=round(float(u.statistic / (len(a) * len(b))), 3), p=round(float(u.pvalue), 4), holding_year_and_notes=partial([r[k] for r in bb], [r["src"] == "RS" for r in bb], [[r["year"] for r in bb], [r["notes"] for r in bb]]))
json.dump(out, open("way4_results.json", "w"), indent=1)
for k, v in out.items():
    print("==", k)
    for a, b in v.items(): print("  ", a, b)
