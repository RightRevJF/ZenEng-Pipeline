"""Song 45, Q16 A: the writer's hand edits to the pick of record (10c3fce99da2), logged in the pick and evaluated again (every gate and
the design gate). Pitches are the search's (G); the record lifts the last chorus.
  Verse 2, line 1 ('I knew the room before they let us in'): the drawn rhythm kept; the nine E3s re-pitched as a line that rises to G3 on
    'knew', settles on E3 for 'room', dips to D3 and lifts to A3 on 'us' (E3 G3 F#3 E3 D3 E3 G3 G3 A3 G3).
  Chorus, line 2 ('You're only in the next room'): seven sixteenths and a bar and a half of rest re-set in eighths and quarters across the
    slot: D4 (pickup) B3 A3 G3 E3, then 'next' A3 on the downbeat of the second bar and 'room' G3 held two beats. Chorus 2 copies it.
  The last chorus's return of that line ('You were only in the next room') re-set to the same rhythm and tune, the pickup two sixteenths (D4 C4)."""
import sys, pickle, copy
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p49", "/home/claude/p40"]
import melody_p45 as P
F = pickle.load(open("/home/claude/p49/melody_final.pkl", "rb")); c = F["pick"]
assert c["fp"] == "10c3fce99da2" and not c.get("hand_edits")
B = 48
def line(sec, i, rows, stresses):
    U = (P.BAR0[sec] + 2 * i) * B
    return [dict(on=U + t, p=p, syl=k, slur=False, stress=stresses[k], dur=d, sec=sec, line=f"{sec}:{i}") for k, (t, d, p) in enumerate(rows)]
st = lambda sec, i: [s for _, s in P.LINES[sec][i]]
CH1 = [(6, 6, 62), (12, 12, 59), (24, 6, 57), (30, 6, 55), (36, 12, 52), (48, 12, 57), (60, 24, 55)]
LC1 = [(6, 3, 62), (9, 3, 60), (12, 12, 59), (24, 6, 57), (30, 6, 55), (36, 12, 52), (48, 12, 57), (60, 24, 55)]
V2P = [52, 55, 54, 52, 50, 52, 55, 55, 57, 55]
old = {k: [dict(n) for n in c["notes"] if n["line"] == k] for k in ("Verse 2:0", "Chorus 1:1", "Chorus 2:1", "Last Chorus:1")}
new = {"Chorus 1:1": line("Chorus 1", 1, CH1, st("Chorus 1", 1)), "Chorus 2:1": line("Chorus 2", 1, CH1, st("Chorus 2", 1)),
       "Last Chorus:1": line("Last Chorus", 1, LC1, st("Last Chorus", 1)),
       "Verse 2:0": [dict(n, p=q) for n, q in zip(old["Verse 2:0"], V2P)]}
assert len(old["Verse 2:0"]) == len(V2P) and len(LC1) == len(P.LINES["Last Chorus"][1]) and len(CH1) == len(P.LINES["Chorus 1"][1])
for k in ("Chorus 1:1", "Chorus 2:1", "Last Chorus:1"): new[k][-1]["hold"] = 24
c["notes"] = sorted([n for n in c["notes"] if n["line"] not in new] + [n for k in new for n in new[k]], key=lambda n: n["on"])
for a, b in zip(c["notes"], c["notes"][1:]): assert a["on"] + a["dur"] <= b["on"], (a, b)
for p in ("V", "C"): P.KNOBS[p].update(F["run"]["knobs"][p])
P.LK.update(F["run"]["line_knobs"])
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| design:", P.design_fails(c) or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not P.design_fails(c) and not c["info"]["soft"]
c["judge"] = P.judge(c["notes"]); c["meas"] = meas
fmt = lambda ns: [(n["on"], n["p"], n["dur"]) for n in ns]
c["hand_edits"] = [dict(line=k, why=w, before=fmt(old[k]), after=fmt(new[k])) for k, w in (
    ("Verse 2:0", "Q16 A: nine E3s re-pitched, the drawn rhythm kept"), ("Chorus 1:1", "Q16 A: sixteenths and a long rest re-set across the slot"),
    ("Chorus 2:1", "Q16 A: chorus 2 copies chorus 1"), ("Last Chorus:1", "Q16 A: the last chorus's return re-set to match"))]
F["pick"] = c; pickle.dump(F, open("/home/claude/p49/melody_final.pkl", "wb"))
print("judge", round(c["judge"]["combined"], 3), "composite", meas["composite"])
