# Share of P/L/R moves on Amiot's torus of phases: frozen before any outcome is joined

Run 04, 24 November 2026, by the chair. **One hypothesis (R04-G2, merged with R04-L2).** No cover count, version, release, `first_year`, versions file or `covers.json` has been opened. "Chair" = notes-only checks on the 2,672 songs of `hooktheory_clips.json.gz` with 3 or more distinct chords. **Run 04 does not touch the McGill hold-out.**

## Claim (Geometer G2 with Listener L2; Amiot, Definition 1 and his triad table)
- **The mathematics:** on the flat (φ₃, φ₅) torus, a major or minor triad's three nearest triads (distance ≤ 1.229; the next is 1.656) are exactly its P, L and R relatives. These are the two-common-tone moves any arranger can revoice.
- **Extrapolation:** within an artist's own songs, **a larger share of P/L/R moves goes with more covers.**
- **Merge:** the mean torus step (TS, L2) is the near-complement (ρ −0.70) and is reported only. The Geometer and the Skeptic both say the a priori case is weak: I–IV–V–I has no P/L/R move.

## Rows, token, merging, wrap and model
These are exactly as `run03/experiments/fifths_path/PREDICTION.md` and `run03/experiments/bridge/PREDICTION.md`:
- the same chord token and merging of consecutive equal tokens, with the wrap move last → first when the tokens differ;
- data-pack measures weighted by `n_mel`;
- the `within()` model, CR1 clustered SE, and md5 artist halves.

**One change:** the gate's song list is taken from the notes, not from the outcome file. It is the `video` values of `hooktheory_clips.json.gz`, which by construction are the songs matched to Discogs-VI. A song's clips are its records in the clips file that are also a `k` in the surprise and rhythm files, in surprise-file order. Keep songs with at least 3 distinct tokens pooled.

Only after the gate passes, read `hooktheory_covers_discogs.json` for `covers` and `first_year`. Keep songs with a truthy `first_year`, then artists with 2 or more songs. *Chair, before the first-year filter: 2,672 songs; 1,924 songs in 420 artists with 2+ songs (run 03's model had 1,924 and 420).* Songs with an undefined PLR are dropped before the artist rule (chair: none).

## Measure (frozen)
- **Chord point:** for each merged run, take the pitch-class set S of its first event, relative to the clip's tonic (as FP). Then a₃ = Σ_{k∈S} e^{−2πi·3k/12} and a₅ = Σ_{k∈S} e^{−2πi·5k/12}. φ₃ = `numpy.angle(a₃)`, undefined if |a₃| < 1e-6; φ₅ likewise.
- **Moves:** run 03's moves, i.e. consecutive runs plus the wrap when the tokens differ.
  - Skip a move, and count it, if any of the four phases is undefined. *Chair: 1,801 of 60,579.*
  - Step s = √(w(Δφ₃)² + w(Δφ₅)²), where w(x) = ((x + π) mod 2π) − π. The half-turn ambiguity (card 1; the brainstorm) changes a sign, never a length.
  - Skip a move, and count it, if s < 1e-9. This is the same pitch-class set under two tokens, not a chord change. *Chair: 37.*
- **P/L/R move:** s < 1.25.
- **PLR** = the number of P/L/R moves divided by the number of kept moves, pooled over all of the song's clips. *Chair: 10th / 50th / 90th percentile 0.00 / 0.22 / 0.50.*
- **TS** = the mean of the kept s (reported only).
- **Unit values (must reproduce):** d(C,Am) 1.065; d(C,Cm) = d(C,Em) 1.229; d(C,F) = d(C,G) 1.656; d(C,Fm) 1.824; d(Cm,D) 3.26. Among the 24 major and minor triads, exactly 36 pairs have s < 1.25, and the same 36 pairs fall below the cut with φ₅ stretched by 0.7365. Loops with one beat per chord:

| Loop | PLR | TS |
|---|---|---|
| I–V–vi–IV | 0.25 | 1.760 |
| I–IV–V | 0 | 2.208 |
| I–vi | 1 | 1.065 |
| IV–V | 0 | 3.312 |
| I–iii–vi–IV | 0.50 | 1.442 |

## Gate (before any outcome-side field; failing either records "stopped" and no outcome is joined)
1. **Clip-to-clip:** clip-level PLR (that clip's kept moves; both clips defined), clip 1 vs clip 2, Spearman **≥ 0.20**. *Chair: 0.349 (1,279 pairs).*
2. **Overlap:** |Spearman| **≤ 0.7** with each of the 17 data-pack measures, distinct chords, links and clips. *Chair: largest +0.14 (links).* Printed, deciding nothing: TS −0.70, FP −0.19, and D3 (thirds_axis) +0.26.

## Model columns (run 03's `within()`: y = log(1 + covers), all columns standardised, demeaned within artist, OLS with no constant, CR1 by artist)
PLR, `ch_rep`, `ch_ic_mean`, `first_year`, log(clips per song), distinct links, and dummies for distinct chords 4…11 and 12+ (3 is the reference). statsmodels is not installed, so use the CR1 formula of run 03's bridge PREDICTION.

## Prediction
**β = +0.02 SD of log(1 + covers) per SD of PLR**, within artist.

## Power (notes-side; printed again by the script from its SE before β)
- **Method:** run 03's within-artist SE scaling, which takes FP's realised SE of 0.018 on the same 1,924 songs and multiplies it by √(FP's residual share / PLR's residual share).
- **Residual shares:** after the artist fixed effect and the columns above (first year is unavailable notes-side), PLR 0.710 and FP 0.679.
- **SE ≈ 0.0176; power at +0.02, p < .01 two-sided: 0.075** (0.21 at p < .05). Power = Φ(0.02/SE − 2.5758) + Φ(−0.02/SE − 2.5758).
- **Power floor:** far below the proposed 0.5 floor (R03-4, undecided). Printed, not blocking. A kill is the likeliest informative result.

## Rules
**Tonight counts five hypotheses, so p < .05/5 = .01, two-sided.** The threshold does not move if a test is stopped.
- **Pass:** β > 0, p < .01, and β > 0 in both artist halves.
- **Opposite sign:** β < 0 and p < .01. The prediction is killed. This is reported as a new hypothesis ("long, every-voice-moves steps are what coverers take up"), not a pass.
- **Kill:** β < +0.01.
- **Unsettled:** anything else, including split halves.

## Reported, deciding nothing
- TS in place of PLR.
- Covers within 5 years and more than 10 years after `first_year` (as in run 03).
- β without `ch_ic_mean`.
- The skipped-move counts.
- The share of zero-PLR songs.

## What it cannot say
- **Not fresh:** these are run 03's songs, and their covers have been looked at many times. Only the measure is new, so a pass is a lead for unused songs.
- **Triad-based cut:** the 1.25 cut is exact for triads only. Seventh chords and other sets sit at other magnitudes, so the cut is a convention for them.
- **Low power; no cause; hits only.**
- **McGill:** the hold-out is untouched.
