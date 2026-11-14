---
title: "The World Is Asking: test report"
subtitle: "Words and music: Jason Bryant"
---

# Intake

| Question | Answer |
|---|---|
| What the song is about | From the writer's paper *Beyond the Kantian Seal*: the world is asking |
| Voice | One who believed the seal, first person |
| Stance | Answers the summons, with a prayer rather than a proof |
| Sound | Indie folk: acoustic guitar, piano, strings that open up |
| Singer | Baritone |
| Tempo | ♩ = 84, walking, fingerpicked 4/4 |
| Form | Verse, chorus, verse, chorus, bridge, last chorus |
| Title | The World Is Asking |
| Never say | No technical words (Kant, formula, quantum and the rest), and never "God" |
| Lyric | Four drafts; the writer's notes on verse 1, the chorus's images, and verse 2's repeated openings; locked at draft 4 |
| Key | G major |
| Form length | Every line two bars; 4-bar intro and outro; 100 bars, 4:46 |
| Hook | A question left open: up to D4 on "ask-", held; the last line home to G |
| Bridge | Down and in; a bar of silence before "Here I am"; held open on D |
| Deliverables | No GarageBand MIDI; a full score instead (the writer, 14 November) |

# The melody search (Luthier v4)

Engine: melody_l4_p59.py, written by gen_l4_p59.py from song 48's Luthier v4 file (680 to 683 in force), with the song's own parts. Seed 20261113+449; 1,000 builds each, main and control.

| | Main | Control |
|---|---|---|
| Survivors | 628 | 618 |
| Order | a467ceb242b7 | e8691d73b008 |
| Deaths, leading | bridge opening unrelated 111; the chorus above the verse 110; rhythm, no placement 65; key word off a chord tone 35 | 124; 118; 48; 36 |

**The pick of record:** eaf2dcc068b6, the engine's pick on the default path (the refit's first clean survivor with a gain of 0.14 or more; its gain is 0.347), taken as drawn, with no hand edits. It passes every gate and all three designs.

**Each fix's own reading** (main / control; the targets are the paper's):

