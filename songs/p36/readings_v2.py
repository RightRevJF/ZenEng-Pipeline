"""Version 2's readings: the whole song as rebuilt (the v1 sections kept, three lines remapped, the new bridge), and the bridge and the
riff against what the writer asked of them."""
import sys, pickle, numpy as np
sys.argv = ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p36")
import melody_p36 as M
R2 = pickle.load(open("/home/claude/p36/melody_v2.pkl", "rb")); c = R2["pick"]; M.LINES = R2["lines2"]
V1 = pickle.load(open("/home/claude/p36/readings.pkl", "rb"))
ns = c["notes"]; ps = [n["p"] for n in ns]
br = [n for n in ns if n["sec"] == "Bridge"]; v1b = [n for n in pickle.load(open("/home/claude/p36/melody_main.pkl", "rb"))["alive"][0]["notes"] if n["sec"] == "Bridge"]
def iois(xs): return [b["on"] - a["on"] for a, b in zip(xs, xs[1:]) if a["line"] == b["line"]]
def share(xs, v): i = iois(xs); return sum(1 for x in i if x == v) / len(i)
on = {n["on"] for n in ns}
def ct(xs): return sum(1 for n in xs if n["p"] % 12 in M.CH[M.chord_for(n, on)][1]) / len(xs)
d = M.phrase_designs(ns)
out = dict(pitch=M.pitch_bits(ps), iv=M.interval_shares(ps), exact=M.repetition(ns)["exact"], stock8=d["stock8"], stock16=d["stock16"],
           bridge_label=d["at8"]["Bridge bars 1-8"]["label"], bridge_u3=d["at8"]["Bridge bars 1-8"]["u3"][1:],
           returns=[(r[0], r[1], round(r[2], 2), round(r[3], 2)) for r in M.returns_related(c)], keyword=M.keyword_chord(ns)[0],
           chord_tones=M.chord_tone_share(ns)[0], rhythm=M.rhythm_bits(ns), pushed=M.pushed_share(ns), range=(min(ps), max(ps)),
           bridge=dict(sixteenth=share(br, 3), eighth=share(br, 6), quarter_plus=sum(1 for x in iois(br) if x >= 12) / len(iois(br)), chord_tones=ct(br), range=(min(n["p"] for n in br), max(n["p"] for n in br)), **{k: v for k, v in c["bridge"].items() if k not in ("range", "chord_tones")}),
           bridge_v1=dict(sixteenth=share(v1b, 3), eighth=share(v1b, 6), quarter_plus=sum(1 for x in iois(v1b) if x >= 12) / len(iois(v1b))),
           meas=c["meas"], riff=R2["riff"], riff_drawn=R2["riff_drawn"], riff_pass=R2["riff_rows"], deaths=dict(R2["deaths"]), survivors=R2["survivors"],
           built=R2["built"], order=R2["order"], rerun=R2["rerun"], fp=c["fp"], score=c["bridge_score"])
pickle.dump(out, open("/home/claude/p36/readings_v2.pkl", "wb"))
for k, v in out.items(): print(k, v if not isinstance(v, float) else round(v, 3))
