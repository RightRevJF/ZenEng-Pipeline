"""Checks the voice against what the guitar and cello are sounding: a sung note a semitone (or a minor ninth) from a sounding note, on
notes of a beat or longer or on a beat, listed with the bar and the chord."""
import pickle
REC = pickle.load(open("/home/claude/p49/song_record.pkl", "rb"))
ring = [(e["on"], z, p, "gtr") for e in REC["gtr"] for p, z in zip(e["p"], e["ring"])]
ring += [(e["on"], e["on"] + e["dur"], e["p"][0], "vc") for e in REC["cello"]]
out = []
for n in REC["lead"]:
    a, z = n["on"], n["on"] + n["dur"]
    if n["dur"] < 12 and n["on"] % 12: continue
    hits = sorted({(p, w) for on, off, p, w in ring if on < z and off > a and (n["midi"] - p) % 12 in (1, 11)})
    if hits:
        b = REC["bars"][a // 48]; out.append((a // 48 + 1, b["sec"], b["chord"], n["text"], n["midi"], n["dur"], hits))
NM = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
for r in out: print(f"bar {r[0]:2d} {r[1]:12s} {r[2]:5s} '{r[3]}' {NM[r[4] % 12]}{r[4] // 12 - 1} dur {r[5]}  against {[(NM[p % 12] + str(p // 12 - 1), w) for p, w in r[6]]}")
print(len(out), "of", len(REC["lead"]))
