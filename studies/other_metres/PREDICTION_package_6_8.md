# The 6/8 repair for v54: the rule file, before any code or run

27 November 2026, 14:54 ET. Asked for by the songwriting session (14:55 ET). The form is mine to set down from what the two 6/8 readings showed; **the marks below are proposed and are the songwriting session's to accept or change before anything runs.** Nothing here has been run, and I have not looked at what the title's-room rule would give song 52's title line.

## What the readings showed (`RESULT_6_8.md`, `RESULT_plan_6_8.md`)
Two bars a line leaves song 52 22 living builds in 1,000. Bars from Essen's density, padded, gives 248 and a pool of 37, and misses Essen's notes a bar on the sparse side (3.20 against 3.60 to 4.33) because of the padded bar; 780 takes 455 builds at one copied line; 840 takes 228 at a title line left with two bars.

## The form, three parts, each behind its switch, all unset by default
1. **Bars from the table's density, unpadded for folk** (`LUTHIER_PLAN_6_8=folk`). A line's sung bars are whichever of 2, 3 or 4 puts its syllables a bar nearest Essen 6/8's median of 4.0 (a tie to the fewer). Essen is folk, so a three-bar line takes three bars and no pad. *Settled:* a section whose bars come to an odd count rests a bar at its end, as every section already does; phrases are then not square, which is how the folk tunes run. (`LUTHIER_PLAN_6_8=1` remains the padded form as tried.)
2. **The title's room** (`LUTHIER_TITLE_ROOM=1`, as written for 3/4): a line that sings the title takes more bars, to four, until half its stressed syllables can land on a beat in half the kept windows by count.
3. **The copy's join** (`LUTHIER_COPY_JOIN=1`, as written for 3/4): a copy that would begin before the line ahead of it has ended is sung again and the build lives.

No range part: against Essen the 6/8 tune's range and pitches were inside the kept 10th. They are reported.

## The trial
Song 52's lyric as the engine has it (a seen song), Essen 6/8 table, seed 1, 1,000 builds, the three switches on.

## Marks proposed
Every figure the form claims to move is read on **the living builds' median** (the chosen record's fitted spec, 600 builds) **and** on the chosen tune; a mark is met only if both meet it.
- **S1.** Every line's sung bars and slot, printed before the draw; the title lines' bars before and after the title's-room rule.
- **S2.** Living builds 30 or more; pool 10 or more.
- **S3.** Notes a bar, over the bars of sung phrases, inside Essen 6/8's middle half, 3.60 to 4.33.
- **S4.** Onsets on the beat at or over 0.389; onsets on the bar's first beat at or over 0.211 (Essen's 25th by song).
- **S5.** 731: the median build's stressed syllables on a beat at or over 0.40 (every build made).
- **S6.** Deaths on 780 and on 840 each under one in ten of builds made.
- **S7.** Every note inside the voice; no leap past an octave inside a line.
- **Reported only:** every other gate's deaths; range and distinct pitches against Essen's and the lead sheets' 10th and 25th; each switch off one at a time, 200 builds; the song's length against the kept 75th; the joint-gate distance.
- **Byte for byte**, every switch unset: 54, 55, 52, and song 53's Essen arm.

## Stopping rule proposed
One reading, and at most one revised form for a reason the reading names; then 6/8 closes for v54.

## What I expect
S2, S5 met (the padded form met them). S3 met without the pad: three bars at four notes is four notes a bar. S4 likely. **S6 is the doubt**, on 840: I do not know that any bar count gives a line with five stressed syllables in seven half its stresses on a beat in half the windows; if none does, the rule leaves it at two bars and 840 keeps taking builds. Three-bar slots are also new ground for the draw (so far only four-bar phrases were split), and something may break there. Two chances in five.

## Accepted, with one addition (15:07 ET, before any code or run)
The songwriting session accepted S1 to S7 and the stopping rule as written (15:02 ET) and added one figure, **reported only:** stressed syllables on the bar's first beat, on the living builds' median and on the chosen tune.

It asked for Essen 6/8's by-song figures. **Essen's tunes carry no words, so no such figure can be made from them.** What exists, written here before the run:
- the 6/8 lead sheets with words (85 songs with 20 stressed syllables or more, `trial_tables/6-8_leadsheet_stress_by_song.json`): stressed syllables on the bar's first beat, by song, 10th 0.324, 25th 0.390, 50th 0.509; on either beat, 10th 0.534, 25th 0.657, 50th 0.784;
- the hymns in 6/8 (6 hymns, pooled, 583 stressed syllables): 0.515 on the first beat, 0.84 on either beat.
These are popular song and hymnody, not folk; they stand beside the figure and decide nothing.

If 840 keeps taking builds, the result gives the title line's window shares for each bar count, as asked.
