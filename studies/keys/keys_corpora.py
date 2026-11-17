"""Key choice in five collections. McGill Billboard (salami_chords.txt via ChoCo; 739 distinct songs 1958-91): tonic from the header
(the first tonic; songs that change key counted once by their first), mode from whether the tonic chord is more often minor than major,
the song's lead instrument as the most often marked of guitar, piano, synthesizer, organ, saxophone or horns, strings. BiMMuDa (381
top-five singles 1950-2022): tonic, mode and broad genre from its per-song metadata. PDMX (English songs with words, by category) and
OpenEWLD standards: the first lyric part's key signature, with mode from the file or, when absent, from the melody's last note (minor
when it is the relative minor's tonic). Writes keys_results.json and prints the tables."""
import os, re, sys, csv, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "words"))
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(n):
    p = PC[n[0]]
    for a in n[1:]: p += 1 if a in "#♯" else -1 if a in "b♭" else 0
    return p % 12
NAME = {0: "C", 1: "D♭", 2: "D", 3: "E♭", 4: "E", 5: "F", 6: "F♯", 7: "G", 8: "A♭", 9: "A", 10: "B♭", 11: "B"}
MNAME = {0: "Cm", 1: "C♯m", 2: "Dm", 3: "E♭m", 4: "Em", 5: "Fm", 6: "F♯m", 7: "Gm", 8: "G♯m", 9: "Am", 10: "B♭m", 11: "Bm"}
OPEN_MAJ = {4, 9, 2, 7, 0}       # E A D G C: open-chord guitar keys
OPEN_MIN = {4, 9, 2}             # Em Am Dm
FLAT_MAJ = {5, 10, 3, 8, 1}      # F Bb Eb Ab Db
def label(t, minor): return MNAME[t] if minor else NAME[t]
def summary(rows):
    n = len(rows) or 1
    c = collections.Counter(label(t, m) for t, m in rows)
    maj = [t for t, m in rows if not m]; mi = [t for t, m in rows if m]
    return dict(songs=len(rows), minor=round(100 * len(mi) / n), top=c.most_common(8),
                open_guitar=round(100 * (sum(t in OPEN_MAJ for t in maj) + sum(t in OPEN_MIN for t in mi)) / n),
                flat_major=round(100 * sum(t in FLAT_MAJ for t in maj) / max(len(maj), 1)),
                sharp_major_EAB=round(100 * sum(t in (4, 9, 11) for t in maj) / max(len(maj), 1)))
OUT = {}
# --- McGill
SRC = "/home/claude/data/choco/smashub-choco-f7dd3ee/partitions/billboard/raw"
year = {r["id"].zfill(4): int(r["chart_date"][:4]) for r in csv.DictReader(open(f"{SRC}/billboard-2.0-index.csv")) if r["title"]}
INS = ["guitar", "piano", "synthesizer", "organ", "saxophone", "horns", "trumpet", "strings", "electric piano"]
rows = collections.defaultdict(list); seen = set()
for sid in sorted(os.listdir(f"{SRC}/original")):
    if sid not in year: continue
    T = open(f"{SRC}/original/{sid}/salami_chords.txt").read()
    t = re.search(r"# title: (.*)", T); a = re.search(r"# artist: (.*)", T); k = re.search(r"# tonic: (\S+)", T)
    key = ((t.group(1) if t else "").lower(), (a.group(1) if a else "").lower())
    if key in seen or not k: continue
    seen.add(key)
    try: ton = pc(k.group(1))
    except Exception: continue
    maj = len(re.findall(rf"\b{re.escape(k.group(1))}:(maj|7|9|maj7|6|sus)", T)); mi = len(re.findall(rf"\b{re.escape(k.group(1))}:min", T))
    minor = mi > maj
    insc = collections.Counter()
    for i in INS: insc[i] = len(re.findall(r"\(" + i, T, re.I))
    lead = insc.most_common(1)[0][0] if insc and insc.most_common(1)[0][1] > 0 else "none marked"
    if lead in ("trumpet", "horns", "saxophone"): lead = "horns or sax"
    if lead == "electric piano": lead = "piano"
    y = year[sid]; per = "1958-69" if y < 1970 else "1970-79" if y < 1980 else "1980-91"
    for g in ("all", per, "lead: " + lead): rows[g].append((ton, minor))
OUT["McGill Billboard"] = {g: summary(r) for g, r in rows.items()}
# --- BiMMuDa
rows = collections.defaultdict(list)
for r in csv.DictReader(open("/home/claude/data/bimmuda/BiMMuDa/metadata/bimmuda_per_song_metadata.csv")):
    try: ton = pc(r["Tonic 1"].strip())
    except Exception: continue
    minor = r["Mode 1"].strip().lower().startswith("min"); y = int(r["Year"]); g = r["Genre (Broad 1)"].strip()
    per = "1950-69" if y < 1970 else "1970-89" if y < 1990 else "1990-2009" if y < 2010 else "2010-22"
    for k in ("all", per, "genre: " + g): rows[k].append((ton, minor))
OUT["BiMMuDa"] = {g: summary(r) for g, r in rows.items() if len(r) >= 15}
# --- MusicXML
from mxl_words import load_xml, strip_ns, STEP
def mxl_key(path):
    root = strip_ns(load_xml(path))
    for part in root.findall("part"):
        if not part.findall(".//lyric"): continue
        k = part.find(".//attributes/key")
        if k is None or k.find("fifths") is None: return None
        f = int(k.find("fifths").text); m = k.find("mode"); mode = m.text.lower() if m is not None and m.text else None
        last = None
        for n in part.iter("note"):
            p = n.find("pitch")
            if p is not None and n.find("chord") is None: last = (STEP[p.find("step").text] + int(float(p.find("alter").text if p.find("alter") is not None else 0))) % 12
        maj = (7 * f) % 12; rel = (maj + 9) % 12
        minor = mode == "minor" if mode in ("major", "minor") else (last == rel)
        return (rel if minor else maj, minor)
    return None
def work(a):
    try: return a[1], mxl_key(a[0])
    except Exception: return a[1], None
if __name__ == "__main__":
    from pdmx_words import selection
    from multiprocessing import Pool
    D = "/home/claude/data/pdmx"; d = selection()
    jobs = [(os.path.join(D, "x", p.lstrip("./")), c) for c, p in zip(d.cat, d.mxl) if os.path.exists(os.path.join(D, "x", p.lstrip("./")))]
    jobs += [(f, "standards (OpenEWLD)") for f in glob.glob("/home/claude/data/openewld/OpenEWLD/dataset/*/*/*.mxl")]
    rows = collections.defaultdict(list)
    with Pool(2) as pool:
        for cat, k in pool.imap_unordered(work, jobs, chunksize=50):
            if k: rows[cat].append(k)
    OUT["MusicXML"] = {g: summary(r) for g, r in rows.items()}
    json.dump(OUT, open(os.path.join(HERE, "keys_results.json"), "w"), indent=1, ensure_ascii=False)
    for src, G in OUT.items():
        for g, s in G.items(): print(src, "|", g, "|", s["songs"], "| minor", s["minor"], "| open", s["open_guitar"], "| flat maj", s["flat_major"], "| E A B maj", s["sharp_major_EAB"], "|", s["top"][:6])
