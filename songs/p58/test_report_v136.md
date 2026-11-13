# The Ratios Hold: test report, ZenEng v136

*Words and music: Jason Bryant. The spec is ZenEng v136 (v135 plus Module 27.80, Window 156). Ported here in one pass:*

- *573 and 577 from v135;*
- *578 (the session's 583, amended): every drawn line takes its gap values and run lengths from kept lines of its slot's rate band, from zeneng_v136_slot_rate.json, using the two-bar-slot tables;*
- *579 (the session's 584): class 0 for lines of 13 notes and over in two-bar slots, at the kept share for the line's own rate;*
- *589: a reading only.*

*Song 48 was rerun once, main and control, with the same seed and the writer's same designs. The judge was not refitted. The engine of record is gen_v136_p58.py, which writes melody_v136_p58.py from melody_v134_p58.py. The song's record and documents are unchanged: the v134 pick stands. New findings are numbered from 590.*

## How the ports were made

- **578:** each drawn line (three syllables or more, not fixed) takes the kept position table (372) for the band of its slot's rate, read as 504 reads it: notes over the slot's bars.
  - The table is reweighted so that its share of each gap value matches the kept lines' share in the two-bar-slot table.
  - The line carries no aimed weights, as under 551, and its runs are drawn from the band's kept lengths (1 to 8, where 8 means 8 or more), as 558 drew them.
  - 551's caps stand where 551 and 558 put them.
- **579:** the line's own rate is not known until its rhythm is drawn, so it was read as 551 expects it (the kept middle span). Finding 592 shows that this reading was the wrong one.
- **573:** a plan return that adds three syllables or more, and whose fit fails, becomes a fresh line, counted.
- **577:** 566's loop runs three times, so the source can be redrawn a second time; the redraws are counted.

## In brief

| Reading | v134 (main / control) | v136 (main / control) | Test |
|---|---|---|---|
| Survivors | 918 / 926 | 886 / 937 | — |
| 557, verse | −1.38 / −1.40 | −1.32 / −1.40 | printed |
| 557, chorus | −2.29 / −2.53 | −2.26 / −2.32 | printed |
| Verse sixteenths / eighths / quarters | 48 / 39 / 6% and 49 / 38 / 7% | 48 / 40 / 5% and 49 / 38 / 6% (kept 29 / 54 / 8%) | misses (591) |
| Chorus sixteenths / eighths / quarters | 7 / 71 / 18% and 6 / 73 / 18% | 18 / 59 / 14% and 20 / 55 / 16% (kept 10 / 58 / 18%) | eighths and quarters pass; sixteenths are the hook's (590) |
| Dense lines' median longest run | 4 / 4 | 4 / 4 (kept 4) | passes |
| 579 class 0, 13 notes and over | 0.654 / 0.638 | 0.700 / 0.686 (kept 0.65 / 0.51 / 0.34 by rate) | misses (592) |
| 589, verse window ends on the tonic | 1.6% / 1.2% | 2.3% / 2.3%, always under B | printed (593) |
| Join deaths | 1 / 1 | 1 / 0 | passes (577) |

## Findings (590–)

### 590. 578 in the chorus: the eighths come down to the kept share; the sixteenths over it are the hook's.

**Problem:** None for the drawn lines. The section's sixteenths sit 8.6 and 10.5 points over the kept share, and the excess is the writer's hook: its figure is half sixteenths (gaps of 6, 6, 3, 3). It is sung in every chorus, so the control misses 578's test by half a point.

**Evidence** (Chorus 1, all lines; main / control; kept: two-bar slots, by each line's slot band, weighted by gaps):

| Gap | v134 | v136 | Kept |
|---|---|---|---|
| Sixteenth | 6.6% / 6.3% | 18.2% / 19.5% | 9.6% / 9.0% |
| Eighth | 71.2% / 72.5% | 59.1% / 54.8% | 58.0% / 58.1% |
| Quarter | 18.3% / 17.7% | 13.9% / 15.8% | 17.7% / 17.9% |

On the main run, sixteenths make up 14.3% of the drawn (fresh) lines' gaps against 50% of the hook's. The last chorus reads the same as the first (17.7% / 18.9%; 60.3% / 56.2%; 13.5% / 15.4%).

**Fix:** Read 578's test on drawn lines, with the designed lines set aside.

**Check:** Drawn chorus lines within ten points of the kept shares for all three gaps.

### 591. 578 in the verse: the shares do not move, because the verse sings more notes in a shorter span than the band's kept lines.

**Problem:** The verse lines are drawn from the slot band's table, reweighted to the kept shares, and still sing about half their gaps as sixteenths. Their slot rate is 7.2 notes a bar in a band that starts at 5.5 (the kept mean is 6.4). A line of 14.7 notes over 0.75 of its slot cannot keep the kept mean gap.

**Evidence** (Verse 1; main / control; kept 5.5 and over, two-bar slots):

| Gap | v134 | v136 | Kept |
|---|---|---|---|
| Sixteenth | 48.3% / 48.6% | 48.2% / 49.1% | 29.4% |
| Eighth | 39.1% / 37.9% | 39.8% / 38.3% | 53.7% |
| Quarter | 6.3% / 7.2% | 5.4% / 5.9% | 7.5% |

- Verse 2 reads the same: 49.4% / 50.7% sixteenths.
- The bridge (14-syllable lines) is at 41.3% / 41.5% against 26.1%.
- Verse lines (main): 14.7 notes; first to last onset 0.75 of the slot (the kept median is 0.786); mean gap 5.2 twelfths of a beat. The kept table's shares give a mean gap of about 6.0.
- At that mean gap, 13.7 gaps need 0.86 of the slot, near the band's kept 75th percentile (0.872).

**Fix:** Give the kept gap values in narrower cells of slot rate inside 5.5 and over (for example 5.5–6.5, 6.5–7.5, 7.5 and over), and read the test against the cell of the line's own slot rate. If kept lines at 7 and over also sing near half sixteenths, the verse already stands at the kept figure and the test, not the engine, is what misses.

**Check:** The verse's sixteenths, eighths and quarters within ten points of the kept shares for the cell of its slot rate.

### 592. 579 misses: the line's rate, read before its rhythm, puts most long lines in the wrong cell.

**Problem:** 579 draws the class by the line's own rate, but that rate is known only once the rhythm is drawn. The port read it as 551 expects it (the kept middle span), which put 86% of draws under 8 notes a bar (class 0 at 65%). The lines as sung run at 8 to 10 and over, where the kept class 0 share is 51% and 34%. Class 0 rose from 0.654 / 0.638 to 0.700 / 0.686.

**Evidence** (reachable drawn lines of 13 notes and over in two-bar slots, by the rate as sung; class 0; main / control):

| Rate as sung | Lines | v136 | v134 | Kept |
|---|---|---|---|---|
| Under 8 | 222 / 250 | 0.671 / 0.664 | 0.717 / 0.695 | 0.65 |
| 8 to 10 | 6,121 / 6,072 | 0.702 / 0.695 | 0.659 / 0.641 | 0.51 |
| 10 and over | 2,537 / 2,569 | 0.697 / 0.668 | 0.635 / 0.618 | 0.34 |
| All | 8,880 / 8,891 | 0.700 / 0.686 | 0.654 / 0.638 | 0.517 |

The class was drawn at the rate read under 8 in 5,991 / 5,987 lines, and at 8 to 10 in 1,000 / 1,000.

**Fix:** Read the rate from the span the line's slot band gives (578's first-to-last share for the band: 0.786 for 5.5 and over in two-bar slots, so about 8.3 notes a bar for a 14-note line). Or draw the class after the span is drawn, when the rate is known.

**Check:** Class 0 within ten points of the kept share for the rate as sung.

### 593. 589: the verse's window ends under the dominant in every build; the chorus's window ends on the hook.

**Problem:** None; a reading. The song's chart puts B (V) under the last note of the verse's window, a half cadence at bar 8 of the verse. The tonic is not a tone of B, so 424's weight toward the tonic cannot land without a non-chord tone. The chorus's window ends under E, where the tonic is a chord tone, but its last note is the hook's held B4, the writer's.

**Evidence** (main / control):

| Window | Last note on the tonic | Chord under it | Tonic a chord tone |
|---|---|---|---|
| Verse 1, v136 | 2.3% / 2.3% | B in 100% | no |
| Verse 1, v134 | 1.6% / 1.2% | B in 100% | no |
| Chorus 1, v136 | 0% / 0% | E in 100% | yes |
| Chorus 1, v134 | 0% / 0% | E in 100% | yes |

**Fix:** None. For the paper: read the kept windows' last note on the tonic by the chord under it. If kept windows that end under V seldom end on the tonic, the verse's 2% is the kept figure for its chart, and 424's aim belongs only to windows that end under I.

**Check:** Printed.

### 594. 557 by section after 578: the chorus control comes nearer by two tenths; the rest within a tenth.

**Problem:** None; a reading.

**Evidence** (the judge of v132, not refitted; score less the band's kept mean; windows under the band's kept 5th; main / control):

| Window | v134 | v136 |
|---|---|---|
| Verse 1 | −1.38 / −1.40; 26.9% / 27.7% | −1.32 / −1.40; 27.6% / 29.0% |
| Chorus 1 | −2.29 / −2.53; 41.8% / 47.4% | −2.26 / −2.32; 39.6% / 40.4% |
| Both | −1.83 / −1.97; 34.4% / 37.6% | −1.79 / −1.86; 33.6% / 34.7% |

The v134 figures were read again here with the same code and match Window 156's.

**Fix:** None.

**Check:** Printed.

### 595. The run: survivors, deaths and the ports' counts.

**Problem:** None; a reading. 578 costs the main run 32 survivors, mostly through two limits: the longest notes in eight bars, and memory.

**Evidence** (main / control):

- **Survivors:** 886 / 937 (v134 918 / 926). Orders 473ea72c00d9 / 54d5fcc4eae6. Seed and designs as v134.
- **Limit deaths:** 44 / 20 (v134 21 / 15). Run_max 24 / 12; the longest notes in eight bars 17 / 12 (v134 1 / 3); memory 14 / 12 (v134 1 / 3).
- **Design deaths:** the chorus above the verse 46 / 28; the bridge's build 4 / 1.
- **Join deaths:** 1 / 0, at ('Verse 1', 3). That is under two in a thousand, so 577's test passes. Align deaths 0 / 0.
- **573:** no fallbacks; no plan return in song 48 adds three syllables.
- **577:** no second redraws.
- **578:** 17,542 / 17,561 lines drawn by their slot's rate (12,552 / 12,576 at 5.5 and over, 3,992 / 3,988 at 3.5 to 4.5, 998 / 997 under 3.5). The drawn run length could not be met in 64,217 of 243,166 draws (26%) and 64,051 of 241,774 (26%).
- **Dense lines** (nine notes or more at eight a bar and over): longest equal-gap run, 50th / 75th / 90th / 95th, 4 / 5 / 6 / 7 on both runs (kept median 4). The test of 558 and 578 holds.

**Fix:** None.

**Check:** Printed.
