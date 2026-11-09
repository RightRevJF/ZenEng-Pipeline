---
title: "I Took Him for the Gardener — Test report (ZenEng v64 + v65 fixes)"
author: "For the engine's maintainers; not for musicians"
date: "8 November 2026"
---

# I Took Him for the Gardener — test report (ZenEng v64, v65 fixes 1–94 as ports)

This is the engine's record of song 32, kept apart from the songbook (musicians only). The test: an Easter concert solo in the vein of song 29, for one trained high voice, piano, cello and strings, in 6/8, minor turning to major on one designed syllable.

## The intake

| Question | His answer |
|---|---|
| Brief | "Ready to write an Easter solo in a similar vein to The Breath that Made the World?" |
| The moment | A: the garden, Mary Magdalene takes him for the gardener until he says her name (John 20:16) |
| Who sings | A: Mary, first person; soprano and mezzo editions, no tenor (fix 92) |
| The turn | B: the gardener was right, "I took him for the gardener, and he was" |
| Title | A: "I Took Him for the Gardener" (fix 94's test: sung every refrain, on the refrain's top note; no song found by that name) |
| Harmonic arc | A: minor while she weeps; major on "Mary" |
| Metre and tempo | A: 6/8 at ♩. = 52 |
| Form | A: song 29's shape (the run grew it from 84 to 82 bars: the Name and the last refrain each gained a four-bar last line; see below) |
| Never-say | A: the Easter clichés (risen, alleluia, glory, triumph, lilies, angels, heaven, hope, sunrise, "he is risen", "rolled away" and others). "The key as always is theological and emotional depth" |

## The writing room

Four drafts. The writer locked draft 4 ("A"), declining the offered micro-adjustments ("clean" to "bare", "still in the earth", a period on the last line; draft 4 already ends on one).

| Round | What changed | Why |
|---|---|---|
| Draft 1 | The run's lyric | — |
| Draft 2 | Verse 3: the two in white frame the empty place; "someone stood among the trees" (Genesis 3:8); the Name: "give me back my dead" | His notes: "outside" vague; "I begged him for the dead" compressed; the angels report |
| Draft 3 | Verse 1: "I'd tied my hair back for the work"; verse 3 "a body's length of empty stone"; the last refrain "his hands in the earth again" | His notes, taken one at a time ("receive these notes until I tell you") |
| Draft 4 | "just give me back the body" (his lean); "I walked this one in the dark and called" (God called the man; she called; he answered); verse 3 "Two sat in white on either side, / the stone between them clean" | His notes on draft 3 |

**Stress ports (finding 95).** Line-final "where", "own", "was" stressed; "in-STEAD", "it-SELF", "SOME-one" (the dictionary stresses both syllables); "rab-BO-ni"; "just" weak before a stressed word; a wh-word opening an indirect question after its object pronoun stressed ("asked me WHO", "asked me WHY", "tell me WHERE").

## The quotable line (10.20)

- **Remembered:** "I took him for the gardener," leads (+7.03; the title, sung three times and again in the last line).
- **Annotated:** "I said, sir, if you carried him," leads (+5.20).
- **The middle slot:** "and someone stood among the trees.", the one line in the top quarter of both lists apart from the Annotated top.
- **The writer's blind pick (9 Nov):** C, "I took him for the gardener,": the Remembered top.

## The melody

**The designed notes first.**

