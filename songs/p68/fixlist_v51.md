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

Next finding 749.206; next fix 965.

## Carried, open

- 749.185 the loop gate with a chance (song 63 reserved).
- 749.171 inside a one-bar line; rhythm scaling leans low.
- 749.144, 749.147, 749.148 to 749.152 (hymns), 749.163. (749.165 and 749.170, the region, are now part of 749.200.)

## Closed

- 749.182 (the leaps: 749.186, mended by 964), 749.189 and 749.191 (the plant's line and its centre: not the fault), 749.192 (fix 964), 749.193.
