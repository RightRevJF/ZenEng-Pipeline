# Three counts before song 69 (28 Nov 2026): the run mend and the chord; how many lines it touches; where 840's deaths come from. Counts; nothing predicted, nothing run under a changed form.

01:00 ET. Asked by the songwriting session (00:31 and 00:49 ET). count_run_mend.py (300 builds; each line sung again twice from one random state, with the mend and without), count_b.py (400 builds) and count_840_path.py (600 builds), on the last trial's records. Figures printed from count_run_mend_*.json, count_840_*.json and count_840_path_*.json by the command that wrote this file.

## 1 and 2. The run mend (749.247): how many lines, and what it does to the chord
| | Lines sung again (300 builds) | Share with a note moved | Share of their notes moved | Moved notes on a beat | A chord tone before the move | after | Source lines' notes on a beat that are chord tones | The copies' share without the mend | with it |
|---|---|---|---|---|---|---|---|---|---|
| Song 52 | 4500 | 0.064 | 0.006 | 186 | 1.0 | 0.0 | 0.898 | 0.966 | 0.958 |
| Song 61's words | 4500 | 0.098 | 0.013 | 213 | 0.934 | 0.066 | 0.898 | 0.968 | 0.957 |
| Song 50's words | 2400 | 0.059 | 0.008 | 122 | 0.959 | 0.041 | 0.938 | 0.979 | 0.966 |
| Song 49's words | 3300 | 0.051 | 0.007 | 114 | 0.991 | 0.009 | 0.877 | 0.966 | 0.957 |
| Song 58's words | 6900 | 0.052 | 0.007 | 198 | 1.0 | 0.0 | 0.916 | 0.976 | 0.968 |

- The mend touches 5 to 10 lines in 100 sung again, and about one note in a hundred.
- **The songwriting session's worry is borne out.** A moved note that falls on a beat was a chord tone before the move in 93 to 100 cases in 100, and is one afterwards in 0 to 7. The mend runs after the clash rule and moves a chord tone a step off the chord on a strong beat, with nothing to check it.
- Over all the copies' notes on a beat the fall is about a point (0.97 to 0.96), still over the source lines' own share, because so few notes are moved. But the moved notes themselves are far under the source's.

## 3. 840: which title lines, and how they were drawn
Builds dying on 840, of 400:

| | Builds made | Died on 840 |
|---|---|---|
| Song 52 | 400 | 0 |
| Song 61's words | 400 | 3 |
| Song 50's words | 400 | 33 |
| Song 49's words | 400 | 27 |
| Song 58's words | 400 | 17 |

How the title line drawn fresh was made, in builds that die on 840 and in those that do not (600 builds):
- Song 50's words, Chorus 1:6: {"did not | a kept window | earliest start on or before the bar line | the line itself passes 840's test | over its bars": 537, "died on 840 | the weighted rule (760) | earliest start on or before the bar line | the line itself fails it | all in one bar": 54, "did not | the weighted rule (760) | earliest start on or before the bar line | the line itself fails it | all in one bar": 9}
- Song 49's words, Chorus 1:0: {"did not | a kept window | earliest start on or before the bar line | the line itself passes 840's test | over its bars": 542, "died on 840 | the weighted rule (760) | earliest start on or before the bar line | the line itself fails it | all in one bar": 36, "did not | the weighted rule (760) | earliest start on or before the bar line | the line itself fails it | all in one bar": 20, "did not | the weighted rule (760) | earliest start on or before the bar line | the line itself passes 840's test | all in one bar": 2}
- Song 49's words, Chorus 1:6: {"did not | a kept window | earliest start on or before the bar line | the line itself passes 840's test | over its bars": 519, "did not | a kept window | earliest start on or before the bar line | the line itself passes 840's test | all in one bar": 45, "died on 840 | a kept window | earliest start on or before the bar line | the line itself passes 840's test | over its bars": 33, "died on 840 | a kept window | earliest start on or before the bar line | the line itself passes 840's test | all in one bar": 3}
- Song 58's words, Chorus 1:0: {"did not | a kept window | earliest start on or before the bar line | the line itself passes 840's test | over its bars": 549, "did not | the weighted rule (760) | earliest start on or before the bar line | the line itself passes 840's test | all in one bar": 22, "died on 840 | the weighted rule (760) | earliest start on or before the bar line | the line itself fails it | all in one bar": 22, "did not | the weighted rule (760) | earliest start on or before the bar line | the line itself fails it | all in one bar": 6, "did not | a kept window | earliest start on or before the bar line | the line itself passes 840's test | all in one bar": 1}

- **Every title line that fails 840's test was made by the weighted rule (760) and sung all in one bar.** A title line drawn from a kept window passes the test in every build, as 749.244 intends.
- The path: 876 lets a two-bar line be sung in one bar with the next bar silent. For a title line of five to seven syllables no kept one-bar rhythm is to hand, so the weighted rule sets it, and the weighted rule knows nothing of 840's test. 749.244 filters kept windows only.
- On song 49's words the second title line of the chorus passes on its own in builds that die: the death there is the first title line's doing (840 reads the title lines together).
- Since the title's room was retired, title lines sit in two bars, where 876 applies; in three or four bars it did not. That is why 840 came back.

## Forms that follow (each its own rule, before any code)
- **The run mend and the chord:** where a run is over the cap, the note moved is one that does not fall on a beat, where the run has one; a note on a beat moves to the nearer chord tone and not a step.
- **749.244 on every path:** a title line does not take a rhythm that fails 840's test (from 876's one bar or the weighted rule) while a kept window that passes can be had.
