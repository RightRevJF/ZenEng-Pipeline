# Does the tune move less than the chords under it? Result

Run 03, 23 November 2026. The rule was frozen before any outcome was opened (`PREDICTION.md`, commit 09ce7bd). `test.py` ran it once, as written. The numbers are in `result.json`.

## Verdict: **stopped**. No outcome was joined.

The rule had a gate that the measure had to pass before any cover count was looked at. One part of it failed, so the test ended there. The script never opened `first_year`, the cover counts or the versions file.

## The gate
- **Do two clips of the same song agree?** For each song with two or more transcribed clips, the measure was worked out on clip 1 alone and on clip 2 alone. The rule needed these to agree with a Spearman correlation of at least **0.20**. They agreed at **0.1947** (1,277 songs). The chair expected 0.195. That is a fail, narrowly. Under the rule there is no rounding up.
- **Is it just another measure under a new name?** This part passed. The largest overlap with the 17 covers-study measures, distinct chords, links and clips was 0.175 (`length_variety`). The rule allowed up to 0.7.

When two clips of one song give such different readings, the measure is mostly noise about the song. That is why the rule stops here rather than testing it against covers.

## Checks on the measure (notes only)
- **Songs:** 2,672 with at least 3 chords, as the chair found. 3 had no usable chord change and were dropped (chair: 3).
- **Spread of the measure:** 10th / 50th / 90th percentile +0.18 / +0.88 / +1.55 semitones, matching the chair. In almost every song the tune moves more than its chords.
- **Absolute pitch:** 70.8% of melody time falls on the sounding chord's notes (chair 70.5%).
- **Size:** song size explains R² 0.019 of the measure (chair 0.02).
- **The distance formula:** it reproduced both checks in the rule (C to F♯ = 6, C major to G major = 1). It also matched an exact solver on 200 random cases.
- **One count differs.** 88.6% of chord changes were kept (53,660 of 60,579), against the chair's 81%. The measure's spread matches the chair's to two decimals, so the measure itself agrees. The chair's count probably used a different total. It does not touch the gate.

## Idea for later (not tried)
A tune measure that needs one value per song might be steadier if it pooled more clips. A version that also used octave and contour might be steadier too. Either would need its own rule, frozen first, and fresh songs.

## Data credit
- **Notes and chords:** Hooktheory, via Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022). CC BY-NC-SA 3.0.
- **Covers and versions** (not opened for this test): Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024). CC BY-SA 4.0.
