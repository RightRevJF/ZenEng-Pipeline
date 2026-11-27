# key_travel: result (run 08, counted, card 1)

**In plain words.** Do a composer's tunes that travel further around the keys get recorded by more artists than that composer's other tunes? No. More travel went with slightly *less* covering, and the predicted size is ruled out: **killed** by the rule written first.

**How the measure works (a worked example).** Put the 12 notes on the circle of fifths (C, G, D, A, E, B, F#, Db, Ab, Eb, Bb, F, then back to C). Cut a chart into 4-bar windows and ask how far the notes must move, around that circle, to turn one window into the next. Take a tune whose windows are C major, C major, F major, C major. C to C costs 0. C (C, E, G) to F (F, A, C) costs 1: each note slides one step (G to C, C to F, E to A). F back to C costs 1. The tune's travel is the average, (0 + 1 + 1) / 3 = 0.67. If the middle window were Db major, three steps away, each move would cost 3 and the travel would be 2.0. A plain note-by-note count (L1, held in the model) scores those two moves as 1.33 and 2.0, so it barely tells near from far. Travel does.

**What was predicted (frozen before the outcome).** +0.05 SD of coverage (y_cov, the standardised log of 1 + distinct artist sets) per SD of travel (TRAV5). It passes with p < .01, a positive sign in both composer halves and a positive Poisson coefficient. It is killed if +0.05 lies outside the estimate ± 1.96 SE.

**What came out.** 5,829 songs, 1,198 composers.
- Power, printed before the estimate: 0.213 (composer share 0.3), matching the frozen 0.213; 0.323 at share 0.5.
- Estimate −0.031, SE 0.026, p 0.23; 95% range −0.082 to +0.020.
- Halves: −0.031 (SE 0.037) and −0.035 (SE 0.036).
- Poisson on n_sets: +0.057, SE 0.049, p 0.25 (log scale, opposite sign).

**Verdict: KILLED.** +0.05 is above the range's top (+0.020), 3.1 SE from the estimate. A range kill doesn't depend on alpha, so moving from .01 to .05/6 changes nothing.

**How firm.** Fairly firm on size. If +0.05 were true, this kill would fire on only 3.7% of fake draws, and the real SE (0.026) matches the fake one (0.028). Both halves agree. The sign is not settled: the Poisson model points the other way, and its range includes +0.05. So "no gain of the predicted size" is firm. "Travel hurts" is not.

**Renaming check (measure_gates.json).** Two-chart stability 0.738 (0.619 after size), iReal against Wikifonia 0.515. Within composer, ρ with ch_rep is −0.285 and with V +0.208. The gate passes, so this is not a renamed known measure. Its ρ with TRAVL1 is 0.822, which widens the SE.

**Readings (they decide nothing).** E (predicted +0.08): −0.026, SE 0.018, p 0.14. TRAV5 without TRAVL1: −0.011, SE 0.015, p 0.49. Writer-match songs only (5,516 songs): −0.025, SE 0.026, p 0.34.

**What it cannot say.**
- Genre is held, style within genre is not; TRAV5 partly detects jazz idiom, which may drive covering on its own.
- Chart writers spell keys differently (cross-source 0.52).
- Songs are joined to recordings by name matching.
- Only tunes someone charted are included.
