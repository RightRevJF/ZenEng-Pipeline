"""Discogs-VI cover counts for the Hooktheory songs: match on the cleaned title and the Hooktheory artist among the clique's
performing artists. Covers = distinct performing artist sets in the clique minus one (0 = only the original artist's versions)."""
import json, re, gzip, collections
import numpy as np
def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))
Q = json.load(open("/home/claude/shape/discogs_cliques.json")); by = collections.defaultdict(list)
for q in Q: by[q["title"]].append(q)
D = json.load(gzip.open("/home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz")); songs = {}
for c in D.values():
    yt = (c.get("youtube") or {}).get("id")
    if yt: songs[yt] = (norm(c["hooktheory"]["artist"]), norm(c["hooktheory"]["song"]))
out = {}
for vid, (a, s) in songs.items():
    cands = [q for q in by.get(s, []) if a in q["artists"]]
    if cands:
        q = max(cands, key=lambda q: q["n_artist_sets"])
        out[vid] = dict(covers=q["n_artist_sets"] - 1, versions=q["versions"], releases=q["releases"], first_year=q["first_year"], clique=q["id"])
json.dump(out, open("/home/claude/shape/hooktheory_covers_discogs.json", "w"))
c = np.array([o["covers"] for o in out.values()])
print(len(songs), "videos;", len(out), "matched; covers median", np.median(c), "IQR", np.percentile(c, [25, 75]), "share with no cover %.2f" % np.mean(c == 0), "max", c.max())
