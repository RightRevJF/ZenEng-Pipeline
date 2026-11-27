# Kept tables for 3/4 from lead sheets: result (27 Nov 2026). All four tables steady. Nothing given to the engine.

Rule: `PREDICTION_tables_3_4.md` (c95e1e1, with two additions at ee2cff3, both before any table). Figures: `tables_3_4.json`, from `python3 studies/other_metres/tables_3_4.py` (corpora fetched by `fetch.sh`).

## The songs
**538** Wikifonia lead sheets in 3/4 (not the 571 counted earlier: the table script also asks that a song's notes sit on the grid of twelfths and that 60 remain in its 3/4 bars). 511 with English words; 466 composers; 25,831 bars; 25,249 stressed syllables scored. OpenEWLD's public-domain part beside them: 59.

**Dating.** Only 57 of the 538 files carry any year (quartiles 1920, 1957, 1969); OpenEWLD's are 1893 to 1912. Wikifonia is known as mostly standards and show tunes of the 1920s to 1960s, and these figures do not contradict that, but the files cannot prove it. The set is older than the pop collection, and waltz-heavy.

## Steady? (halves split by composer: 297 and 241 songs)
| table | test | halves | steady |
|---|---|---|---|
| Bar rhythms | twenty commonest, correlation 0.9 or more | 0.996 | yes |
| Two-bar windows | twenty commonest, correlation 0.8 or more | 0.967 | yes |
| Stress | stressed syllables on the first beat within 3 points | 65.4 and 64.9 in 100 | yes |
| Notes a beat | medians within 0.05 | 0.787 and 0.768 | yes |

## Beside the others (medians)
| | Wikifonia 3/4 | OpenEWLD 3/4 | Essen 3/4 (folk) | 4/4 pop |
|---|---|---|---|---|
| Notes a beat | 0.78 | 0.76 | 1.15 | 1.07 |
| Notes a bar | 2.3 | 2.3 | 3.4 | 4.3 |
| Onsets on a beat | 0.84 | 0.86 | 0.67 | 0.45 |
| Onsets on the bar's first beat | 0.38 | 0.41 | 0.26 | 0.12 |
| Gaps of a beat or more | 0.76 | 0.80 | 0.39 | 0.35 |

Stressed syllables on the bar's first beat: Wikifonia 65 in 100, OpenEWLD 70, hymns 81. Stressed syllables off the beat: 7, 4, 3.

Commonest bars, share of bars: Wikifonia one note on the first beat 0.22, three quarters 0.20, a half and a quarter 0.16; Essen three quarters 0.155, a half and a quarter 0.115, one note 0.079.

## What it says
- The lead-sheet waltz is a **sparser, squarer** thing than the folk 3/4 the engine has been drawing from: about two notes a bar against three and a half, and one bar in five is a single held note. Song 53 and any 3/4 lyric drawn from Essen's tables would come out busier than a popular waltz.
- The two lead-sheet sets agree with each other on every row, though one is a small part of the other.
- Words: stress sits on the first beat less than in hymns, and more often off the beat, as one would expect of popular song against hymnody.
- Lead sheets are written plain; singers bend them. Some of the squareness is the notation, not the singing. The 4/4 pop column is transcribed from recordings and is not like for like. That gap cannot be closed from these files.

## What I expected, and got wrong
I expected lead sheets denser and more syncopated than Essen. They are sparser and more on the beat.

## What follows (nothing built)
The tables are steady, so a trial is licensed: a 3/4 lyric written through with the draw reading the Wikifonia 3/4 bar rhythms, windows and stress in place of Essen's, marks from the songwriting session first. There is no 3/4 lyric in the from-lyric engine yet (song 53 was made from a hand spec in hymn mode), so the trial needs a 3/4 lyric to run on; a seen one is to be chosen or made.
