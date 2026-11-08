---
title: "The Word Without a Word — Test report (ZenEng v64 + v65 fixes)"
author: "For the engine's maintainers; not for musicians"
date: "7 November 2026"
---

# The Word Without a Word — test report (ZenEng v64, v65 fixes as ports)

This is the engine's record of song 29, kept apart from the songbook (musicians only). The test: a concert carol for one trained high voice, piano, cello and strings, in 3/4 with a tempo change and a key lift, built to a single climactic note.

## The intake

| Question | His answer |
|---|---|
| Source | His brief: "the best Christmas song ever", exceedingly memorable words on the Incarnation, perfectly paired with the music, a soloist's tour de force, never saccharine or cliché |
| Which part of the Incarnation | A: the Word that can't say a word (Andrewes 1618, *Verbum infans*) |
| What kind of song | A: a concert carol (piano and strings, a trained voice, one great climb) |
| Voice | A: high voice, written for soprano C4–A5 with one B♭5; a tenor an octave lower (a concert row 11.2 lacks; finding 63) |
| Tempo and feel | A: 3/4 at ♩ = 66, the end broadened to ♩ = 56 |
| Form | B: 80 bars, about 3:45, with an interlude, a bridge and a broadened last refrain (the longest line printed per option, fix 56) |
| Key | A: D♭, lifting a whole step to E♭ at verse 4 |
| Title | A: "The Word Without a Word". His additions: a lyric draft before the music, and a full score |

- **Never-say:** the run's default list of carol clichés (silent, holy night, precious, lowly, manger, angels, sweet, little baby, born to die and others), shown with draft 1; nothing sung from it.

## The writing room

Three drafts. The writer locked draft 3.

| Round | What changed | Why |
|---|---|---|
| Draft 1 | The run's lyric: Genesis 1, Sinai, John 8, Hebrews 1:1–2; the refrain "O Word without a word, the Speech that cannot speak" | — |
| Draft 2 | Verse 2 bodily (bread softened on his tongue, rain in a cupped hand, held up to the stars); verse 3's milk and spit and "ma"; the interlude given a job (her lullaby on the cello); verse 4 starts in the cry; plainer diction ("sleeping on her chest", "what God meant to say"); the bridge's first word "Abba", and Joseph turns | His five notes |
| Draft 3 | "he reaches up past both of them" (the explanation gone); "is milk and spit and half a sound"; "hoarse against her ear"; the last line left open ("goes in, and out, and in"); "ma" and "Abba" marked as anchors | His five further notes |

**Fix 56 in force.** The form question printed the longest line each option could hold (11 syllables in two bars at ♩ = 66, 13 at ♩ = 56); every drafted line was 6–9 syllables, and no locked line died on span.

**Stress ports.** "with NOT a single word", "at ALL" (line-final), "past BOTH of them", "NOW: Abba", and "it's"/"she'll" as function words before a verb (finding 64).

## The quotable line (10.20)

- **Remembered:** "The Word without a word" leads (+12.59; the title, sung three times).
- **Annotated:** "The voice that said, Let there be light," leads (+3.27), and is the only line in the top quarter of both.
- **The middle slot:** "the breath that made the world", by the most-repeated hook line rule (the both-lists line already fills the Annotated slot).
- **The writer's blind pick (8 Nov):** B, "The Word without a word": the Remembered top (the title, the most-repeated hook line).

## The melody

**The designed notes first.**

