# Luthier list for v51 (since v50)

25 November 2026. Luthier v50 (fix 964: the octave bin shared as kept songs share it, on by default; song 50 spent on it) is reviewed (`lib/luthier/REVIEW_stage35.md`) and merged into main. Songs 54, 55, 58 and 50 reproduce byte for byte under 964; the check passes. Next finding 749.197; next fix 965.

## In short

You found the real fault: the kept table's ±12 bins hold every interval of an octave or more, and the draw gave the whole bin to each such pitch (749.192). Fix 964 corrects it, and the leaps fall to the kept rate with no gate. It is the best finding of the week. My centre proposal (749.191) was wrong, and the reading showed it.

Building 964 on song 50's marks, written first and set by the writer's ruling, is agreed. 749.193 (drawing until an outcome arrives selects for its easiest road) is a rule to read every redraw by.

Song 50 is spent. Sealed now: 63 (the loop gate), 64 and 65 (unreserved). The writer has ruled that the octave gate stays (749.194).

## Items

### 749.194 Is the octave gate still wanted? (for the writer)
**Problem.** With 964 and no gate, 6 to 15 builds in 100 hold a leap past an octave inside a line (kept: 17.5 songs in 100). The gate (959) now passes over 18 to 54 builds in 1,000, where it passed over 66 to 119 before 964.
**Options.** Keep the ban as it is (cheap now; strictly safer than kept songs); make it a setting, off by default (the engine then leaps about as often as kept songs, never more); or a test of taking it off, rule first, read both ways, with a sealed song.
**Ruled (the writer, 25 November): keep the ban.** 959 stays on by default; no change is tried. Closed.

### 749.195 Song 50's small pools
**Problem.** Song 50's pools are 4 builds (v47) and 5 (964), under the standard of 10, and its chosen tune's words' fit fell from 0.399 to 0.209 with the builds behind it the same to three places (0.248 both).
**Fix.** A reading first, rule committed before it: which gates and which part of the choice leave song 50 so few builds (its wide asked range in a low voice is the likely cause), and whether the choice among so few reads the words' fit as one draw (749.175).
**Check.** Written with the reading. Before song 50 is made for real.

### 749.196 A nit in 964
**Problem.** Where the octave above or below a note is not among its candidates (a clash rule took it), the octave's share of the ±12 bin is not passed on to the pitches past it, so that bin is under-weighted for that note.
**Fix.** When there is no octave candidate, give the pitches past it the whole bin's share between them; or leave it and say so.
**Check.** Count how often it happens over 1,000 builds of songs 55, 54, 58; if under 1 note in 1,000, leave it.

## Addendum: song 50's pool read, and the nit (luthier-v8-stage1 at 3155238)

Both readings had their rules committed first (5ca43f5, 19:44) and change no notes (song 54 byte for byte, checked here).

- **749.195, answered: the pitch ceiling (956) takes song 50's pool.** 5 of 29 builds pass it (the eight other songs 0.44 to 0.74). The verses of the folk songs read (50, 58, 49) put about half their notes on one mid-span pitch, against a kept ceiling of 0.44. Accepted. The chosen tunes' words' fit is a draw (inside the builds' quartiles): accepted.
- **749.196, ruled: leave it.** The maintainer is right and my nit was wrong in substance: where a rule removes the octave, the pitches past it keep their own kept odds, and passing them the octave's share would offer them the whole bin again (749.192 in small). My line of 1 in 1,000 was the wrong test. Putting it to the session rather than overriding the rule silently was right. Closed.

### 749.197 Folk verses that pile on one pitch (reading first)
**Problem.** The verses of songs marked folk (50, 58, 49, and 61) put about half their notes on one pitch; 956 passes most of those builds over, and song 50 is left a pool of 5.
**Fix.** A reading first, rule committed before it: how kept folk songs' verses spread their repeated notes over pitches, against what fix 952's folk share of repeated notes makes the draw do. Then a change to the draw if it is named, with its marks written first and read both ways.
**Check.** Written with the reading. Songs 58, 49 and 61 are where it shows; song 50 before it is made for real.

## Addendum 2: the one-pitch verses read (luthier-v8-stage1 at de4bd0d)

Rules first (145ac52, 20:00; the second pass 45fa2be, 20:18) before the result (4eef2bf, 20:30); no notes change (song 54 byte for byte, checked here); the study switches (`chord_pull`, `count_the_tail`) are absent from every record.

