"""The control for the outer-voice gates: the same tunes (the same seed and generator), harmonized with a bass of chord roots and the
outer-voice terms off. How many of the new gates would bite when the search does not build them in."""
import random, collections, pickle, sys
import melody_p35 as M
M.ABLATE = True
rng = random.Random(20261110 + 35); would = collections.Counter(); built = 0; harm_fail = 0
for i in range(500):
    c = M.generate(rng); h, err = M.harmonize(c, rng)
    if err: harm_fail += 1; continue
    built += 1; f, rd = M.audit(c, h)
    for g in f: would[g] += 1
print(f"control: {built} harmonized with root-position basses ({harm_fail} could not be)")
for g in M.NEW_GATES: print(f"   {would[g]:5d}  {g}")
pickle.dump(dict(built=built, harm_fail=harm_fail, would=would), open("/home/claude/p35/ablate.pkl", "wb"))
