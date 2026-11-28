# typ11_typical: TYP11, a typical melody

**Verdict: KILLED.** The prediction lies outside the estimate's 95% range.

## What was predicted

Frozen in `PREDICTION.md` (commit e1858c0) before any outcome was joined: a melody whose time over the scale degrees matches the Hooktheory corpus profile feels already known and is taken up more often. Counted, rank 4 of 5, the best powered. **β = +0.03** within artist. Pass: p < 0.01 (K = 5), the predicted sign, and both halves and the conditional logit with that sign. Kill: the prediction outside β̂ ± 1.96 SE. Otherwise unsettled.

## What came out

**β = +0.002** SD per SD (SE 0.009), 95% range −0.016 to +0.020, p = 0.82; 9,586 songs, 1,741 artists. Extras held: mel_ic_mean.

Artist halves: +0.003 (SE 0.014, p 0.83; 4,616 songs, 886 artists) and +0.003 (SE 0.012, p 0.81; 4,970 songs, 855 artists).

Conditional logit: +0.021 (SE 0.047), sign as predicted. It uses only the 464 artist groups (3,640 songs) where the outcome varies, so only its sign counts.

Taken up by another artist: 2,130 of 9,586 songs (22.2%).

The sign is right, and so are both halves and the logit, but the estimate is near zero and the range tops out at +0.020. `result.json` states **killed** by the range rule.

## Readings (uncounted; they decide nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `bare_no_extras` | +0.006 | 0.009 | 0.50 | + |
| `all_13_baselines_and_mel_ic_mean_held` | +0.010 | 0.010 | 0.33 | + |
| `intensive_covers_first_year_held` | +0.035 | 0.020 | 0.075 | + |
| `pc_entropy_held` | +0.007 | 0.009 | 0.42 | + |
| `tonic_share_held` | +0.004 | 0.009 | 0.62 | + |
| `TYP_KK11` | +0.003 | 0.008 | 0.76 | + |
| `TYP_all_12_bins` | +0.009 | 0.009 | 0.34 | + |

## The gate

From `measure_gates11.json`, before any outcome: clip-to-clip stability 0.212 (4,266 pairs; bar 0.20); top overlap n_int +0.245 (bar 0.70); R² on the 13 baselines 0.163. Gate: **passes**.

## Power

Printed before the join (`power.json`, 300 fake outcomes, seed 11): **0.387** at α 0.01; kill if true 0.037, kill if zero 0.660; fake SE 0.013.

The real SE, 0.009, came out smaller than the fake-outcome SE, 0.013. The real outcome's variance is partly between artists, and the artist fixed effect absorbs that part; the fake outcome had none. So the frozen power figures understated the test's real power. This changes no verdict.

## How firm it is

Firm as a kill of +0.03, but a small positive effect is not excluded: every reading is positive, the largest the intensive one (+0.035, p 0.075). TYP_KK11 is near zero too, so the style-or-schema question stays open.

## What it cannot say

- **Seen songs.** The 9,588 within-artist Hooktheory songs had been joined to chord measures in runs 04 to 06. The measure is new to them; the songs are not.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **Within artist only.** It compares songs by the same artist, not artists with each other.
- **No first year on this margin.** Songs missing from Discogs-VI have none; only the intensive reading holds it.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
