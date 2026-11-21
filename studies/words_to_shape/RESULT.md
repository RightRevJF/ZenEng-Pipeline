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
