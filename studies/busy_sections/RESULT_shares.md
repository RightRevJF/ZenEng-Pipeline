# The verse sung closer, by kept shares (the trial of 749.153): result

25 November 2026. Form and checks frozen in `PREDICTION_shares.md` (486ecff) before anything was run. A thousand builds a song, form off against form on (`trial_shares.py`; figures in `shares_trial/`).

**The trial fails. The form stays off, and by the rule no other variant is tried in this window.**

| The builds' middle (off; shares; and 958, "apart", for comparison) | Song 55 | Song 54 | Song 58 | Song 49 |
|---|---|---|---|---|
| Words' fit | 0.265; 0.253; 0.253 | 0.221; **0.198**; 0.193 | 0.306; 0.302; 0.320 | 0.264; **0.215**; 0.224 |
| Rhythm scaling | 0.592; 0.622; 0.678 | 0.576; 0.601; 0.620 | 0.555; 0.583; 0.592 | 0.594; 0.634; 0.636 |
| Bars with nothing sung | 0.144; 0.136; 0.184 | 0.067; 0.092; 0.087 | 0.097; 0.112; 0.096 | 0.094; 0.168; 0.152 |
| Verse over chorus, notes a bar | 1.01; 1.12; 1.17 | 0.99; 1.09; 1.12 | 0.92; 1.07; 1.11 | 1.19; **1.53**; 1.58 |
| Builds that live | 342; 336; 281 | 309; 330; 304 | 419; 383; 405 | 344; 350; 356 |
| Range (the floor) | 15; 15; 15 (14.6) | 15; 17; 15 (15.4) | 17; 17; 17 (16.6) | 15; 15; 14 (14.6) |
| Lines given one bar, a verse | 1, 1, 2 | 1, 1, 1, 1 | 2, 2, 2 | 1, 2 |

| The chosen tune (off; shares) | Song 55 | Song 54 | Song 58 | Song 49 |
|---|---|---|---|---|
| Words' fit | 0.341; **0.301** | 0.275; **0.199** | 0.307; 0.339 | 0.326; 0.343 |
| Rhythm scaling | 0.601; 0.621 | 0.570; 0.639 | 0.574; 0.564 | 0.612; 0.630 |

**The checks.**
1. Builds' words' fit within 0.02 of form off, in each song: **fails** in song 54 (−0.023) and song 49 (−0.049).
2. Chosen tune's words' fit within 0.02, songs 55, 54, 58: **fails** in song 55 (−0.040) and song 54 (−0.076).
3. The verse lines not given one bar, within 0.02, songs 54 and 49: **fails** in song 54 (0.252 to 0.202); holds in song 49 (0.137 to 0.140).
4. Rhythm scaling higher in three songs of four: holds in all four.
5. Soundness and the rest: the three chosen tunes are sound with no lean; builds live; the floor and the ceiling are kept. **The guard fails in song 49:** its verse runs 1.53 times its chorus, past the kept 90th (1.48). It stands at 1.19 with the form off, because its verse lines are longer than its chorus's to begin with. (Song 54's builds' middle range is under its floor with the form off, 15 against 15.4; the form does not cause that.)
6. Song 50: **not run.** The trial had already failed on the seen songs, so running the hold-out could change nothing and would spend it. It is still sealed; its lyric file is made and nothing of the engine has touched it.

**Against what I expected.** I expected about half of 958's gain in rhythm scaling and less than half of its cost in words' fit, and gave the checks an even chance. The gain is about half (0.03 against 0.02 to 0.09). The cost is not less: song 49 loses 0.049 with three lines taken, where 958 took four and cost 0.040. The cost in words' fit does not shrink with the number of lines taken.

## 749.154: where the fall is

Read in the builds, line by line (each line's fit is a rank correlation within the line; means over every living build):

| Mean line fit (off; shares; 958) | Song 54 | Song 49 |
|---|---|---|
| Lines the form gives one bar | 0.404; 0.395; 0.383 | 0.247; **0.334**; 0.330 |
| The other verse lines | 0.252; 0.202; 0.231 | 0.137; 0.140; 0.131 |
| The rest of the song | 0.138; 0.177; 0.133 | 0.338; 0.321; 0.332 |

(Lines named as the shares form names them. Under 958's naming: song 49's untouched verse lines 0.141 off, 0.127 under 958.)

- **Song 49's untouched verse lines do not fall in the builds** (0.137 to 0.140; under 958, 0.141 to 0.127). The fall Review 30 read on the two chosen tunes (0.536 to 0.068) was the draw of one tune, not the form.
- **In song 49 the lines given one bar fit their words better, read within the line** (0.247 to 0.334), and yet the song's whole fit falls by 0.049. So the fall is not inside any group of lines. The whole fit is one rank correlation over every note of the song, and it ranks note lengths across lines: a line sung in one bar has all its notes short, so its weighty syllables rank short against the rest of the song even when each stands out in its own line. That is my reading of the figures, not yet a test.
- Song 54 does not agree so cleanly: its untouched verse lines fall under the shares form (0.252 to 0.202) and less under 958 (0.259 to 0.240).

**What this suggests, to be ruled on and not built here.** The check that keeps failing may be reading pace between lines as misfit within them. Whether the whole fit or the line-by-line fit is the truer reading is a question for the kept songs: do kept songs whose sections differ in pace have a lower whole fit at the same line-by-line fit? Rule first, in a later window. Until then the form is off and stays off.
