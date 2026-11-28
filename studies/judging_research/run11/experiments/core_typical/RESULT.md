# core_typical: core_ic, a typical skeleton

**Verdict: ESTIMATE.** Uncounted; not in K; it decides nothing.

## What was predicted

Frozen in `PREDICTION.md` (commit e1858c0) before any outcome was joined: a melody whose on-beat skeleton walks the corpus's common paths (low surprisal) is already known before it is heard and is taken up more often. Its power was under the 0.2 floor. **β = −0.03** within artist. Uncounted: not in K = 5, so its verdict is "estimate" whatever comes out. Had it been counted, it would be killed if the prediction fell outside β̂ ± 1.96 SE.

## What came out

**β = +0.002** SD per SD (SE 0.012), 95% range −0.022 to +0.025, p = 0.89; 8,877 songs, 1,728 artists. Extras held: pc_entropy, mel_ic_mean.

Artist halves: −0.010 (SE 0.017, p 0.58; 4,276 songs, 882 artists) and +0.011 (SE 0.017, p 0.51; 4,601 songs, 846 artists).

Conditional logit: −0.008 (SE 0.061), sign as predicted. It uses only the 430 artist groups (3,273 songs) where the outcome varies, so only its sign counts.

Taken up by another artist: 1,948 of 8,877 songs (21.9%).

The estimate is near zero and the halves split; only the logit has the predicted sign. −0.03 lies outside the range (`prediction_outside_range`: true), so had it been counted it would have been killed. `result.json` states **estimate**.

## Readings (uncounted; they decide nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `bare_no_extras` | −0.016 | 0.009 | 0.095 | − |
| `all_13_baselines_and_mel_ic_mean_held` | +0.002 | 0.013 | 0.90 | − |
| `intensive_covers_first_year_held` | −0.035 | 0.028 | 0.21 | − |
| `run10_form_pc_entropy_only` | −0.006 | 0.011 | 0.56 | − |
| `R_SURF_IC` | −0.001 | 0.012 | 0.91 | − |
| `R_TSG_R10-L2b` | +0.002 | 0.010 | 0.85 | − |

## The gate

From `measure_gates11.json`, before any outcome: clip-to-clip stability 0.386 (3,415 pairs; bar 0.20); top overlap mel_ic_mean +0.590 (bar 0.70); R² on the 13 baselines 0.409. Gate: **passes**.

## Power

Printed before the join (`power.json`, 300 fake outcomes, seed 11): **0.190** at α 0.01; kill if true 0.030, kill if zero 0.397; fake SE 0.018.

The real SE, 0.012, came out smaller than the fake-outcome SE, 0.018. The real outcome's variance is partly between artists, and the artist fixed effect absorbs that part; the fake outcome had none. So the frozen power figures understated the test's real power. This changes no verdict.

## How firm it is

The bare reading has the predicted sign (−0.016, p 0.095) but shrinks to −0.006 with pc_entropy held and to about zero with mel_ic_mean held too. What the bare form picks up looks like what existing measures already carry.

## What it cannot say

- **Seen songs.** The 9,588 within-artist Hooktheory songs had been joined to chord measures in runs 04 to 06. The measure is new to them; the songs are not.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **Within artist only.** It compares songs by the same artist, not artists with each other.
- **No first year on this margin.** Songs missing from Discogs-VI have none; only the intensive reading holds it.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
