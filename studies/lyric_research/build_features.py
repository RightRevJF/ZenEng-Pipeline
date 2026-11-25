"""Compute the frozen measures over the Billboard year-end corpus (task 67).

Reads lyric text from outside the repo and writes numbers only, also outside
the repo (/home/claude/lyr_dl/feat.csv). Run: python3 build_features.py
"""
import csv, re, sys, math, pickle
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/lyric_research")
import measures as M

BB = "/home/claude/lyr_dl/wq/bb.csv"
RS = ["/home/claude/lyr_dl/rs/rs%d.csv" % y for y in (2004, 2010, 2021)]
OUT = "/home/claude/lyr_dl/feat.csv"
TAB = "/home/claude/lyr_dl/stock_table.pkl"   # hashes only, never committed


def norm(s):
    s = s.lower(); s = re.sub(r"\(.*?\)|\[.*?\]", "", s)
    s = re.sub(r"\s(feat|featuring|with|and|&|duet)\b.*", "", s)
    s = re.sub(r"^the ", "", s.strip()); return re.sub(r"[^a-z0-9]", "", s)


def main():
    rs = {}
    for p in RS:
        for r in csv.DictReader(open(p, encoding="utf-8-sig")):
            rs.setdefault(norm(r["Song"]), []).append((norm(r["Artist"]), int(r["Edition"]), int(r["Rank"])))
    rows = [r for r in csv.DictReader(open(BB, encoding="latin-1")) if len(r["Lyrics"].split()) > 50]
    # one row per song (some songs appear in two year-end lists): keep first year
    seen, uniq = set(), []
    for r in rows:
        k = (norm(r["Song"]), norm(r["Artist"]))
        if k in seen:
            continue
        seen.add(k); uniq.append(r)
    table = M.build_stock_table((norm(r["Artist"]), r["Lyrics"]) for r in uniq)
    pickle.dump(table, open(TAB, "wb"))
    cols = ["song_key", "artist_key", "year", "rank", "rs", "rs_best"] + ["n_words"] + M.MEASURES
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for i, r in enumerate(uniq):
            t, a = norm(r["Song"]), norm(r["Artist"])
            best = None
            for ra, ed, rk in rs.get(t, []):
                if ra[:6] in a or a[:6] in ra:
                    best = rk if best is None else min(best, rk)
            ft = M.features(r["Lyrics"], table, a)
            w.writerow([t, a, r["Year"], r["Rank"], int(best is not None), best or ""] +
                       [ft.get("n_words")] + [ft.get(m, "") for m in M.MEASURES])
            if i % 500 == 0:
                print(i, len(uniq), flush=True)
    print("done", len(uniq))


if __name__ == "__main__":
    main()
