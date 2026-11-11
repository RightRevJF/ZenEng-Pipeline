import sys, pickle
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p41"]
import melody_p41 as P
fn = sys.argv_[1] if hasattr(sys, "argv_") else "melody_p41_main.pkl"
D = pickle.load(open(fn, "rb")); c = D["pick"]
NM = "C C# D Eb E F F# G G# A Bb B".split()
def nm(p): return f"{NM[p % 12]}{p // 12 - 1}"
print(c["fp"], c["meas"]["composite"], round(c["judge"]["combined"], 3), c["info"]["soft"], c["info"]["lift"], c["meta"]["plans"])
for ln in dict.fromkeys(n["line"] for n in c["notes"]):
    s, i = ln.split(":"); i = int(i); ns = [n for n in c["notes"] if n["line"] == ln]; U = P.line_start(s, i)
    sy = P.LINES[s][i]
    out = []
    for n in ns:
        t = n["on"] - U; b, r = divmod(t, 48)
        out.append(f"{'~' if n['slur'] else sy[n['syl']][0].strip(',.;:')}{'*' if n['stress'] else ''}:{nm(n['p'])}@{b + 1}.{r / 12 + 1:g}/{n['dur'] / 12:g}")
    print(f"{ln:14s} {c['meta']['kinds'].get((s, i), ''):10s} {P.CHORD[U // 48]:3s}", " ".join(out))
