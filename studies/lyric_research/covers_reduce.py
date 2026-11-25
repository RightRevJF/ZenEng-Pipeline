"""Reduce Discogs-VI (streamed from stdin) to cover counts for the Billboard songs.

unzip -p main.zip main/Discogs-VI-20240701.jsonl | python3 -I covers_reduce.py
Writes /home/claude/lyr_dl/covers.csv: song_key, artist_key, n_cover_artists
(distinct recording artists in the clique other than the hit's artist).
"""
import sys, json, csv, re

FEAT = "/home/claude/lyr_dl/feat.csv"
OUT = "/home/claude/lyr_dl/covers.csv"


def norm(s):
    s = s.lower(); s = re.sub(r"\(.*?\)|\[.*?\]", "", s)
    s = re.sub(r"\s(feat|featuring|with|and|&|duet)\b.*", "", s)
    s = re.sub(r"^the ", "", s.strip()); return re.sub(r"[^a-z0-9]", "", s)


songs = {}
for r in csv.DictReader(open(FEAT)):
    songs.setdefault(r["song_key"], []).append(r["artist_key"])
best = {}
n = 0
for line in sys.stdin:
    n += 1
    if n % 50000 == 0:
        print(n, len(best), file=sys.stderr, flush=True)
    c = json.loads(line)
    titles, arts = set(), set()
    for v in c["versions"]:
        for t in v["tracks"][:1]:
            titles.add(norm(t.get("track_title_cleaned") or t["track_title"]))
            for a in t["track_artist_names"]:
                arts.add(norm(re.sub(r"\s\(\d+\)$", "", a)))
    for t in titles & set(songs):
        for a in songs[t]:
            if any(a[:6] in x or x[:6] in a for x in arts if x):
                k = (t, a); others = sum(1 for x in arts if x and not (a[:6] in x or x[:6] in a))
                best[k] = max(best.get(k, 0), others)
with open(OUT, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["song_key", "artist_key", "n_cover_artists"])
    for (t, a), k in best.items():
        w.writerow([t, a, k])
print("cliques", n, "matched", len(best), file=sys.stderr)
