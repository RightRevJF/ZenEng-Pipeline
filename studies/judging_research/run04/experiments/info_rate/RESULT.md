# Information rate (R04-I3): result

Run 04, 24 November 2026. The rule is `PREDICTION.md` in this folder, frozen in commit 00ab557 before this script was written. The script is `test.py` and its full output is `result.json`. Run it with `python3 test.py`, or `python3 test.py --notes-only` to stop before the outcome. It takes about 30 seconds.

**Verdict by the rule: KILL.** β = −0.16 pp per SD of D. The kill line is β > −0.3 pp.

## What was predicted
- **The claim (Inventor):** each song has a rate, its surprise per beat: r = (`n_mel`·`mel_ic_mean` + `n_ch`·`ch_ic_mean`) / `beats`.
- **D** is how far a song's rate sits from the habitual rate: |ln r − ln 4.32|, where 4.32 is the corpus median over clips.
- **The prediction:** within one artist's own songs, a larger D goes with a lower chance of the song being in Discogs-VI. The predicted size was **−0.8 pp per SD of D**.
- **Pass needed all of these:** β < 0, p < .01 (five hypotheses tonight, so .05/5), β < 0 in both md5 artist halves, and a negative conditional-logit coefficient.

## What was done, in the rule's order
1. **Rows and measure, from the notes only.**
   - The data files' md5 sums were checked against `origin/main`.
   - The clip median of r is 4.3234; the chair's figure was 4.323.
   - Every one of the 21,998 clips has a defined r.
   - There are **9,574 songs from 1,741 artists**, after dropping 14 songs that have no rhythm clip. All three numbers match the chair's.
   - The beats-per-bar dummies count 354 / 456 / 167, matching the chair's.
2. **Gate (before any outcome was read): passed.**
   - **Clip-to-clip:** Spearman of clip 1 vs clip 2 is **0.278** on 4,263 pairs. It needed ≥ 0.20; the chair had 0.279 on 4,271 pairs.
     - Why the pair counts differ: I counted pairs over the 9,574 model songs, as the rule says. The chair's 4,271 is the count over move_extensive's 9,588 songs. Eight of the 14 dropped songs had 2+ clips. The result passes either way.
     - The residualised version, printed and deciding nothing, is 0.287 (chair 0.290).
   - **Overlap:** the largest |Spearman| between D and any of the 17 data-pack measures, `n_ch`, `beats`, clips per song and bpb is **+0.173**, with `mel_ic_mean`. The limit was 0.7; the chair had +0.17. For comparison: `ch_ic_mean` +0.075, `ch_rep` −0.030, density +0.052.
3. **Not an existing measure renamed (printed).**
   - Against the fields outside the gate list, no |Spearman| is above 0.16: `mel_ic_sd` +0.154, `long_rests_per_bar` −0.120.
   - All 27 existing song fields together explain only R² = 0.29 of z(D) within artist (linear fit).
   - So D is not a relabelled existing field.
4. **Power at the notes stage:**
   - Within-artist residual share of z(D) after the controls: 0.646.
   - SE bound: 0.518 pp.
   - Power at −0.8 pp and p < .01: 0.151.
   - All three match the chair's figures.
5. **Only then was the key set of `hooktheory_covers_discogs.json` read.** Nothing else in that file was used.
   - It has 3,080 keys. 311 of them are not among the surprise songs; that count is a diagnostic only.
   - Model rows: N = 9,574. 2,224 of them have y = 1 (23.2%).

## Numbers
All coefficients are in pp of P(in Discogs-VI) per SD.

| | Value |
|---|---|
| **Clustered SE (CR1, by artist)** | 0.344 pp |
| **Power at −0.8 pp, p < .01, from that SE** (printed before β) | **0.40** |
| **β, z(D), primary LPM** | **−0.161** |
| p (normal, two-sided) | 0.639 |
| 95% range | −0.835 to +0.513 |
| Half 0 (886 artists, 4,608 songs) | +0.437 (SE 0.460, p 0.34) |
| Half 1 (855 artists, 4,966 songs) | −0.741 (SE 0.510, p 0.15) |
| Conditional logit, z(D) (log-odds) | −0.026 (SE 0.047, p 0.57) |

