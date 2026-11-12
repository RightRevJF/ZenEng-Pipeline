"""Prints a build line by line: syllable, pitch, bar.beat, length (the pick, or a fingerprint)."""
import sys, pickle, importlib
sys.argv_, sys.argv = sys.argv, ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p49")
import melody_p45 as P
D = pickle.load(open(sys.argv_[1], "rb")); fp = sys.argv_[2] if len(sys.argv_) > 2 else None
c = D["pick"] if fp is None else next(x for x in D["alive"] if x["fp"] == fp)
NM = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(p): return f"{NM[p % 12]}{p // 12 - 1}"
by = {}
for n in c["notes"]: by.setdefault(n["line"], []).append(n)
for sec in P.SUNG:
    for i, sy in enumerate(P.LINES[sec]):
        ns = by.get(f"{sec}:{i}", []); words = P.M.WORDS_OF[sec][i][1]
        cells = []
        for n in ns:
            b, t = divmod(n["on"], P.BAR); cells.append(f"{sy[n['syl']][0] if not n.get('slur') else '~'}:{nm(n['p'])}@{b + 1}.{t / 12 + 1:g}/{n.get('dur', 0)}")
        print(f"{sec}:{i} {[P.CHORD[b_] for b_ in range(P.line_start(sec,i)//P.BAR, P.line_start(sec,i)//P.BAR+2)]} [{c['meta']['kinds'].get((sec, i), '?')}] {words}\n    " + " ".join(cells))
print("pick", c["fp"], "registers", c["meta"]["registers"]["sections"])
