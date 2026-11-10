import pickle, sys
import melody_p33 as M
R = pickle.load(open("melody_result.pkl", "rb"))
c = R["alive"][int(sys.argv[1]) if len(sys.argv) > 1 else 0]
NM = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
def nm(p): return NM[p % 12] + str(p // 12 - 1)
print(c["fp"], c["meas"])
for s in M.SINGS:
    print("==", s, c["plans"].get(s))
    for ln in M.SECS[s]:
        ns = [n for n in c[s] if n[4] == ln["idx"]]
        bar0 = M.BARS.index(M.bar_of(ln["at"])) + 1
        print(f"  b{bar0:2d} {ln['line'][:44]:44s} " + " ".join(f"{n[3][0][:5]}{'*' if n[3][2] else ''}:{nm(n[2])}@{n[0]-ln['at']}/{n[1]}" for n in ns))
