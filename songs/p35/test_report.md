---
title: "The First Wood — Test report (ZenEng v88)"
author: "Words and music: Jason Bryant"
date: "10 November 2026"
---

# The First Wood — test report (ZenEng v88)

This is the engine's record of song 35. It is kept apart from the songbook, which is for musicians only.

**The brief, in the writer's words:**
- Build under ZenEng v88, not v64 plus old lists.
- Run as code every rule for the song's class from fixes 135 to 163 and 173 to 177, and say which ran, which could not, and why.
- Report how many candidates each new gate killed.
- Number new findings from 178, after checking the paper's version.

v88's version row (v122) ends at fix 177. The class tables come from the writer's tables file (zeneng_v88_tables.json, 451,281 bytes, sha256 561355b1…68255), read, not refitted. Where a band in the file and the paper differ at an edge, the paper's band was used.

## Intake

- **Ten questions, one per turn,** each with three pictures, Q0 verbatim with a one-line reading, plus four lyric drafts.
- **Class:** carol (the hymn and concert classes).
- **Speaker:** Joseph.
- **Turn:** the wood: the manger is the first wood to hold him, not the last, and the cross is never named.
- **Title:** "The First Wood."
- **Form:** Common Metre with a two-line refrain whose second line moves and turns. 3/4 at ♩ = 92, F major, SATB and organ, tune C4–D5.
- **Never-say:** a list including the turn's words (cross, nails, Calvary, crucified, tree).
- **The lyric:** four drafts.
  - The writer's notes moved stanza 2 from tender to weighty ("I made no part of trough or child; / I hold them both at once").
  - The refrain's second line now varies.
  - Two crowded lines were smoothed.
  - On a later note, three of the rhymes it called slant (squared/pared, grain/plane, true/knew) were kept as full rhymes, and one echo was moved ("while I have arms to hold").
- **A session miss:** fix 139 asks the form question to print each option's summed bars and its time. Q6 offered the metres without them. The form was later fixed at 104 bars, 3:23.

## The search (melody and bass together)

**The construction.**
- One tune for four stanzas. The declamation is read on every stanza's words: 24 lines.
- Bar rhythms are drawn from the class's 3/4 vocabulary: half–quarter 44%, three quarters 29%, dotted quarter–eighth–quarter 6%, half–two eighths 2.7%. At most one slurred bar per line.
- Notes are drawn from the class's pitch model: R 4, P 3, the major key profile.
- The monotony floor is built into the fill.
- The summit is placed as one designated note (D5 on "first," everything else at C5 or below: fix 165).
- Cadence targets come from the lyric's punctuation: lines 1–3 and refrain 1 half closes, line 4 and refrain 2 full closes (138).
- The bass and the chords are drawn with each tune in one pass (137), with the class's first choices (174):
  - the dominant before the tonic
  - roots falling by fifth
  - inversions where they make the bass move by step
  - the chord held under a held note
- The inner voices are written after (137).

