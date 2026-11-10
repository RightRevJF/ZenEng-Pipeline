"""print a build line by line: syllable, pitch, onset (bar.beat), length; the chord under each note."""
import sys, pickle
sys.argv = [sys.argv[0]] + sys.argv[1:] + ["main"] * (2 - len(sys.argv[1:]))
FP, MODE = sys.argv[1], sys.argv[2]
sys.argv = ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p38")
import melody_p38 as P
d = pickle.load(open(f"/home/claude/p38/melody_{MODE}.pkl", "rb"))
c = next(c for c in d["alive"] if c["fp"].startswith(FP))
NAMES = "C C# D D# E F F# G G# A A# B".split()
def nm(p): return f"{NAMES[p % 12]}{p // 12 - 1}"
cur = None
for n in c["notes"]:
    if n["line"] != cur:
        cur = n["line"]; s, i = cur.split(":"); sy = P.LINES[s][int(i)]
        print(f"\n{cur}  [{c['meta']['kinds'].get((s, int(i)))}]  {' '.join(w for w, _ in sy)}")
    s, i = n["line"].split(":"); w = P.LINES[s][int(i)][n["syl"]][0]
    bar = n["on"] // 48 + 1; beat = (n["on"] % 48) / 12 + 1
    print(f"   {('~' if n['slur'] else w):12s} {'*' if n['stress'] else ' '} {nm(n['p']):4s} bar {bar:3d} beat {beat:4.2f} len {n['dur'] / 12:4.2f}  {P.M.chord_at(n['on'])}")
