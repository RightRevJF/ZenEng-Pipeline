---
name: songwrite
description: Write a song with Jason Bryant through ZenEng — intake, lyric, melody search, demo, lead sheet, score, songbook with production notes, test report and fix list — using the ZenEng pipeline.
---

# Songwrite: a ZenEng song with Jason

Jason writes songs with ZenEng, his songwriting engine. Another AI maintains the engine's rules (the ZenEng spec: v64 plus the v65 fix list). This skill is how the songs actually get made: the working method, the tools, the deliverables and the checks. The spec decides *what the engine requires*; this skill decides *how we work*. When they disagree, the newest spec wins, and the disagreement goes on the next fix list.

## 0. Before the first question

1. **Get the tools.** In order of preference:
   - The GitHub repo `RightRevJF/ZenEng-Pipeline` (private). Attach it with the repo tool if one is available, then clone it to `/home/claude/zeneng-pipeline`.
   - Otherwise ask Jason to attach `zeneng-pipeline.zip` and unzip it to `/home/claude/zeneng-pipeline`.
   - Then run `bash setup.sh` from the repo root. It installs LilyPond, FluidSynth with the FluidR3 GM soundfont, pandoc, ffmpeg, the Python packages, the spaCy models and Playwright's Chromium, and links `lib/carol` and `lib/pop` to `/home/claude/carol` and `/home/claude/pop`. If LilyPond or FluidSynth can't be installed, say so at once: the lyric and melody work still runs, but the engraving and the demo won't.
2. **Get the rules.** Ask Jason for the current ZenEng spec if it isn't attached (v64 is the base; the v65 fix list is the Doc https://claude.ai/artifact/22vP86jMUxjoUBdy7mqz3H). Read both before intake. Apply the v65 fixes as the run's ports and log each one used.
3. **Start the song.** `bash newsong.sh NN` copies the template (the latest finished song) to `/home/claude/pNN` and renames the scripts. Every song-specific part must be rewritten: the intake LOG, the lyric, FORM, chords, designed notes, arrangement and all document text. Read `songs/p21`–`p24` for patterns the template lacks (duets and 7/8 in p22; a band, riff and push in p23; guitar with capo and TAB parts in p24).

## 1. Working with Jason

- **One question per turn.** Always three options, A, B and C, with a recommendation where it helps (mark it "(Recommended)"). Never group questions, even where the spec allows it.
- **Concise replies.** He reads on a phone. Lead with the answer. Don't recap steps.
- **Log every choice** in `intake.py`'s `LOG`: the question, the options, the recommendation and his answer, verbatim where he wrote words. This includes choices made after delivery.
- **Show the lyrics before any music.** Always show the whole lyric, every draft. Take his notes, revise, and show the full revised lyric. The music starts only when he says to lock it.
- **Credit line:** "Words and music: Jason Bryant" on every document.
- **Source material** he attaches (his books, poems) is read, used, and never copied into the repo.

## 2. The pipeline, one song

| Step | Script | Notes |
|---|---|---|
| Intake | `intake.py` | The song's constants: NEVER_SAY, NEVER_PHRASES, WRITER_PHRASES, voice row, tempo and metre, form with its length, key, title |
| Writing room | `w1.py` | Score every line; report the deaths and which lines the writer's lock keeps |
| Lyric | `lyric.py` | The locked lyric, sections, roles, SUNG order |
| Melody | `melody_pNN.py 500` | Inside `timeout 590`; never two runs at once. Read the deaths and fix the cause, not the symptom |
| Inspect the pick | by hand | Print every line: syllable, pitch, slot, length. Check that each line's last stress lands on a beat, the aimed notes, the ranges, the breaths and the joins. Any hand edit is logged in the record and must still pass `evaluate` |
| Record | `build_pNN.py` | One record holds every event (voice, accompaniment, instrumental lines). Every document is written from it |
| Demo | `demo_pNN.py` | MP3, General MIDI and GarageBand MIDI. MIDI tempo in quarters (♩. = 54 is ♩ = 81). ASCII track names. Stems: voice ≥ +3 dB over the band. 9.12 energy arc: each chorus above its verse, the last chorus or bridge the top, the build read where it arrives |
| Lead sheet | `engrave_pNN.py` | Voice, lyric, chord names, cue staves. Read the MIDI back per staff |
| Full score | `score_pNN.py` | Always for a keyboard-led song, and whenever asked. Read the MIDI back per staff |
| Parts | `parts_pNN.py` | For production: one part per instrument, written from the record (see p22–p24) |
| Chart | `nashville_pNN.py` | Each section numbered in its own key; band notes |
| Quotable line | `q1020.py` | The three blind-pick slots |
| Songbook | `songbook.md` | See section 3 |
| Test report | `test_report.md` | The engine's record: intake, room, melody search, arrangement, documents, findings |
| Consistency | `consistency.py` | Every document against the record. Everything must pass before delivery |

