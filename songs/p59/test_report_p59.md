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

# Arrangement and demo

- Fingerpicked acoustic guitar; piano; strings that open up; acoustic bass from halfway through verse 1; brushes in the choruses, sticks in the last.
- The bridge falls silent for its ninth bar, voice and band.
- Harmony (above and below) on the hooks and on every line of the last chorus.
- Energy by section (9.12): Verse 1 0.65, Chorus 1 0.76, Verse 2 0.66, Chorus 2 0.83, Bridge 0.53 (a build), Last Chorus 0.99, Outro 0.30. Each chorus is above its verse, and the last chorus is the top.
- The lead stands +4.1 dB over the band (the rule asks +3).

# Documents

The lead sheet, full score, parts, number chart, songbook, MusicXML (lead sheet and full score) and the demo (MP3, General MIDI).

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
