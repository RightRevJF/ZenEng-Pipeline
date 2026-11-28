"""Reads Discogs-VI 20240701 main.zip (outside the repository) once and writes two files beside it:
  clique_titles.jsonl  per clique: its exact and loose title keys, a traditional-credit flag, and for the match check
                       up to six titles, eight writers, three performing artists (alphabetical) and three genres. No count.
  clique_counts.json   per clique: n_sets, the number of different performing-artist sets (read only at the join).
Artist fields are stored as the text of Python lists; they are parsed as lists here.
python3 -I discogs_index.py /home/claude/dl/discogsvi/main.zip"""
import sys, os, json, zipfile, ast, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import keys as K

def L(v):
    if isinstance(v, list): return v
    if not v: return []
    try:
        x = ast.literal_eval(v); return x if isinstance(x, list) else []
    except Exception: return []

def anorm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))

def main(path):
    out_dir = os.path.dirname(os.path.abspath(path)); z = zipfile.ZipFile(path)
    ft = open(os.path.join(out_dir, "clique_titles.jsonl"), "w"); counts = {}
    with z.open("main/Discogs-VI-20240701.jsonl") as f:
        for i, line in enumerate(f):
            d = json.loads(line); titles = collections.Counter(); writers = collections.Counter(); sets = {}; genres = collections.Counter()
            for v in d["versions"]:
                for t in v["tracks"]:
                    titles[t.get("track_title_cleaned") or t.get("track_title") or ""] += 1
                    titles[t.get("track_title") or ""] += 0
                    for w in L(t.get("track_writer_names")) + L(t.get("release_writer_names")): writers[w] += 1
                    arts = L(t.get("track_artist_names")) or L(t.get("release_artist_names"))
                    a = tuple(sorted({anorm(x) for x in arts if anorm(x) and anorm(x) != "various"}))
                    if a and a not in sets: sets[a] = ", ".join(arts)
                    for g in L(t.get("release_genres")): genres[g] += 1
            raw_titles = [x for x in titles if x]
            ek = sorted({K.exact_key(x) for x in raw_titles} - {""}); lk = sorted({K.loose_key(x) for x in raw_titles} - {""})
            trad = any(K.TRAD.search(w or "") for w in writers)
            arts_show = sorted(sets.values())[:3]
            ft.write(json.dumps(dict(id=d["clique_id"], ek=ek, lk=lk, trad=trad, titles=[x for x, _ in titles.most_common(6)],
                                     writers=[w for w, _ in writers.most_common(8)], artists=arts_show, genres=[g for g, _ in genres.most_common(3)])) + "\n")
            counts[d["clique_id"]] = len(sets)
            if i % 50000 == 0: print(i, flush=True)
    ft.close(); json.dump(counts, open(os.path.join(out_dir, "clique_counts.json"), "w"))
    print(len(counts), "cliques")

if __name__ == "__main__":
    main(sys.argv[1])
