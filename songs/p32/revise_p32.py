"""Revision 1 of 'I Took Him for the Gardener' (9 Nov, after delivery): the writer's note on verse 3, line 2. 'the stone between them clean'
asked the listener to infer why the stone matters; replaced (his choice A) by 'with no one in between' -- six syllables, the same rhythm,
the long-e sound kept against 'trees'. The new words take the old line's notes syllable for syllable: with F4 (pickup) | NO G4 one G4
in G4 be- F4 | -TWEEN E4 on bar 44's downbeat, where 'clean' was. Every other note of the frozen melody is kept; re-evaluated."""
import pickle, sys
sys.path[:0] = ["/home/claude/p32", "/home/claude/carol", "/home/claude/pop"]
import melody_p32 as M
c = pickle.load(open("/home/claude/p32/melody_final_v1.pkl", "rb"))
ln = M.SECS["Verse 3"][1]
assert ln["line"] == "with no one in between;" and len(ln["syl"]) == 6
old = [n for n in c["Verse 3"] if n[4] == 1]; assert len(old) == 6
new = [(o, d, p, x, 1) for (o, d, p, _, _), x in zip(old, ln["syl"])]
out = dict(c); out["Verse 3"] = sorted([n for n in c["Verse 3"] if n[4] != 1] + new, key=lambda n: n[0])
cert, meas = M.evaluate(out)
print("evaluate:", cert or "passes", {k: (round(float(v), 3) if not isinstance(v, int) else v) for k, v in (meas or {}).items()})
assert cert is None
edit = "verse 3 line 2 rewritten (revision 1): 'with no one in between', on the old line's notes syllable for syllable (-TWEEN on E4 at bar 44's downbeat)"
out["meas"] = meas; out["hand"] = list(c["hand"]) + [edit]; out["from_v1"] = c["fp"]; out["fp"] = M.fingerprint(out); out["revision"] = 1
pickle.dump(out, open("/home/claude/p32/melody_final.pkl", "wb"))
print([(x[0], o - ln["at"], p) for o, d, p, x, _ in new]); print("fp", out["fp"], "(was", c["fp"] + ")")
