# Lyric research: result (task 67)

Read against PREDICTION.md (commit e068657). Data: 4,612 Billboard year-end hits, 1965-2015, with lyrics; 245 of them on a Rolling Stone 500 list. Within-writer test: 132 artists with both kinds, 1,027 songs, 194 acclaimed. Covers: 1,172 songs matched to a Discogs-VI version clique.

## Verdict by the rule: no measure passes
| Measure | Within writer | Across writers | Covers | Verdict |
|---|---|---|---|---|
| image_noun_rate | +0.04 (p .59) | **+0.14 (p .010)** | -0.03 | unsettled |
| conc_noun | +0.05 (p .60) | +0.12 (p .066) | -0.10 (p .010) | unsettled |
| stock_rate | -0.11 (p .34) | **-0.27 (p .003)** | -0.01 | unsettled |
| zipf_content | -0.04 (p .72) | -0.11 (p .045) | 0.00 | unsettled |
| emo_rate | -0.03 (p .75) | -0.14 (p .10) | +0.06 | unsettled |
| you_rate | -0.09 (p .35) | -0.15 (p .052), opposite to prediction | +0.04 | unsettled |
| verb_share, repetition, mattr, allit, asson, poetic_stock, sem_dist | all near zero | near zero | near zero | unsettled |

(Coefficients are per standard deviation; within = conditional logit by artist; across = logit with 5-year bands, year-end rank and length, errors clustered by artist.)

## What it means
1. **Within a writer, the words don't pick the canon.** A writer's acclaimed hit is not more concrete, fresher, less repetitive or more sonorous than the same writer's other hits. Which of a writer's songs lasts is decided by things these measures can't see (the music, the line and rhyme, the performance, the moment).
2. **Across writers, the expected traits show up.** The writers whose hits got canonised use more concrete image nouns, fewer stock phrases, somewhat rarer words, and fewer named emotions and less "you" than other hit-makers. These mark the writer, not the song. Stock phrases alone would survive a Holm correction (p .003 × 13 = .04), but the rule tests within writer first, so it is advice, not a gate.
3. **The instrument works.** Positive controls reproduce the known trends: repetition rises with year (rho +0.21), compressibility falls (-0.25), first-person rises (+0.10), named emotions fall (-0.14).
4. **Covers don't follow the critics on these traits.** Among songs with a version clique, more concrete nouns went with slightly fewer covering artists.

## Our songs (ours.json; songs 59, 50 and 63 not read)
Median percentile among the hits: image nouns 93rd, noun concreteness 90th, stock phrases 12th, named emotions 0 (none), stock poetic words 0, "you" 20th, verb share 28th, word rarity 53rd.

Medians, ours against acclaimed hits: image nouns 13.7 vs 7.4 per 100 words; named emotions 0 vs 1.2; "you" 2.0 vs 4.5; verb share 0.36 vs 0.39.

So we already sit past the acclaimed writers on every trait that separates them from other hit-makers. The corner we occupy (image density at our level with no named emotion) holds 5.7% of acclaimed hits against 1.8% of all hits: a real and favoured corner, but a narrow one. Pushing further along these lines cannot be supported from this data.

## Limits
- One magazine's list; rock and soul of the 1960s and 1970s weigh heavily.
- Only hits; only words; no lines, so rhyme, line length, the turn and setting were not tested.
- Our lyrics were scored from the printed drafts (choruses printed once), the corpus from sung transcriptions.
