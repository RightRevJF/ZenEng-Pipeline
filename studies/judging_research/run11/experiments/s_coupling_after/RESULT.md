# s_coupling_after: Jason's S = 1 + g/π, g as the coupling of the song's outer voices

**Verdict: KILLED** by the rule written first (344be9b, pushed before the outcome was joined). This was the one more, novel attempt Jason asked for on 28 November 2026; written after seeing run 11's results, so it is not in K.

## What was predicted
Songs whose melody line and bass line move against each other over whole songs (g below 0, contrary motion) are more often taken up by another artist: **β = −0.03** SD per SD, within artist. Killed if −0.03 lies outside the 95% range.

## What came out (`result.json`)
- **β = +0.017** (SE 0.017), 95% range −0.016 to +0.050, p 0.30; 4,853 songs, 1,449 artists; 41.8% taken up by another artist.
- Halves: +0.014 and +0.020 (both the wrong way).
- Conditional logit: the frozen code passed the artist groups as a list, which statsmodels refused, so the column came back empty. Rerun of that column alone after the result (`logit_fix.py`, `logit_fix.json`; year bins left out there, since they made the fit singular): +0.048 (SE 0.046), the wrong way too. It cannot change the verdict: the kill rule does not use it.
- −0.03 lies outside the range, so the prediction is killed: if outer-voice coupling matters at all, it is smaller than predicted and, if anything, the other way.

## Readings (decide nothing)
| Reading | β | SE | p | Predicted sign |
|---|---|---|---|---|
| |g| (coupling strength) | +0.026 | 0.015 | 0.087 | + |
| g, one bar | +0.016 | 0.017 | 0.34 | − |
| g, two bars | +0.019 | 0.017 | 0.26 | − |
| g, four bars | +0.013 | 0.017 | 0.42 | − |
| g, holding ch_rep and run 07's gap | +0.018 | 0.017 | 0.29 | − |
| S_MEL (the melody's DFA exponent) | −0.026 | 0.014 | 0.069 | + |
| −|S_MEL − 1| (nearness to criticality) | +0.020 | 0.013 | 0.13 | + |

None reaches .05. The strength reading and the criticality reading lean their predicted ways; the exponent itself leans the other way. These are readings on seen songs and settle nothing.

## The formula's own identity (notes only, `gates.json`, seen before the rule)
With g measured directly as this coupling, π(S − 1) of the melody does not track it: Spearman 0.006 over 4,853 songs. Median S of the melody 1.04 (close to criticality, as the shape study found); median g +0.036.

## Gates and power
Stability between two different MIDI files of the same song: Spearman 0.45 (187 pairs; bar 0.20). Largest overlap with run 07's measures |ρ| 0.05. Power before the join: 0.23 at α .05 (fake SE 0.021); the real SE came out 0.017, smaller, as R11-4 says.

## How firm, and what it cannot say
Firm as a kill of this prediction on these songs: a contrary-motion effect of −0.03 is ruled out. It cannot say that outer-voice coupling never matters: the melody line here is a skyline over the arrangement (not always the sung tune), the songs were joined to other measures in run 07, and the outcome is uptake by another artist, not lasting love.

Credit: Lakh MIDI Dataset (Raffel 2016) and the Lakh Pianoroll Dataset (Dong et al. 2018), CC BY 4.0; Million Song Dataset names via Gold-Caps (CC BY 4.0); Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
