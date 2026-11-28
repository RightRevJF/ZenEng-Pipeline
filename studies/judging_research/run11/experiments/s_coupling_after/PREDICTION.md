# s_coupling_after: Jason's S = 1 + g/π, with g read as a coupling (one more, novel attempt)

Run 11, 28 November 2026. **Written after seeing this pass's results**, at Jason's request ("Eliminate my formula from consideration only after one more, novel attempt"). Not in K: a pass is a lead to be confirmed on songs never used; a kill is the attempt failing. The outcome has not been joined.

## Why this form is new
The formula, as the shape study on main states it: a system's scaling exponent S sits at 1 (criticality) plus a coupling g over π. Every test so far read S as an exponent (studies/shape, DFA of the pitch series, across songs) or replaced g by a spectral gap (runs 02, 07, 10, 11). None measured **g as a coupling**. Here g is the coupling between the song's two outer voices: the melody line and the bass line, over whole songs.

## Measure (frozen; `test.py`, key `G_COUP`)
Lakh Pianoroll Dataset (LPD-5 cleansed, CC BY 4.0), whole songs. Melody line = the highest sounding pitch over piano, guitar and strings at each eighth note (the skyline); bass line = the lowest sounding pitch of the bass track; gaps hold the last pitch. g = ρ_DCCA (detrended cross-correlation coefficient, Zebende 2011) between the two lines, averaged over box sizes of one, two and four bars; S_C = 1 + g/π. Files need 32 bars. Song value = mean over the song's MIDI files.

Measure-side gates, notes only (`gates.json`, computed before this rule): stability between two different MIDI files of the same song, Spearman **0.45** (187 pairs; bar 0.20); largest overlap with run 07's measures |ρ| 0.05 (bar 0.70). Passes. Also seen before this rule, notes only: the formula's own identity does not hold with this g: π(S_MEL − 1), from the melody's DFA exponent, is unrelated to g (Spearman 0.006); median S_MEL 1.04; median g +0.036; 40% of songs have g below 0.

## Songs
Run 07's within-artist Lakh songs (`data/lakh_songs_discogs_run07.json`) with a value, by artists with two or more such songs: **4,853 songs, 1,449 artists**. SEEN: joined in run 07 to y_foreign and eight chord measures (including run 07's spectral gap `g`, killed); never to this measure.

## Outcome and model
y_foreign (taken up by another artist; run 07's rule, from the committed table). OLS of z(y_foreign) on z(G_COUP), artist fixed effects, run 07's controls (ln_chg, V, ln_bars, five-year bins of the MSD year), CR1 by artist. Halves: md5 of the artist key. Second model: conditional logit, sign.

## Prediction
**β = −0.03**: songs whose outer voices move against each other (contrary motion, g below 0; the oldest rule of good counterpoint) are more often taken up by other artists.

## Rule
- **Lead passed:** p < .05, negative, both halves negative, conditional logit negative.
- **Killed:** −0.03 outside β ± 1.96 SE. This ends the attempt.
- **Unsettled:** otherwise. Said now: an unsettled result does not decide; whether the formula is then dropped is Jason's call.
- Power (fake outcomes, iid noise, before the join; `power.json`): **0.23** at α .05 (fake SE 0.021); chance of a kill if the true effect is zero 0.22 at that SE. The real SE is likely smaller (R11-4), so both are understated.

## Readings (decide nothing)
|g| (coupling strength, sign +); g at one, two and four bars (−); g holding ch_rep and run 07's gap (−); S_MEL, the melody's DFA exponent (+); nearness of S_MEL to 1, −|S_MEL − 1| (+, the criticality reading, within artist).

## How to run
`python3 test.py run` (refuses unless this file, test.py, spec.json and common11.py are pushed).