## 3. Deliverables

1. **Demo:** MP3, plus General MIDI and GarageBand MIDI files.
2. **Lead sheet** (PDF). **Full score** (PDF) when piano-led or asked. **Nashville chart** (PDF).
3. **Songbook and production notes**, as one document, delivered as a Doc and as Word (`pandoc --reference-doc=/home/claude/carol/songbook/ref.docx`). It is for musicians only: **no engine terms at all** (no module numbers, scores, fingerprints, certificates or version numbers). It contains:
   - at a glance, the form, what the song is about, and how to play it;
   - section by section: chords beside each line, with melody notes that give real bar numbers and pitches;
   - for each player, for the singer, and the arrangement;
   - the production notes at the end: a lyric sheet with bar numbers, a production brief (the song, three references checked by a live web search, non-negotiables), session notes (tempo and click, key, chords per bar, range, tracking, blend and panning, any part one player can't play at once recorded as its own pass), and the score and parts list.
4. **Parts PDF** when the song goes to production.
5. **Test report** (Word), kept separate: the engine's record and the numbered findings.
6. Send every file with SendUserFile, plus the Doc link. Then one line on what changed or what to know (for example, a form that grew).

## 4. Checks before anything goes out

- MIDI readback matches the record for every staff of every engraving.
- `consistency.py` passes every check. Add a check for each new designed feature (aimed notes, the turn, a texture's placement).
- Look at the rendered pages of every PDF: spacing, cut-off footers, stray staves, spelling (sharps from the key).
- Every bar number, pitch and chord written in the songbook is read from the record, not remembered.
- References are verified by search. Claim only what the sources say.

## 5. After delivery

1. **The blind pick:** offer the three 10.20 slots in shuffled order as A, B and C. Log his answer and which slot it was, and update the test report's blind-pick record.
2. **The fix list.** Offer to add the song's findings to the cumulative fix list for the other AI. It is always a Doc, and it is always overall: every song since the last spec version, nothing left out. Each fix has **Problem, Evidence, Fix, Check**, numbered in sequence. Also update the songs table, the order of work, the regression line and the blind-pick tally. Send the link.
3. Offer the production package if it wasn't asked for.

## 6. Engraving lessons (LilyPond 2.24)

- `\compressMMRests`; chord-name skips over rests must be a single `s1*n` (or `s2.*n`), or the rests won't compress.
- In 6/8, split durations so nothing crosses the bar's middle beat; dotted quarters at 0 and 3; `\tempo 4. = 54`.
- Spell pitches from the key: sharps for the leading tone in minor keys.
- More than one rhythm on a staff: pack the events greedily into voices (`\voiceOne`, `\voiceTwo`); spacer rests in the lower voices.
- `\RemoveEmptyStaves` plus `\override VerticalAxisGroup.remove-first = ##t` for instruments that rest. Put dynamics only on sounding notes, or the empty staves won't hide.
- Two voices on one staff: `\voiceOne`/`\voiceTwo`. TAB with string numbers: `<d\4 a\3>8`, with `\omit StringNumber` on the Staff. Capo shapes: a second ChordNames line under `\transpose`.
- Drum names: bd, sn, hh, hho, cymr, cymc, cymch, toms, tomfl.
- Read back each staff through a plain `\midi` compile of its tokens, and compare sorted pitches with the record.

## 7. Docs

- Create a Doc with its full markdown in one call when the content is ready. Add later sections with `insert` after a block id. Replace a block with `ifHash` plus `ifRev` from the read that showed it.
- Renaming a Doc isn't available from here. Say so if it matters.

## 8. Helping Jason use the files

- **GarageBand on iPhone:** save the .mid to Files. In GarageBand, open a song, go to Tracks view (the stacked-bars button), set the section to Automatic, then Loop Browser › Files › "Browse items from the Files app". If the file isn't listed, move it to On My iPhone › GarageBand › GarageBand File Transfer. Each MIDI track becomes a Keyboard track. Set the tempo in quarters and pick sounds per track.
