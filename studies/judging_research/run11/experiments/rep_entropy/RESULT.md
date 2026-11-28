# rep_entropy: REP, fewer pitch classes

**Verdict: PASSED.** p < 0.01 with the predicted sign, both halves and the conditional logit agreeing.

## What was predicted

Frozen in `PREDICTION.md` (commit e1858c0) before any outcome was joined: a melody that spreads its time over fewer pitch classes (lower pitch-class entropy, McBride and Leroi's measure) is taken up by other artists more often. Counted bare, rank 3 of 5, the replication anchor. **β = −0.03** within artist. Pass: p < 0.01 (K = 5), the predicted sign, and both halves and the conditional logit with that sign. Kill: the prediction outside β̂ ± 1.96 SE. Otherwise unsettled.

## What came out

**β = −0.029** SD per SD (SE 0.011), 95% range −0.051 to −0.008, p = 0.0076; 9,586 songs, 1,741 artists. Extras held: none.

Artist halves: −0.010 (SE 0.016, p 0.50; 4,616 songs, 886 artists) and −0.046 (SE 0.016, p 0.0037; 4,970 songs, 855 artists).

Conditional logit: −0.164 (SE 0.050), sign as predicted. It uses only the 464 artist groups (3,640 songs) where the outcome varies, so only its sign counts.

Taken up by another artist: 2,130 of 9,586 songs (22.2%).

All four conditions hold, so `result.json` states **passed**.

The two halves differ in size (4,616 songs against 4,970) and in strength: half 0 is small and far from significant (−0.010, p 0.50), while half 1 carries most of the signal (−0.046, p 0.0037). The rule asks only that both share the sign.

## Readings (uncounted; they decide nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `all_other_12_baselines_and_mel_ic_mean_held` | −0.029 | 0.020 | 0.16 | − |
| `intensive_covers_first_year_held` | −0.016 | 0.017 | 0.35 | − |
| `n_pitch_range_mel_ic_mean_held` | −0.026 | 0.015 | 0.073 | − |
| `n_pc` | −0.021 | 0.010 | 0.031 | − |

## The gate

From `measure_gates11.json`, before any outcome: clip-to-clip stability 0.389 (4,271 pairs; bar 0.20); top overlap n_pc +0.878 (bar 0.70; exempt, REP is a baseline by design); R² on the 13 baselines 1.000. Gate: **passes**.

## Power

Printed before the join (`power.json`, 300 fake outcomes, seed 11): **0.220** at α 0.01; kill if true 0.017, kill if zero 0.547; fake SE 0.015.

The real SE, 0.011, came out smaller than the fake-outcome SE, 0.015. The real outcome's variance is partly between artists, and the artist fixed effect absorbs that part; the fake outcome had none. So the frozen power figures understated the test's real power. This changes no verdict.

## How firm it is

Modest. p = 0.0076 is just under the bar. The readings with other baselines held keep the size but lose significance: −0.029 (p 0.16) with the other 12 and mel_ic_mean held, −0.026 (p 0.073) with n_pitch, range and mel_ic_mean held. So this cannot separate pitch-class spread from melody size. On seen songs, a pass is a lead until unseen melodies confirm it.

## What it cannot say

- **Seen songs.** The 9,588 within-artist Hooktheory songs had been joined to chord measures in runs 04 to 06. The measure is new to them; the songs are not.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **Within artist only.** It compares songs by the same artist, not artists with each other.
- **No first year on this margin.** Songs missing from Discogs-VI have none; only the intensive reading holds it.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
