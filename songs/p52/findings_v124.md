## Findings (450–463)

### 450. Song 45's deaths at 267 come from the bridge's G raised to G-sharp, not from 392 or 398 (corrects 412).

**Problem:** After assembly, song 45 raises every sung G over the bridge's E chord to G-sharp (finding 375's correction). Bridge 3 returns Bridge 0's tune, but the two lines sit over different chords at the same place. So one sings G-sharp where the other sings G, and 267 reads the return as changed early. 412 blamed 392 and 398.

**Evidence:**
- **Where the builds die:** a debug harness on the step-3 code found every 267 failure at Bridge 3 ← Bridge 0, 48 twelfths into the line (G-sharp 56 against G 55), in "both" and "rhythm" returns.
- **412 as proposed** (returns keep their source's range, which was already so; 398 on drawn notes only): 146 deaths at 267 in the main run and 219 in the control (v119: 154 and 216; v118: 33 and 60).
- **With 267 reading the G before its raise** (diagnostic, ZE_DIAG450=1): no deaths at 267, and survivors rose from 551 to 693. Every other count was unchanged.

**Fix:** Read the raise as Q1 A reads 386: 267 compares a return's pitches before the raise. Or make the raise follow the tune, as 394 does for passing notes: raise the G in every occurrence of the tune, or in none.

**Check:** Song 45's deaths at 267 at or under v118's 33, with the raise kept on the bridge's E.

### 451. With 428, empty bars fall far under both collections, and song 45 loses builds at its joins.

**Problem:** 428 removes the empty-bar rate. Lines now fill their slots: 378's spans and 414's density both push the last onset toward the slot's end. Empty bars fall below both collections, and on song 45 the line ahead has less room to breathe before the next one.

**Evidence:**
- **Empty bars** (of eight, main runs): 0.26, 0.26, 0.30, 0.35 and 0.13 on songs 40–45, against CoCoPops 0.47 and BiMMuDa 0.51. Under v119, with the rate, they read 0.34–0.51.
- **Song 45's deaths:**
  - joins (a line with no held end and breath): 96, against 65 under v119;
  - align: 122, against 66;
  - survivors: 551 and 563, against 594 and 594.
- **What does not change them:** neither 413 off (align 103, joins 83) nor 414 off (130, 92).
- **428 off** (the empty-bar rate restored, side run):
  - empty bars 0.35;
  - align deaths 72 and join deaths 64, back to v119's;
  - rhythm deaths 73, against 11 with 428;
  - survivors 588.
- So 428 trades about 60 rhythm deaths for about 80 align and join deaths on song 45.

**Fix:** Keep 428: empty bars are not aimed. Under 378, let a line's span end where the kept lines end, by the bar of the slot (the kept share of lines whose last onset falls in the slot's last bar), rather than only by the share of the time to the next line.

**Check:** Empty bars within a fifth of a standard deviation of the nearer collection, unaimed, and song 45's join deaths within two spreads of v119's 65.

### 452. Separation on the agreed measures is under v118's: 0.719 on songs 40, 42 and 43.

**Problem:** None; this is the check of record.

**Evidence:**

| Run | 40/42/43 across | Five songs across | Pitch | Rhythm | Form (40/42/43) |
|---|---|---|---|---|---|
| v118 | 0.756 | 0.796 | 0.723 | 0.701 | 0.514 |
| v119 step 3 | 0.765 | 0.778 | 0.723 | 0.742 | 0.496 |
| Run 1 | 0.719 | 0.759 | 0.717 | 0.710 | 0.452 |

- **Within songs:** 40 0.884, 42 0.880, 43 0.856, 44 0.962, 45 0.989.
- **Costliest measures, five songs pooled:** pitch spread 0.66 (2.46 against 2.97), gaps of an eighth 0.66 (58% against 48%), range 0.63 (8.9 against 10.9), last note on the tonic 0.23.

The fall is in rhythm and form. Pitch stays where it was.

