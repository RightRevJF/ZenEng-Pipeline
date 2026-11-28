# windows_lakh_after: result (after seeing results; an estimate)

**Predicted (rule 2d64143, before any Lakh cover timing was joined):** on run 07's within-artist Lakh songs, chord repetition (ch_rep, read from the MIDI file) goes with fewer LATE covers (age 8+) more than early ones (ages 0-3): Δ = β_L − β_E = −0.12. K = 4 for the pass, α .0125.

**Two runs, both reported (NOTE_rerun.md, 3f22888).** The first run's code read the YouTube-matched subset of Discogs-VI, not the full file PREDICTION.md names; I fixed that one line and declared, before the second run, that the second is the verdict of record.

| Run | Songs (artists) | β early | β late | Δ (SE) | p | Halves Δ |
|---|---|---|---|---|---|---|
| **Second (full Discogs-VI; of record)** | 1,926 (601) | +0.115 (0.080) | +0.122 (0.082) | **+0.006 (0.097)** | .95 | −0.094, +0.133 |
| First (YT subset; void) | 1,069 (352) | +0.076 (0.113) | −0.038 (0.106) | −0.114 (0.116) | .32 | −0.360, +0.046 |

**Verdict: unsettled, and an estimate.** The prediction −0.12 lies inside the range (−0.18 to +0.20), so it is not killed; Δ is not negative, so nothing passes. The real SE (0.097) is above the 0.072 that PREDICTION.md said would make the power fall under the 0.2 floor, so by its own rule this is an estimate that passes nothing and kills nothing.

**What it says, plainly.** On Lakh songs there is no sign that chord repetition's link to covers sits in the late window: both windows lean the same way (and the opposite way to Hooktheory, positive here, both within noise). Readings: skyline pitch-class entropy Δ +0.008 (SE 0.082); ch_rep on songs from 1970 on Δ −0.040 (SE 0.091). The Hooktheory window gap (Δ −0.24, analytic SE 0.072) was not reproduced. It stays an unconfirmed lead on seen songs, weaker now.

**What it cannot say.** Lakh's chord repetition is read from an arranger's MIDI and agrees only 0.32 with Hooktheory's, so this is a test of the idea, not of the same number. The SEs are large: a true Δ of −0.12 would be missed most of the time.

Credit: Lakh MIDI / LPD (CC BY 4.0); Discogs-VI 20240701 (CC BY-SA 4.0).
