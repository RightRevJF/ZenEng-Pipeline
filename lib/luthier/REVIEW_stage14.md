# Review 14: Luthier v27 (fixes 907–912)

Branch `luthier-v8-stage1` at 588535c, main merged in.

## Byte for byte

All five makers now run from the repo, `kept_plan.py` included (910), and each writes its table byte for byte: `4-4_pop_sung.json`, `kept_readings.json`, `kept_word_weight.json`, `kept_returns.json`, `kept_line_ends.json`, `register_plan.json`. The song reruns (54, 55, 58 and 52 by `song_from_lyric.py`; 52 and 53 by `metre_engine.py`; 53's hymn parts; stage 4) reproduce every committed record. `git status` is clean after them. `kept6a.json` is gone.

## 908, checked hardest: the words' fit gated at the builds' median

The code does what the README says. It gates on the whole fit and the fit by length, each at the builds' median, with the kept 10th as the floor, measured on each build's notes. `studies/kept_checks/place_in_gate.py` rebuilds each song's 1,000 builds, applies the engine's gates and reproduces all three picks (9935135dbac1, dcc3342024cd, 792d57d983db).

| Pick, as sung | 55 | 54 | 58 | kept 25th, median, 75th |
|---|---|---|---|---|
| fit, whole | 0.429 | 0.303 | 0.377 | 0.248, 0.318, 0.402 |
| by length | 0.336 | 0.218 | 0.191 | 0.118, 0.209, 0.297 |
| by place | 0.393 | 0.269 | 0.499 | 0.115, 0.242, 0.333 |
| by height | 0.111 | 0.024 | 0.067 | 0.045, 0.106, 0.178 |
| stressed syllables on a beat | 0.722 | 0.581 | 0.821 | 0.446, 0.542, 0.661 |

The fit by length is up in all three, as 749.85 asked. Three things go with it.

- **The gate measures the builds' notes, not the notes as sung.** Melismas come after the pick. Song 58's fit by length is 0.324 at the gate and 0.191 as sung, just under the kept median (749.91).
- **Place rides along.** The whole fit is the mean of length, place and height, and the builds already sit over the kept on place (song 58's builds: median 0.356 against the kept 0.242). Gating the whole fit at the builds' median pushes place further: song 58's pick reads 0.499 by place, past the kept 90th (0.412).
- **Song 58's 0.82 is not 908's doing.** Its pick is build 0, which passes with or without the median gate. Across the pool, 908 moves the median of stressed syllables on a beat by 0.01 to 0.03.

## 912, checked hardest: every kept rhythm

- The new path filters exactly as the old one did: the last onset by `end`, the first by `tmin`, and the early entries the same way. The cache is keyed on the line's syllable list, which the engine keeps for its whole run, plus bars and hook. The lead is read from the syllables, so the key is safe.
- A window is scored `log(c)` where it was `log(c + 1)`. A window seen once now scores 0 against log 2. That is a small lean toward commoner windows, and harmless.
- The draw is now over everything: 5,862 two-bar windows where the cut allowed 992. 61 in 100 of the kept lines' windows lie beyond the old sixty commonest, and 40 in 100 are windows seen only once. Bar rhythms: 1,688, where there were 400.
- Builds' onsets on the beat fall from 0.53 / 0.49 / 0.54 to 0.50 / 0.47 / 0.51 (kept quartiles 0.38, 0.45, 0.53). That is inside the kept middle half. Holds.
- What 912 exposes: **stressed** syllables on a beat stay high in the builds, with medians of 0.70 (58) and 0.65 (55) against the kept 0.54. Each window's score carries 879's place weight (1.5, times 1.4 in the window score) on every syllable. Fitted when twelve windows were on offer, it now picks the most stress-aligned windows out of hundreds (749.90).

## Question 2: gate on length and height only, leaving place out?

Yes. But leaving place out of the gate alone barely moves the picks, because the squareness is in the builds. With 908 as written, then with place left out:

| | 55 | 54 | 58 |
|---|---|---|---|
| builds' stressed on a beat, median | 0.658 | 0.585 | 0.706 |
| builds inside the kept middle half (0.446 to 0.661) | 0.51 | 0.87 | 0.27 |
| pool past 908: median; share in the kept middle half | 0.663; 0.48 | 0.603; 0.87 | 0.726; 0.10 |
| pool past length and height: median; share | 0.652; 0.54 | 0.585; 0.91 | 0.711; 0.16 |

Across the builds, the fit by place moves with stressed syllables on a beat (correlation 0.60, 0.71, 0.85): it is nearly the same reading. The fit by height runs under the kept (builds' medians 0.05 to 0.07 against 0.106), so gating it pulls toward the kept.

The place weight is what does it (`studies/kept_checks/place_weight_sweep.py`, 300 builds a setting):

| WORD_PLACE | 58: stressed on a beat; fit; by place | 55: the same |
|---|---|---|
| 1.5 (now) | 0.704; 0.361; 0.349 | 0.652; 0.334; 0.294 |
| 0.75 | 0.642; 0.337; 0.268 | 0.588; 0.308; 0.209 |
| 0 | 0.512; 0.254; 0.082 | 0.508; 0.262; 0.111 |

At 0.75 the builds' fit and fit by place meet the kept medians (0.318, 0.242), and stressed syllables on a beat come inside the kept middle half. With 0.75 and the gate on length and height, all 1,000 builds and the engine's own pick rule:

| Pick | 55 | 54 | 58 | kept middle half |
|---|---|---|---|---|
| stressed on a beat | 0.545 | 0.504 | 0.597 | 0.446 to 0.661 |
| fit, whole | 0.366 | 0.317 | 0.383 | 0.248 to 0.402 |
| by length | 0.414 | 0.257 | 0.348 | 0.118 to 0.297 |
| by place | 0.150 | 0.208 | 0.291 | 0.115 to 0.333 |
| by height | 0.081 | 0.131 | 0.171 | 0.045 to 0.178 |

These fits are on the builds' notes, before melismas. So the answer: gate on length and height, and halve the place weight.

## 907, 909, 910, 911

- **907.** The lift is drawn from the kept lifts the voice has room for, and `choose_key` puts the verse centre near the voice's middle. Holds. Song 58's title draws at about 0.99 of any sorted list, so it takes the top of its room again: lift 9, the chorus to E4, the top of the baritone. The key B needs capo 2 with A shapes. The verse centre is 2.5 from the middle as `choose_key` reads it (the upper median, before melismas) and 3.5 as sung.
- **909.** Phrases over 12 beats: 0.019 / 0.074 / 0.036 (kept 0.042); song 54 still over. Every remaining long phrase is two lines run together. The rule looks at the onset of a line's last note, so a line of 8 to 11 beats whose last note starts before beat 8 runs straight on (749.92).
- **910, 911.** Hold. ENTRY and the 731 floor are read from the kept table; 847 is recounted and stands; ONE_BAR is 0.09.

## Merged

`origin/luthier-v8-stage1` into main, no fast-forward.
