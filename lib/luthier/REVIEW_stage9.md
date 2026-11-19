# Review of Luthier v22, way 3: the marriage of tune and words (fixes 879 to 884), 18 November 2026

Branch `luthier-v8-stage1` at 1bb7d1f. Reruns are in REVIEW_stage8.md: every record on the branch reproduces byte for byte. Merged into main at 8dea87c.

| Check | Result | Held? |
|---|---|---|
| Every .py in lib/luthier compiles | yes | yes |
| Builds' median fit, songs 55, 54, 58 (README: 0.28 / 0.24 / 0.35) | 0.283 / 0.24 / 0.347 (`judge7.words_gate.builds_fit_quartiles`) | yes |
| 881 the words' gate in the record | `judge7.words_gate`, at least 0.092 | yes |
| 883 the fit and its parts in the checks | song 58: 0.29; by length, place, height 0.019, 0.541, 0.027 (kept medians 0.132, 0.311, 0.104) | yes |
| Song 52 and the hymns unchanged and flagged | 52 note for note; flag "no kept table of them outside 4/4" | yes |
| `stage9_results.json`, `tables/kept_word_weight.json` reproducible here | no maker; the study's paths are on the maintainer's machine (749.70) | no |

## 882, checked hardest

Method: `review9_trace882.py` wraps `Engine.again` and `Engine.build` and reruns song 58 (the record is unchanged by the trace). The picked build is build 0,
the first made (872). Its 34 calls to `again()`: 23 lines sung again (712) and 11 fresh lines that borrow an earlier line (818); 882 acts on both.
`review9_again_check.py` compares each line sung again with its source at v21 (1ffe2e6) and v22 (59e473c); `review9_stressed16.py` counts stressed syllables
a sixteenth long.

What holds:
- A line of the same count keeps its tune, as claimed: a change of a same-count line costs 16 against fits that move by a few units, and in song 58's pick
  5 of 23 lines sung again are kept note for note. Where a same-count line changes (6 of song 58's 11), its source's pickup was dropped first, by 772 before a stressed opening or by the line before (`tmin`), and 882 then adds the notes back inside the line.
- The splits, drops and lead-ins follow the place table: function words go to finer places, stressed syllables to beats. The one lead-in in song 58's pick
  (Last Chorus line 6) is placed an eighth before its source.
- The fit rises where the README says, and nearly all of it from 882.

What does not:
- **749.66 A split halves the note it splits, chosen by place alone, so a stressed syllable can be left a sixteenth long.** Song 54's lines sung again:
  stressed syllables a sixteenth long 3 of 137 under v21, 19 of 134 under v22; its other lines 4 of 82. Song 55: 5 to 9 of 81. Song 58's pick, Verse 2
  line 1, "sure the crowd was on its way": its source's two pickups dropped (772), two notes split back in, and "crowd" is left 3 twelfths long before four sixteenths. Song 58 itself is little changed (5 to 3 of 75). The README says length is
  not married; here 882's choice of where to split takes length away from the stressed syllable.
- **749.67 Returns keep less of their source.** Lines sung again whose count differs keep, in order, this share of their source's pitches and rhythm
  (v21, then v22): song 58 0.86 to 0.76 and 0.84 to 0.74; song 55 0.74 to 0.68 and 0.80 to 0.71; song 54 0.80 to 0.78 and 0.81 to 0.79. The maintainer's own
  figure agrees (song 58's builds' place under the old 4/4 judge, 0.83 to 0.62). There is no kept figure for how much of its source a returning line keeps,
  so neither the cost (`again_cost` 8) nor this loss is set against kept songs.
- **882 is undocumented for 818.** It also refits fresh lines that borrow an earlier line of their section (11 of song 58's 34 calls). Probably meant, but the
  README speaks only of lines sung again.
- **749.72 Two fits for one pick, two sets of kept figures.** Song 58's record prints the fit as 0.29 in its checks and 0.325 in `judge7.pick_words_fit`
  (with and without the melismas' second notes). `word_weight.py`'s docstring gives the kept fit as 0.18 / 0.28 / 0.37 and 87 in 100 beating the shuffled
  control; the README and the checks give 0.20 / 0.29 / 0.38 and 89 in 100.

## The other fixes

- 879 places scored by weight, 880 the step between words: both in `stress_score`, `weighted` and `pitches`, behind `word_weight` in the spec. As stated, alone
  they gain little.
- 881 the words' gate passes every build in all three 4/4 songs (749.68): builds' fit quartiles 0.24 to 0.38 against a gate at 0.092.
- 884 the reading: `word_weight.py` reads the weights from the engine's own (text, stressed) pairs; melisma second notes, whose text is empty, read as function
  words unless left out, which `song_from_lyric.py` does and the judge does not (749.72).

## New findings

749.66, 749.67 and 749.72 above; with v21's 749.68 to 749.71 in the fix list for v23 (`songs/p68/fixlist_v23.md`).
