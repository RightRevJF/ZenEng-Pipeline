---
name: songwrite
description: Write a song with Jason Bryant through ZenEng (the Luthier engine), in any chat window - set up the repo, intake, lyric, melody, demo, scores, songbook, test report, fix list; also porting a new Luthier spec, rerunning songs, and writing by sketch outside 4/4 or in hymn style.
---

# Songwrite: a ZenEng song with Jason

Jason writes songs with ZenEng, his songwriting engine. Another AI (the maintainer) keeps the engine's rules: the spec, a Word file called Luthier, and the cumulative fix list written after it. This skill is how the songs actually get made: the setup in a fresh window, the working method, the tools, the deliverables and the checks. The spec decides *what the engine requires*; this skill decides *how we work*. When they disagree, the newest spec wins, and the disagreement goes on the next fix list.

## Where things stand (16 November 2026)

- **Spec:** Luthier v7 (Module 27.88, Window 164). Luthier v8 is being prepared by the maintainer.
- **Fix list:** the Doc "Luthier fix list for v8 (since v7)", https://claude.ai/artifact/GkotrMu5VoLYJMpnG8UiYQ. It holds 33 findings, 740 to 749.23. The next new finding is **749.24**. When v8 arrives, start a new Doc for findings after it.
- **Everything learned while the engine was offline** (fix list, new rules, metre atlas, every report and study) is on one page, https://claude.ai/artifact/X6p4r6u1b7GiieXsYgjQSW, and in one PDF (`reports/Luthier - everything learned while offline (14-15 November 2026).pdf`). The rules and ranked avenues are also in the Doc https://claude.ai/artifact/MH68uxfVXV8MRuEB1yVBuT.
- **Songs:** folder `pNN` holds song NN−10 (p63 is song 53). The newest songs are 52, The Room Next Door (p62, 6/8, by sketch, three editions), and 53, Sung to Sleep (p63, a 3/4 carol for organ and choir, by sketch, four editions). Next is song 54 in `p64`.
- **Open items:** song 53's blind pick; a one-note change to song 53's refrain re-entry, offered and awaiting Jason; the engine's own reruns of songs 52 and 53 once v8 is ported.

Read the current state at the start of any new window: the fix list Doc (Docs `read`), the last song's `intake.py` LOG and test report. Don't ask Jason for anything written there.

## 0. Before the first question

1. **Get the tools.**
   - Attach the private GitHub repo `RightRevJF/ZenEng-Pipeline` with the repo tool (push access), then clone it to `/home/claude/zeneng-pipeline`. Only if that fails, ask Jason to attach `zeneng-pipeline.zip` and unzip it there.
   - Run `bash setup.sh` from the repo root. It installs LilyPond, FluidSynth with the FluidR3 GM soundfont, pandoc, ffmpeg, music21, statsmodels, the other Python packages, the spaCy models and Playwright's Chromium. It links `lib/carol` and `lib/pop` to `/home/claude/carol` and `/home/claude/pop`, every `songs/pNN` to `/home/claude/pNN`, the metre atlas to `/home/claude/atlas` (tables at `/home/claude/atlas/tables`), and the study scripts flat into `/home/claude/shape` (for `perception.py` and the others), which is where the scripts look for them.
   - It ends with checks. If LilyPond or FluidSynth can't be installed, say so at once: the lyric and melody work still runs, but the engraving and the demo won't.
   - Large research data (Hooktheory, PDMX, Discogs-VI and so on) is not in the repo. The song work doesn't need it. If a study needs it, fetch it again the way its script's docstring says.