- **The title cell (refrain line 1):** i F4 | TOOK A4 him G4 for A4 the C5 | GAR-den-er D5 (the feminine tail on D5, rule 21.7a), over Dm | B♭. Refrain 2 copies refrain 1.
- **The seed (fix 89 as a port, now from the start):** line 1 of verses 1–3 sings the cell's opening (F4 A4 G4 A4) and turns down to F4 where the title climbs to D5. Verse 1's nine syllables take it with a two-note pickup ("It was").
- **Aimed:** DAWN on A4 over F; GONE on A4 over A, a half cadence.
- **The Name (fix 67 as a port: anchors):** line 3's NAME on A4 with the band silent (N.C.); line 4 designed over four bars: MA-ry on F♯5, the first F♯ of the song, as D major arrives; a bar's silence; "and I said, rab-BO-ni" to E5 over A.
- **Verse 4 (designed):** God walked the first garden (EVE on D5); MADE on E5; "and CALLED" on E5, syncopated; "and he AN-swered" on F♯5; NAME on C♯5 over A. The walk could not set its first line (ten syllables, five stresses, no pickup after RABBONI) or keep the climb; finding 97.
- **The last refrain (designed except line 4):** the cell in D major; refrain 1's line 2 in major; line 3 climbs to EARTH on A5 (the summit); line 4 walked, aimed at C♯5 over A; line 5 over four bars: the cell, a bar's silence, "and he WAS" on D5 over D, closed.

**The search.**

