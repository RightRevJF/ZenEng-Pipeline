# Song 48 under Luthier v4: findings 690 to 698

One rerun, main and control, 1,000 builds each, seed 20261113+448, the designs as before, the judge not refitted. Orders e897f1e17e02 / 8924d5f25684; survivors 723 / 702. Under 685, each fix is tested on its own kept-only reading. The judge of record is printed beside density peers and does not decide any test; it still makes the pick.

## 690 The session's reading of "bars sung in a kept song" counts only the table's rhythms
**Problem.** The session can read a bar as sung in a kept song only where its rhythm is in 652's table, which holds rhythms sung in two kept songs or more. The paper's reading counts every kept song. The two readings are not the same number.
**Evidence.** Run B: the session reads 45% / 43% where the paper reads 60% / 57%. Luthier v2: 35% against the paper's 51%. The 4-note bars show the gap most: the session reads 13% to 20%, the paper 93% to 94%. The commonest 4-note bar, (30, 36, 42, 45), is the hook's bar in its copies, and it is not in the table. Under v4 the session reads 63% / 63% overall. By notes in the bar: 1 note 99.6%; 2 notes 96%; 3 notes 81%; 4 notes 20%; 5 notes 82%; 6 notes 62%; 7 notes 56%; 8 notes 35%. Reading only the drawn bars (designed bars aside) gives 63%; reading by line rather than by bar gives 67%.
**Fix (proposed).** Either the paper reads the v4 runs with its full set, or it supplies every kept bar rhythm with the songs that sing it, so the session can read the same number. 680's draw stays on the table: rhythms sung in two songs or more.
**Check.** The session's reading of run B matches the paper's 60% / 57%.

## 691 Every bar whole: the drawn bars come up most of the way
**Problem.** None; 680's test is read under 690's caveat.
**Evidence.** 680 drew 4,991 / 5,069 lines in whole kept bars, and a further 610 / 520 around the template's bars. 494 / 488 fell back to the old draw, as did 3,244 / 3,378 lines on template bars whose counts did not fit. Bars sung in a kept song (the table reading): 63% / 63%, against 45% / 43% under run B. By count, 5, 6 and 7 notes are now at or near the kept shares (82%, 62%, 56% against 78%, 69%, 52%). The 4-note shortfall is 690's.
**Fix.** None.
**Check.** As 680's, read again under 690.

## 692 A product of the palette's shares over a bar's gaps favours the commonest class
**Problem.** 680 weights a kept bar by the product of the palette's shares for its gaps. A bar of seven eighths multiplies seven shares near 0.6, and a bar with sixteenths multiplies shares near 0.1. So the product compounds whatever class the palette favours, and in nearly every palette that is eighths.
**Evidence.** Eighths: Verse 1 66% / 65% against 51% for its cells; Chorus 1 71% / 71% against 60%. The chorus's drawn lines, 655's check against the build's own capped palette: eighths 73% against 59% (over ten points), sixteenths 10% against 11%. Bits saved first half to second: 0.12 / 0.12 a gap (run B 0.17 / 0.18; kept 0.29). The dense lines' longest run of equal gaps: median 5 / 6, 75th 8 (kept median 4). The spectral limit now leads the limit deaths (67 / 54). On the judge, the verse's costliest measure is the eighths (1.12).
**Fix (proposed).** Weight each gap by the palette's share over the kept mean palette's share for its class (a likelihood ratio), not by the bare share. A bar is then favoured for what marks the song, not for being the corpus's commonest bar twice over.
**Check.** 578's test against the build's own palette within ten points; bits saved 0.29 within 0.1; the dense lines' longest run at the kept median.

## 693 The template returns
**Problem.** None; 682 passes.
**Evidence.** Same rhythm four bars apart within a section: 17.4% / 16.8% (kept 20%; run B 7.6% / 8.9%). Gain under the kept couplings: 0.169 / 0.168 (the test asks 0.12; run B 0.056 / 0.073). Survivors at or over 0.14: 61% / 59% (run B 16% / 22%). 682 took 3,184 / 3,032 lines exactly. 3,085 / 3,204 were not taken (counts more than one apart, or no room), and 633's split still ran on 3,553 / 3,501.
**Fix.** None.
**Check.** As 682's.