| Reading | Target | Song 49 | Result |
|---|---|---|---|
| Bars sung in a kept song (the session's table reading) | 81% within 8 | 81.3% / 81.9% | Pass |
| Same rhythm four bars apart | 20% within 8 | 19.1% / 19.8% | Pass |
| Gain under the kept couplings | 0.12 or more | 0.244 / 0.254 | Pass |
| Sung note easier than a neighbour | 89% within 3 | 87.1% / 87.1% | Pass |
| Easier than every neighbour | 73% within 5 | 67.7% / 67.6% | Fail, by a third of a point |
| Mean ease, bits a note | 3.3 to 4.35 | 4.35 / 4.33 | Pass, at the top |
| Repeats: song; verse window; chorus window | kept quartiles | 24.5%; 26.2%; 24.0% | Pass |
| Bars on a figure already sung | 49% within 8 | 45.3% / 45.9% | Pass |
| Bits saved first half to second, a gap | 0.29 within 0.1 | 0.087 / 0.087 | Fail |
| Deaths for want of a placement | under 20 a thousand | 65 / 48 | Fail (699) |

The judge of record beside density peers (printed, not deciding): -1.51 / -1.36; Verse 1 -1.24 / -1.13; Chorus 1 -1.78 / -1.59.

# The melody search (Luthier v6, 14 November)

Engine: melody_l6_p59.py, written by gen_l6_p59.py from song 48's Luthier v6 file (711 to 715 and 717 in force). Same seed (20261113+449), designs and lyric; 1,000 builds each, main and control.

| | Main | Control |
|---|---|---|
| Survivors | 660 | 662 |
| Order | ef9d3a2a2039 | bf016d1e7243 |
| Deaths, leading | the chorus above the verse 150; rhythm, no placement 60; limits 37; bridge opening unrelated 29 | 123; 55; 49; 41 |
| The judge's pick (715) | 625a95a05b1f | 8ab6722be0f2 |

**The pick of record: e2b80cdc3a1c** (the writer's choice C, 14 November). The judge's pick, 625a95a05b1f, has no charge, but its Verse 1 chants on one note through its first two lines (eight D3s, then eight C3s): its verse window repeats a note in 59% of its moves against a kept 75th percentile of 36%. The judge reads repeated notes over the whole song (34%, inside the kept middle half), so it does not see a verse that chants (728). Among the 470 builds the judge finds eligible, 135 keep every section's window under that ceiling; the judge's own rule among them (least charge, then nearest the kept medians among the 54 within 0.02) gives e2b80cdc3a1c: charge 0.0005, the 86.2% place among kept songs. Taken as drawn, no hand edits; it passes every gate and all three designs. Its verse sits around D3 and its chorus around B3, nine semitones higher (the v4 pick: G3 and A3); its verse repeats a note in 23% of its moves; its chorus's line 2 takes up the hook's climb again.

**Each fix's own reading** (main / control; the targets are the paper's):

| Reading | Target | Song 49 under v6 | Result |
|---|---|---|---|
| Bars whose rhythm a kept song sings (710, the full list) | 81% within 8, both sides | 82.3% / 82.8% | Pass |
| Eighths against the build's own palette: verse; chorus; bridge | within 10 | 64.4 v 54.5; 63.6 v 54.2; 66.4 v 54.2 | Verse and chorus at the edge, bridge fails |
| Bits saved first half to second, a gap | 0.29 within 0.1 | 0.066 / 0.071 | Fail (725) |
| Dense lines' longest run of equal gaps | 4 within 1 | 5 / 5 | Pass |
| Deaths for want of a placement | under 20 a thousand | 60 / 55 | Fail, all at Verse 1 line 4 (726) |
| Sung note easier than a neighbour; than every neighbour | 89% within 3; 73% within 5 | 87.0 / 86.9; 69.3 / 69.0 | Pass; pass |
| Repeats: verse window (kept 75th 36.2%); chorus window | under the ceiling | 36.7% / 38.3%; 25.9% / 27.5% | Verse over (723); chorus passes |
| Mean ease, the judge's reader | 3.3 to 4.35 | 3.88 / 3.89 | Pass |
| Entries before / on / after the bar line (3.5 to 4.5 notes a bar) | kept 33 / 18 / 50 within 10 | 22 / 33 / 45 | Fail (721) |
| Bars on a kept figure (717) | 56% within 15 | 42.0% / 43.0% | Pass, at the edge (722) |
| Bars on a figure already sung (651) | 49%, kept middle half | 46.8% / 46.6% | Pass |
| The ruler (718): pick; median build | beside 22% and 10% | 0 at 86.8%; 0.020 at 84.3% | Printed |

The judge of v132 beside density peers (printed, not deciding): -1.44 / -1.41; Verse 1 -1.27 / -1.21; Chorus 1 -1.61 / -1.60.

# Arrangement and demo

- Fingerpicked acoustic guitar; piano; strings that open up; acoustic bass from halfway through verse 1; brushes in the choruses, sticks in the last.
- The bridge falls silent for its ninth bar, voice and band.
- Harmony (above and below) on the hooks and on every line of the last chorus.
- Energy by section (9.12), rebuilt on the v6 pick: Verse 1 0.64 (a build), Chorus 1 0.75, Verse 2 0.66, Chorus 2 0.84, Bridge 0.53 (a build), Last Chorus 0.99, Outro 0.30. Each chorus is above its verse, and the last chorus is the top.
- The lead stands +4.1 dB over the band (the rule asks +3).

# Documents

Rebuilt on 14 November from the v6 pick of record, e2b80cdc3a1c: the lead sheet, full score, parts, number chart, songbook, MusicXML (lead sheet and full score) and the demo (MP3, General MIDI). The songbook's verse notes, the singer's register, the lyric sheet's pickups and the note outside the scale are read from the record.

- Every pitched staff of the lead sheet, parts and full score reads back from LilyPond's MIDI note for note.
- Every drum hit is written.
- MusicXML reads back with music21: onsets and pitches match the record.
- Consistency: 43/43 checks pass.

# The blind pick (10.20)

Three slots, to be offered in shuffled order:

- **Remembered:** "But the world is asking"
- **Middle:** "In the first light of it all" (top quartile under both)
- **Annotated:** "I don't have proof, I have a door"

# Findings

## 699 Song 49 under Luthier v4: the rhythm lands, the template's bar meets 308's cap

**Problem.** On a new song, the v4 readings land where song 48's did not. The one recurring failure is a template bar that holds more of a line than 308's cap allows.

**Evidence.**

- Bars sung in a kept song: 81.3% / 81.9%, even on the session's table reading. By count, 4 notes 90%, 6 notes 86%, 7 notes 63%, 8 notes 49%.
- Same rhythm four bars apart: 19.1% / 19.8%. Gain 0.244 / 0.254.
- Repeats sit at the kept medians for each window's density.
- The per-note reading: 87.1% / 87.1% (passes); 67.7% / 67.6% easier than every neighbour (fails 73% within five by a third of a point), at a power of 3.10 / 3.03.
- Mean ease 4.35 / 4.33, at the top of the band.
- Bits saved a gap: 0.087 / 0.087 (kept 0.29). This is 692's compounding again: the verse and chorus sing eighths.
- Every death for want of a placement (65 / 48) is at Verse 1's fifth line, "I grew up trusting what I could touch" (9 syllables). Its template line, "There's a door in my father's house" (8 syllables), sings all eight notes in its first bar. A bar of 8 of 9 notes exceeds 308's cap for a line of nine (57%, so 5), so 313 will not copy it, 680 cannot take it as the template's bar, and the old draw rarely finds room.

**Fix (proposed).** 308's cap applies to drawn bars, not to the template's bars: a template bar that passed its own line's cap is taken as it is. With 692's likelihood ratio, the bits saved are read again.

**Check.** Deaths for want of a placement under 20 in a thousand on song 49; the template's recurrence held.

## 728 The judge reads repeats over the whole song, so its pick can chant a verse

**Problem.** 715's eligibility asks the song's repeated notes and ease to lie in the kept middle half; 713's ceiling is a test on each window. The judge's pick for song 49 lies inside the first and far outside the second.

**Evidence.** Song 49 under v6, main: the judge's pick 625a95a05b1f, charge 0, the 86.8% place. Its song repeats a note in 34% of its moves (kept middle half 19% to 38%), but its Verse 1 window in 59% and Verse 2 in 58%, against the kept 75th of 36% for their density: the verse's first two lines sing eight D3s, then eight C3s. Of the 470 eligible clean survivors, 135 keep every section window under the ceiling. The writer chose the re-pick e2b80cdc3a1c (charge 0.0005, the 86.2% place).

**Fix (proposed).** Add to 715's eligibility what 713 tests: every section window's repeats under the kept 75th for its density; or let the judge read repeats by window.

**Check.** The pick's windows under 713's ceiling, on songs 48 and 49.
