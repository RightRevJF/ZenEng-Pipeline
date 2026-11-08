"""Revision 1 of 'The Word Without a Word' (8 Nov, after delivery): the writer's attached notes, move 1 -- the refrain's seed planted in the
verses. Line 1 of verses 1-3 now carries the title line's shape in small, a fourth lower: a held reciting note, a step down, back, and a
fourth up to the line's second downbeat (refrain: Bb4 Bb4 Bb4 Ab4 Bb4 | Eb5; the seed: F4 F4 F4 F4 F4 Eb4 F4 | Bb4 over Bb minor). All three
lines have eight syllables with stresses on both downbeats, so they take the seed's onsets and pitches syllable for syllable. Every other note of the frozen pick (f10477ea1784) is
kept; the joins are re-trimmed and the result re-evaluated. Verse 4 keeps its climb (its line 1 would lose the E-flat5 the build needs)."""
import pickle, sys
sys.path[:0] = ["/home/claude/p29", "/home/claude/carol", "/home/claude/pop"]
import melody_p29 as M
c = pickle.load(open("/home/claude/p29/melody_final_v1.pkl", "rb"))
S = M.SECS
SEED_SL = [-3, -2, -1, 0, 3, 4, 5, 6]; SEED_DU = [1, 1, 1, 2, 1, 1, 1, 3]; SEED_P = [65, 65, 65, 65, 65, 63, 65, 70]
ln0 = S["Verse 1"][0]
assert len(ln0["syl"]) == 8
seed = [(ln0["at"] + s_, d, p, x, 0) for s_, d, p, x in zip(SEED_SL, SEED_DU, SEED_P, ln0["syl"])]
edits = ["verse 1 line 1 designed: the seed (F4 x5, Eb4, F4 | Bb4 on the second downbeat, over Bb minor)"]
new = {"Verse 1": seed}
for sec in ("Verse 2", "Verse 3"):                        # eight syllables each, both stressed on the downbeats: the seed's own onsets and pitches
    ln = S[sec][0]; assert len(ln["syl"]) == 8 and ln["syl"][3][2] and ln["syl"][7][2], sec
    new[sec] = [(ln["at"] + s_, d, p, x, 0) for s_, d, p, x in zip(SEED_SL, SEED_DU, SEED_P, ln["syl"])]
    edits.append(f"{sec.lower()} line 1 set to the seed, syllable for syllable (eight syllables, the stresses on both downbeats)")
out = dict(c)
for sec, ns in new.items():
    out[sec] = sorted(ns + [n for n in c[sec] if n[4] != 0], key=lambda n: n[0])
allz = sorted([(o, d, p, x, (s_, i), s_) for s_ in M.SINGS for o, d, p, x, i in out[s_]], key=lambda n: n[0])
for j in range(len(allz) - 1):
    a, b = allz[j], allz[j + 1]
    assert b[0] > a[0], (a, b)
    if a[4] != b[4] and a[0] + a[1] > b[0] - 1:
        nd = b[0] - 1 - a[0]; assert nd >= 1, (a, b); allz[j] = (a[0], nd) + a[2:]
    elif a[0] + a[1] > b[0]: allz[j] = (a[0], b[0] - a[0]) + a[2:]
for s_ in M.SINGS: out[s_] = [(o, d, p, x, k_[1]) for o, d, p, x, k_, ss in allz if ss == s_]
cert, meas = M.evaluate(out)
print("evaluate:", cert or "passes", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in (meas or {}).items()})
print("was:", {k: (round(float(v), 3) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()})
assert cert is None
out["meas"] = meas; out["hand"] = list(c["hand"]) + edits; out["from"] = c["fp"]; out["fp"] = M.fingerprint(out); out["revision"] = 1
out["plans"] = dict(c["plans"]); 
for sec in ("Verse 1", "Verse 2", "Verse 3"): out["plans"][sec] = "line 1 the refrain's seed (revision 1); lines 2-4 " + str(c["plans"][sec])
pickle.dump(out, open("/home/claude/p29/melody_final.pkl", "wb"))
for e in edits: print(" ", e)
print("fp", out["fp"])
