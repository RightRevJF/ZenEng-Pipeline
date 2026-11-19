# Round two: the mathematician

## 1. The two strongest ideas from the others

**(a) The cloud of versions: physicist's idea 1 (stiff and sloppy directions) with evolutionist's idea 3 (the conserved core).** This is the right object. It is the quotient I asked for in round one, measured instead of guessed: the directions covers never move are the song, the directions they move freely are the symmetry. The physicist's step of learning the stiff subspace P from covered works and then scoring any single recording by its distance from neighbours inside P only is the best single proposal in the room, and it explains why "unlike its year" was weak (+0.09): it mixed directions that matter with directions that do not.

Three corrections from my side.
- *The per-song spectrum is mostly artefact.* With n versions in d feature dimensions and n smaller than d, the sample covariance has rank at most n − 1, and its eigenvalues spread widely even when the truth is a round ball (the Marchenko-Pastur effect: a small sample of a sphere looks like a cigar). "Anisotropy" and "stiff-core rank" per work will therefore track n, which is the cover count, which is the yardstick. Fix: cut d to at most n/3 by projecting onto the pooled leading directions first, subsample every work to the same n, and compare against round-ball simulations at that n and d.
- *The spread of a cloud is partly the yardstick again.* A song covered across many genres has a wide cloud because its coverers differ, not necessarily because the song permits more. Only the predictive forms (physicist's P-distance on one recording; evolutionist's 3c, conservation predicted from the page) escape this circle. Run those; treat the cloud shapes as description.
- *Features are not all vectors.* Key lives on a circle of twelve and tempo is a ratio. Use log tempo and (cos, sin) of key, or the covariance is meaningless in those coordinates.
- One caution on the slogan "largest symmetry group": fixing little and leaving much is maximised by a song of one note. The claim only has content with the constraint stated: largest free volume *at fixed distinctness from every other song*.

**(b) The hymn table with texts and tunes crossed: sceptic's idea 1 (also songwriter 2, evolutionist 2).** The only design in the room that removes the record, the star, the charts and the words at once, with full range and exact scores.

What mathematics adds.
- *Comparability.* Tune effects b_j are only comparable inside a connected piece of the text-tune graph, and metre cuts that graph into pieces (a common-metre text never meets a long-metre tune). Tunes must be graded within metre class, not merely "controlled for" it.
- *The pairing term.* With one count per cell, a free pairing effect g_ij cannot be told apart from noise. The estimable version is low-rank: g_ij = u_i · v_j, each text and each tune a short vector, fitted by matrix factorisation on the cells that are structurally possible. That is not a nuisance; it is a space, learned from four centuries of choices with no ears in the loop, in which a tune and a text are close when they belong together. It is the nearest thing on the table to the Hilbert space the owner asked for.

## 2. The weakest idea in the room: my own idea 7

The coordinate-free shape comparison (Gromov-Wasserstein between songs treated as sets of bars) will fail, for two exact reasons. First, a set of bars with distances between them forgets the order of the bars. What survives is the pattern of which bars resemble which, which is repetition and form, and those already failed. I proposed a "shape" that discards the arrow of time while proposing in idea 6 that the arrow of time might be the point. Second, I called the nearest-neighbour test "decisive". It is not. By the sceptic's power arithmetic, a nearest-neighbour classifier on three thousand songs with a noisy distance cannot see an effect of the size everything real here has (0.05 to 0.25). Its failure would retire nothing. I withdraw the word and the idea.

Runner-up: the physicist's wild coupling g, which is defined two ways ("pi times (S − 1), or the low-frequency coherence"). A quantity with two definitions cannot be proved wrong.

## 3. A new idea that needs several papers at once: let the coverers draw the map

*Sources: evolutionist's cover network (idea 4), sceptic's "similar pages, similar fates" (idea 3), my cover-taught metric (idea 5), and the factorisation in 1(b) above.*

**Plain words.** Every yardstick so far squeezes the cover lists into one number per song and throws away *who* covered it. Keep it. Two songs are close if the same performers chose both. That defines a space of songs built entirely from behaviour: no features, no ears, no theory. Then ask a matrix-against-matrix question instead of forty feature-against-number questions: do songs that are close on the page get covered by the same people? This uses every pair of songs, millions of comparisons instead of a few thousand, so it has the power the scalar tests lacked.

**Mathematics.**
- M = performers by works, entry 1 if the performer recorded the work. Drop performers with fewer than 3 works and works with fewer than 5 versions. Down-weight prolific coverers: multiply each performer's row by log(number of works / number that performer covered).
- Behaviour kernel K_cover = cosine similarity between columns of M. Embedding z_w = the work's coordinates in the top 30 singular vectors of M. The first axis is roughly "how much covered"; set it aside.
- Page kernel K_page (sceptic's interval-and-duration n-gram kernel), sound kernel K_sound (Essentia), arrangement kernel (producer's vector).
- Test A, alignment: centre each kernel (subtract row and column means), then A = sum of entrywise products of the two, divided by the product of their norms. Null: shuffle the works within the same five-year band and genre, 1,000 times.
- Test B, readable axes: ridge regression from page features to each coordinate of z_w, scored on held-out works. Axes the page predicts are *song* axes; axes only the sound predicts are *record* axes. The split of the yardstick falls out of the data instead of being imposed.
- Greatness inside the space: with axis 1 removed, the spread of a work's coverers across the remaining axes (the evolutionist's reach, now with coordinates).

**Data.** Have: cover lists, tunes, Essentia. The same construction runs on the hymn table (texts and hymnals choosing tunes).

**Wrong if** the alignment of K_page with K_cover sits inside the shuffle null within year and genre bands: then who takes up a song has nothing to do with its notes beyond genre.

**Odds.** 40% that the page aligns above null within bands; 25% that the readable axes then grade the yardstick.

## 4. Votes

**First test with data in hand:** the producer's idea 6, run inside five-year bands. Take the features that already held (spectral concentration, event rate, unlikeness) and correlate them separately with covers and with lasting play. Nothing new needs computing. It answers at once the two questions most of the room raised: is the +0.25 an era effect, and which half of the yardstick does each signal belong to. Five of seven papers proposed splitting the yardstick independently; that agreement should be cashed first.

**First test needing new data:** the hymn text-by-tune-by-hymnal table (Hymnary; the Irish session dump on GitHub as fallback), analysed within metre class with the low-rank pairing term.

## 5. The converging theory, and whether I believe it

*A great song fixes a small core hard and leaves the rest open: room around the voice on the record, room for the next performer in the song, so that greatness is the size of the family of versions that are still recognisably it.*

I half believe it, about 35%, and only in the constrained form: most free room *per unit of distinctness*. Two warnings. As stated it is close to a restatement of the yardstick (many covers means a large family of versions), which is why four independent wild ideas landed on it; it becomes a theory only when the free room is predicted from one specimen before any cover exists. And it joins two different things by metaphor: empty space in a recording's spectrum and freedom in a song's identity. Nobody has yet shown they are the same quantity. The test in section 4 is the first step toward finding out.
