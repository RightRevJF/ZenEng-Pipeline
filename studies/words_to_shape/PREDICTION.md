# Do a song's words and form predict its tune's shape? The rule, written before the data is read

**Why.** Luthier gives each 4/4 song its shape (how wide it ranges, how it moves, how much it repeats) by drawing one kept song at random and taking that song's numbers. Jason's objection: the engine should decide a song's shape from the song itself and its own theory, with other songs as a style guide only. Before rebuilding, one thing must be known. In real songs, is the tune's shape something the words and form decide, or a free choice?

**Data.** The 160 kept 4/4 songs (CoCoPops Billboard) with their words.

**What the engine would know before any music is written (the predictors), all from the words and the form:**

1. syllables in the song (log);
2. syllables a line, mean;
3. how uneven the lines are (spread of syllables a line over the mean);
4. syllables a word, mean;
5. different words over all words;
6. share of lines that say an earlier line again, word for word;
7. share of words that fall in a three-word run already sung;
8. how many kinds of section the song has;
9. share of the syllables that are in a chorus;
10. whether it has a bridge;
11. major or minor;
12. year.

(Lines in this data are marked by rests in the singing, so predictors 2, 3 and 6 lean a little on the music. That favours finding a link, not missing one.)

**The shape (what is to be predicted):** range; moves by step; moves by leap; repeated notes; bars on a figure already sung; bars on a rhythm already sung; rhythm scaling.

**Method.** For each shape reading, a ridge regression on the twelve predictors, tested five-fold with every artist's songs kept in one fold, so no song is predicted from its own artist's others. The score is the rank correlation between the predicted and the true reading on the held-out songs. Chance is read by shuffling the true readings 500 times.

**The rule.**

- A shape reading is **predicted** if its held-out rank correlation is 0.25 or more and beats 95 in 100 shuffles.
- **The words decide the shape** if three or more of the seven are predicted. Then the redesign has a foundation: build the shape from the words.
- **The words decide part of it** if one or two are predicted. Then build those from the words, and the rest is a choice.
- **The shape is a free choice** if none is predicted. Then nothing in the words can set it honestly, and the writer (or a stated rule of the engine's own) must.

Whatever the result, the engine stops taking one song's numbers.

**A check on the method:** notes a bar is read too, and decides nothing. It should be predictable from how many syllables the lines hold; if it is not, the method cannot see what is plainly there.