**The run.**
- N 500, seed 20261145.
- **Survivors:** 86 (17.2%).
- **Reproduced exactly** on three runs: 500 built, 86 survivors, the same frozen order 638be4d08765 (fix 145's record: seed, N, code hash 4071eccb06b1, Python 3.13.18, numpy 2.5.3, PYTHONHASHSEED 0, the tables file's hash).
- **The pick:** d99d993b5228 (#1), no hand edits.
  - Composite 0.864 on the hymn calibration: IC 0.67, CMP 0.57, memory horizon 0.51, realness 0.56, fit 1.0.
  - Pitch 2.497 bits a note, against the band 2.02–3.11.
  - Rhythm 1.965 bits, against the 3/4 band 0.68–3.30.

**Deaths (the first gate each build failed, in the order the gates run):**

| Gate | Builds killed |
|---|---|
| harmonize: no chord holds the tune | 28 |
| harmonize: no chord path | 19 |
| congregational interval (tritone or seventh) | 71 |
| monotony (166) | 37 |
| hymn invariant: tessitura | 35 |
| hymn invariant: steps | 17 |
| leaps beyond a fifth (class prior) | 14 |
| hymn invariant: leaps | 11 |
| **sequence legs (148)** | **7** |
| spectral (Table B) | 26 |
| CMP (Table B) | 59 |
| memory (Table B) | 89 |
| surprisal (Table B) | 1 |

**Each new gate, read on every harmonized build** (would fail, whether or not an earlier gate killed the build), and the same gates on a control. The control used the same 500 tunes, harmonized with a bass of chord roots and the outer-voice terms off; 458 could be harmonized.

| New gate | Killed (first) | Would fail (of 453 harmonized) | Control: would fail (of 458) |
|---|---|---|---|
| register: refrain top not below the stanza's (133) | 0 | 0 | 0 |
| cadence arrivals (138) | 0 | 0 | 0 |
| pitch band (153) | 0 | 0 | 2 |
| rhythm band (163) | 0 | 0 | 0 |
| rhythm floor (147) | 0 | 0 | 0 |
| pushed notes (159) | 0 | 0 | 0 |
| sequence legs (148) | 7 | 14 | 23 |
| declamation, last stress (161) | 0 | 0 | 0 |
| outer voices: motion (136) | 0 | 0 | 157 |
| outer voices: parallel perfects (136) | 0 | 0 | 209 |
| outer voices: imperfect consonances (136) | 0 | 0 | 35 |
| key word on a chord tone (134) | 0 | 0 | 0 |
| summit once (165) | 0 | 0 | 0 |

**Spread on the harmonized builds (5th percentile – median – 95th percentile):**

| Reading | Spread | Class figure |
|---|---|---|
| pitch bits | 2.30 – 2.52 – 2.81 | band 2.02–3.11 |
| rhythm bits | 1.85 – 1.91 – 2.05 | band 0.68–3.30 |
| imperfect consonances | 0.51 – 0.61 – 0.72 | — |
| contrary motion | 0.52 – 0.65 – 0.77 | — |
| parallel perfects | 0 – 0 – 0.03 | — |
| bass by step | 0.42 – 0.54 – 0.64 | hymn median 0.42 |

## Fixes 135–163 and 173–177: which ran, which could not, and why

| Fix | Rule | Status | Reading or reason |
|---|---|---|---|
| 135 | outer-voice reading | ran | Imperfect 0.56, perfect 0.41, fourth 0, dissonance 0.02. Contrary 0.65, oblique 0.15, similar 0.18, parallel 0.03. Parallel perfects 0, direct perfects 0. Bass by step 0.53, by fourth or fifth 0.28. Struck together 1.0. Hymn medians: 0.46, 0.41, 0.03, 0.05; 0.44, 0.21, 0.20, 0.10; 0; 0.01; 0.42, 0.34; 0.97 |
| 136 | outer-voice gates, hymn and concert classes | ran as gates | 0 killed. The joint search meets them by construction; the control shows their bite (157, 209 and 35 of 458) |
| 137 | the bass as a line | ran | Drawn with the tune, inversions chosen for steps, inner voices after. Bass by step 0.53 (hymn median 0.42, chorale 0.65) |
| 138 | cadence arrivals by strength | ran as a gate | 0 killed (targets set at the line ends). Lines 1 and 3: G over C. Line 2 and refrain 1: A over F. Line 4 and refrain 2: F over F |
| 139 | the form's length summed | **not done** | A session miss at Q6 (see the intake) |
| 140 | compounds and independent possessives | ran | The stress function, with fix 168's list; no compound of that kind in the lyric; 'mortise' patched (finding 185) |
| 141, 142 | 9.12 from the record, layers by loudness | ran | Introduction 0.39, stanza 1 0.52, stanza 2 0.51, stanza 3 0.41, stanza 4 0.57 (the top, asserted) |
| 143 | the gate names its cause; a capping aim lowers a ceiling first | ran | Every death prints its gate. The summit's ceiling (C5) is set before the walk |
| 144 | the riff off the tonic | not applicable | No riff |
| 145 | the rerun record names the hash seed | ran | Reproduced exactly, three runs |
| 146 | repetition reading | ran | Rhythm recurs in 0.75 of bars (hymn median 0.71). 6 distinct bar rhythms, 4 covering four-fifths (median 5 and 3). Exact repeats 0.21 (0.25). Transposed 0.25 (0). Sequences: one of two legs |
| 147 | the rhythm floor, 38% | ran as a gate | 0 killed (the walk's letter plan repeats rhythms) |
| 148 | sequences of two legs | ran as a gate | 7 killed (14 would fail) |
| 149 | text-setting reading | ran | Word-initial syllables on stronger beats than later ones: 0.76 against 0.63. Initial over later duration 1.47. Melisma 12.5% (5 of 40 syllables), none at a phrase's end. Final lengthening 3.3 times the line's median. 5 of 6 lines start off the downbeat. Summit "first" (ER), a half note, first reached 78% of the way through the tune |
| 150 | melisma and length set by class | **could not set** | The tables file has text-setting rows for pop, standards and Lieder only, none for hymns or carols. The reading is printed and no class target applied (finding 182) |
| 151 | the open-vowel summit, concert classes only | **not applied** | The paper does not say whether a carol is a "concert class" here; 27.23 groups hymn, carol, art song and concert solo together (finding 182). The summit's vowel (ER) is printed |
| 152 | class priors for the walk | ran | R 4, P 3, K_major from the file. Range 14 semitones (C4–D5; class median 12). Leaps beyond a fifth limited to one |
| 153 | pitch band 2.02–3.11 | ran as a gate | 0 killed; built 2.30–2.81 (finding 179) |
| 154 | Phenomenon 3 corrected | nothing to run | A change to the paper's text |
| 155 | originality one-sided for hymns | **could not run** | The flag needs the edge of the most original fifth of 7,494 hymn tunes, and the measure's hymn table. Neither is in the tables file (finding 183) |
| 156 | same-piece calibration before comparing corpora | ran as a constraint | Readings compared only with the hymn tables, except harmony against Bach chorales, v88's own stand-in for hymns (labelled) |
| 157 | pop's rhythm floor withdrawn | not applicable | Pop only |
| 158 | rhythm reading | ran | Onsets on the downbeat 0.44 (hymn median 0.29), other beats 0.51, eighth off-beats 0.04. Pushed 0. Inter-onset intervals: quarter 0.60, half 0.22. nPVI 61.6 (class median 30.2, p95 60.4). 1.88 onsets a bar (class p05 2.07). 0.67 of bars in the 3/4 vocabulary (finding 181) |
| 159 | rhythm by class, pushed-note limit | ran | Bar rhythms drawn from the 3/4 vocabulary. Pushed notes 0 (gate: 0 killed) |
| 160 | a pushed note read against the next chord | ran | No pushed notes, so nothing to read |
| 161 | declamation reading; last stress on a strong beat (gate) | ran | 24 of 24 lines put their last stress on a downbeat (gate: 0 killed). 20 of 24 start before the downbeat. Spans 3–5 bars with the pickup and the held close. The tables file has no 3/4 hymn declamation; the paper's 3/4 rule (the last stress on the downbeat) was used (finding 180) |
| 162 | schema vocabularies by class | **partly** | No 3/4 hymn schema table in the file. Schemas printed: "1 \| 1 \| 1" 9 lines, "1 \| 1 3 \| 1" 4, "1 \| 1 \| 1 \| 1" 4, "1 \| 1" 2, others single. "1 \| 1 \| 1" is the commonest 3/4 schema the paper gives (standards, 14%) |
| 163 | rhythm band (3/4: 0.68–3.30) | ran as a gate | 0 killed; built 1.85–2.05 (finding 179) |
| 173 | harmony reading | ran | 42 chords, 8 distinct, 1.75 a bar. Tonic 0.52 of the time. Sevenths 0.21. Inverted 0.45. Before the tonic: V or V7 11 of 15, IV 3, vii° 1. Roots: falling fifth 23 of 41 moves, rising fifth 5, step 9. Two notes outside the chord, both resolving by step |
| 174 | harmony by class, first choices | ran | Against Bach chorales (v88's stand-in): V before the tonic 0.73 against 0.68; inverted 0.45 against 0.38; 1.75 chords a bar against the chorale's 3.4 and the Lied's 1.6 (finding 184) |
| 175 | pull and distance | ran | Mean pull 0.32 (the classical table). Mean distance from the tonic 3.86 |
| 176, 177 | section harmony, section jobs | not applicable | Pop classes only. v88: "the hymn and concert classes have no sections of this kind" |

Fixes 164–172 belong to the metal class and leads, and do not apply here, with two exceptions: 165 (the summit placed) and 166 (the monotony floor), which ran.

## The arrangement, the demo, the documents

- **The record:** 104 bars, 3:23.5.
  - **Introduction:** the organ plays the refrain.
  - **Stanza 1:** unison, with the organ in four parts.
  - **Stanza 2:** four parts with the organ.
  - **Stanza 3:** four parts, unaccompanied.
  - **Stanza 4:** four parts, full organ, the tune an octave higher in the right hand.
- **Inner voices:** alto B♭3–G4, tenor E3–E4, bass F2–G3. No parallel fifths or octaves between any two voices. Every chord complete; no voicing relaxed.
- **The demo:** choir aahs and church organ. The choir sits +3.8 dB over the organ where both sound. Words are lyric events in the MIDI files.
- **The score** (choir and organ, hymnal layout, 1 page), **lead sheet** (1 page), **parts** (S, A, T, B, organ; 5 pages), **number chart** (1 page).
- **MIDI readback** matches the record on every staff: soprano 45, alto 43, tenor 42, bass 43 notes.

## Findings (from 178; v88 ends at 177)

178. **The new gates kill nothing when the search builds them in, and "0 killed" says nothing about them.** In 500 builds, 12 of the 13 new gates killed no build. The sequence rule killed 7. Each gate is met by construction: the walk draws from the class model the bands are cut from, the rhythms come from the class vocabulary, and the bass is drawn against the outer-voice terms. The control (a root-position bass with the outer-voice terms off) shows the outer-voice gates would bite: motion 157, parallel perfects 209, imperfect 35 of 458. **Proposed fix 178:** every new gate's report includes a control run with its construction switched off, so a gate's bite is measured and not inferred from zero deaths.

179. **The class priors (152) and the surprise band (153) use the same model, so the band cannot bind a walk drawn from it.** Builds read 2.30–2.81 bits in a band of 2.02–3.11, and 1.85–2.05 in a rhythm band of 0.68–3.30. The 3/4 rhythm band's top, 3.30, rests on 47 pieces (4/4: 2.27 on 192). **Proposed fix 179:** state that the bands gate candidates drawn by other means (hand edits, other generators, other classes' priors) and are a reading for the class's own walk; mark the 3/4 hymn rhythm band provisional.

180. **The tables file has no 3/4 declamation or schemas for hymns.** The declamation table holds 4/4 only; it counted 59 3/4 hymn lines but gives no table for them. 161's gate fell back on the paper's 3/4 sentence (the last stress on the downbeat); 162 had no 3/4 hymn vocabulary to draw from. **Proposed fix 180:** add the 3/4 hymn declamation and schemas, or state the fallback.

181. **The class rhythm medians pool metres.** The hymn rhythm medians (243 pieces, 192 in 4/4) put the median at 3.33 onsets a bar and nPVI 30. A 3/4 carol built from the 3/4 vocabulary's commonest bar (half–quarter, 44% of 3/4 hymn bars) reads nPVI 61.6, above the class's 95th percentile, and 1.88 onsets a bar, below its 5th. **Proposed fix 181:** give 158's class figures by metre.

182. **Text setting has no hymn row, and 151's "concert classes" is undefined.** 150 cannot set melisma or length for a hymn or carol: the file has rows for pop, standards and Lieder only. 151 keeps the open-vowel summit "for the concert classes only," while 27.23 names "hymn and concert classes (hymn, carol, art song, concert solo)." **Proposed fix 182:** add a hymn row (melisma rate, length, final lengthening, summit), and list the classes 151 covers.

183. **155's one-sided originality flag cannot run from the file.** It needs the edge of the most original fifth of the 7,494 hymn tunes, and the transition table the measure reads; 27.16 still names the Lakh hits' table. **Proposed fix 183:** add the hymn quintile edges and the hymn transition table to the tables file.

184. **The hymn harmony class stands on Bach chorales, whose chord rate does not fit a congregational carol.** The pick changes chord 1.75 times a bar in 3/4, against the chorale's 3.4 in 4/4. Its inversions read 0.45 against 0.38. v88 notes that hymns have no chord labels. **Proposed fix 184:** a hymn harmony count (a printed hymnal's harmonies), or the class figures in chords a beat, with the chorale marked as a stand-in.

185. **Fix 168's list misses double stresses that are not compounds.** The dictionary gives "mortise" two primary stresses (MOR-TISE); the session added it to the list. **Proposed fix 185:** a word with two primary stresses that is not a compound takes the first, without a list.

186. **The joint draw (137) can choose an outer pair the inner voices cannot complete.** Three draws chose a V7 with the tune on the bass's note, or the seventh in both outer voices; with two inner voices the chord could not be completed or its seventh was doubled. **The run's port:** the harmonizer refuses those pairs, and the bass must sit at least a fifth below the tune. **Proposed fix 186:** 137's joint draw checks, chord by chord, that the inner voices can complete the chord without doubling the leading tone or the seventh.

187. **136 counts only parallel perfects by similar motion; octaves by contrary motion pass.** The pick closes with C5 over C3 moving to F4 over F3, octaves by contrary motion at the final cadence. Kept hymns do this, and the gate is right to pass it. **Proposed fix 187:** print contrary perfects in 135's reading beside the parallel ones, so a reader can see them.

## Blind-pick record

Song 35 (10 Nov): A, "the edges never pared.": the Annotated top (offered as A; B was the Remembered top, C the middle). Through song 35, over 23 picked songs: Annotated top 9, Remembered top 7, middle 6, refrain 1.
