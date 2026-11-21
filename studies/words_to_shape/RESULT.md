# Do a song's words and form predict its tune's shape? Result

Rule in PREDICTION.md, written first. 160 kept 4/4 songs, 125 artists; each song predicted only from other artists' songs; chance read from 500 shuffles.

| Shape reading | Held-out rank correlation | Shuffles' 95th | Predicted? | What predicts it most |
|---|---|---|---|---|
| Bars on a figure already sung | +0.53 | 0.10 | **yes** | words in a three-word run already sung (+0.49); different words over all words (-0.39); lines said again (+0.37) |
| Bars on a rhythm already sung | +0.46 | 0.11 | **yes** | the same three (+0.44, -0.35, +0.35) |
| Range | +0.44 | 0.09 | **yes** | syllables in the song (+0.35); year (+0.33); syllables a word (+0.23) |
| Moves by step | +0.20 | 0.11 | no | |
| Rhythm scaling | +0.19 | 0.11 | no | syllables a line (+0.42 alone, but not held out) |
| Repeated notes | +0.14 | 0.10 | no | |
| Moves by leap | -0.10 | 0.12 | no | |
| Notes a bar (the method's check) | +0.61 | 0.09 | yes | syllables a line (+0.86) |

**Verdict, by the rule: the words decide the shape** (three of seven predicted; three were needed).

**In plain terms.**

- **How much a tune repeats is set by how much its words repeat.** A lyric that says its lines and phrases again is sung on bars it has sung before. This is the strongest link, and it is the thing seven versions chased by copying another song's number.
- **How wide a tune ranges** follows the song's length, its era and its word length. Caution: a longer song has more notes and so more chances to reach its extremes; part of this link is arithmetic.
- **How a tune moves** (steps, leaps, repeated notes) is **not** set by the words. That is a free choice, or belongs to something the words do not carry.

**What the random draw was doing (`ours.py`).** Each of Luthier's songs, read by the kept songs' own link from words to shape, against what the song it drew told it:

| | From its own words | Told by the song it drew |
|---|---|---|
| Song 59, bars on a figure already sung | 0.61 | 0.32 (Two Hearts) |
| Song 58, range | 18 | 9 (Bird Dog) |
| Song 58, bars on a figure already sung | 0.50 | 0.70 |
| Song 55, bars on a rhythm already sung | 0.69 | 0.53 (Don't Ask Me Why) |

Song 59's lyric repeats its lines more than the other three, and the draw told it to repeat least. The draw was often working against the words.

**What follows.** The engine should stop taking one song's numbers. Repetition and range can be set from the lyric itself, by a link found in the kept songs as a body (a style guide, not a model song). Movement needs another source: the writer's choice, or a rule of the engine's own.

## Amended in Window 198 (749.128): the words read the same way on kept songs and on Luthier's

The songwriting session found that the first run split a kept song's words into lines in proportion to each line's notes, while a Luthier lyric's real lines were read. "Lines said again word for word" was nearly missed in kept songs (median 0.03) and read at full strength in Luthier's lyrics, so the table asked Luthier's songs for too much repetition and too little range.

Mended: each kept word is tied to its notes by its syllables, and a line's words are the words that begin in it (`words_to_shape.kept_lines`). The study was run again (`result.json`; the first run is `result_v39.json`):

| Shape reading | Held-out rank correlation: first run, mended |
|---|---|
| Bars on a figure already sung | +0.53, **+0.58** |
| Bars on a rhythm already sung | +0.46, **+0.52** |
| Range | +0.44, **+0.42** |

The verdict stands and the two repetition links are stronger. Kept songs' lines said again now read 0.08, 0.32, 0.52 at the 10th, middle and 90th; Luthier's five lyrics read 0.23, 0.14, 0.19, 0.33, 0.28, the kept 17th to 54th: alike, and if anything Luthier's lyrics say their lines again a little less than kept songs do.

What the words ask, first run and mended (songs 55, 54, 58, 59, 60): range 15.6, 17.3, 18.0, 15.9, 16.3 to **18.0, 18.8, 19.9, 18.8, 19.0**; bars on a figure already sung 0.51, 0.46, 0.46, 0.55, 0.55 to **0.42, 0.39, 0.41, 0.45, 0.46**; bars on a rhythm already sung 0.63, 0.60, 0.59, 0.66, 0.66 to **0.54, 0.53, 0.55, 0.57, 0.58**.

**So the builds already sing their bars again about as often as their words ask** (Window 196's builds: 0.38 to 0.49 and 0.50 to 0.60). The piece Window 196 recorded as "asked by the words and not yet acted on" needs no acting on. The mistake was in my measure.
