# Lyric research: prediction (written and committed before any corpus reading)

Date: 25 November 2026. Measures: `measures.py` (this folder), frozen at this commit.

## Question
Among songs that were all big hits, which measurable traits of the words go with lasting acclaim? The aim is what separates lasting lyrics across many writers and styles, not any one writer's style.

## Data
- **Songs:** Billboard Hot 100 year-end lists, 1965-2015 (walkerkq/musiclyrics, 5,100 rows; songs with more than 50 words of lyrics kept). The text is lowercase with no punctuation or line breaks, so only word-level measures are used. No lyric text is stored or committed; only numbers.
- **Outcome 1 (acclaim):** on Rolling Stone's 500 Greatest Songs in any edition (2004, 2010, 2021), matched by normalised title and artist.
- **Outcome 2 (covers, replication):** number of distinct recording artists in the song's Discogs-VI version clique (log scale), where it can be matched.
- **Controls:** year (fixed effects by year), year-end rank, log word count.

## Measures and predicted directions (acclaimed vs other hits)
| Measure | Prediction | Basis |
|---|---|---|
| conc_noun (mean noun concreteness) | higher | Kao & Jurafsky 2015 |
| image_noun_rate (concrete nouns per 100 words) | higher | Kao & Jurafsky 2015 |
| emo_rate (named emotions per 100 words) | lower | Kao & Jurafsky 2015 |
| poetic_stock_rate | lower | Walsh 2024 |
| verb_share | higher | Dai 2024; Hampton 2019 |
| you_rate | higher | Packard & Berger 2020 |
| stock_rate (common 4-grams, leave-artist-out) | lower | Lu 2025; Saakyan 2026 |
| repetition (repeated 4-grams) | lower | critics vs charts (section G) |
| mattr (lexical diversity) | higher | as above |
| zipf_content (word commonness) | lower (rarer words) | Weinstein 2022 |
| allit_rate, asson_rate (sound devices) | higher | Kao & Jurafsky 2015 |
| sem_dist (distance between neighbouring words) | inverted U: a sweet spot | Orwig 2025 |
| adj_share, i_rate, we_rate, compress, archaic_rate | no prediction (described only) | |

## Tests
1. **Within writer (primary):** conditional logistic regression grouped by artist, over artists with at least one acclaimed and one other hit. Each measure alone, standardised, with log word count and year as covariates.
2. **Across writers:** logistic regression with year-band (5-year) fixed effects, year-end rank and log word count.
3. **Covers (replication):** OLS of log distinct covering artists with artist fixed effects, the same covariates.
4. sem_dist adds a squared term; the prediction holds if the squared term is negative and the peak lies inside the observed range.

## Rule for "passes"
A measure passes if, in test 1, its sign is as predicted with p < 0.05 after Holm correction over the 13 predicted measures, **and** test 2 has the same sign. It is **confirmed** if test 3 also has the same sign at p < 0.05 (one-sided). A measure with the opposite sign at p < 0.05 in test 1 is reported as **reversed**. Everything else is **unsettled**. Only passing measures go into the writing room as checks; unsettled ones may go on the craft checklist only as advice, marked as such.

## Cautions written down now
- Rolling Stone's list is one magazine's taste, weighted to rock and soul of the 1960s and 1970s; year fixed effects only partly fix that.
- Billboard hits are a narrow slice: all the songs here were already popular.
- The lyrics have no lines, so rhyme, line length and the turn cannot be tested here.
- Songs 59, 50 and 63 are hold-outs and are not scored in this study.
