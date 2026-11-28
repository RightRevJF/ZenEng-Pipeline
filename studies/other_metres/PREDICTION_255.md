# 749.255, 956's ceiling outside 4/4 at the metre's own table: the form and marks, before any code or run; and the list of 4/4-only settings

28 November 2026, 07:19 ET. Accepted and numbered by the songwriting session (07:10 ET), with its marks. (Counted before this file, as asked: the ceiling. No engine code, no build.)

**The form (`LUTHIER_CEILING_TABLE=1`, unset by default):** outside 4/4, 956 acts where a file of the commonest-pitch share stands beside the metre's table, at that table's own 90th: a build whose verses, pooled, or choruses, pooled, put more of their notes on one pitch than the ceiling is passed over (waived, as in 4/4, where no build past the other gates passes). No file beside the table, no gate.

**The ceiling, printed before the run** (`trial_tables/3-4_pop_sung.commonest.json`, made by `pop_commonest_by_part.py` from the raw clips, which stay outside the repository):
- Hooktheory gives **no section label** (all 399 clips of 20 notes or more: no label). So, as ruled, the clips' own 90th stands for every part: **0.396** for verse and for chorus. The clips' 10th, 25th, 50th, 75th, 90th: [0.159, 0.203, 0.261, 0.318, 0.396].
- For comparison, 4/4's ceilings (the kept 90th by part): verse 0.44, chorus 0.479.
- *Said plainly:* a clip is one section; 956 reads all of a song's verses pooled and all its choruses pooled. A pooled part is longer than a clip, and a longer stretch tends to a lower commonest share, so the gate is if anything a little loose. K5 stays a test at the by-song 75th (0.303).
- The 6/8 folk table has no such file, so the form does nothing in 6/8.

## Trial
Pop 3/4, song 55's words, the package of RESULT_253_254's arm 2 with the switch, seeds 1, 2 and 3, 1,000 builds each.

## Marks (the songwriting session's)
1. Every mark on the living median at seeds 1, 2 and 3, all nine figure marks (with the share drawn fresh, the chord mark, the source lines at 0.40, late lines at 0.15 as before).
2. The pool on the six like marks at or over 76.2 in 100 at each seed.
3. K1 at each seed: living at least 30, pool at least 10.
4. The pick reported at each seed (not a mark this round).
Watched: 838 (flag over 450); the pool's share meeting all nine; how many builds the ceiling passes over.

Checks: the five 6/8 lyrics on song 69's package with the switch set come out byte for byte the same; every switch unset, 54, 55, 52 and song 53's Essen arm byte for byte; room files after.

## What I expect
- At seed 3 the ceiling (0.396 by part) passes over the worst builds, but K5 reads the whole song at 0.303 and seed 3's pool median is 0.318: a part ceiling at 0.396 is a long way above that. **I expect seed 3's median commonest pitch to fall only a little, to 0.30 to 0.32, and K5 to miss still at seed 3; one chance in three that it passes.** Seeds 1 and 2 keep every mark on the median.
- Mark 2 and K1 are met at every seed.
- If K5 still misses at seed 3, the K5-by-lift count is next by the ruling.

## The list: settings that sit inside the planner's 4/4-only lines (a list, no form)
Read from `lib/luthier/song_from_lyric.py` and `metre_engine.py` today. "Off" means absent outside 4/4.

| Setting | In 4/4 | Outside 4/4 today |
|---|---|---|
| 731's floor (stressed syllables on a beat) | the kept 10th by song (0.35) | on, at the engine's hand-set 0.4, not a table's figure |
| 912: every kept two-bar rhythm may be drawn | on | off (the twelve best-scored of the table's windows) |
| 922/923: the page gate's floor | on | off; stays off until its evidence is restated without TheSession (749.242) |
| 956: the commonest-pitch ceiling by part | on, the kept 90th | **off** (749.255 is this) |
| 749.220: the bridge's ceiling | a trial, off | off |
| 959: no leap past an octave in a line | on | **off** (K7 tests it; no build has broken it in these trials) |
| 961: the title line's longest note on a stress | a setting the lyric asks for | off |
| 879 to 882, 881: the words' weights and the words' gate | on (kept table) | off: no kept table of words outside 4/4; 749.231's stress file stands in for the place part |
| 899: the kept line ends (and 771's entry shares read from them) | on | off; **771's entry weights are on at the engine's default (0.20, 0.42, 0.38 for a stressed opening), a 4/4 figure** |
| 834: the early entry | on, one time in five | on at the same 4/4 share (749.253 turns it off) |
| 870: the rest a line may wait | 4/4's kept rests | on at 4/4's rests (749.245 gives the table's own) |
| 876: a line in one bar, the next silent | 0.09, a 4/4 count | **on at 4/4's 0.09** |
| 818: a line sings the line two above again | 0.8, fitted to 4/4's kept median | **on at 4/4's 0.8** |
| 920, 925: the aimed kept song and its lift | on | off; the lift is drawn from the kept (4/4) songs' lifts |
| 958: the verse sung closer | on | off |
| 966, 967: a copy's clash, melismas cleared | on where set | off |
| 749.207 borrow_kept, 749.216, 749.201, 749.198, 964 | trials or 4/4 tables | off |
| 883, 899, 903: the record's readings of words' fit and line ends beside the kept | on | off (reports only) |

Three more 4/4 figures act outside 4/4 without a table of the metre behind them, beyond the two already mended (749.245, 749.253): **771's entry weights, 876's 0.09, and 818's 0.8.** And the lift (838) is drawn from 4/4's kept songs in every metre. I have not traced every constant in the engine (the move weights, the registers' plan); this list is the planner's 4/4 lines and what tonight's counts met.