**Fix:** None. Songs 44 and 45 stay near 0.96–0.99 within; their costs are range and spread (453).

**Check:** At or under 0.756 on later runs, and 425's refit made from these runs.

### 453. Range: song 45's chorus floor (392) is most of the narrowing across five songs; 398 takes 0.2–0.5 semitones on songs 40, 42 and 43.

**Problem:** Range across the five songs fell from 9.30 (v118) to 9.09 (v119) and 8.91 (Run 1), against the pooled kept 10.90. 392 raises song 45's chorus floor to the verse's median plus three, and so halves the chorus window's range. 398's chord-tone weights pull drawn notes toward the chord.

**Evidence:**
- **Window range and pitch spread** (semitones and sd, Verse 1 and Chorus 1 windows, main runs):

| Song | v118 | v119 step 1 | v119 step 3 | Run 1 | 398 off | 400 off | 392 off |
|---|---|---|---|---|---|---|---|
| 40 | 9.58 / 2.53 | 9.90 / 2.67 | 9.74 / 2.53 | 9.52 / 2.49 | 10.00 / 2.68 | 9.53 / 2.50 | |
| 42 | 10.76 / 2.92 | 10.66 / 2.90 | 10.61 / 2.80 | 10.33 / 2.71 | 10.69 / 2.90 | 10.51 / 2.73 | |
| 43 | 10.59 / 2.92 | 10.33 / 2.84 | 10.55 / 2.88 | 10.24 / 2.80 | 10.44 / 2.88 | 10.55 / 2.91 | |
| 44 | 7.90 / 2.30 | — | 8.06 / 2.29 | 7.97 / 2.30 | 7.92 / 2.29 | 7.92 / 2.24 | |
| 45 | 7.67 / 2.25 | — | 6.50 / 1.93 | 6.47 / 1.92 | 6.44 / 1.93 | 6.42 / 1.90 | 7.67 / 2.25 |

- **Song 45's chorus window** ranges 6.09 as run and 8.38 with 392 off.
- **Song 44** sits at 7.9–8.1 in every run. Its costs on the 30 are range 2.75 and spread 1.10.
- **Song 43:** range costs 0.21 here, not the 2.4 of the paper's reading.

**Fix:** For 392, keep the lift over the verse (Q14 A) but leave the chorus at least the kept octave: its floor no higher than the chorus top less eight, as v118 had it. For 398, aim the window's range at the pooled kept mean by the register's widen knob on unaimed builds, beside 398's knobs, as 424 aims its measures.

**Check:** Range within a fifth of a standard deviation of the pooled kept mean on songs 40, 42 and 43. Song 45's chorus window range inside the kept middle half (8–13), with 377's lift failures under one in twenty. Song 44's range printed against its intake.

### 454. Song 43's memory breaks come from neither 386 nor 389; 400's turn knob raises them on songs 43 and 44.

**Problem:** 416 asked what remains of song 43's memory breaks. Neither 386 nor 389 accounts for them. Holding turns down with 400's knob makes the tune less memorable.

**Evidence:**
- **Song 43** (memory breaks by 373's limit; v114: 13, spread 6.6):
  - Run 1 main: 31;
  - 386 off: 35;
  - 389 off: 64;
  - 398 off: 50;
  - 400 off: 24.
- **Song 44:** Run 1 66; 398 off 80; 400 off 37.
- **400's knob** ends at 0.35 (song 43) and 0.14 (song 44). Turns still read 0.60–0.69 against 0.587.

**Fix:** Run 2's 408 (257's contours aimed at the kept turns), with 400's knob held at 0.5 or above.

**Check:** Song 43's memory breaks within two spreads of v114's 13, with turns per move within 0.04 of 0.587.

### 455. 405: runs on drawable lines hold on songs 43 and 44; song 40's densest band runs too much, song 42's sparsest too little, and the rates cannot move them.

