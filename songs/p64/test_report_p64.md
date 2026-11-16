---
title: "The Man Mama Prayed I'd Be (song 54): test report"
subtitle: "Luthier v7 (Module 27.88, Window 164), the default path"
author: "Words and music: Jason Bryant"
---

*Words and music: Jason Bryant. 16 November 2026. Folder songs/p64.*

# Intake

Sixteen questions, one a turn, every answer logged verbatim in `intake.py`.

| Question | Answer |
|---|---|
| What the song is about | The writer's own earlier lyric, to be renovated ("I like the story these lyrics tell but it would need a serious renovation") |
| How far the renovation goes | A: keep the story, the four-refrain shape and his best details; steady metre and rhyme; a concrete image for "love sparkled fresh"; one comic line; plant the coffee |
| The sound | A: a mid-tempo country story song, neotraditional two-step (he asked whether it is the most commercial lane; answered with a check of the 2026 charts) |
| Who tells it | A: a narrator; he sings his refrains; she sings the last chorus |
| Never-say | A: country's stock words (truck, tailgate, dirt road, beer, whiskey, cold one, small town, Friday night) and "love sparkled fresh"; one "hell", the buddies' |
| Title | A: The Man Mama Prayed I'd Be |
| Draft 1 | Notes: the dream line generic; the graveyard-shift line unclear; verse 4 short of a concrete picture |
| Draft 2 | Five notes from another AI; three taken, one in part, one declined (the opening kept, as his own and called back in verse 4) |
| Draft 3 | A: locked |
| Unknown words | A: six readings (sleepin', mildewed, 'n', rooster's, mornin', fixin'), asked as one question |
| Key and voice | A: G major, baritone, verses about B2–B3, the hook to D4; she an octave up |
| Form | A: q = 120; intro 4; (verse 16, chorus 12) ×3; turnaround 4; verse 16; chorus 12; tag 4; ending 2 = 126 bars, about 4:12 |
| Type | A: N/V, Narrative primary, Love Song secondary |
| Love-song subtype | A: Longing (Ionian, the leading tone sung) |
| The hook | A: climbs to D4 on "Ma-"; open on D in choruses 1–3; home to G only in her chorus and the tag |
| The band | A: acoustic, Telecaster, fiddle, pedal steel, bass, drums (two-step, sticks), a little piano; "don't forget to include each instrument's notes on the parts file" |

# Method

The engine path: 4/4, written by Luthier v7 as ported (fixes 730–736; readings 737–739). `gen_l7_p64.py` writes `melody_l7_p64.py` from song 51's v7 file, changing only the song's own parts, each patch asserted to match once: the lyric and lexicon, G major, q = 120, the form, every line in two bars (308), the chart drawn by 438 with the designs' half-bars kept (song 51 had held its writer's chords), the designs as gates (317), and guards for a song with no bridge (749.24). Seed 20261113 + 454, calibration seed + 1, PYTHONHASHSEED 0.

# The melody search

| Run | Built | Survivors | Clean | Order |
|---|---|---|---|---|
| Main | 1,000 | 185 (18.5%) | 143 | 63a84b18e7dc (made twice, reproduced) |
| Control (243 off) | 1,000 | 192 (19.2%) | 157 | c43334ae0deb (made twice, reproduced) |

Deaths, main: no placement 667; the chorus above the verse 101; joins 18; limits 14; align 10; key word on a chord tone 5. The designs of the hook and the tag never failed. A 40-build smoke test ran first (12 survivors).

Where the placement deaths fall (main, by line): verse 2 line 7, "The boss never looked up from his clipboard" (10 syllables), 168; verse 3 line 6, "A workin' man where a rebel had been" (10), 122 with its fit ahead; chorus 1 line 5, "And all at once he wanted to be" (9), 72; verse 1 line 3 (9), 68; chorus 2 line 5 (10), 59 with its fit ahead. See 749.25.

# The pick

The judge's pick (730), d48480b70b0d (charge 0.0137, place 0.843, 107 eligible of 143 clean), sings "coffee" and "can" on one onset in verse 4: the second syllable of "coffee" has no length (749.1). No singer can sing it. 87 of the 143 clean survivors carry the same fault (749.26).