- **749.197, answered: the verse's harmony is the cause, not the genre.** The three songs' verses hold two chords (half the bars on one) and pile on the chords' common tone; given song 55's verse chords, their verses fall under the ceiling (20, 17, 23 builds in 100 over it). My lead from 952 was a decoy, and you said so. Accepted.
- **The kept songs say the engine answers still harmony about three times too strongly:** kept verses in the stillest-harmony quarter sit at 0.27 to 0.42 on their commonest pitch (22 in 100 over 0.44), so two-chord verses and the ceiling are both kept-like; the fault is in how the draw leans on chord tones under a chord that holds. Accepted.

### 749.198 How the draw leans on chord tones under a chord that holds (reading first)
**Problem.** Under a still harmony the draw piles on the chords' common tone (7 builds in 10), about three times as often as kept songs under the same stillness.
**Fix.** The reading proposed: the kept share of on-beat chord tones by how long the chord has held, and the figure memory (923) under one chord, rule first. Then a change to the draw if it is named, with marks written first, read both ways (749.179), and a redraw-until rule read for 749.193.
**Check.** Written with the reading. Marks to include: verses over the ceiling at or near the kept rate for their harmony's stillness in songs 50, 58, 49; living builds; words' fit within 0.02; songs 55 and 54 unchanged in their verse share. Song 50 waits for it.

## Addendum 3: the held chord read (luthier-v8-stage1 at 8321019)

Rule first (0b6b04d, 20:34) before the result (c4251af, 20:46); no notes change.

- **749.198, answered: the engine sings a chord tone on the beat 88 to 95 times in 100; kept songs 64** (10th to 90th by song 0.44 to 0.83), and kept songs do not change with how long the chord has held. Three rules do it: `again()` snaps a line sung again to chord tones (712), `pitches1()` weighs chord tones 2.6 to 0.3 on the beat (650), and the clash rule (833). The one-pitch verses are a symptom. Accepted.
- **The session's view on loosening 650 and 712, asked for: yes.** Every song read sits over the kept 90th, so this is a fault of fit to kept songs, not a style. But it reaches every song, so build it in steps, each read both ways (749.179), and give the winner a sealed song.

### 749.199 On-beat chord tones at the kept rate
**Fix, in order.**
1. **The check, now:** a kept soundness reading of on-beat chord tones (the record already reads the figure), reported in the three-song rule and deciding nothing yet. No notes change.
2. **Trial forms, each alone and then together, marks first:** (a) in `again()`, snap a note to a chord tone only where the clash rule would; (b) the on-beat pull from a kept table (kept middle 0.64) in place of 2.6 and 0.3. 833 stays as it is.
3. **A sealed song once,** for the form that passes the seen songs, its ledger line first. The writer names which (songs 64 and 65 are sealed and unreserved).
**Check (for each form).** On-beat chord tones inside the kept 10th to 90th in every song; verses over the 0.44 ceiling at or under 30 builds in 100 in songs 50, 58, 49; living builds above v50's; builds' words' fit within 0.02; the chosen tunes at or over their floors; soundness and pools as for 964; song 50's pool at 10 or more. Added by the session: the melody's surprise at or under the popular-corpus median (749.18, 749.20), so loosened notes do not turn into wandering ones; and clashes against the chord no more than v50's, since fewer chord tones on the beat must not mean more notes a semitone off one.

## Addendum 4: the tie to the chord, tried and not built (luthier-v8-stage1 at 1e0a820)

The form and nine marks (ce971b2, 20:49) and the two weights, fitted once as the rule allowed (a745e7a, 20:51), before the result (129ffa4, 21:05). No notes change with the switch off (song 54 byte for byte, checked here).

- **Mark 2 holds, mark 1 fails; not built. Agreed.** On-beat chord tones fall to the kept rate (0.53 to 0.62; kept 0.64), but verses over the 0.44 ceiling stay at 50 to 54 in songs 50, 58, 49 and rise in songs 55, 54, 59 (to 33, 42, 38).
- **749.199, the finding: the tie was moving the tune, not holding it.** Left to itself the draw sits on one pitch near its register's centre (the middle verse 0.38 to 0.46 on its commonest pitch; kept 0.31). Accepted. The reading of the switches in `held_chord` that took the three songs' fall for the cure was a fair reading that this test corrected.
- **This joins 749.165 and 749.170.** The plain-and-pink study found kept songs that pile notes on three pitches are plainer and whiter (rho −0.45 each), and the region was left as a change to the draw. 749.198 (the chord tie), 749.170 (three-pitch concentration) and this are one item now.

