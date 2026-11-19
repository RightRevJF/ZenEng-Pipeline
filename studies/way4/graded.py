"""The larger graded set (way 4 groundwork). Four sources, one form: each song a list of (onset in quarter-note beats, midi pitch), with what is known of how it fared.
  HT  Hooktheory clips (melody), joined by title and artist to the Hot 100 record (peak, weeks, first week)      -> the largest
  CB  CoCoPops Billboard sample, whole songs (peak, weeks)
  RS  CoCoPops Rolling Stone 200, whole songs (the 2004 list's rank)
  BM  BiMMuDa, Billboard year-end top five 1950-2022, a song's sections joined (year-end position)
python3 graded.py -> graded.pkl, graded_summary.json"""
import gzip, json, re, sys, glob, pickle, collections, os
import numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/rightrevjf/zeneng-pipeline/studies/ssm")
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
def hot100():
    b = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); b["t"] = b.title.map(norm); b["a"] = b.performer.map(norm); b["year"] = b["first"].str[:4].astype(int); return b
def hooktheory(B):
    D = json.load(gzip.open("/home/claude/corpus_new/sheetsage-data/hooktheory/Hooktheory.json.gz")); by = collections.defaultdict(list); idx = collections.defaultdict(list)
    for r in B.itertuples(): idx[r.t].append(r)
    for k, v in D.items():
        if "MELODY" not in v["tags"]: continue
        A = v["annotations"]; m = A.get("melody") or []
        if len(m) < 8 or len(A["meters"]) != 1 or A["meters"][0]["beats_per_bar"] != 4: continue
        ns = sorted((float(x["onset"]), int(60 + 12 * x["octave"] + x["pitch_class"])) for x in m); by[(v["hooktheory"]["artist"], v["hooktheory"]["song"])].append((k, ns, A["keys"][0]["tonic_pitch_class"]))
    out = []
    for (a, s), clips in by.items():
        an, sn = norm(a.replace("-", " ")), norm(s.replace("-", " ")); hit = [r for r in idx.get(sn, []) if an and (an in r.a or r.a in an)]
        g = min(hit, key=lambda r: r.peak) if hit else None
        out.append(dict(src="HT", id=f"{a}/{s}", title=sn, artist=an, clips=[ns for _, ns, _ in sorted(clips)], peak=float(g.peak) if g else None, weeks=float(g.weeks) if g else None, year=int(g.year) if g else None))
    return out
def cocopops_billboard():
    d = pd.read_csv("/home/claude/zeneng/corpus/cocopops_notes.csv.gz"); out = []
    num = lambda x: min(float(v) for v in re.findall(r"\d+", str(x))) if re.findall(r"\d+", str(x)) else None
    for s, g in d.groupby("song", sort=False):
        g = g.sort_values("abs_beat"); ns = [(float(t), int(p)) for t, p in zip(g.abs_beat, g.pitch) if p == p]
        if len(ns) >= 100: out.append(dict(src="CB", id=str(s), title=norm(g.title.iloc[0]), artist=norm(str(s).split("_")[0]), clips=[ns], peak=num(g.peak.iloc[0]), weeks=(max(float(v) for v in re.findall(r"\d+", str(g.weeks.iloc[0]))) if re.findall(r"\d+", str(g.weeks.iloc[0])) else None), year=int(g.year.iloc[0])))
    return out
def rolling_stone():
    import ssm_lib as L; out = []
    for f in sorted(glob.glob("/home/claude/corpus/try2/CoCoPops/RollingStone/Data/*.hum")):
        try: S = L.read_hum(f)
        except Exception as e: continue
        ns = sorted((float(t), int(p)) for b in S["bars"] for t, p in b["mel"] if p is not None); head = open(f, errors="ignore").read(600)
        rk = re.search(r"Rolling Stone List Rank:\s*(\d+)", head); otl = re.search(r"!!!OTL:\s*(.*)", head); yr = re.search(r"_(\d{4})\.hum", f)
        if len(ns) >= 100 and rk: out.append(dict(src="RS", id=os.path.basename(f)[:-4], title=norm(otl.group(1) if otl else ""), artist=norm(os.path.basename(f).split("_")[0]), clips=[ns], rank=int(rk.group(1)), year=int(yr.group(1)) if yr else None))
    return out
def bimmuda():
    B = json.load(open("/home/claude/corpus/parsed_bimmuda.json")); by = collections.defaultdict(list); meta = pd.read_csv("/home/claude/corpus/BiMMuDa/metadata/bimmuda_per_song_metadata.csv")
    for m in B:
        if m.get("ts") not in ("4/4", None): continue
        y, pos, n = m["id"].split("_"); pos = re.sub(r"\D", "", pos); by[(int(y), int(pos))].append((n, [(float(x["off"]), int(x["p"])) for x in m["notes"]]))
    T = {(int(r.Year), int(re.sub(r"\D", "", str(r.Position)))): (norm(r.Title), norm(r.Artist)) for r in meta.itertuples()}; out = []
    for (y, pos), secs in by.items():
        clips = [ns for _, ns in sorted(secs) if len(ns) >= 8]
        if sum(len(c) for c in clips) >= 40: out.append(dict(src="BM", id=f"{y}_{pos}", title=T.get((y, pos), ("", ""))[0], artist=T.get((y, pos), ("", ""))[1], clips=clips, position=pos, year=y))
    return out
if __name__ == "__main__":
    B = hot100(); S = hooktheory(B) + cocopops_billboard() + rolling_stone() + bimmuda()
    # the Hot 100 record for the Rolling Stone and BiMMuDa songs too, where they charted
    idx = collections.defaultdict(list)
    for r in B.itertuples(): idx[r.t].append(r)
    for s in S:
        if s["src"] in ("RS", "BM") and s["title"]:
            hit = [r for r in idx.get(s["title"], []) if s["artist"] and (s["artist"][:6] in r.a or r.a[:6] in s["artist"])]
            if hit: g = min(hit, key=lambda r: r.peak); s["peak"], s["weeks"] = float(g.peak), float(g.weeks)
    pickle.dump(S, open("graded.pkl", "wb")); R = {}
    for src in ("HT", "CB", "RS", "BM"):
        v = [s for s in S if s["src"] == src]; g = [s for s in v if s.get("peak") is not None]
        R[src] = dict(songs=len(v), with_chart_record=len(g), notes_median=int(np.median([sum(len(c) for c in s["clips"]) for s in v])), clips_median=float(np.median([len(s["clips"]) for s in v])),
                      peak_quartiles=[float(x) for x in np.percentile([s["peak"] for s in g], (25, 50, 75))] if g else None, weeks_quartiles=[float(x) for x in np.percentile([s["weeks"] for s in g], (25, 50, 75))] if g else None)
    json.dump(R, open("graded_summary.json", "w"), indent=1); print(json.dumps(R, indent=1))
