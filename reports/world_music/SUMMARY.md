# World music research: the ten most useful findings

28 November 2026, branch `world-music`. Ranked by how directly each one bears on the 3/4 and 6/8 work. Every figure comes from the three reports beside this page, where each claim carries its link and its label. This page has no new figures and is not a result for the engine. The maintainer tests each idea rule first.

Labels: **measured** (a study counted it), **theory** (a published model says it, with no data on that point), **our inference** (worked out here; no source says it).

## The short answer

Music the world over shares one rhythm base: beats of 2 and 3, a long note to close a group, and a comfortable beat speed. Each style sets its own weights on that base: how hard beat one lands, how often a note comes early, how much a section repeats itself. That's your "one language, many dialects", and it fits how the engine's rules should be written: once for every metre, with weights by style.

The three numbers the engine most needs haven't been published for 3/4 or 6/8. We'll have to count them on the songs we already hold.

## The ten findings

| # | Finding | Label | Bears on |
|---|---|---|---|
| 1 | Nobody has published how strongly beat one is favoured in triple metre, how often tunes arrive early there, or how many bar rhythms a section uses. They have to be counted on our own songs. | measured (a gap) | 749.231, .252, .253, .259; K3 |
| 2 | In 3/4, the borrowed first-beat figure of 0.45 looks reasonable: carried over from German folk songs in 4/4, it comes out at 0.40 to 0.49. Beat three probably works as a lead-in to the next bar more than beat two does. | our inference | K3; 749.252 |
| 3 | A heavy beat one and arriving early are style choices, not rules of music. In one Indian rhythm cycle (rupak), beat one is the least filled: split into smaller notes about 28% of the time, against over 95% for the other main beats. Early arrivals run from almost none in 1800s song to a third or a half of the strong beats in rock. | measured | 749.253; K3 |
| 4 | People keep time most easily at a beat of about 0.6 seconds. Rules should follow the beat nearest that speed. Slow 6/8 pop is partly felt in eighth notes, so the first-beat rule should depend on tempo. | measured; our inference | K3; 749.256 |
| 5 | A sung phrase lasts about 5 seconds, one breath, in songs from many cultures (4.5 seconds in Western songs, 6.2 elsewhere). At song tempos, that makes a 3/4 line three to four bars long, which supports the 3/4 plan. | measured; our inference | 749.226 |
| 6 | "10 different bar rhythms in 16 bars" and "6 of the 16 bars repeat an earlier rhythm" are the same number. A small repeat bonus can't move it: with hundreds of choices, the bonus would need to be over 100 times stronger. Mixing the section's own rhythms with the style table, about 2 to 1, would act directly. | our inference | 749.259, .257 |
| 7 | Across 113 song collections from many cultures, rhythm repeats more than pitch: about 71% of a melody's rhythm against 51% of its pitches. The engine remembers pitch within a section but not rhythm. (One check is still due on the main source: its song list hasn't been screened for TheSession data.) | measured (flagged) | 749.259 |
| 8 | The same rhythm sounds more off-beat in 6/8 than in 4/4. Each metre needs its own off-beat range, measured by the beat-strength tree. | measured; our inference | 749.256 |
| 9 | The 3/4 range problem lies between phrases. A folk phrase spans about 9 semitones and a whole folk song about 12.5. The engine's whole 3/4 tune spans 9, which is one folk phrase. | measured; our inference | 749.227 |
| 10 | No study anywhere counts how much of a song sits on its commonest pitch. Heavy leaning on one pitch goes with chant and recitation, not dance songs. The engine's 0.39 to 0.42 sits between folk (about 0.28) and chant. A pitch-spread measure can't catch this, so it needs its own mark. The home note needn't be the commonest. | measured; our inference | 749.226, .255 |

## The first counts to make (cheapest first)

| Count | On | Answers |
|---|---|---|
| Notes on each beat and each eighth of the bar, in 3/4 and 6/8 | Essen, Hooktheory clips, the lead sheets, Lieder | Findings 1, 2 |
| How often a strong beat is left empty because the note came early | the same | Findings 1, 3 |
| Different bar rhythms in a section's first 16 bars, against shuffled bars | Hooktheory clips, lead sheets | Findings 1, 6 |

Each report's table of testable ideas has the full list: 29 rows for rhythm, 19 for pitch, 19 for form.

## One correction, and what's still to check

- **Correction to the last report:** Hayes and Kaun's 10.9% are lines whose first word comes in late. They don't show that 89% of lines begin with a pickup, so that sentence should go (749.253).
- **Figures to check:** most papers were read through a summary tool, so their exact figures are flagged in each report's source list. Check them before anything is built in.
- **Licences not yet confirmed:** Essen, the Hooktheory clips' source, the lead sheets, and several world archives (listed in each report). Confirmed: OpenScore Lieder (CC0), the Meertens songs (non-commercial), the Natural History of Song transcriptions (non-commercial).
- **Not reached:** Arabic rhythm cycles, most Indian cycles, and call and response. Each is too little studied in numbers to say anything yet.
- No TheSession data and no figure from the withdrawn studies was used.
