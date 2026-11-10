# ZenEng fix list after v91

*Song 36 onward · fixes 194–205 · with the test results the brief asked for, the rule-by-rule run, the deaths per gate and the tables gaps*

v91's version row (v125) ends at fix 193, checked before numbering. This list starts at 194 and covers every song since v91. Each fix gives the problem, the evidence, the proposed fix and the check.

The brief for song 36, as relayed by the writer:

- ZenEng_v91.docx is the single source of the rules. Read the tables (zeneng_v88_tables.json, zeneng_v91_hymn_supplement.json), don't refit; the paper decides at an edge.
- Port into the code before the search, in this order: 181, 182, 178–180, 184, 191–193 (and 183).
- Write a pop, rock or country song; show the full lyric before any music.
- Report: for 181, every section's phrase-design label at 8 and 16 bars and the stock share; for 182, the pick's pitch surprise, the spread across builds, and its shares of repeated notes, steps and leaps past a fifth; exact bar repetition; a control with 181 and 182 off (same seed and N) with the same readings on its first pick; deaths per gate, and for each gate met by construction its control failures (184); which fixes ran, which could not, and why.
- Number new findings from 194.

The test results follow the fixes, as Reports 1–3.

## Songs since v91

| Song | Title | What it tested | Fixes found |
|---|---|---|---|
| 36 | Dance Anyway | The pop class under v91, with 181, 182, 178–180, 184 and 191–193 ported first. A woman alone in her kitchen at 2 a.m. dances to an old song; the bill stays unpaid, the clock stays wrong. Female mezzo B♭3–D5; 4/4 at ♩ = 118, E♭ major, four-on-the-floor disco-pop; 88 bars, 2:59. Chords by the section jobs of 177, the bass the chord roots (183). Two controls: 181 and 182 off, and the constructions off. | 194–203 |

## The fixes

### 194. Secondary stresses are read as stresses

**Problem:** The stress reading marks a syllable stressed when the dictionary gives it a primary or a secondary stress. 191 removes only a second primary stress, so a word with a primary and a secondary keeps both.

**Evidence:** In song 36's lyric the reading put two stresses on 'July' (JH UW2 L AY1), 'radio' (R EY1 D IY0 OW2), 'microwave' (M AY1 … W EY2 V), 'somewhere' (S AH1 M W EH2 R) and 'anyway' (EH1 N IY0 W EY2). None has two primaries, so 191 acted on nothing. Read as written, 'July' would be set ju-LY with both syllables strong and 'radio' with a stress on its last syllable.

**Fix:** In a word of two or more syllables only the primary stress counts. A secondary stress counts only on a line's last syllable, where it carries the rhyme or the hold ('dance an-y-WAY'). No list.

**Check:** Reread songs 21–36: no polysyllable away from a line's end carries two stresses; the declamation reading changes only on those words.

### 195. 181's relatedness test reads bar windows, so the next line's pickup and a held last note decide it

**Problem:** 27.31 reads a unit as an equal span of bars. The window holds the next phrase's pickup, which differs between a first unit and its return, and a line that holds its last note for a third of the window is decided by that note, so the ending 181 lets change can break the contour test. Lines whose syllable counts differ cannot keep the onsets at all.

**Evidence:** Song 36 built every named return from its first unit's rhythm and pitches, gave a broken return its first unit's pitches back, and still 204 of 500 builds had a named return the test called unrelated (143 died at it first). By place: Bridge line 3 → line 1 (2 bars) 94; Chorus 1 line 3 → line 1 (2 bars) 85; Verse 1 line 3 → line 1 (2 bars) 28; Chorus 1 line 7 → line 3 (4 bars) 24; Verse 1 line 4 → line 2 (2 bars) 17. The bridge return (12 syllables on 9) failed most. In one case traced during development the two units' notes were identical but for the held last note (E♭4 against A♭4, 24 of 64 sixteenths) and the next section's pickup; the correlation was 0.59. The engine had to add a rule of its own: a form names a return only between lines within three syllables of each other, the extra syllables going before the unit as a pickup.

**Fix:** Read a unit from its first onset to the next unit's first onset, so the next phrase's pickup is outside it; leave a changed last note out of the contour test (it is the ending 181 lets change); and say in 181 that a form names a return only between lines whose syllable counts differ by three or fewer, the extra syllables sung as a pickup.

**Check:** Rerun song 36's search: no build dies at 181 where its construction was used; the 8-bar stock share stays at or above the chart's 39%.

### 196. The monotony floor's three-pitch clause is not obeyed by kept pop

