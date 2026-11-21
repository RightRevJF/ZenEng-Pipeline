"""749.134: the commonest pitch's share, by part, kept songs and Luthier's. See PREDICTION.md. python3 studies/commonest_pitch/study.py -> result.json"""
import sys, os, json, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC
def kind(x): x = str(x).lower(); return "Chorus" if ("chorus" in x or "refrain" in x) else "Verse" if "verse" in x else None
def share(ps): return max(collections.Counter(ps).values()) / len(ps) if len(ps) >= 20 else None
kept = {"Verse": [], "Chorus": []}
for k in KC.kept_songs():
    for part in kept:
        s = share([p for p, x in zip(k["p"], k["sec"]) if kind(x) == part])
        if s is not None: kept[part].append(s)
out = dict(kept={part: dict(songs=len(v), p10_25_50_75_90=[round(float(x), 3) for x in np.percentile(v, (10, 25, 50, 75, 90))]) for part, v in kept.items()}, songs={})
for tag, path in (("55", "songs/p65/lyric55.song.json"), ("54", "songs/p64/lyric54.song.json"), ("58", "songs/p68/lyric58.song.json"), ("60", "songs/p70/lyric60.v42.song.json"), ("59", "songs/p69/lyric59.song.json")):
    R = json.load(open(os.path.join(ROOT, path))); ns = R["melody"]["notes"]; out["songs"][tag] = {}
    for part in kept:
        s = share([n["midi"] for n in ns if kind(n.get("sec")) == part]); out["songs"][tag][part] = None if s is None else dict(share=round(s, 3), over_the_kept_90th=bool(s > out["kept"][part]["p10_25_50_75_90"][4]))
T4 = ("55", "54", "58", "60"); out["over_of_four"] = {part: sum(bool(out["songs"][t][part] and out["songs"][t][part]["over_the_kept_90th"]) for t in T4) for part in kept}
out["verdict"] = "the engine's: a floor is proposed" if max(out["over_of_four"].values()) >= 2 else "one song's: flagged, not gated" if max(out["over_of_four"].values()) == 1 else "closed: no chosen tune over the kept 90th"
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1)
