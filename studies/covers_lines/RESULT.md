# Design B: the line test against covers, within a writer: result

25 November 2026, the songwriting session. Read against `PREDICTION.md` (commit cf89d36, before any feature was joined to a cover count). Scripts: `join.py`, `build.py`, `analyze.py`, `linefeat.py` (the maintainer's, unchanged); numbers in `result.json`. No lyric text is stored. For the maintainer to check.

**Two measures pass: "I" plus "you" (more covering artists) and syllables a line (fewer, more covering artists). Both effects are small. The second does not survive holding repeated lines constant, so it may be the chorus, or fans' typing, and not the line.**

## The data, as it came
- Join (titles and credits only): 978 writers with 10 or more matched songs; 140,513 of their English WASABI songs, 24,471 matched to a Discogs-VI clique in which the performer is a credited writer.
- Features for 139,377 (the rest had under 50 words or 8 lines). Test 1: **972 writers, 24,284 songs**; median 4 recording artists a song. Test 3 (unmatched songs counted as one artist): 138,709 songs, 17.5% matched.

## The verdicts
Coefficients are in log recording artists per SD of the measure, within writer, with log word count and first year; errors clustered by writer.

| Measure | Predicted | Within writer | p; Holm | Two halves | With zeros | Verdict |
|---|---|---|---|---|---|---|
| `iyou_rate` | higher | **+0.021** | .002; .015 | +0.028, +0.016 | +0.022 (p < .0001) | **passes** |
| `syl_line` | lower | **−0.029** | .001; .007 | −0.041, −0.015 | −0.013 (p < .0001) | **passes** |
| `rhyme_rate` | higher | +0.012 | .086; .35 | +0.011, +0.014 | +0.003 | unsettled |
| `line_cv` | lower | −0.014 | .047; .23 | −0.013, −0.016 | +0.000 | unsettled |
| `end_weight` | higher | +0.011 | .11; .35 | +0.008, +0.013 | −0.000 | unsettled |
| `you_lines` | higher | −0.009 | .20; .40 | −0.012, −0.005 | +0.005 | unsettled |
| `feel_late` | higher | +0.005 | .43; .43 | −0.005, +0.014 | −0.000 | unsettled |

Described only: `repeat_share` +0.077 (p < .0001; halves +0.084, +0.071); `i_rate` +0.030 (p < .0001); `emo_rate` +0.023 (p .003); `perfect_share` +0.014 (p .12); `stanzas` +0.013 (p .16).

**How big.** At the median of 4 recording artists, +0.021 a SD is about one more covering artist for every 12 songs one SD higher in "I" plus "you". Real and steady, and small.

## Readings after the result (not tests)
Repeated lines are the strongest thing here, and the line test warned they may be fans typing famous songs out in full. So both passes were read again on first-sung lines only, and with `repeat_share` held:

| | As tested | First-sung lines only | With repeat_share held |
|---|---|---|---|
| "I" plus "you" | +0.021 (p .002) | +0.025 (p .0007) | +0.016 (p .026); first-sung +0.019 (p .008) |
| syllables a line | −0.029 (p .001) | −0.023 (p .006) | −0.010 (p .28); first-sung −0.010 (p .22) |

- **"I" plus "you" holds** on first-sung lines and with repeats held. It is not the chorus or the typing.
- **Syllables a line does not separate from repetition** (r = −0.24 with `repeat_share`). Shorter lines and more returning lines travel together, and it is the pair that goes with covers. Whether that is a real chorus or a transcriber's habit, WASABI cannot say.

## Beside the critics (the line test)
| | Critics (RS500, within artist) | Musicians (covers, within writer) |
|---|---|---|
| "I" plus "you" | +0.04, p .34 (unsettled) | **+0.021, passes** |
| "you" lines | **−0.13, reversed** | −0.009, unsettled |
| syllables a line | −0.23 (lead) | **−0.029, passes** (with repetition) |
| rhyme | unsettled | unsettled |

The two channels again: a song with a speaker and someone spoken to is one other singers take up; critics do not reward it, and lean away from "you" alone. Shorter lines go with both, but tied to repetition.

## Against what I expected
I expected little; two passed. I guessed `you_lines` upward: wrong (unsettled, a little down). I guessed `repeat_share` (described only) would move: right, and most of all.

## For the engine and the room
- Nothing becomes a gate. The effects are small, and syllables a line is not separable from repetition.
- `lyric_people.py`'s advice to put a speaker and an addressee in the song now has a passed test behind it, **for musicians and listeners, not critics**. The note it prints can say so.
- Next, if wanted: test shorter lines against sung transcriptions (CoCoPops, BiMMuDa), where no one types a chorus out or leaves it, to tell the line from the habit.
