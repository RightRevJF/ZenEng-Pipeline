---
title: "Either Or — Test report (ZenEng v64 + v65 fixes)"
author: "For the engine's maintainers; not for musicians"
date: "7 November 2026"
---

# Either Or — test report (ZenEng v64, v65 fixes as ports)

This is the engine's record of song 27, kept apart from the songbook (musicians only). The test: art rock from the writer's own poem, in mixed metre (5/4 verses, 4/4 refrain) and a mode (D Dorian against F major).

## The intake

| Question | His answer |
|---|---|
| Source | His poem, three stanzas ("Where is the conflict, its with either or" / "Theologians are cowards, hiding in words" / "The mugwumps are hated by denizens of dread") |
| How to treat the words | "B leaning towards C": the stanzas as verses plus a refrain from his words, shaped for singing |
| What the poem is about | The run's reading, given at his request: against either/or (Aristotle's excluded middle), theologians systematizing the wind, the partisans of dread who hate the mugwumps |
| What the refrain carries | C: the wind, the spirit that won't be systematized (over the recommended both/and) |
| Voice (11.2) | A: tenor D3–A4, B♭4 once |
| Sound | A: angular art rock, two interlocking clean guitars, melodic bass, accented drums; the refrain opens into ringing chords over an organ drone |
| Metre and tempo | A: verses 5/4, refrain 4/4, ♩ = 132 |
| Form | B: extended, 84 bars, 2:55, an 8-bar intro and an 8-bar 5/4 build (lengths printed per option, fixes 13 and 31) |
| Key | A: D Dorian verses (B natural), F major refrain (B♭): the either/or in one note |
| Title | B: "Either Or" (over the recommended "Systematizing Wind") |
| Production | "I'm going to need an all parts pdf for production": a band parts PDF |

## The writing room

Five drafts. The writer locked draft 5. The room scored 37 lines; 28 lived.