**Problem:** 166 (from v43) asks at least three distinct pitches in every line-length phrase. Under 132 a universal gate must be obeyed by kept songs; in pop this clause is not.

**Evidence:** The tables' gate audit (198 chart songs) gives two-pitch lines at a median of 7.4% of lines (deciles 0, 0, 7.4%, 18.9%, 50.4%); only 34.3% of songs have none. In song 36 the floor killed 121 of 500 builds with its run clause built into the walk; with 182 off it killed 318.

**Fix:** For pop, rock and country keep 'no pitch more than three times running' as the floor and make 'three pitches a line' a reading: the song's two-pitch share printed against the chart's deciles. The notated classes keep the clause where their corpora obey it.

**Check:** Song 36 rerun: monotony deaths come from the run clause only; the two-pitch share is printed.

### 197. 182's walk can draw several leaps past a fifth in a row

**Problem:** Drawing each move from Table CG independently lets rare leaps come back to back. Kept melodies turn after a leap.

**Evidence:** Under the rules before this fix, the search's #1 (afd2849fd733) had a bridge line of three leaps past a fifth in a row: B♭4–C4–A♭4–C4 on 'July, I sat'. Each was a 2–3% draw, and the composite ranked the build first.

**Fix:** After a move past a fifth, the next move is a step or a third in the opposite direction. Song 36 ran with this rule; it is the engine's and is not in the paper.

**Check:** No survivor has a leap past a fifth followed by another leap; the leaps-past-a-fifth share stays within the class's band.

### 198. The shares the walk draws are not the shares that survive

**Problem:** 182 says the walk draws from Table CG's interval habits. The finished melody adds moves the draw does not make and loses builds the gates kill, so the shares that reach the song are not Table CG's.

**Evidence:** The walk draws repeats 27.6%, steps 42.6%, past a fifth 3.0%. The main run's complete builds read 23.7%, 47.3% and 1.3% at the median; the pick 17.0%, 49.7% and 4.7%. Causes: a melisma's second note is always a step; a split event in a mapped line is a step; the monotony floor kills repeat-heavy builds.

**Fix:** Read 182's shares on the finished melody and aim the draw so the finished melody lands near the class's medians (repeats drawn a little above 27.6%, steps a little below).

**Check:** The main run's median repeats, steps and leaps past a fifth within two points of Table CG's.

### 199. The walk puts too few notes on chord tones

**Problem:** The three-term pitch model has no chord in it, and the walk's light chord weight on stressed beats does not make up the difference.

**Evidence:** The pick puts 40% of its notes on tones of the bar's chord (Billboard melody_chord_tones median 62%; Hooktheory pop 72% on the beat, 62% off it), resolves 29% of the others by step (45%), and sets the key word on a chord tone in 50% of lines (chart 73%). The key-word gate (134) killed 42 builds and would have failed 94.

**Fix:** Add the chord to the walk on the beat: a chord-tone term fitted to the class's chord-tone shares on and off the beat, and print the melody's chord-tone share against harmony_by_class.

**Check:** The pick's chord-tone share between the chart's 25th and 75th percentiles; key-word deaths fall.

### 200. Table CG gives pop ♭3 and ♭7 in major, but not over which chords

**Problem:** The class key profile sings ♭3 (3.7%) and ♭7 (3.2%) of notes in major keys. A walk that draws them without the chord can set them against chord tones a semitone away.

**Evidence:** An early song 36 pick put G♭ over C minor (a diminished fifth over the root, on the stressed 'floor') and G♭ over B♭; a copied line carried G♭ onto an E♭ chord.

**Fix:** Sing ♭3 and ♭7 only where no chord tone lies a semitone away and the note is not a tritone from the root (in E♭: G♭ over A♭, D♭ over E♭ or D♭). A copied note that lands on a clash moves to the nearest scale tone, a chord tone first.

**Check:** No ♭3 or ♭7 a semitone from a chord tone in any survivor.

### 201. A two-bar line packs its syllables into sixteenths, and nothing reads it

**Problem:** The form gives each lyric line two bars; 159 and 163 read rhythm a bar at a time and as one band. A line of many syllables is crammed into sixteenths, its last note held long, and the band passes it.

**Evidence:** Song 36's lines run 6 to 14 syllables at ♩ = 118. The pick's gaps between notes are a sixteenth 38% of the time (Hooktheory pop 2%); onsets on sixteenths 24% (4.5%); a line's last note 6.5 times its median note (2.0); melisma 4.1% of syllables (16.4%). Rhythm 2.35 bits, inside the band 1.33–3.57.