**Problem:** 389's rate decides whether a drawable line may run. It does not decide how much a line that may run actually runs, and whether that line keeps any run at all.
- **Dense drawable lines:** they run on most sixteenth positions at any rate.
- **Sparse lines:** they seldom take a sixteenth even when allowed.

**Evidence:**
- **Song 40's 5.5-and-over band:** 50% of drawable lines' sixteenth onsets in runs, against a kept 36%. The rate is at 0.13 (main) and 0.15 (control).
- **Song 42's under-3.5 band:** 11% (main) and 2% (control), against a kept 27%, with the rate at 1.0.
- **Lines by kind** (song 40, main):
  - 18,121 drawable lines;
  - 5,144 fell back;
  - 1,450 had no room.
  - Those that fell back or had no room run 66–79% of their onsets.
- **Song 45's rhythm deaths:** 11 and 12, against v119's 63.

**Fix:** Aim the sixteenth-gap weight by band (354's s16, one knob for each band) beside 389's rate.

**Check:** Drawable lines' runs within ten points of each band's kept share, where a band has 200 onsets or more, on all five songs.

### 456. 409: the window's last note reaches the collections on song 40 alone; elsewhere it is not the walk's to choose.

**Problem:** On most songs the window's last note is set by the song rather than by the walk. It is an ending rule, a copy, a carried extreme, the next section's pickup, or a designed or pinned note. 424's test reads every window.

**Evidence:** Each window's last note, by where it comes from (main runs). The shares are windows, with the tonic share in brackets.

| Song | Last note on the tonic | Walked | By source |
|---|---|---|---|
| 40 | 22.5% (control 24.0%) | 72% | The walk: verse 35%, chorus 16% |
| 42 | 16.0% | 0% | The chorus's last line has an ending rule (38% on the tonic); the verse's ending forbids it |
| 43 | 10.3% | 43% | Walked chorus notes 22% |
| 44 | 1.3% | 0% | The chorus window ends on the next section's pickup in every build |
| 45 | 2.1% | 33% | The walked chorus notes are never on the tonic (0 of 503) |

The knob is at its cap of 10 on all ten runs.

**Fix:** Read 424's last-note test on the windows whose last note the walk chose. Print the rest by source as the song's design.

**Check:** Walked last notes on the tonic between the collections' means, or within a fifth of a standard deviation of the nearer, on every song with 100 walked windows or more.

### 457. 413: the drawn unit returns are lost to the one-onset rule after the line's rhythm is drawn.

**Problem:** A line drawn on a returning unit weights off-copy onsets at 0.04, not zero. Most bars then come out more than one onset off the unit and are left out of the copy (303, 351).

**Evidence:**
- **Free units' returns** against the pooled kept 16.4%, 30.1% and 19.4%:
  - song 42's unit 4: 1.6%;
  - song 43's unit 3: 6.8%;
  - song 44's unit 3: 14.3%, and its unit 4: 7.7%.
- **Held on songs 40 and 45.**
- **Bars left out** (413's count) against bars copied: 6,591–7,678 left out, against 3,144–3,864 copied, on every song.
- **Lines given up and builds lost** are few: 78–1,292 lines and 2–14 builds.

**Fix:** Draw a unit-return line's bars strictly on the unit's onsets (360's strict mode) from the first try. Fall back to the weighted copy at half the tries, and count it.

**Check:** Bars left out under a fifth of bars copied, and unit returns within ten points of the pooled kept rates on the free units of all five songs.

### 458. 414: 423's syllables a second is a song's figure, too low for a line's sung span; on songs 40 and 43 the band and the density part on most lines.

**Problem:** 423's 1.4 to 2.3 syllables a second counts the song's whole time, rests included. Across a line's sung span the kept lines sing faster. So for dense lines the density bound and 378's band do not meet, and the span is drawn from the 5th–95th instead.

**Evidence:**
- **Lines taking the 5th–95th:** 12,016 of 14,015 on song 40 and 9,377 of 9,880 on song 43.
- **Spans given up:**

| Song | v119 | Run 1 (main / control) |
|---|---|---|
| 40 | 16.6% | 13.9% / 13.8% |
| 42 | 9.6% | 1.1% / 0.9% |
| 43 | 5.4% | 5.3% / 5.6% |
| 44 | 1.6% | 1.9% / 1.7% |
| 45 | 21% | 3.5% / 3.4% |

- **Song 45's 6–8-note lines** still read a median share of 0.875, over the kept 53–80%.

**Fix:** Take the density bounds from kept lines: syllables a second across the sung span, by notes in the line (Window 138's lines), not 423's song figure.

**Check:** Spans given up under one line in twenty on all five songs, with the band and the density meeting on most lines.

### 459. 415: bars with verse 1's syllable count are too few on songs 43 and 44.

**Problem:** A bar is read only where verse 2 has exactly verse 1's number of syllable onsets. On songs 43 and 44 that leaves 0–3 bars, and some builds have none.

**Evidence:**
- **Bars read** (median share of verse 2's bars): 25% (song 40), 50% (42), 17% (43), 17% (44), 33% (45).
- **Builds with no such bar:** 244 of 772 (song 43) and 175 of 745 (song 44).
- **The median share** is 0.5 on songs 40, 42, 44 and 45, and 1.0 on song 43.
- **331's rate** ends at 1.0 on song 43 and 0.22 on song 44.

**Fix:** Read the bars whose syllable counts differ by one or less, as 303 lets a copied bar differ by one onset.

**Check:** At least half of verse 2's bars read on every song, and the median share within ten points of 50%.

### 460. The six measures (426) meet 429's rule to enter on every song.

**Problem:** None; a reading for 429.

**Evidence:** Five of the six sit on the same side of both collections on all five songs; the sixth, most onsets in a beat, on four (song 44 between):
- **Longest run of equal gaps:** 5.2–7.4, against 4.9.
- **A gap equal to the one before:** 0.46–0.58, against 0.39–0.40.
- **Gap entropy:** 1.66–1.73, against 1.79–1.84.
- **Phrases that begin at the same place:** 0.47–0.51, against 0.55.
- **Three moves that zigzag:** 0.35–0.43, against 0.32–0.33.
- **Most onsets in a beat:** 2.9–3.8, against 2.6–2.8.

**Fix:** None from the session. Under 429 the six may enter at 425's refit (427's aims are the paper's).

**Check:** Printed on later runs.

### 461. 398 closes the chord-tone gap on two collections; the chorus's first beats sit below the verse's.

**Problem:** None for 431. For 432 and 441: in the chorus, the bar's first note is a chord tone, and the chord's third, less often than in the verse.

**Evidence:**
- **Chord tones (431)**, standard deviations from Billboard:
  - overall: −0.06 to −0.32;
  - on the beat: 0.00 to −0.12;
  - off the beat: −0.10 to −0.49 (song 44 lowest);
  - on the first beat: −0.01 to −0.30.
  - Under v118 these were −0.39 to −0.68.
- **First-beat chord tones** (verse / chorus):
  - 40: 78% / 68%;
  - 42: 67% / 72%;
  - 43: 72% / 63%;
  - 44: 74% / 56%;
  - 45: 69% / 76%.
- **First-beat thirds** sit lower in the chorus on all five songs (for example song 43: 26% / 12%; song 45: 32% / 12%). Kept: Billboard 24% / 25%, Rolling Stone 24% / 31%.
- **442:**
  - a step above a chord tone: 20–31%, against a kept 23–25%;
  - a second or seventh from the bass: 18–34%, against 18–20% (song 44's chorus 34%).
- **443:**
  - parallel fifths or octaves: 5.5–10% of bass moves, against a kept 11–14%;
  - contrary of the two moving: 0.43–0.58, against 0.40–0.43;
  - the bass never stays under a new chord: 0%, against 1.4–6.8%.

**Fix:** For Run 2, if the paper confirms 432 and 441: read 398's downbeat knob by section, so that the chorus is aimed as the verse is.

**Check:** The chorus's first-beat chord tones and thirds not below the verse's on every song.

### 462. The second verse is the section farthest from its kind, and the second chorus is always an exact copy.

**Problem:** A reading for 433, 434, 435 and 437.

**Evidence:**
- **Measures outside the kept middle half for their section** (of 27; songs 40 / 42 / 43 / 44 / 45):

| Section | 40 | 42 | 43 | 44 | 45 |
|---|---|---|---|---|---|
| Verse 1 | 6 | 2 | 5 | 5 | 8 |
| Verse 2 | 7 | 5 | 6 | 10 | 11 |
| Chorus 1 | 5 | 2 | 1 | 4 | 9 |
| Bridge | 7 | 2 | 8 | 10 | 12 |

- **Verse 2 beside verse 1:**
  - the pitch kept where both strike: 0.57–0.67, against a kept 0.72–0.79 (435 asks for three in four);
  - bars of the same rhythm: 0.11–0.20, against 0.28–0.35.
- **Chorus 2:** the same as chorus 1 in every bar of every build. Kept: bars of the same rhythm 0.59–0.71, all bars the same in 27–30% of songs.
- **The last chorus:** the same as chorus 1 on songs 40 and 43, with bars of the same rhythm 0.78 (42), 0.87 (44) and 0.35 (45).
- **The bridge:**
  - notes a bar 4.1–6.2, against kept medians of 3.5–3.75;
  - its top 1–9 semitones over verse 1's (song 44: 9).

**Fix:** For the paper, which ports 434 and 435. Chorus 2 is copied by the song's form (how(): "copy"); a varied second chorus is a design decision for each song's intake.

**Check:** Printed on later runs.

### 463. The writer's edit to song 45 reads as Window 141 read it; the second verse's edit moves the judge the other way.

**Problem:** None; 430's readout.

**Evidence:**
- **The judge used:** v121's provisional judge on the 36 measures, on the pick of record (10c3fce99da2) before and after the writer's Q16 A edits.
- **The chorus 1 window:**
  - the judge reads 1.02 drawn and 0.30 edited, as Window 141 has it;
  - the measures that moved it most: empty bars (one to none, −0.65), peak position (0.77 → 0.27, −0.42), mean interval (−0.25) and gaps of an eighth (−0.21);
  - most onsets in a beat (four to three) moved it +1.18.
- **The verse 2 window** (not read by the judge of record): −3.05 drawn and −2.26 edited. Mean interval (1.59 → 1.77) moved it −0.30 and zigzags −0.17. Against them: notes on the tonic (+0.30), turns per move (+0.29), steps (+0.21) and repeated notes (+0.19).

**Fix:** None.

**Check:** Printed when the writer edits a pick.

## Order of work

1. **450:** song 45's raise read before 267 (its builds return at once).
2. **453:** song 45's chorus floor, and the range aimed. **451:** where a line ends in its slot.
3. **457, 458, 459:** the unit returns' bars, the density bounds, and verse 2's bars.
4. **455, 456:** the sixteenth weight by band, and the last-note test on walked windows.
5. **454:** with Run 2's 406 and 408 (400's knob, 257's contours).
6. **460–463:** readings for the paper (429, 432, 434, 435, 441, 425's refit).

## Regression line

After these fixes, songs 40, 42, 43, 44 and 45 rerun at PYTHONHASHSEED 0, N 1000, main and control, each made twice and reproducing its order. Today's orders:

- song 40: 8f3936c3689d / 014f58a770d5 (seed 20261511);
- song 42: 52dc9a46d9ef / ed52e0e3fdc4 (20261552);
- song 43: 3511c8c7ab62 / 2dd71ca5dab5 (20261553);
- song 44: fab04751f234 / f8f36e0570f7 (20261554);
- song 45 as drawn: 02564e4f9e2a / 4c64cd471575 (20261555).