| Round | What changed | Why |
|---|---|---|
| Draft 1 | His poem, set nearly as written, with the run's refrain | — |
| Draft 2 | Three spots fixed for clarity (Aristotle named; the line of thought) | His choice B of three |
| Draft 3 | New verses in the refrain's voice, built around his strongest phrases | "I like the poem, don't like the lyrics other than the refrain"; then C of three |
| Draft 4 | A sharper opening (Aristotle's line in the dust); "weighing the wind by the words that they heard"; verse 3 about the ones punished for not choosing | His attached suggestions document |
| Draft 5 | "from the keepers of the dead"; "you can't fence it in, you can't keep score"; "sprinkled holy water on the laws they wrote"; "and we've bled across that line ever since"; "handing down their fathers' wars by name" | His five pasted notes |

- **Deaths of the poem's own lines.** The room killed 5 of the poem's 12 original lines, all on distinctive or rare words: "theologians are cowards, hiding in words" (3 distinctive words); "crowing their nonsense, syllables for the birds" (3); "the mugwumps are hated by denizens of dread" (4); "and it's into perdition that you're being led" (perdition, Zipf 2.46); "telling you one thing, different from what's read" (strong-beat agreement 0.17). Finding 50.
- **A locked line that died.** "said one thing's true and the other must be lies" (draft 4 on) died on V1, no concrete image. It stands by the writer's lock: in an argument song the abstract half of a couplet is the argument, and the next line ("the dust", "blood") carries the image. Finding 53.

## The quotable line (10.20)

- **Remembered:** "the wind was never either or" leads (+5.16; the title line, sung three times plus the turn).
- **Annotated:** "you can't fence it in, you can't keep score" leads (+3.98), and is in the top quarter of both lists.
- **The middle slot:** "and the wind blows where it wants to blow", by the rule for a song whose both-lists line already tops a list: the most-repeated hook line.
- **The writer's blind pick:** B, "the wind was never either or" (the Remembered top, the title line).

## The melody

**Mixed metre (the run's port).** A new metre, 5/4: 10 eighth slots a bar, beats on slots 0, 2, 4, 6 and 8, strong beats on 0 and 6 (3+2). Verses, intro, break and build in 5/4, refrains and outro in 4/4, ♩ = 132 throughout; a line takes two bars in either metre (20 slots in 5/4, 16 in 4/4). Finding 44.

**The designed notes first.**

- **SCORE:** F4 over B♭ in refrains 1–3; raised to B♭4 over B♭ in refrain 4, the song's only B♭4 (aimed; the B♭ that answers the verses' B natural).
- **OR:** the title line's last note on a tone of C (aimed): C4, beat 3 of the line's second bar.
- **The refrains:** refrains 2–4 copied from refrain 1 (by construction).
- **The turn:** "and YOU were never either or" on the title line's notes, alone after the band stops at bar 79 (by construction). "You" takes the stress "wind" had (finding 46).

**The search.**

- **Volume:** 500 built from 596 attempts; 389 survived (77.8%).
- **Deaths:** spectral 56; join verse 1 > verse 1 33; realness 30; verse 3 24; verse 2 22; breath 18; verse 1 16; verse contour 6; join verse 2 > verse 2 1; surprisal 1.
- **Pick:** b4e50177eaf9. Composite 0.922, realness 0.48, IC 0.96, CMP 0.59, M 0.64, fit 1.00, lift +8, strong-beat alignment 1.00, longest breath 4.77 s, no line ending off the beat.
- **Plans:** verses 1 and 2 ABAC (line 3 fitted by stress to line 1); verse 3 AABC (the fit to line 1 refused; re-walked, contour kept); refrain lines 1 and 3 drawn AB.
- **No hand edits.**

**Ranges:** verses F3–D4 (verse 3 F3–C4); refrains C4–A4; B♭4 once.

**Two early tries were set aside.** The first trial batches killed the locked lines on weak endings (finding 45) and on the breath limit (finding 47); refrain 3 then read above refrain 4 at the join until the first refrain line's peak was capped (first_maxpk 2).

## The arrangement and the demo

- **Band:** guitar 1 (the 5/4 eighth figure, accents on 1 and 4; ringing chords on 1 and 3 in the refrains), guitar 2 (offbeat answers; driving eighths in the refrains; tacet in verse 1 and the build), the break's hocket between them, fretless bass, organ (an F–C drone under the refrains, a swell through the build, D–A in the outro), drums (kick 1 and 4, snare 3 and 5 in 5/4; a ride groove in the refrains).
- **The stop:** everything rests from bar 79; the last line is the voice alone, N.C. on the lead sheet and in every part (finding 52).
- **Guide voice:** clarinet.
- **Stems:** the voice sits 3.3 dB over the band (rule: at least +3), at vocal gain 28, band CC7 84.
- **Energy (9.12), read per four beats (the run's port, finding 48):**

  | Section | Read |
  |---|---|
  | Intro | 0.77 (a build) |
  | Verse 1 | 0.74 |
  | Refrain 1 | 0.89 |
  | Verse 2 | 0.84 |
  | Refrain 2 | 0.89 |
  | Break | 0.76 |
  | Verse 3 | 0.77 |
  | Build | 0.93 (a build) |
  | Refrain 3 | 0.96 |
  | Refrain 4 | 0.88 |
  | Outro | 0.37 |

  Each refrain reads above its verse; refrain 3 is the top. Refrain 4 reads below it only because its last two bars are the designed stop (finding 52). Read per bar, the 5/4 verses carried a quarter more events than the 4/4 refrains and read as busy (finding 48).

## Documents

- **Lead sheet (3 pages):** voice (treble 8vb) with the lyric and chord names, `\time 3,2 5/4` and 4/4, D Dorian (no signature) and F major, the stop marked. LilyPond's MIDI read back: voice 257; matches.
- **Nashville chart (1 page):** D Dorian numbered from D (1m, 4, ♭3, 5m, ♭7, 1⁵), F major from F.
- **Band parts (9 pages):** guitar 1, guitar 2, bass, organ, drums; compressed rests, rehearsal marks, chord symbols, N.C. at the stop. Read back: guitar 1 782 notes, guitar 2 932, bass 453, organ 34, drums 737 of 737; all match the record.
- **Songbook and production notes:** one document (v65 fix 36), as a Doc and Word.
- **Consistency check:** 36 of 36, with new checks for the metre per section, the stop (no band note in bars 79–80; N.C. on every chord line), the B♭4 once on "score", the refrain copies, the turn, and B natural against B♭.

## Findings

44. **No 5/4, and no mixed metre.** The engine's metre table has no 5/4 and a form can't change metre between sections. **The run's port:** 5/4 with 10 slots, beats 0/2/4/6/8, strong 0 and 6 (3+2); a metre per section in FORM; `\time 3,2 5/4` in the engraving; the eighth split never crosses the 3+2 line. **Proposed fix 44:** add 5/4 (3+2 and 2+3) and 7/4 to the metre table, and make metre a field of each section, read by the walk, the breath rule, the engraving and the MIDI.
45. **The weak-ending test ignores the stress rules.** It read the last syllable's lexicon stress, not the line's stress after v58's rules, so locked lines ending "score", "or" and "no" died on weak endings. **The run's port:** the test reads the stress the rules assign. **Proposed fix 45:** every test that asks "is this syllable stressed?" reads the one stress function.
46. **Binary pairs and contrastive pronouns.** "yes or NO", "either OR" and "and YOU were never" read with the stress on the wrong word. **The run's port:** in "X or Y" at a line's end, Y carries the stress; a pronoun before "was/were/are never" in a line that repeats an earlier line with one word changed is contrastive. **Proposed fix 46:** add both to v58's stress rules, beside fixes 7, 19, 24 and 39.
47. **Fix 38's breath limit doesn't scale.** A fixed 4.6 seconds killed 5/4 lines of 14 syllables in 20 eighths. **The run's port:** the limit is the longest line's span plus two slots (5.0 s here). **Proposed fix 47:** state fix 38's limit as the line's span plus a breath, with a hard ceiling (6 s).
48. **9.12 counts per bar.** In mixed metre a 5/4 bar is a quarter longer than a 4/4 bar, so the verses read as busy as the refrains. **The run's port:** energy is counted per four beats. **Proposed fix 48:** 9.12 counts per unit of time (four beats or two seconds), never per bar; this joins fix 41's eighth windows.
49. **The calibration has no modes.** Its key profile is major/minor; D Dorian verses read as off-key against it. **The run's port:** the verses transposed +5 into the F frame for the calibration; CMP read on the refrain only. **Proposed fix 49:** the calibration reads a modal section in its parent major key, and names the frame in the record.
50. **The room kills the writer's own voice.** From his own poem, the distinctive-word limit (2 a line) and the rare-word floor (Zipf 2.75) killed 5 of 12 original lines: "theologians", "mugwumps", "denizens", "perdition" are the poem. **Proposed fix 50:** lines from the writer's source text are locked at intake like WRITER_PHRASES, and the room reports their distinctive and rare words instead of killing them; the writer chooses.
51. **Unknown words.** "systematizing", "birthed", "mugwumps" and "perdition" were missing from the lexicon. **The run's port:** LEXICON entries in intake. **Proposed fix 51:** intake lists the source text's unknown words, with a proposed stress for each, before the room runs.
52. **No field for a stop.** A sung section where the band drops out had nowhere to live, and 9.12 read the designed drop as a fall in the last refrain. **The run's port:** `stop_at` in the record; every part rests from it; N.C. on the lead sheet and parts; the songbook's non-negotiable. **Proposed fix 52:** a stop field per section (bars, who stops), read by the arrangement, the engraving and the parts; 9.12 leaves stop bars out of the section's read.
53. **V1 reads lines, not couplets.** "said one thing's true and the other must be lies" died for having no concrete image; its couplet partner has two ("the dust", and "blood" two lines on). Kept by the lock. **Proposed fix 53:** V1 passes an abstract line when the other line of its couplet carries an image of 4.0 or more.
54. **Fix 40 confirmed.** With the calibration read over all three verses (the refrains are copies), survival fell from song 26's 94.8% to 77.8%: the verses now face a real test. Still 7.8 points above fix 28's band; the designed refrains are half the sung bars.
55. **v65 fixes used as ports:** 9 and 24 (stress), 13 and 31 (form lengths), 14 (tenor row), 26 (ASCII track names), 29 (line-final stress on a beat), 30 (aimed notes exempt), 32 (fitted cells clear the pickup), 33 (MIDI tempo in quarters), 34 (spelling from the key), 36 (production notes in the songbook); and from song 26's list, 38 (breath in seconds, scaled by finding 47), 39 (line-final stress) and 40 (calibration over every sung section).

## Blind-pick record

Song 27: B, the Remembered top ("the wind was never either or", the title line). With songs 13–26, the tally over 15 songs: Annotated top 6, Remembered top 5, middle 3, refrain 1.
