"""Reads WASABI's song.json (outside the repository) and writes numbers only: one row a song of every artist with a Rolling Stone 500 song.
Usage: python3 build.py /path/json.zip /path/rs_dir out.csv"""
import sys, os, re, csv, html, zipfile, ijson, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linefeat as LF
def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower(); s = re.sub(r"\(.*?\)|\[.*?\]", " ", s); s = s.replace("&", " and ")
    s = re.sub(r"^the\s+", "", s.strip()); return re.sub(r"[^a-z0-9]+", "", s)
zp, rsd, out = sys.argv[1:4]; RS = {}
for y in (2004, 2010, 2021):
    for r in csv.DictReader(open(f"{rsd}/rs{y}.csv", encoding="utf-8-sig")): RS.setdefault(norm(r["Artist"]), set()).add(norm(r["Song"]))
best = {}; n = 0; COLS = None
for o in ijson.items(zipfile.ZipFile(zp).open("song.json"), "item"):
    n += 1; a = norm(o.get("name") or "")
    if a not in RS or (o.get("language_detect") or "") != "english" or not o.get("lyrics"): continue
    t = html.unescape(o["lyrics"]); st = [[re.sub(r"<.*?>", " ", l).strip() for l in re.split(r"<br\s*/?>", s)] for s in re.split(r"(?:<br\s*/?>\s*){2,}", t)]
    f = LF.features(st)
    if f is None: continue
    tk = norm(o.get("title") or ""); m = re.match(r"(\d{4})", (o.get("publicationDate") or "") or (o.get("publicationDateAlbum") or "")); f.update(artist=a, title=tk, rs=int(tk in RS[a]), year=m.group(1) if m else "")
    if (a, tk) not in best or best[(a, tk)]["n_words"] < f["n_words"]: best[(a, tk)] = f
rows = list(best.values()); cols = ["artist", "title", "rs", "year"] + [k for k in rows[0] if k not in ("artist", "title", "rs", "year")]
w = csv.DictWriter(open(out, "w", newline=""), cols); w.writeheader(); w.writerows(rows); print(n, "songs read;", len(rows), "rows;", sum(r["rs"] for r in rows), "listed; RS songs", sum(len(v) for v in RS.values()))
