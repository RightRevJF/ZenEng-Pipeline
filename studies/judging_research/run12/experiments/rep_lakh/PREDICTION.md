# rep_lakh: the REP replication on Lakh whole songs (the skyline's pitch-class entropy)

Run 12, 28 November 2026 (the 10:17 ET pass). Frozen by the chair before any outcome is joined. No outcome was opened, and only a dry run on a synthetic outcome was made. Idea: the replication that run 11's first principles asked for. REP passed on Hooktheory clips, which are seen songs; no melody measure has been joined to the Lakh songs. **Status: ESTIMATE.** Power at .05/3 is 0.070, under the 0.2 floor, so it passes nothing and kills nothing. K = 3, α = .05/3 = 0.0167 for the counted tests.

## The measure (frozen; `build_lakh12.py`, key `REP_L`)
Run 11's REP recipe on the Lakh skyline:
- **Skyline:** the highest pitch of tracks 1, 2 and 4 at each eighth, trimmed to the sounding span.
- **Profile:** the duration-weighted pitch-class profile, counting sounding eighths per pitch class (rests carry nothing).
- **REP_L:** the Shannon entropy of that profile in bits.
- **Song value:** the mean over kept files. Near-duplicate files are counted once, under the rule in `pi3c_lakh/PREDICTION.md`.

**Gate:** two-file stability **0.596** (159 non-duplicate pairs). The largest overlap with an existing measure is V +0.63. Its twin H1 (+0.885) is exempt, as REP was. **Passes.**

## Songs
Lakh within-artist songs with REP_L and the controls finite: **5,848 songs, 1,661 artists**. SEEN, as in pi3c_lakh.

## Outcome
**y_foreign** (run 07's rule).

## Model and controls
- OLS of z(y_foreign) on z(REP_L), with artist FE.
- Run 07's controls: ln_chg, V, ln_bars and five-year year bins.
- The Skeptic's Lakh controls: LNEV, NPB, ACT, NFILES.
- CR1 SEs by artist; conditional logit for the sign; halves md5(artist) mod 2.

## Prediction
**β = −0.02**, run 11's −0.03 shrunk.

## Verdict rules (they would apply if it were counted)
- **Pass:** p < 0.0167, β < 0, both halves < 0, and the conditional logit < 0.
- **Killed:** −0.02 lies outside β̂ ± 1.96 SE.
- **Unsettled:** otherwise.

## Power (within-artist share 0.46; 300 draws, seed 12)

| α | power | median fake SE | kill if zero |
|---|---|---|---|
| 0.0167 | **0.070** | 0.0182 | 0.167 |
| 0.05 | 0.170 | | |

The bare form, with run 07's controls only, gives power 0.097 at 0.0167 (SE 0.0166). It is under the floor at every K, so the frozen form was not changed to chase power.

## Readings (uncounted)
- **Bare:** run 07's controls only.
- **With ln events held only.**
- **H1:** the event pitch-class entropy, which is the Listener's twin, with all controls.

All three have predicted sign −.

## How to run (once, after commit and push)
`cd run12/experiments && python3 harness12.py run rep_lakh`