- **The refrain:** the title's last WORD on E♭5 over A♭ (aimed); WORLD on line 3's second downbeat; RESTS on A♭4 over A♭ (aimed), a half cadence. Refrain 2 copies refrain 1.
- **MA (verse 3):** held at least a half note (the walk's condition), on a beat; the arrangement moves nothing under it.
- **The bridge's last line (designed):** NOW on C5 | AB-ba on A♭4 falling to F4, the falling third of a child's call, the band silent | and JO-seph TURNS rising to D5 over B♭, the pivot into E♭.
- **The last refrain (designed):** lines 1–2 refit from refrain 1 a step up (song 28's refit, finding 59); line 3 climbs E♭5–F5–G5–A♭5 to WORLD on B♭5 over E♭, the only B♭5; line 4 falls to the last IN on B♭4 over B♭, open.

**The search.**

- **Volume:** 500 built from 755 attempts; 406 survived (81.2%).
- **Deaths:** join verse 2 > verse 2 85; join verse 1 > verse 1 77; CMP 56; spectral 20; verse 3 20; join verse 3 > verse 3 19; verse 4 16; realness 15; join verse 1 > refrain 1 15; the refrain 11; join verse 2 > refrain 2 8; memory 2; the bridge into NOW 2; verse 1 1; tritone 1; bridge 1.
- **A floor added after the run:** verse 4 must climb to E♭5. The ranking's #1 and #2 kept verse 4 at C5 and D5, below the refrains, against the design (a verse 4 that climbs into the last refrain). Applied to the frozen ranking, #3 is the first that passes (finding 65).
- **Pick:** f10477ea1784 (#3). Composite 0.906, realness 0.59, IC 0.96, CMP 0.50, M 0.61, fit 1.00, lift +7, strong-beat alignment 0.95, longest breath 5.91 s.
- **Plans:** refrain ABAD (drawn ABAA; the last line takes its own letter for its aimed note); verses ABCD, ABAC, AABC, ABCD; the bridge AAB plus the designed line.
- **No hand edits.**

**Ranges:** verses D♭4–B♭4; refrains F4–E♭5; the bridge E♭4–D5; verse 4 F4–E♭5; the last refrain G4–B♭5.

## The arrangement and the demo

- **Ensemble:** piano (the cradle figure: the left hand root, fifth, tenth, octave, tenth, fifth in eighths; a right-hand chord from refrain 1), cello (the root from verse 2; the interlude's lullaby, refrain 1's tune an octave below the voice), strings (pads in the refrains, the interlude's swell, building through the bridge, full in verse 4 and the last refrain).
- **The anchors:** no accompaniment onset under MA; the whole ensemble silent for the bar of ABBA; everyone back on B♭ for "and Joseph turns".
- **Guide voice:** flute, at the soprano's pitch.
- **Stems:** the voice sits 4.4 dB over the ensemble (rule: at least +3), at vocal gain 2, ensemble CC7 104.
- **Energy (9.12), per four beats:**

  | Section | Read |
  |---|---|
  | Intro | 0.25 |
  | Verse 1 | 0.13 |
  | Refrain 1 | 0.48 |
  | Verse 2 | 0.46 |
  | Refrain 2 | 0.68 |
  | Interlude | 0.63 |
  | Verse 3 | 0.46 |
  | Bridge | 0.64 |
  | Verse 4 | 0.75 |
  | Refrain 3 | 0.84 |
  | Coda | 0.06 |

  Each refrain reads above its verse; the last refrain is the top. Its last quarter falls to 0.64 because the last line thins by design: 9.12 reads the arrival, not the ending, which is right here.

## Documents

- **Lead sheet (3 pages):** the voice with the lyric and chord names; 3/4; D♭ to E♭; the tempo change; the anchors marked. LilyPond's MIDI read back: 231 notes; matches.
- **Full score (4 pages):** voice, piano (grand staff), cello, strings. Read back: voice 231, piano right hand 191, left hand 374, cello 62, strings 129; all match.
- **Nashville chart (1 page):** D♭ numbers, then E♭; the anchors as cues.
- **Songbook and production notes:** one document, as a Doc and Word, with the producer one-sheet on its own page (added after delivery at the writer's request).
- **Consistency check:** 30 of 30, with new checks for the tempo change, the key lift on "and Joseph turns", the one B♭5 on "world", the title's E♭5 and RESTS's half cadence, the open last note, MA (nothing moves) and ABBA (the ensemble silent), and the cello's lullaby.

## Findings

63. **11.2 has no concert row.** The voice table's rows are pop ranges; a trained soprano (C4–A5, one B♭5) or tenor (C3–A4, one B♭4), and the convention that one part serves both an octave apart, aren't there. **Proposed fix 63:** add concert rows (soprano, mezzo, tenor, baritone) with the "high voice / low voice" octave convention, and print both ranges on the lead sheet.
64. **Five more stress readings.** "with NOT a single word" (negation before "a"), a line-final "ALL", the pronoun "BOTH", a clause-initial "NOW" before a colon, and "it's"/"she'll" as function words before a verb. **The run's port:** a song-29 pass in the stress rules. **Proposed fix 64:** fold these into v58's rules with fixes 7, 19, 24, 39, 46 and 57, read through fix 45's single stress function.
65. **Nothing checks that a lifted verse climbs.** The key lift and the design asked verse 4 to rise toward the last refrain; the ranking's top two left it lower than the refrains. **The run's port:** a floor (verse 4 reaches E♭5), applied after the run to the frozen ranking. **Proposed fix 65:** a "climb" field per section (the least top note it must reach), set by the form's design and checked in evaluation, so the arc of a tour de force is part of the search, not a post-hoc filter.
66. **Joins are the biggest waste.** 204 of 349 builds that failed died on joins inside a verse. A re-walked new letter ignored the next line's pickup until the run fixed it; fitted cells still collide when a later line is re-walked. **Proposed fix 66:** build a section's rhythms from the last line back (as fix 59's refit does), so every line knows the next one's pickup before it is placed.
67. **Anchors have no field.** "Ma" and "Abba" are words the writer asked the arranger to protect: a held note with nothing moving under it, and a bar of total silence. **The run's port:** a walk condition for MA's length; the arrangement drops every onset under MA and silences the ABBA bar; the lead sheet and score mark both. **Proposed fix 67:** an "anchor" field on a syllable (hold, and what the ensemble does: hold, or stop), read by the walk, the arrangement, the engraving and consistency. This joins fix 52's stop.
68. **The modulation can be a word.** "And Joseph turns" carries the pivot chord and the leading tone of the new key. **The run's port:** the line designed note for note. **Proposed fix 68:** let a key change be anchored to a named syllable (the pivot falls under it), checked like an aimed note.
69. **No page for the producer.** The songbook carries everything a producer needs, but spread across the production brief and the session notes. The writer asked for a producer one-sheet (song 29, after delivery). **The run's port:** one printed page in the songbook, between the lyric sheet and the production brief: the emotional target, references, dynamic arc, non-negotiables and mix priorities; consistency checks it is there. **Proposed fix 69:** add the one-sheet to fix 36's production notes as a standard part of every songbook, checked to fit one page.
70. **v65 fixes used as ports:** 9 and 24 (stress), 13, 31 and 56 (form lengths and the longest line), 25 (voice options), 26 (ASCII track names), 29 (line-final stress on a beat), 30 (aimed notes exempt), 32 (fitted cells clear the pickup), 33 (MIDI tempo in quarters), 34 (spelling from the key), 36 (production notes in the songbook; the full score on request), 47 (breath scaled: 7.0 s at the broadened tempo), 48 (9.12 per four beats), 59 (refit).

## Blind-pick record

Song 29: the Remembered top (the title line). Through song 29 (with song 30 already counted), over 18 picked songs: Annotated top 6, Remembered top 6, middle 5, refrain 1.
