# The bridge's ceiling: the trial's result (27 Nov 2026). Missed on the pools. Not built.

Marks: `PREDICTION_trial.md` (commit 15229c9, before the run). Figures: `trial.json` (`N=300 python3 studies/section_ceiling/trial_read.py ON OFF`; the written records are outside the repository). `LUTHIER_BRIDGE_CEILING=1`; songs 58, 49, 50, 59, 61, 66 written through; song 66 also with the switch off, as its v53.

| | 58 | 49 | 50 | 59 (read only) | 61 | 66 |
|---|---|---|---|---|---|---|
| Pool, v53; trial | 20; 16 | 12; **7** | 5; **3** | 21; **15** | 22; **8** | 33; **9** |
| Trial's pool over v53's | 0.80 | 0.58 | 0.60 | 0.71 | 0.36 | 0.27 |
| Chosen tune's bridge, v53; trial | 0.284; 0.284 | 0.349; 0.349 | 0.367; 0.367 | 0.460; 0.460 | 0.755; 0.245 | 0.538; 0.450 |
| Chosen tune, the same as v53's | yes | yes | yes | yes | no | no (key Dm to Bm) |
| Verse, v53; trial | 0.310; same | 0.423; same | 0.418; same | 0.335; same | 0.323; 0.396 | 0.430; 0.294 |
| Chorus, v53; trial | 0.286; same | 0.360; same | 0.365; same | 0.321; same | 0.345; 0.233 | 0.342; 0.241 |
| Chosen tune's words' fit, v53; trial | 0.372; same | 0.338; same | 0.209; same | 0.228; same | 0.295; 0.329 | 0.308; 0.321 |
| Range (floor) | 17 (16.6) | 16 (14.6) | 17 (14.6) | 19 (15.5) | 19 (15.5) | 17 (16.0) |
| Living builds; builds' fit, pitch scaling, surprise | the same in every song, as said beforehand: the gate changes no build |

## By the marks
- **W3 missed.** The pool is under 0.8 of v53's in five songs of six, and newly under 10 in three (49: 12 to 7; 61: 22 to 8; 66: 33 to 9). Song 50's falls from 5 to 3.
- **W5 met.** Every chosen tune's bridge is under 0.481; songs 61 and 66 come back under it (0.245 and 0.450).
- **W2 met.** The waiver was used in none.
- **W4 met.** Words' fit no lower anywhere; every floor kept.
- **W6 met.** Every verse and chorus under 956's lines; in the two songs whose tune changed, three of four readings are lower and song 61's verse is higher (0.323 to 0.396).
- **W7 met by construction** (no build changes).
- **W1 not read.** `studies/soundness/neighbour.py` makes its own pool and its ceiling code does not know the bridge, so its run with the switch on gave v53's figures to the last digit. It said nothing and its file is not kept. With W3 missed I did not mend the study to read it.
- **Byte for byte met.** Switch off, songs 54 and 55 are v53's records.

## What it says
The gate does what it is for, and costs more pool than the marks allow, because the engine's bridges are over the kept line too often for a gate to be cheap (21 to 82 builds in 100, `read.json`). A gate is the wrong tool where the fault is this common: the builds themselves want mending. I expected a miss on the pools (one chance in three of passing); it missed more widely than I guessed.

## Not built
The switch stays in the code, off. The finding stands: bridges sit on one pitch more than kept bridges do, and two delivered songs (61, 66) are over the kept 90th.

## A next step, if wanted (a reading, nothing built)
Why a bridge build sits on one note: which lines of the bridge carry the commonest pitch (fresh, copied, sung again), how wide the bridge's register is against the verse's and chorus's, and how many chords it has under it. Rule first. If one cause carries most of it, a form at the draw could be tried, which would cost no pool.
