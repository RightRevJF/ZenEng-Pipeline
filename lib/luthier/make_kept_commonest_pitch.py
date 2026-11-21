"""956 (749.134): tables/kept_commonest_pitch.json from the kept 4/4 songs. python3 lib/luthier/make_kept_commonest_pitch.py
The share of a part's sung notes on its commonest pitch, verses pooled and choruses pooled (a part of fewer than 20 notes left out). The engine passes over a build over the kept 90th in either part
(studies/commonest_pitch, studies/pitch_ceiling)."""
import os, sys, json, re, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kept_corpus as KC
def kind(x):
    """957 (749.139): a part told by its exact name. 'Chorus 2', 'Last Chorus', 'refrain' are choruses; 'Verse 3' a verse; a pre-chorus or pre-verse is neither (22 kept songs' pre-choruses had been pooled with their choruses)."""
    w = re.findall(r"[a-z]+", str(x).lower())
    if any(z.startswith("pre") for z in w): return None
    return "Chorus" if ("chorus" in w or "refrain" in w) else "Verse" if "verse" in w else None
def share(ps): return max(collections.Counter(ps).values()) / len(ps) if len(ps) >= 20 else None
if __name__ == "__main__":
    kept = {"Verse": [], "Chorus": []}
    for k in KC.kept_songs():
        for part in kept:
            s = share([p for p, x in zip(k["p"], k["sec"]) if kind(x) == part])
            if s is not None: kept[part].append(s)
    rng = np.random.default_rng(0)                                                          # 957: each ceiling with its bootstrap range (songs resampled, 2,000 times)
    out = dict(source="kept 4/4 songs (CoCoPops Billboard); made by lib/luthier/make_kept_commonest_pitch.py", what="the share of a part's sung notes on its commonest pitch; ceiling = the kept 90th",
               parts={part: dict(songs=len(v), p10_25_50_75_90=[round(float(x), 3) for x in np.percentile(v, (10, 25, 50, 75, 90))], ceiling=round(float(np.percentile(v, 90)), 3),
                                 ceiling_range_90=[round(float(x), 3) for x in np.percentile([np.percentile(rng.choice(v, len(v)), 90) for _ in range(2000)], (5, 95))]) for part, v in kept.items()})
    json.dump(out, open(os.path.join(HERE, "..", "..", "tables", "kept_commonest_pitch.json"), "w"), indent=1); print(out["parts"])
