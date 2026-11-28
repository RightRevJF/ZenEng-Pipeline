# lockp_peaks: LOCKP, the footfall

**Verdict: ESTIMATE.** Uncounted; not in K; it decides nothing.

## What was predicted

Frozen in `PREDICTION.md` (commit e1858c0) before any outcome was joined: a melody whose contour peaks land on heavier beats is taken up more often (the dancer lifts on the strong beat). No extras. It failed the gate and ran only under Jason's test-everything rule. **β = +0.02** within artist. Uncounted: not in K = 5, so its verdict is "estimate" whatever comes out. Had it been counted, it would be killed if the prediction fell outside β̂ ± 1.96 SE.

## What came out

**β = +0.007** SD per SD (SE 0.009), 95% range −0.011 to +0.024, p = 0.46; 9,377 songs, 1,740 artists. Extras held: none.

Artist halves: +0.012 (SE 0.013, p 0.36; 4,515 songs, 886 artists) and +0.002 (SE 0.012, p 0.85; 4,862 songs, 854 artists).

Conditional logit: +0.041 (SE 0.042), sign as predicted. It uses only the 458 artist groups (3,554 songs) where the outcome varies, so only its sign counts.

Taken up by another artist: 2,090 of 9,377 songs (22.3%).

The main estimate, both halves and the logit have the predicted sign, but nothing is near significance. +0.02 sits inside the range (`prediction_outside_range`: false), so had it been counted it would have been unsettled. `result.json` states **estimate**.

## Readings (uncounted; they decide nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `all_13_baselines_and_mel_ic_mean_held` | +0.006 | 0.009 | 0.46 | + |
| `intensive_covers_first_year_held` | −0.016 | 0.019 | 0.40 | + |
| `LOCK_R10-I2` | +0.004 | 0.009 | 0.61 | + |
| `LOCKW` | +0.003 | 0.008 | 0.67 | + |

## The gate

From `measure_gates11.json`, before any outcome: clip-to-clip stability 0.143 (3,965 pairs; bar 0.20); top overlap ln_notes +0.071 (bar 0.70); R² on the 13 baselines 0.016. Gate: **stopped**.

## Power

Printed before the join (`power.json`, 300 fake outcomes, seed 11): **0.133** at α 0.01; kill if true 0.033, kill if zero 0.300; fake SE 0.013.

The real SE, 0.009, came out smaller than the fake-outcome SE, 0.013. The real outcome's variance is partly between artists, and the artist fixed effect absorbs that part; the fake outcome had none. So the frozen power figures understated the test's real power. This changes no verdict.

## How firm it is

Weak. The measure is not stable from one clip of a song to the next, so it reads mostly noise, and its frozen power was 0.133. A small positive drift is all it shows.

## What it cannot say

- **Seen songs.** The 9,588 within-artist Hooktheory songs had been joined to chord measures in runs 04 to 06. The measure is new to them; the songs are not.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **Within artist only.** It compares songs by the same artist, not artists with each other.
- **No first year on this margin.** Songs missing from Discogs-VI have none; only the intensive reading holds it.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
