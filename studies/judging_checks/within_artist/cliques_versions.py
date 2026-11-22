"""R02-2: as studies/covers/discogs_cliques.py (the same per-clique reduction, the same output), and beside it each clique's versions kept:
per version its earliest year, its performing artists and its release ids. Reads main.zip without unpacking.
python3 cliques_versions.py -> /home/claude/shape/discogs_cliques.json and /home/claude/shape/discogs_versions.jsonl (not committed: large)."""
import zipfile, json, re, collections
def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))
z = zipfile.ZipFile("/home/claude/dl/shape/discogs/main.zip"); out = []; vf = open("/home/claude/shape/discogs_versions.jsonl", "w")
with z.open("main/Discogs-VI-20240701.jsonl") as f:
    for i, line in enumerate(f):
        d = json.loads(line); titles = collections.Counter(); artists = set(); years = []; releases = set(); writers = set(); per = {}
        for v in d["versions"]:
            for t in v["tracks"]:
                titles[t.get("track_title_cleaned") or ""] += 1
                a = tuple(sorted(norm(x) for x in (t.get("track_artist_names") or t.get("release_artist_names") or [])))
                y = re.match(r"(\d{4})", t.get("released") or ""); yy = int(y.group(1)) if y and 1890 <= int(y.group(1)) <= 2025 else None
                if a:
                    artists.add(a); p = per.setdefault(a, dict(year=None, releases=[]))
                    if yy is not None: p["year"] = yy if p["year"] is None else min(p["year"], yy)
                    if t.get("release_id") is not None and len(p["releases"]) < 5: p["releases"].append(t.get("release_id"))
                if yy is not None: years.append(yy)
                releases.add(t.get("release_id")); writers.update(t.get("track_writer_names") or [])
        out.append(dict(id=d["clique_id"], title=norm(titles.most_common(1)[0][0]) if titles else "", artists=sorted({x for a in artists for x in a}),
                        n_artist_sets=len(artists), versions=len(d["versions"]), releases=len(releases), first_year=min(years) if years else None, writers=sorted(writers)[:6]))
        vf.write(json.dumps(dict(id=d["clique_id"], sets=[[list(a), p["year"], p["releases"]] for a, p in per.items()])) + "\n")
        if i % 50000 == 0: print(i, flush=True)
json.dump(out, open("/home/claude/shape/discogs_cliques.json", "w")); vf.close()
print(len(out), "cliques")