The pick of record is d12c2728e6f1, by 730's own rule (`luthier_judge5.pick`: least charge, then nearest the kept medians within 0.02) over the 56 clean survivors without the fault (42 eligible): charge 0.0005, place 0.862, its most-repeating window at 0.843 (inside 0.55–0.93), distance 4.55. This is the rule song 51's re-pick used; it was the run's call, logged and offered to the writer at delivery. It passes `evaluate` and every design gate; no hand edits.

The chant check: the longest run of one pitch is 9 (verse 1, line 5, on F♯3 over D; the kept median 6, the 90th percentile 9.5). Lines 4 and 8 of every verse, on the D chord, stay on F♯3 for seven to nine notes, near speech. First-eight-bar repeats by section: verses 0.17–0.44, choruses 0.19–0.21.

The line read: verses B2–B3, choruses D3–D4, D4 only on the hook's "Ma-"; the hook's notes as designed in every chorus; the widest leap a fifth; no scale note against a chord it clashes with (the song has no flat seventh).

# Research checks (section 2b)

| Rule | Reading | Target | Held? |
|---|---|---|---|
| 749.18, 749.20 surprise, melody | 3.05 bits | popular median 2.89 or under | No |
| surprise, chords | 1.85 bits | median 3.79 or under | Yes |
| surprise, rhythm | 3.42 bits | median 2.49 or under | No |
| 749.4–749.7 syncopation | 0.18 a note | popular 0.29 | (lead-sheet side) |
| stress | 55% of stressed syllables on a beat, 28% on 1 or 3 | (no kept band for country) | read |
| 749.17 intensity | top at chorus 4, 0.857–0.952 of the song; release in the tag (0.79) and ending (0.70); each chorus above its verse, each return above the last | top at 0.65–0.85, short release, each return higher | Late; the rest yes |
| 749.19 breath | the band stops on beat 3 of bar 108 (0.853), 3.5 beats before she enters on C5 over C, the song's first note in her octave | 0.55–0.60 | Late (the story's turn) |
| 749.21 low intervals | 0 in the chordal parts (after the acoustic voicings were rewritten; 586 before) | 0 | Yes |
| band over the sung line | him 81%, her 15%; within a second 13% | 2% | No for him (749.27) |
| phrases | median 2.25 s, 1.0–6.8 s, 3 over 6 s, none over 8 s | 2–6 s, 8 at most | Yes |
| 749.22 two channels | chord changes a bar: verses 0.56, choruses 0.75–0.83, tag 1.0; rests 44% of beats; length variety 1.65 (popular 1.52) | harmony moving within sections; room in the melody | Yes |
| 749.23 chromatic | no chord outside the key | pop: the departure budget | Yes |

# Arrangement and documents

The record (`build_p64.py`) holds every event: him, her, the other voices, eight parts. She sings the engine's line an octave up (chorus 4, the tag's second line). The bass in the sung sections is the routine's (bass_v134), root–five elsewhere. The 9.12 arc as read from the demo: verse 1 0.67, chorus 1 0.82, chorus 2 0.90, chorus 3 0.97, turnaround 0.80, verse 4 0.68, chorus 4 0.99, tag 0.79. Stems: the voices +5.2 dB over the band.

Readback: every staff of the lead sheet, the full score and the parts matches the record (him 432, her 62, harmony 45, acoustic 3,246, Telecaster 124, fiddle 56, steel 201, piano 220, bass 711 pitches; drums 1,521 of 1,521 hits). MusicXML: every part's onsets and the lyric count read back. `consistency_p64.py`: 70 of 70 checks pass. The producer one-sheet fits one page in the Word copy.

# Readings the paper does not give

- 715/730: the judge's pick and the pick of record differ only by 749.1; the pick of record's charge is the run's least among the eligible.
- 734: two raises in turn that did not count; the power returned to 1.000 (round 4).
- 739: printed each run beside its kept middle halves (run log).
- 438: the chart drawn over the plan: verse 0.56 changes a bar, chorus 0.75; Bm entered the chorus's line 3; the designs' half-bars kept (G, D in choruses 1–3; D to G in chorus 4 and the tag).

# Findings

## 749.24 The engine assumes a bridge

**Problem.** Song 54 has no bridge. Six readers in the v7 file read `BAR0["Bridge"]` or `LINES["Bridge"]` and stopped the run: the bridge plan draw, the era reading's three windows, 278's aims, 208/279's bridge-opening gate, the lift's bridge median and the reading's bridge axes.

