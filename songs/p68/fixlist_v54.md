# Luthier list for v54 (since v53)

Started 27 November 2026. Findings from 749.226. The settled items up to v53 are on `fixlist_v53.md`.

## Songs
| Song | Folder | State |
|---|---|---|
| 67, A Door in the Coral | p77 | locked, banked, unrun; made for real once the drafting fix lands |
| 68, Save Me from My Muse | p78 | locked, banked, unrun; a 3/4 punk waltz for high tenor; made for real once the 3/4 draw reads well; the writer chooses its path now that the v54 draw has closed (27 Nov) |

## 749.226. In 3/4 the plan gives every line two bars
- **Problem:** a 3/4 lyric's plan (`spec.slots`) gives every line two bars, whatever table the draw reads. So a line's density is fixed before the draw begins: eight syllables in two bars of 3/4 is four notes a bar, and seven is three and a half.
- **Evidence:** the 3/4 trial on song 53's words (`studies/other_metres/PREDICTION_trial_3_4.md` at 9deaabc, before the run; `RESULT_trial_3_4.md`, `trial_3_4.json` at dfc493d). Against Wikifonia's middle half (2.06 to 2.70 notes a bar; onsets on a beat 0.731 to 0.939; first-beat stress by song 0.583 at the 25th), the lead-sheet arm made 3.29, 0.571 and 0.306, and the Essen arm 3.5, 0.576 and 0.306. The arms are nearly the same, so the table isn't the cause. Living builds aren't the problem (610 and 566 of 1,000), unlike 6/8.
- **Fix (proposed, to be tried rule first):** in 3/4 a line's sung bars are whichever of 2, 3 or 4 puts its syllables a bar nearest the table's median. A line of three sung bars is padded to a four-bar phrase with a held last note or a rest, and the draw reads a four-bar line as two windows. The maintainer's first version rounded to 2 or 4 only. That would leave 6- and 7-syllable lines, every line of song 68, in two bars.
- **Check:** marks P1 to P7 in `coord/songwriting.md` (27 Nov, 10:58 ET); byte for byte on 54, 55 and 52 with the switch unset. One form only.
- **Read (27 Nov):** marks 740bb4e, result 02e75c3 (`RESULT_plan_3_4.md`, `plan_3_4.json`). P1 to P5 met: every line three sung bars in a four-bar phrase; 731 living, pool 268; 2.09 notes a bar over the sung phrases; onsets on a beat 0.893; first-beat stress 0.622. P6 missed: the commonest pitch 0.424 and 0.390, against 0.287 and 0.280 for the Essen arm. By the stopping rule the 3/4 draw closes for this version; the form stays a switch (`LUTHIER_PLAN_3_4`), unset. The density part of the fix works; 749.227 is what's left.
- **Read in 6/8 (27 Nov):** marks 2f76d96, result c5cc225 (`plan_6_8.json`), on song 52's words. Q1, Q2, Q4 and Q5 met: 248 living and a pool of 37, where v53 had 22 and none; onsets on the beat 0.467 and on the first beat 0.242; 731's median 0.551. Q3 missed: 3.20 notes a bar against Essen 6/8's middle half of 3.60 to 4.33, because the padded fourth bar overshoots folk density (the lead sheets' 6/8 run 2.86 to 3.95). 6/8 closes for this version beside 3/4. For v54: bars from the table's density in both metres, with the padded bar chosen by style.

## 749.227. In 3/4 the tune's range and pitch count are under the kept waltzes' 10th
- **Problem:** in 3/4 the engine writes a narrow tune, whatever table it reads: a range of 9 semitones and 6 pitches, against the lead-sheet waltzes' 10th of 12 and 8. The commonest pitch (0.32 whole tune, against a 90th of 0.31) and the repeated figures (0.86, against a 90th of 0.78) follow from that. The 4/4 engine has a range floor and a register plan read from kept songs; 3/4 has neither.
- **Evidence:** the plan-form result (`plan_3_4.json`, 02e75c3) against the lead sheets' own by-song figures (`leadsheet_waltz_figures.json`, 4f0ff4c; 538 songs: range 12 / 14 / 19, distinct pitches 8 / 11 / 14.3, commonest pitch 0.167 / 0.225 / 0.313, bars on a rhythm already sung 0.706 / 0.846 / 0.918). Both arms read range 9 and 6 pitches. The rhythm's repetition (0.90) sits between the kept 75th and 90th, so it is a waltz's.
- **Fix (to be specified rule first):** a range floor and register plan for 3/4, read from kept waltzes of about the same length (by bars sung), since song 53 is a short carol and most lead-sheet waltzes are full songs with a bridge.
- **Check:** marks read against kept waltzes of similar length, on song 53's words. Song 68 is the real test after it.

## 749.228. Four-bar phrases break the join before a copy
- **Problem:** under the plan form, the join before a copied line (780) turns builds away.
- **Evidence:** `plan_6_8.json` (c5cc225): 780 took 455 of 1,000 builds in 6/8.
- **Fix (to be specified rule first):** the join reads a copied four-bar phrase as the line it copies, padded bar included.
- **Check:** 780 deaths under the plan form no higher than v53's 4/4 share on songs 54 and 55.

