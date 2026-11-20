# Review 21 (Luthier v35): is 936 behind the pools' rise?

`song_from_lyric_no936.py` is v35's `song_from_lyric.py` with the repeat weight taken out of the fit (936 off; 934 and 935 left in). Run as a trial through neighbour.py:

    mkdir -p tmp_trial/no936 && cp studies/review21/song_from_lyric_no936.py tmp_trial/no936/song_from_lyric.py
    PYTHONHASHSEED=0 MARGIN_TURNS_OF_FOUR=$PWD/tmp_trial/no936 TRIAL_NAME=v35_no936 python3 studies/soundness/neighbour.py songs/p65/lyric55.json songs/p64/lyric54.json songs/p68/lyric58.json

(The trial copy's HERE points at lib/luthier, so it must sit two folders below the repo root.)

| | v34 | v35 | v35 without 936 |
|---|---|---|---|
| Neighbour choice fails the rule, in 100 | 0.5 | 2.5 | 4.8 |
| A random pick from the engine's pool fails, in 100 | 2.5 | 2.6 | 5.4 |
| Pool builds' repeated notes, under 25th / over 75th | 0.16 / 0.32 | 0.21 / 0.20 | 0.16 / 0.34 |
| Two-sided variety (kept 10.5) | 1.82 | 1.75 | 1.81 |

936 is not the cause: it lowers both failure rates. The rise came with 934 and 935 together. 935 acts in every build of songs 55 and 54 (1,000 of 1,000), not only song 59.
