# Review of Luthier v21 (fixes 867 to 878), 18 November 2026

Branch `luthier-v8-stage1` at 1bb7d1f (v21 is 1ffe2e6, v22 59e473c, main merged in after each). Merged into main at 8dea87c. v21 and v22 were reviewed together, since every record
on the branch is v22's; this file covers v21's fixes and the closing of 749.57 to 749.64, and REVIEW_stage9.md covers v22.

## Reruns (PYTHONHASHSEED=0, on the branch head)

| Command | Result | Held? |
|---|---|---|
| `song_from_lyric.py songs/p68/lyric58.json 1000 12` (127 s) | .song.json and .song.txt identical | yes |
| `song_from_lyric.py songs/p65/lyric55.json 1000 12` (139 s) | identical | yes |
| `song_from_lyric.py songs/p64/lyric54.json 1000 12` (190 s) | identical | yes |
| `song_from_lyric.py songs/p62/lyric52.json 1000 12` | identical | yes |
| `mkspec52.py` + `metre_engine.py spec52.json 3000` | identical | yes |
| `mkspec53.py` + `metre_engine.py spec53.json 3000` + `hymn_parts.py` | spec53.json, .run.json, .parts.json identical; tune pick unchanged | yes |
| `chord_writer.py`, `write_song.py spec52.json 1000 12`, `stage4_extras.py` | stage4_results.json and spec52 written chords identical | yes |
| `stage8_results.json` | no committed script writes it (749.70) | no |

"About four minutes a song" is two to three on this machine, with two runs side by side.

## 749.57 to 749.64, finding by finding (the v22 records of songs 52, 53, 54, 55, 58)

Counts from the records (rests between lines of a section, melismas, line-final words), with each record's own checks and judge 7 block:
`python3 lib/luthier/review8_findings.py songs/p6[2458]/lyric5*.song.json`.

| Finding | Fix | Its check | Reading | Closed? |
|---|---|---|---|---|
| 749.57 descant ceiling read in the written key | 878 | summit at A5 or under as sung | song 53: summit 78 written, 81 (A5) as sung, `sung_shifts` [1, 3], `descant_shift` 3; every voice in range as sung | yes. The summit now falls at note 23 of 34, not in the last quarter (the paper's own "not met") |
| 749.58 rests at the kept 10th percentile | 870 | median rest between lines within the kept quartiles; rest share inside the kept middle half | median rest between lines of a section: 52 12, 54 12, 55 12, 58 15 twelfths (kept 25th 15, median 24); exactly a quarter 27/28, 25/49, 30/49, 24/50 (was 28/28, 34/49, 30/49). Rest share 0.135, 0.169, 0.218, 0.19 (kept middle half 0.21 to 0.39) | **no**: met on song 55's rest share and song 58's median only. Carried as 749.58 |
| 749.59 melismas on function words | 875 | within ten points of the kept | 0 of 22 (52), 0 of 40 (54), 0 of 14 (55), 0 of 65 (58) | yes |
| 749.60 pick ranked by readings the bench rejected | 872 | no reading chooses | the pick is the first build past the gates in the order built; directed readings printed only. Traced on song 58: the pick is build 0 | yes |
| 749.61 the band | 873 | in 4/4 the pool is not the far tail; in 6/8 the median build passes | band dropped; 4/4 pools 308 (58), 428 (54), 363 (55) of the old charge's least half. 6/8: song 52 0 of 76 pass the joint gate (quartiles 4.54 to 5.07 against a gate of 3.57) | 4/4 yes; **6/8 no**. Carried as 749.61 (6/8) |
| 749.62 the old judge chose nothing | 874 | the record lists every gate the pick passed | `gates_passed` and `words_gate` in each record | yes. But see 749.68: in 4/4 the joint and words gates now pass nearly every build |
| 749.63 slots round a ballad's lines to one bar | 869 | song 58 sixteenths within ten points of the kept 15; fit deaths under one in ten | sixteenths 5.3 in 100; no "cannot fit" deaths; 615 of 1000 survive (deaths: 838 326, 840 59) | yes. The song now runs 343 s (749.69) |
| 749.64 weak syllable held at a line's end | 871 | no line-final word holds its unstressed syllable longer, beyond the kept rate | song 58: 0 of 13 two-syllable endings; song 55 0 of 6. One three-syllable word does: "completely", stressed syllable 3 twelfths, last 6 (749.71). Song 52 (6/8, words not read): "worry" 3 then 6 | yes for its scope; widened as 749.71 |

## v21's other fixes

- **867, 868 scaling.** Both exponents are among judge 7's readings ("pitch scaling", "rhythm scaling") and in the directed readings. Song 58's pick: pitch 0.873,
  rhythm 0.471 (kept rhythm 0.61 to 0.72; the paper's own "not met").
- **876, 877 where the voice stays out.** "876: a line sung in one bar, the next bar silent" 1373 times in song 58's run; Turn 2 (two bars) in its form.
- **The breath count.** Real breaths (an onset gap of three beats or more) a minute: song 58 1.8 under v20, 6.1 now; 54 6.6, 55 6.2. Human median 7 (CoCoPops,
  10th to 90th 3 to 13; `studies/breath/rates.py`). 749.65's lead (breath on the grid) did not hold out and asks for nothing.
- **870's cause.** `kept_rests` draws a median of 24 twelfths, but it is drawn only for fresh lines and only where the slot leaves room; lines sung again and
  copies keep their source's join. So the median stays at a quarter.

## New findings from v21 (numbered with v22's in the fix list for v23)

749.68 (gates that pass nearly everything), 749.69 (two lengths for one song, both past the kept 75th), 749.70 (tables and results with no maker in the repo),
749.71 (line-final stress in a longer word). Problem, Evidence, Fix and Check for each are in the fix list for v23 (`songs/p68/fixlist_v23.md`).
