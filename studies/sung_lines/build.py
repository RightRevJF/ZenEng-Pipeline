"""Sung lines against WASABI (PREDICTION.md). Numbers only; every output is outside the repository.
  python3 build.py sung      -> /home/claude/lyr_dl/sung/sung.csv and wanted.csv (BiMMuDa features; WASABI ids matched by artist and title)
  python3 build.py wasabi    -> /home/claude/lyr_dl/sung/wasabi.csv (the matched WASABI lyrics' features, streamed once)
  unzip -p main.zip main/Discogs-VI-20240701.jsonl | python3 -I build.py covers -> /home/claude/lyr_dl/sung/covers.csv"""
import sys, os, re, csv, glob, gzip, html, json, zlib, struct
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "covers_lines"))
import linefeat as LF
OUT = "/home/claude/lyr_dl/sung"; os.makedirs(OUT, exist_ok=True)
BIM = "/home/claude/data/bimmuda/BiMMuDa"
def norm(s):
    s = s.lower().replace("&", "and"); s = re.sub(r"\(.*?\)|\[.*?\]", "", s); s = re.sub(r"\s(feat|featuring|ft|with)\.?\s.*", "", s)
    s = re.sub(r"^the ", "", s.strip()); return re.sub(r"[^a-z0-9]", "", s)
def amatch(a, b): return bool(a) and bool(b) and (a[:6] in b or b[:6] in a)
def stanzas(text):
    return [[l.strip() for l in s.split("\n")] for s in re.split(r"\n\s*\n", text.strip())]

if sys.argv[1] == "sung":
    meta = {}
    for r in csv.DictReader(open(f"{BIM}/metadata/bimmuda_per_song_metadata.csv", encoding="utf-8", errors="replace")):
        meta[(r["Year"], r["Position"])] = r
    rows = []
    for f in sorted(glob.glob(f"{BIM}/bimmuda_dataset/*/*/*_lyrics.txt")):
        y, pos = os.path.basename(f).split("_")[:2]; m = meta.get((y, str(int(re.match(r"\d+", pos).group(0)))))      # a few singles are split into parts (02a, 02b): each part read, the longest kept below
        if not m: continue
        ft = LF.features(stanzas(open(f, encoding="utf-8", errors="replace").read()))
        if ft is None: continue
        k_ = f"{y}_{int(re.match(r'\d+', pos).group(0)):02d}"; ft.update(key=k_, artist=norm(m["Artist"]), title=norm(m["Title"]), year=int(y))
        if not rows or rows[-1]["key"] != k_: rows.append(ft)
        elif ft["n_words"] > rows[-1]["n_words"]: rows[-1] = ft
    w = csv.DictWriter(open(f"{OUT}/sung.csv", "w", newline=""), ["key", "artist", "title", "year"] + [k for k in rows[0] if k not in ("key", "artist", "title", "year")]); w.writeheader(); w.writerows(rows)
    byT = {}
    for r in csv.DictReader(gzip.open(os.path.join(HERE, "..", "covers_lines", "data", "wasabi_english_meta.csv.gz"), "rt", newline="")):
        byT.setdefault(norm(r["title"]), []).append((norm(r["artist"]), r["id"], int(r["n_lines"])))
    want = []
    for r in rows:
        c = [x for x in byT.get(r["title"], []) if amatch(r["artist"], x[0])]
        if c: want.append(dict(key=r["key"], id=max(c, key=lambda x: x[2])[1]))
    w = csv.DictWriter(open(f"{OUT}/wanted.csv", "w", newline=""), ["key", "id"]); w.writeheader(); w.writerows(want)
    print("sung songs with features", len(rows), "matched in WASABI", len(want))

elif sys.argv[1] == "wasabi":
    import ijson
    want = {r["id"]: r["key"] for r in csv.DictReader(open(f"{OUT}/wanted.csv"))}
    class Stream:
        def __init__(s):
            s.f = open("/home/claude/lyr_dl/scout/wasabi/song_json.deflate", "rb"); h = s.f.read(30); nl, el = struct.unpack("<HH", h[26:30]); s.f.read(nl + el); s.d = zlib.decompressobj(-15); s.buf = b""
        def read(s, n=-1):
            while (n < 0 or len(s.buf) < n) and not s.d.eof:
                c = s.f.read(1 << 22)
                if not c: break
                s.buf += s.d.decompress(c)
            out, s.buf = (s.buf, b"") if n < 0 else (s.buf[:n], s.buf[n:]); return out
    rows = []
    for o in ijson.items(Stream(), "item"):
        i = (o.get("_id") or {}).get("$oid", "")
        if i not in want or not o.get("lyrics"): continue
        t = html.unescape(o["lyrics"]); st = [[re.sub(r"<.*?>", " ", l).strip() for l in re.split(r"<br\s*/?>", s)] for s in re.split(r"(?:<br\s*/?>\s*){2,}", t)]
        ft = LF.features(st)
        if ft: ft["key"] = want[i]; rows.append(ft)
    w = csv.DictWriter(open(f"{OUT}/wasabi.csv", "w", newline=""), ["key"] + [k for k in rows[0] if k != "key"]); w.writeheader(); w.writerows(rows)
    print("WASABI features", len(rows), "of", len(want))

elif sys.argv[1] == "covers":
    songs = {}
    for r in csv.DictReader(open(f"{OUT}/sung.csv")): songs.setdefault(r["title"], []).append((r["artist"], r["key"]))
    best = {}; n = 0
    for line in sys.stdin:
        n += 1; c = json.loads(line); titles, arts = set(), set()
        for v in c["versions"]:
            for t in v["tracks"][:1]:
                titles.add(norm(t.get("track_title_cleaned") or t["track_title"]))
                for a in t["track_artist_names"]: arts.add(norm(re.sub(r"\s\(\d+\)$", "", a)))
        for t in titles & set(songs):
            for a, k in songs[t]:
                if any(amatch(a, x) for x in arts if x): best[k] = max(best.get(k, 0), len(arts))
    w = csv.writer(open(f"{OUT}/covers.csv", "w", newline="")); w.writerow(["key", "n_artists"])
    for k, v in best.items(): w.writerow([k, v])
    print("cliques", n, "matched", len(best), file=sys.stderr)
