# rep_singletons_after: REP on single-song artists

**Verdict: LEAD-UNSETTLED.** Written after seeing results; never in K. p misses .05, and −0.03 sits inside the range.

## What was predicted

Written in `PREDICTION.md` (commit 1ffa3b6) **after** the eight results were seen and rep_entropy had passed, before this outcome was joined: the same measure (pc_entropy) on the Hooktheory songs whose artist has only one song, which run 04's rows leave out. **β = −0.03**. Lead passes on p < .05 with a negative sign, both halves and the logit negative; killed if −0.03 falls outside β̂ ± 1.96 SE; otherwise unsettled.

## What came out

**β = −0.025** (SE 0.016), 95% range −0.056 to +0.006, p = 0.12; 3,596 songs, one per artist. There is **no artist effect**: the comparison is **across artists** (HC1 robust SEs).

Halves: −0.007 (SE 0.022, p 0.76; 1,845 songs) and −0.043 (SE 0.023, p 0.059; 1,751 songs). Both negative.

Logit: −0.075 (SE 0.051), negative. With one song per artist there are no artist groups, so it is a plain logit on all the songs, sign only.

Taken up by another artist: 514 of 3,596 songs (14.3%).

The signs all fit, but p misses .05, so the lead does not pass; −0.03 is inside the range, so it is not killed. `result.json` states **unsettled**.

## Reading (decides nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `held_n_pitch_range_ln_notes_mel_ic` | +0.040 | 0.022 | 0.073 | − |

With size (n_pitch, range, ln_notes) and mel_ic_mean held, the estimate **changes sign**, to +0.040 (p 0.073). Across artists, the raw tilt cannot be told apart from melody size.

## The gate

None was run on these songs. REP's figures in `measure_gates11.json` (within-artist songs): stability 0.389 (4,271 pairs); top overlap n_pc +0.878 (exempt); R² on the 13 baselines 1.000.

## Power

Printed before the join (`power.json`): **0.383** at α .05, fake SE 0.017 on 3,610 songs. The real SE (0.016) came out a little smaller. The artist-effect reason given for the eight within-artist tests does not apply here, since there is no artist effect; the gap is small and changes nothing.

## How firm it is

Not firm: chosen after the fact, uncounted, unsettled, and its one reading flips sign.

## What it cannot say

- **Seen songs, chosen after seeing results.** These songs were joined once before (run 05, one chord measure).
- **Across artists.** Genre and era are not held.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **No first year.** Not held on this margin.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
