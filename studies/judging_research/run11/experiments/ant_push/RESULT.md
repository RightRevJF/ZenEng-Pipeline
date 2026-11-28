# ant_push: ANT, the push

**Verdict: KILLED.** The prediction lies outside the estimate's 95% range.

## What was predicted

Frozen in `PREDICTION.md` (commit e1858c0) before any outcome was joined: a melody that reaches the next chord's new tone early carries the changes itself, so a cover artist with another groove still gets them, and it is taken up more often. Counted, rank 5 of 5. **β = +0.03** within artist. Pass: p < 0.01 (K = 5), the predicted sign, and both halves and the conditional logit with that sign. Kill: the prediction outside β̂ ± 1.96 SE. Otherwise unsettled.

## What came out

**β = −0.004** SD per SD (SE 0.011), 95% range −0.025 to +0.016, p = 0.68; 9,361 songs, 1,740 artists. Extras held: density.

Artist halves: −0.015 (SE 0.014, p 0.30; 4,512 songs, 885 artists) and +0.006 (SE 0.015, p 0.70; 4,849 songs, 855 artists).

Conditional logit: −0.013 (SE 0.043), sign against the prediction. It uses only the 451 artist groups (3,515 songs) where the outcome varies, so only its sign counts.

Taken up by another artist: 2,084 of 9,361 songs (22.3%).

The estimate is near zero on the wrong side, the halves split, the logit is negative, and the range tops out at +0.016. `result.json` states **killed**.

## Readings (uncounted; they decide nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `bare_no_extras` | −0.005 | 0.010 | 0.63 | + |
| `all_13_baselines_and_mel_ic_mean_held` | −0.003 | 0.010 | 0.78 | + |
| `intensive_covers_first_year_held` | +0.016 | 0.017 | 0.35 | + |
| `sync_per_note_held` | −0.003 | 0.011 | 0.80 | + |
| `CT_held` | −0.007 | 0.011 | 0.55 | + |

## The gate

From `measure_gates11.json`, before any outcome: clip-to-clip stability 0.252 (3,981 pairs; bar 0.20); top overlap density +0.272 (bar 0.70); R² on the 13 baselines 0.109. Gate: **passes**.

## Power

Printed before the join (`power.json`, 300 fake outcomes, seed 11): **0.280** at α 0.01; kill if true 0.027, kill if zero 0.610; fake SE 0.014.

The real SE, 0.011, came out smaller than the fake-outcome SE, 0.014. The real outcome's variance is partly between artists, and the artist fixed effect absorbs that part; the fake outcome had none. So the frozen power figures understated the test's real power. This changes no verdict.

## How firm it is

Firm as a kill of +0.03; every reading is near zero. The measure depends on where the transcriber put each chord change, which the artist effect absorbs only in part.

## What it cannot say

- **Seen songs.** The 9,588 within-artist Hooktheory songs had been joined to chord measures in runs 04 to 06. The measure is new to them; the songs are not.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **Within artist only.** It compares songs by the same artist, not artists with each other.
- **No first year on this margin.** Songs missing from Discogs-VI have none; only the intensive reading holds it.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