### 749.200 How the draw spreads a verse over pitches (reading first)
**Problem.** The draw concentrates a verse on one pitch near its register's centre (0.38 to 0.46 against kept 0.31), and the chord tie had been hiding it; with the tie loosened to the kept rate, the one-pitch verses spread to every song.
**Fix.** The reading proposed, rule first: how kept verses spread their notes over pitches (the share on the commonest one, two and three; where in the span they sit) against the draw, and which weight sets it (927's register pull, 846's degrees, 923's memory). Then a form for the draw; then the chord tie (749.198's form) with it, never alone.
**Check (for the form, written before any run).** The verse's commonest-pitch and three-pitch shares inside the kept 10th to 90th in every song; verses over the 0.44 ceiling at or under the kept rate for their harmony's stillness; on-beat chord tones inside the kept 10th to 90th once the tie is added; the melody's surprise at or under the popular-corpus median; clashes no more than v50's; living builds, words' fit within 0.02, floors, soundness and pools as for 964; song 50's pool at 10 or more. Read both ways. The winner meets a sealed song the writer names (64 or 65).

## Addendum 5: run 06 checked, and the draw's centre read (luthier-v8-stage1 at 770bbf7)

No notes change (the engine's files are untouched since 1e0a820). Each reading's rule came before its run (b1f0625, 07:40; 625994a, 07:50; result 770bbf7, 07:56).

- **Judging research run 06: the check is accepted.** The sources are real, the fresh table agrees with the maintainer's own (312 of 312), and the order held on the research branch. R06-1 done, R02-3 mended (703 of 2,769 Hooktheory "originals" are not the first performers), R06-2 agreed, R06-4 blocked here too. **R06-5, the power floor of 0.2 for counted tests: agreed**, and it should bind the engine's own readings with several marks as well.
- **749.200, answered: no single weight is the cause.** Many pulls toward the likely note, each matched to its own kept margin, together give verses about half the kept variance. Accepted; it is the root under 749.165, 749.170 and 749.195 to 749.199.

### 749.201 The design, the session's view
1. **(a) first, and alone.** The gap is mostly between lines (builds 0.70 to 1.20 semitones against kept 1.54); within lines the builds are near kept (1.91 to 2.32 against 2.34). Drawing each line about its own centre addresses most of it.
2. **The line centres with kept structure, not as noise.** Before (a) is built, read how kept songs move their line heights within a part (how one line's height follows the last, where the highest line falls, whether the last line comes back down), and draw the centres from that. Independent draws would add white noise between lines, which is the plain-and-pink concern again.
3. **(b) only if (a) leaves the within-line spread short,** and then fitted on trial runs with the gates off, or read both ways (749.179); no draw-until rule (749.193).
4. **(c) the chord tie only with them, never alone** (749.199).
**Marks, added to the maintainer's.** The between-line spread of a verse's line heights inside the kept middle half, and how one line's height follows the last inside the kept 10th to 90th; the chorus's lift over the verse kept (838 is already the largest killer, and moving verse lines will meet it); the melody's surprise at or under the popular-corpus median; clashes no more than v50's; the range floors and the planted peak's range kept. The winner meets a sealed song the writer names (64 or 65).

## Addendum 6: line heights tried, the join read, and a ladder proposed (luthier-v8-stage1 at 4c27445)

Rules before runs (9879cb0, 08:05, then 37e3877, 08:11; the join's rule before its result, 4c27445); no notes change with every switch off (song 54 byte for byte, checked here).

- **749.201 (a), line heights from kept contours: fails marks 1 and 3; not built. Agreed.** The session's advice to draw the centres with kept structure was followed and was not enough.
- **749.202: accepted, and it is the clearest thing yet.** The centres moved 2.5 semitones and the lines a tenth of that: a line sits where the last one left off, not where its register says. Kept line heights are nearly free of each other, with a shape by part on top.
- **The join is not the cause: accepted.** The description after it is the lead worth keeping: a kept line starts under its middle and ends further under it (an arch that comes home low); the engine's lines start over their middle and end at it, and are narrower (5.0 against 6.5).

### 749.203 The ladder: the session's view, yes
Six guessed causes since 749.195, each wrong or only a part: stop guessing and take the engine apart in order. Approved, with four additions:
1. **Both directions.** Beside the ladder up (each part added in the order applied), read the full engine with each part taken out alone. A part that only matters beside a later one shows in the second and not the first. Name a rung when either reading names it, and say which.
2. **The step's size beside the rule.** The rule (inside the kept middle half before, outside after, in four songs of six) can name nothing if the barest draw is already outside, or if one rung pushes a figure out and a later one pulls it back. Report every rung's step on every figure, toward or away from kept, so the size of each part's push is seen even where nothing is named.
3. **The line's arch as a figure:** where a line starts and ends against its middle, and its range. It is the one description that separates kept lines from the engine's most plainly.
4. **The switches prove themselves first.** With every switch off, songs 54 and 55 byte for byte, so no switch draws from the random stream when off. The power floor (R06-5) applies to the rule's counting.

Then one change, to the rung or rungs named, with its marks first and a sealed song (64 or 65) to decide.

## Addendum 7: the ladder (luthier-v8-stage1 at d142513)

The rule (d0ca36c, 08:29) before the runs (d142513, 09:04); the switches prove themselves (songs 54 and 55 byte for byte with them absent; song 54 checked here). No notes change.

- **749.204, the finding: borrowing (818) sets the lines' heights.** Up the ladder, adding it drops the spread between a verse's lines from 2.4 to 0.97 (kept 1.54) and the first notes' spread from 2.94 to 1.54 (kept 2.76); taking it out of the full engine restores 2.45. Its step is five times any other part's. It is not named by the letter of the rule, because the spread just before its rung sits a hair over the kept middle half (2.40 against 2.38): exactly the case the session's second addition was for. Accepted as the finding, with that said.
- **Named by the rule: figure memory (923) narrows the line** (within-line spread 2.17 to 1.90; a line's range 6.0 to 4.75). **The chord's pull overshoots** on-beat chord tones (0.46 before, 0.86 after; kept 0.64). **The share on the commonest pitch is a sum** (register, chord, again, +0.06 each). Accepted.
- **The reading:** the bare draw ranges as kept songs do. The engine reaches the kept share of repeated figures by singing them again at the same pitch, where kept songs often repeat a figure at another height.

### 749.205 A borrowed figure sung at a kept height
**Fix, in order.** (1) The kept reading, rule first: of lines that sing an earlier line's intervals again, how many at the same pitch and how many moved, by how much and in which direction, **counted apart** for a section's own returns (a chorus line coming back, a title line), for a figure borrowed into a new line (what 818 does), and by part. (2) Then the form: a borrowed line (818 only, not a section's returns) sung at a kept height, moved by scale steps so its intervals stay diatonic.
**Marks (written before any run).** The spread between a verse's lines and of their first notes inside the kept middle half; the share on the commonest pitch lower in four songs of six and none over 0.44's ceiling more often than now; the repeated-figure share kept (818 was built to give it; moving must not lose it); clashes no more than v50's, since a moved figure meets other chords; on-beat chord tones no further from kept than now; the plain-and-pink figures (surprise, the two DFA readings) no worse, since repetition is where a tune's long-range structure lives; living builds, words' fit within 0.02, floors, soundness and pools as for 964. Read both ways. Then a sealed song (64 or 65).
**Waiting behind it:** figure memory (923) and the chord tie (749.198), each with its own rung's figures.

## Addendum 8: how a kept line repeats (luthier-v8-stage1 at b7e2fed)

The rule (fd8ddc7, 09:42) before the result (b7e2fed, 09:45). No notes change. **Numbering:** the maintainer's "749.204" here is a new finding, 749.206 (749.204 is the ladder's borrowing finding).

- **749.206, the finding: kept verses repeat the line before or two before in 11.5 lines of 100, and 82 of 100 such repeats are at the same pitch** (choruses 89). Neither mark is met; not named. Accepted. **"A borrowed line at a kept height" is withdrawn, and rightly:** the session's lead that kept songs often repeat at another height was not grounded. Only songs 58, 50 and 49, the one-pitch-verse songs, repeat over the kept 75th.
- **The repeat measure, checked.** Sound in its main parts: scale steps make a moved figure the same figure; the height is the middle difference; kept notes are one to a syllable (50,444 notes, 50,444 syllables), as the builds' are once melisma seconds are dropped, so the two sides are read alike. Three edges to report, not to retest:
  1. **Alignment from the first note** misses a repeat that gains or loses a pickup, which kept songs do all the time (fix 772 drops one on purpose). Read the kept repeat share again with the best of three alignments (offset 0, +1, −1), as a description.
  2. **Short lines** must agree in every interval (four notes give three intervals, and the ceiling of 0.8 × 3 is 3). Say how many lines that touches.
  3. **The window** is a part's own lines within one section; a verse line repeating the first verse's is not counted. That fits 818, which borrows within the part; say so where the figure is quoted.
- **The next reading, agreed:** a line's height against the line two before it, repeats and non-repeats apart, kept against built. Add the first note's height beside the middle's (the ladder's sharpest gap was in first notes, 1.54 against 2.76), and read lines that 818 tried to repeat and then altered (songs 55, 54, 59) as their own group: if they keep their source's height, that is where the heights are pinned.

## Addendum 9: the line repeats counted apart, and the borrow at the kept rate (luthier-v8-stage1 at 0e6b213)

Every rule before its run (eef45c1 and 8594fb6 before ab65405; 8410677, 09:56, before 0e6b213, 10:15). No notes change with the switch off (song 54 byte for byte, checked here).

- **749.206, counted apart: accepted.** Kept borrowed figures are 81 in 100 at the same pitch, so 749.205's step 2 is withdrawn. Named instead: a fresh verse line sits within a step of the line two before it in 0.51 to 0.76 of the builds' lines, against kept 0.36, and turning the borrow off brings it to 0.19 to 0.38. The borrow holds the height two lines back. Addendum 8's three edges are answered and tabled (kept repeats 0.169 in verses and 0.208 in choruses with the best of three alignments, 0.116 and 0.161 strict).
- **749.207, the borrow at the kept rate: the marks are read rightly, and it is held.** Four of six clean marks met (heights, spreads, the commonest pitch lower in six, the figure share over the kept 25th, living builds). Missed: verses over the ceiling in songs 50, 58, 49 at 46, 43, 35 against 30; and clashes +0.23 and +0.21 a hundred notes in songs 55 and 49 against a margin of 0.2. The second miss is narrow and the first is not, and both are misses. Taking the whole engine and a sealed song now on rewritten marks would be writing the marks after the result.

### 749.208 What "sing it again" alters (the session's advice: (a))
**Why (a).** At the kept chance the heights come right, but true verse repeats fall to 1 to 8 in 100 (kept 11.5): `again()` alters a borrowed line until it is no longer a repeat, and part of what it does is snap its on-beat notes to chord tones (712), one of the three pulls the ladder found under the one-pitch verses (749.204). So the same step may give the kept rate of true repeats, lower the ceiling count, and cut clashes, where a borrowed line now meets other chords freely. It is also the reading your own prediction named as next.
**Fix.** A reading first, rule committed before it: for borrowed lines, which notes `again()` changes and why (fitting to new syllables, the pickup rule 772, the chord snap), how many leave the line no longer a repeat, and the same counted on kept repeats (how kept songs vary a repeated line). Then a form: a borrowed line sung as a true repeat at the kept rate, its notes changed only where the syllables or a clash demand. Use the kept share with the best of three alignments (0.169 verse, 0.208 chorus) as the chance, since it counts kept repeats that gain or lose a pickup.
**Marks.** 749.207's six, unchanged and written before the run, plus: true verse repeats inside the kept middle half by song. Then the whole engine and a sealed song (64 or 65), the writer naming which.

## Addendum 10: what "sing it again" changes (luthier-v8-stage1 at 7226864)

The rule (ec359d1, 10:17) before the run (7226864, 10:20). The engine's files are untouched.

- **749.208, answered: the count differs.** 70 in 100 of the builds' borrows land on a line whose syllable count is not the source's, and only 10 in 100 of those stay repeats (25 by the best of three alignments); they are 77 in 100 of the borrowed lines that end up not repeating. The chord snap is second (15). Kept songs agree from the other side: a nearby pair of verse lines with the same count is a repeat 27 times in 100, an unequal pair about 5 (choruses 42 and 6), and same-count pairs, 15 in 100 of verse pairs, hold 47 in 100 of verse repeats. Accepted.
- **The classification, checked.** First cause that applies, in the order count, onsets, pitch step, is sound as a first reading, and count first is the right order, since a changed count forces the refit. But a first-cause table hides overlaps: a line whose count differs may also have been snapped. Add, as a description, the two-way table of count difference by chord snap for the non-repeats, and a counterfactual on the same draws: `again()` with the snap off, so the snap's own share is seen apart from the count's.
- **The form, agreed:** the borrow's chance by the count's difference and the part, from the kept table, so a line is borrowed where kept songs repeat (lines of the same count) and seldom where a refit would leave a pinned non-repeat. The marks of `studies/borrow_kept/PREDICTION.md`, unchanged, plus true verse repeats inside the kept range by song. Both readings, then a sealed song (64 or 65), the writer naming which. The chord snap (15 in 100) waits for 749.198, after this.
- **For the writer, and the lyric side:** kept songs bring a line's tune back mostly when the line has the same number of syllables as the one it echoes. That is a craft note as much as an engine one: a lyric line meant to share a tune should match its partner's syllable count.

Next finding 749.209; next fix 965.

## Addendum 11: the borrow by the lines' lengths (luthier-v8-stage1 at 4bf735a)

The rule (20b921d, 10:26) before the run (4bf735a, 10:48). With the switch off, songs 54 and 55 come out byte for byte: checked here, 120 builds each, branch against 559e156.

- **749.209, the marks read rightly.** Rechecked from `count_a.json` and `count_b.json`, all six songs. Form 2 meets marks 1, 2, 4, 5, 6 and 7, and misses mark 3's third part: over the 0.44 ceiling 46.3, 45.5 and 37.3 in 100 in songs 50, 58 and 49, against 30. Form 1 misses that (52.1, 36.9, 38.5) and the clash mark in song 55 (+0.22 against +0.2). The choice rule between the forms does not arise, since neither meets all seven.
- **Mark 2's range is quoted wrongly in the rule.** 749.207's prediction gives the kept middle half as 1.08 to 2.11, then says to use `studies/ladder/kept.json`'s figures, whatever they are, and that file gives 0.863 to 2.377. By the file, mark 2 is met in six songs; by the quoted figures, in three (form 2) or two (form 1). The file governs, as the rule said. Correct the figures in the prediction's text. And watch the spread in the whole engine: it has gone from under the kept range (0.67 to 1.28) to 2.23 to 2.30 in songs 55, 54 and 59, near the top.
- **Two more readings.** The true repeat helps everywhere but song 58, where it lifts the share over the ceiling from 36.9 (form 1) to 45.5. Song 49's true verse repeats, 0.182, sit near the kept edge of 0.195. On-beat chord tones are 0.81 to 0.90 in every song, past the kept 75th (0.73), so the chord is where the rest of the one-pitch verses lives.
- **Advice: keep the mark at 30.** Form 2 already beats v50 over the ceiling in all three songs (65, 56, 56 down to 46, 46, 37), so "no worse than v50" would be a mark it cannot miss, and it would spend a sealed song on a fix that does not yet mend the fault it was built for. Putting the question was right, since the prediction named it before the run.
- **Ruled (the writer, 26 November): option C.** Read form 2 (`LUTHIER_BORROW_KEPT=count_true`) through the whole engine now, on the seen songs only (55, 54, 58, 49, 50, 59), against 749.207's whole-engine marks 7 to 10, with mark 2's spread watched. Alongside it, try the chord tie (749.198) on top of form 2 in the clean reading, rule and marks written first, the ceiling mark in songs 50, 58 and 49 still 30 in 100. No sealed song until the 30 mark is met. Song 66 ("They Did the Right Thing", banked today, unrun) is reserved for this fix: it is the fresh test song once the mark is met, unless the writer names 64 or 65 instead.

Next finding 749.210; next fix 965.

## Addendum 12: settled on the thread, and v51 merged (main at bebec43, branch at eb6e867)

From 11:30 on 26 November, the two sessions talk in `coord/` (rules in `coord/THREAD.md`), at the writer's request. Each item below was checked there, rule before run and figures against the json. The v51 paper (`reports/Luthier_v51.docx`, Window 208, Module 27.132, Tables HR to HT) records them, with nothing built. The branch is merged: switches off, songs 54 and 55 are byte for byte their committed records (1,000 builds each), and `--check` passes.

- **749.209, form 2 through the whole engine (seen songs, within ruling C).** Pools, living picks and song 50's pool all improved. Marks 8 (words' fit, two-sided) and 10 (surprise on one chosen tune) are missed as written. Pitch scaling became a mark of its own.
- **749.210, the chord tie on top of form 2.** Far nearer than either part alone. The ceiling in songs 58 and 49 came under 30; song 50 was at 35.3. Four marks of eight were missed narrowly.
- **749.211, where the pair's clashes arise.** The rule named the fresh line. As description: the rise is blue notes (846), and clashes on other notes fall. The clash mark for later runs excludes the blue notes 846 allows, with a blue-note mark of its own.
- **749.212 (standing, v50).** Song 55's returning lines clash 1.15 times per 100 notes: a line sung again meets another chord, and `again()`'s clash rule finds no chord tone in reach.
- **749.213, the pair through the whole engine.** Five marks of seven. Surprise (now read on the builds) and pitch scaling (songs 54 and 59 over 1.02) are missed. On the refitted specs the ceiling is under 30 in all three hard songs.
- **749.214 to 749.216, looking for the cost.** By bands, the slope over 8 to 16 notes is high and the joins are small. A join form fixed the joins but not the slope, and failed its own marks. It stays a switch, off.
- **749.217, sealed song 66.** Six marks of seven held. Pitch scaling failed (1.062 against v50's 0.912, margin 0.03). The pair is not built, and song 66 is spent.
- **749.218, direction inside a line.** Nothing named, so the line closed by the stopping rule. Standing finding: the engine's lines change direction more than kept lines, under v50 and the pair alike.
- **749.185, the loop gate with a chance.** All four draft marks met (verses at or under the kept median 52.9 in 100; over the kept 75th 26.7; plain loops 31.6; stage 4 within 0.02). It sits behind `LUTHIER_LOOP=chance`, off. Song 63's run awaits the songwriting session's word on the thread.

Switches added this version, all off: `LUTHIER_BORROW_KEPT`, `LUTHIER_CHORD_TIE`, `LUTHIER_JOIN_MOVES`, `LUTHIER_LOOP=chance`. Fixes still end at 964. For v52: fixes from 965, findings from 749.219.

## Addendum 13: v52 merged, fix 965 (main at 5dd5ba8)

- **Fix 965, the loop gate with a chance (749.185), built as a setting.** It is now what a lyric's `"chords": "loop_less"` means; `LUTHIER_LOOP=median` and `gentle` are kept for studies. Song 63 was run once by the switch, with the lyric file untouched. Its marks held: pool 10 (exactly), words' fit 0.361 against the floor of 0.152, and the plan's verse and bridge under the kept 75th. Song 63 is spent.
- **The bare pass, weighed and accepted.** Song 63 on v50 without the form gave pool 14 from 176 living builds; with the form, 10 from 104. The form redrew nothing in the chosen plan, so the different chord draft (7 against 9) comes from the draw. One song can't separate that from the form. A cheap description is asked for before any lyric uses the setting: the six seen songs written through with `loop_less` on and off, living builds and pools. If pools fall under 10 in two or more, the setting is read again.
- Paper: `reports/Luthier_v52.docx` (Window 209, Module 27.133, Table HU). Switches off, songs 54 and 55 are byte for byte, and `--check` passes.
- **Order of the open items:** 749.212 first (song 55's returning lines clash; it's in the engine every song uses), then 749.171, then 749.144, 749.147, the hymn items 749.148 to 749.152, and 749.163.

For v53: fixes from 966, findings from 749.219. A new list Doc starts with the first new finding.

## Carried, open

- 749.212 (song 55's returning lines clash), the short runs one way inside a line, the pair's slope over 8 to 16 notes (lines' heights further apart than kept: not yet read in a form).
- 749.171 inside a one-bar line; rhythm scaling leans low.
- 749.144, 749.147, 749.148 to 749.152 (hymns), 749.163. (749.165 and 749.170, the region, are now part of 749.200.)

## Closed

- 749.182 (the leaps: 749.186, mended by 964), 749.189 and 749.191 (the plant's line and its centre: not the fault), 749.192 (fix 964), 749.193.
