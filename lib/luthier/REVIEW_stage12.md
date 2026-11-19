# Review of Luthier v25: how a line ends (fixes 899 to 903), 18 November 2026

Branch `luthier-v8-stage1` at 43710c1 (main merged in). Merged into main at 9b149f6. The paper: `reports/Luthier_v25.docx` (read as Markdown in `src/`).

## Reruns (PYTHONHASHSEED=0)

| Command | Result | Held? |
|---|---|---|
| `make_kept_line_ends.py` | `tables/kept_line_ends.json` byte for byte | yes |
| `song_from_lyric.py` songs 58, 55, 54, 52 (1000 12) | records and logs identical | yes |
| song 52 and 53 hand specs, hymn parts, `stage4` | identical | yes |
| Every .py in lib/luthier compiles | yes | yes |

## 899, checked hardest: a line's last syllable and its rest drawn as a pair

How it works: the time to the next line (G) is set by the build (for a fresh line, drawn from the kept G where the slot leaves room); the last syllable's held length (D) is then drawn from the kept counts for its weight and that G, with D up to G (a line may run on). Where a cell has under 20 kept lines the weights are pooled. That is the joint draw 749.76 asked for.

What it gives (`studies/kept_checks/line_ends_engine.py`, `studies/breath/silences.py`, `studies/breath/phrases.py`):

| | kept (as parsed) | song 54 | song 55 | song 58 |
|---|---|---|---|---|
| stressed line-final syllable, an eighth or less | 0.24 | 0.27 | 0.34 | 0.19 |
| stressed, a half or more | 0.27 | 0.18 | 0.21 | 0.27 |
| lines run on (under a beat of rest) | 0.27 | 0.23 | 0.33 | 0.20 |
| silences of a beat or more per 100 beats | 7.0 / 9.1 / 11.1 | 9.5 | 9.5 | 10.4 |
| median silence (beats) | 1.5 / 2.0 / 3.0 | 3.0 | 2.0 | 2.5 |
| phrases over 12 beats (breath at half a beat) | 0.046 | 0.057 | 0.038 | 0.019 |

749.76 and 749.80 are closed: the line endings, the run-ons, the breaths and the phrase lengths now sit with the kept songs. Function-word line ends in song 54 are held a half or more in 15 of 24; that follows from their G (mostly 48 to 84 twelfths, where kept function words are held that long in 52 to 69 of 100), not from the draw. Rest share is still under the kept middle half in songs 54 and 55 (0.20, 0.171), as the paper says.

The one new thing this exposes: the band check from 749.21, "sung phrases over eight seconds", now reads 7, 7 and 5, because it counts a breath only at a full beat of silence. On that rule kept songs also run long (13 phrases in 100 over 12 beats); on a half-beat rule the songs match the kept (above). This is 749.83.

## 901, checked hardest: 871 and 890 retired

Recounted with `make_kept_line_ends.line_ends` (`studies/kept_checks/recount_901.py`: a line end on a word's weak syllable, its stressed syllable found by walking back through the same word):

| Corpus | Line ends | Ending on a weak syllable after its stressed one | Weak outlasts stressed | Stressed under a quarter |
|---|---|---|---|---|
| kept corpus as parsed (the maintainer's count: 619, 0.47, 0.72) | 5,242 | 664 | 0.49 | 0.73 |
| the same with tied notes read (749.82) | 5,542 | 794 | 0.42 | 0.64 |

Either way, in kept songs the weak last syllable outlasts the stressed one in four to five line ends in ten. The retirement stands. 749.64, 749.71 and 749.78, which I filed, rested on the premise that a held weak syllable is a fault; the kept songs do not support it. Song 58 now holds the weak syllable longer in 8 of its 14 such endings.

## The parser drops every note that begins a tie (749.82)

Found while recounting. `cocopops_parse.recip_dur` reads a duration only at the start of the token, so a note written `[8B` (the first note of a tie) has no duration and is skipped, syllable and all. Its tied end (`2B]`) is then kept as a melisma note, or merged into an earlier note of the same pitch. In the Billboard files 7,833 sung kern notes begin a tie. Example, Chiquitita: "sor- [8B -row. 2B]" is read as "sor-" then a melisma, so the word "sorrow" is never completed and its line end is unread.

Rebuilt with the tie's first note read (`studies/kept_checks/parse_ties.py`: the same parser, `[` set aside before the duration is read), the three kept tables move:

| Table | Reading | As parsed | Ties read |
|---|---|---|---|
| kept_line_ends | line ends read | 5,242 | 5,542 |
| | last syllable unread | 697 | 264 |
| | held a half or more: function, weak, stressed | 0.353, 0.196, 0.273 | 0.18, 0.115, 0.29 |
| | an eighth or less: function, weak, stressed | 0.259, 0.424, 0.236 | 0.358, 0.481, 0.182 |
| | lines run on | 0.269 | 0.295 |
| kept_word_weight | fit, 10th / 25th / 50th / 75th / 90th | 0.092 / 0.202 / 0.291 / 0.384 / 0.435 | 0.152 / 0.248 / 0.318 / 0.402 / 0.446 |
| | fit by length, median | 0.132 | 0.209 |
| | songs above their shuffled words | 0.893 | 0.944 |
| | stressed last notes counted | 1,791 | 2,833 |
| kept_returns | verse, other count, rhythm kept | 0.574 / 0.681 / 0.806 | 0.558 / 0.688 / 0.819 |

The words' gate (the kept 10th) would move from 0.092 to 0.152; 885's length term and 887/899's line ends were drawn from the as-parsed shares.

## The other fixes

| Fix | Reading | Held? |
|---|---|---|
| 900 two notes where three cannot clear the voice | guitar under sung notes 1.0 in songs 54, 55, 58 (song 54 0.656 before); "guitar above the sung note" printed with no kept figure | yes |
| 902 each flag once | song 55's flags once each | yes |
| 903 9.12 as kept songs meet it | last chorus against first: 16/12, 20/16, 16/14 bars | yes |

## 749.77

Not raised in v25. A kept figure for returning lines (`studies/kept_checks/stressed16_returns.py`): stressed syllables a sixteenth long inside lines are as common in kept songs' later verses and choruses as in their first (0.117 against 0.121 as parsed; 0.108 against 0.109 with ties read; the later-minus-first difference by song has a median of 0). Kept songs vary widely (by song, the 25th, 50th, 75th and 90th percentiles are 0, 0.034, 0.13 and 0.33). Song 54's lines sung again (17 of 124 syllables, 0.137) sit at the kept 75th. I agree: 749.77 is closed.

## Breaths and silences, read again

Above (899). By onsets (a gap of three beats), real breaths a minute: songs 54, 55, 58 7.8, 9.5, 6.6 (human median 7).

## New findings

749.82 and 749.83, in `songs/p68/fixlist_v26.md` and its Doc.
