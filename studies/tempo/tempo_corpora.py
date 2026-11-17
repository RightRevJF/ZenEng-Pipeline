"""Tempo, metre and length. BiMMuDa (381 top-five singles 1950-2022): BPM 1 by era, genre and mode; how often a second tempo is listed
(BPM 2, a half- or double-time reading or a tempo change); time signatures by era. McGill Billboard (739 songs 1958-91): metre from the
header and length from the annotation by period (lengths from ../edges/edges_billboard.json). Writes tempo_results.json."""
import csv, json, collections, statistics as st, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
def q(v):
    v = sorted(v); n = len(v)
    return [round(v[int(.25 * (n - 1))]), round(st.median(v)), round(v[int(.75 * (n - 1))])] if n else None
rows = list(csv.DictReader(open("/home/claude/data/bimmuda/BiMMuDa/metadata/bimmuda_per_song_metadata.csv")))
def era(y): return "1950-59" if y < 1960 else "1960-69" if y < 1970 else "1970-79" if y < 1980 else "1980-89" if y < 1990 else "1990-99" if y < 2000 else "2000-09" if y < 2010 else "2010-22"
G = collections.defaultdict(list); TS = collections.defaultdict(collections.Counter); B2 = collections.Counter(); N = collections.Counter(); REL = collections.Counter()
for r in rows:
    try: b = float(r["BPM 1"]); y = int(r["Year"])
    except ValueError: continue
    g = r["Genre (Broad 1)"].strip(); mode = "minor" if r["Mode 1"].strip().lower().startswith("min") else "major"
    for k in ("all", era(y), "genre: " + g, "mode: " + mode): G[k].append(b); N[k] += 1
    ts = r["Time Signature 1"].strip(); TS[era(y)][ts] += 1; TS["all"][ts] += 1
    b2 = r["BPM 2"].strip()
    if b2:
        try:
            x = float(b2); B2[era(y)] += 1; B2["all"] += 1
            ratio = max(x, b) / min(x, b)
            REL["half or double" if abs(ratio - 2) < 0.15 else "other change"] += 1
        except ValueError: pass
out = {"BiMMuDa": {k: dict(songs=len(v), bpm=q(v), under80=round(100 * sum(x < 80 for x in v) / len(v)), over130=round(100 * sum(x > 130 for x in v) / len(v)),
                        band_95_130=round(100 * sum(95 <= x <= 130 for x in v) / len(v)), second_tempo=round(100 * B2[k] / N[k]) if k in B2 else 0)
                   for k, v in G.items() if len(v) >= 15},
       "BiMMuDa second tempo kinds": dict(REL),
       "BiMMuDa time signatures": {k: {t: round(100 * c / sum(v.values())) for t, c in v.most_common(5)} for k, v in TS.items()}}
# McGill
SRC = "/home/claude/data/choco/smashub-choco-f7dd3ee/partitions/billboard/raw"
E = json.load(open(os.path.join(HERE, "..", "edges", "edges_billboard.json")))
def per(y): return "1958-64" if y < 1965 else "1965-69" if y < 1970 else "1970-74" if y < 1975 else "1975-79" if y < 1980 else "1980-84" if y < 1985 else "1985-91"
M = collections.defaultdict(collections.Counter); L = collections.defaultdict(list)
for x in E:
    p = per(x["year"]); m = (x.get("metre") or "").strip()
    M[p][m] += 1; M["all"][m] += 1; L[p].append(x["length"]); L["all"].append(x["length"])
out["McGill metre"] = {k: {t: round(100 * c / sum(v.values())) for t, c in v.most_common(5)} for k, v in M.items()}
out["McGill length (s)"] = {k: dict(songs=len(v), length=q(v), under_180=round(100 * sum(s < 180 for s in v) / len(v)), over_240=round(100 * sum(s > 240 for s in v) / len(v))) for k, v in L.items()}
json.dump(out, open(os.path.join(HERE, "tempo_results.json"), "w"), indent=1)
for k, v in out.items(): print(k); [print("  ", a, b) for a, b in (v.items() if isinstance(v, dict) else [])]
