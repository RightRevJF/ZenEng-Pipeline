# Card 2: JSIR (Lee & Jeong, arXiv:2610.15356)

## 1. Citation and copy read
Lee, Sihun & Jeong, Dasaem (Sogang University, Seoul). "JSIR: An Audio-Aligned, Multi-Task Dataset of Jazz Standard Recordings." arXiv:2610.15356v1, submitted 11 Oct 2026. Only v1 exists. Categories: cs.SD, cs.DL, cs.LG, cs.MM, eess.AS. The abstract page has no comments field. I read the HTML full text through WebFetch: sections 1-5 and the bibliography (29 entries). The paper has no appendices. I also read the local repo (`/home/claude/dl/jsir/repo`): the README, `metadata.json`, `lead_sheets.json`, and the CSVs for chords, structure and segments.

## 2. Claim and data
- **What was built.** 267 commercial recordings of 44 standards, 25.6 h of audio. The introduction says "about 29 hours", which contradicts the abstract and Table 1. The repertoire covers the Great American Songbook, blues, and bebop/hard-bop. Every recording has beats and downbeats, chords and sections, all on one beat grid. The paper puts it at 3.7x the audio of JAAH. Audio is not released, only MusicBrainz and YouTube ids.
- **How recordings were chosen.** Candidates came from each standard's MusicBrainz work entry. They were ranked by number of releases, which stands in for prominence, then screened by ear. Each standard kept 4-9 recordings (mean 6.1), from 173 distinct artist credits. The paper does not say what the ear screening checked for. The README fills the gap: recordings were picked mainly for prominence and for following the "canonical" changes. **This is a selection on our outcome variable.** Heavily reharmonised versions were screened out on purpose.
- **Who annotated.** One person, the first author, a jazz musician. The labels were revised over several passes in a purpose-built tool (JSIR-annotator). Beats started from madmom output and were corrected by hand.
- **How the lead sheets were made.** The paper names no fake book, Real Book or iReal Pro. The authors compared lead sheets from several unnamed sources. They then assembled the progression that **the largest number of recordings agree on**. So the "lead sheet" is partly a consensus of the recordings themselves, not an independent written source. Chords are in Harte shorthand. `lead_sheets.json` holds one entry per standard with these fields: `chord_changes` (one string per bar, one token per beat, `%` meaning the previous chord continues), `coda` (8 tunes), `key`, `signature` (43 in 4/4, 1 in 3/4), `tonality`, `tempoclass`, `rhythmfeel`, `composer` and the MusicBrainz work id.
- **How recording chords were made.** The lead-sheet progression was transposed to the recording's key and laid on the beat grid. The annotator then (i) corrected bars where the performance departs from it (turnaround substitutes, tritone subs, alternate changes), (ii) put N where there is no harmony, and (iii) added interludes, vamps and codas. The paper gives no counts for these edits.
- **Agreement checks.** None. There is no second annotator and no kappa. The limitations section admits that chord subjectivity cannot be removed.
- **Licence.** The annotations are CC BY-SA 4.0 per the README. The paper itself states no licence.

## 3. Is the measure from the notes?
Yes, but with a caveat. The labels are an expert's lead-sheet-level reading of what the band plays, written as Harte chords on beats. They are not a note transcription. Passing ii-Vs that one comper plays only implicitly are probably not labelled. The recording labels are also **anchored on the lead sheet**: annotation starts from it and changes only what the annotator judged to depart from it. Both points push recordings to look like the chart.

## 4. Effect sizes / how checked
- **Beats** (Beat This!, 8-fold CV). Adding JSIR raises the downbeat F on external jazz sets from 87.7 to 89.2 (+1.5, 95% CI 0.5-2.6, p=0.03). Most of the gain is on JAAH (+3.0). Non-jazz sets stay within a 0.5-point margin. On JSIR itself, downbeat F goes 86.5 to 90.6.
- **Chords** (Consonance-ACE). Sevenths accuracy on JAAH is 33.7 for the pop model zero-shot, 36.8 trained on JSIR from scratch, and 41.3 for pop then JSIR fine-tuning. On JSIR the same three figures are 23.1, 48.3 and 48.9. The learning curve has not flattened at 217 recordings.
- **Structure** (SongFormer). Boundary HR.5F goes from 56 to 79 once peak-picking is tuned. The majority-label baseline scores 49.
- No human agreement figures are reported anywhere.