2. **Get the rules.** Ask Jason once for the newest Luthier spec (.docx) if it isn't attached. Convert it with Microsoft's MarkItDown into `src/` (never committed), then read the new Window and Module and the rulings on the last findings before intake. Read the fix list Doc for everything since. The data files a spec names are on the tables page (artifact 40f1717e-73ba-43c6-9b36-0f6b991cd360): fetch them with read_file and copy the saved blobs.
3. **Port the new fixes before a new song** (when a new spec has arrived).
   - Port all the new fixes in one pass, with a generator script (`gen_lN_p58.py`) that builds the new engine from the last one. Each patch is asserted to match exactly once, and each fix sits behind an ON flag, so `ZE_PART_LN=0` gives the previous version back. Another song's engine is made from song 48's file by its own generator (`gen_lN_p59.py`).
   - Port checks come before any run. Save a supplied judge exactly as given; never edit or refit it. It must reproduce the picks the paper lists for the earlier runs. Check every new reader against the tables' kept figures until they match.
   - Run a 40-build smoke test first. Then run the songs Jason names, 1,000 main and 1,000 control, at the same seed and designs. The box has two cores, so allow about 12 minutes for four runs in parallel.
   - When a cause is uncertain, instrument the engine (wrap the function, log the failing calls) and trace the cause before writing the finding.
   - Write a port report with one row per fix: its test, the main (control) result, and whether it held. Add the readings the paper doesn't give, by fix number, and new findings numbered from the next free number.
   - **If a fix can't be ported as written, or two fixes conflict, stop and tell Jason before running, naming the fix numbers.**
   - Commit every file a run reads. `trace_opens.py` lists them; check each one is in the repo.
   - Deliver every port: a new fix list Doc (contents in section 5); one Word test report for all the songs run; an intake LOG entry with Jason's message; and the commit, pushed.
4. **Choose the path.**
   - **Engine path:** a song in 4/4 that the ported engine can write (most pop, rock, folk and worship songs). Sections 2 and 3 below.
   - **Sketch path:** a metre the engine can't yet write (3/4, 6/8, 9/8, 12/8, additive metres), a hymn or carol, or organ and choir. Use the song-52 and song-53 sketches (section 2a) until v8 ports metre and hymn mode. Say which path you took at intake.
5. **Start the song.**
   - `bash newsong.sh NN` copies the template into `/home/claude/pNN` (NN is the folder number: song 54 is `bash newsong.sh 64`). The template is old (song 28), so build from the latest song of the same kind instead: `songs/p59` (The World Is Asking: indie folk, every line in two bars) for the engine path; `songs/p62` for 6/8; `songs/p63` for 3/4, hymn mode and organ.
   - Rewrite every song-specific part: the intake LOG, the lyric, FORM, the chords, the voice row and registers, designed notes, the arrangement, and all document text.
   - Patterns elsewhere: p22, duets and 7/8; p23, a band, a riff and a push; p24, guitar with capo and TAB; p40, riff-led rock, two singers and a harmony; p41, a swung shuffle, brushes and sticks, a countermelody.

## 1. Working with Jason

- **One question per turn.** Always three options, A, B and C, with a recommendation where it helps (mark it "(Recommended)"). Never group questions, even where the spec allows it.
- **Show content first, then ask** in plain text, so a question dialog doesn't hide what he needs to see.
- **Concise replies.** He reads on a phone. Lead with the answer. Don't recap steps. He calls himself technically inept: give him one file or one link to pass on, never a set of steps across apps if it can be avoided.
- **Log every choice** in `intake.py`'s `LOG`: the question, the options, the recommendation and his answer, verbatim where he wrote words. This includes choices made after delivery and research requests made in a song's session.
- **Show the lyrics before any music.** Always show the whole lyric, every draft. Take his notes, revise, and show the full revised lyric. The music starts only when he says to lock it.
- **Credit line:** "Words and music: Jason Bryant" on every document.
- **Lyrics and poems:** no punctuation at line ends, plain text (never a code block), as few em-dashes as possible.
- **Editions:** a new edition never overwrites the last. Put its label in every file name, for example "Sung to Sleep (fourth edition) - full score (organ).pdf", and in each document's subtitle and footer, the MusicXML title and the Doc's title. Keep the earlier editions in `out/<label>/`.
- **His documents** (PDFs, Word files, not scores): convert them with MarkItDown before reading.
- **Source material** he attaches (his books, poems) is read, used, and never copied into the repo.
- **No GarageBand MIDI.** He doesn't use it. The full score replaces it.

