"""Discogs-VI (CC BY-SA 4.0; Araz, Serra & Bogdanov, ISMIR 2024): 348,796 cliques of versions found from Discogs editorial metadata
(shared writers and title). Streamed from main.zip without unpacking; reduced per clique to the cleaned title, the distinct
performing artists (a version's track artists), versions, releases carrying the song, the earliest release year and the writers.
Writes discogs_cliques.json (compact)."""
import zipfile, json, re, collections, sys
def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))
z = zipfile.ZipFile("/home/claude/dl/shape/discogs/main.zip"); out = []
with z.open("main/Discogs-VI-20240701.jsonl") as f:
    for i, line in enumerate(f):
        d = json.loads(line); titles = collections.Counter(); artists = set(); years = []; releases = set(); writers = set()
        for v in d["versions"]:
            for t in v["tracks"]:
                titles[t.get("track_title_cleaned") or ""] += 1
                a = tuple(sorted(norm(x) for x in (t.get("track_artist_names") or t.get("release_artist_names") or [])))
                if a: artists.add(a)
                y = re.match(r"(\d{4})", t.get("released") or "")
                if y and 1890 <= int(y.group(1)) <= 2025: years.append(int(y.group(1)))
                releases.add(t.get("release_id")); writers.update(t.get("track_writer_names") or [])
        out.append(dict(id=d["clique_id"], title=norm(titles.most_common(1)[0][0]) if titles else "", artists=sorted({x for a in artists for x in a}),
                        n_artist_sets=len(artists), versions=len(d["versions"]), releases=len(releases), first_year=min(years) if years else None, writers=sorted(writers)[:6]))
        if i % 50000 == 0: print(i, flush=True)
json.dump(out, open("/home/claude/shape/discogs_cliques.json", "w"))
print(len(out), "cliques")