## 694 Placement deaths stay in the verse sung again
**Problem.** 681 shortened the breath before a line sung again in 1,532 / 1,500 lines, but the deaths remain.
**Evidence.** Deaths for want of a placement: 39 / 52 in a thousand (run B 51 / 50; the test asks under 20). By line: Verse 2:0 21, Verse 2:1 12, Verse 2:2 5, Verse 2:3 1 (main). The verse sung again copies Verse 1's bars at 293's rate (1.0). Those bars are now whole kept bars, often with a pickup, and their syllable counts differ (Verse 1 sings 15, 14, 14, 14; Verse 2 sings 14, 14, 16, 15). The copy is drawn through the old placement with the bars as weights, and it cannot both keep them and fit a different count under 308's cap.
**Fix (proposed).** A line sung again whose count is its source's within one takes its source's onsets as 682 takes the template's: exactly, with the odd note a melisma begun on the longest note, or the longest note split. Otherwise it is drawn in whole kept bars by 680, the source's bars first.
**Check.** Deaths for want of a placement under 20 in a thousand.

## 695 With repeats held, 650 cannot reach its shares, and the power runs away
**Problem.** 683 holds each window's repeats at the kept share, and it lands there. But the walk can then make the sung note the easiest of its neighbours only so far. The calibration raised the power every round without moving the reading, and the mean ease sits at the top of the kept band.
**Evidence.** Repeats: the song 28.3% / 27.0% (kept 28.7%); the verse window 32.8% / 31.8% (its band's kept quartiles 19.5% to 43.6%); the chorus window 23.8% / 22.4% (12.1% to 36.7%). All three pass. The sung note is the easier of a pair in 86.2% / 86.3%: inside 89% within three points, at the edge. It is easier than every neighbour in 62.6% / 62.9%, which fails 73% within five. The power rose from 1.45 to 5.74 / 5.65 over six rounds while the first share stayed between 0.84 and 0.86. Mean ease is 4.34 / 4.36 bits a note: at or just over the 4.35 bound the session was given, and over the paper's 4.3. The hold acted on about 50,000 moves, lowering the repeat's weight, and about 40,000, raising it.
**Fix (proposed).** Stop the power where a round no longer raises the reading by half a point, so it does not climb on no evidence. Read the two shares as the ceiling of this walk with repeats held. Or calibrate the hold and the power together against the joint kept figures, so that "easier than every neighbour" is what the power is set by.
**Check.** 650's two shares within their bounds with repeats inside the kept quartiles; mean ease 3.3 to 4.3.

## 696 Survivors are within a tenth of run A
**Problem.** None; 686 passes.
**Evidence.** 723 / 702 against 752 / 750 (a tenth: 677 / 675). Deaths: limits 72 / 67 (spectral 67 / 54, run_max 2 / 0); bridge opening unrelated 67 / 74 (run A 32 / 49); the chorus above the verse 57 / 70; rhythm, no placement 39 / 52; key word on a chord tone 28 / 24 (run A 5 / 4).
**Fix.** None asked. The rise in key words off a chord tone and in the bridge opening unrelated follows the whole bars, which move where stressed syllables land. Read again after 692.
**Check.** As 686's.

## 697 653's spans and entries and 656's class after 680 (684, read only)
**Evidence.** Entries before / on / after the bar line: 6.5 to 7.5, 24 / 43 / 33 against a kept 49 / 22 / 30; 7.5 and over, 31 / 38 / 31 against 36 / 31 / 33; 3.5 to 4.5, 12 / 37 / 51 against 33 / 18 / 50. A whole bar begins on its bar line unless a pickup precedes it, so lines open on the downbeat about twice as often as kept lines. Spans, median against kept: 3.5 to 4.5 off the downbeat 0.41 (0.50), on it 0.53 (0.62); under 3.5, 0.29 (0.375 and 0.50); 6.5 to 7.5, 0.73 to 0.77 (0.77 to 0.81); 7.5 and over, 0.77 to 0.80 (0.85 to 0.88). 656's class 0 by the rate as sung, all lines: 24% / 25% against a kept 52% (lines now end inside their slot); 656 drew again only 394 / 350 times. A reading.

## 698 The judge of record, printed and not deciding (685)
**Evidence.** Both windows beside density peers: -1.76 / -1.70 (run B -1.20 / -1.18). Verse 1: -1.46 / -1.40. Chorus 1: -2.05 / -2.00. The costliest measure in both windows is gap_eighth (Verse 1.12 / 1.07; Chorus 1.45 / 1.45), which is 692's eighths as the judge charges them. Pick: ea7f5ae3eb75 (gain 0.208) / cd8adf428fc1 (0.181). A reading.
