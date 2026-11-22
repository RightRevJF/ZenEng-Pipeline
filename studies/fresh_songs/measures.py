"""Fresh songs (J6b): the chord measure and the controls on the McGill charts, computed before any cover count is joined (PREDICTION.md).
ch_rep with the judging research's frozen rules: token = the chart's Roman numeral with its quality, plus "7" where the chart flags a seventh;
no-chord marks (None) dropped; a chord repeating the one before merged (bar lines ignored); the first instance of each distinct section
letter, sections of at least 4 merged chords; the share of a section's chord 3-grams already heard earlier in that section
(studies/surprise/surprise_hooktheory.py's repetition, n = 3); averaged over those sections weighted by bar count.
Freshness: not in Hooktheory (normalised artist and title) and not in a Discogs-VI group already matched to a Hooktheory song (checked at the join).
Controls: the year first charted (McGill's chart date), merged chords in the sections read, and, for the sensitivity, weeks on the Hot 100 and
peak rank from the McGill index in ChoCo (raw/billboard-2.0-index.csv).
    python3 studies/fresh_songs/measures.py -> measures.json"""
import json, gzip, re, csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))
def repetition(s, n=3):
    seen = set(); rep = 0; tot = 0
    for i in range(len(s) - n + 1):
        g = tuple(s[i:i + n]); tot += 1
        if g in seen: rep += 1
        seen.add(g)
    return rep / tot if tot else 0.0
D = json.load(open(os.path.join(ROOT, "studies/harmony/billboard_sections.json")))
H = json.load(gzip.open("/home/claude/chrisdonahue/sheetsage-data/hooktheory/Hooktheory.json.gz"))
HT = {(norm(c["hooktheory"]["artist"]), norm(c["hooktheory"]["song"])) for c in H.values()}
IDX = {r["id"]: r for r in csv.DictReader(open("/home/claude/data/choco/smashub-choco-f7dd3ee/partitions/billboard/raw/billboard-2.0-index.csv"))}
out = []
for s in D:
    seen = set(); secs = []
    for sec in s["sections"]:
        if sec["letter"] in seen: continue
        seen.add(sec["letter"]); seq = []
        for b in sec["bars"]:
            for r, sv in zip(b["rn"], b["sev"]):
                if r is None: continue
                t = r + ("7" if sv else "")
                if not seq or seq[-1] != t: seq.append(t)
        if len(seq) >= 4: secs.append((repetition(seq), len(sec["bars"]), len(seq)))
    if not secs: continue
    w = sum(b for _, b, _ in secs)
    ix = IDX.get(str(int(s["id"])), {})
    out.append(dict(id=s["id"], artist=s["artist"], title=s["title"], a=norm(s["artist"]), t=norm(s["title"]), in_hooktheory=(norm(s["artist"]), norm(s["title"])) in HT,
                    year=int(s["date"][:4]), ch_rep=sum(r * b for r, b, _ in secs) / w, merged_chords=sum(n for _, _, n in secs), sections_read=len(secs),
                    weeks=int(ix["weeks_on_chart"]) if ix.get("weeks_on_chart") else None, peak=int(ix["peak_rank"]) if ix.get("peak_rank") else int(s["peak"]) if s.get("peak") else None))
json.dump(out, open(os.path.join(HERE, "measures.json"), "w"), indent=0)
fresh = [r for r in out if not r["in_hooktheory"]]
print(len(D), "charts;", len(out), "with a section read;", len(fresh), "not in Hooktheory;", sum(r["weeks"] is not None for r in fresh), "with weeks")
