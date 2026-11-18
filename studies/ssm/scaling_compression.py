"""Tests S1-S3 and K1-K3 (PREDICTION_3.md). python3 scaling_compression.py -> scaling_compression.json"""
import sys, os, re, csv, glob, json, lzma
import numpy as np
from scipy.stats import spearmanr, mannwhitneyu
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); import ssm_lib as L, heldout_bimmuda as HB
def notes_of(song):
    ns = sorted((t, p) for b in song["bars"] for t, p in b["mel"]); out = []
    for t, p in ns:
        if not out or t > out[-1][0] + 1e-6: out.append((t, p))
    return out
def dfa(x, smin=4):
    x = np.asarray(x, float)
    if len(x) < 64: return np.nan
    y = np.cumsum(x - x.mean()); smax = len(x) // 4; scales = np.unique(np.floor(np.logspace(np.log10(smin), np.log10(smax), 12)).astype(int)); F = []
    for s in scales:
        n = len(y) // s; seg = y[:n * s].reshape(n, s); t = np.arange(s); f = []
        for row in seg: c = np.polyfit(t, row, 1); f.append(np.mean((row - np.polyval(c, t)) ** 2))
        F.append(np.sqrt(np.mean(f)))
    return float(np.polyfit(np.log(scales), np.log(F), 1)[0])
def readings(song):
    ns = notes_of(song)
    if len(ns) < 64: return None
    p = [q for _, q in ns]; ioi = [b[0] - a[0] for a, b in zip(ns, ns[1:])]
    ap, ar = dfa(p), dfa(ioi)
    tok = ",".join(f"{(q - song['tonic']) % 12}:{round(d * 4)}" for q, d in zip(p, ioi + [1.0])).encode()
    k = len(lzma.compress(tok, preset=9)) / len(tok)
    return dict(alpha_pitch=ap, alpha_rhythm=ar, near_pitch=-abs(ap - 1), near_rhythm=-abs(ar - 1), compress=k, notes=len(ns))
C = "/home/claude/data/cocopops/CoCoPops"; rows = []
for grp, pat in (("RS", "RollingStone/Data/*.hum"), ("BB", "Billboard/Data/*.hum")):
    for f in sorted(glob.glob(os.path.join(C, pat))):
        s = L.read_hum(f); r = readings(s)
        if not r: continue
        meta = {x.group(1): x.group(2) for x in (re.match(r"!!!([^:]+):\s*(.*)", l) for l in open(f, errors="ignore")) if x}
        pk = re.match(r"\d+", meta.get("BillboardPeak", "")); wk = re.match(r"\d+", meta.get("BillboardWeeksOnChart", ""))
        r.update(group=grp, title=s["title"], peak=int(pk.group(0)) if pk else None, weeks=int(wk.group(0)) if wk else None); rows.append(r)
B = "/home/claude/data/bimmuda/BiMMuDa"; norm = lambda s: re.sub(r"[^a-z]", "", s.lower()); coco = {norm(r["title"]) for r in rows}; bim = []
for m in csv.DictReader(open(B + "/metadata/bimmuda_per_song_metadata.csv")):
    if m["Time Signature 1"] != "4/4" or m["Time Signature 2"] or norm(m["Title"]) in coco: continue
    pos = m["Position"].strip(); mm = re.match(r"(\d+)(\w*)", pos)
    f = f"{B}/bimmuda_dataset/{m['Year']}/{pos}/{m['Year']}_{int(mm.group(1)):02d}{mm.group(2)}_full.mid"
    if not os.path.exists(f): continue
    got = HB.read_midi(f, HB.pcname(m["Tonic 1"]) or 0)
    if not got: continue
    r = readings(got[0])
    if r: r.update(title=m["Title"], position=int(mm.group(1)), year=int(m["Year"])); bim.append(r)
def auc(a, b): u = mannwhitneyu(a, b); return [round(float(u.statistic / (len(a) * len(b))), 3), round(float(u.pvalue), 4)]
def sp(x, y): ok = [i for i in range(len(x)) if x[i] == x[i] and y[i] == y[i]]; r = spearmanr([x[i] for i in ok], [y[i] for i in ok]); return [round(float(r[0]), 3), round(float(r[1]), 4), len(ok)]
def sweet(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float); ok = ~(np.isnan(x) | np.isnan(y)); x, y = x[ok], y[ok]
    from scipy.stats import rankdata
    rx, ry = rankdata(x) / len(x), rankdata(y) / len(y); q = np.quantile(rx, [1 / 3, 2 / 3]); thirds = [y[rx <= q[0]], y[(rx > q[0]) & (rx <= q[1])], y[rx > q[1]]]
    X = np.column_stack([np.ones(len(rx)), rx - 0.5, (rx - 0.5) ** 2]); b, *_ = np.linalg.lstsq(X, ry, rcond=None); res = ry - X @ b
    se = np.sqrt(np.sum(res ** 2) / (len(ry) - 3) * np.linalg.inv(X.T @ X)[2, 2]); from scipy.stats import t as T
    return dict(median_outcome_by_third=[round(float(np.median(t)), 2) for t in thirds], square_term=round(float(b[2]), 3), p=round(float(2 * T.sf(abs(b[2] / se), len(ry) - 3)), 4))
RS = [r for r in rows if r["group"] == "RS"]; BB = [r for r in rows if r["group"] == "BB"]; res = dict(n=dict(RS=len(RS), BB=len(BB), BiMMuDa=len(bim)))
for k in ("near_pitch", "near_rhythm", "alpha_pitch", "alpha_rhythm", "compress"):
    a = [r[k] for r in RS if r[k] == r[k]]; b = [r[k] for r in BB if r[k] == r[k]]
    res[k] = dict(medians=dict(RS=round(float(np.median(a)), 3), BB=round(float(np.median(b)), 3), BiMMuDa=round(float(np.nanmedian([r[k] for r in bim])), 3)),
                  auc_RS_over_BB=auc(a, b) if k != "compress" else auc([-x for x in a], [-x for x in b]),
                  billboard_peak=sp([r[k] for r in BB], [-(r["peak"] or np.nan) for r in BB]), billboard_weeks=sp([r[k] for r in BB], [r["weeks"] or np.nan for r in BB]),
                  bimmuda_position=sp([r[k] for r in bim], [-r["position"] for r in bim]))
res["K1 sweet spot, Billboard (outcome = minus peak)"] = sweet([r["compress"] for r in BB], [-(r["peak"] or np.nan) for r in BB])
res["K3 sweet spot, BiMMuDa (outcome = minus position)"] = sweet([r["compress"] for r in bim], [-r["position"] for r in bim])
res["notes vs compress, all"] = round(float(spearmanr([r["notes"] for r in rows + bim], [r["compress"] for r in rows + bim])[0]), 3)
json.dump(dict(res=res, cocopops=rows, bimmuda=bim), open(os.path.join(H, "scaling_compression.json"), "w"), indent=1); print(json.dumps(res, indent=1))