**Fix:** Give a line its span from its syllable count (about four or five syllables a bar at this tempo, so a 13-syllable line takes three bars or the lyric is cut), and print sixteenth gaps, onsets on sixteenths and final lengthening against rhythm_by_class and text_setting.

**Check:** Song 36's sixteenth-gap share within Hooktheory's 5th–95th; final lengthening near 2.0.

### 202. A declared summit is placed without its position read

**Problem:** 165 places the summit where the design names it; 151 reads where kept songs put their peak. The intake asks for the summit without showing 151's figure.

**Evidence:** Song 36's D5 falls 97% of the way through, in the last chorus. Chart pop's peak sits at a median 31% of the way in, and in the chorus or bridge in 67% of songs.

**Fix:** When the intake asks for a summit (133's design clause), show 151's position figure beside the options.

**Check:** The intake's summit question prints the position reading.

### 203. 192 has nothing to check in a band arrangement

**Problem:** 192 asks that the joint draw of tune and bass leave two inner voices able to complete the chord. A band song has no joint draw: the band plays whole triads over a root bass.

**Evidence:** In song 36 the check passed on all 500 builds; it cannot fail with a root bass under band triads.

**Fix:** Scope 192 to the classes whose bass is drawn with the tune (hymn, carol, concert solo). In the band classes print instead whether the tune doubles the leading note in the bass, which a root bass on V cannot do.

**Check:** A band song's report lists 192 as not applicable.

### 204. Nothing ranks the bridge

**Problem:** Table B and the composite (Table C) read verse 1 and chorus 1 only. Every other section, the bridge included, only has to pass the gates. Nothing asks a bridge to change gear and leave a melodic shape of its own.

**Evidence:** Song 36's bridge passed every gate and was never scored: lowest in the song (B♭3–A♭4), at the verses' sixteenth-packed density. The writer: "the melodic line itself is more functional than distinctive."

**Fix:** Score every section against its job. For the bridge: a contrast term (fewer onsets or longer notes than the verse, a contour unrelated to verse and chorus by 27.31's test) and a memory term of its own, ranked beside the composite.

**Check:** A rerun's bridge has longer notes than its verse, a contour unrelated to verse and chorus, and its score printed.

### 205. Nothing writes an instrumental hook

**Problem:** The arrangement quotes the vocal hook (27.21's quote kind); no module writes an instrumental hook of its own.

**Evidence:** Song 36's synth played "so I dance anyway" an octave up in the intro and outro, and nothing else. The writer: the figure "appears relatively simple … needs one more memorable contour or rhythmic twist." Every sung line ends on a long hold (fix 201), leaving room for an answer.

**Fix:** For the band classes, search a one- or two-bar instrumental hook (rhythm from the class's table, its own contour, chord tones on the beat, unrelated to the vocal hook) and place it in the intro, the holds after chorus lines, and the outro; gate it like a lead (164).

**Check:** The riff is unrelated to the vocal hook, sounds only where the voice holds or rests, and appears in intro, choruses and outro.

## Order of work

1. **195** (relatedness windows) first: 181 cannot be met by construction until the test reads the unit the construction builds.
2. **194** (secondary stresses): every declamation, text-setting and key-word reading stands on it.
3. **196** (the three-pitch clause in pop): it is the largest killer after 181 and is not obeyed by kept songs.
4. **199, 198, 197, 200** together: the walk's chord term, its aim on finished shares, the turn after a leap, and the ♭3/♭7 rule are one change to 182's walk.
5. **201** (line span from syllables, the sixteenth readings).
6. **202, 203** (the intake's summit question; 192's scope): wording.

## Regression line

After these fixes, song 36 rerun at N 500, seed 20261146, PYTHONHASHSEED 0 must still: reproduce its frozen order twice; keep the pitch median inside 2.76–3.31 (the run's was 2.84); keep the 8-bar stock share at or above 39% (the pick's 56%) and every chorus a period at 16 bars; keep 0 deaths at the bands, the summit and the leap limits; pass 38 of 38 consistency checks. Control A (181 and 182 off) must still read the back-test (median 2.45 bits, 36% repeats), so the comparison stands.

## Report 1: the test results the brief asked for

**The search.** N 500, seed 20261146, PYTHONHASHSEED 0, code d12a92b06320, Python 3.13.18, numpy 2.5.3, tables 561355b1110d1d8e…. 155 survivors (31.0%); reproduced exactly on a second run, frozen order ea5efd07813a. Pick 862839a1b813 (#1), no hand edits; composite 0.854 on the pop calibration (IC 0.67, CMP 0.67, memory horizon 0.67, realness 0.69, fit 0.75). Plans: verse ABAB, chorus A B A C A' B' A' C', bridge ABAC.

### 181: phrase design at 8 and 16 bars

Related: onsets Jaccard ≥ 0.6 and contour correlation ≥ 0.6. Units are bar windows (two bars at 8, four at 16). Each cell gives the label, then unit 2 against unit 1 and unit 3 against unit 1 (Jaccard, correlation).

| Span | Pick | u2 vs u1 | u3 vs u1 | Control's first pick |
|---|---|---|---|---|
| Verse 1 bars 1-8 (8) | period | 0.29, -0.67 | 0.86, 0.92 | period |
| Chorus 1 bars 1-8 (8) | period | 0.00, -0.14 | 0.60, 0.71 | contrasting |
| Chorus 1 bars 9-16 (8) | contrasting | 0.00, -0.14 | 0.67, 0.60 | contrasting |
| Verse 2 bars 1-8 (8) | period | 0.33, -0.47 | 0.87, 0.90 | period |
| Chorus 2 bars 1-8 (8) | period | 0.00, -0.14 | 0.60, 0.71 | contrasting |
| Chorus 2 bars 9-16 (8) | contrasting | 0.00, -0.14 | 0.67, 0.60 | contrasting |
| Bridge bars 1-8 (8) | period | 0.30, 0.41 | 0.88, 0.93 | contrasting |
| Last Chorus bars 1-8 (8) | contrasting | 0.00, -0.14 | 0.50, 0.65 | contrasting |
| Last Chorus bars 9-16 (8) | contrasting | 0.00, -0.14 | 0.55, 0.60 | contrasting |
| Chorus 1 (16) | period, unit 4 returns to unit 2 | 0.36, 0.38 | 1.00, 1.00 | contrasting |
| Chorus 2 (16) | period, unit 4 returns to unit 2 | 0.36, 0.38 | 1.00, 1.00 | contrasting |
| Last Chorus (16) | period | 0.33, 0.30 | 1.00, 1.00 | contrasting |

Pre-choruses are four bars and have no 8-bar reading.

- **Stock share at 8 bars:** pick 56% (5 of 9 spans), against chart pop 39% and the back-test 9%; control's first pick 22%. Across complete builds (5th – median – 95th): main 11% – 33% – 89%; control 0% – 0% – 33%.
- **At 16 bars:** pick 100% (three periods); control 0%.
- **The pick's named returns:** Verse 1 line 3 → line 1 (2 bars) related (0.86, 0.92); Verse 1 line 4 → line 2 (2 bars) related (1.00, 0.89); Chorus 1 line 3 → line 1 (2 bars) related (0.60, 0.71); Chorus 1 line 5 → line 1 (4 bars) related (1.00, 1.00); Chorus 1 line 7 → line 3 (4 bars) related (0.95, 0.95); Bridge line 3 → line 1 (2 bars) related (0.88, 0.93); Last Chorus line 8 → line 1 (2 bars) not related (0.55, 0.40). The last is the hook's third statement (180), not a 181 return, and not gated.

### 182: pitch surprise and intervals

- **The pick:** 3.08 bits a note, against the chart band 2.39–3.97 (median 2.96, p25 2.76); back-test median 2.53. Not flagged. 11 of the 40 top survivors were flagged under p25.
- **Spread across builds (5th – median – 95th):** main 2.67 – 2.84 – 3.01; control 2.37 – 2.45 – 2.53.

| Moves | Pick | Main median | Control's first pick | Control median | Chart pop |
|---|---|---|---|---|---|
| repeated notes | 17.0% | 23.7% | 36.0% | 35.9% | 27.6% |
| steps | 49.7% | 47.3% | 41.4% | 44.9% | 42.6% |
| leaps past a fifth | 4.7% | 1.3% | 0.0% | 0.0% | 3.0% |

### Exact bar repetition

Pick 51% of sung bars (chart pop median 38%; back-test 20%); control's first pick 48%. Main run 47% – 54% – 59%; control 43% – 46% – 50%. The pick's other kinds: transposed 3%, reshaped 3%, rhythm only 3%, new 40%. Chorus 2 is chorus 1 whole (16 exact bars of 72). Under 157 this reading gates nothing.

### The control: 181 and 182 off

Same seed and N. Returns by the old grammar (same rhythm, new pitches); the walk before 182 (proximity sd 2, leaps to a fifth, the old chord weights); no p25 flag; the band gate kept. 133 survivors, order fedc015927e6. First pick 4248c817537c: composite 0.858; pitch 2.49 bits (flagged); repeats 36.0%, steps 41.4%, past a fifth 0.0%; exact bars 48%; stock 22% at 8 bars, 0% at 16. The control reproduces the back-test: median build 2.45 bits (2.53), 36% repeats (33%), 0.0% past a fifth (1%).

## Report 2: deaths per gate, with the controls for gates met by construction (184)

Died: the first gate a build failed, in the order the gates run. Would fail: every gate read on every complete build. Control A: 181 and 182 off. Control B: the constructions off (summit placement, ceilings and floors, the monotony run ban, the leap limits, 181's returns), 182's walk kept.

| Gate | Died | Would fail | Control A would fail | Control B would fail | Met by construction |
|---|---|---|---|---|---|
| pitch band (153/182) | 0 | 0 | 54 | 0 | the walk (185) |
| rhythm band (163) | 0 | 0 | 0 | 0 | — |
| pushed notes (159) | 0 | 0 | 0 | 0 | — |
| density (159) | 0 | 0 | 0 | 0 | — |
| sequence legs (148) | 0 | 0 | 0 | 0 | — |
| key word on a chord tone (134) | 42 | 94 | 0 | 64 | — |
| register (133) | 0 | 1 | 0 | 72 | caps |
| summit once (165) | 0 | 0 | 0 | 462 | summit |
| monotony (166) | 121 | 124 | 319 | 439 | monotony |
| leaps: tritone or past an octave | 15 | 15 | 3 | 343 | leaps |
| returns related (181) | 143 | 204 | 500 | 491 | returns |
| chords completable (192) | 0 | 0 | 0 | 0 | — |

- Table B in the main run: surprisal 13, cmp 4, spectral 6, realness 1. Survivors: main 155, control A 133, control B 1.
- The bands (pitch, rhythm, pushed, density) killed nothing in the main walk, as 185 says; the pitch band's control is control A, with 54 builds below the floor.
- With the constructions off, 462 builds sound D5 other than once, 343 leap a tritone or past an octave, 439 break the monotony floor, 72 put a chorus under its verse, 491 leave a named return unrelated.
- Two constructions do not fully hold: the monotony floor still kills 121 (fix 196) and 181 still fails 204 builds (fix 195).

## Report 3: which fixes ran, and what the tables did not carry

| Fix | Ran? | How, or why not |
|---|---|---|
| 181 | yes | construction, gate and reading (Report 1) |
| 182 | yes | the walk from Table CG; p25 flag; p05 gate |
| 178 | yes | phrase-design reading at 8 and 16 bars |
| 179 | yes | the chorus's 16-bar default a period |
| 180 | yes | rhymed ends in every chorus; the idea stated three times in the last |
| 184 | yes | controls A and B (Report 2) |
| 191 | yes, acted on nothing | no word in this lyric has two primary stresses and is not a compound (194 is the related case) |
| 192 | as a check | band triads over a root bass; nothing to complete (203) |
| 193 | yes | contrary perfects printed: 8.6% of bass moves |
| 183 | yes | the root bass read against billboard_implied_bass |
| 133, 134, 148, 153, 159, 160, 163, 165, 166 | yes | gates for pop |
| 157 | yes | no rhythm floor; the repetition reading printed |
| 135 | yes | outer-voice reading |
| 136 | no gate | pop has none |
| 137, 138 | not applicable | joint tune-and-bass draw and cadence strengths belong to the hymn and concert classes |
| 149–152, 158, 161, 162 | yes | readings; 152 through 182; the line's rhythm drawn from the pop 4/4 table |
| 173–177 | yes | the chord plan from the section jobs; the harmony and section readings |
| 185–190 | not applicable | hymn and concert amendments |
| 155 | no | not in the brief; no pop originality quintiles on file |

**What the tables file did not carry:**

- A contrary-perfect figure in billboard_implied_bass, so 193's reading has nothing to stand against.
- The unit definition behind 27.31's corpus figures (bar windows or phrase spans), which 195 turns on.
- A chord-tone share in harmony_by_class split by beat for the Billboard corpus (Hooktheory has it), which 199 needs.
- Pop originality quintiles for 155.
- The tables' caution was kept: where a band in the file and the paper differ at an edge, the paper's band was used. No reading fell at an edge.

## Blind-pick tally

| Slot | Picks |
|---|---|
| Annotated top | 9 |
| Remembered top | 7 |
| Middle | 7 |
| Refrain | 1 |
| Songs picked | 24 |

Song 36: the Middle slot (top quartile under both regimes), "by the green of a clock stuck on twelve." It ends the Annotated top's run of three (songs 33–35).
