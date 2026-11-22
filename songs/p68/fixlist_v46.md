# Luthier list for v46 (since v45)

22 November 2026. Luthier v45 (958, song 49 as a second hold-out, 749.145, 749.146) is reviewed (`lib/luthier/REVIEW_stage30.md`) and merged into main at 06829b1. Every kept table, every record (song 49 with and without the form, song 60's v45 record), `soundness.json`, `neighbour_v45.json` and the lever-range study reproduce byte for byte. Both checks pass. Song 58 has no new edition (see 749.153). Next finding 749.170; next fix 959 (960 proposed in 749.159).

## In short

958 meets every check on the songs it was fitted to. The hold-out, song 49, fails the check that guarded it: its builds' words' fit falls 0.040 and its chosen tune's 0.116. I turn the form off by default and approve the maintainer's proposed trial, with checks written now and a fresh hold-out, song 50.

A line-by-line reading of song 49 adds one thing: the larger fall is in the verse lines the form did not touch, so the trial must read those lines too.

749.145 and 749.146 are closed. The within-artist result holds, narrowly, and is read correctly.

Added since (running tab, 22 November): the fresh-songs test came out same direction, not settled, and the maintainer's own run is the test of record (749.158); the chord writer loops more than kept songs in every kind, so the loop-less trial goes ahead, its rule written first (749.159). Song 62 (He Remembered Today) was written with the verses' chords walking by hand: it gave the nearest pick to the kept songs of any run (749.164), and it showed two things the engine cannot yet see: holding the tune plain whitened its pitches (749.165), and a pink tune and a plain one pulled apart (749.166).

## Items

### 749.153 958 off by default; the form returns only as a trial weighted by kept shares at the song's tempo
**Problem.** 958 was tuned on songs 55, 54 and 58. On song 49, which nothing was fitted to, it lowers the words' fit beyond what those songs were allowed.
**Evidence.** Window 202, Table HL. Song 49 with the form: builds' middle words' fit 0.264 to 0.224; chosen tune's 0.326 to 0.210; range 20 to 16. `studies/lever_range`: kept verse lines take one bar 28, 18 and 9 times in 100 at 6, 7 and 8 syllables (fast tempo: 12, 3, 1; middle: 40, 24, 13; slow: 40, 38, 21). The form gives two to four of a verse's eight lines one bar, whatever their length.
**Fix.**
- From v46 the form is off unless a lyric asks for it ("verse_closer": true); the code stays.
- Records rerun under v46 return to their v44 notes; say so per song.
- The trial (the maintainer's proposal, made concrete): in each verse of a 4/4 song, each line of 6 to 8 syllables that would take two bars carries s, the kept share of verse lines that long taking one bar in the song's tempo band.
- A verse takes round(Σ s) such lines, the highest s first (shorter first on a tie), none beside one already taken. At a fast tempo this is usually none.
- The maintainer may refine the rule before the run, but not after.
**Check.** All must hold, written before the trial is run:
1. Words' fit, the builds' middle: no more than 0.02 under the form-off builds in each of songs 55, 54, 58 and 49.
2. Words' fit, the chosen tune: no more than 0.02 under the form-off tune in songs 55, 54 and 58. Song 49 is reported, not judged (one draw).
3. The verse lines not given one bar: their mean words' fit in the builds (as `studies/review30_holdout49/per_line.py` reads lines) no more than 0.02 under the form-off builds, in songs 54 and 49 (749.154).
4. Rhythm scaling, the builds' middle: higher than without the form in at least three of the four songs. Reaching the kept quartiles is not required.
5. The soundness rule and the pool standard; the guard on verse over chorus; the floor and the ceiling; 7 builds in 10; the builds' middle range not under the floor in any song (song 55's fell from 17 to 15 under 958).
6. Song 50, the new hold-out (749.155): run with and without only after the trial is frozen. If its builds' middle words' fit falls more than 0.02, the trial is not built. Reported either way.

If any check fails, the form stays off and no further variant is tried in the same window.

### 749.154 Song 49's fall sits in the verses, more in the lines the form left alone
**Problem.** The maintainer's account of the fall (eight syllables in one bar leave no long note for a weighty syllable) explains the lines given one bar, but not the larger fall in the verse lines left at two bars.
**Evidence.** `studies/review30_holdout49/per_line.json`, the engine's fit read line by line on the two chosen tunes:
- Verse lines given one bar: mean 0.269 to −0.034.
- The other twelve verse lines: 0.536 to 0.068.
- The rest of the song: 0.370 to 0.502.
- By part, height falls most (0.206 to 0.066); length least (0.278 to 0.254).
One chosen tune cannot separate the draw from the form.
**Fix.** Read the same three groups in the builds of song 49 with and without 958, and of each song in the trial. If the untouched verse lines fall in the builds, find why before any form is built: for example, the verse tune is drawn whole and a verse that mixes one-bar and two-bar lines draws a worse tune for its two-bar lines.
**Check.** The three groups printed for songs 54 and 49, form off and form on, in the window's table; check 3 of 749.153 judged on them.

### 749.155 A fresh hold-out for the trial: song 50
**Problem.** Song 49 has been seen, and the trial is aimed at what it showed, so it cannot hold the trial out.
**Evidence.** The rule of Review 29: the most recent song in 4/4 not yet run by this engine, with at least four verse lines of 6 to 8 syllables.
- Song 51 has one such verse line (`songs/p61/lyric_locked.md`).
- Songs 52 and 53 are in 6/8 and 3/4.
- Song 50, "The Small Things" (`songs/p60`, words by Jason Bryant), is a swung 4/4 at about 76 beats a minute, folk, with 14 of its 16 verse lines at 6 to 8 syllables.
**Fix.** Make `songs/p60/lyric50.json` from `lyric_locked.md` with no change of words. Take tempo, genre and voice from its intake. Mark the swing as its intake says, or report that the engine reads it straight. Never fit to it. Song 49 joins songs 55, 54 and 58 as a seen song; song 59 stays a hold-out for everything else.
**Check.** The lyric file matches the locked lyric line for line, and song 50 is run only after 749.153's trial is frozen.

### 749.156 Song 55's range under the form
**Problem.** Under 958 the builds' middle range in song 55 fell from 17 to 15 semitones, and its chosen tune sits at the floor's edge. The paper said so plainly.
**Evidence.** Window 202, the records paragraph.
**Fix.** Nothing to build now: 958 is off. Kept as check 5 of 749.153, so the trial cannot pass by narrowing a song.
**Check.** Song 55's builds' middle range at or over the floor under the trial.

### 749.157 The judging research: holds, narrowly; what it permits and what it does not
**Problem.** The within-artist result (−0.042, p .009) passes its rule by 0.002, carried by one half of the artists (the other at p .16). Chord surprise passed among sixteen further measures, where about one would by chance.
**Evidence.** `studies/judging_checks/within_artist/RESULT.md`. Not rerun here: its views and cover counts are not committed.
**Fix.** Before the trial of sections that loop less in the chord writer, write its rule and its fresh-songs leg (McGill, J6b) first, and commit a script that rebuilds the views and counts from public sources, so the review can rerun it. Chord surprise gets its own rule-first test before it is used anywhere.
**Check.** The trial's rule and the fresh-songs leg are committed before any outcome is read; the review reruns the test from the repository.

### 749.158 The fresh-songs leg (J6b): the chord finding points the same way on songs it was not chosen on, but too weakly to count
**Problem.** The chord finding was chosen on Hooktheory songs. 749.157 asked for a test on songs it never saw, rule first.
**Evidence.** `studies/fresh_songs` (rule 59182c6, measures 4ae7515, test d0cd57b, then the data; result c42b36b). 439 McGill songs in no part of Hooktheory, matched to Discogs-VI version groups. Chord repetition within a section against covers, year and chords read held: −0.060, p .21 (95% −0.154 to +0.034). Power to see −0.04 was 0.13. With weeks and peak: −0.085, p .058. Artist held: −0.039, p .63. Weeks on the Hot 100 against repetition: +0.073, p .086, the other sign.
**Fix.** No engine change. Record the verdict by its own rule: unsettled. The maintainer's side ran the same test at the same time, rule first (f25209f, `studies/judging_checks/fresh_songs`): −0.028, range −0.11 to +0.05, 438 songs, same direction, not settled. That run is the test of record; this one is a second reading of the hold-out, and counts as one. The 0.03 between them comes from model choices alone. The test reruns from public sources (Zenodo 13983028 and the committed McGill charts), as 749.157 asked.
**Check.** `python3 -I studies/fresh_songs/join_and_test.py main.zip` gives `result.json` byte for byte.

### 749.159 The trial of sections that loop less (proposed as 960), with its rule written before any build
**Problem.** The chord writer takes a section's structure, which bars repeat which, from one kept section, drawn at random (800). Its sections loop at the kept rate. Songs that loop less within a verse or bridge get more covers: across artists on two sources, within artist narrowly (749.157), and the same way but unsettled on fresh songs (749.158). Weeks on the chart lean the other way, so the chorus is left alone.
**Evidence.** 749.157, 749.158; night one's J1 and night two's R02-1.
**Fix.**
- Step one, a reading, no change (done: `studies/loop_less_reading`, see below): within-section chord repetition (the research check's frozen rules) of the writer's verses, choruses and bridges, 1,000 drafts a kind per mode, against the kept median of that kind. If the writer's verse and bridge sit below the kept median already, stop: there is nothing to trial.
- Step two, the trial, behind its flag and off by default: verse and bridge structures drawn only from kept sections of that kind below the kept median. Chorus and every other kind unchanged.
**Check.** Written now, before any build:
- Verse and bridge repetition of the chosen builds below the kept median on at least three of the four songs run; chorus repetition within 0.02 of the flag off.
- The stage 4 held-out readings (first, last, chords, bigrams, bars) stay within their floors.
- On the songs run, the words' fit and the judge's pick fall no more than the guarded amount of 749.155.
- A fresh hold-out the maintainer names, not song 50 (959's) and not song 59 (read only). It must pass the same guard.
- On by default only if every check passes and the maintainer rules that the evidence (across artists strong, within artist narrow, fresh unsettled) is enough. Otherwise it stays a setting a lyric can ask for.

**Step one's reading (22 November, `studies/loop_less_reading/RESULT.md`).** The writer loops more than kept songs in every kind and both modes (verse medians 0.385 against 0.333 major, 0.412 against 0.333 minor; chorus and bridge higher too, minor bridge not significantly). The trial goes ahead. One change to its rule before any build: half the major-key kept bridges never repeat a three-chord run (median 0.0), so for the bridge both the draw and the check read at or below the kept median, not below it.

### 749.160 The planted peak can land a note an octave or more from its neighbours inside a word
**Problem.** Song 62's first design pick (904b4764e66f) sang Eb3 Ab4 Db3 Eb4 across "a nod across" and "remembered".
**Evidence.** `songs/p72/intake.py` LOG; `songs/p72/design62.py`.
**Fix.** A gate: no leap past an octave inside a line.
**Check.** Song 62's design runs; the gate's deaths reported per song.

### 749.161 Melody surprise has no ceiling
**Problem.** A song 62 design tune passed every gate while less plain than 85 of 100 kept tunes, against 749.18.
**Evidence.** `songs/p72/test_report62.md`, the scorecard.
**Fix.** Not a ceiling on its own: 749.165 shows that on song 62 it whitened the sung pitches. If taken up, only together with 749.165's floor on the pitches' long-range order, behind a flag.
**Check.** Songs 59 and 61 with both on: survivors, words' fit and the pitch DFA reported.

### 749.162 The title line's long note can fall on an unstressed syllable
**Problem.** In two song 62 picks the title's long note fell on "re-" and on "-bered" of "remembered"; the words' fit did not catch it on the line that matters most.
**Evidence.** `songs/p72/build62.py` (the hand fixes).
**Fix.** Read the words' fit on the title line alone, and gate its longest note onto a stressed syllable.
**Check.** Songs 61 and 62.

### 749.163 The masking rule leaves strings almost no room above a tenor
**Problem.** With 749.21 kept, song 62's violins can play only in the voice's rests: 41 string notes in 94 bars, and the last refrain cannot bloom.
**Evidence.** `songs/p72/out` record readings; `songs/p72/build62.py`.
**Fix.** A ruling: does the rule, measured on piano song, apply to sustained strings and to a voice sounding an octave below its written line?
**Check.** The ruling written into the arrangement rules, with a reading on song 62.

### 749.164 A pilot of 749.159 by hand
**Problem.** None; a case for the trial.
**Evidence.** Song 62: verses that walk (repetition 0.10) with an engine tune gated to plainness gave the nearest pick to the kept songs of any run (judge 7 distance 1.66; the engine's own draw 2.33, its verse repetition 0.857).
**Fix.** None now. One song decides nothing.
**Check.** 749.159's trial as written.

### 749.165 Holding melody surprise down whitened the sung pitches
**Problem.** With the surprise ceiling (749.161), song 62's pick put 79% of its sung syllables on three pitches, and the writer's own scorer read its pitches as the whitest in the corpus: N 325, DFA-1 0.774, DFA-2 0.796, below the band on both orders; three pitches 82.5% of the attacks; the score held at 9.0.
**Evidence.** Reproduced on the 326 sung syllables with `lib/luthier/scaling.py` (it reads higher): the pick 0.846 / 0.920, three pitches 79%; the engine's own draw 0.959 / 1.050, 60%; the first design tune, before the ceiling, 0.900 / 0.926, 52%. Two independent implementations on the writer's side agree with each other exactly. `songs/p72/intake.py` LOG.
**Fix.** A floor on the sung pitches' long-range order (DFA, orders 1 and 2, on the syllables' pitches, melisma notes left out) and a ceiling on the share of the three commonest pitches, read as gates; the band to come from the writer's scorer, so the engine reads what he reads.
**Check.** The kept songs' readings on the same series give the band's quartiles; songs 59, 61 and 62 rerun with the gate on, survivors reported.

### 749.166 On song 62, a pink tune and a plain tune pulled in opposite directions
**Problem.** With 749.165's gate (DFA at least 0.95 and 1.0, three pitches at most 65%) in place of the surprise ceiling, 1 build in 9000 survived. It was pink (0.967 / 1.069, three pitches 59%) and restless: less plain than 77 of 100 kept tunes, words' fit 0.334 (from 0.401), judge 7 distance 1.86 (from 1.66).
**Evidence.** `songs/p72/run_d/design_g5.log`; `songs/p72/design62.py` (gate 5).
**Fix.** No engine change yet. A question for the research: across the kept songs, how do melody surprise and the pitches' DFA go together? If kept songs manage both, the writer has a target region; if they trade, the gates must choose a point on the trade, not both ends.
**Check.** The kept songs' scatter of the two, and where songs 52 to 62 fall in it.

### 749.167 The second refrain comes back note for note
**Problem.** Song 62's second refrain repeats the first exactly; the writer's scorer counts that against the song, and it flattens the pitches' long-range order. 839 lifts one held note in a returning line, but fired on about one copied line in four across the builds (9,066 of 36,000) and not at all in the pick.
**Evidence.** `songs/p72/run_d/lyric62_d_g4.song.json` stats; the pick's later-chorus readings (0.56 to 0.75 of bars the same, kept 0.57).
**Fix.** When a whole section returns note for note, require at least one line of it to vary (839's lift, or a second form of it), rather than leaving it to chance. `songs/p72/build62.py --vary-refrain` does it by hand: lines 2 to 4 each lift their longest held note a scale step onto a chord tone.
**Check.** Song 62's second refrain; the share of songs whose returning sections vary, against the kept share.

### 749.168 A blue-note song is drawn whatever the style
**Problem.** Song 62's only pink tune (749.166) carried nine lowered thirds, two of them held, in a chamber-pop ballad. The engine draws a blue-note song from the genre family's share, and chamber pop falls in the family "other" with pop and folk.
**Evidence.** `songs/p72/run_d/lyric62_d.song.json` checks: 'a song with blue notes' True; flat thirds 0.026 of notes.
**Fix.** Let the lyric's settings name a style the blue-note draw respects (chamber pop, hymn, art song: none), or let the writer turn it off.
**Check.** Song 62 rerun with it off; no lowered thirds.

### 749.169 One hold-out, two readings
**Problem.** The fresh-songs test (J6b) was run twice on the same McGill hold-out on 22 November, by the maintainer's side and by the writer's, neither knowing of the other. Under `studies/judging_data/README.md` both count, and the hold-out is spent faster than it should be.
**Evidence.** `studies/judging_checks/fresh_songs` (test of record, -0.028) and `studies/fresh_songs` (-0.060); 749.158.
**Fix.** A one-line ledger in `studies/judging_data/README.md`: who is running which test on a hold-out, written before the run.
**Check.** The ledger exists and each test against a hold-out names its line in it.

## Closed

- 749.142: built as 958 and turned off by 749.153.
- 749.143: done; song 49 was the hold-out and is now a seen song.
- 749.145: the neighbour block reads the table; `neighbour_v45.json` reproduces byte for byte.
- 749.146: the range does not widen (`studies/lever_range`, reproduced byte for byte); song 61's remedy is 749.144 or the lyric.

## Carried, open

- 749.144: song 58, bars with nothing sung (the second carrier of rhythm scaling).
- 749.147: a short line in a long slot holds its weak words.
- 749.148 to 749.152: the five hymn items from song 12 (the peak band, the hymn judge's line shape, the four-part search, the room check on a hymn, weak-syllable length in every stanza).
- Older: 749.125, 749.127, 749.109, 749.116, 749.103, 749.101, 749.61.
