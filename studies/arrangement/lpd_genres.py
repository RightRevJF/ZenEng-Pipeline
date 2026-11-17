"""Arrangement study, part 2a: a genre for each Lakh Pianoroll (LPD-5 cleansed, Dong et al. 2018; CC BY 4.0, Zenodo 5646574) song from
the Million Song Dataset's artist terms (via Gold-Caps LMD-Matched, Zenodo 10178563; CC BY 4.0): the family of the artist's
highest-weighted term. Artist-level and noisy: a reading, not ground truth. Writes lpd_genres.json."""
import json, os, glob, collections, ast
G = json.load(open("/home/claude/data/lpd/goldcaps.json"))
FAM = [("gospel", ["gospel", "ccm", "christian", "worship", "praise", "hymn"]), ("country", ["country", "honky tonk", "bluegrass", "americana", "outlaw", "nashville"]),
       ("soul / r&b", ["soul", "r&b", "rhythm and blues", "motown", "quiet storm", "funk"]), ("blues", ["blues"]), ("folk", ["folk", "singer-songwriter"]),
       ("metal", ["metal"]), ("hip hop", ["hip hop", "rap"]), ("jazz", ["jazz", "swing", "bebop"]), ("electronic", ["house", "techno", "trance", "electronic", "electro", "eurodance", "disco"]),
       ("rock", ["rock", "punk", "grunge"]), ("pop", ["pop", "ballad", "easy listening", "adult contemporary"])]
def fam(term):
    t = term.lower()
    for f, keys in FAM:
        if any(k in t for k in keys): return f
    return None
byid = {}
for r in G:
    try: terms = ast.literal_eval(r["artist_terms"]); fr = ast.literal_eval(r["artist_terms_freq"])
    except Exception: continue
    if not terms: continue
    best = sorted(zip(fr, range(len(terms)), terms), key=lambda x: (-x[0], x[1]))
    f = next((fam(t) for _, _, t in best[:3] if fam(t)), None)
    if f: byid[r["track_id"]] = dict(genre=f, term=best[0][2], artist=r.get("artist_name"), title=r.get("title"))
files = glob.glob("/home/claude/data/lpd/lpd_5/lpd_5_cleansed/*/*/*/*/*.npz")
out = {}
for f in files:
    tid = f.split("/")[-2]
    if tid in byid: out[f] = byid[tid]
json.dump(out, open("lpd_genres.json", "w"))
print(len(files), "files;", len(out), "with a genre;", collections.Counter(v["genre"] for v in out.values()).most_common())
