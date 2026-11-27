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
- **Fix (to be specified rule first):** in 3/4, a pull to the bar's first beat for stressed syllables in the draw's scoring.
- **Check:** the living builds' median first-beat stress at or over the kept 25th (0.583), on song 53's words, with R1 to R8 held. Then song 68 as the real test.
