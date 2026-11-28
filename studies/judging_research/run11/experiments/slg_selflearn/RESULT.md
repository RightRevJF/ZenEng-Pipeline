# slg_selflearn: SLG, the tune that teaches itself

**Verdict: ESTIMATE.** Uncounted; not in K; it decides nothing.

## What was predicted

Frozen in `PREDICTION.md` (commit e1858c0) before any outcome was joined: a melody whose own earlier notes predict its second half better than the corpus does is learned by ear quickly and taken up more often. Sixth in rank with the counted set full. **β = +0.03** within artist. Uncounted: not in K = 5, so its verdict is "estimate" whatever comes out. Had it been counted, it would be killed if the prediction fell outside β̂ ± 1.96 SE.

## What came out

**β = −0.010** SD per SD (SE 0.011), 95% range −0.032 to +0.012, p = 0.36; 8,877 songs, 1,728 artists. Extras held: bar_rep, ln_notes.

Artist halves: −0.015 (SE 0.015, p 0.33; 4,276 songs, 882 artists) and −0.007 (SE 0.016, p 0.68; 4,601 songs, 846 artists).

Conditional logit: −0.059 (SE 0.055), sign against the prediction. It uses only the 430 artist groups (3,273 songs) where the outcome varies, so only its sign counts.

Taken up by another artist: 1,948 of 8,877 songs (21.9%).

The main estimate, both halves and the logit all point the wrong way. +0.03 lies outside the range (`prediction_outside_range`: true), so had it been counted it would have been killed. `result.json` states **estimate**.

## Readings (uncounted; they decide nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `bare_no_extras` | −0.007 | 0.010 | 0.51 | + |
| `all_13_baselines_and_mel_ic_mean_held` | −0.001 | 0.015 | 0.97 | + |
| `intensive_covers_first_year_held` | −0.050 | 0.032 | 0.11 | + |
| `mel_rep_held` | −0.013 | 0.012 | 0.28 | + |
| `R_SLGW` | −0.011 | 0.012 | 0.35 | + |

## The gate

From `measure_gates11.json`, before any outcome: clip-to-clip stability 0.247 (3,415 pairs; bar 0.20); top overlap mel_rep +0.443 (bar 0.70); R² on the 13 baselines 0.471. Gate: **passes**.

## Power

Printed before the join (`power.json`, 300 fake outcomes, seed 11): **0.227** at α 0.01; kill if true 0.023, kill if zero 0.487; fake SE 0.016.

The real SE, 0.011, came out smaller than the fake-outcome SE, 0.016. The real outcome's variance is partly between artists, and the artist fixed effect absorbs that part; the fake outcome had none. So the frozen power figures understated the test's real power. This changes no verdict.

## How firm it is

Clear for an estimate: no sign of the predicted effect, and holding its main renamer, mel_rep, does not change that. Fewer songs qualify (it needs 16 collapsed and 8 on-beat notes).

## What it cannot say

- **Seen songs.** The 9,588 within-artist Hooktheory songs had been joined to chord measures in runs 04 to 06. The measure is new to them; the songs are not.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **Within artist only.** It compares songs by the same artist, not artists with each other.
- **No first year on this margin.** Songs missing from Discogs-VI have none; only the intensive reading holds it.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