## 2. The pipeline, one song (engine path)

| Step | Script | Notes |
|---|---|---|
| Intake | `intake.py` | The song's constants: NEVER_SAY, NEVER_PHRASES, WRITER_PHRASES, voice row, tempo and metre, form with its length, key, title |
| Writing room | `w1.py` | Score every line; report the deaths and which lines the writer's lock keeps |
| Lyric | `lyric.py` | The locked lyric, sections, roles, SUNG order |
| Melody | `melody_pNN.py 1000 main\|ctl` | 1,000 main and 1,000 control (243 off), each made twice; the frozen orders must reproduce. Seed 20261113 + 400 + NN, calibration seed + 1, PYTHONHASHSEED 0. Each inside `timeout 590`, one after another, never two at once (a run script in the background is fine). Read the deaths and fix the cause, not the symptom |
| Inspect the pick | by hand | The pick of record is the judge's: `luthier_judge5.pick` over the clean survivors (no soft break). Check it for chant: the longest run of one pitch (kept median 6, 90th percentile 9.5), and each section's repeated notes in its first eight bars. If the pick chants, send Jason both demos, offer a re-pick by the judge's own rule among builds that don't chant, log it as his choice, and put it on the fix list (song 49: e2b80cdc3a1c). Print every line: syllable, pitch, onset, chord, length. Check the line endings, the aimed notes, the ranges, the leaps, the breaths and the joins, and look for scale notes held against a ♭VII chord (F♯ over F). On the default path, take the pick as drawn. Any hand edit is logged and must still pass `evaluate` |
| Research checks | section 2b | Run the offline-research checks on the pick and report them in the test report |
| Record | `build_pNN.py` | One record holds every event (voice, accompaniment, instrumental lines). Every document is written from it |
| Demo | `demo_pNN.py` | MP3 and General MIDI. MIDI tempo in quarters (♩. = 54 is ♩ = 81). ASCII track names. Stems: voice ≥ +3 dB over the band. 9.12 energy arc: each chorus above its verse, the last chorus or bridge the top, the build read where it arrives |
| Lead sheet | `engrave_pNN.py` | Voice, lyric, chord names, cue staves. Read the MIDI back per staff |
| Full score | `score_pNN.py` | Every song. Read the MIDI back per staff |
| Parts | `parts_pNN.py` | Every song: one part per instrument, written from the record (see p20, p22–p24, p30). Strummed guitar as rhythm slashes under the chord names (`\improvisationOn`), picked figures in notes; empty bars compressed; each section mark carries that part's cue; read back per part (slashes by count), drum hits counted |
| Chart | `nashville_pNN.py` | Each section numbered in its own key; band notes |
| Quotable line | `q1020.py` | The three blind-pick slots |
| Songbook | `songbook.md` | See section 3 |
| Test report | `test_report.md` | The engine's record: intake, the melody search (survivors, deaths, orders), the pick, the research checks, the arrangement and documents, the readings the paper doesn't give (by fix number), and findings numbered from the next free number |
| Consistency | `consistency.py` | Every document against the record. Everything must pass before delivery |

## 2a. The sketch path (other metres, hymns, organ and choir)

Until v8 ports metre and hymn mode, songs outside the engine's 4/4 are written by sketch, from the metre atlas's kept tables. Build from the nearest finished sketch:

