---
title: "Dance Anyway — Test report (ZenEng v91)"
author: "Words and music: Jason Bryant"
date: "10 November 2026"
---

# Dance Anyway — test report (ZenEng v91)

This is the engine's record of song 36. It is kept apart from the songbook, which is for musicians only.

**The brief, in the writer's words (abridged):**
- ZenEng_v91.docx is the single source of the rules; its version row is v125 and it ends at fix 193 (song 35's 178–187 are in it as 184–193).
- Read the tables (zeneng_v88_tables.json, zeneng_v91_hymn_supplement.json), don't refit; where a band and the paper differ at an edge, the paper decides.
- Port before the search, in this order: 181, 182, 178–180, 184, 191–193 (and 183).
- Write a pop, rock or country song; show the full lyric before any music.
- Report, for 181, every section's phrase-design label at 8 and 16 bars and the stock share; for 182, the pick's pitch surprise and the spread across builds, and its share of repeated notes, steps and leaps past a fifth; exact bar repetition; a control with 181 and 182 off (same seed and N) and the same readings on its first pick; deaths per gate, and for each gate met by construction its control failures (184); which fixes ran, which could not, and why.
- Number new findings from 194, after checking the version row.

The version row was checked: v125, last fix 193. Tables: zeneng_v88_tables.json (sha256 561355b1…68255) and the hymn supplement (sha256 e74e7c30…), read and not refitted; the supplement holds nothing for pop.

## Intake

- **Nine questions, one per turn,** each with three pictures, plus four lyric drafts.
- **Class:** pop. **Moment:** a kitchen dance at 2 a.m. (the writer: "Dancing for the sheer joy of life seems like a good pop subject"). **Who:** her, alone. **Turn:** anyway — the bill stays unpaid, the clock stays wrong, she dances; joy chosen, not caused (the writer: "Joy of the face of everyday life! Songs almost counter cultural").
- **Title:** "Dance Anyway." **Voice:** female mezzo, written B♭3–D5. **Feel:** 4/4, ♩ = 118, E♭ major, four-on-the-floor disco-pop.
- **Form (fix 139, summed and timed):** Intro 4 · Verse 8 · Pre 4 · Chorus 16 · Verse 8 · Pre 4 · Chorus 16 · Bridge 8 · Last Chorus 16 · Outro 4 = 88 bars, 2:59. **Never-say:** dance-pop clichés (on the dance floor, lose control, dance like nobody's watching …) and four self-help words.
- **The lyric:** four drafts. The writer's notes made one object the signature (the microwave clock blinking twelve since a July power cut), turned the pre-chorus into the last breath before the decision, made the bridge show what waiting cost (the July night on the floor), made the bill heavier, protected the socks line, and cut the dish towel. Draft 4 locked: "A".

## The search

**The construction (ports in the order given).**
- Every lyric line is a two-bar unit; chords are one a bar, written by the section jobs of 177 (verse home on I; pre-chorus opens on IV and ends on V; chorus opens on I and brings ♭VII; bridge opens on IV, has no tonic, adds ii and ends on V). The bass is the chord roots.
- **181:** the form's returns are built, not hoped for. Letter plans are drawn per section: verse ABAC/AABC/ABAB, bridge AABC/ABAC, the chorus a 16-bar period with rhymed ends (its second half sings the first again, unit 4 returning to unit 2 with its ending changed) and an 8-bar head of ABCD or ABAC. A returning line takes its first unit's rhythm and pitches, at the same level or a diatonic step or two away; where its words have more syllables, up to three unstressed leading syllables go before the unit as a pickup and the longest events are split; where fewer, a syllable takes two notes. Its ending may change. A form may name a return only between lines whose syllable counts differ by three or fewer (the engine's rule; finding 195). Every named return is checked with 27.31's test after the build; a return the ending's change has broken gets its first unit's pitches back; a build whose return still fails dies.
- **182:** each move is drawn from Table CG's pop shares (repeat 27.6%, step 42.6%, third 18.5%, fourth/fifth 8.4%, past a fifth 3.0%; descending 53%), then the pitch by the class's range and key terms (R 5, the major profile). ♭3 and ♭7 are sung only where no chord tone lies a semitone away (finding 200). After a leap past a fifth the next move turns back by a step or third (finding 197). Under the class's 25th percentile (2.76) a card is flagged and nothing ranks by it; under the 5th (2.39) the build dies.
- **178–180:** the phrase-design reading at 8 and 16 bars; the chorus's 16-bar default a period (179 gives pop sentence 15%, period 11%); rhymed ends (180); the last chorus states its idea a third time (its last line sings the hook, 'so I dance anyway' on the hook's notes, 'I'm still here' sung before it).
- **Rhythm:** each fresh line's onsets are drawn over the pop 4/4 rhythm table (RT[position][distance]) with stresses pulled to strong places, a weak monosyllable not held (150), the last stress aimed at a strong beat, the line done by beat 3 of its second bar so the next line has a half-beat breath (v43). Melisma: a third of line ends and a tenth of long inner notes take a second note (150).
- **Constructions (184):** the summit D5 placed on 'for-EV-er' with every other note at C5 or below (165); section ceilings (verse B♭4, the rest C5) and floors (chorus from D4) by plan (133); the monotony floor's run ban in the walk (166); no tritone and nothing past an octave in the walk; the returns of 181.
- **Gates:** pitch band 2.39–3.97 (153/182); rhythm band 1.33–3.57 (163); pushed notes ≤ 42% and density 1.1–4.9 notes a second (159); sequence legs ≤ 2 (148); key word on a chord tone ≥ 40% of lines (134); each chorus's top not below its verse's (133); the summit once (165); the monotony floor (166: no pitch more than three times running, three pitches a line); no tritone, no leap past an octave; returns related (181); chords completable (192). Then Table B on the pop calibration (spectral, CMP, memory horizon, IC, realness, read on verse 1 and chorus 1 in E♭). Table C ranks the survivors (118).

**The run.**
- N 500, seed 20261146, PYTHONHASHSEED 0, code d12a92b06320, Python 3.13.18, numpy 2.5.3, tables 561355b1110d1d8e… (fix 145's record).
- **Survivors:** 155 of 500 (31.0%). **Reproduced exactly** on a second run: the same survivors and the same frozen order, ea5efd07813a.
- **The pick:** 862839a1b813 (#1), no hand edits. Composite 0.854: IC 0.67, CMP 0.67, memory horizon 0.67, realness 0.69, fit 0.75 (the chorus's median 5 semitones over the verse's). Plans: verse ABAB, chorus A B A C A' B' A' C', bridge ABAC. Range B♭3–D5.
- **Survivors flagged under p25 (2.76):** 11 of the 40 kept for ranking; the pick is not flagged.

**A session miss.** The by-hand inspection script first printed the second-ranked candidate (it read its argument after overwriting it). The first round of inspection — and the rule for ♭3 and ♭7 that came from it — was made on that candidate; the true #1 was then inspected, which is how the three leaps in one bridge line were found (finding 197). Every rule change was followed by a full rerun of all three searches.

## What the brief asked for

### 181: phrase design at 8 and 16 bars

Two units are related when their onsets overlap (Jaccard ≥ 0.6) and their contours correlate ≥ 0.6. Units are bar windows: two bars at the 8-bar scale, four at the 16. The table gives each span's label with unit 2 against unit 1 and unit 3 against unit 1 (Jaccard, correlation).

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

Pre-choruses are four bars and have no 8-bar reading; no other section runs 16 bars.

- **Stock design at 8 bars:** the pick 56% of spans (5 of 9), against chart pop's 39% and the back-test's 9%. The control's first pick: 22%. Across the main run's complete builds: 11% – 33% – 89% (5th – median – 95th); the control's: 0% – 0% – 33%.
- **At 16 bars:** the pick 100% (all three choruses read as periods); the control 0%.
- **The returns the form named,** each read by the same test: Verse 1 line 3 → line 1 (2 bars): related (0.86, 0.92); Verse 1 line 4 → line 2 (2 bars): related (1.00, 0.89); Chorus 1 line 3 → line 1 (2 bars): related (0.60, 0.71); Chorus 1 line 5 → line 1 (4 bars): related (1.00, 1.00); Chorus 1 line 7 → line 3 (4 bars): related (0.95, 0.95); Bridge line 3 → line 1 (2 bars): related (0.88, 0.93); Last Chorus line 8 → line 1 (2 bars): not related (0.55, 0.40). The last is the third statement of the hook (180), which is not a 181 return and is not gated.
- **Where 181's construction failed** (named returns not related, all 500 builds): Bridge line 3 -> line 1 (2 bars): 94; Chorus 1 line 3 -> line 1 (2 bars): 85; Verse 1 line 3 -> line 1 (2 bars): 28; Chorus 1 line 7 -> line 3 (4 bars): 24; Verse 1 line 4 -> line 2 (2 bars): 17. With the construction off (the old grammar: same rhythm, new pitches) every build fails at least one: Chorus 1 line 7 -> line 3 (4 bars): 473; Chorus 1 line 5 -> line 1 (4 bars): 447; Verse 1 line 3 -> line 1 (2 bars): 446; Bridge line 3 -> line 1 (2 bars): 441; Chorus 1 line 3 -> line 1 (2 bars): 241; Verse 1 line 4 -> line 2 (2 bars): 214.

### 182: pitch surprise and intervals

- **The pick:** 3.08 bits a note, against the chart band 2.39–3.97 (median 2.96, p25 2.76); the back-test median was 2.53.
- **Spread across builds (5th – median – 95th):** main 2.67 – 2.84 – 3.01; control 2.37 – 2.45 – 2.53.

| Moves | Pick | Main run (median) | Control's first pick | Control run (median) | Chart pop |
|---|---|---|---|---|---|
| repeated notes | 17.0% | 23.7% | 36.0% | 35.9% | 27.6% |
| steps | 49.7% | 47.3% | 41.4% | 44.9% | 42.6% |
| thirds | 16.8% | — | 17.4% | — | 18.5% |
| fourths and fifths | 11.8% | — | 5.2% | — | 8.4% |
| leaps past a fifth | 4.7% | 1.3% | 0.0% | 0.0% | 3.0% |
| descending share of moves | 56.8% | — | 47.3% | — | 52.7% |

The walk draws Table CG's shares; what survives is not those shares (finding 198).

### Exact bar repetition

- The pick: 51% of sung bars repeat an earlier bar exactly (rhythm and pitches), against chart pop's median 38% and the back-test's 20%. The control's first pick: 48%. Main run 47% – 54% – 59%; control 43% – 46% – 50%.
- The pick's other kinds: transposed 3%, reshaped 3%, rhythm only 3%, new 40%; a bar's rhythm heard before in 60% of bars; 29 distinct bar rhythms in 72 sung bars. Chorus 2 is chorus 1 whole, which alone makes 16 exact bars. Under 157 this reading gates nothing.

### The control: 181 and 182 off

Same seed and N; the returns built by the old grammar (same rhythm, new pitches); the walk before 182 (proximity sd 2 round the last note, leaps to a fifth, the old chord weights); no p25 flag; the band gate (153) kept. 133 survivors, order fedc015927e6. Its first pick, 4248c817537c: composite 0.858, pitch 2.49 bits (flagged under p25), repeats 36.0%, steps 41.4%, leaps past a fifth 0.0%, exact bars 48%, stock design 22% at 8 bars and 0% at 16. The control reproduces the back-test: its median build reads 2.45 bits (back-test 2.53), 36% repeats (back-test 33%) and 0.0% leaps past a fifth (back-test 1%).

### Deaths per gate, and the controls for gates met by construction (184)

Deaths count the first gate a build failed, in the order the gates run. 'Would fail' reads every gate on every complete build. Control A is 181 and 182 off; control B switches off the constructions (summit placement, ceilings and floors, the monotony run ban, the leap limits, 181's returns) and keeps 182's walk.

| Gate | Main: died | Main: would fail | Control A: would fail | Control B: would fail | Met by construction |
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

Table B deaths in the main run: surprisal (Table B) 13, cmp (Table B) 4, spectral (Table B) 6, realness (Table B) 1. Control A: 133 survivors; control B: 1 (with the constructions off, almost nothing lives).

- **The bands never bit the main walk** (pitch, rhythm, pushed, density: 0 of 500), as 185 says a class walk cannot leave its class's band. The pitch band's control is the walk before 182: 54 builds below the floor.
- **The constructions' bite:** with them off, 462 builds sound D5 other than once, 343 leap a tritone or past an octave, 439 break the monotony floor, 72 put a chorus under its verse, 491 leave a named return unrelated.
- **The monotony floor still kills 121 builds with its run ban on,** because its second clause (three pitches in every line) is not built in and the copies and returns can break the first. Finding 196.

### Which fixes ran

| Fix | Ran? | How, or why not |
|---|---|---|
| 181 | yes | construction, gate and reading (above) |
| 182 | yes | the walk from Table CG; p25 flag; p05 gate |
| 178 | yes | the phrase-design reading at 8 and 16 bars |
| 179 | yes | the chorus's 16-bar default a period |
| 180 | yes | rhymed ends in every chorus; the idea stated three times in the last |
| 184 | yes | two controls (A and B); the table above |
| 191 | yes | in the stress reading; this lyric has no word with two primary stresses that is not a compound, so it acted on nothing (finding 194 is the related case) |
| 192 | as a check | the band writes whole triads over a root bass; nothing to complete (finding 203) |
| 193 | yes | contrary perfects printed: 8.6% of the pick's bass moves |
| 183 | yes | a bass of chord roots, read against billboard_implied_bass |
| 133, 134, 148, 153, 157, 159, 160, 163, 165, 166 | yes | as gates or readings for pop; 157: no rhythm floor |
| 135 | yes | outer-voice reading |
| 136 | no gate | pop has none; reading only |
| 137, 138 | no | the joint tune-and-bass draw and cadence strengths are the hymn and concert classes' |
| 149–151 | yes | text-setting reading; the walk's durations hold the word's last syllable; melisma aimed at 16% |
| 152 | yes | through 182 |
| 158, 161, 162 | yes | readings; the line's rhythm drawn from the 4/4 table, its schema printed |
| 173–177 | yes | the chord plan from the section jobs; harmony and section readings |
| 185–190 | not applicable | hymn and concert class amendments (bands' scope, 3/4 figures, hymn declamation, hymn harmony, text-setting for the concert classes, the hymn originality flag) |
| 155 | no | not in the brief; the tables file has no pop originality quintiles |

### The other readings

**Text setting (149–151), the pick against chart pop's medians:**
- word-initial syllables on the downbeat 33% (22%); later syllables 5% (4%)
- initial over later syllable length 0.43 (0.84)
- melisma 4.1% of syllables (16.4%), 13% of them at phrase ends (30%)
- final note over the phrase's median 6.5 (2.0); phrases starting off the downbeat 95% (88%)
- the summit: D5 on the stressed syllable of 'forever', bar 82, beat 2.00, 2.0 times the median note (1.5), 97% of the way through (chart pop's peak sits at 31%; finding 202)

**Rhythm (158), against pop (Hooktheory medians):**
- onsets on the downbeat 11.7% (13.9%), other beats 26.9% (33.3%), the eighth off the beat 37.6% (37.5%), sixteenths 23.8% (4.5%)
- gaps of a sixteenth 37.6% (2%), an eighth 53.4% (43.1%), a quarter 5.5% (15.5%); nPVI 31.1 (45.4)
- pushed notes 8.6% (12.5%; gate 42%); 5.32 onsets a bar (4.71); 2.35 notes a second (2.42; band 1.1–4.9); rhythm 2.35 bits (band 1.33–3.57) — finding 201

**Declamation (161):** the last stress on beat 1 or 3 in 65% of lines, on the downbeat in 22%; 95% start before the downbeat; spans: 2 bars 33, 3 bars 7. Commonest schemas: '1 2 3' ×4; '4.5 | 1 2' ×3; '1 2 2.25 3' ×3; '1.5 4 | 1 1.5 3' ×3; '3.75 4.5 | 1 2' ×3.

**Harmony (173):** six chords (I, ii, vi, IV, V, ♭VII), all root position, no sevenths; before the tonic: IV 15, V 3, bVII 3 (pop: V and IV about equal, ♭VII 13%); root motion: down a fourth / up a fifth 40%, by step 28%, by third 21%, up a fourth / down a fifth 11%; 0.92 chords a bar; tonic 30% of the time (chart median 43%).

**Sections (176):**

| Section | First | Last | Tonic time | New chords | Join |
|---|---|---|---|---|---|
| Intro | I | IV | 25% | I, V, vi, IV | — |
| Verse 1 | I | V | 50% | — | IV → I |
| Pre 1 | IV | V | 0% | — | V → IV |
| Chorus 1 | I | I | 31% | bVII | V → I |
| Verse 2 | I | V | 50% | — | I → I |
| Pre 2 | IV | V | 0% | — | V → IV |
| Chorus 2 | I | I | 31% | — | V → I |
| Bridge | IV | V | 0% | ii | I → IV |
| Last Chorus | I | I | 31% | — | V → I |
| Outro | I | I | 50% | — | I → I |

**Outer voices (135, 183, 193), the melody against the chord roots, with billboard_implied_bass medians and 5th–95th:**
- imperfect: 39.0% (28.1%; 9%–55%)
- perfect: 27.1% (46.4%; 22%–76%)
- fourth: 3.4% (3.3%; 0%–23%)
- dissonance: 30.5% (15.5%; 0%–40%)
- oblique: 22.4% (14.9%; 0%–37%)
- contrary: 27.6% (36.8%; 11%–64%)
- similar: 48.3% (30.2%; 9%–58%)
- parallel: 1.7% (11.1%; 0%–45%)
- parallel perfect: 0.0% (4.9%; 0%–42%)
- direct perfect: 12.1% (5.6%; 0%–23%)
- bass by step: 36.2% (32.1%; 0%–74%)
- bass by 4th 5th: 34.5% (48.6%; 4%–96%)
- contrary perfects (193): 8.6% of moves (no corpus figure on file); 59 bass moves

**Chord tones:** the key word on a chord tone in 50% of lines (gate 40%; chart median 73%); all notes 40% (chart melody_chord_tones median 62%); notes outside the chord resolved by step 29% (45%). Finding 199.

## The record and the documents

- **The band:** drums (four on the floor, clap and snare on 2 and 4), octave bass, electric piano stabs, muted guitar sixteenths, a pad, and a synth that plays the hook in the intro and the outro. Every part written from the record.
- **Demo:** +4.9 dB voice over band (rule ≥ +3); the energy arc: Intro 0.57, Verse 1 0.53, Pre 1 0.66, Chorus 1 0.66, Verse 2 0.45, Pre 2 0.65, Chorus 2 0.65, Bridge 0.63, Last Chorus 0.70, Outro 0.68 — each chorus above its verse, the last chorus the top.
- **Engravings:** lead sheet (3 pages) and parts (10 pages: synth, electric piano, guitar, pad, bass, drums). MIDI readback matches the record on every staff: voice 383 notes; syn 12, key 886, gtr 1611, pad 204, bas 640; drums 1704 hits of 1704.
- **Number chart** and **songbook** (Doc and Word) written from the record; consistency checks below.

## Findings (194–203)

### 194. The engine reads secondary stresses as stresses

**Problem.** The stress reading marks every syllable the dictionary gives a primary or a secondary stress. In this lyric that put two stresses on 'July' (JH UW2 L AY1), 'radio' (R EY1 D IY0 OW2), 'microwave' (AY1 … EY2), 'somewhere' (AH1 … EH2) and 'anyway' (EH1 … EY2). None of these has two primaries, so 191 does not touch them.

**Fix.** In a word of two or more syllables only the primary stress counts; a secondary stress counts only on a line's last syllable (where it carries the rhyme or the hold: 'an-y-WAY'). No list.

**Check.** Reread songs 21–36: no polysyllable outside a line's end carries two stresses; the declamation reading changes only on those words.

### 195. 181's relatedness test reads bar windows, so the next line's pickup and a held last note decide it

**Problem.** In 500 builds the engine built every named return from its first unit's rhythm and pitches, and still 204 builds failed the test somewhere (bridge line 3 → 1: 94; chorus line 3 → 1: 85). The two-bar window holds the next line's pickup, which differs between the first unit and its return; and a line that holds its last note for a third of the window is decided by that one note, so a changed ending ('its ending may change') can break the contour test. Lines whose syllable counts differ cannot keep the onsets: the engine had to add its own rule that a form names a return only between lines within three syllables of each other.

**Fix.** Read a unit from its first onset to the onset of the next unit's first note, so the next phrase's pickup is not in it; let the ending's change (the last note) be outside the contour test; and state in 181 that a form names a return only between lines whose syllable counts differ by three or fewer, the extra syllables going to a pickup.

**Check.** Rerun song 36's search: no build dies at 181 where its construction was used; the 8-bar stock share stays at or above the chart's 39%.

### 196. The monotony floor's three-pitch clause is not obeyed by kept pop, so under 132 it cannot be a universal gate

**Problem.** 166 (from v43) asks three distinct pitches in every line. In the chart corpus (gate_audit, 198 songs) the median song has 7.4% two-pitch lines and only 34% of songs have none. In this run the clause killed 121 of 500 builds with the run ban on (control A: 318).

**Fix.** For pop, rock and country, keep 'no pitch more than three times running' as the floor and make 'three pitches a line' a reading (the two-pitch share against the chart's deciles: 0, 0, 7.4%, 18.9%, 50%). The notated classes keep the clause if their corpora obey it.

**Check.** Song 36 rerun: monotony deaths fall to the run clause alone; the two-pitch share is printed.

### 197. 182's walk can draw several leaps past a fifth in a row

**Problem.** Drawing each move from Table CG independently, the first pick under the final rules (before this fix) had a bridge line of three such leaps in a row: B♭4–C4–A♭4–C4 on 'Ju-ly, I sat'. Each is a 2–3% draw; the composite ranked the build first. Kept melodies turn back after a leap.

**Fix.** After a move past a fifth the next move is a step or a third in the opposite direction. (Song 36 ran with this; it is the engine's rule and is not in the paper.)

**Check.** Leaps past a fifth followed by another leap: none in the survivors; the class's 3% share of such leaps holds within its band.

### 198. The shares the walk draws are not the shares that survive

**Problem.** The walk draws repeats 27.6%, steps 42.6% and leaps past a fifth 3.0%. The main run's builds read 23.7%, 47.3% and 1.3% at the median; the pick 17.0%, 49.7% and 4.7%. Three causes: a melisma's second note is always a step, a split event in a return is a step, and the monotony floor kills the repeat-heavy builds.

**Fix.** Read 182's shares on the finished melody, not on the draw, and aim the draw so the finished melody lands near the class's medians (draw repeats a little above 27.6%, steps a little below).

**Check.** The main run's median repeats, steps and leaps within two points of Table CG's.

### 199. 182's walk puts too few notes on chord tones

**Problem.** The pick puts 40% of its notes on tones of the bar's chord (chart median 62%; Hooktheory pop 72% on the beat), resolves 29% of the others by step (45%), and its key words sit on chord tones in 50% of lines (chart 73%; gate 40%). The key-word gate killed 42 builds. The three-term pitch model has no chord in it, and the light chord weight on stressed beats does not make up the difference.

**Fix.** Add the chord to the walk on the beat: a chord-tone term fitted to the class's chord-tone share on and off the beat (Hooktheory 72% and 62%), and print the melody's chord-tone share against harmony_by_class.

**Check.** The pick's chord-tone share inside the chart's 25th–75th percentiles; key-word deaths fall.

### 200. Table CG says pop sings ♭3 and ♭7 in major, but not over which chords

**Problem.** The class profile gives ♭3 3.7% and ♭7 3.2% of notes. Drawn without regard to the chord, the walk put G♭ over C minor (a diminished fifth over the root) and G♭ over B♭.

**Fix.** Sing ♭3 and ♭7 only where no chord tone lies a semitone away and the note is not a tritone from the root (in E♭: G♭ over A♭; D♭ over E♭ and D♭). A copied note that lands on a clash moves to the scale.

**Check.** No ♭3 or ♭7 a semitone from a chord tone in any survivor.

### 201. The two-bar line packs its syllables into sixteenths

**Problem.** The lyric's lines run 6 to 14 syllables and the form gives each two bars at ♩ = 118. The pick's gaps between notes are sixteenths 38% of the time (Hooktheory pop 2%), its onsets fall on sixteenths 24% of the time (4.5%), and each line's last note is 6.5 times its median note (2.0). Melisma is 4.1% (16.4%). The rhythm band (1.33–3.57) passes it at 2.35; no reading flags it.

**Fix.** Give a line its span from its syllable count (about 4–5 syllables a bar at this tempo, so a 13-syllable line takes three bars or the lyric is cut), and add bands for sixteenth gaps and final lengthening from rhythm_by_class and text_setting as readings.

**Check.** Song 36's sixteenth-gap share within the Hooktheory 5th–95th; final lengthening near 2.0.

### 202. A declared summit is placed without its position read

**Problem.** 165 places the summit where the design names it; 151 reads where kept songs put their peak (chart pop's median: 31% of the way in, in the chorus or bridge in 67% of songs). Song 36's D5 is 97% of the way through, in the last chorus. Nothing in the intake showed the corpus figure when the summit was chosen.

**Fix.** When the intake asks for a summit (133's design clause), show 151's position figure beside the options.

**Check.** The intake question for the summit prints the position reading.

### 203. 192 has nothing to check in a band arrangement

**Problem.** 192 asks the joint draw of tune and bass to leave two inner voices able to complete the chord. In song 36 the band plays whole triads over a root bass; the check passed on every build.

**Fix.** Scope 192 to the classes whose bass is drawn with the tune (hymn, carol, concert); in the band classes, print instead whether the tune doubles the leading note in the bass (it cannot with a root bass on V).

**Check.** The test report of a band song lists 192 as not applicable.

## Consistency

38 of 38 checks pass: the record against the frozen pick; range, summit, chorus 2 and the register clause; the demo's notes, tempo, stems and energy arc; the GarageBand file; every staff's MIDI readback; the credit lines; the chart's numbers; the songbook's 40 line rows, its references and its freedom from engine terms; and the report's figures against the readings.

## The blind pick

Offered after delivery: the three quotable-line slots, shuffled.
