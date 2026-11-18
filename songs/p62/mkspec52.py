"""Song 52 (The Room Next Door, 6/8) as a spec for lib/luthier/metre_engine.py (Luthier v12, fix 790). Everything here is the song, nothing is the metre's.
    python3 songs/p62/mkspec52.py   ->  songs/p62/spec52.json"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); src = open(f"{H}/gen68.py").read()
ns = {}; exec(src[src.index("SCALE ="):src.index("FORM =")], ns); exec(src[src.index("DOOR ="):src.index("DSPEC =")], ns)
SY = json.load(open(f"{H}/syllables.json")); kind = lambda s: "Verse" if s.startswith("Verse") else "Bridge" if s == "Bridge" else "Chorus"
order = ("Intro", "Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Interlude", "Verse 3", "Bridge", "Verse 4", "Last Chorus", "Outro")
how = {}
for i in range(4):
    how[f"Verse 1:{i}"] = ["plan", "verse"]
    for v in ("Verse 2", "Verse 3", "Verse 4"): how[f"{v}:{i}"] = ["again", "Verse 1", i]
    how[f"Chorus 2:{i}"] = ["copy", "Chorus 1", i]
for s in ("Chorus 1", "Chorus 2", "Last Chorus"): how[f"{s}:4"] = ["design", ns["DOOR"]]
how["Last Chorus:5"] = ["design", ns["HOME"]]; how["Bridge:3"] = ["design", ns["THERE"]]; how["Bridge:2"] = ["plan", "bridge"]
how["Last Chorus:0"] = ["copy", "Chorus 1", 0]; how["Last Chorus:1"] = ["copy", "Chorus 1", 1]; how["Last Chorus:3"] = ["again", "Chorus 1", 3]
spec = dict(title="The Room Next Door (song 52)", metre="6/8", seed=20261113 + 452, scale=sorted(ns["SCALE"]), chords={k: sorted(v) for k, v in ns["CHT"].items()},
            form=[[s, ns["SECCH"][s]] for s in order], sung=[[s, kind(s), SY[s]] for s in SY], how=how,
            registers={"Verse": [64, 57, 69], "Chorus": [68, 62, 73], "Bridge": [62, 57, 66], "Bridge:3": [66, 59, 71]},
            plans={"verse": ["ABCD", "ABAC", "ABCB"], "bridge": ["ABCX", "ABAX"]},
            line_rules={"Verse 1:3": {"end_off": 2}, "Last Chorus:2": {"avoid": [6, 1, 11]}},
            gates=[{"type": "top only in", "name": "D5 only on 'door'", "pitch": 74, "lines": [["Chorus 1", 4], ["Chorus 2", 4], ["Last Chorus", 4]]},
                   {"type": "median above", "name": "the chorus above the verse", "a": "Chorus 1", "a_lines": [0, 1, 2, 3], "b": "Verse 1", "by": 2},
                   {"type": "cap", "name": "the bridge's first lines low", "section": "Bridge", "lines": [0, 1, 2], "pitch": 66}])
json.dump(spec, open(f"{H}/spec52.json", "w"), indent=1); print("wrote spec52.json:", sum(len(l) for _, _, ls in spec["sung"] for l in ls), "syllables")
