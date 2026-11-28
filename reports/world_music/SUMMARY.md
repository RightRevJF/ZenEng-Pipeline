# World music research: the ten most useful findings

28 November 2026, branch `world-music`. Five passes:
1. rhythm and metre;
2. melody, pitch and psychoacoustics;
3. form and repetition;
4. music as a language;
5. the world's traditions, region by region.

The ten findings below are ranked by how directly each bears on the 3/4 and 6/8 work. Every figure comes from the five reports beside this page, where each claim carries its link and its label. This page has no new figures and is not a result for the engine. The maintainer tests each idea rule first.

Labels: **measured** (a study counted it), **theory** (a published model says it, with no data on that point), **our inference** (worked out here; no source says it).

## The short answer

Music the world over shares one base: beats of 2 and 3, a long note to close a group, a comfortable beat speed, small steps, short repeated phrases. Each style sets its own weights on that base: how hard beat one lands, how often a note comes early, how much a section repeats itself, which pitch it leans on. That's your "one language, many dialects". It fits writing the engine's rules once for every metre, with weights by style.

The dialect layer now has a measured size: listeners from other cultures read the feeling in a voice about 7% less accurately than listeners from the singer's own culture. Rousing against soothing is understood everywhere. Happy against sad only partly, and major against minor not at all, since that's learned.

Music and language share one formal structure that data backs: the grid of strong and weak beats. They don't share a dictionary of meanings, and the brain's language areas don't process music.

The three numbers the engine needs most still haven't been published for 3/4 or 6/8 in any tradition. They have to be counted on the songs the project already holds.

## The ten findings

| # | Finding | Label | Bears on |
|---|---|---|---|
| 1 | Nobody has published how strongly beat one is favoured in triple metre, how often tunes arrive early there, or how many bar rhythms a section uses, in any of the world's traditions. They have to be counted on our own songs. | measured (a gap) | 749.231, .252, .253, .259; K3 |
| 2 | In 3/4, beat three behaves like a lead-in to the next bar: notes cluster there, as in the Viennese waltz, the Norwegian springar, the Arabic waltz rhythm and the run-up to a cadence in Indian music. Stressed syllables may still prefer beat two, but that's open. The borrowed first-beat figure of 0.45 looks reasonable. | measured (timing); theory; our inference | 749.252; K3 |
| 3 | A heavy beat one and arriving early are style choices, not rules of music. In one Indian cycle beat one is the light one. Early arrivals run from almost none in 1800s song to a third or a half of strong beats in rock. They also follow the lyric's language: common in English song, rare in German, Italian and French. | measured | 749.253, .233; K3 |
| 4 | Time should be measured in seconds, not bars. People keep time best at a beat of about 0.6 seconds. A sung phrase lasts about 5 seconds, one breath. Song moves far more slowly than speech, in 20 of 21 societies tested. At song tempos a 3/4 line comes out three to four bars long, and the first-beat rule should depend on tempo. | measured; our inference | 749.226, .243, .256; K3 |
| 5 | In 6/8, the fourth eighth is a second landmark, and the second and fifth eighths are the weakest. The same rhythm sounds more off-beat in 6/8 than in 4/4, so each metre needs its own off-beat range. | measured (small samples); theory | 749.231, .256 |
| 6 | "10 different bar rhythms in 16 bars" and "6 of the 16 bars repeat an earlier rhythm" are one number. A small repeat bonus can't move it; a direct mix of the section's own rhythms with the style table, about 2 to 1, would. Where a drum or text cycle repeats exactly, the melody can vary freely over it. Pop 3/4 has no such cycle, so the melody must carry the repetition itself. The engine's missing rhythm memory is a gap in how it's built, not a setting to tune. | our inference | 749.259, .257 |
| 7 | Across 113 song collections from many cultures, rhythm repeats more than pitch: about 71% of a melody's rhythm against 51% of its pitches. The engine remembers pitch within a section but not rhythm. One check is still due: the main source's song list hasn't been screened for TheSession data. | measured (flagged) | 749.259 |
| 8 | A people's song rhythm barely tracks their speech rhythm (a correlation of about 0.09). So the rhythm tables should come from sung songs of the style, not from the lyric's language. | measured | 749.233 |
| 9 | The 3/4 range problem lies between phrases. A folk phrase spans about 9 semitones and a whole folk song about 12.5. The engine's whole 3/4 tune spans 9, the size of one folk phrase. | measured; our inference | 749.227 |
| 10 | No study counts how much of a song sits on its commonest pitch. Heavy leaning goes with chant and recitation. The home note and the leaned-on note can differ (an Indian raga's main note, a Turkish makam's named note). Short ornament notes inflate a count by notes but not by time. So count by time, by third of the song, and alongside syllable rate. | measured; theory; our inference | 749.226, .255 |

## Also found

- **Call and response, measured for the first time in these passes, by our own count:**
  - leader and chorus alternate in about 64% of sub-Saharan songs and 70% of diaspora songs, against 19% of European songs;
  - the parts overlap in about 45%, 53% and 8%.

  This is our count of the Global Jukebox codes, not a published figure, and it needs redoing rule first. The scripts are in `cantometrics_count/`. Nobody has measured how long a call is against its response.
- **No study ties 3/4 or 6/8 to lullabies or any feeling.** "Lullabies are in 6/8" traces back to a news feature, not a count.
- **The engine's devices already have names in music theory.** The stress rule, early entry, a line sung again and the padded fourth bar each match a preference rule in Lerdahl and Jackendoff. The 4/4 figures left over outside 4/4 (749.256) are those rules' weights, not yet fitted for other metres.

## The first counts to make (cheapest first)

| Count | On | Answers |
|---|---|---|
| Notes and stressed syllables on each beat and eighth, in 3/4 and 6/8, counted separately | Essen, Hooktheory clips, the lead sheets, Lieder | Findings 1, 2, 5 |
| How often a strong beat is left empty because the note came early, by the lyric's language | the same | Findings 1, 3 |
| Different bar rhythms in a section's first 16 bars, against shuffled bars | Hooktheory clips, lead sheets | Findings 1, 6 |
| Time on the commonest pitch, by duration and by third of the song | Essen, Lieder | Finding 10 |

The five reports' testable-idea tables hold the full list, more than 120 rows, with duplicates pointed to rather than repeated.

## Corrections, and what's still to check

- **Correction to the last report:** Hayes and Kaun's 10.9% are lines whose first word comes in late. They don't show that 89% of lines begin with a pickup (749.253).
- **Licence corrections:** the Weimar Jazz Database is ODbL. Cantometrics has a stated conflict, with the stricter reading taken.
- **Figures to check:** most papers were read through a summary tool, so their figures are flagged in each report's source list. Check them before anything is built in.
- **Licences:**
  - Confirmed: OpenScore Lieder (CC0), SANGEET and the raga pitch features (CC BY 4.0), the Meertens songs, SymbTr and the Natural History of Song transcriptions (non-commercial).
  - Not confirmed: Essen, the Hooktheory clips' source, the lead sheets and most world archives.
- **Indigenous song:** nothing sacred, ceremonial, healing or restricted is to be counted. The archives' own protocols say so.
- No TheSession data and no figure from the withdrawn studies was used.
