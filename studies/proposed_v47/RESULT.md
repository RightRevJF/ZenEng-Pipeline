# The flagged patches for v47, tested one at a time: result

25 November 2026. Rules in `PREDICTION.md` (committed before any run). Songs 58, 60, 61, 62; 1,000 builds a song a flag (3,000 for `region`), the real engine with the flag applied (`run.py`; summaries in `runs/`). Chord drafts and the stage 4 readings: `drafts.py`, `drafts_*.json`. Nothing here is built into the engine yet.

## One thing to know before the table

**A chosen tune is one draw, and any flag changes which draw it is.** Across the flags the chosen tune's words' fit moves by up to 0.10 in either direction with no change in the builds behind it (song 61: 0.363 flag off; 0.272 with the octave gate, 0.265 with blue notes off, while the builds' middle is 0.238, 0.244 and 0.242). So a rule that judges a flag by the chosen tune's words' fit to within 0.02, as mine did, mostly reads the draw. The builds' middle words' fit is read beside it below (`builds_median_words_fit.json`) and is the steadier figure.

## The verdicts

| Flag | Its own reading | Builds it kills, in 100 | Builds' middle words' fit, off → on (58, 60, 61, 62) | Verdict |
|---|---|---|---|---|
| `octave` | No chosen tune holds a leap past an octave in a line (flag off: song 60's holds 4; the others none) | 11, 8, 10, 10 of every 100 tried; about 3 living builds in 10 | 0.306, 0.297, 0.238, 0.316 → 0.296, 0.289, 0.244, 0.314 | **Keep.** |
| `title_stress` | Every title line's longest note on a stressed syllable (flag off: 14 of 15 lines; song 62's one title line fails) | 0.2, 2, 4, 5 | → 0.306, 0.294, 0.254, 0.308 | **Keep.** |
| `no_blue` | No lowered third (song 61 flag off: 7; song 62: 0) | none | 61: 0.238 → 0.242; 62: 0.316 → 0.305 | **Keep as a lyric's setting.** Never a default. |
| `vary_returns` | Song 58: two held notes lifted in Chorus 2; song 60: one; songs 61 and 62: no section returns whole | none | chosen tunes 0.307 → 0.308; 0.359 → 0.360 | **Keep.** |
| `region` | All four chosen tunes inside the region (flag off: none of four) | leaves 6, 22, 10, 14 of 3,000 | 0.306, 0.297, 0.238, 0.316 → 0.272, 0.290, 0.232, 0.297 | **Drop as a gate.** |

**`octave`, more fully.** The session counted 12 to 15 builds in 100 killed; here about 10 in 100 of all tries, which is 27 to 42 in 100 of the builds that otherwise live. The gate is a ban. Kept songs, read the same way (a leap past an octave inside a phrase): 28 kept songs of 160 hold at least one (17.5%); the kept 90th is 4.4 such leaps in a thousand notes, about one or two in a song. So Luthier's builds leap this way about twice as often as kept songs do, and a ban is a little stricter than the kept songs. It passes the session's rule and mine. A ceiling of one such leap a song would be the kept-shaped form; I keep the ban as written and note the difference.

**`region`, more fully.** It does what it says: the chosen tunes are plain and pink together. But it leaves pools of one or two builds (song 58: 6 living builds of 3,000, under the session's bar), the builds' middle words' fit falls in three songs, and song 61's chosen tune fits its words at 0.230, under the kept 25th. As I expected. The finding behind it stands (749.170: kept songs do not trade plainness for pink); as a gate it asks more than the draw can give. The remedy is in the draw: fewer notes piled on three pitches. Not tried here.

## Sections that loop less (749.159)

On 1,000 drafted sections a kind (major; the kept median is 0.333 for verses, 0.0 for bridges):

| | Verse: median; share at or under the kept median | Bridge | Chorus median (off 0.364) |
|---|---|---|---|
| Flag off | 0.389; 45% | 0.140; 41% | 0.364 |
| Templates (the session's patch) | 0.231; 69% | 0.000; 68% | 0.364 |
| Structure (its first repair) | 0.286; 59% | 0.056; 48% | 0.373 |
| Gate (its second repair) | 0.143; **99%** | 0.000; **96%** | 0.375 |

| Check | Templates | Structure | Gate |
|---|---|---|---|
| 1. Chosen plans' verse and bridge at or under the kept median, 3 songs of 4 | verse 3 of 4, bridge 2 of 4: **fails** | verse 2 of 4: **fails** | verse 4 of 4 (0.31, 0.31, 0.29, 0.31), bridge 3 of 3: holds |
| 2. Chorus within 0.02 of flag off | holds on the drafts | holds | holds (0.375 against 0.364) |
| 3. Stage 4 readings no further from held-out kept sections than the unpatched writer by more than 0.02 | **fails** (verse bigrams +0.058, bars +0.022) | **fails** (verse chords, bigrams, bars) | **fails narrowly**: verse bigrams +0.028, bridge last chord +0.087; verse first, last and bars are *nearer* the kept sections (−0.051, −0.044, −0.083) |
| 4. Words' fit | builds' middle unchanged | unchanged | unchanged (0.306, 0.297, 0.238, 0.316 → 0.304, 0.294, 0.247, 0.313) |
| 5. A fresh hold-out (song 63) | not run | not run | not run |

- Check 2 as the session wrote it, on the one chosen plan, fails for every form: a different draw of twelve drafts gives a different chorus (song 58's 0.14 becomes 0.63, 0.24 or 0.69). On the drafts the chorus does not move. I read it on the drafts.
- **The session saw the fault in its own patch rightly:** filtering kept templates leaves song 61's verse at 0.64. Only the gate holds check 1.
- **The gate does more than asked.** It puts 99 verses in 100 at or under the kept median, where kept verses are half over it by definition. Kept verses are plain periodic loops 30 times in 100; the unpatched writer's 32; the gate's 17. It does not bring the writer back to the kept rate: it takes it well under.
- By my own check 3 no form passes, the gate nearest.

**Where that leaves it.** The gate is the only form worth carrying. It costs nothing in the words. It is not a pass, it has met no hold-out, and it moves the writer away from kept sections in how often a verse simply loops. My view, written before the runs and unchanged: a setting a lyric can ask for, not the default, until fresh songs settle the covers finding. A gentler gate (redraw only verses over the kept 75th, so the writer's excess is trimmed and the kept spread kept) is the form I would try next, rule first.

## Against what I expected

- `octave`: I expected 10 to 15 in 100 killed and no cost. Right on both.
- `title_stress`: about 3 in 100 killed, kept. Right.
- `region`: under 3 in 100 left, words' fit down in two songs or more. Right (0.2 to 0.7 in 100 left).
- `loop_less`: I expected templates to fail check 1 (right), the gate to pass check 1 (right) and to fail check 3 on bars or bigrams (it fails on bigrams, narrowly, and is *better* on bars), and structure to land between (it lands last).
- What I did not expect: how much the chosen tune's words' fit moves with any change at all. My own added rule for the flags could not read what it was written to read.
