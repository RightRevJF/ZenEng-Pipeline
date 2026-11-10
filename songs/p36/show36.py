"""Print the pick line by line: syllable, onset (bar:beat.sixteenth, bars counted from 1), length in sixteenths, pitch, chord."""
import sys, pickle
K = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 0
sys.argv = ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p36")
import melody_p36 as M
R = pickle.load(open("/home/claude/p36/melody_main.pkl", "rb"))
k = K
c = R["alive"][k]
NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
def nm(p): return f"{NAMES[p % 12]}{p // 12 - 1}"
def pos(t): b, r = divmod(t, M.BAR); return f"{b + 1}:{r // 12 + 1}.{(r % 12) // 3 + 1}"
for ln in dict.fromkeys(n["line"] for n in c["notes"]):
    sec, i = ln.split(":"); i = int(i); sy = M.LINES[sec][i]
    ns = [n for n in c["notes"] if n["line"] == ln]
    print(f"{ln:15s}", " ".join(f"{('-' if n['slur'] else (sy[n['syl']][0][:5].upper() if sy[n['syl']][1] else sy[n['syl']][0][:5]))}/{nm(n['p'])}/{pos(n['on'])}/{n['dur'] // 3}{'*' if n['on'] % 48 == 0 else ''}" for n in ns))
print(c["meta"]["plans"], c["meta"]["shifts"])
