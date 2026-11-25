# The line test, within a writer: result

25 November 2026. Read against `PREDICTION.md` (commit 325ce68, before any WASABI lyric was read). Scripts: `linefeat.py`, `check_rhyme.py`, `build.py`, `analyze.py`; numbers in `rhyme_check.json`, `result.json`. No lyric text is stored.

**Nothing passes. One measure is reversed: within an artist, the song on the Rolling Stone list has "you" in fewer of its lines.**

## The data, as it came

WASABI's 2,079,510 songs were read once. 59,445 English songs by artists with a listed song; 689 of the 780 listed songs found. After the rule (five songs or more, at least one listed and one not, a year known: 88 rows in 100 have one, so year is used): **356 artists, 50,834 songs, 672 listed.**

The rhyme detector, on its first run and not tuned: against CoCoPops's hand marks (201 songs, 5,497 line ends) precision 0.75, recall 0.74, **F1 0.74**, over the bar of 0.70. It calls 54 lines in 100 rhymed; the hand marks, 54. Both rhyme measures count, so Holm's correction is over six.

## The verdicts

| Measure | Predicted | Within artist (per SD) | p; Holm | Two halves | Listed; others | Verdict |
|---|---|---|---|---|---|---|
| `rhyme_rate` | higher | +0.06 | .17; .83 | +0.05, +0.07 | 0.673; 0.674 | unsettled |
| `perfect_share` | lower | −0.01 | .92; 1 | −0.01, 0.00 | 0.493; 0.494 | unsettled |
| `iyou_rate` | higher | +0.04 | .34; 1 | +0.01, +0.08 | 13.3; 13.1 | unsettled |
| `you_lines` | higher | **−0.13** | **.004**; .024 | −0.16, −0.08 | 0.253; 0.277 | **reversed** |
| `end_weight` | higher | 0.00 | .98; 1 | +0.03, −0.05 | | unsettled |
| `feel_late` | higher | −0.01 | .83; 1 | +0.03, −0.06 | | unsettled |

Described only (no prediction was made, so these are leads and not findings):

| Measure | Within artist | p | Two halves | Listed; others |
|---|---|---|---|---|
| `repeat_share` (lines sung before) | +0.20 | < .0001 | +0.14, +0.28 | 0.30; 0.25 |
| `syl_line` (syllables a line) | −0.23 | .0002 | −0.34, −0.12 | 8.1; 8.4 |
| `stanzas` | +0.09 | .003 | +0.12, +0.06 | 9.0; 7.2 |
| `i_rate` | +0.09 | .02 | +0.08, +0.11 | 8.4; 8.1 |
| `emo_rate` | +0.05 | .18 | | 2.3; 2.2 |
| `line_cv` | +0.02 | .68 | | |

## What it says

1. **Rhyme does not pick a writer's canonised song.** How much a song rhymes, and how perfectly, is the writer's habit: the listed song and the others are the same to the third decimal.
2. **"Address someone" is not supported for acclaim, and runs the other way.** The listed song has "you" in 25 lines of 100, the artist's others in 28. It holds in both halves, and it agrees with round one, where "you" ran lower among acclaimed writers (p .052). Listeners buy "you" (Packard and Berger); this list's critics lean away from it. "I" plus "you" together does nothing.
3. **Weight at the stanza's end and a feeling named late: nothing.** The measures are crude (word lists), so this is no proof of absence, but there is no sign of an effect either.
4. **The leads.** The listed song has shorter lines, more lines that return, and more stanzas. Two of those may be how fans write famous songs out (every chorus typed in full, where a lesser song gets "chorus x2"), so I do not trust them until checked against sung transcriptions (CoCoPops or BiMMuDa). Shorter lines is the one I would test next, rule first: it is a thing the engine and the room can act on, and it sits with what the kept songs showed about one-bar lines.

## Against what I expected

I expected nothing to pass: right. I guessed that if one moved it would be `iyou_rate`, sign unknown: wrong, it did not move; `you_lines` did, in the direction I had half-suspected for critics.

## For the engine and the room

- Nothing here goes into the engine.
- The room's advice on people stays as advice for feeling and warmth, with this caution written on it: it is no route to acclaim. `lib/luthier/lyric_people.py` now says so where it suggests a "you".
- Not done: the covers outcome (the round-two Design B), the Grammy list, the standards (word stress against the beat).
