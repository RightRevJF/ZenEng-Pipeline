# tie_rooms: TIE, melody-harmony rooms

**Verdict: KILLED.** The prediction lies outside the estimate's 95% range.

## What was predicted

Frozen in `PREDICTION.md` (commit e1858c0) before any outcome was joined: a tune in which each chord "owns" its own melody notes (a high G_TIE, from the pitch-class by chord table) is taken up more often, since another artist can re-arrange the backing and keep the song. Counted, rank 2 of 5. **β = +0.03** within artist. Pass: p < 0.01 (K = 5), the predicted sign, and both halves and the conditional logit with that sign. Kill: the prediction outside β̂ ± 1.96 SE. Otherwise unsettled.

## What came out

**β = −0.010** SD per SD (SE 0.009), 95% range −0.028 to +0.008, p = 0.26; 9,574 songs, 1,741 artists. Extras held: ln_notes, density, n_pc.

Artist halves: −0.011 (SE 0.014, p 0.43; 4,607 songs, 886 artists) and −0.010 (SE 0.012, p 0.40; 4,967 songs, 855 artists).

Conditional logit: −0.078 (SE 0.048), sign against the prediction. It uses only the 462 artist groups (3,628 songs) where the outcome varies, so only its sign counts.

Taken up by another artist: 2,126 of 9,574 songs (22.2%).

The main estimate, both halves and the logit are all negative, and the range tops out at +0.008. `result.json` states **killed**.

## Readings (uncounted; they decide nothing)

| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| `bare_no_extras` | −0.011 | 0.009 | 0.19 | + |
| `all_13_baselines_and_mel_ic_mean_held` | −0.012 | 0.010 | 0.26 | + |
| `intensive_covers_first_year_held` | −0.036 | 0.020 | 0.070 | + |
| `CT_held` | −0.013 | 0.010 | 0.21 | + |
| `G_TIE_BC_bergsma` | −0.003 | 0.008 | 0.69 | + |
| `HB` | −0.008 | 0.009 | 0.36 | + |

## The gate

From `measure_gates11.json`, before any outcome: clip-to-clip stability 0.265 (4,258 pairs; bar 0.20); top overlap ln_notes −0.342 (bar 0.70); R² on the 13 baselines 0.342. Gate: **passes**.

## Power

Printed before the join (`power.json`, 300 fake outcomes, seed 11): **0.330** at α 0.01; kill if true 0.027, kill if zero 0.603; fake SE 0.014.

The real SE, 0.009, came out smaller than the fake-outcome SE, 0.014. The real outcome's variance is partly between artists, and the artist fixed effect absorbs that part; the fake outcome had none. So the frozen power figures understated the test's real power. This changes no verdict.

## How firm it is

Firm. Every reading is negative too, including the intensive one and the Inventor's HB. The measure also leans on where Hooktheory annotators placed the chords.

## What it cannot say

- **Seen songs.** The 9,588 within-artist Hooktheory songs had been joined to chord measures in runs 04 to 06. The measure is new to them; the songs are not.
- **Uptake, not love.** The outcome is a version by another artist (a covers measure), not lasting love.
- **Within artist only.** It compares songs by the same artist, not artists with each other.
- **No first year on this margin.** Songs missing from Discogs-VI have none; only the intensive reading holds it.

## Credit

Hooktheory TheoryTab annotations via Sheet Sage (CC BY-NC-SA 3.0). Discogs-VI 20240701 (CC BY-SA 4.0).
