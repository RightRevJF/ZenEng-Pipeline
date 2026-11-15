"""Cover counts for the Hooktheory songs: SHS100K (SecondHandSongs research release, github.com/NovaFrost/SHS100K) lists ~9,400 works
with the versions it sampled. A Hooktheory song matches a work when the normalised title equals the Hooktheory song slug and one of
the work's performers equals the Hooktheory artist slug. Writes hooktheory_covers.json: video id -> versions, performers."""
import json, re, collections, gzip
def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))
works = collections.defaultdict(lambda: dict(title=None, perf=[], n=0))
for line in open("/home/claude/dl/shape/shs/SHS100K/list", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 4: continue
    w = works[p[0]]; w["title"] = w["title"] or p[2]; w["perf"].append(p[3]); w["n"] += 1
by_title = collections.defaultdict(list)
for k, w in works.items(): by_title[norm(w["title"])].append(k)
D = json.load(gzip.open("/home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz"))
out = {}; songs = {}
for c in D.values():
    yt = (c.get("youtube") or {}).get("id"); h = c["hooktheory"]
    if not yt: continue
    songs[yt] = (norm(h["artist"]), norm(h["song"]))
for vid, (a, s) in songs.items():
    for k in by_title.get(s, []):
        w = works[k]
        if any(norm(p) == a for p in w["perf"]):
            out[vid] = dict(versions=w["n"], work=k, title=w["title"], original=w["perf"][0], artist_is_first=norm(w["perf"][0]) == a); break
json.dump(out, open("/home/claude/shape/hooktheory_covers.json", "w"))
import numpy as np
v = np.array([o["versions"] for o in out.values()])
print(len(songs), "Hooktheory videos;", len(out), "matched to SHS100K works; versions median", np.median(v) if len(v) else None, "IQR", np.percentile(v, [25, 75]) if len(v) else None,
      "; the Hooktheory artist is the first performer in", sum(o["artist_is_first"] for o in out.values()))
