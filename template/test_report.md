---
title: "Through Its Breaking — Test report (ZenEng v64)"
author: "For the engine's maintainers; not for musicians"
date: "6 November 2026"
---

# Through Its Breaking — test report (ZenEng v64)

This is the engine's record of song 25, kept apart from the songbook (musicians only).

## The intake

The writer's seed: his parable book, *Wild Fruit* (Wild_Fruit_KDP_v4.docx), "material to read to consider for the next song."

| Question | His answer |
|---|---|
| Which parable | A: "The Cracked Bell" |
| Who tells it | A: a third-person story ballad |
| Sound | B: piano ballad. The piano is the bell (low ringing octaves; the crack a half step struck together); strings build to the night |
| Voice (11.2) | A: female, A3–B4, C5 once |
| Tempo and feel | B: 6/8 in two, ♩. = 54, the bell swinging |
| Form | A: two long verses, each into the chorus; the winter night as the bridge; the last chorus turned (about 3:10) |
| Key | A: A minor verses, C major chorus; C5 on the tonic at the turn |
| Title | B: "Through Its Breaking" |
| Never say | C: both lists (the sermon words; the clichés, kept clear of Cohen's crack and light) |
| The winter night's need | A: unnamed, as in the parable |

- **Standing ask:** show the lyrics before drafting the music.
- **The form grew** from 84 bars (about 3:10) to 88 bars (3:16): two 2-bar bell interludes after choruses 1 and 2 (finding 4).

## The writing room

Two drafts. The writer locked draft 2. The room scored every line afterwards: 38 written, 35 alive.

| Round | What changed | Why |
|---|---|---|
| Draft 1 | The run's lyric | — |
| Draft 2 | Verse 1 trimmed to six lines. The chorus's second couplet: "like your name in a stranger's mouth / and every hour she rings it through." Verse 2 gained "she never meant to love the thing / it found her, year by year, at the wheel" | His notes: verse 1 listed the bell's functions; the chorus couplet lacked weight; the keeper needed one more precise interior moment |

- **Deaths:**
  - "and every hour she rings it through" died on a weak ending ("through"). Kept by the writer's lock. "Rings it through" is a phrasal verb: the particle carries the stress (v65 fix 24).
  - "she thought: the note is still in it" died on a weak ending ("it"). Kept by the writer's lock. A pronoun-object ending after a stressed word (v65 fix 9).
  - "two almost-notes where one should be" (draft 1's chorus) died on a weak ending, and the writer cut it.

## The quotable line (10.20)

- **Remembered:** "and every hour she rings it through" leads (+5.12).
- **Annotated:** "the bell rings" leads (+3.47).
- **In the top quarter of both:** "it rang through its breaking" (the title line), which fills the middle slot.
- **The writer's blind pick:** A, "it rang through its breaking" (the middle slot, top quarter under both). The title line, and the line the melody was built around.

## The melody

**The designed notes first.**

- The title line, "it rang THROUGH its BREAKing," runs over four bars (F G C C). THROUGH is on C5 over C at the third bar's downbeat, held; this is the C5 allowance, used once.
- "TRUE" is on A4 over F in every chorus. "rings it THROUGH" is on G4 over G, left open.
- "REACHED" is on B4 at the end of the bridge, the bridge's top.
- The tag is low (C4–D4); "CARries" is on C4 over C.

**The search.**

- **Volume:** 480 built from 1,053 attempts; 63 survived.
- **Deaths:** realness 353; verse 2 143; join chorus 1>chorus 1 138; join verse 2>verse 2 114; tag 60; bridge 57; line-final stress off the beat 52 (the new test, finding 1); join verse 1>chorus 1 39; spectral 10.
- **Pick:** 255b01910113. Composite 0.924, realness 0.51, IC 0.88, CMP 0.62, M 0.77, fit 1.00, lift +4, strong-beat alignment 0.95.
- **Plans:** verse 1 ABBAEE; verse 2 ABCDEEEE (each quatrain its own letters); bridge AABCEFGH.

**The first run was set aside.** Its pick (290f374a7d5d, composite 0.931) put nine lines' last stressed syllable off the beat: "at all," "fell still," "like snow," "the only bell," "frozen fields," "the bell rings," and others. The engine had no test for this. The run added one (finding 1) and searched again. The new pick has two left, both in the bridge: "fell still" (slot 8) and "the split note went" (slot 7). These are within the new limit of two.

**One hand edit, logged.** In the tag, each "the" moved off the downbeat to the eighth before the stressed word, so the bell has the downbeat to itself. The pick's fingerprint after the edit is 88b42878b8cd; it still passes every check (composite 0.924).

**Ranges:** verse 1 A3–E4; chorus C4–A4; verse 2 A3–E4; bridge A3–B4; chorus 3 C4–C5; tag C4–D4.

## The arrangement and the demo

- **Piano:** the 6/8 ballad figure in the left hand (R–5–8–10–8–5); verse 1 thinner; a right-hand chord in the choruses.
- **The bell:** on the piano, its own MIDI track. A low octave toll on 1, and the crack on 2: the root with the half step below it. It plays in the intro, the interludes, bridge bars 61–68, all of chorus 3, the tag and the outro. The last bar is B4 against C5 over C, unresolved.
- **Cello:** from chorus 1's second couplet. **Strings:** chorus 2, building through the bridge, full in chorus 3, out for the tag.
- **Guide voice:** oboe.
- **Stems:** the voice sits 7.9 dB over the band (rule: at least +3).
- **Energy (9.12):**

  | Section | Read |
  |---|---|
  | Intro | 0.34 |
  | Verse 1 | 0.14 |
  | Chorus 1 | 0.49 |
  | Interlude 1 | 0.42 |
  | Verse 2 | 0.57 |
  | Chorus 2 | 0.67 |
  | Interlude 2 | 0.48 |
  | Bridge | 0.90 (a build) |
  | Chorus 3 | 0.97 |
  | Tag | 0.44 |
  | Outro | 0.35 |

  The first arc read the interludes above chorus 1 and the bridge above chorus 3. Fixed by softening the interlude bell and bringing the bell into chorus 3.
- **27.21 (the instrumental line) was not run.** The bell is a texture, not a tune (finding 6).

## Documents

- **Lead sheet:** voice and lyric, with the bell cued on a small piano grand staff (crack above, toll below) that appears only where the bell plays. LilyPond's MIDI read back: voice 287, crack 70, toll 70; all match.
- **Nashville chart:** each section numbered in its own key (A minor: 1m, ♭3, 4m, 5, ♭6, ♭7; C major: 1, 3m, 4, 5, 6m).
- **Consistency check:** 27 of 27.

## Findings

1. **The last stressed syllable of a line off the beat.** The rhythm walk scored strong-beat agreement for the whole line but had no test for where the line's last stress lands, so the first run's pick ended nine lines off the beat. **The run's port:** the walk prefers rhythms whose last stressed syllable falls on a beat (in 6/8, a dotted-quarter pulse); evaluation allows at most two lines without it, aimed lines exempt. **Proposed fix 29:** make this a standing rule for every metre.
2. **Weak endings the writer keeps.** "rings it THROUGH" and "still in IT" both died in the room. They are covered by v65 fixes 24 (phrasal verb stress) and 9 (pronoun-object ending). This song confirms both.
3. **An aimed peak on a weak word.** THROUGH (C5) was refused as a reduced syllable, so chorus 3 never built. **The run's port:** aimed notes are exempt from the reduced-peak rule. **Proposed fix 30:** generalise song 24's refrain exemption to every aimed note.
4. **Dense lines in compound metre.** Lines of 9–10 syllables in two bars of 6/8 left no room for the next line's pickup, so joins failed. Three changes were needed:
   - 2-bar interludes after choruses 1 and 2;
   - pickups up to four eighths at the bridge's start and three inside the bridge;
   - chorus 3's line-3 pickup worked out from line 2's end.

   The form grew by four bars. **Proposed fix 31:** intake's form-length estimate (v65 fix 13) counts syllables per bar against the metre and prices interludes before the writer chooses.
5. **A fitted cell must clear the next line's pickup.** A repeated letter fitted by stress could end where the next line's pickup begins. **The run's port:** the check was added. **Proposed fix 32.**
6. **A texture is not an instrumental line.** The bell has no tune, so 27.21 doesn't apply, but v65 fix 27 (the instrumental lead in energy) still counts it as band. **Proposed:** a "texture" kind beside fixes 10 (riff kind) and 21 (quote kind).
7. **Tempo for compound metre.** The MIDI tempo was written as dotted-quarter BPM. The first render ran 4:56 instead of 3:18. **Proposed fix 33:** the record carries the beat unit; MIDI tempo is written in quarters (♩. = 54 is ♩ = 81).
8. **Spelling from the key.** The lead sheet spelled A minor's leading tone as A♭ until the pitch map took sharps. **Proposed fix 34:** engraving spells pitches from the section's key.

## Blind-pick record

Song 25: A, the middle slot (the title line). With songs 13–24 from the v65 fix list, the tally over 13 songs: Annotated top 5, Remembered top 4, middle 3, refrain 1.
