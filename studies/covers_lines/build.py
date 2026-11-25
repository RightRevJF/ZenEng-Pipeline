"""Design B, step 2: line features for the joined songs, numbers only.
Streams WASABI's song.json member (the data scout's raw-deflate copy, outside the repo), reads only the ids in covers_join.csv,
and splits stanzas and lines as the maintainer's build.py does. Writes /home/claude/lyr_dl/covers_feat.csv."""
import sys, os, re, csv, html, zlib, struct, ijson
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linefeat as LF
SRC = "/home/claude/lyr_dl/scout/wasabi/song_json.deflate"; JOIN = "/home/claude/lyr_dl/covers_join.csv"; OUT = "/home/claude/lyr_dl/covers_feat.csv"
want = {r["id"] for r in csv.DictReader(open(JOIN))}
class Stream:
    def __init__(s):
        s.f = open(SRC, "rb"); h = s.f.read(30); nl, el = struct.unpack("<HH", h[26:30]); s.f.read(nl + el); s.d = zlib.decompressobj(-15); s.buf = b""
    def read(s, n=-1):
        while (n < 0 or len(s.buf) < n) and not s.d.eof:
            c = s.f.read(1 << 22)
            if not c: break
            s.buf += s.d.decompress(c)
        out, s.buf = (s.buf, b"") if n < 0 else (s.buf[:n], s.buf[n:]); return out
rows = []; n = 0
for o in ijson.items(Stream(), "item"):
    n += 1; i = (o.get("_id") or {}).get("$oid", "")
    if i not in want or not o.get("lyrics"): continue
    t = html.unescape(o["lyrics"]); st = [[re.sub(r"<.*?>", " ", l).strip() for l in re.split(r"<br\s*/?>", s)] for s in re.split(r"(?:<br\s*/?>\s*){2,}", t)]
    f = LF.features(st)
    if f is None: continue
    f["id"] = i; rows.append(f)
cols = ["id"] + [k for k in rows[0] if k != "id"]
w = csv.DictWriter(open(OUT, "w", newline=""), cols); w.writeheader(); w.writerows(rows)
print(n, "songs read;", len(rows), "with features of", len(want), "joined")
