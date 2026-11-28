# Run 12: first principles

28 November 2026. Recommendations only; nothing is dropped without Jason.

## 1. Bedrock
**Facts.**
- K = 4 (three frozen, one after seeing), α .0125. Nothing passed.
- **Killed:** PI3c (predictive information, Lakh): −0.011; its range stops at +0.0296, just short of the predicted +0.03.
- **Unsettled:** v1_rep −0.012 (p .11, the predicted size); PIC on clips +0.015 (p .23, half the prediction).
- **Covers show no rich-get-richer.** The frozen fitness model let a song's own covers raise its later rate; the data set that term to nothing (A → ∞). So FIT is covers per year of opportunity, shrunk for small numbers: 0.985 with log covers, first year held. "Fitness beats counts" was arithmetic.
- **Windows:** on Hooktheory, chord repetition went with fewer *late* covers (Δ −0.24, analytic SE 0.072; frozen bootstrap failed). On Lakh, rule first: +0.006 (SE 0.097). Not reproduced.
- **Estimates:** REP on Lakh −0.022 (SE 0.021), run 11's sign; ROUGH_X +0.015, wrong sign.
- **CANAL pilot:** arrangers agreeing on pitch content agree on melody spread (H1 0.52, E5 0.50), and on voicing roughness too (0.34; P3 false).

**Assumptions.** A Discogs year dates a coverer's choice; one ageing curve fits every song; within-artist removes fame; a MIDI skyline stands for the melody.

## 2. Question every requirement
- **Yardstick.** Love is still unused. Covers now reduce to one steady rate per song; "lasting" adds only through windows, which are underpowered. Flag.
- **Notes only.** Main's sound study held 0.08 on a second store; notes give 0.02 to 0.04. Keep; know the ceiling.
- **Hits only.** Card 2: hits are the early lottery's winners; that selection might hide rich-get-richer (speculation). Flag.
- **Fitness estimator.** It separates luck from appeal only by timing within a song, resting on Discogs dates and seven age bins. It cannot see a launch boost. Flag.
- **Power floor.** Run 11's fix overshot: realised SEs exceeded fake ones (v1_rep 0.0073 vs 0.0055; PI3c 0.0207 vs 0.0168; windows about 3×). Flag: calibrate on last pass's realised SEs.
- **K counting.** An after-seeing test joined K; PIC was counted against its author's withdrawal. Neither is a written rule. Seen songs are still counted per pass, not per project. Flag.
- **Kill rule.** PI3c died by 0.0004: "killed" means "+0.03 is unlikely", not "zero".

## 3. Delete (recommended)
- **PI3c:** killed; every sign wrong.
- **The rich-get-richer term (A):** the data refused it.
- **The V1 horse race (FIT against counts):** they cannot differ when A → ∞.
- **FIFTHS (E5):** stopped at its overlap gate (ρ −0.71 with REP).
- **CANAL's P3 (voicing is the arranger's):** false; agreeing pairs may share a source file.
- **Roughness (vector 4):** not failed, but undecidable and wrong-signed. Park until recordings exist.

## 4. Simplify
Within one artist, melodies spending their time on fewer pitch classes are covered more often *for their age and era*. Outcome: covers divided by those expected for that age and era. Plainest twin: the count of pitch classes.

## 5. Speed the loop
**Prediction, first.** On melodies never joined to an outcome, within artist: REP **−0.02** per SD on the age-adjusted cover rate. Killed if −0.02 lies outside the 95% range.

**Data.** New named melodies linked to Discogs-VI, about 11,000 within-artist songs for power 0.5 (run 11's scaling). **It cannot run this pass without re-spending:** every Hooktheory and within-artist Lakh song with covers has met REP.

**Free now, no notes touched.** Refit fitness.py with finer age bins; prediction: the likelihood still rises with A.

## 6. The obstacle and the way through
**Obstacle.** Covers behave like one steady appeal per song; the notes explain a sliver of it, and the allowed named melodies are spent.

**Way through (speculation).**
- Each cover is nearly an independent vote, so more songs per artist buys more than more covers per song.
- Vector 3: request recordings aligned to notes; sound carried 0.08 to 0.2 on main.
- Vector 5, done properly: compare an original's notes with transcriptions of its covers. What coverers keep is the invariant, with no shared source file.

> **For Jason: "no rich-get-richer in cover timing"**
>
> Two 1975 songs by one writer. By 1980 Song A has 10 covers, Song B 2.
>
> - *Rich-get-richer* would mean covers breed covers: A's yearly rate climbs as its pile grows, and B falls further behind even if equal underneath.
> - *What the data showed:* A simply has more pull. Allowing for age and era, it keeps earning about two a year, B about one every two or three years, however many each already has.
>
> So past covers show how appealing a song is; they do not cause the next one. "Fitness" is just covers per year of opportunity, small numbers shrunk toward the average.
