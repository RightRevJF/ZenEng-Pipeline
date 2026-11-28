# gap_rooms: GAP, the two-room melody

**Verdict: KILLED.** The prediction lies outside the estimate's 95% range.

## What was predicted

Frozen in `PREDICTION.md` (commit e1858c0) before any outcome was joined: a melody whose pitch-transition graph splits into two "rooms" joined by a thin doorway (a small spectral gap; Jason's S = 1 + λ2/π is the same test) is taken up by other artists more often. Counted, rank 1 of 5. **β = −0.03** within artist. Pass: p < 0.01 (K = 5), the predicted sign, and both halves and the conditional logit with that sign. Kill: the prediction outside β̂ ± 1.96 SE. Otherwise unsettled.

## What came out

**β = +0.001** SD per SD (SE 0.011), 95% range −0.020 to +0.022, p = 0.93; 9,564 songs, 1,740 artists. Extras held: range, n_pitch, ln_notes.

Artist halves: +0.013 (SE 0.015, p 0.36; 4,604 songs, 885 artists) and −0.012 (SE 0.016, p 0.45; 4,960 songs, 855 artists).

Conditional logit: −0.018 (SE 0.050), sign as predicted. It uses only the 463 artist groups (3,630 songs) where the outcome varies, so only its sign counts.

Taken up by another artist: 2,121 of 9,564 songs (22.2%).

The estimate is at zero on the wrong side, the halves split, and the range stops at −0.020. `result.json` states **killed**.

## Readings (uncounted; they decide nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `bare_no_extras` | +0.011 | 0.010 | 0.28 | − |
| `all_13_baselines_and_mel_ic_mean_held` | +0.001 | 0.014 | 0.95 | − |
| `intensive_covers_first_year_held` | −0.007 | 0.023 | 0.77 | − |
| `G_ROOMS` | −0.005 | 0.008 | 0.54 | + |
| `G_ROOMS_holding_G_GAP` | −0.005 | 0.009 | 0.55 | + |
| `SETTLE` | −0.025 | 0.012 | 0.038 | + |
| `R_CHEEGER_R10-C1` | +0.014 | 0.012 | 0.25 | − |
| `R_CUT_AB_R10-L3` | +0.009 | 0.010 | 0.35 | + |
| `R_SGAP_R10-G3` | −0.002 | 0.012 | 0.83 | − |
| `R_PE_H0_R10-G1` | −0.015 | 0.012 | 0.22 | + |
| `R_IRR_R10-G2` | −0.001 | 0.009 | 0.96 | − |
| `R_ARCH_R10-I1` | +0.004 | 0.008 | 0.64 | − |

## The gate

From `measure_gates11.json`, before any outcome: clip-to-clip stability 0.200 (0.2004 to four places) (4,239 pairs; bar 0.20); top overlap n_pitch −0.612 (bar 0.70); R² on the 13 baselines 0.571. Gate: **passes**.

## Power

Printed before the join (`power.json`, 300 fake outcomes, seed 11): **0.220** at α 0.01; kill if true 0.023, kill if zero 0.473; fake SE 0.015.

The real SE, 0.011, came out smaller than the fake-outcome SE, 0.015. The real outcome's variance is partly between artists, and the artist fixed effect absorbs that part; the fake outcome had none. So the frozen power figures understated the test's real power. This changes no verdict.

## How firm it is

Firm as a kill of −0.03; a small negative effect nearer zero is not excluded. The measure only just passed its stability gate, which blurs any real effect. SETTLE (p 0.038) runs against its predicted sign and is only a reading. The six run 10 readings failed the gate and read noise.

## What it cannot say

- **Seen songs.** The 9,588 within-artist Hooktheory songs had been joined to chord measures in runs 04 to 06. The measure is new to them; the songs are not.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **Within artist only.** It compares songs by the same artist, not artists with each other.
- **No first year on this margin.** Songs missing from Discogs-VI have none; only the intensive reading holds it.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