**Our pilot on the local files.** I wrote a throwaway script, not one of the pipeline's experiments. A ii-V is a min7 followed by a 7/9/13 chord whose root is 5 semitones higher. I collapsed repeated chords and wrapped the lead sheet from its last bar to its first. Across the 44 standards the mean ii-V share is 0.155 for lead sheets, 0.151 for heads and 0.155 for solos (valid segments only). The lead-to-solo correlation across tunes is 0.99, and lead-to-head is 0.97. The mean absolute per-tune gap is 0.012 for solos. Solo shares beat the lead sheet in 19 of 44 tunes. The largest gains are Summertime (+0.028), There Will Never Be Another You (+0.025) and Blue Bossa (+0.025). The largest losses are Wave (-0.061) and Bye Bye Blackbird (-0.048). Five modal or minor tunes have no ii-Vs at all. Taken at face value, recordings in JSIR do not add ii-Vs relative to the lead sheet. But the anchoring and selection described above make this result close to built in.

## 5. What it says about lasting love and covers
The paper says nothing directly. It is an MIR resource paper. Its prominence proxy (MusicBrainz release count) is close to our covers outcome. That is useful as a cross-check, but within JSIR it is only used to rank candidates.

## 6. Methods or measures it suggests for this pass's experiments
**(a) Lead-sheet ii-V share.** Expand `chord_changes` to beats, replacing each `%` with the previous chord. Parse root to a pitch class and take the quality before any `(` or `/`. Collapse consecutive identical chords. Count transitions between adjacent distinct non-N chords, including the wrap from the last bar to the first, since tunes are played in a loop. ii-V share = (min7 to dominant with (root2 - root1) mod 12 = 5) / transitions. Report two variants as well: one that includes `hdim7` to 7 (minor-key iiø-V), and one that counts `coda` separately or excludes it. The share does not change under transposition, so the key never matters.

**(b) Per recording, heads vs solos.** Turn `structure/<yt_id>.csv` (columns `time,name`) into intervals, each ending at the next onset or at `audio_length`, and keep the label before the `:`. Intersect each head or solo interval with `segments/<yt_id>.csv` (`start,end`; 185 files have one segment, the rest 2-6). Take the `chords/<yt_id>.csv` events (`time,chord`, Harte, possibly with stray spaces; strip them). Add the chord already sounding at the start of each interval and count transitions within that interval only. Pool counts per recording, then average per standard. Pair each standard as solo minus lead and head minus lead. Run a sign test or Wilcoxon over the 44 tunes, and use a mixed model with tune as a random effect if you work at recording level. A finer test is bar-level agreement with the lead sheet. Use `beats/` downbeats from the section start, index bars modulo the form length, and score the share of beats whose chord matches the transposed lead sheet. It is worth also flagging ii-Vs in recordings at bars where the lead sheet has none.

**(c) Join to other charts.** Match `title` (and `composer` and the MusicBrainz work id) against iReal Pro, WJD or JAAH titles. Normalise case, punctuation, a leading "The", "St."/"Saint" and the apostrophe in "Bags'". Check by hand the tunes whose titles clash with pop songs (Summertime, Caravan, Wave). The MusicBrainz work id is the strongest key for joining to cover counts.

**Biases against a "performers add ii-Vs" reading.**
- Recordings were selected for canonical changes, which removes the reharmonised versions that would show added ii-Vs.
- The lead sheet is a consensus of the recordings, so performer habits leak into the reference itself.
- Annotation starts from the lead sheet, an anchoring bias that pulls labels toward zero difference.
- There is one annotator and no agreement figure.
- Labels are at lead-sheet level, so implied passing ii-Vs are missed.
- The recordings are prominent, mostly classic ones. Charlie Parker and Miles Davis lead the artist credits, and later or amateur practice is not covered.
- With only 44 tunes and 4-9 recordings each, power is limited.

Together these mean a null result here bounds the leakage only weakly. A positive gap would still be informative.

**Years.** The paper gives no recording years. `metadata.json` has artist, album, MusicBrainz *recording* ids and YouTube ids, but no dates. Years would have to be fetched from MusicBrainz using the recording id (earliest release date), a separate step.

## 7. Leads
1. Eremenko et al., JAAH, ISMIR 2018 (no DOI shown in the paper). It has audio-aligned jazz chords and can be a second recording-side test set.
2. Pfleiderer et al. (eds.), *Inside the Jazzomat*, 2017 (Weimar Jazz Database). Its solo-level chord changes can be compared with JSIR lead sheets.
3. Durán & de la Cuadra, "Transcribing lead sheet-like chord progressions of jazz recordings," Computer Music Journal 2020. It spells out what level of harmony gets annotated.
4. Poltronieri, Serra & Rocamora, "From discord to harmony," ISMIR 2025. It aligns chord vocabularies across datasets and should help with join step (c).
5. Balke et al., JSD, TISMIR 2022. It gives jazz structure (head/solo) for 340 recordings and could extend the heads-vs-solos split.
