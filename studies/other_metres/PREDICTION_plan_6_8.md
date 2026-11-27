# The plan form in 6/8 on song 52's words: the songwriting session's marks, set down before any run

27 November 2026, 13:05 ET. Form and marks from `coord/songwriting.md` (12:35 ET). One form: if it misses, 6/8 closes for the version beside 3/4. (A clock note: my posts headed 12:25 and 12:45 ET today were committed at 12:17 and 12:19; I had not looked at the clock. This one is by `date`.)

## The form (`LUTHIER_PLAN_6_8=1`, unset by default)
749.226's rule in 6/8, read from Essen's 6/8 table: a line's sung bars are whichever of 2, 3 or 4 puts its syllables a bar nearest the table's median (4.0; a tie to the fewer); three sung bars are padded to a four-bar phrase, the last note held through the fourth bar at the table's held-bar share (bars of one note on the first beat) or the bar resting; a four-bar phrase is drawn as two windows, split as in `PREDICTION_plan_3_4.md`. No other change.

By this rule song 52's lines of 10 to 13 syllables take three sung bars in four, its one line of 14 takes four, and its lines of 6 and 7 keep two. **The title line (7 syllables, 5 stressed) keeps its two bars**, so the form does not change what 840 asks of it.

## Marks (song 52's lyric as the engine has it, seed 1, 1,000 builds, Essen 6/8 table)
- **Q1.** Every line's sung bars as the rule gives them, printed per line before the draw.
- **Q2.** Living builds 30 or more, pool 10 or more.
- **Q3.** The chosen tune's notes a bar, over the bars of its sung phrases, inside Essen 6/8's middle half: 3.60 to 4.33.
- **Q4.** The chosen tune's onsets on the beat at or over 0.389, and on the bar's first beat at or over 0.211 (Essen 6/8's 25th by song, 907 tunes, from `kept_readings.json`, written here before the run).
- **Q5.** 731: the median build's stressed syllables on a beat at or over 0.40 (read over every build made, as `read_6_8.py` read it: 0.358 without the form).
- **Q6, reported only:** deaths by gate; the chosen tune's range and distinct pitches against Essen 6/8's 10th by song (9 and 6: by the table below) and the 99 lead sheets.
- **Byte for byte**, both switches unset: 54, 55, 52, and song 53's Essen arm of the first 3/4 trial.

Essen 6/8 by song, 10th / 25th / 50th / 75th / 90th, for Q6: range and distinct pitches are printed by the script's first lines and copied into the result; I have not yet seen them beside any tune.

## What I expect
Q1 and Q3 met. Q4 likely on the beat, less sure on the first beat. Q5 likely (four notes a bar leave beats for the stresses). **Q2 is the doubt:** 840 took 682 builds because the chorus title line is under half in 80 builds of 100, and the form leaves that line alone; only the bridge's title line gets room. If 840 still takes most builds the pool may still be nil. One chance in three for the whole.