- **Cross-checks:**
  - The CR1 code matches statsmodels `cov_type="cluster"` (df_correction=True) to 1e−8.
  - The conditional logit converged (statsmodels `ConditionalLogit`, exact likelihood, BFGS). Its max |score| is 0.03 on the summed log-likelihood, about 1e−5 per song.
- **Conditional-logit drops:** 1,271 artists and 5,925 songs, because all their songs are 0 or all are 1 (180 of those artists are all 1). It keeps 470 artists and 3,649 songs.
- **Why power is higher than the notes-side figure:** the clustered SE (0.344) came out below the notes-side bound (0.518). The bound assumed an outcome variance of 0.21·0.79, and the within-artist residual variance is smaller.

## Verdict, by the rule as written first
- **Pass?** No. β is negative but p = 0.64, far from .01. The halves split (+0.44 and −0.74). The conditional logit is negative.
- **Opposite sign?** No. β is not > 0.
- **Kill?** **Yes.** β = −0.16 > −0.3.

**Verdict: KILL.**

## How firm
- **The kill is firm by the rule:** the point estimate is about half the kill line from zero, and nothing is close to significant.
- **The data do not cleanly rule out the predicted size, though.**
  - The 95% range (−0.84 to +0.51) only just reaches −0.8.
  - Tested against −0.8 itself, z = −1.86 (two-sided p ≈ 0.06).
  - With power of 0.40, a true −0.8 pp effect would often have come out like this.
- **What is clear:** there is no sign of the effect at the size predicted, and the halves disagree in sign.
- **What is less clear:** whether a small negative effect, under 0.8 pp, exists.

## Reported, deciding nothing
The rule lists these runs in advance. None of them affects the verdict.

1. **β of z(D) with `ch_rep` and `ch_ic_mean` added:** −0.154 (SE 0.346, p 0.66). D's null result does not depend on whether those surprise terms are held.
   - The coefficients on the added terms come from this model, not from move_extensive's model, which has other columns: `ch_rep` +1.25, `ch_ic_mean` −0.08.
2. **Signed ln r − ln 4.32 (z) in place of D:** −0.80 (SE 0.62, p 0.20). Its direction would mean songs with a faster-than-habitual rate are versioned a little less. That is a one-sided reading, not the two-sided "distance from habit" claim, and it is not significant.
3. **D from the melody term alone** (n_mel·mel_ic_mean / beats, measured from its own clip median of 3.109): −0.64 (SE 0.36, p 0.077).
4. **D from the chord term alone** (n_ch·ch_ic_mean / beats, measured from its own clip median of 1.055): +0.22 (SE 0.33, p 0.52).
   - For items 3 and 4 the rule named no reference point. I fixed each one at its own all-clip median in the script, before the outcome was read.
   - These are post-hoc views of where any trace of an effect might sit: slightly on the melody side. They are not tests, and the melody-only one would not clear p < .01.

## What it cannot say
- **Not a measured rate:** 4.32 is a median of the Hooktheory corpus, not a measured human information rate. The rate is per beat, not per second, because there is no tempo. Coupé et al. 2019 is the Inventor's analogy, recalled and not checked.
- **Built from surprise:** D is made from two surprise means. That is why the run with `ch_rep` and `ch_ic_mean` added is printed.
- **Weak outcome:** the outcome is documented versioning in Discogs-VI, not lasting love. A non-match is not a true negative, because of missing credits, retitles and failed matches. Noise like that weakens effects, which makes a null weak evidence.
- **No era control:** era is held only through the artist fixed effect. Changes across a career are not held.
- **Limited power:** 0.40 at the predicted size. A null does not clear a small effect.
- **No cause; hits only.**
- **McGill:** the McGill hold-out was not touched. No song 59, `songs/p69` or `studies/holdout59` file was read.

## Data credit
Hooktheory data via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI (CC BY-SA 4.0).
