# What gives a kept song's rhythm its long memory? Result

Rule in PREDICTION.md, written first. 160 kept 4/4 songs; Luthier's builds under Window 196.

| | Rank correlation with rhythm scaling | Carries it? | Kept quartiles | Songs 55, 54, 58 (builds) | Song 59 (hold-out) |
|---|---|---|---|---|---|
| Slow change in how busy the singing is | +0.68 | **yes** | 0.34, 0.42, 0.56 | 0.27, 0.25, 0.20: all under the kept 25th | 0.40 |
| Silence (bars with nothing sung) | +0.58 | **yes** | 0.12, 0.19, 0.28 | 0.15, 0.06, 0.11: two under the kept 25th | 0.19 |
| Near answers (a bar's rhythm within the eight before) | -0.16 | no | 0.17, 0.27, 0.38 | 0.19, 0.19, 0.25 | 0.20 |
| Far returns (from over sixteen bars back) | +0.06 | no | 0.13, 0.20, 0.27 | 0.28, 0.37, 0.25 | 0.29 |
| Rhythm scaling | | | 0.61, 0.66, 0.72 | 0.59, 0.57, 0.56 | 0.68 |

**The cause, by the rule: the singing is the same busyness all the way through, and it rests too little.**

- A kept song has stretches where the voice is busy and stretches where it is sparse or silent, lasting many bars. That is what rhythm scaling measures, and those two things carry it.
- Where a bar's rhythm comes back from (near or far) does **not** carry it. The songwriting session's 749.123 and my own guess after Window 195 were both wrong about that.
- The hold-out agrees without being asked: song 59 stands in the kept middle on both things, and its rhythm scaling is in the kept middle too. It is the one song with an eight-bar break and with long verse lines against short chorus lines.

**Why Luthier's songs are like this.** Every line is given a slot of about the same length and filled at about the same rate, verse and chorus alike. And songs 54 and 58 have long lyrics (four and three verses of eight lines, 307 and 337 seconds against a kept upper quartile of 243), so there is no room left for a bar in which nobody sings.

**What follows.** Two different remedies, each needing its own rule and trial:

1. On the engine's side: let sections differ in how busy they are (a chorus of held notes against a verse of quick ones), and keep bars of rest between sections.
2. On the lyric's side: a check when the lyric is locked, before any music, that says how much of the song the words will fill and whether the sections differ in line length. A lyric that fills every bar cannot be given a kept song's rhythm by any setting.
