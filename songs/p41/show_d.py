import sys, pickle
fps = sys.argv[1:]
sys.argv = ["x", "1", "design"]; sys.path[:0] = ["/home/claude/p41"]
import melody_p41d as P
D = pickle.load(open("melody_p41d_design.pkl", "rb"))
NM = "C C# D Eb E F F# G G# A Bb B".split(); nm = lambda p: f"{NM[p % 12]}{p // 12 - 1}"
short = [c for c in D["alive"] if c["fp"] in set(D["short"])]
if not fps or fps == ["list"]:
    for k, c in enumerate(short[:12]):
        ns = c["notes"]; iv = [abs(b["p"] - a["p"]) for a, b in zip(ns, ns[1:]) if a["line"] == b["line"]]
        print(k + 1, c["fp"], c["meas"]["composite"], round(c["judge"]["combined"], 2), c["info"]["lift"], "leaps>7", sum(x > 7 for x in iv), "range", nm(min(n["p"] for n in ns)), nm(max(n["p"] for n in ns)))
    sys.exit()
for fp in fps:
    c = next(x for x in D["alive"] if x["fp"] == fp)
    print("=====", fp, c["meas"]["composite"], round(c["judge"]["combined"], 3), c["info"]["lift"], c["meta"]["plans"])
    for ln in dict.fromkeys(n["line"] for n in c["notes"]):
        s, i = ln.split(":"); i = int(i)
        if s in ("Chorus 2", "Verse 2", "Pre 2") : continue
        ns = [n for n in c["notes"] if n["line"] == ln]; U = P.line_start(s, i); sy = P.LINES[s][i]
        out = [f"{'~' if n['slur'] else sy[n['syl']][0].strip(',.;:')}:{nm(n['p'])}" for n in ns]
        print(f"{ln:14s} {P.CHORD[U // 48]:3s}", " ".join(out))
