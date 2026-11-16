"""Harmony study, part 1: the McGill Billboard annotations (salami_chords.txt, 890 files; ChoCo v1.0.0's raw copy, Zenodo 7706751)
parsed into section instances with their chords bar by bar, as Roman numerals on the current tonic. Writes billboard_sections.json.
Duplicate titles (the same song sampled twice) are kept once. Mode: a song (or a tonic span) is minor when its tonic chord is minor
more often than major. Words and music for the engine: Jason Bryant's ZenEng; this file reads only published annotations."""
import os, re, json, collections, csv
SRC = "/home/claude/data/choco/smashub-choco-f7dd3ee/partitions/billboard/raw"
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(n):
    p = PC[n[0]]
    for a in n[1:]: p += 1 if a == "#" else -1 if a == "b" else 0
    return p % 12
def qual(q):
    q = q.split("/")[0]; q = re.sub(r"\(.*?\)", "", q)
    if q.startswith("min") or q == "min": return "m"
    if q.startswith("hdim") or q.startswith("dim"): return "o"
    if q.startswith("aug"): return "+"
    if q.startswith("sus"): return "s"
    if q in ("5", "1"): return "5"
    return "M"                                        # maj, 7, 9, 11, 13, maj7, 6 ...
DEG = {0: "I", 1: "bII", 2: "II", 3: "bIII", 4: "III", 5: "IV", 6: "#IV", 7: "V", 8: "bVI", 9: "VI", 10: "bVII", 11: "VII"}
def rn(ch, ton):
    if ch in ("N", "X", "&pause", "*"): return None
    root, _, q = ch.partition(":")
    if root not in [k for k in (r + a for r in PC for a in ("", "#", "b", "bb", "##"))]: return None
    d = (pc(root) - ton) % 12; k = qual(q or "maj"); s = DEG[d]
    return s.lower() if k == "m" else s + ("o" if k == "o" else "+" if k == "+" else "sus" if k == "s" else "5" if k == "5" else "")
def seventh(ch): return bool(re.search(r":(7|9|11|13|min7|maj7|hdim7|dim7|min9|maj9)", ch))
index = {}
with open(f"{SRC}/billboard-2.0-index.csv") as f:
    for r in csv.DictReader(f): index[r["id"]] = r
songs = []; seen = set()
for sid in sorted(os.listdir(f"{SRC}/original")):
    L = open(f"{SRC}/original/{sid}/salami_chords.txt").read().split("\n")
    meta = {}; ton = None; met = "4/4"; secs = []; cur = None
    for line in L:
        if line.startswith("#"):
            k, _, v = line[1:].partition(":"); k = k.strip(); v = v.strip()
            if k == "tonic": ton = pc(v)
            elif k == "metre": met = v
            else: meta[k] = v
            continue
        if "\t" not in line: continue
        t, body = line.split("\t", 1)
        m = re.match(r"^([A-Z]'*), ([^,|]+),\s*(.*)$", body)
        if m: cur = dict(letter=m.group(1), label=m.group(2).strip(), bars=[], tonic=ton, metre=met, start=float(t)); secs.append(cur); body = m.group(3)
        if cur is None or "|" not in body: continue
        rep = re.search(r"\bx(\d+)\b", body); n = int(rep.group(1)) if rep else 1
        barstr = body[body.index("|"): body.rindex("|") + 1]
        bars = [b.strip() for b in barstr.split("|")[1:-1]]
        out = []
        for b in bars:
            toks = b.split()
            if not toks: continue
            ch, prev = [], None
            for tk in toks:
                if tk == ".": ch.append(prev); continue
                prev = tk; ch.append(tk)
            out.append(dict(ch=ch, tonic=ton, metre=met))
        cur["bars"] += out * n
    key = (meta.get("title", "").lower(), meta.get("artist", "").lower())
    if key in seen or not secs: continue
    seen.add(key)
    ix = index.get(str(int(sid)), {})
    S = []
    for s in secs:
        bars = []
        for b in s["bars"]:
            r = [rn(c, b["tonic"]) if c else None for c in b["ch"]]
            bars.append(dict(rn=r, sev=[seventh(c) if c else False for c in b["ch"]], metre=b["metre"]))
        if bars: S.append(dict(letter=s["letter"], label=s["label"], bars=bars, start=s["start"]))
    songs.append(dict(id=sid, title=meta.get("title"), artist=meta.get("artist"), date=ix.get("chart_date"), peak=ix.get("peak_rank"), sections=S))
# mode by song: the tonic chord minor more often than major
for so in songs:
    c = collections.Counter(x for s in so["sections"] for b in s["bars"] for x in b["rn"] if x in ("I", "i"))
    so["mode"] = "minor" if c["i"] > c["I"] else "major"
json.dump(songs, open("billboard_sections.json", "w"))
lab = collections.Counter(s["label"] for so in songs for s in so["sections"])
print(len(songs), "songs;", sum(len(so["sections"]) for so in songs), "sections;", collections.Counter(so["mode"] for so in songs), lab.most_common(14))