- **Volume:** 500 built from 1,007 attempts; 348 survived (69.6%). Order frozen c0bfe2d3ef48.
- **Deaths:** the refrain 249; verse 3 175; spectral 104; joins inside verse 3 32; realness 32; joins inside refrain 1 16; joins inside the Name 15; join verse 3 > the Name 8; range 8; the Name 7; tritone 6; verse 2 4; surprisal 2; verse 1 1.
- **Evaluation rules for this song:** A5 once, on EARTH; no F♯ in the voice before MARY; verse 4 reaches E5; the Name's line 4 and refrain 3's line 3 exempt from their section caps (F♯5, A5).
- **Pick:** 0313b36ca953 (#1). Two hand edits, logged and re-evaluated:
  1. Refrains 1–2, line 4: the walk's G4 G4 G4 A4 G4 A4 became G4 | A4 C5 D5 A4 | A4 ("just tell me WHERE he's gone"), the best of the variants that pass (finding 102).
  2. Verse 3's last line: TREES moved from the fifth eighth to the second beat; the Name's "he" shortened to an eighth pickup.
- **The edited melody:** 7ccaf9f2d1d8, passes. Composite 0.880 (the pick 0.878), realness 0.50, IC 0.70, CMP 0.57, memory horizon 0.76, fit 0.875, lift +2, strong-beat alignment 0.88, longest breath 4.62 s, no line-final stress off the beat.
- **Plans:** refrain ABCD drawn (surface ABC, skeleton ABA′, line 1 designed); verses ABCD, AAAA, ABCD drawn (line 1 the seed); the Name ABAC drawn (surface ABC, skeleton AAA′) plus the designed line.

**Ranges:** verses D4–B♭4; refrains F4–D5; the Name F4–E5 and the one F♯5; verse 4 G4–F♯5; the last refrain F♯4–A5. Mezzo edition: everything a minor third lower (B3–F♯5).

## The arrangement and the demo

- **Ensemble:** piano (the walking figure: the left hand root, fifth, tenth | octave, tenth, fifth in eighths; verse 1 bare; a right-hand chord from refrain 1, on both beats in verse 4 and the last refrain), cello (the root from verse 2; the answers; the interlude; held bass), strings (pads in the refrains, the interlude's swell, the Name's build, full from verse 4).
- **The anchors:** the whole ensemble silent for bar 54 ("said my name"); bars 55–56 one soft D major chord a bar ("Mary"); bar 77 the strings alone on A, the voice silent; checked in the build.
- **Fix 90 (the cello answers):** 4 answers (verse 2 lines 2–4, verse 3 line 2). Five lines had no room: the seed lines end on bar 2's second beat, and verse 3's last two lines run late (finding 101).
- **Fix 91 (the interlude, one note changed):** the cello sings refrain lines 1–2 an octave below; DAWN rises from A3 to C♯4 over A (bar 40), the leading tone.
- **Fix 93 (the coda returns):** the piano states refrain 3's title notes (F♯4 A4 G4 A4 C♯5 D5 D5 D5); the last chord D with an added E, A4 on top.
- **Guide voice:** flute, at the soprano's pitch.
- **Stems:** the voice sits 5.0 dB over the ensemble (rule: at least +3), vocal gain 2, ensemble CC7 104.
- **Energy (9.12), per four beats:**

  | Section | Read |
  |---|---|
  | Intro | 0.25 |
  | Verse 1 | 0.11 |
  | Refrain 1 | 0.47 |
  | Verse 2 | 0.51 |
  | Refrain 2 | 0.67 |
  | Interlude | 0.68 |
  | Verse 3 | 0.49 |
  | The Name | 0.50 |
  | Verse 4 | 0.74 |
  | Refrain 3 | 0.79 |
  | Coda | 0.13 |

  Each refrain reads above its verse; the last refrain is the top. The Name's last quarter falls (0.61 to 0.42) by design: the silent bar and the held chords under "Mary".

## Documents

- **Lead sheets (2 pages each), soprano and mezzo (fix 92):** D minor to D major at bar 55 (B minor to B major); the tempo changes; NAME, MARY, the summit and the close marked; the F♯5 ossia (D♯5 in the mezzo). LilyPond's MIDI read back: 250 notes each; match.
- **Full score (4 pages):** voice, piano (grand staff, split by hand: finding 103), cello, strings. Read back: voice 250, piano right hand 198, left hand 421, cello 78, strings 150; all match.
- **Parts (4 pages):** piano, cello, strings; all read back and match.
- **Nashville chart (1 page):** numbers in D minor (1 = D: 1m, ♭3, 4m, 5, ♭6, ♭7), then D major; N.C. in bar 54.
- **Songbook and production notes:** one document, as a Doc and Word, with the producer one-sheet; references checked by a live search.
- **Consistency check:** all checks pass, with new ones for the title cell, the seed, the aimed notes, NAME (the band silent), MARY (the first F♯, D major), the one A5, the close on D, the hush bar, the cello's answers, the interlude's changed note, the coda and both editions.

## Findings

95. **More stress readings.** Line-final "where", "own", "was"; two-stress dictionary words ("instead", "itself", "someone"); "rabboni"; "just" before a stress; a wh-word after its object pronoun. **The run's port:** a song-32 pass in the stress rules. **Proposed fix 95:** fold these into the stress rules with fixes 7, 19, 24, 39, 46, 57 and 64, read through fix 45's single function.
96. **A line before a downbeat-start line loses an eighth.** The rhythm limit was n−3 when the next line has no pickup, n−2 otherwise; "I said, just give me back the body" (nine syllables) could not fit and the Name died 41 times in 60. **The run's port:** n−2 always (an eighth's breath before the next line). **Proposed fix 96:** the same, in the section rhythm builder.
97. **Designed lines are still walked.** The section's rhythm pass walks every line, including the ones a design replaces; a designed line the walk cannot set (verse 4's ten-syllable first line with no pickup; the Name's four-bar line) kills the whole section. **Proposed fix 97:** skip designed lines in the rhythm pass and take the next line's pickup limit from the designed cell.
98. **A mode turn has no field.** The arc (minor until a word, major from it) was hand-built: the scale per bar, the key signature at the bar, a custom check that no F♯ is sung before MARY. **Proposed fix 98:** a "mode turn" anchor on a syllable (with fix 68's key-change anchor): the new scale from that bar, the characteristic note barred before it, the engraving's key change placed there, all checked.
99. **The refit transposes by semitones, not by mode.** Refrain 3 sings refrain 1's tune in the parallel major; the run mapped F→F♯, C→C♯, B♭→B by hand. **Proposed fix 99:** a modal map in fix 59's refit (degree for degree).
100. **The leap rule reads across rests.** MARY's F♯5 to "and" a bar later died as a 9-semitone leap until the answer was moved to B4. **Proposed fix 100:** measure leaps within phrases; a rest of a beat or more starts a new phrase.
101. **The answer window is too tight for late endings.** "End by the next line's downbeat" left room for 4 of 9 possible answers. **Proposed fix 101:** shorten the figure to the room (two notes when three won't fit), or let it run under a one-eighth pickup an octave below.
102. **Refrain lines sag under a designed title.** With the title designed to D5, the walked lines 2–4 centred G4–B♭4; the last line sat on G4. **The run's port:** a hand edit chosen from the variants that pass, by the composite. **Proposed fix 102:** set later refrain lines' centres from the designed title's top (for example, top minus a fourth), or aim one of them at the title's top note.
103. **The full score split the piano by pitch.** Left-hand tenths above C4 landed in the right-hand staff. **The run's port:** split by each event's hand. **Proposed fix 103:** the same in every score and parts script (an engraving lesson for the skill).
104. **Two engraving lessons.** A held note overlapping the next entry (the cello's root under the interlude's pickup) forced a second voice and stopped the parts' rests compressing: trim held notes to the next entry in the build. And "#" in LilyPond markup is Scheme: write "C-sharp" in prose markup.
105. **The tail rule and a spoken name.** Rule 21.7a put both syllables of "Ma-ry" on F♯5. The run kept it as the design ("as he would say it"), but a falling third is the natural call (song 29's "Ab-ba"). **Proposed fix 105:** let a designed anchor exempt itself from 21.7a with a logged reason.
106. **v65 fixes used as ports:** 9, 24 and 64 (stress), 13, 31 and 56 (form lengths), 25 (voice options), 26 (ASCII track names), 29 (line-final stress on a beat), 30 (aimed notes exempt), 32 (fitted cells clear the pickup), 33 (MIDI tempo in quarters: ♩. = 52 written as 78), 34 (spelling from the key: C♯ in D minor, A♯ in B minor), 36 (production notes in the songbook; the full score for a keyboard-led song), 47 (breath scaled: 7.0 s), 48 (9.12 per four beats), 59 (refit), 67 (anchors), 69 (the producer one-sheet), 89 (seed), 90 (answers), 91 (one note changed), 92 (editions and ossia), 93 (the coda returns), 94 (the title test).

## Revision 1 (9 Nov, after delivery)

The writer was still reluctant about verse 3's "the stone between them clean": "I don't think the lyric works because it confuses the listener." Checked against the line: it asks the listener to infer, at tempo and on one hearing, that she came to wash a body and the place is already clean; read, it lands; sung, "clean" arrives without its reason. Three options were offered; he chose A, **"with no one in between"**: six syllables in the same rhythm, the long-e sound kept against "trees", the empty place stated plainly, and "no one" setting up "someone" two lines later.

- **Melody:** the new words take the old line's notes syllable for syllable (with F4 | NO G4 one G4 in G4 be- F4 | -TWEEN E4 at bar 44's downbeat). No note changed; the melody re-evaluates unchanged (composite 0.880; strong-beat alignment 0.867, was 0.876, since "in" now sits on the second beat).
- **Arrangement:** unchanged (the cello's answer to the line plays the same three notes).
- **Documents:** lead sheets (both editions), full score and parts re-engraved and read back (all match); songbook (Doc and Word) updated; the quotable-line slots unchanged.

**Finding from the revision**

107. **No listener-clarity test in the room.** The room scores stress, span, rhyme and the never-say list; nothing asks whether a line can be understood on one hearing at tempo without an inference the song hasn't set up. "The stone between them clean" passed every test and the run defended it; the writer heard the problem. **Proposed fix 107:** a one-hearing check in the writing room: flag a line whose key word's sense depends on an earlier line by more than one step (here, "clean" needs "wash the dead" from verse 1), and show it to the writer with the inference spelled out.

## Blind-pick record

Song 32 (9 Nov): C, "I took him for the gardener,": the Remembered top (the title line). Through song 32, over 20 picked songs: Annotated top 6, Remembered top 7, middle 6, refrain 1.
