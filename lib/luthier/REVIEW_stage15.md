# Review 15: Luthier v28 (fixes 913–915)

Branch `luthier-v8-stage1` at b3fa22d, main merged in.

## Byte for byte

The tables are unchanged. The song reruns (54, 55, 58 and 52 by `song_from_lyric.py`; 52 and 53 by `metre_engine.py`; 53's hymn parts; stage 4) reproduce every committed record. `git status` is clean after them.

## 913: WORD_PLACE 0.75; the gate on length and height

As written. The whole fit is held only to the kept floor; length and height are gated at the builds' medians. The picks' stressed syllables on a beat are 0.545 / 0.504 / 0.597 (songs 55, 54, 58), as predicted. Read on the notes as sung, every fit reading is inside the kept middle half except song 55's fit by length (0.387, past the kept 90th, 0.369). That is one song, not a lean.

## 914: the words' gate reads each build as sung

`melisma_notes` is 848's draw, unchanged, as a function of the notes. `Engine.as_sung` hands it the builds written on C, with the scale on C, which matches how the builds are written. The draw's only randomness is the title's seed, and its choices depend on lengths, stresses, words, lines and the step below, none of which a key shift changes. So the gate's melismas for the pick are the melismas the record ends up with. Holds.

## 915: look ahead before a run-on

The look-ahead runs to the next line's last onset plus the least last note. Phrases over 12 beats: 0.041 / 0 / 0; longest 17.0 / 10.5 / 10.0. Song 55's 17 beats is one long line with no rest inside it, which no line-end rule can split. Holds.

Line ends moved as a side effect. Stressed line ends held a half note or more: 0.34 / 0.27 / 0.08 (v27: 0.18 / 0.09 / 0.27; kept pooled 0.29). Song 58's 0.08 looks low against the pooled share, but read song by song, kept songs run 0.075 to 0.52 across the middle half. Read the same way, 58 is 0.105 and inside it.

## The soundness checks

`studies/soundness/soundness.py` and `SOUNDNESS.md`: 23 checks, each read the same way on the 160 kept songs and on the three records. The rule asks that the three songs not lean together:
- no check with all three beyond the kept 10th or 90th on the same side;
- no more than two checks with all three beyond the 25th or 75th on the same side.

Three kept songs drawn at random fail it 6.8 times in 100. Under v28 one check fails: rhythm scaling, all three under the kept 10th.

## Rhythm scaling (749.93)

Across the kept songs, rhythm scaling follows how much the density of sung onsets changes over a song. The Spearman correlation is 0.65 with the spread of onsets per 4-bar block, and 0.56 with the share of 4-bar blocks the voice leaves empty (`studies/soundness/rhythm_scaling_why.py`).

| Reading | 55 | 54 | 58 | Kept 25th / median / 75th |
|---|---|---|---|---|
| spread of onsets per 4-bar block | 0.236 | 0.137 | 0.250 | 0.353 / 0.438 / 0.554 |
| 4-bar blocks with no sung onset | 0 | 0 | 0 | 0 / 0.082 / 0.129 |
| silences of two bars or more | 1 | 0 | 0 | 1 / 2 / 3 (877) |
| chorus's density over the verse's | 0.89 | 0.99 | 1.01 | 0.77 / 0.88 / 1.06 |

Section against section, the density is kept-like. What the songs lack is the voice leaving for whole stretches. 888 drops the turn when it would take a song past the kept 75th of lengths, and in all three songs it would, so none keeps one.

Taking an earlier line's rhythm does not help. With 818's rhythm borrow at 0, 0.2 and 0.4, song 58's builds read 0.475, 0.463 and 0.436 for rhythm scaling (`rhythm_borrow_sweep.py`).

Pitch scaling (58: 1.20, past the kept 90th) follows the lift as it does in kept songs. Kept songs with a lift of 8 or more have a median pitch scaling of 1.115 (`pitch_scaling_lift.py`). It is not a separate fault.

## Merged

`origin/luthier-v8-stage1` into main at 88f4091, no fast-forward.
