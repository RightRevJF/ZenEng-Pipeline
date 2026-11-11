import pickle, sys
D = pickle.load(open(sys.argv[1], "rb")); short = set(D["short"])
NM = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
nm = lambda x: NM[x % 12] + str(x // 12 - 1)
secs = sys.argv[3].split(",") if len(sys.argv) > 3 else ["Chorus 1"]
for c in [c for c in D["alive"] if c["fp"] in short][:int(sys.argv[2])]:
    print("==", c["fp"], "comp", round(c["meas"]["composite"], 3), "judge", round(c["judge"]["combined"], 2), c["info"]["lift"], c["meta"]["plans"]["tail"], c["meta"]["plans"]["line5"])
    lines = {}
    for n in c["notes"]: lines.setdefault(n["line"], []).append(n)
    for ln, ns in lines.items():
        if ln.split(":")[0] in secs:
            print(f"  {ln:14s}", " ".join(f"{nm(n['p'])}{'~' if n['slur'] else ''}{'@' + str(n['on'] % 48 // 12 + 1) if n['on'] % 12 == 0 else ''}:{n['dur']}" for n in ns))
