"""Word setting in PDMX (Long et al.; public-domain MuseScore scores on Zenodo, record 15571083, CC BY 4.0): scores with lyrics,
deduplicated, no licence conflict; English only (score_words.english); the first part that carries lyrics. Categories from PDMX's
genre and tag fields: hymns and sacred (religious genre, or tags or title naming hymn, gospel, carol, Christmas, church, sacred,
Christian), folk, popular (pop, rock, R&B, jazz, soundtrack, country), and other classical (art song, choral, opera).
Fetch: PDMX.csv and mxl.tar.gz from zenodo.org/records/15571083 into /home/claude/data/pdmx; extract with --extract once."""
import os, re, sys, json, tarfile, collections, pandas as pd
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); D = "/home/claude/data/pdmx"
SACRED = re.compile(r"hymn|gospel|carol|christmas|church|sacred|christian|worship|psalm|praise", re.I)
def category(r):
    g = str(r["genres"]).lower(); t = f"{r['tags']} {r['title']} {r['song_name']}"
    if "religious" in g or SACRED.search(t): return "hymns and sacred"
    if "folk" in g: return "folk"
    if re.search(r"pop|rock|rbfunk|jazz|soundtrack|country|electronic|hiphop|rap", g): return "popular"
    return "other classical"
def selection():
    d = pd.read_csv(f"{D}/PDMX.csv", low_memory=False)
    d = d[(d.has_lyrics == True) & (d["subset:deduplicated"] == True) & (d["subset:no_license_conflict"] == True) & (d.n_lyrics >= 30)]
    d = d[d.mxl.notna()]
    d = d.assign(cat=d.apply(category, axis=1))
    return d
def work(args):
    cat, path = args
    from mxl_words import song_notes
    from score_words import measure
    R = collections.defaultdict(collections.Counter)
    try: ok = measure(song_notes(path), cat, R)
    except Exception: return None
    return (ok, {"|".join(k): dict(v) for k, v in R.items()})
if __name__ == "__main__":
    d = selection()
    if "--extract" in sys.argv:
        want = set(p.lstrip("./") for p in d.mxl)
        with tarfile.open(f"{D}/mxl.tar.gz") as tf:
            for m in tf:
                if m.name.lstrip("./") in want: tf.extract(m, f"{D}/x", filter="data")
        sys.exit()
    jobs = [(c, os.path.join(D, "x", p.lstrip("./"))) for c, p in zip(d.cat, d.mxl) if os.path.exists(os.path.join(D, "x", p.lstrip("./")))]
    print(len(d), "selected;", len(jobs), "extracted;", collections.Counter(c for c, _ in jobs))
    R = collections.defaultdict(collections.Counter); n = collections.Counter()
    with Pool(2) as pool:
        for res in pool.imap_unordered(work, jobs, chunksize=20):
            if res is None: n["error"] += 1; continue
            ok, r = res; n["used" if ok else "skipped"] += 1
            for k, v in r.items(): R[tuple(k.split("|"))].update(v)
    from score_words import summarise
    out = summarise(R); out["counts"] = dict(n)
    json.dump(out, open(os.path.join(HERE, "pdmx_words_results.json"), "w"), indent=1)
    print(out["counts"])
    for k, v in out.items():
        if k == "counts": continue
        print(k, v.get("songs"), {m: (x["share"], x["n"]) for m, x in v.items() if isinstance(x, dict) and "share" in x})
        print("   vowels", v.get("vowel all"), v.get("vowel held top"))
