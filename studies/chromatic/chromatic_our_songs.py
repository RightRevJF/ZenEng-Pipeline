"""Chromatic chords in our songs (p21 to p63): every chord symbol written in each song's scripts (quoted chord lists), read
against the song's key (KEY in intake.py where it names one, otherwise the major or minor key that fits the most chord
occurrences). Lists each song's chords outside plain major/minor, by kind: mixture (from the parallel mode), a major chord or
dominant seventh on a degree that could be an applied dominant, or other. An inventory, not a count of bars."""
import re, glob, os, json, collections
SONGS = "/home/claude/zeneng-pipeline/songs"
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
IONIAN = {0, 2, 4, 5, 7, 9, 11}; AEOLIAN = {0, 2, 3, 5, 7, 8, 10}
LIST = re.compile(r"\[\s*['\"][A-G][#b♯♭]?[^'\"\]]{0,9}['\"](?:\s*,\s*['\"][A-G][#b♯♭]?[^'\"\]]{0,9}['\"]){2,}\s*\]?")
SYM = re.compile(r"['\"]([A-G][#b♯♭]?[^'\"]{0,9})['\"]")
def parse(sym):
    s = sym.replace("♯", "#").replace("♭", "b").split("/")[0].strip()
    m = re.fullmatch(r"([A-G])([#b]?)(maj7|maj9|M7|m7b5|m7|m9|m6|m|dim7|dim|aug|\+|sus4|sus2|sus|7sus4|add9|add2|6|7|9|11|13|5)?(\(.*\))?", s)
    if not m: return None
    root = (PC[m.group(1)] + {"#": 1, "b": -1, "": 0}[m.group(2)]) % 12; q = m.group(3) or ""
    if q in ("m", "m7", "m9", "m6"): iv = [3, 4] + ([3] if q in ("m7", "m9") else [])
    elif q in ("dim", "dim7", "m7b5"): iv = [3, 3] + ([3] if q == "dim7" else [4] if q == "m7b5" else [])
    elif q in ("aug", "+"): iv = [4, 4]
    elif q.startswith("sus") or q == "7sus4": iv = [5, 2] if q != "sus2" else [2, 5]
    elif q == "5": iv = [7]
    elif q in ("7", "9", "11", "13"): iv = [4, 3, 3]
    elif q in ("maj7", "maj9", "M7"): iv = [4, 3, 4]
    else: iv = [4, 3]
    P = {root}; a = root
    for x in iv: a += x; P.add(a % 12)
    return root, frozenset(P), tuple(iv), s
def home(tonic, major):
    base = IONIAN if major else AEOLIAN | {11}
    return {(tonic + p) % 12 for p in base}
def key_from_intake(d):
    t = open(f"{SONGS}/{d}/intake.py", encoding="utf-8", errors="ignore").read() if os.path.exists(f"{SONGS}/{d}/intake.py") else ""
    m = re.search(r"^KEY\s*=\s*['\"]([A-G][#b♯♭]?)\s*(major|minor)", t, re.M)
    if not m: return None
    r = m.group(1).replace("♯", "#").replace("♭", "b"); return ((PC[r[0]] + (1 if "#" in r else -1 if "b" in r[1:] else 0)) % 12, m.group(2) == "major")
NAMES = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
def degree(r, tonic, major):
    rel = (r - tonic) % 12
    return {0: "I", 1: "bII", 2: "II", 3: "bIII", 4: "III", 5: "IV", 6: "#IV", 7: "V", 8: "bVI", 9: "VI", 10: "bVII", 11: "VII"}[rel]
out = []
for d in sorted(os.listdir(SONGS)):
    if not re.fullmatch(r"p\d+", d): continue
    syms = collections.Counter()
    for f in glob.glob(f"{SONGS}/{d}/*.py"):
        if re.search(r"(_v\d+|gen_v|melody_v|readings)", os.path.basename(f)): continue
        txt = open(f, encoding="utf-8", errors="ignore").read()
        for L in LIST.findall(txt):
            ss = SYM.findall(L)
            if len(ss) >= 12 and all(len(x) <= 2 for x in ss): continue       # a pitch-name table, not chords
            for s in ss:
                p = parse(s)
                if p: syms[p] += 1
    if not syms: continue
    k = key_from_intake(d) or {"p63": (2, True), "p62": (2, True)}.get(d)
    if k is None:
        best = max(((t, mj) for t in range(12) for mj in (True, False)),
                   key=lambda km: (sum(n for p, n in syms.items() if p[1] <= home(*km)), sum(n for p, n in syms.items() if p[0] == km[0] and (4 in [x for x in p[2][:1]]) == km[1])))
        k, src = best, "inferred"
    else: src = "intake" if key_from_intake(d) else "known"
    H = home(*k); par = home(k[0], not k[1]) - ({(k[0] + 11) % 12} if k[1] else set())
    chrom = {}
    for p, n in syms.items():
        if p[1] <= H: continue
        deg = degree(p[0], *k)
        kind = "applied-dominant shape" if p[2] in ((4, 3), (4, 3, 3)) and deg in ("II", "III", "VI", "VII", "I") and not p[1] <= par else ("mixture" if p[1] <= par else "other")
        chrom.setdefault(p[3], (deg, kind))
    total = sum(syms.values()); nch = sum(n for p, n in syms.items() if not p[1] <= H)
    out.append(dict(folder=d, key=NAMES[k[0]] + (" major" if k[1] else " minor"), key_source=src, distinct=len(syms), chord_mentions=total,
                    chromatic_mentions=nch, chromatic_share=nch / total, chromatic=chrom))
json.dump(out, open("/home/claude/shape/chromatic_our_songs.json", "w"), indent=1)
for o in out:
    print("%-4s %-9s %-8s %2d chords, %4.0f%% chromatic  %s" % (o["folder"], o["key"], o["key_source"], o["distinct"], 100 * o["chromatic_share"],
          ", ".join(f"{s} ({v[0]}, {v[1]})" for s, v in o["chromatic"].items())))
