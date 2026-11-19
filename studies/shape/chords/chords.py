import gzip, json, pickle, hashlib, collections, re, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
D = json.load(gzip.open("/home/claude/corpus_new/sheetsage-data/hooktheory/Hooktheory.json.gz")); Y = pickle.load(open("/home/claude/zeneng/corpus/v25/yardstick.pkl", "rb")); Y = Y[(Y.src == "HT") & (Y.year <= 2005) & Y.love.notna()].drop_duplicates("id").set_index("id")
by = collections.defaultdict(list)
for k, v in D.items():
    if "MELODY" in v["tags"] and "HARMONY" in v["tags"]: by[f'{v["hooktheory"]["artist"]}/{v["hooktheory"]["song"]}'].append(v["annotations"])
def clip(A, acc):
    mel = sorted(A["melody"], key=lambda x: x["onset"]); har = sorted(A["harmony"], key=lambda x: x["onset"]); K = A["keys"][0]; scale = {(K["tonic_pitch_class"] + s) % 12 for s in np.r_[0, np.cumsum(K["scale_degree_intervals"])]}
    if len(mel) < 4 or len(har) < 2: return
    def tones(h): iv = np.r_[0, np.cumsum(h["root_position_intervals"])]; return {(h["root_pitch_class"] + int(i)) % 12 for i in iv}
    def at(t):
        for h in har:
            if h["onset"] <= t < h["offset"]: return h
        return None
    N = []
    for n in mel:
        h = at(n["onset"]); 
        if h is None: continue
        pc = n["pitch_class"] % 12; p = 12 * n["octave"] + n["pitch_class"]; d = n["offset"] - n["onset"]; ct = pc in tones(h); N.append((n["onset"], n["offset"], p, d, ct, h, pc))
    for i, (on, off, p, d, ct, h, pc) in enumerate(N):
        acc["t"] += d; acc["ct"] += d * ct; rel = (pc - h["root_pitch_class"]) % 12
        if not ct and pc in scale and rel in (1, 2, 5, 6, 8, 9, 10, 11): acc["col"] += d
        if abs(on - round(on)) < 1e-6: acc["beat"] += 1; acc["beat_nct"] += (not ct)
        if not ct and i + 1 < len(N): acc["nct"] += 1; acc["res"] += (N[i + 1][4] and 1 <= abs(N[i + 1][2] - p) <= 2)
    for a, b in zip(har, har[1:]):
        if a["root_pitch_class"] == b["root_pitch_class"] and a["root_position_intervals"] == b["root_position_intervals"]: continue
        acc["chg"] += 1; before = [n for n in N if n[0] < b["onset"]]; after = [n for n in N if n[0] >= b["onset"]]
        if not before or not after: continue
        x, y = before[-1], after[0]
        if x[1] > b["onset"] + 1e-6 or (x[2] == y[2] and y[0] - b["onset"] < 1): acc["held"] += 1
        rm = ((b["root_pitch_class"] - a["root_pitch_class"] + 6) % 12) - 6; mm = y[2] - x[2]
        if rm and mm and abs(rm) != 6: acc["both"] += 1; acc["contra"] += (np.sign(rm) != np.sign(mm))
    for h in har:
        d = h["offset"] - h["onset"]; acc["ht"] += d; third = (h["root_pitch_class"] + h["root_position_intervals"][0]) % 12 if h["root_position_intervals"] else h["root_pitch_class"]; acc["off"] += d * (h["root_pitch_class"] % 12 not in scale or third not in scale)
    acc["notes"] += len(N); acc["chords"] += len(har)
rows = []
for sid, clips in by.items():
    if sid not in Y.index: continue
    acc = collections.Counter()
    for A in clips:
        try: clip(A, acc)
        except Exception as e: pass
    if acc["notes"] < 32 or acc["chords"] < 4 or not acc["nct"] or not acc["chg"] or not acc["both"] or not acc["beat"]: continue
    y = Y.loc[sid]; rows.append(dict(id=sid, title=y.title, year=y.year, peak=y.peak, love=y.love, covers=y.covers, notes=acc["notes"], C1=acc["ct"] / acc["t"], C2=acc["res"] / acc["nct"], C3=acc["held"] / acc["chg"], C4=acc["beat_nct"] / acc["beat"], C5=acc["col"] / acc["t"], C6=acc["off"] / acc["ht"], C7=acc["contra"] / acc["both"]))
x = pd.DataFrame(rows).drop_duplicates("title"); x["cov0"] = x.covers.fillna(0); yr = x.year.values; x["cover_rank"] = [float((x.cov0.values[np.abs(yr - y) <= 5] < c).mean() + .5 * (x.cov0.values[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, x.cov0)]
x["G"] = (x.love + x.cover_rank) / 2; x["half"] = [int(hashlib.md5(t.encode()).hexdigest(), 16) % 2 for t in x.title]; x.to_pickle("chords.pkl")
def part(d, m, g, peak=False):
    d = d.dropna(subset=[m, g]); C = np.c_[tuple([np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + ([rankdata(d.peak.fillna(d.peak.median()))] if peak else []))]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(d[m])), res(rankdata(d[g]))); return round(float(r), 3), round(float(p), 4)
print("songs", len(x), x.half.value_counts().to_dict(), "| medians", x[[f"C{i}" for i in range(1, 8)]].median().round(2).to_dict()); out = {}
for m, s in dict(C1=-1, C2=1, C3=1, C4=1, C5=1, C6=1, C7=1).items():
    a, b, p = part(x[x.half == 0], m, "G"), part(x[x.half == 1], m, "G"), part(x, m, "G"); ok = all(np.sign(v[0]) == s for v in (a, b, p)) and a[1] < .05 and b[1] < .05 and p[1] < .007
    out[m] = dict(pred=s, A=a, B=b, pooled=p, peak_held=part(x, m, "G", True), love=part(x, m, "love"), covers=part(x, m, "cover_rank"), verdict="PASS" if ok else "fail"); print(m, out[m])
json.dump(out, open("chords_results.json", "w"), indent=1)
