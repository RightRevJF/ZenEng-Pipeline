---
title: "Sadie — Test report (ZenEng v74)"
author: "For the engine's maintainers; not for musicians"
date: "9 November 2026"
---

# Sadie — test report (ZenEng v74)

This is the engine's record of song 33, kept apart from the songbook (musicians only). The test, the writer's choice: an up-tempo band song in 4/4 that runs what v65–v74 state and the code has not yet run, above all v72–v74's ranking (27.22) and the fixes the ledger lists as ahead of the code.

## The intake

| Question | His answer |
|---|---|
| What kind of song | A: an up-tempo band song in 4/4 (country-rock), a riff from the title, a designed drop, the senses dial "to hit" |
| About | A: Friday night football, the town in the bleachers |
| The fresh angle (fix 72: the image is worn; Chesney, Gilbert, Currington, Allen found) | A: the kicker is a girl, the only one on the team; her father sings from the stands |
| The turn | C: the song never says whether the kick is good; the drop is the ball in the air |
| Title (fix 94) | A: "Sadie" ("Maddie Ray" checked first: no song, but beside the duo Maddie & Tae) |
| Voice (11.2 rows, fix 25) | A: a baritone, a gang on "Sadie" in every chorus, the crowd on the last chorus |
| Tempo and feel | A: 4/4 at ♩ = 124, straight eighths, A major |
| Form (fixes 13, 31, 56) | A, printed as 88 bars, 2:50 (see finding 122) |
| Never-say | B: the football clichés, "Friday night" allowed |
| Commercial profile (fixes 71, 80) | A: country radio, 2020s: hold the norms, depart in two places (the drop, the unresolved kick) |

## The writing room

Four drafts; the writer locked draft 4. Between drafts 2 and 3 he passed on another reader's five vectors: four taken in part (the score line kept for the one-hearing check, fix 107; eye black instead of a visual crossbar, the senses dial; the whisper against the crowd; the Miller boy), the fifth declined because it reversed the locked turn and the writer's own note. His last note caught an ambiguous subject ("Stomping on the aluminum" read as Sadie stomping); "Feet pounding the aluminum" kept the syllable count and the downbeats.

**Stress ports (finding 123).** SOME-bod-y, CLOTHES-line; an independent possessive carries stress ("only MINE to say").

## The quotable line (10.20)

- **Remembered:** "Sadie! Sadie! Feet pounding the aluminum," (+4.83, sung four times).
- **Annotated:** "the holder spins the laces round;" (+3.29).
- **The middle slot:** "The snap comes back and the band goes quiet," (the one line in the top quarter of both).

## The melody

**The designed notes first.**

