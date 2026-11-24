# The thirds axis |a₃|/a₀: result

Run 04, 24 November 2026. The rule is `PREDICTION.md` in this folder, frozen at commit 00ab557 before this script was written. The script is `test.py` and the numbers are in `result.json`. It runs in about 10 seconds. It reads the data from `origin/main:studies/judging_data/`, which is byte-for-byte the same data run 03 used. The McGill hold-out was not touched.

## Verdict: both killed

**β = +0.006** (SE 0.017, p = 0.73). That falls inside the frozen band from −0.01 to +0.01, so under the three-way rule **both readings are killed**. G3 said more thirds-axis weight goes with more covers. I1 said less goes with more covers.

## What was predicted

- **G3 (Geometer):** β = +0.02 SD of log(1 + covers) per SD of D3, within an artist's own songs.
- **I1 (Inventor):** β = −0.025.
- The test was two-sided and counted once, with p < .01 (that is, .05 / 5).

## The measure in plain words, with a worked example

Every chord is a set of notes. Lay the 12 notes on a small clock with only four positions. C, E and G♯ share one position, and C♯, F and A share the next. In general, notes a major third apart land on the same spot. Each chord then becomes an arrow on that clock, and a song's arrows are added up, weighted by how long each chord sounds. D3 is the length of the summed arrow divided by the total amount of sounding notes. It runs from 0, where everything cancels, to about 0.75, which is one major triad held throughout. Because it is a length and not a direction, it does not change when the song is played in another key. A cover's change of key leaves it alone.

Two rules follow from the clock:

- **Chords a major third apart add.** C major and E major point the same way. C–E, alternating, scores 0.745, exactly the same as C held alone.
- **Chords a whole step apart cancel.** F major and G major point in exactly opposite directions. IV–V scores 0, and so does ♭VII–I.

In C, with one beat per chord:

| Chord | Arrow (a₃) |
|---|---|
| I (C) | 2 + 1i |
| vi (Am) | 2 − 1i |
| IV (F) | 1 − 2i |
| V (G) | −1 + 2i |

| Progression | Sum of arrows | Length \|a₃\| | Total notes a₀ | D3 |
|---|---|---|---|---|
| I–IV–V–I | 4 + 2i | 4.47 | 12 | **0.373** |
| I–vi–IV–V | 4 + 0i | 4.00 | 12 | **0.333** |
| I–III | 4 + 2i | 4.47 | 6 | 0.745 |
| IV–V | 0 | 0 | 6 | 0 |

In I–IV–V–I, IV and V wipe each other out, and what is left is the two beats of I. In I–vi–IV–V, IV and V again wipe out, and I plus vi leaves a shorter arrow because the two chords lean opposite ways. The script reproduces all six unit values on the card: 0.745, 0.667, 0.333, 0.248, 0.111 and 0. D3 was also unchanged, to 1e-9, on three random clips that were transposed by 5 and inverted.

## Steps, in the frozen order

1. **The measure, built on the notes only.** There were 2,672 songs with 3 or more distinct chords, and none had an undefined D3. The 10th, 50th and 90th percentiles were 0.153, 0.302 and 0.469, matching the chair exactly.
2. **Gate: passed.**
   - Clip 1 against clip 2: Spearman 0.318 on 1,281 pairs. It needed at least 0.20, and the chair had 0.318.
   - Overlap: the largest |ρ| was 0.250, with `ch_ic_mean` (it needed at most 0.7). Distinct chords gave −0.226 and links −0.207.
3. **Not an existing measure renamed.** No single existing measure comes near 0.7. Together, the 17 data-pack measures and the size block explain R² = 0.135 of D3. Adding FP, PLR and TS raises that to 0.385, so most of D3 is new. The Spearman correlations with TS (−0.34), PLR (+0.26) and FP (+0.04) are printed only and decide nothing.
4. **Notes-side power,** printed before the outcome file was opened. This used 1,924 songs from 420 artists. The residual share was 0.643 for D3 and 0.679 for FP. That gives SE ≈ 0.0185, and power at +0.02 with p < .01 of **0.068** (0.19 at p < .05). This is far below the proposed 0.5 floor, which is printed and does not block.
5. **Outcome joined.** All 2,672 songs have a first year, leaving 1,924 songs from 420 artists with 2 or more songs. Run 03 had the same counts.

## Result

| | |
|---|---|
| Realised SE, printed before β | 0.0172 |
| Power at +0.02, p < .01 | **0.079** (power at I1's −0.025: 0.13) |
| **β(D3)** | **+0.0060** |
| SE | 0.0172 |
| p | 0.727 |
| 95% range | −0.028 to +0.040 |
| Artist half 0 (932 songs, 205 artists) | +0.0097 (p 0.65) |
| Artist half 1 (992 songs, 215 artists) | +0.0016 (p 0.95) |

These are the rule's checks, in order:

- G3 passes? No, p ≥ .01.
- I1 passes? No, β > 0.
- Is −0.01 < β < +0.01? Yes, so **both killed**.

The control measures behave as in run 03: `ch_rep` β = −0.062 and `ch_ic_mean` β = −0.085, both with p < .001.

## How firm

The verdict is firm as a rule: β landed in the kill band, and both halves agree it is small and positive. It is **weak as evidence**. The 95% range, −0.028 to +0.040, still includes both predicted sizes, +0.02 and −0.025. With power near 0.08, this test could not have told a true +0.02 from zero. What it shows is that, on these songs, the thirds axis is not a large signal. Effects of the size anyone predicted are not ruled out.

## Reported, deciding nothing

- **Covers within 5 years of `first_year`:** β = −0.001 (SE 0.018, p 0.95).
- **Covers more than 10 years after `first_year`:** β = +0.005 (SE 0.016, p 0.78).
- **β without `ch_ic_mean`:** +0.016 (SE 0.018, p 0.37). It rises because D3 and `ch_ic_mean` overlap (ρ −0.25), and `ch_ic_mean` carries a strong negative link to covers.
- **β with PLR added:** +0.004 (SE 0.019, p 0.83). Only D3's coefficient is reported here. PLR's own coefficient belongs to the `plr_share` test.
- **Share of songs with D3 below 0.05** (near whole-step cancellation): 1.1% of the 1,924 model songs, and 1.2% of all 2,672.
- Median covers, all / within 5 years / after 10 years: 7 / 1 / 3.

## What it cannot say

- **Not fresh.** These are run 03's songs, and their covers have been looked at many times. Only the measure is new.
- **What D3 counts.** It adds up chord time and ignores order. IV–V cancels whether or not a tonic follows. Neither G3's "shared tones, easy to reharmonise" story nor I1's "balanced regions" story is measured directly; only the sign could have been.
- **Low power.** A null here does not clear an effect of +0.02 or −0.025.
- **No cause; hits only.** Songs that were never matched to Discogs-VI are not in the data.
- **McGill.** The hold-out was untouched, and nothing qualifies to go against it.

## Data credits

Chord and melody data: Hooktheory, via Sheet Sage (CC BY-NC-SA 3.0). Cover versions: Discogs-VI (CC BY-SA 4.0).