- **6/8 (song 52, `songs/p62`):** `tables_68.py` (Essen 6/8 tables), `gen68.py` (the melody sketch), `shape68.py` (the song-wide shape), `vary68.py` (varied repeats, 749.8), `harm68.py` (harmony), then build, engrave, score, Nashville, songbook and consistency scripts.
- **3/4, hymn mode, organ and choir (song 53, `songs/p63`):** `tables_34.py`, `gen34.py` and `gen34h.py` (hymn mode against the 3/4 hymn quartiles, 749.11), `harmonize53.py` (four parts with passing notes), `build53.py` (organ by section role, breaths, Module 9.14 voicing with the pedal in its own octave), `engrave53.py` (organ full score with registrations, and an aligned hymn page for the choir), `intensity53.py`, `organ_readings53.py`, `clash53.py`, and `consistency53.py` (62 checks).
- **Other metres:** take bar length, beat groups and kept tables from `tables/metre_atlas` (`atlas.md` says which metre has which source; 9/8 and 12/8 are built from 6/8 per beat; additive metres from their 2+3 groups). Say which tables you used.
- Log at intake that the song is a sketch, and write the test report as the engine's target: the engine's own run should later match or beat it on every check.

## 2b. Rules from the offline research (apply on either path until v8 ports them)

These come from findings 749.4 to 749.23. Check each one on every song and report the readings in the test report:

- **Metre (749.4 to 749.7, 749.15):** rhythm tables per felt metre from sung tunes; one pitch table serves all metres. English stress on strong beats per metre and per style (hymns, art songs and lead sheets differ; popular song syncopates more).
- **Hymn mode (749.11 to 749.13):** charge a hymn tune against the hymn quartiles, not the folk ones; four parts move with the tune about as real hymns do, with passing notes in the inner voices.
- **Accompaniment by section role (749.14, 749.16):** a texture plan by section, measured against the Lieder accompaniment tables (`tables/metre_atlas/accompaniment_lieder.json`); repeats that share printed bars are varied by registration.
- **One song-wide intensity curve (749.17):** the high point at 0.65 to 0.85 of the song as performed, a short release after it, each return above the one before.
- **Surprise against expectation (749.18, 749.20):** the sung line's melody, chord and rhythm surprise at or below the popular-corpus median; spend surprise where the context is settled.
- **A breath, then a fresh re-entry (749.19):** thin the melody for a beat or two before the best moment and re-enter on a less expected note, at about 0.55 to 0.60 of the song (Luthier's Window 2, confirmed by listeners).
- **Perception checks (749.21):** `perception.py` (in `/home/claude/shape`): Module 9.14's low-interval limits (no second below C4, no third below F3), the accompaniment above the sung tune at most 2% of the time, choir crossings, and phrase lengths of 2 to 6 seconds (8 at most).
- **Two channels (749.22):** audiences reward predictable lines; musicians reward harmony that moves within sections and melodies with room in them. Keep the sung line on the audience side and the harmony and accompaniment on the musician side.
- **Chromatic harmony (749.23):** a style choice, not a default. Pop keeps Luthier's departure budget. Hymn mode: one or two applied dominants a verse (V/V, V/vi, V/ii, about 2% to 4% of chord changes) cost nothing; mixture under 2%. Chorale and art-song styles live in chromatic harmony (chromatic chords in about half of 8-bar spans).

## 3. Deliverables

1. **Demo:** MP3, plus a General MIDI file.
2. **Lead sheet** (PDF). **Full score** (PDF), every song. **Nashville chart** (PDF). MusicXML of the lead sheet and the full score. For organ and choir: the organ full score with registrations and the choir's hymn page, both from one record.
3. **Songbook and production notes**, as one document, delivered as a Doc and as Word (`pandoc --reference-doc=/home/claude/carol/songbook/ref.docx`). It is for musicians only: **no engine terms at all** (no module numbers, scores, fingerprints, certificates or version numbers). It contains:
   - at a glance, the form, what the song is about, and how to play it;
   - section by section: chords beside each line, with melody notes that give real bar numbers and pitches;
   - for each player, for the singer, and the arrangement;
   - the production notes at the end: a lyric sheet with bar numbers; then a **producer one-sheet** on its own printed page (page breaks before and after it in the Word copy), in five blocks: the emotional target (two sentences), the three references (one line each on what to take), the dynamic arc (a table of section, bars, level and what changes, with any silences or anchors), the non-negotiables (one line each), and the mix priorities (what sits where, and what must never be covered); then the production brief (the song, three references checked by a live web search, non-negotiables), session notes (tempo and click, key, chords per bar, range, tracking, blend and panning, any part one player can't play at once recorded as its own pass), and the score and parts list. Check in the rendered Word copy that the one-sheet fits one page.
4. **Parts PDF**, every song: one engraved part per instrument, each with a short note on its role, rehearsal marks with cues, bar numbers and chord symbols. List it in the songbook's score-and-parts section.
5. **Test report** (Word, the same pandoc reference doc), kept separate: the engine's record and the numbered findings.
6. Send every file with SendUserFile, plus the Doc link. Then one line on what changed or what to know (for example, a form that grew).

## 4. Checks before anything goes out

- MIDI readback matches the record for every staff of every engraving.
- `consistency.py` passes every check. Add a check for each new designed feature (aimed notes, the turn, a texture's placement, a breath), and check that the songbook and its Word copy carry the producer one-sheet.
- The research checks of section 2b are run and reported.
- Look at the rendered pages of every PDF: spacing, cut-off footers, stray staves, spelling (sharps from the key).
- Every bar number, pitch and chord written in the songbook is read from the record, not remembered. That includes prose: a sentence saying where a line enters, which note a word lands on, or where a note outside the scale falls is computed in `songbook_pNN.py`, so a new pick can't leave stale claims behind. The lyric sheet gives each line's slot bar and marks pickups, for example "5 (pickup in 4)".
- References are verified by search. Claim only what the sources say.

## 5. After delivery

1. **The blind pick:** offer the three 10.20 slots in shuffled order as A, B and C. Log his answer and which slot it was, and update the test report's blind-pick record.
2. **The fix list.** Offer to add the song's findings to the cumulative fix list for the maintainer.
   - It is always a Doc, and it is always overall: every song, port test and research finding since the last spec version, nothing left out. Until v8 arrives, add to "Luthier fix list for v8 (since v7)" (next number 749.24).
   - Each fix has **Problem, Evidence, Fix, Check**, numbered in sequence.
   - It also carries: the songs table, the port's tests (fix, result, held?), the order of work, the regression line (frozen orders, the checks that must hold), reports, readings the paper doesn't give, and the blind-pick tally. Keep the running total and the opening summary current.
   - Commit a markdown copy to the repo (`songs/pNN/fixlist_vNNN.md`) and send the link.
3. **Made for real.** The first delivery is the engine's test, on the default path. If Jason likes the song, offer a real-song rerun. Ask design questions one at a time:
   - the hook's high point (pitch, word, beat, chord);
   - where the verse sits in the voice and how far the chorus lifts;
   - the rhythm feel (for example, eighths only in a shuffle);
   - the song's peak, and how the last line comes home.

   Then build them into a design copy of the search (`melody_pNNd.py`) as named design gates, and run it twice. Choose by ear from the shortlist, giving reasons against two others. Rebuild everything as `_d` files in `out_d`, with an edition label in every file name (section 1).
4. Offer the production package if it wasn't asked for.
5. **Handing work to the maintainer:** Jason wants one thing to pass on. Rebuild the single PDF (`reports/build.py`) or the single web page (`reports/build_web.py`, published as an artifact) when the fix list or the reports change, and tell him that the page is private until he shares it.

## 6. Git, data and ethics

- Push to `RightRevJF/ZenEng-Pipeline`: `songs/pNN`, `studies/`, `reports/`, `research_notes/`, `tables/metre_atlas`. Never commit `out/`, `src/` or `.pkl` files (the pop calibration in `lib/pop` is the exception). End commit messages with the attribution lines the session gives.
- Before every commit, grep the staged files for "AIza" (a Google API key). Jason's YouTube Data API key is never written to the repo, memory or any document; if a study needs it, ask him for it and keep it in `/root/.secrets/youtube_key` (chmod 600).
- YouTube: keep only aggregates and results, never comment text, usernames or raw statistics; never download audio.
- Don't bypass bot shields or blocked sites (hymnary.org). Use SecondHandSongs only through its published research list. Don't use The Session's data (its licence bans processing by AI). Record each source's licence with its tables.

## 7. Engraving lessons (LilyPond 2.24)

- `\compressMMRests`; chord-name skips over rests must be a single `s1*n` (or `s2.*n`), or the rests won't compress.
- In 6/8, split durations so nothing crosses the bar's middle beat; dotted quarters at 0 and 3; `\tempo 4. = 54`.
- Spell pitches from the key: sharps for the leading tone in minor keys.
- More than one rhythm on a staff: pack the events greedily into voices (`\voiceOne`, `\voiceTwo`); spacer rests in the lower voices.
- `\RemoveEmptyStaves` plus `\override VerticalAxisGroup.remove-first = ##t` for instruments that rest. Put dynamics only on sounding notes, or the empty staves won't hide.
- Two voices on one staff: `\voiceOne`/`\voiceTwo`. TAB with string numbers: `<d\4 a\3>8`, with `\omit StringNumber` on the Staff. Capo shapes: a second ChordNames line under `\transpose`.
- Organ: right hand in two voices where an inner line moves; registrations in their own voice above the staff; the pedal written in its own octave.
- Drum names: bd, sn, hh, hho, cymr, cymc, cymch, toms, tomfl.
- Read back each staff through a plain `\midi` compile of its tokens, and compare sorted pitches with the record.
- A male voice is written an octave up on `\clef "treble_8"`, with the record at sounding pitch. Say so on the lead sheet.
- Swing: write straight eighths under a swing mark: `\tempo \markup { "Shuffle" \concat { "(" \rhythm { 8[ 8] } " = " \rhythm { \tuplet 3/2 { 4 8 } } ")" } } 4 = 96`. Swing only in the demo's playback (an offbeat eighth at two-thirds of the beat), never in the record.
- Brush and stick drums on one channel: change the program on channel 10 (brush kit 40, standard 0) where the record's bar says.
- Join the parts book's bookparts with real newlines, not a literal \"\\n\".

## 7a. Lessons from songs 40–41

- **Long lines and slots.** Fix 308 needs two bars for any line of 9 or more syllables, and 230's default gives such a line four. Count the syllables of the locked lyric against the form before the melody. If a section can't fit, ask Jason one design question: grow those sections, follow 230's default, or trim words.
- **The verse's place in the voice decides the song's register.** The paper doesn't give it (finding 314). On the default path, say what you set. On a real song, ask.
- **A designed word is struck on its own note.** Drop the melisma on a designed final syllable, and cap the walk below the designed top, so the design is the line's top.
- **No sixteenths, with one-bar slots for 7–8 syllables, needs a quicker breath** between those lines (a beat instead of 1.5). Name it as a design consequence.
- **Instrument ranges.** Check every instrumental line's range. The solo's octave repair can climb out of the guitar (finding 319).
- **The bridge opening.** In a design run, expect deaths at the bridge-opening gate and the judge's floor; read the shortlist by ear.

## 8. Docs

- Create a Doc with its full markdown in one call when the content is ready. Add later sections with `insert` after a block id. Replace a block with `ifHash` plus `ifRev` from the read that showed it. Update payloads take the form {"ops": [...]} with engine "prose".
- To rename a Doc, call update with ref {object: project, id} and no container, with payload {kind: "patch", patch: [{op: "set", path: ["name"], value: "..."}]}. Rename its heading as well. For a new edition, create a new Doc with a version label in its title.
- A find target must be the words as they read inside one block, never across table cells, and without markdown markers. For a cell, read the table with `view` and `parentId`, then replace the cell's paragraph by id with `ifHash` and `ifRev`.
- A Doc exported as PDF or long markdown arrives as a saved file you can decode; a short export comes back inline. To turn a Doc into text for a page or a merged file, export it as PDF and convert it with pymupdf4llm.
