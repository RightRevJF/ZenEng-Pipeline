"""Song 32: the frozen pick (top of the ranking) with the inspection's hand edits, logged and re-evaluated."""
import pickle
import melody_p32 as M
R = pickle.load(open("/home/claude/p32/melody_result.pkl", "rb"))
c = dict(R["alive"][0]); S = M.SECS
def setline(sec, i, cell):
    ln = S[sec][i]; ns = [n for n in c[sec] if n[4] == i]; assert len(ns) == len(cell) == len(ln["syl"])
    c[sec] = sorted([n for n in c[sec] if n[4] != i] + [(ln["at"] + o, d, p, x, i) for (o, d, p), x in zip(cell, ln["syl"])], key=lambda n: n[0])
def rel(sec, i): ln = S[sec][i]; return [(n[0] - ln["at"], n[1], n[2]) for n in c[sec] if n[4] == i]
edits = []
# 1. the refrain's last line: the walk's G4 G4 G4 A4 G4 A4 was flat; WHERE now stressed (the song-32 port) -- a rising plea to D5, then GONE on A4
# (the best of the variants that pass, by the composite: 0.880 against the pick's 0.878)
setline("Refrain 1", 3, [(-1, 1, 67), (0, 2, 69), (2, 1, 72), (3, 2, 74), (5, 1, 69), (6, 4, 69)])
setline("Refrain 2", 3, [(-1, 1, 67), (0, 2, 69), (2, 1, 72), (3, 2, 74), (5, 1, 69), (6, rel("Refrain 2", 3)[-1][1], 69)])
edits.append("refrains 1-2, line 4: just G4 | TELL A4 me C5 WHERE D5 he's A4 | GONE A4 (the walk's line sat on G4; WHERE, now stressed, climbs to the title's D5)")
# 2. verse 3's last line: TREES moved from the fifth eighth to the second beat (bar 48), the Name's 'he' a one-eighth pickup
r = rel("Verse 3", 3); assert [x[0] for x in r[-3:]] == [6, 7, 8], r
setline("Verse 3", 3, r[:-2] + [(7, 2, r[-2][2]), (9, 1, r[-1][2])])
r = rel("The Name", 0); assert r[0][:2] == (-2, 2), r
setline("The Name", 0, [(-1, 1, r[0][2])] + r[1:])
edits.append("verse 3 line 4: TREES on the second beat (was the eighth before it); the Name's 'he' shortened to an eighth pickup")
cert, meas = M.evaluate(c)
print("evaluate:", cert or "passes", {k: (round(float(v), 3) if not isinstance(v, int) else v) for k, v in (meas or {}).items()})
print("was:", {k: (round(float(v), 3) if not isinstance(v, int) else v) for k, v in R["alive"][0]["meas"].items()})
assert cert is None
c["meas"] = meas; c["hand"] = edits; c["from"] = R["alive"][0]["fp"]; c["fp"] = M.fingerprint(c)
c["by_construction"] = R["by_construction"]; c["search"] = dict(made=R["made"], tries=R["tries"], survivors=R["survivors"], order_fp=R["order_fp"], deaths=dict(R["deaths"]))
pickle.dump(c, open("/home/claude/p32/melody_final.pkl", "wb"))
for e in edits: print(" ", e)
print("fp", c["fp"], "from", c["from"])
