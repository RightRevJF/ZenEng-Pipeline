"""English hymns (Open Hymnal, 301, four parts, public domain) have no harmonic analyses, so they are measured from the notes:
the share of beats whose sounding notes (all four parts, at the beat's onset) leave plain major or minor of the hymn's key
(Ionian; Aeolian plus the leading tone). This counts passing chromatic notes that sound on a beat and every modulation,
so it is calibrated by running the same measure on the Bach chorales (music21's corpus), whose human analyses give
chrom_global (chromatic_styles.json). Writes chromatic_hymn_beats.json."""
import re, sys, glob, json
import numpy as np
sys.path.insert(0, "/home/claude/zeneng-pipeline/tables/metre_atlas")
import hymn_parse as HP
IONIAN = {0, 2, 4, 5, 7, 9, 11}; AEOLIAN = {0, 2, 3, 5, 7, 8, 10}
PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def home(t, maj): return {(t + p) % 12 for p in (IONIAN if maj else AEOLIAN | {11})}
def beat_share(voices, t, maj, beat):
    H = home(t, maj); notes = [n for v in voices for n in v]
    if not notes: return None
    end = max(n[0] + n[1] for n in notes); tot = chrom = 0
    for b in range(0, int(end), beat):
        P = {n[2] % 12 for n in notes if n[0] <= b < n[0] + n[1]}
        if not P: continue
        tot += 1; chrom += not P <= H
    return chrom / tot if tot else None
def hymn_key(path):
    txt = open(path, encoding="utf-8", errors="ignore").read(); m = re.search(r"^K:\s*([A-G])([#b]?)\s*(m(?:in)?)?", txt, re.M)
    if not m: return None
    return (PCN[m.group(1)] + {"#": 1, "b": -1, "": 0}[m.group(2)]) % 12, not m.group(3)
def hymns():
    out = []
    for p in HP.all_hymns():
        try: h = HP.parse(p); k = hymn_key(p)
        except Exception: continue
        if not k or len(h["voices"]) < 3: continue
        V = [[(n["on"], n["dur"], n["p"]) for n in v if n.get("p") is not None] for v in h["voices"].values()]
        s = beat_share(V, k[0], k[1], 12)          # quarter-note beats on the twelfths grid
        if s is not None: out.append(dict(path=p, share=s, major=k[1]))
    return out
def chorales():
    from music21 import corpus
    out = []
    for i, p in enumerate(corpus.getComposer("bach")):
        if "riemenschneider" in str(p).lower() or not str(p).endswith((".mxl", ".xml", ".krn")): continue
        try:
            s = corpus.parse(p); k = s.analyze("key")
            V = [[(float(n.offset) * 12, float(n.quarterLength) * 12, n.pitch.midi) for n in part.flatten().notes if not n.isChord] for part in s.parts]
            if len(V) < 4: continue
            sh = beat_share(V, k.tonic.pitchClass, k.mode == "major", 12)
            if sh is not None: out.append(dict(path=str(p), share=sh))
        except Exception: continue
    return out
if __name__ == "__main__":
    H = hymns(); print("hymns", len(H), "median %.3f p75 %.3f p90 %.3f" % tuple(np.percentile([h["share"] for h in H], [50, 75, 90])), flush=True)
    C = chorales(); print("chorales", len(C), "median %.3f p75 %.3f p90 %.3f" % tuple(np.percentile([c["share"] for c in C], [50, 75, 90])))
    json.dump(dict(hymns=H, chorales=C), open("/home/claude/shape/chromatic_hymn_beats.json", "w"))
