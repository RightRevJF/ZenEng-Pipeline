# Run 12, round 2: the Inventor

No outcome was opened. New check: `measures/inventor_roughx_check.py`, written to `/home/claude/dl/run12/inventor_roughx_check.json`.

**I-1 PROP: revised, and I accept the merge (G3 / L12-3 / I-1).**
- Fit each window separately, with its own five-year first-year dummies (this gives decade × window).
- Add a reading on 1970+ songs only, to deal with the rival 1950s-60s versions.
- Prediction unchanged: REP β_E = β_L ≈ −0.05, Δ = 0.
- This becomes an estimate (power about 0.1) unless pooling raises it to the 0.2 floor.

**I-2 ROUGH: revised to an uncounted estimate.**
- New measure ROUGH_X: drop octave-multiple pairs from both the sum and the count.
- Check on 156 non-duplicate pairs: stability falls to 0.285, and ρ with mean sounding pitch is −0.63. Most of the roughness is register.
- Controls: register, octave-pair share, active tracks, ln events, notes per beat, number of files and run 07's chord measures.
- Prediction: −0.01.
- Stopped if its two-file stability with register held falls below 0.20.

**I-3 CANAL: withdrawn as a test.** It stays a notes-side pilot until there are more than 156 independent pairs.
