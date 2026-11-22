# He Remembered Today (first edition): test report

Words and music: Jason Bryant. Song 62 (songs/p72). 22 November 2026. Luthier on main (v45 merged; 958 off as ruled in 749.153), PYTHONHASHSEED 0.

## Intake

- Source: the writer's play He Remembered Today (draft 4), read from src/, never stored.
- Lyric: nine drafts, every one shown in full; locked as lyric_locked.md (36 lines). Narrator; a preacher father; the refrain names his gift against what he misses.
- Mouth tests at lock (mouth_p72.py, q = 72 provisional): 36 lines, 6 to 10 syllables (median 8); density at most 2.00 a second; no weak endings, no tongue-twisters; 11 lines flagged (held close or reduced vowels; clusters of 4 at 'asked him', 'asks the'; 'outgrew' rare). No change.
- Settings (question 1): chamber pop, 4/4, 72, tenor, major, piano leads, a string quartet held back to the last refrain. Room check: bars unsung 0.127 (kept middle half), change in busyness 0.337 (just under the kept 25th, 0.343), rhythm scaling 0.655; 293 s over 88 bars. Question 2: every word at 72; the refrain in fewer, longer notes.
- The song was meant as a hold-out; the writer chose to write its music now (logged), so it is a seen song.

## The engine's draw (the test of record)

- Key C, D3 to G4; chord draft 5 of 12; 230 of 1000 builds survive (838: 600; 840: 166); pick 354a3c0084d9; judge 7 distance 2.332 (kept middle half 2.42 to 3.39); longest run of one pitch 6; words' fit 0.361; 313 s (past the kept 75th, flagged).
- Verse chords: I V for four bars, then V for four, twice. Within-section chord repetition 0.857 against the kept verse median 0.333: the habit 749.159's reading found, in a real song.
- As built (958 'apart'): a different song (pick 4549c06a6aef; verse repetition 0.091), not used.

## The design copy (design62.py)

Chords set by hand: verses I I vi vi IV I ii V / I I vi vi IV iii ii vi (verse 3 ends V), the bass walking down a step a bar; bridge IV iii ii V vi iii iv iv (iv, the one departure, under 'for now'); the last refrain's last two bars IV V | I. The refrain's chords are the engine's draft (no departures). Gates, in the order they were added:

1. The refrain's notes on average at least 1.3 times the verses' (question 2).
2. No leap past an octave inside a line (after pick 904b4764e66f zigzagged Eb3 Ab4 Db3 Eb4 across 'a nod across' and 'remembered').
3. Melody surprise at or under the kept median, 3.18 bits an interval (749.18; the scorecard showed the first design tune less plain than 85 of 100 kept tunes).
4. The refrain's median at least two semitones over the verse's (with gate 3 alone the judge's pick chanted, lift 0).

9000 builds, 9 survive; pick 153e06d87365; key Eb, G3 to Ab4; judge 7 distance 1.664; reproduces byte for byte.

## Scorecard (engine's draw, first design, the pick)

| Reading | Engine | Design 1 | Pick |
|---|---|---|---|
| Verse chord repetition (kept median 0.333) | 0.857 | 0.10 | 0.10 |
| Bars of chords from outside the key | 6 | 2 | 2 |
| Melody surprise: kept tunes it is plainer than | 72 | 15 | 60 |
| Words' fit (kept quartiles 0.25, 0.32, 0.40) | 0.361 | 0.409 | 0.401 |
| Refrain over verse, semitones | 1 | 3 | 2 |
| Sure endings | 0.43 | 1.11 | 0.71 |
| Judge 7 distance (kept middle 2.42 to 3.39) | 2.33 | 2.27 | 1.66 |

The writer could not tell the demos apart by ear (General MIDI); the choice was made on this card.

## Hand fixes (build62.py)

- title line: the long note moved from 'bered' to 'MEM'
- title line: 'today' lands on the tonic (60 to 63), the first full close of the song
- bridge: 'for' one beat, 'now' held
- Chorus 1 line 1: the opening 'he' from 67 to 56, a step under 'could'
- Chorus 1 line 2: the opening 'be' from 67 to 56, a step under 'the'
- Chorus 2 line 1: the opening 'he' from 67 to 56, a step under 'could'
- Chorus 2 line 2: the opening 'be' from 67 to 56, a step under 'the'
- Chorus 3 line 2: the opening 'one' from 67 to 56, a step under 'by'
- Chorus 3 line 4: the opening 'and' from 68 to 56, a step under 'he'

## The arrangement and the documents

- The engine's piano part and bass (left hand), with the walking bass in the verses; drums and the harmony voice out; cello from the bridge (bar 59); viola, violins in the last refrain from bar 84, the violins only in the voice's rests; the last line's tune on piano and violin in the outro.
- Strings above a sung note: 0.0 (749.21).
- Full score, lead sheet, parts (piano with the voice cued, violin I, violin II, viola, cello), MusicXML, songbook (Word), demo (MP3, General MIDI). Every staff reads back from its MIDI. consistency62: 37 of 37.

## Readings the paper does not give

- 749.17: the song's top note (Ab4, 'got' in the refrain) falls at 0.27 and 0.56 of the song, not 0.65 to 0.85; the bridge (G4, about 0.63 to 0.70) is the most sustained high singing.
- 749.19: there is no thinned beat before a fresh re-entry at 0.55 to 0.60; the turn before the bridge (bars 55 to 58) is piano alone.
- 749.22: the sung line sits on the audience's side (surprise under the median) and the verse harmony on the musicians' side (repetition 0.10).

## Findings for the list (from 749.160)

- **749.160** The planted peak can land a note an octave or more from its neighbours inside a word (pick 904b4764e66f: Eb3 Ab4 Db3 Eb4). Fix: no leap past an octave inside a line, as a gate. Check: song 62's design runs.
- **749.161** Melody surprise has no ceiling. A design tune passed every gate while less plain than 85 of 100 kept tunes, against 749.18. Fix: a ceiling at the kept median for popular styles, behind a flag; it costs survivors (9000 builds, 24 survive). Check: rerun songs 59 and 61 with it on; survivors and words' fit reported.
- **749.162** The title line's long note fell on an unstressed syllable in two design picks ('re-' and '-bered' in 'remembered'); the words' fit did not catch it on the one line that matters most. Fix: read the words' fit on the title line alone and gate its longest note onto a stressed syllable. Check: songs 61 and 62.
- **749.163** The masking rule (749.21) leaves strings almost no room above a tenor: in this song the violins can play only in the voice's rests (41 string notes in 94 bars). Question for the maintainer: does the rule, measured on piano song, apply to sustained strings and to a voice sounding an octave below its written line?
- **749.164** A chord writer pilot by hand: verses that walk (repetition 0.10) with an engine tune gated to plainness gave the nearest pick to the kept songs of any run (judge 7 distance 1.66). One song decides nothing; it is a case for 749.159's trial.
