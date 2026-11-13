"""Inspect the pick: every line, syllable by syllable: bar.beat, pitch, length; the line's last stress, its range, the breath before the next."""
import pickle, collections
R = pickle.load(open("/home/claude/p56/song_record.pkl", "rb"))
PN = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
by = collections.OrderedDict()
for n in R["lead"]: by.setdefault((n["sec"], n["line"]), []).append(n)
L = list(by.items())
for k, ((sec, i), ns) in enumerate(L):
    nxt = L[k + 1][1][0]["on"] if k + 1 < len(L) else None
    end = ns[-1]["on"] + ns[-1]["dur"]
    ls = [n for n in ns if n["stress"] and n["first"]][-1]
    print(f"{sec}:{i}  bar {ns[0]['on'] // 48 + 1}  range {nm(min(n['midi'] for n in ns))}-{nm(max(n['midi'] for n in ns))}  last stress '{ls['text']}' on beat {ls['on'] % 48 / 12 + 1:.2f}"
          + (f"  breath {(nxt - end) / 12:.2f} beats" if nxt else ""))
    print("    " + "  ".join(f"{n['text']}{'-' if n['hyph'] else ''}:{n['on'] // 48 + 1}.{n['on'] % 48 / 12 + 1:.2f}/{nm(n['midi'])}/{n['dur']}" + ("*F" if n.get("falsetto") else "") for n in ns))
print("song range", nm(min(n["midi"] for n in R["lead"])), nm(max(n["midi"] for n in R["lead"])))
