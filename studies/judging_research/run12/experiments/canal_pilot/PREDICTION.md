# canal_pilot: what stays the same between two arrangers' MIDI files of one song (P11-5), a notes-side pilot

Run 12, 28 November 2026 (the 10:17 ET pass). Idea: **R12-I3 CANAL (Inventor)**. The Inventor withdrew it as a test in round 2 because 156 independent pairs are too few. **Status: PILOT.** It reads no outcome and has no K slot. It joins nothing, so the guard does not apply. It is run once by the chair, after this file was written.

**Disclosure.** An earlier invocation of `harness12.py run canal_pilot` wrote result.json before this file existed. I deleted that result.json unread. The only figure shown was the pair count, 159, which the gates had already printed. The two-file stabilities of the single measures are in `measure_gates12.json` and were seen before this file was written: PCE_ALL 0.736, H1 0.691, REP_L 0.596, E5_L 0.566, PI3c 0.471, ROUGH_X 0.299. They are therefore **not** predictions here.

## The measure
- **CANAL** = 1 − the minimum over the 12 rotations of the Jensen-Shannon divergence (bits) between the two kept files' pitch-class profiles. A profile is the sounding steps of tracks 1, 2 and 4.
- **Pairs:** songs with 2+ kept, non-duplicate files, using file 1 against file 2. There are 159 pairs.
- The near-duplicate rule is in `../pi3c_lakh/PREDICTION.md`.

## Predictions (none computed before this file was written)
- **P1.** Across pairs, CANAL correlates positively with the agreement of the two files on melody entropy. Spearman(CANAL, −|ΔH1|) > +0.20 and Spearman(CANAL, −|ΔREP_L|) > +0.20. When two arrangers agree on the pitch content, they agree on the tune's spread.
- **P2.** Spearman(CANAL, −|ΔPI3c|) is positive but smaller than both P1 values. Order structure is less tied to the profile than spread is.
- **P3.** |Spearman(CANAL, −|ΔROUGH_X|)| < 0.15. Voicing belongs to the arranger, not to the song's pitch content.
- **P4.** |Spearman(CANAL, mean PCE_ALL)| < 0.30, so CANAL is not simplicity under another name. The Inventor saw +0.19 on 156 pairs with a slightly different duplicate rule, so P4 is a check of my recipe, not a fresh prediction.

Also printed, deciding nothing: the CANAL quantiles, the share of pairs in the same key, and the same correlation for E5_L and NPB.

## Kill
Each of P1-P4 is reported true or false. A false P1 would mean the profile's invariance does not carry to the melody measures, and that would weaken the case for using two-file stability as the gate.

## How to run
`cd run12/experiments && python3 harness12.py run canal_pilot`. It reads only the notes-side cache and was run by the chair. Its result is `result.json` here.
