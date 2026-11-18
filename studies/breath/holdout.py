"""Breath held out on Hooktheory songs joined to the Hot 100 (PREDICTION_holdout.md, written first). python3 holdout.py -> holdout.json
Data: /home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz (Sheet Sage); /home/claude/data/hot100/hot-100-current.csv
(https://raw.githubusercontent.com/utdata/rwd-billboard-data/main/data-out/hot-100-current.csv)."""
import gzip, json, re, glob, csv, os, collections
import numpy as np, pandas as pd
from scipy.signal import periodogram
from scipy.stats import fisher_exact, mannwhitneyu
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$|with .*$", "", str(s).lower().replace("&", "and").replace("-", " ")))
def signal(on, dt=0.25, gap=1.5):
    on = np.array(sorted(set(on))) - min(on); s = np.zeros(int(on[-1] / dt) + 8)
    for a, b in zip(on, list(on[1:]) + [on[-1] + 1]):
        end = b if b - a < gap else a + 1.0; s[int(a / dt):int(end / dt)] = 1
    return s
def reading(on, spq, maxper):
    s = signal(on); s = s - s.mean(); f, P = periodogram(s, fs=4.0, window="hann")
    w = (f >= 1 / maxper) & (f <= 1 / 3); dom = 1 / f[w][np.argmax(P[w])]
    return dict(dom_beats=float(dom), dom_s=float(dom * spq), locked=bool(any(abs(dom - k) < 0.6 for k in (4, 8, 16))), hyper4=16 * spq)
H = pd.read_csv("/home/claude/data/hot100/hot-100-current.csv"); H["t"] = H.title.map(norm); H["a"] = H.performer.map(norm)
best = H.groupby(["t", "a"]).peak_pos.min().reset_index(); bytitle = collections.defaultdict(list)
for t, a, p in best.itertuples(index=False): bytitle[t].append((a, int(p)))
seen = set()
for f in glob.glob("/home/claude/data/cocopops/CoCoPops/*/Data/*.hum"):
    for l in open(f, errors="ignore"):
        if l.startswith("!!!OTL"): seen.add(norm(l.split(":", 1)[1])); break
for m in csv.DictReader(open("/home/claude/data/bimmuda/BiMMuDa/metadata/bimmuda_per_song_metadata.csv")): seen.add(norm(m["Title"]))
D = json.load(gzip.open("/home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz")); clips = {}
for k, v in D.items():
    a = v["annotations"]; al = (v.get("alignment") or {}).get("refined")
    if "MELODY" not in v["tags"] or not a.get("melody") or not al or len(a["meters"]) != 1 or a["meters"][0]["beats_per_bar"] != 4 or a["meters"][0]["beat_unit"] != 4: continue
    key = (norm(v["hooktheory"]["song"]), norm(v["hooktheory"]["artist"]))
    if key[0] in seen: continue
    if key not in clips or a["num_beats"] > clips[key][0]["num_beats"]: clips[key] = (a, al)
rows = []
for (t, art), (a, al) in clips.items():
    cand = [p for ha, p in bytitle.get(t, []) if ha == art or ha.startswith(art) or art.startswith(ha)]
    if not cand: continue
    b = np.array(al["beats"], float); ts = np.array(al["times"], float)
    if len(b) < 2: continue
    spq = float(np.median(np.diff(ts) / np.diff(b))); on = [n["onset"] for n in a["melody"]]
    if len(on) < 20 or not (0.25 < spq < 1.5): continue
    rows.append(dict(t=t, a=art, peak=min(cand), beats=a["num_beats"], spq=spq, on=on))
def test(minbeats, maxper):
    R = []
    for r in rows:
        if r["beats"] < minbeats or max(r["on"]) - min(r["on"]) < minbeats - 8: continue
        x = reading(r["on"], r["spq"], maxper); x.update(peak=r["peak"]); R.append(x)
    top = [x for x in R if x["peak"] <= 10]; low = [x for x in R if x["peak"] > 20]
    a, c = sum(x["locked"] for x in top), sum(x["locked"] for x in low)
    odds, p1 = fisher_exact([[a, len(top) - a], [c, len(low) - c]], alternative="greater")
    u = mannwhitneyu([x["hyper4"] for x in top], [x["hyper4"] for x in low], alternative="greater")
    return dict(n_top10=len(top), n_below20=len(low), H1_locked_share=[round(a / len(top), 3), round(c / len(low), 3)], H1_odds=round(float(odds), 3), H1_p=round(float(p1), 4),
                H2_hyper4_median=[round(float(np.median([x["hyper4"] for x in top])), 2), round(float(np.median([x["hyper4"] for x in low])), 2)],
                H2_auc=round(float(u.statistic / (len(top) * len(low))), 3), H2_p=round(float(u.pvalue), 4),
                H3_top10_commonest=collections.Counter(round(x["dom_beats"]) for x in top).most_common(4),
                below20_commonest=collections.Counter(round(x["dom_beats"]) for x in low).most_common(4),
                breath_s_median=[round(float(np.median([x["dom_s"] for x in top])), 2), round(float(np.median([x["dom_s"] for x in low])), 2)])
res = dict(joined=len(rows), primary_64=test(64, 32), secondary_32=test(32, 16))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "holdout.json"), "w"), indent=1); print(json.dumps(res, indent=1))