**Evidence.** The first smoke test failed on each in turn; songs 48–51 all had bridges.

**Fix.** Make the bridge optional: draw its plan only if it is sung; read the era over the windows present (two here); leave the bridge's aims and gate unread when there is none.

**Check.** A song with no bridge runs with no song-specific guard; songs 48–51 reproduce their orders.

## 749.25 Placement deaths at nine- and ten-syllable lines with borrowed rhythms

**Problem.** Two-thirds of builds died for want of a placement (667 main, 662 control), the most of any song since v7 (songs 49–51: 741, 747, 749.3).

**Evidence.** A trace wrapped the rhythm draw and logged every call over 80 control builds. Failed and kept calls had the same room (earliest start and latest last onset alike), so the window is not the cause. The failures fall on lines of 9 and 10 syllables in two-bar slots whose rhythm is borrowed: verse lines sung again on verse 1's onsets (712), and verse 1 and chorus 1 lines drawn on a partner's or a returning unit's bars (310, 361). Of the 58 sung lines, 18 have 9 syllables or more.

**Fix.** When a borrowed rhythm cannot take a line's syllables, split its longest note (as 682 does for the template) or draw the bar fresh, rather than end the build.

**Check.** Song 54's main run keeps its pick; placement deaths fall under a third; songs 48–51 reproduce.

## 749.26 Two syllables on one onset, in most of the clean survivors

**Problem.** 749.1 again, and larger: 87 of 143 clean survivors (61%) sing two syllables on one onset, and the judge's pick was one of them ("coffee" / "can", verse 4).

**Evidence.** Main run; re-pick by 730's rule over the other 56 (42 eligible), d12c2728e6f1.

**Fix.** A note of no length is a death (or 715 makes the build ineligible); find where the second onset is lost (a melisma split on the line's last note, by the look of the case).

**Check.** No survivor with two syllables on one onset; the pick unchanged where it had none.

## 749.27 The band-over-the-tune limit does not carry over to a low lead

**Problem.** 749.21's limit (the accompaniment above the sung tune at most 2% of the time) was set on organ and choir, where the tune is the top line. With a baritone under guitars, fiddle and steel, 81% of his notes have something above them, as on most country records.

**Evidence.** Song 54: him 81%, her 15% (her accompaniment was kept below her); within a second of the tune, 13%; the voices sit 5.2 dB over the band.

**Fix.** Keep the 2% limit where the tune is the top line (choir, organ, a high lead). For a lead below the band, read salience by level and by what lies within a second of the tune.

**Check.** Songs 52, 53 and 54 each pass under the rule that fits them.

## 749.28 A story's turn falls later than the shape targets

**Problem.** 749.17 puts the high point at 0.65–0.85 of the song and 749.19 the breath at 0.55–0.60. In a story song whose twist is in the last verse, both fall late: the breath at 0.853, the top at chorus 4 (0.857–0.952).

**Evidence.** Song 54's form (A), the writer's; her entry is the payoff and cannot move earlier without changing the story.

**Fix.** Read the targets against the song's turn when the type is Narrative: the breath before the turn and the high point at it, wherever the story puts them, with the release after.

**Check.** A Narrative song's breath and top fall at its turn; other types keep 0.55–0.60 and 0.65–0.85.

## 749.29 The lexicon check: dialect forms and "a.m."

**Problem.** Five of the six unknown words were g-dropped forms of known words (sleepin', mornin', fixin' and so on), and "Git 'n' Split" read its "n" as the letter N, stressed. "a.m." splits into "a" and "m". Protocol 0b v67 asks one word at a time; the writer's rule is one question a turn, so the six went as one question.

**Evidence.** Song 54's intake; readings in `gen_l7_p64.py` (LEX64); "'n'" added to the function words.

**Fix.** Derive -in' forms from the -ing entry; read "'n'" as unstressed AH0 N; read "a.m." as one word, EY2 EH1 M; ask only words with no derivable reading, all in one question.

**Check.** Song 54's lyric needs only "mildewed" asked.

# Blind pick

The three 10.20 slots (`q1020.py`): remembered, "For a boy who's been gone too long"; middle, "The man Mama prayed I'd be"; annotated, "And sir I'm finally fixin' to be". Offered shuffled as A (annotated), B (remembered), C (middle); the writer chose C, "The man Mama prayed I'd be": Middle.
