---
title: "Your Yard Man (song 55): test report"
subtitle: "Luthier v7 (Module 27.88, Window 164), the default path"
author: "Words and music: Jason Bryant"
---

*Words and music: Jason Bryant. 16 November 2026. Folder songs/p65.*

# Intake

Nine questions, one a turn, logged verbatim in `intake.py`. The writer asked for song 54's treatment: his earlier lyric renovated, the same lane.

| Question | Answer |
|---|---|
| The song | The writer's earlier lyric (the yard man), "same kind of treatment as the last one, use the ideas and structure but craft a lyric that actually works" |
| Never-say | B: song 54's list as it is (no truck, no beer: "half-ton" and no drink named) |
| Title | A: Your Yard Man ("I'm your yard man ... but I'm my own man") |
| Draft 1 | Notes: the travel jokes decline (Australia sitcom-like); verse 2 the least distinctive; the emotional range narrow |
| Draft 2 | A: locked. Verse 2 became his daddy (thirty-one years at the mill; his last summers watching his son cut his grass); chorus 2 turns on it (the summers Daddy never got to); Holland first, Paris last after the hat |
| Unknown word | A: callin' as CALL-in |
| Key and voice | A: A major, baritone, the chorus to E4 on "yard" |
| Form | A: q = 120; intro 4; (verse 16, chorus 14) ×2; break 4; verse 16; chorus 14; tag 2; ending 2 = 102 bars, about 3:24 |
| Type | A: N/A, Narrative primary, Anthem secondary |
| The hook | A: the call ("I'm your yard man", E4 on "yard") and its answer ("but I'm my own man", home on A) |

The band was taken as song 54's (the writer: "same kind of treatment"); one singer. "own" is read stressed in this song.

# Method

The engine path on Luthier v7 as ported. `gen_l7_p65.py` writes `melody_l7_p65.py` from song 54's file (with its guards for a song with no bridge), changing only the song's own parts, each patch asserted once: the lyric and lexicon, A major, q = 120, the form, verse lines in two bars, the chorus's frame lines (1–4, 9–10) in one bar and its middle lines in two, the tag's lines in one; the chart drawn by 438 with the designs' bars kept on A; the call and the answer as designs (317). Seed 20261113 + 455.

# The melody search

| Run | Built | Survivors | Clean | Order |
|---|---|---|---|---|
| Main | 1,000 | 153 (15.3%) | 107 | 000c3f344509 (made twice, reproduced) |
| Control (243 off) | 1,000 | 149 (14.9%) | 109 | 42fad285b3c0 (made twice, reproduced) |

Deaths, main: no placement 678; joins (212) 124; the chorus above the verse 23; limits 14; align 7; the judge's floor 1. The hook and tag designs never failed. By line, the placement deaths fall on the chorus's one-bar lines: chorus 1 line 2 ("That's all I aim to be", 6 syllables) 259; line 3 (5) 177; line 4 (5) 155; chorus 2 line 2, its copy, 79 (749.30).

# The pick

The judge's pick (730), eb35d48bcd4d (charge 0.011, place 0.849; 24 eligible of 107 clean), sings two syllables on one onset in verse 3 ("half-ton"). 45 of the 107 clean survivors carry the same fault (749.26, again). The pick of record is 8fcba32b9784, by 730's own rule over the 62 clean survivors without it (16 eligible): charge 0.007, place 0.849, its most-repeating window at 0.571 (inside 0.55–0.93), distance 5.45. It passes `evaluate` and every design gate; no hand edits.

The chant check: the longest run of one pitch is 6 (verse 1, line 1; kept median 6). First-eight-bar repeats: verses 0.23–0.31, choruses 0.21–0.28.

The line read: verses B2–B3 (lower than the C♯3–C♯4 offered at intake: the register draw does not take the stated verse place, as 314 says); choruses E3–E4; E4 only on the hook; the widest leap a fifth. Two of the middle lines spread across their two bars with a long rest inside: "To be plumb … sick of it" and "Never got … to" (749.31).

# Research checks (section 2b)

| Rule | Reading | Target | Held? |
|---|---|---|---|
| 749.18, 749.20 surprise, melody | 3.01 bits | popular median 2.89 or under | No |
| surprise, chords | 2.14 bits | 3.79 or under | Yes |
| surprise, rhythm | 3.63 bits | 2.49 or under | No |
| syncopation | 0.23 a note | popular 0.29 | read |
| stress | 60% of stressed syllables on a beat, 38% on 1 or 3 | (no kept band for country) | read |
| 749.17 intensity | top at chorus 3, 0.824–0.961; release in the tag and ending; each chorus above its verse, each return above the last; verse 2 the quietest verse | 0.65–0.85 | Close (the top's start inside) |
| 749.19 breath | the break's last bar (bar 68, 0.657) the acoustic alone; verse 3 re-enters on E3 | 0.55–0.60 | Near |
| 749.21 low intervals | 0 | 0 | Yes |
| band over the sung line | 85%; within a second 14% (749.27) | 2% | No (a low lead) |
| phrases | median 2.25 s, 0.8–6.0 s, none over 6 | 2–6 s | Yes |
| 749.22 two channels | chord changes a bar: verses 0.56, choruses 0.86; rests 43% of beats | moving harmony, room | Yes |
| 749.23 chromatic | none | the pop budget | Yes |

# Arrangement and documents

The record holds the voice, the harmony on the call and answer (and chorus 3's lines 2–4) and eight parts. The 9.12 arc: verse 1 0.69, chorus 1 0.82, verse 2 0.66, chorus 2 0.91, break 0.74 (ending at 0.36), verse 3 0.81, chorus 3 0.99, tag a build from the stop. Stems: the voice +4.8 dB.

Readback: every staff of the lead sheet, the full score and the parts matches the record; drums 1,218 of 1,218; MusicXML onsets and 357 lyrics read back. `consistency_p65.py`: 62 of 62. The one-sheet fits one page in the Word copy.

# Findings

## 749.30 One-bar lines die in fresh draws

**Problem.** The chorus's one-bar frame lines (4 to 6 syllables) carried most of song 55's placement deaths: 678 a thousand, 590 of them on chorus lines 2 to 4 and their copies.

**Evidence.** The trace (songs/p65/diag/trace_place.py, 60 control builds): chorus 1 line 4 failed 14 calls of 35 and line 2 11 of 49, drawn fresh (no borrowed rhythm), with the same room in failed and kept calls. The cause is inside the draw for a one-bar slot, the span (600) by the look of it, not the window.

**Fix.** Read the one-bar draw's failures by step (span, gaps, run lengths) and let a one-bar line of up to seven syllables take any span that fits the bar.

**Check.** Song 55's main run keeps its pick; deaths at the one-bar lines under one in ten.

## 749.31 A short line spread across two bars with a long rest inside

**Problem.** Lines of four to six syllables in two-bar slots can be drawn with a rest of three beats or more between their words.

**Evidence.** The pick of record: "To be plumb (3.5 beats) sick of it" and "Never got (3.5 beats) to". They pass every reader.

**Fix.** Cap a line's inner rest at the kept lines' 90th percentile for its syllables and slot, or give such lines one bar.

**Check.** No pick with an inner rest over the kept 90th percentile.

## 749.26, again

**Evidence added.** Song 55: 45 of 107 clean survivors sing two syllables on one onset, and the judge's pick was one (verse 3). The fault is general, not song 54's.

# Blind pick

The three 10.20 slots: remembered, "I'm your yard man"; middle, "But I'm my own man"; annotated, "Half-ton, trailer, mower on the back".