- **The title cell (chorus line 1):** SA E4, die C♯4, SA E4 pushed onto the and of 2, die C♯4, FEET A3 | POUND B3 pushed and held, -ing the a-LU-mi-num on B3 over E (21.7a's tail). Choruses 2 and 3 copy chorus 1; chorus 4 copies lines 1–3.
- **Chorus 4's last line (designed):** NEV-er on F♯4 over F♯m, the song's one F♯4, falling to SAME on A3 over D.
- **The drop (designed):** "it's UP," G♯3 to B3 on beat 3 of bar 61.
- **Aimed:** UP on B3 over E (pre-chorus); SOUND on E3 over E (bridge).

**27.22 as amended in v74, run as code for the first time.**

- **The register gate (110, 117):** verse top < pre top ≤ chorus top < the last chorus's top line, the bridge no higher than the chorus, and the verse at least a whole tone under the chorus. It killed 75 of 500 builds (the second-largest cause after one join), most where the aim on UP capped the pre-chorus at the verse's height.
- **The composite ranks the gate's survivors (112, 118).**
- **The flags (109, 111, 119, 120):** a line's last stress lands when it falls on a beat or is pushed an eighth ahead and held; a chorus line is dull with fewer than three pitches or a span under a third. The pick carries neither flag; of the top eight, one has a landing flag.
- **The top twenty kept, and the rerun record (113, 121):** seed 20261142, N 500, the code's hash, PYTHONHASHSEED 0. **Rerun: reproduced exactly** (500 built, 396 survivors, order frozen 8abbb8830302, both times). Fixing PYTHONHASHSEED is what makes it reproduce; v74 reports that song 32's run did not, and song 32 did not fix it.

**The search.** 500 built from 700 attempts; 396 survived (79.2%). Deaths: join chorus 2 > bridge 98; the register gate 75; the bridge 24; join verse 2 > pre 2 18; joins inside verse 1 17; chorus 4 into NEVER 17 (the first NEVER cell had a two-eighth pickup; moved to one); realness 13; join verse 1 > pre 1 8; spectral 8; CMP 8; verse 1 7; others 11.

**Pick:** fdf974a2136d (#1), no hand edits. Composite 0.935, realness 0.58, IC 0.89, CMP 0.69, memory horizon 0.79, fit 1.00, lift +5, strong-beat alignment 0.98, longest breath 4.35 s (limit 4.4 s, the line's span plus a breath; fix 47). Plans: chorus ABBC (line 1 designed); verses ABCA and AAAB; pre AB; bridge AAAB.

**Ranges (by section top, the gate's reading):** verses A3 (57); pre-choruses C♯4 (61); choruses E4 (64); bridge A3 (57); the last line F♯4 (66). Lowest note C♯3.

## The arrangement and the demo

- **The riff (fix 22, run as code):** the lead guitar plays the title cell's first bar (E C♯ E C♯ A B), then an open-A chug with a lick, transposed with the chord (finding 127).
- **The answers (fix 101, run as code for the first time):** each verse line is answered by its last notes an octave up, the figure fitted to the room before the next line: 7 of 8 lines answered (one three-note figure, six two-note figures), one line left none (a gap of one eighth).
- **The gang (fix 43):** "Sadie! Sadie!" in every chorus, unison and the octave below; all of chorus 4; two outro shouts.
- **The drop (fixes 60, 76, 82, 87):** the cut list carries it; bar 61 one hit, bars 62–64 the kick's heartbeat only; the build asserts the silence; the chart prints N.C.
- **Guide voice:** trombone, at the baritone's pitch. **Stems:** the voice 4.4 dB over the band (vocal gain 26, band CC7 82).
- **Energy (9.12, per four beats; the drop's three silent bars out of the reading, fix 87):**

  | Section | Read |
  |---|---|
  | Intro | 0.77 (a build) |
  | Verse 1 | 0.71 |
  | Pre 1 | 0.72 |
  | Chorus 1 | 0.83 |
  | Riff | 0.74 |
  | Verse 2 | 0.72 |
  | Pre 2 | 0.73 |
  | Chorus 2 | 0.84 |
  | Bridge | 0.66 |
  | Drop | 0.59 (bar 61 alone) |
  | Chorus 3 | 0.84 |
  | Chorus 4 | 0.92 |
  | Outro | 0.90 |

  Each chorus reads above its verse; the last chorus is the top; the drop reads below both neighbours (fix 60). Two corrections were needed on the way (findings 124, 125).

## Documents

- **Lead sheet (2 pages):** the voice in treble 8vb with the lyric and chord names; the gang cues, the drop and the one F♯4 marked. Read back: 326 notes, match.
- **Parts (11 pages):** drums, bass, rhythm guitar, lead guitar, acoustic, organ, gang (with its words). Every pitched part reads back and matches; drum hits 1,007 = the demo's. The drum part is spaced (fix 88: seven systems a page at most; the first build compressed three pages).
- **Nashville chart (1 page):** numbers in A; N.C. in bars 62–64.
- **Songbook and production notes:** a Doc and Word, the producer one-sheet included; references checked by a live search.
- **No full score:** the song is not keyboard-led (fix 36); available on request.

## The ledger, for song 33

Ran as code in this song: 22, 29, 43, 47, 60, 76, 82, 87, 88, 101, 108 in part (the build asserts who plays in the drop and consistency checks the documents' words against it; the rest of the prose is still hand-written), 110 and 117, 112 and 118, 109, 111, 119, 120 (computed; none fired on the pick), 113 and 121 (reproduced). Still ahead: 115 (the senses dial applied by hand; the norm sets are not on this machine), 80 (the departures named, no corpus measured), 23 (not reached: the riff is a riff kind).

## Findings

122. **The form option's length was typed, not summed.** Option A printed 88 bars; its parts summed to 84 (2:43). The outro took 8 bars to keep the length the writer chose. **Proposed fix 122:** the form question prints the sum of its parts and the length computed from it, never a typed total (with 13, 31, 56).
123. **Three more stress readings.** SOME-bod-y and CLOTHES-line read with two stresses; "mine" read weak in "only MINE to say". **The run's port:** a song-33 pass. **Proposed fix 123:** fold into the stress rules (with 95): one stress for compounds the dictionary double-stresses; an independent possessive (mine, yours, hers, ours, theirs) carries stress.
124. **9.12's windows read the humanized MIDI.** A downbeat entry humanized four ticks early fell into the section before it, adding a "track" to chorus 1 (0.89 against chorus 2's 0.84). **The run's port:** windows shifted 20 ticks. **Proposed fix 124:** read 9.12 from the record's events, not the humanized file, or window with a tolerance.
125. **9.12's mean velocity punishes a quieter added layer.** A tambourine at velocity 72 in chorus 2 lowered its reading below chorus 1's. **Proposed fix 125:** weigh added layers by loudness, not mean velocity (with 11).
126. **The register gate discriminates through the aims.** 75 of its deaths came from an aim that caps the line below it: UP aimed at B3 held the pre-chorus to B3, the verse's height in some builds. **Proposed fix 126:** the gate's report names the capping aim, and the plan can lower the verse's ceiling instead of killing the build.
127. **27.21's riff kind does not follow the chord.** The first build played the riff only on the tonic bars and left intro bar 3 (D) empty. **The run's port:** the riff transposes with the chord (up a fourth on D, down a fourth on E). **Proposed fix 127:** a riff kind states how it meets a non-tonic bar (transpose, pedal, or rest), and an intro may not leave a bar empty.
128. **The rerun record needs the hash seed.** Song 33 reproduced exactly only with PYTHONHASHSEED fixed. **Proposed fix 128:** fix 121's record names PYTHONHASHSEED, and every search sets it.

## Blind-pick record

Song 33: (pending).
