# Review of stage 7 (Luthier v20, fixes 858 to 866), 18 November 2026

Branch `luthier-v8-stage1` at 0f5d1b6, a fast-forward from main (6b and 6c were merged at caa6832). Merged.
749.57 to 749.59 (REVIEW_stage6b_6c.md) are not touched by stage 7 and stay open.

| Check | Result | Held? |
|---|---|---|
| Every .py in lib/luthier compiles | yes | yes |
| `luthier_judge7.py` | 4/4 pop: 159 kept songs, gate 3.46, usual 2.56, middle half 2.10 to 3.01; 6/8: 907, 3.57; 3/4: 1585, 3.53, as stage7_results.json | yes |
| `song_from_lyric.py` songs 54, 55, 52 | .song.txt and .song.json identical, all three | yes |
| song 52 from its hand spec (3000) | identical: pick 36cf66ee1827, charge 3.315 | yes |
| 860: kept songs inside the gate | 0.912 read with themselves in; the loo quantile is the gate | yes |
| 861: the pick inside the kept middle half where a build stands there | song 54 2.301, song 55 2.141 (both inside 2.10 to 3.01); song 52 none stands there (see 749.61) | yes |
| 862: a withheld reading printed | the old charge beside each shortlisted build | yes |

## 749.60 The pick is ranked by two readings the bench rejected

**Problem.** 863 ranks the builds in the kept middle half by "low surprise" and "sure endings", at equal weight, and takes the first. 865 tried both readings
against the chart record first, and neither held.
**Evidence.** stage7_results.json, new_readings, 131 songs: the ending gap against peak Spearman -0.142 (p 0.105), against the sign predicted (N1, more than 0);
mean surprise against peak -0.026 (p 0.77). Only chord rarity held, weakly (0.11; 0.07 held out). 863's test asks for a direction and a source written in
advance, and both have them; but the bench is the standing test (858), and on it these two point nowhere, one of them slightly the wrong way.
**Fix.** Until a reading passes the bench, choose inside the band by the seed alone (or by the one reading that held), and print the two directed readings
beside the pick as 862 prints the old charge.
**Check.** No reading chooses the pick unless the bench holds it at the gate's level.

## 749.61 Where kept songs stand is not where one song's builds should stand

**Problem.** The kept middle half of distance (2.10 to 3.01 in 4/4) holds the spread between kept songs: different lyrics, tempos, keys and writers. One song's
builds share all of those, so they sit nearer the centre than kept songs do, and the band takes the most outlying of them. In 6/8 the builds sit far outside.
**Evidence.** Song 54: 760 of 763 builds pass the gate, quartiles 1.51, 1.83, 2.15; the band keeps 202, about the furthest quarter. Song 55: 762 of 763 pass,
quartiles 1.55, 1.78, 2.06; the band keeps 158. The old picks stood at 0.88 and 1.39 and passed the gate. The shortlisted builds' old charges run 0.33 to 1.52,
where the least among the builds is 0.0. Song 52 (6/8 from its lyric): 2 of 186 pass, quartiles 4.26, 4.55, 4.86; no build stands in the band, so the gate is
nearly the whole choice there. In 4/4 the gate refuses almost nothing; in 6/8 almost everything.
**Fix.** Read a build against the spread one song's builds can have (kept songs of the same tempo and density, or the kept within-song spread across a song's
own sections), or keep the gate and drop the band. Look at the 6/8 table separately: its builds are all past the kept songs.
**Check.** In 4/4 the gate refuses some builds and the pool is not the far tail; in 6/8 at least the median build passes the gate.

## 749.62 859 says the old judge stays as a gate; in the code it chooses nothing

**Problem.** The README says the old judge "stays as a gate". Under `judge: 7` the pool is every survivor, and the old charge is only printed.
**Evidence.** The bench ranks the old charge first at damage (a tenth of the notes changed: 90 in 100 against the new gate's 75; bars shuffled: 100 against 53).
Song 55's pick carries an old charge of 1.35, the highest of its shortlist; song 54's 0.707.
**Fix.** If the old charge is meant to gate, apply it before the band (for example, builds inside its kept widths, or the least half), and say so in the record.
**Check.** The record says which gates the pick passed, the old charge among them.

## Song 58

Written next with song_from_lyric.py, once the writer gives its settings.
