"""Held-out test of nesting (PREDICTION_2.md). Melody alone throughout. python3 heldout_bimmuda.py -> heldout_bimmuda.json"""
import sys, os, re, csv, glob, json
import numpy as np, mido
from scipy.stats import spearmanr, mannwhitneyu
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); import ssm_lib as L
B = "/home/claude/data/bimmuda/BiMMuDa"; C = "/home/claude/data/cocopops/CoCoPops"; P = "/home/claude/zeneng-pipeline/songs"
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pcname(s):
    s = (s or "").strip()
    if not s or s[0] not in PC: return None
    return (PC[s[0]] + s[1:].count("#") - s[1:].count("b")) % 12
def ssm_mel(song):
    S = L.bar_sets(song); n = len(S); M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = S[i][0], S[j][0]
            M[i, j] = (len(a & b) / len(a | b)) if (a and b) else (1.0 if i == j else 0.0)
    return M
def read_midi(path, tonic):
    m = mido.MidiFile(path); tpq = m.ticks_per_beat; t = 0; notes = []; num, den = 4, 4; ts_first = None
    for msg in mido.merge_tracks(m.tracks):
        t += msg.time
        if msg.type == "time_signature" and ts_first is None: ts_first = (msg.numerator, msg.denominator)
        if msg.type == "note_on" and msg.velocity > 0: notes.append((t / tpq, msg.note))
    num, den = ts_first or (4, 4); barq = num * 4.0 / den
    if not notes: return None
    n = int(max(t for t, _ in notes) // barq) + 1; bars = [dict(t0=i * barq, len=barq, mel=[], ch=set()) for i in range(n)]
    for tq, p in notes: bars[int(tq // barq)]["mel"].append((tq, p))
    while bars and not bars[0]["mel"]: bars.pop(0)
    return dict(tonic=tonic, bars=bars), (num, den)
norm = lambda s: re.sub(r"[^a-z]", "", s.lower())
coco_titles = set()
for f in glob.glob(C + "/*/Data/*.hum"):
    for l in open(f, errors="ignore"):
        if l.startswith("!!!OTL:"): coco_titles.add(norm(l.split(":", 1)[1])); break
meta = list(csv.DictReader(open(B + "/metadata/bimmuda_per_song_metadata.csv"))); rows = []; skipped = dict(not_44=0, in_cocopops=0, no_file=0, short=0)
for r in meta:
    if r["Time Signature 1"] != "4/4" or r["Time Signature 2"]: skipped["not_44"] += 1; continue
    if norm(r["Title"]) in coco_titles: skipped["in_cocopops"] += 1; continue
    pos = r["Position"].strip(); m_ = re.match(r"(\d+)(\w*)", pos)
    if not m_: skipped["no_file"] += 1; continue
    f = f"{B}/bimmuda_dataset/{r['Year']}/{pos}/{r['Year']}_{int(m_.group(1)):02d}{m_.group(2)}_full.mid"
    if not os.path.exists(f): skipped["no_file"] += 1; continue
    got = read_midi(f, pcname(r["Tonic 1"]) or 0)
    if not got or len(got[0]["bars"]) < 24: skipped["short"] += 1; continue
    M = ssm_mel(got[0]); nf, nmin = L.nest_fine(M)
    rows.append(dict(title=r["Title"], year=int(r["Year"]), position=int(m_.group(1)), bars=len(M), nest=nf, nest_min=nmin))
coco = []
for f in glob.glob(C + "/Billboard/Data/*.hum"):
    s = L.read_hum(f); m = re.match(r"\d+", str(s.get("peak") or ""))
    if not m or sum(len(b["mel"]) for b in s["bars"]) < 40 or len(s["bars"]) < 24: continue
    M = ssm_mel(s); nf, nmin = L.nest_fine(M); coco.append(dict(title=s["title"], peak=int(m.group(0)), bars=len(M), nest=nf, nest_min=nmin))
eng = {}
for f, nm in ((P + "/p64/lyric54.song.json", "song 54"), (P + "/p65/lyric55.song.json", "song 55"), (P + "/p68/lyric58.song.json", "song 58")):
    M = ssm_mel(L.read_record(f)); eng[nm] = [round(x, 3) for x in L.nest_fine(M)]
res = dict(bimmuda_songs=len(rows), skipped=skipped, cocopops_songs=len(coco))
for k in ("nest", "nest_min"):
    x = [r[k] for r in rows if r[k] == r[k]]; y = [-r["position"] for r in rows if r[k] == r[k]]; rho, p = spearmanr(x, y)
    res[f"N1 {k} vs year-end position (rho, one-sided p)"] = [round(float(rho), 3), round(float(p / 2 if rho > 0 else 1 - p / 2), 4)]
    low = [c[k] for c in coco if c["peak"] > 20 and c[k] == c[k]]; u = mannwhitneyu(x, low)
    res[f"N2 {k}: BiMMuDa over CoCoPops peak > 20 (AUC, p)"] = [round(float(u.statistic / (len(x) * len(low))), 3), round(float(u.pvalue), 4), len(low)]
    cx = [c[k] for c in coco if c[k] == c[k]]; cy = [-c["peak"] for c in coco if c[k] == c[k]]
    res[f"N3 {k} vs Billboard peak, discovery sample (rho, p)"] = [round(float(z), 3) for z in spearmanr(cx, cy)]
    res[f"medians {k}: BiMMuDa, CoCoPops all, CoCoPops peak<=10, CoCoPops peak>20"] = [round(float(np.median(x)), 3), round(float(np.median(cx)), 3),
        round(float(np.median([c[k] for c in coco if c["peak"] <= 10 and c[k] == c[k]])), 3), round(float(np.median(low)), 3)]
res["N4 Luthier (nest, nest_min)"] = eng
res["bars vs nest, BiMMuDa"] = round(float(spearmanr([r["bars"] for r in rows], [r["nest"] for r in rows])[0]), 3)
res["year vs nest, BiMMuDa"] = round(float(spearmanr([r["year"] for r in rows], [r["nest"] for r in rows])[0]), 3)
json.dump(dict(res=res, bimmuda=rows, cocopops=coco), open(os.path.join(H, "heldout_bimmuda.json"), "w"), indent=1); print(json.dumps(res, indent=1))
