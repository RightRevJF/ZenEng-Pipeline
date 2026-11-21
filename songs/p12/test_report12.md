# Wood and Cloth (second edition): test report

21 November 2026. Song 12, rewritten on the sketch path (a 3/4 hymn; Luthier does not yet write 3/4 or hymn mode). Words and music: Jason Bryant. Every choice is logged in `songs/p12/intake.py`.

## What changed from the first edition (4 November)

- **Words.** Five lines rewritten after the writer's review and an outside review: 1.2 "Maker small enough to tend," 1.3 "wood would hold him, raised for dying," stanza 4 new (the king and the crown of thorns), 5.2 "stone rolled back and none to find." 2.4 and 3.3 kept at the writer's choice. Joseph kept, with scripture notes on the hymnal page.
- **Tune.** New, in D major (was C), A B A C (line 3 repeats line 1), E5 once on "cloth," a recurring figure of two even dotted quarters (bars 5, 7, 13), final cadence C#5 to D5 (was B4 A4 C5).
- **Harmony.** Two applied dominants a stanza (E7 bar 7, F#7 bar 10); stanza 4 its own setting with G minor 6 (bar 14) as the one borrowed chord; stanza 5 the organ's own harmony with a descant.
- **Documents.** New organ score with choir (88 bars, registrations); hymnal page, lead sheet, MusicXML, demo; no engine terms on any page.

## Mouth tests (locked lyric)

No unstressed syllable on a strong position in any stanza; 87 87 exact. Heavy monosyllables on weak positions (2.4, 5.2, 4.2, 3.1), given even notes. Close vowels on held syllables ("lin-en," "Ju-dah," "sleep-ing"), singable at a hymn's pace. Joins of four consonants: "and cloth," "against the," "friends would." The room check did not run (749.151).

## The tune

`gen12.py 3000`, seed 20261113 + 412: 2630 of 3000 built survive (87.7%). Judge's pick 2c26d99ebe1c (charge 0.406); chosen by ear instead build 1060 (charge 0.406, the same least charge): the pick's line 1 stays in D4 to F#4 and line 3 repeats it (749.149). Readings of the chosen tune against the 3/4 hymn quartiles:

| Reading | Value | Kept quartiles | Inside |
| --- | --- | --- | --- |
| repeated notes | 0.182 | 0.14 to 0.213 | yes |
| moves by step | 0.606 | 0.487 to 0.618 | yes |
| moves by leap | 0.091 | 0.067 to 0.111 | yes |
| turns of direction | 0.423 | 0.337 to 0.456 | yes |
| range | 14 | 12.0 to 14.0 | yes |
| distinct pitches | 9 | 7.0 to 9.0 | yes |
| longest run of one pitch | 3 | 2.0 to 3.0 | yes |
| distinct rhythms over bars | 0.312 | 0.156 to 0.318 | yes |
| notes a bar | 2.125 | 2.118 to 2.66 | yes |
| onsets on the beat | 0.853 | 0.84 to 1.0 | yes |
| onsets on the bar's first beat | 0.324 | 0.359 to 0.446 | no |
| gaps of a sixteenth | 0.0 | 0.0 to 0.0 | yes |
| gaps of an eighth | 0.061 | 0.0 to 0.238 | yes |
| gaps of a quarter or more | 0.939 | 0.742 to 1.0 | yes |
| notes a beat | 0.708 | 0.706 to 0.887 | yes |
| gaps of half a beat | 0.061 | 0.0 to 0.238 | yes |
| gaps of a third of a beat | 0.0 | 0.0 to 0.0 | yes |
| gaps of a beat or more | 0.939 | 0.742 to 1.0 | yes |
| gaps under a third of a beat | 0.0 | 0.0 to 0.0 | yes |

The one reading outside, onsets on the first beat, follows from the design: the even dotted quarters put onsets off the beat.

## The four-part settings

Song 53's beam search (`harmonize12.py`), downbeats locked to the plans, with two costs added for the low-interval limits (749.150). Costs: hymnal 34.2, stanza 4 32.0, stanza 5 36.4. Parallels after the search: {'hymnal': [], 'stanza4': [], 'stanza5': []}; hand edits: ['stanza 4 bars 14-15 voiced by hand: bass G2 G2 A2 A2 (was G2 B-flat2 C-sharp3, an augmented second), tenor B-flat3 to A3'].

## Research checks (749.4 to 749.23)

- **Metre and stress:** every stressed syllable of every stanza on a downbeat.
- **Hymn mode:** charged against the hymn quartiles; four parts with passing notes in the inner voices.
- **Accompaniment by section:** full (stanzas 1–2), manuals only (3), silent (4), link, full organ (5).
- **Song-wide intensity:** peak at 0.97 of the song (descant G5 over "cloth," bars 85–86), late against 0.65–0.85 by design (749.148); release in stanza 4 (0.60–0.77); fresh re-entry at bar 69 (0.78).
- **Chromatic harmony:** two applied dominants in 16 bars a stanza; one borrowed chord in 88 bars (about 1%).
- **Perception:** no third below F3 or second below C4 in the choir; 23 samples where the men's unison tune meets the organ bass in stanza 5; organ above the tune 0%; no choir crossings. Phrases 7.2 seconds (a line of four bars at ♩ = 100), above 6 and under 8.
- **Surprise against expectation:** not measured on this path.

## Consistency

53 of 53 checks pass (`consistency12.py`).

## Findings (running tab, fix list for v45)

749.148 the peak band and hymns with a last-stanza descant; 749.149 the hymn judge reads no line shape or tessitura; 749.150 the four-part search: augmented seconds, low intervals, parallels across a melisma; 749.151 the room check cannot read a hymn.
