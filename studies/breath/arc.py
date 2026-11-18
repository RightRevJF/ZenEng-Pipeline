"""Does a song's breathing arc sit near the body's 10-second rhythm (0.1 Hz: Mayer waves, the rosary's 6 breaths a minute)?
For each song: the clock length of its bar (McGill timestamps, CoCoPops) and of its four-bar unit; for Billboard songs also the clock length of a
lyric line and of a pair of lines (the McGill line breaks). Compared across Rolling Stone, Billboard (peak) and BiMMuDa (tempo from its metadata).
python3 arc.py -> arc.json"""
import re, os, glob, json, csv, sys
import numpy as np
from scipy.stats import spearmanr, mannwhitneyu
C = "/home/claude/data/cocopops/CoCoPops"
def bars_and_lines(path):
    Lr = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8", errors="ignore") if l.strip() and not l.startswith("!!")]
    head = next(r for r in Lr if r[0].startswith("**"))
    if "**timestamp" not in head: return None
    ts = head.index("**timestamp"); ph = head.index("**phrase") if "**phrase" in head else None
    meter = None; bar_start = []; line_starts = []; pending_bar = False
    for r in Lr[Lr.index(head) + 1:]:
        if len(r) <= ts: continue
        if r[0].startswith("*"):
            for x in r:
                m = re.match(r"\*M(\d+)/(\d+)", x)
                if m and meter is None: meter = (int(m.group(1)), int(m.group(2)))
            continue
        if r[0].startswith("!"): continue
        if r[0].startswith("="): pending_bar = True; continue
        try: sec = float(r[ts])
        except ValueError: sec = None
        if pending_bar and sec is not None: bar_start.append(sec); pending_bar = False
        if ph is not None and r[ph] == "newline" and sec is not None: line_starts.append(sec)
    if len(bar_start) < 16: return None
    bd = np.diff(bar_start); bd = bd[(bd > 0.8) & (bd < 6)]
    if len(bd) < 8: return None
    out = dict(bar_s=float(np.median(bd)), meter=meter)
    if len(line_starts) > 8:
        ld = np.diff(line_starts); ld = ld[(ld > 0.8) & (ld < 30)]; out["line_s"] = float(np.median(ld)) if len(ld) else None
    return out
rows = []
for grp, pat in (("RS", "RollingStone/Data/*.hum"), ("BB", "Billboard/Data/*.hum")):
    for f in sorted(glob.glob(os.path.join(C, pat))):
        g = bars_and_lines(f)
        if not g or (g["meter"] and g["meter"][0] not in (4, 2)): continue
        meta = {x.group(1): x.group(2) for x in (re.match(r"!!!([^:]+):\s*(.*)", l) for l in open(f, errors="ignore")) if x}
        pk = re.match(r"\d+", meta.get("BillboardPeak", "")); wk = re.match(r"\d+", meta.get("BillboardWeeksOnChart", ""))
        g.update(group=grp, file=os.path.basename(f), peak=int(pk.group(0)) if pk else None, weeks=int(wk.group(0)) if wk else None, hyper4=4 * g["bar_s"])
        if g.get("line_s"): g["couplet"] = 2 * g["line_s"]
        rows.append(g)
B = "/home/claude/data/bimmuda/BiMMuDa"; bim = []
for m in csv.DictReader(open(B + "/metadata/bimmuda_per_song_metadata.csv")):
    if m["Time Signature 1"] != "4/4" or m["Time Signature 2"]: continue
    try: bpm = float(m["BPM 1"])
    except ValueError: continue
    if m["BPM 2"]: continue
    pos = re.match(r"\d+", m["Position"]).group(0); bim.append(dict(title=m["Title"], year=int(m["Year"]), position=int(pos), bpm=bpm, hyper4=16 * 60 / bpm, bar_s=4 * 60 / bpm))
near = lambda x: -abs(np.log(x / 10.0))
def auc(a, b): u = mannwhitneyu(a, b); return [round(float(u.statistic / (len(a) * len(b))), 3), round(float(u.pvalue), 4)]
res = {}
for k in ("hyper4", "couplet"):
    rs = [r[k] for r in rows if r["group"] == "RS" and r.get(k)]; bb = [r for r in rows if r["group"] == "BB" and r.get(k)]
    res[k] = dict(n=dict(RS=len(rs), BB=len(bb)), quartiles_RS=[round(float(x), 2) for x in np.quantile(rs, (0.25, 0.5, 0.75))] if rs else None,
                  quartiles_BB=[round(float(x), 2) for x in np.quantile([r[k] for r in bb], (0.25, 0.5, 0.75))],
                  share_8_to_12_s=dict(RS=round(float(np.mean([(8 <= x <= 12) for x in rs])), 3) if rs else None, BB=round(float(np.mean([(8 <= r[k] <= 12) for r in bb])), 3)),
                  nearness_RS_over_BB=auc([near(x) for x in rs], [near(r[k]) for r in bb]) if rs else None,
                  nearness_vs_peak=[round(float(z), 3) for z in spearmanr([near(r[k]) for r in bb if r["peak"]], [-r["peak"] for r in bb if r["peak"]])],
                  nearness_vs_weeks=[round(float(z), 3) for z in spearmanr([near(r[k]) for r in bb if r["weeks"]], [r["weeks"] for r in bb if r["weeks"]])])
bh = [b["hyper4"] for b in bim]
res["bimmuda_hyper4"] = dict(n=len(bim), quartiles=[round(float(x), 2) for x in np.quantile(bh, (0.25, 0.5, 0.75))], share_8_to_12_s=round(float(np.mean([(8 <= x <= 12) for x in bh])), 3),
                             nearness_vs_position=[round(float(z), 3) for z in spearmanr([near(b["hyper4"]) for b in bim], [-b["position"] for b in bim])],
                             nearness_hits_over_BB_low=auc([near(x) for x in bh], [near(r["hyper4"]) for r in rows if r["group"] == "BB" and r["peak"] and r["peak"] > 20]))
json.dump(dict(res=res, rows=rows, bimmuda=bim), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "arc.json"), "w"), indent=1); print(json.dumps(res, indent=1))
