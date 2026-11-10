---
title: "Swallowed Up — Test report (ZenEng v78)"
author: "Words and music: Jason Bryant"
date: "10 November 2026"
---

# Swallowed Up — test report (ZenEng v78)

This is the engine's record of song 34. It is kept apart from the songbook, which is for musicians only. The test was the writer's choice: the new heavy metal class (Module 9-M, v75), in the preset that departs furthest from what the engine does. The writer asked for "the toughest to nail." The song also ran v76's gate rules (fixes 132–134) and v78's fixes 139, 140, 141, 142, 143 and 145 where they apply.

## Intake

- **Ten questions, one per turn, each with three concrete pictures** (v43 fix 5.2), plus two lyric drafts. Every answer is logged verbatim, with a one-line reading beside it (Q0 verbatim, fix 5.5).
- **Q1:** the writer asked for the hardest preset and got the answer **5 Death** (9-M.2's order): growled throughout, so the voice has no melody search (9-M.10a); chromatic riff chains; blasts and the slowdown.
- **Q2:** straight death (MELODIC off). SCENE aim, by implication.
- **Q3:** a graveside burial, with the CHRISTIAN overlay (9-M.8).
- **Q4:** the speaker is the minister at the grave, a fighter against death (the overlay's combatant).
- **Q5:** stance from lament to defiance (9-M.8's dial, kept apart from heaviness).
- **Q6:** the title "Swallowed Up" (a participle, 9-M.8).
- **Q7:** ♩ = 200, with the slowdown to ♩ = 100; tuned to B.
- **Q8:** form option C, 152 bars, 3:22. The form question printed sums and times computed from the parts (fix 139, run: the option lengths 128, 88 and 152 bars were summed at print, and intake.py asserts the chosen plan).
- **Q9:** never-say list A.
- **Q10:** the man in the box is the speaker's own father.
- **The lyric:**
  - Draft 1 drew three notes: verse 3 was sermon, not scene; some lines were too smooth to growl; the chorus's middle lines explained too much.
  - Draft 2 rewrote verse 3 at the edge of the hole, cut the smooth lines short, and made the chorus "Clay jaw. Stone throat." The writer locked it.

## The class, run as code

**The riffs, written and frozen first (9-M.4).**
- Eight riffs (A, B, B′, C, D, E, F, G), the count for a long song, frozen as 7f7d89c5e09d before the voice or the solo was placed. The voice and the solo record the frozen riff's hash, and the build asserts they match.
- The tonic is the low open string (B1).
- Pedal plus accents: the open accents fall on ♭5, 4, ♭2, ♭3, ♭6 and 5.
- **Terminal modifications** on every fourth statement:
  - riff A: G F♯ F C (♭2 to 1)
  - riff B: G to F♯ (♭6 to 5)
  - riff C: F E C (♭2 to 1)
- Death's shifting centres: riff B′ moves riff B up a half step for verse 3's first eight bars.
- The solo's loop is i–♭VII–♭VI–V, from the cells on file.
- Every intro bar sounds (fix 144, asserted).

**The feel ladder (9-M.5, Table BY).**
- The intro enters in layers.
- The riff, verses and solo are double time (snare on the "and" of each beat), with the kick taken from the guitar's rhythm (Death).
- The choruses are the blast (snare on the odd sixteenths, kick on the even).
- The slowdown is a true halving of tempo, in half time. A beat of silence follows (bar 120, asserted): 9-M.5's gap of at least a beat.
- The breakdown is in quarter time: unison strokes in the low register, silence between, and the cymbal thinning (china on every stroke, then on the first stroke only, then crash, then none).
- Pairings kept: pedal riffs with double time, tremolo with the blast, long chords with half time, the breakdown with china.

**Form (9-M.6).**
- A buildup intro, a pre-verse (the verse riff alone), three rotations, a bridge carrying the solo and the slowdown with the breakdown, a re-intro, and the return.
- This is compound AABA with a third rotation, as the writer chose.

**The voice (9-M.7), placed, not searched.**
- 301 strokes. Families and registers:
  - verses: a low growl
  - the choruses and the taunt: a mid shout (the intelligibility budget: the title, the hook and the taunt go to the voice that can be understood, are repeated, and are printed)
  - the last "Swallowed up!": a high fry scream
- Each line takes two bars and ends with a breath before the cycle ends (asserted). Every stressed syllable falls on a beat or one of the guitar's open accents (lock 1.00). In the breakdown, every stressed syllable sits on a unison stroke.
- **Vowel shape:** the growl darkens its stressed vowels toward back vowels, opens at the emphatic word (the content word on the strongest hit) and darkens at the line's end. The shout keeps the words' own vowels. The scream brightens.

**The solo (9-M.10a), the only search.**
- **The search:**
  - N = 500, seed 20261144.
  - 42 survivors (8.4%).
  - **Rerun: reproduced exactly**, order frozen b644ed162840 both times (fix 145's record: the seed, N, code hash 2a8b7700725f, Python 3.13.18, numpy 2.5.3, PYTHONHASHSEED 0, the frozen riff's hash).
- **Deaths:**
  - monotony 169
  - the design clause THE SUMMIT ONCE 126
  - range 69
  - leap 65
  - fewer than four pitches in a phrase 29
- **Gates:**
  - range B3–B5
  - leaps of an octave at most
  - bar downbeats on chord tones in at least 40% of bars (fix 134's floor, read on the lead)
  - THE SUMMIT ONCE, in phrase 7 (declared by the design: fix 133's rule that a design clause binds when declared)
  - a cadence onto A♯ or F♯ over F♯5
- **Not applied:** the tritone filter, the consonance and spectral gates (9-M.10b). Realness prints OUT OF CALIBRATION and ranks nothing.
- **Pick:** 7b3e247237eb (#1), no hand edits.
  - composite 0.574 (IC 0.356, CMP 0.418, memory horizon 0.686)
  - chord-tone downbeats 0.88
  - realness 0.383, out of calibration
  - summit B5 once, bar 110
  - range D4–B5, ending A♯4 in bar 112

**The register gate (9-M.10c).** The voice is harsh throughout, so the plan was read on section energy, with the breakdown allowed as the summit.

**The outer voices (27.23, v77), printed, gating nothing (the metal class).** On the solo against the bass (8 bass moves):
- imperfect consonances 0.38, perfect 0.62
- contrary motion 0.57, parallel 0.29, similar 0.14
- one parallel perfect

**Heaviness (9-M.10d), reported, not scored.**

| Section | Onsets/s | Kick/s | Snare/s | Palm-muted unison | Distortion cost |
|---|---|---|---|---|---|
| Verses | 9.17 | 8.75 | 3.33 | 0.64 | 3.58 (verse 3: 3.49) |
| Choruses | 13.33 | 6.67 | 6.67 | 0.00 | 4.75 |
| Solo | 10.00 | 10.00 | 3.33 | 0.67 | 2.80 |
| Slowdown | 1.85 | 1.30 | 0.31 | 0.00 | 7.04 |
| Riff 2 | 7.50 | 5.00 | 2.50 | 0.35 | 3.94 |
| Outro | 5.10 | 4.69 | 1.67 | 0.40 | 5.47 |

The harsh-voice flag is on in every section with a voice.

**Energy (9.12 on 9-M.5's terms, from the record (fix 141), layers summed by loudness (fix 142)).**

| Section | Energy |
|---|---|
| Intro | 0.23 |
| Riff | 0.63 |
| Verses | 0.66 |
| Choruses 1–3 | 0.87 |
| Solo | 0.73 |
| Slowdown | 0.44 (the breakdown marked as the peak, 9-M.6) |
| Riff 2 | 0.55 |
| Last chorus | 0.90 (the top, asserted) |
| Outro | 0.52 |

Each chorus reads above its verse (asserted).

**Vocabulary (9-M.8).**
- Verses: type-token ratio 0.67 pooled (per verse 0.80, 0.79, 0.75), against Death's target of about 0.66.
- Rare words: 2.7%, 6.0% or 13.1% of verse tokens, at Zipf below 3.0, 3.5 or 4.0. The target is about 20%, but the module does not say what counts as rare (finding 154).
- The love-song machinery was off. The overlay's lexicon was kept dark (fire, body, death, the numinous), the enemy is death, and the imagery comes from 1 Corinthians 15, Proverbs 30 and Genesis 4.

**The demo (9-M.9).**
- The two guitars are rendered apart: about 10 ms and +6 cents, hard left and right. Palm mutes are short notes.
- Snare backbeats 115–120. Blast snares 125–127, with 84 of 256 at 127 (never every stroke).
- Quantised to about 90%. Reverb CC91 at 8 in the blasts.
- The voice is a stand-in (finding 151), +4.0 dB over the band where it sounds. The demo runs 3:24.

## Documents

- **Lead sheet** (2 pages): the voice on a three-line staff with cross noteheads at three heights, the technique boxed at each change, the words beneath, power-chord names, and each section boxed with its riff and feel. MIDI readback: 301 of 301 strokes match.
- **Parts** (21 pages): guitars (tuning at the head, P.M. spans, open strokes accented), lead, bass, drums, voice. Readback matches for all four pitched or drum parts: guitar 2,943 notes, lead 255, bass 1,511, drums 2,550.
- **Number chart** (1 page), in B minor.
- **Songbook:**
  - written to the producers' four targets (impact, energy, precision, extremity), with where the song sits between naturalistic and hyperreal
  - three references checked by search: Death, "Pull the Plug" (1988); Suffocation, "Infecting the Crypts" (1991); Mortification, "Scrolls of the Megilloth" (1992)
  - the plain statement that the demo is a reference for rhythm, form and the lead's pitches, not for tone
- **Not run this song:** v76's writing room (10.11, twelve candidates by named moves) and v78's blend report (10.14). The engine's own word vectors are not in the pipeline repository. The lyric was drafted and revised by hand over two drafts.

## Findings (numbered from 146; v78's last fix is 145)

146. **9-M.10a hands the lead to the search but gives it no gates or ranking.** Module 27's composite, its floors and its calibration stand on sung lines over pop or hymn corpora. Song 34's solo had no syllables and no corpus. **The run's port:** gates on range, leap, chord tones on downbeats (134's floor), the declared summit and a cadence; the composite from IC, CMP and the memory horizon (0.35, 0.35, 0.30); realness printed out of calibration. **Proposed fix 146:** 9-M.10 states the lead's gates and composite, and names the corpus a lead calibration needs.

147. **The design clause THE SUMMIT ONCE kills most lead builds unless the plan builds the summit.** In the first run, 219 of 500 died at it. With every phrase but the seventh held below E5 (fix 143's way: the ceiling lowered so the clause is met by construction), 126 still died, because a sixteenth-note phrase strikes its own top note more than once. **Proposed fix 147:** where a summit is declared, the plan places it as one designated note and caps the rest of its phrase a step below.

148. **No monotony floor for an instrumental fill.** v77 built a monotony floor into the sung fill. Song 34's first solo build had runs of twelve identical notes, from the walk clamped at the range's edge. **The run's port:** no pitch more than three times running, and at least four pitches in each phrase but the cadence. **Proposed fix 148:** the monotony floor applies to every searched line, sung or played.

149. **9-M.7's lock is empty when the kick comes from the guitar, and the placement has no stated method.** "Strokes lock to the kick and the guitar's accents." But Death derives the kick from the guitar's rhythm, so in the verses the kick strikes on 11 of 16 sixteenths and any placement is "locked." **The run's port:** a placement that puts stressed syllables on the guitar's open accents or the beats and weak syllables on eighths, a breath before the two-bar cycle ends, and, in the breakdown, stressed syllables on the unison strokes. Lock 1.00. **Proposed fix 149:** 9-M.7 defines the lock on the guitar's unmuted accents and the beats (never on a derived kick), and states the placement procedure.

150. **Fix 140's compound rule cannot find compounds by itself.** The dictionary double-stresses Sunday, backhoe and everything. Separately, "like" as a preposition and "you'll" read strong. **The run's port:** a list. **Proposed fix 150:** 28.12's compound test is the dictionary's double stress on a closed (unspaced) word, checked against a compound list. A preposition "like" is weak.

151. **9-M.9's harsh-voice placeholder, "an unpitched placeholder on three keys," does not sound like a voice in an MP3.** **The run's port:** the MIDI files keep the three keys (C3, G3, D4) with lyric events. The MP3 renders each stroke as noise and a rough buzz through the formants of its target vowel, darkened for the growl and brightened for the scream, so the voice's rhythm, height and vowel shape can be heard. **Proposed fix 151:** 9-M.9's demo renders harsh lines this way, still a DEFAULT to be checked by ear.

152. **9-M.5's section energy names five terms and no weights.** These are feel, kick density, cymbal, riff type and layers. **The run's port:** 0.30, 0.20, 0.15, 0.15, 0.20, with feel ranked on the ladder. **Proposed fix 152:** 9-M.5 states the weights, or 9.12 prints the five terms and ranks on none.

153. **9-M.10d's distortion cost does not state its low-register penalty.** **The run's port:** ratio complexity (log₂ of the ratio's product) × gain (1.0) × (1 + (48 − the lowest note) / 12 below C3). **Proposed fix 153:** state the penalty.

154. **9-M.8's vocabulary targets cannot be computed as written.** "Rare" has no threshold, and the type-token ratio has no window. Song 34's verses read 0.67 pooled or 0.75–0.80 per verse. Rare words read 2.7%, 6.0% or 13.1% at Zipf below 3.0, 3.5 or 4.0. **Proposed fix 154:** state Kahraman 2020's definition of a rare word and the TTR window, or mark both as DEFAULT.

## Blind-pick record

Song 34: (pending).