## 749.229. A title line keeps its two bars under the plan form
- **Problem:** a chorus title line short enough to round to two bars keeps them. In 6/8, five stressed syllables in two bars have four beats to land on.
- **Evidence:** `plan_6_8.json`: 840 still took 228 of 1,000 builds. The title line ("you're just in the room next door", 7 syllables, 5 stressed) put half or more of its stresses on a beat in 0.314 of its windows, and all of them in none.
- **Fix (to be specified rule first):** a title line's bars are chosen so that its stressed syllables can land on beats, not by syllables a bar alone.
- **Check:** 840 deaths in 6/8 under a tenth of builds; the title line's stresses on a beat inside the kept range.

## 749.230. The chord writer can give a bridge too few chords
- **Problem:** a bridge on one chord, or with one change in twelve bars, is under the kept bridges' 10th of distinct chords (2.2).
- **Evidence:** the bridge reading (`studies/section_ceiling/RESULT_bridge.md`, `bridge_read.json`, rule 048f679 before the run). The two worst bridges are the two thinnest: song 66's one chord in eight bars (over in 82 builds of 100) and song 61's two chords in twelve (49). Bridges with four to eight chords are still over in 21 to 42 of 100, against the kept 10, so a thin plan worsens the ceiling but does not cause it. Nothing was named by the rule.
- **Fix:** a fact about the chord writer, for v54: a bridge's distinct chords no fewer than the kept 10th.
- **Check:** distinct chords per bridge against kept bridges, on every engine song in v54.

## The 3/4 repair package (749.226 to 749.229), first reading (27 Nov)
- **Marks:** R1 to R8 (`coord/songwriting.md`, 14:08 ET), read against the 52 lead-sheet waltzes of like length (a third either side of 128 bars of sung phrases). Rule file `PREDICTION_package_3_4.md` (1f890fd), result 5423a1f (`package_3_4.json`).
- **Met:**
  - R1, R2, R3: 636 living, pool 171; 2.09 notes a bar; 0.832 on a beat; first-beat stress 0.622.
  - R4's range: 14.
  - R6: figures again 0.825; rhythm again 0.900.
  - R7: 60 to 74, no leap.
  - R8: no deaths on 780 or 840.
- **Missed:** R4's pitch count (8, against 9) and R5 (commonest pitch 0.313, against 0.275).
- **Cause, as the reading names it:** the register plan gives the room but leaves the centres at 64, so 75 notes in 100 fall on four pitches and 7 in 100 above 69.
- **Untested here:** the title's room and the copy's join change nothing on song 53's words. Song 68 will read them.
- **Revised form (the last for v54):** B, which moves each section's centre to the middle of its floor and new top. Marks unchanged. If it misses, the 3/4 repair closes for v54, and a pick floor on all three figures becomes a candidate for v55.

## The 3/4 repair package, second and last reading (form B, 27 Nov)
- **Form:** each section's centre moved to the middle of its floor and new top (867290a, before any code or run). Result: 6ee8ebf (`RESULT_package_3_4_b.md`, `package_3_4_b.json`).
- **Met:**
  - R4: range 17, 11 pitches.
  - R5: commonest pitch 0.269.
  - R1, R2, R6, R7, R8: 530 living, pool 139; 2.09 notes a bar; figures again 0.789, rhythm again 0.906; 59 to 76; no deaths on 780 or 840.
  - Living builds meeting R4 and R5 together: 23.3 in 100, up from 10.0.
