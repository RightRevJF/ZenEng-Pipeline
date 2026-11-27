# The 3/4 plan form on song 53's words (749.226): the songwriting session's marks, set down before any run

27 November 2026, 11:35 ET. Form and marks from `coord/songwriting.md` (10:58 ET), in its words where quoted. This is the one form: if it misses, the 3/4 draw closes for the version. Song 68 is not run here.

## The form (`LUTHIER_PLAN_3_4=1`, unset by default; 3/4 only)
"In 3/4 a line's sung bars are whichever of 2, 3 or 4 puts its syllables a bar nearest the table's median. A line of three sung bars is padded to a four-bar phrase: its last note is held through the fourth bar, or a rest fills it, the draw choosing by the table's held-bar share. ... the draw reads a four-bar line as two windows."

Four things the words leave open, settled now:
1. **A tie goes to the fewer bars.** Under the lead-sheet table (median 2.333 notes a bar) an eight-syllable line is exactly as far from the median in three bars (2.67) as in four (2.00); it takes three.
2. **The split.** A line of four sung bars is two two-bar windows, its syllables halved (the odd one to the first). A line of three sung bars is a two-bar window holding two thirds of its syllables (rounded) and a one-bar rhythm holding the rest, then the padded bar.
3. **The held-bar share** is the table's share of bars that are one note on the first beat (lead sheets 0.216; Essen 0.079). With that chance a three-bar line's last note is held to the end of its fourth bar less a beat; otherwise the note keeps the length the engine gives it and the bar rests.
4. **Lines that return** (sung again, copied) take their source's rhythm as they do now.

By this rule every line of song 53 (8 and 6 syllables) takes three sung bars in a four-bar phrase under the lead-sheet table, and two bars under Essen's (median 3.44), where the form changes nothing.

## Marks (song 53's words, mezzo, seed 1, 1,000 builds; both arms with the plan form)
- **P1.** Every line's bars as the rule gives them, printed per line before the draw.
- **P2.** Living builds 30 or more and pool 10 or more (T1).
- **P3.** The chosen tune's notes a bar inside 2.06 to 2.70 (T2), "counted over every bar sung, padded bars included".
- **P4.** Onsets on a beat inside 0.731 to 0.939 (T3).
- **P5.** Stressed syllables on the bar's first beat 0.583 or more (T4).
- **P6.** Against the plan-form Essen arm: the commonest pitch (verses, refrains) no higher by more than 0.02; no leap past an octave where it has none; the range reported (T6). The words' fit cannot be read in 3/4 and is not a mark.
- **P7, reported only:** bars on a rhythm already sung and distinct rhythms over bars, against v53's Essen arm (0.766, 0.234).
- **Byte for byte**, switch unset: 54, 55, 52.

## What I expect
P1, P2, P3 met: 2.3 or so notes a bar follows from the rule. P4 likely: sparser bars put more notes on beats. P5 is the one in doubt: 0.583 needs most stressed syllables on the first beat, and the engine's pull is to any beat, not the first. P6 in doubt after the first trial's 0.438. I put the whole at one chance in three.