- **Missed:** R3, first-beat stress 0.469 against 0.583.
- **Closed for v54,** unbuilt, switches unset. Song 68 stays banked.
- **What the miss showed:** the earlier passes on first-beat stress (P5, and the first reading's R3, both 0.622) were the pick's, not the form's. Across living builds the median is 0.54 under both forms. From now on, a form's marks read the living builds' median beside the chosen tune for every figure the form claims to move.
- **Stands as read, for v55:** bars from density (749.226); centres moved into the room (749.227, form B).

## 749.231. In 3/4 the draw scores a stressed syllable on any beat, not on the bar's first
- **Problem:** the draw rewards a stressed syllable on any beat. In 3/4 the kept lead-sheet waltzes put stresses on the bar's first beat more often than the engine's tunes do.
- **Evidence:** `package_3_4_b.json` and the first reading. The living builds' first-beat stress has quartiles 0.47 / 0.54 / 0.62 under both forms, against the kept by-song 25th of 0.583. The plan form lifted it from 0.31 (v53) to a median of 0.54.
- **Also in 6/8 (27 Nov):** the 6/8 repair's first reading (27a35f0) puts stressed syllables on the bar's first beat at 0.261 chosen and 0.256 median, under the 6/8 lead sheets' by-song 10th of 0.324 (median 0.509). Essen has no words, so it can't be read there.
- **Fix (to be specified rule first):** in 3/4 and 6/8, a pull to the bar's first beat for stressed syllables in the draw's scoring.
- **Check:** the living builds' median first-beat stress at or over the kept 25th (0.583), on song 53's words, with R1 to R8 held. Then song 68 as the real test.

## The 6/8 repair, second reading (27 Nov)
- **Form and result:** form 163122c, before any code or run; result 23f6bd7 (`RESULT_package_6_8_b.md`).
- **Met:** S2 to S4, on the pick and the living median (391 living and a pool of 169; 3.89 and 3.87 notes a bar; on the beat 0.450 and 0.422; on the first beat 0.221 and 0.219).
- **Missed:** S6. 840 is unmoved.
- **Stands:** bars from Essen's density, unpadded; the copy's join.
- **The writer reopened the metres work** at 15:38 ET: a miss now leads to the next form.

## 749.232. In 6/8 a title line's room is taken at its front by the line before it
- **Problem:** a long line before the title line runs into the title line's first bar. The title line then starts late and crowds its syllables into the bars that are left.
- **Evidence:** `RESULT_package_6_8_b.md` (23f6bd7). The chorus title line, given four bars, starts five eighths into its slot in three builds of four, and on its bar line in only 6 in 100. The line ahead of it has thirteen syllables in three unpadded bars. The bridge's title line starts on its bar line in 76 in 100 and does better. Four bars would land half its stresses in 0.99 of kept windows if it could start on time.
- **Fix (to be specified rule first):** the line before a title line leaves the bar line clear, or the title line's bars are counted from where it can begin.
- **Check:** 840 deaths in 6/8 under one in ten builds made; the title line's entry on its bar line in most builds; S1 to S7 held.

## 749.231 read (27 Nov): 879's rule in 3/4 moves first-beat stress at the draw
- **Form and result:** rule 5be2e5f, result d59b7e8 (`living_231.json`, `package_231.json`), on song 53's words with the plan form and form B.
- **Moved at the draw:** the living builds' median first-beat stress went from 0.541 to 0.607, past the mark of 0.583. The pick reads 0.561. Stress off the beat is 0.071, at the mark.
- **Still over:** the commonest pitch, 0.302 on both the pick and the median (form B's median was 0.299, so its pick of 0.269 was luck).
- Read as a result for the standard-or-waltz style.

## 749.233. Metre apart from style: a lyric's genre chooses its style table
- **Problem:** every 3/4 mark so far came from one style, the Wikifonia standards. If those figures become the metre's, the engine writes waltzes for every 3/4 lyric. The writer (15:52 ET): "If we let everything to that in 3/4, don't we doom the engine to writing waltzes?"
- **Evidence:** the Hooktheory clips carry metre: 600 songs in 3/4 and 778 in 6/4 (felt in two, like 6/8). By song (the 54 Discogs-joined songs in 3/4), pop in three against the lead-sheet waltz: notes a bar 2.75 against 2.33; onsets on a beat 0.68 against 0.84; rhythm again 0.55 against 0.85; figure again 0.33 against 0.60 (`hooktheory_by_song.json`, 31c8841).
- **Fix:** forms work at the level of the metre (the grid, three beats with the first strongest). Target figures come from a style table that the lyric's genre names: folk (Essen), hymn (the hymns), standard (Wikifonia), and pop, rock and indie (Hooktheory). Hooktheory has no words, so a pop lyric borrows a stress table, and the rule file says so.
- **Check:** a pop-style 3/4 trial on a spent pop or rock lyric (marks K1 to K8, 16:08 ET). Song 68 is the real test after it.

## 749.234. Lines that share a tune get different bars under the plan form
- **Problem:** the plan form gives each line its bars from its own syllables. A line that sings again a tune of a different length can't fit it.
- **Evidence:** the pop 3/4 trial on song 55's words (rule cee6e2d, result 7baa306, `RESULT_pop_3_4.md`). 982 of 1,000 builds were never made ("the syllables cannot fit the window"), leaving 10 living builds and a pool of 5. Verse 1 came out [3,2,3,2,3,2,3,3] and verse 2 [2,2,3,2,2,3,2,3]. With the plan off, 120 of 200 builds live. Songs 52 and 53 hid the fault, because their matching lines match in length.
- **Fix:** lines that share a tune share their bars, the count chosen from the median syllables of every line that will sing it. This is metre-level and holds in any style.
- **Check:** K1 to K8 on song 55's words (K6 within sections).

## 749.235. In 6/8 870's wait pushes a title line late
- **Problem:** with the line ahead ending early (749.232), the chorus title line still enters late. 870, a fresh line's kept rest, takes the room the title line was given.
- **Evidence:** `RESULT_232.md`, `package_232.json` (7baa306). Living builds rose to 719 and the pool to 329. 840 fell from 4.3 in ten to 1.3. 128 of 129 deaths on 840 have a late title line. The chorus title line is on its bar line in 28.7 builds of 100 (6 before); the bridge's in 91.4.
- **Fix:** a title line doesn't take 870's wait. A pickup before the bar line is still allowed.
- **Check:** U1 to U5 unchanged (the title line on its bar line or before it in 75 builds of 100; 840 and 780 each under one in ten); the pickup use reported.

## The deduction method: passed its check (27 Nov)
- **Rule and result:** rule with the songwriting session's bar at 5cd85c3; result 928ce91 (`RESULT_deduce.md`, `deduce_check.json`).
- **The check:** pop 3/4 = standard 3/4 × pop 4/4 ÷ standard 4/4 predicted four countable figures. All four fell inside the counted Hooktheory 3/4 middle half with the right sign, and the median error was 0.24 of a middle half (bar: 0.5).
- **The deduced table:** a pop 3/4 stress table (`trial_tables/3-4_pop_sung.stress.json`) gives stressed syllables 0.50 on the first beat, 0.29 on another beat and 0.21 off the beat. It is labelled DEDUCED, its stress cell comes from the Billboard songs, and it is to be replaced when counted.

## 749.234 read (27 Nov): shared bars make the pop 3/4 trial live
- **Result:** 93736dd (`RESULT_234.md`, `pop_234.json`), on song 55's words, genre rock.
- **Living:** 316 living builds, pool 158 (10 and 5 before). The three verses share [3,2,3,2,3,2,2,3].
- **Met on the living median and the pick:** density 2.62; range 17 and 13 pitches; commonest pitch 0.197; rhythm again within sections 0.40; figures again 0.25; voice; 840 under one in ten.
- **Missed:** K3, words' placement (749.236).

## 749.236. In pop 3/4 the stress rule doesn't decide where syllables go
- **Problem:** first-beat stress 0.24 and stress off the beat 0.35 to 0.39, against marks of 0.45 and 0.26. Both the deduced and the shrunk stress tables give the same pick and the same medians.
- **Cause, as read:** the draw takes a kept window by its count first. The pop table's windows come from songs without words, and they are syncopated.
- **Next:** read whether K3 is reachable on song 55's lines at all (an upper bound, and the bound within kept windows). If it is reachable, the form is a window scored by its kept count and its stress fit together, with the trade-off fitted on the lead sheets.

## 749.235 read (27 Nov): 870 was not the cause in 6/8
- **Result:** 93736dd, corrected at fa940fb (`RESULT_235.md`, `package_235.json`).
- **840:** hardly moved (1.2 in ten). 121 of 122 deaths still have a late title line.
- **The pickup:** the bridge's title line opens unstressed and begins before its bar line in 87 builds of 100, so the draw uses the pickup.
- **Suspected:** 818 makes the chorus title line sing an earlier line's rhythm again. Count first, then the form (a title line drawn fresh).

## 749.237. In 6/8 818 makes the title line sing an earlier line again, and late
- **Problem:** 818 sang the chorus title line again from an earlier line of its section, refitting a thirteen-syllable line's rhythm to seven syllables, so the title line started late.
- **Evidence:** the count (`counts_818_K3.json`, rule 5b0fe49 before 18f2eaa7): on time 16.7 in 100 where 818 made it (807 builds), 100.0 where it was drawn fresh (186). All 122 deaths on 840 were among the 818 builds.
- **Fix:** a title line is drawn fresh, and 818 doesn't apply to it (`LUTHIER_TITLE_FRESH=1`).
- **Check, read (141883a before 8d6aca8, `title_fresh.json`):** every 6/8 mark met on song 52, on the median and the pick. 847 living, pool 380; 840 none; 3.79 notes a bar; onsets on the beat 0.456, on the first beat 0.245; the title lines on time in every build.
- **Next:** the same package on a second, spent lyric chosen by rule, before 6/8 is called working.

## 749.236 read: K3 is reachable on song 55's lines
- **The counts:** an upper bound of 0.743 and 0.674 within kept windows, against the draw's 0.241, so the ordering is the cause (window count before stress).
- **The weight:** fit on worded songs of the same style (Billboard pop 4/4). It carries to pop 3/4 if the lead sheets show the same weight in 3/4 and in 4/4; otherwise it is deduced.

## 749.238. A dense line with no kept window at its planned bars is never made
- **Problem:** a line whose syllables have no kept window at the bars the plan gives it can't be built.
- **Evidence:** 127 of 300 builds of song 55's pop trial were never made. 102 died at Verse 1's eighth line (nine syllables in three sung bars) and 23 at its seventh (nine in two).
- **Fix (to be specified rule first):** such a line takes a bar more.
- **Check:** builds never made under 5 in 100, with K1 to K8 held.

## 749.232 revised (27 Nov): the second 6/8 lyric found the early end fitted to one lyric
- **Evidence:** song 61's words in 6/8 (choice and marks a9dec5f, result cb72f12, `second_6_8.json`). No build was ever made. All 300 traced builds stop at Chorus 1's seventh line, the line ahead of the title line (six syllables, two bars to three, with a one-bar window holding two syllables on one beat).
- **Revised form (accepted 18:22 ET):** the line ahead of a title line keeps its own sung bars, and its slot takes the extra bar as rest. Marks unchanged, read on songs 52 and 61 both. The rest's length before each title line is reported against Essen.

## 749.232 read again (27 Nov): the title entry is fixed on both lyrics
- **Form and result:** fefedb2, then 5af9e5c (`rest_232.json`).
- **Song 52:** every 6/8 mark met. 828 living, pool 328; 3.95 and 3.92 notes a bar; first-beat onsets 0.234 and 0.229.
- **Song 61's words:** the title lines are now on time, but 572 of 600 builds are never made, at five dense lines. Notes a bar (3.5) and first-beat onsets (0.171) miss.
- **The rest:** the rest before a title line runs 4 to 5 eighths, against Essen's 6/8 rests of 1 to 3 (none as long as a bar).

## 749.239. The draw is a phrasebook: where kept windows are few or none, no build is made
- **Problem:** a line's rhythm is looked up among kept windows for its syllables and bars. Where the table has no entry, the build dies. Each fix today (749.229, .232, .235, .237, .238) patched one missing entry for one lyric. The writer (18:50 ET): "We must mathematically extrapolate from what we know into what we don't, test it, then try again if we fail."
- **Fix (accepted 18:58 ET, rule first):** a rhythm grammar. A window's chance comes from the metrical level of each onset given the density, and from the step between onsets, fitted by maximum likelihood on the kept table. Kept windows stay; the grammar supplies windows where they are few or none, labelled generated.
- **Check before use:** fit on half the songs; generate for held-out cells with 20 windows or more.
  - (a) Generated readings inside the counted middle half in 9 cells of 10.
  - (b) Counted windows carry 0.60 of the generated mass.
  - (c) Three of the counted top five in the generated top five, in 8 cells of 10.
- **Tables:** run on Essen 6/8 and on the Hooktheory 3/4 pop table.
- **Then:** song 61's words in 6/8 (S1 to S7, U1 to U4, song 52 read again) and the pop 3/4 trial (K1 to K8). The rest before a title line comes from the table, inside Essen's 1 to 3 eighths.
- **First form read (27 Nov, 0b696ab before 247b5c5):** place and step, fitted on the kept windows. It missed on both tables, so it isn't used.
  - Essen 6/8: (a) 11 of 12, (b) 0, (c) 0.
  - Pop 3/4: (a) 9 of 11, (b) 3, (c) 3.
  - It gets the averages but not the rhythms. The step is blind to place, and the pickup bar (one note on the last eighth, as common as one on the first beat) is a word of its own.
- **Second form accepted (19:14 ET):** bars as words. A first bar's counted share, times the second bar given the first; conditioned on the line's syllables; chained for three and four bars. Same check.
- **Second form read (876caa2, `grammar_b_*.json`):** Essen 6/8 meets (a), (b) and (c) cell by cell in two-bar cells 4 to 11, with carry 0.65 to 0.87. It misses at 3, 12, 13 and 14. Pop 3/4 misses in the middle (carry 0.57 down to 0.28).
- **Ruled (19:50 ET, after the result, stricter):** in Essen 6/8 the grammar supplies windows only in two-bar cells 4 to 11. Kept windows only elsewhere.
- **Pop next:** the bar given the two before it, with back-off, plus a repeat at a distance of two bars.

## 749.240. A line sung again overruns its own slot, and the next line can't fit
- **Problem:** a line sung again (the lyric's "again", or 818) wasn't held to a fresh line's rule of beginning its last syllable a breath before its slot ends. The next line was left fewer grid places than it has syllables.
- **Evidence:** `RESULT_why_no_fit.md`. In song 61's words in 6/8, 286 of 286 stopped builds had the line ahead past its slot. In pop 3/4, 127 of 127. This corrects the reading at 18:50 to 18:58 ET that these builds failed for want of a phrasebook entry: the draw already has a fallback (760).
- **Fix:** a line sung again begins its last syllable inside its own slot, or is drawn fresh, and 818 doesn't apply to it (`LUTHIER_AGAIN_INSIDE=1`).
- **Read (b9e3eed before 8b9540d, `again_inside.json`):** never made fell from 572 to none on song 61's words and from 127 to none in pop. But the "again" lines drawn fresh rose fivefold (1,220 to 6,121, and 564 to 5,523), so the songs repeat less. On song 61's words, density 3.5, onsets 0.373 and 0.193, and 840 at 1.8 in ten still miss. Song 52's pick missed first-beat onsets by 0.003.
- **Next:** refit the line sung again inside its slot rather than dropping it, and add shared bars to the 6/8 package. Then song 61's density, and a count on its 840 and first-beat onsets.

## Parked, by the writer's word (27 Nov, 20:03 ET)
- **Timbre on the arrangement side:** instrument tone, brightness, distortion and how close the voice sits, measured from real recordings, for the engine's arrangements and demos. It is kept out of the "why it lasts" test on purpose, since covers change timbre by definition. The writer: "Let's wait until what we are working on works." Take it up once 3/4 and 6/8 write properly.

## 749.241. A copied line's split-off note lands past the line's limit
- **Problem:** when a copy has more syllables than its source has notes, the routine splits the widest gap. It counts the last gap to an eighth before the slot's end, but the line's limit is a breath before, so the split-off note lands past it and the "again" is drawn fresh.
- **Evidence:** `RESULT_why_again_fresh.md` (deca102). In pop 3/4, 1,319 of 7,800 tries were turned away for ending past the slot, and 377 by the join. On song 61's words in 6/8, 479 and 279 of 4,500. Every one was past by 3 to 9 twelfths, almost all where the copy outnumbered its source's notes.
- **Fix (to be specified rule first):** the gap after a line's last note is counted only as far as the line's own limit.
- **Check:** S1 to S7 and U1 to U4 on songs 52 and 61's words, K1 to K8 in pop, and the "again" lines drawn fresh at most 1,569, 1,830 and 846.

## 749.242. The page gate's evidence partly rests on TheSession, whose licence we can't use
- **Problem:** the page gate (fixes 922 and 923), a default in the built engine, was chosen partly on a study of TheSession.org tunes. That licence forbids processing with LLMs. Its table comes from the 167 kept CoCoPops songs, so no TheSession figure is in the engine.
- **Fix:** restate its evidence without the session leg. Test any part that the hymn and within-artist legs don't carry alone again on an allowed source, rule first, after the metres work. It is not removed now (nothing is built until the metres work).
- **749.241 read (a59236e before 48eff35, `split_241.json`):** song 52 meets every 6/8 mark and the 712 mark (880). On song 61's words the 712 count is met (778), but first-beat onsets (0.189 pick) and 840 (1.71 in ten) are short. Pop 3/4 meets every figure but K3; its 712 count is 1,023 against 846.

## 749.243. The plan can make a section denser than the table allows
- **Problem:** the density rule works line by line and never reads a section's total. Song 61's Verse 1 runs 4.58 syllables a sung bar, over Essen 6/8's 75th of 4.33. A bar has one first beat, so the section's first-beat onsets can't exceed 1 in 4.58, which is 0.218, just above the mark.
- **Evidence:** count (b) (`RESULT_count_b.md`, 672421a).
- **Fix (rule first):** the plan reads each section's total. Where a section would be denser than the table's 75th, its densest line takes a bar more until the section is inside. Tried together with 749.231's stress score in 6/8 (borrowed from the 99 worded 6/8 lead sheets until Lieder is counted).
- **Check:** S1 to S7 and U1 to U4 on both 6/8 lyrics, marks unchanged. Each switch off in turn for 200 builds.

## 749.244. A title line is drawn only among windows that pass 840's own test
- **Fix:** a title line is drawn only among the windows that put half its stresses on a beat, wherever any exist. 749.243 is read from both ends (each section inside the table's middle half).
- **Read (5672d40 before eb00414, `title_840.json`):** both 6/8 trial lyrics meet every mark, on the pick and the living median.
  - Song 52: 814 living; 3.90 notes a bar; first beat 0.214 and 0.221; 840 none.
  - Song 61's words: 822 living; 3.607 notes a bar; first beat 0.218 and 0.242; 840 none.
  - No title line found every window failing.
- **Seen ground:** five forms were shaped on song 61's words tonight. A held-out third spent lyric goes before song 69, with the silence before a title line added as a mark (at or under Essen 6/8's 90th rest).

## The 6/8 held-out reading (5e860bb)
- **Result:** songs 52 and 61's words meet every mark, silence included. The held-out song 50's words, read once, miss first-beat onsets (0.198 on the pick, 0.204 on the median, against 0.211).
- **The count (449bf61):** lines begin after their bar line in 0.22 to 0.39 of cases, against Essen's 0.081. A fresh line lands on beat one in 92 bars of 100; the late lines come from 870's wait and from pickup-shaped windows, and copies carry them on.

## 749.245. Outside 4/4, 870's wait draws from 4/4's rests
- **Problem:** 870's wait picks from a fixed list of rests (12 to 48 twelfths), which are 4/4's kept figures. In 6/8 that's a third of a bar to a bar and a third, while Essen's own rests are 1 to 3 eighths.
- **Fix:** outside 4/4, the wait draws from the table's own rests, at the table's rate, or is off where the table has none.

## 749.246. A window whose first bar holds only a pickup is sung a bar late
- **Problem:** Essen's 691 two-bar windows whose first bar holds one note on its last eighth are a pickup caught a bar early. The draw sings them as the line's first bar, so the line starts late.
- **Fix (preferred):** read such a window as a pickup before the bar line followed by its second bar. Otherwise, don't offer it as a line's rhythm.
- **Check (749.245 and 749.246):** songs 52, 61's words and 50's words on every mark, each off in turn; then a new held-out lyric (49 or 58), read once.

## 749.247. A line sung again makes its own run of one pitch, and the join refuses it
- **Problem:** after the title's room was retired, song 61's words drew 0.097 of their "again" lines fresh (limit 0.076). Every refusal at the join (929), on all four seen lyrics, is a run of one pitch over the cap of 3. The source's longest run is 2 or 3, and the copy's is 4 to 6. Splitting a note for extra syllables repeats its neighbour's pitch, and notes moved onto the new section's chord land on one another (count at 0b92d08b, `why_join_refuses_*.json`).
- **Fix:** when a line is sung again, each note that would be the fourth or later of one pitch in a row moves a scale step toward the next different note, inside the line's register. The join then tests as now. Switch `LUTHIER_AGAIN_RUNS=1`.
- **Check:** the four seen lyrics on every mark, share at most 0.076. Watched: the chord-tone share of mended notes on a beat, against the source's own. Then song 58's words, held out and read once.
- **Read (0b92d08b before 7f8f67d7, `held_out_3_6_8.json`):** all four seen lyrics meet every mark (share 0, 0.0153, 0, 0.0009). **The third held-out lyric, song 58's words, read once, meets every mark:** 4.061 and 4.035 notes a bar, first beat 0.218 and 0.243, 840 0.4 in ten, 1 of 6,900 drawn fresh. 6/8 folk passes on unseen words. The test that counts is song 69, written for 6/8.
- **Watched:** 840 is back toward its limit on two seen lyrics (0.84 and 0.63 in ten) since the title's room was retired. Counts asked before song 69: mended notes' chord fit, mended lines, and 840 by title line.

## 749.247 revised (28 Nov): the mend kept the run but lost the chord
- **Evidence (30a27177, `count_run_mend_*.json`):** moved notes on a beat were chord tones before the move in 0.93 to 1.0 of cases, and after it in 0 to 0.07, against the source lines' 0.88 to 0.94.
- **Fix:** move the run's off-beat note where it has one. On a beat, move to the nearer chord tone, not a step.

## 749.248. 749.244 filters only the kept windows; the weighted rule's title lines fail 840
- **Problem:** every 840 death on the five 6/8 lyrics is a title line set by the weighted rule (760) and sung in one bar by 876's path (54 of 54 on song 50's words, 22 of 22 on song 58's). Kept windows pass every time. Retiring the title's room put more title lines on that path.
- **Fix:** a title line takes no rhythm that fails 840's test, on any path, while a kept window that passes can be had.
- **Check:** the five lyrics on every mark, with 840 under one in ten. Watched: the distinct rhythms each title line is drawn with.
- **Read (dc595e56 before b5737493, `forms_247_248.json`):** all five 6/8 lyrics meet every mark with both forms. 840 is 0, 0.02, 0, 0, 0 in ten. Moved notes on a beat: 1 in all, a chord tone. This is song 69's package.
- **Watched:** across builds, one rhythm takes 0.86 to 0.93 of a short title line on three lyrics. To be counted against Essen's own share before it's called a fault.

## 749.249. A title line's doubled stress pull narrows its rhythm to one window
- **Problem:** across 600 builds one rhythm takes 0.55 to 0.93 of a two-bar title line in 6/8 folk, against the table's commonest share of 0.13 to 0.59 among the windows that pass 840. For example, song 50's words 0.863 against 0.252, and song 58's words 0.925 against 0.585. The doubled stress pull (2.8, 840's first form) does it: with no pull the share falls to 0.335 and 0.607 (3b6c6997, `count_title_weights_*.json`). 749.244 and 749.248 now do the doubled pull's job directly.
- **Fix, two arms:** A, no stress pull on a title line; B, the pull any line takes (1.4).
- **Check:** the five lyrics on every mark, with the title lines' stresses on a beat at least the median of the lyric's other fresh lines. Watched: the commonest share against the table's, and whether our commonest is the table's.
- **Read (c4013713 before aab4fef5, `forms_249.json`):** neither arm passes. A (no pull) sets title lines worse than their neighbours on three lyrics (for example 0.5 against 0.8) and misses onsets on the beat on song 58's words. B (1.4) misses the stress mark on song 52's first chorus title (0.6 against 0.75), as the doubled pull does. **The doubled pull stays. The narrow choice is a known cost.** As built, our commonest is the table's commonest on one title line of six.
- **Mark 2 rewritten for later runs:** each line's stress-on-beat share is read against what its stresses and beats allow, min(1, beats ÷ stresses), and on the present package first.

## 749.250. The pickup room for a title line stops at the section's edge
- **Problem:** 749.232's third reading gives the line ahead of a title line pickup room, but only within a section. A title line that opens a section on light syllables gets none. On song 49's words, 530 builds of 600 hold the chorus's first line to its bar line, leaving 9 of its 55 passing windows. The formula's share among those 9 (0.901) matches the builds' (0.907), so the limits narrow it, not the stress pull (aab4fef5, `count_title_limits_49_c0.json`).
- **Fix:** where a title line opens a section on light syllables, the last line of the section before gives the same room.
- **Check:** the five lyrics on every mark, with mark 2 rewritten, and the section's last line inside its slot. Watched: the title's choice against the table, and whether ours is the table's commonest.
- **Read (4934a733 before 64d2e6ff, `forms_250.json`):** song 49's words meet every mark. Its first chorus line is held to its bar line in no build (was 530 of 600), and its commonest rhythm's share fell from 0.907 to 0.683. The other four lyrics come out the same as before. **In song 69's package.**
- **Standing gaps (from 749.249):** song 52's chorus title line sits at 0.75 of its stress ceiling against its neighbours' 0.833. Our commonest title rhythm is not the table's commonest (on song 49's words it ranks eighth, with 0.021 of the count).

## Pop 3/4 with the overnight's forms (992fa4d85)
- Every mark met but K3: first beat 0.337 and 0.326 against 0.45; off the beat 0.326 and 0.348 against 0.26. 840 none; share drawn fresh 0.0004; the chord mark met.

## 749.251. Outside 4/4, a line sung again to new words is refitted blind to stress
- **Problem:** in pop 3/4 the kept windows' ceiling for first-beat stress is 0.674 and kept count alone gives 0.421, but the builds give 0.317. Fresh, title and copied lines meet K3 (0.467 to 0.512). Lines sung again to new words don't (0.272, and 818's 0.227), and they carry seven tenths of the song's stresses. The refit splits the widest gap and drops the narrowest. In 4/4 it chooses by the words' weights (882); outside 4/4 it never has (9cc6427b4, `count_k3_by_made_pop55.json`).
- **Fix:** the refit chooses which gaps are split and which notes dropped to set the new words' stresses best, by the table's own stress score.
- **Check:** pop 3/4 K1 to K8, with K6 held. The five 6/8 lyrics come out byte for byte the same, since there's no stress table there.
- **Read (3f73df9f8 before 48bd4b434, `RESULT_251.json`): not passed.** On the living median, first beat rose from 0.326 to 0.412 and off the beat fell from 0.348 to 0.203. The pick is worse than the median: 0.337, 0.321, commonest 0.317, rhythm again 0.3. "Again" lines closed about half their gap (0.272 to 0.362). Living builds meeting every figure mark rose from 0.3 to 11.4 in 100. The 6/8 lyrics come out byte for byte the same. It stays unset. Next: counts on lines matching one for one, and on the pick.

## 749.252. A line that will be sung again is drawn for its first words only
- **Problem:** after 749.251, lines sung again still sit under fresh lines on the first beat. Same count 0.312, notes split 0.359, notes dropped 0.428, against fresh lines' 0.465. Mending the same-count lines alone would reach 0.438, short of 0.45. Every line sung again as good as fresh would reach 0.481. The pick is the first build past the gates, so its miss is chance: only 24.1 in 100 living builds meet K3's first beat (aa6d3d6, `RESULT_counts_251.json`).
- **Fix:** a line that will be sung again is drawn by the table's stress score summed over every set of words it will carry, the first words weighted as now. 749.251 stays on beneath it.
- **Check:** pop 3/4 K1 to K8, with K6 held and the source lines' first singing at least 0.40 on the first beat. The five 6/8 lyrics come out byte for byte the same.
- **Read (e7089f3 before d93811cf, `RESULT_252.json`): not passed.** On the median, first beat moved 0.412 → 0.422, and same-count lines didn't move (0.313). The source lines' first singing held (0.431). The 6/8 lyrics come out byte for byte the same. Unset. Next: whether the table's stress score, at its best, prefers beat one over beats two and three.

## 749.253. Outside 4/4, 834's early entry fires at 4/4's share and is scored as if it hadn't moved
- **Problem:** in pop 3/4, drawn lines would reach 0.591 on the first beat with no limit, and 0.472 is built. 834 alone takes 0.072 of that: a line opening on a stress sings its rhythm an eighth or a quarter early, at 0.2, 4/4's figure, since the pop table has no entry shares. The early rhythm is scored as if it hadn't moved. Title lines go from 0.656 to 0.531 under 834 alone (7c744143, `RESULT_counts_AB.json`).
- **Fix:** outside 4/4, the early entry is taken only at the metre table's own share, and where the table has none, not at all.

## 749.254. 749.252's summed score is led by unstressed syllables
- **Problem:** a single rhythm can serve all the sets of words a source line carries (0.538 on the first beat). The rhythm with the best summed score reaches 0.459, because the whole score summed over two dozen sets is led by where the unstressed syllables fall.
- **Fix:** on every set past the first words, the sum counts stressed syllables only.
- **Check (both):** two arms on pop 3/4 (749.253 alone; 749.253 with 749.252 and 749.254). Marks: K1 to K8, K6 held, and lines beginning late at most 1.5 × the table's 0.10. Arm 2 also needs the source lines' first singing at least 0.40. 6/8 is read on every mark if 749.253 acts there; song 69's package doesn't change tonight.
- **Read (98358a29 before f601fad6, `RESULT_253_254.json`):** arm 1 (749.253 alone) misses K3 by a hair (0.449 and 0.444). **Arm 2 (749.253 with 749.252 and 749.254) meets every pop 3/4 mark on the pick and the median:** first beat 0.455 and 0.46, off the beat 0.118 and 0.134, K6 held, source lines 0.527, lines late 0.027. The pool meeting every figure mark rose from 10.8 to 36.5 in 100. Taken as the pop 3/4 package. Narrow, on one seen lyric and one seed, so two more seeds come before song 68. With 749.253, the five 6/8 lyrics change and still meet every mark. Song 69's package is unchanged.
- **Seeds 2 and 3 (2b8a8a71 before 309175a0, `RESULT_seeds_3_4.json`):** K3's median holds at 0.46 at every seed. Seed 2's pick misses K3 (0.439). Seed 3 misses K5 on pick and median (0.335 and 0.331), in a narrow register (E, [44, 56]; pick range 12, 8 pitches). The pool meeting every mark is 36.5, 40.1 and 23.9 in 100. **Not ready for song 68.** Next: what the seed fixes for the whole run, and the pre-tonight package at seeds 2 and 3. And, as a reference for the bar, the 4/4 engine's own pool share meeting its marks.

## 749.255. Outside 4/4, 956's ceiling on the commonest pitch never acts
- **Problem:** pop 3/4 misses K5 (commonest pitch) on the median at seed 3 (0.331 against 0.303), and did before tonight's forms too. In 4/4 the pool meets the commonest-pitch limit by a gate, 956's ceiling by part, which `song_from_lyric.py` sets only inside `if L["metre"] == "4/4"`. In 3/4 the gate isn't there (8f5f5377, `RESULT_counts_K5_pool.json`; code read).
- **Fix:** outside 4/4, 956 acts at the metre table's own 90th by part.
- **Check:** every mark on the median at three seeds; the pool on the six like marks at least 4/4's median (76.2 in 100); the pool still at least 10. Ruled in the same post: the bar's pool half is read on the six like marks, against 4/4's own.
