# Two tests the brainstorm voted for — rules written 19 Nov 2026 before measuring

## Test 1. Same song, different hit recordings (five votes)
Works = SecondHandSongs works with two or more Hot 100 recordings by different performers (title and performer both matched), love known for each.
Love = Spotify 2021 popularity ranked within three years of the recording's own chart date, then with chart peak and year taken out.
 Q1  the intraclass correlation of love across recordings of the same work (one-way, works as groups), with a bootstrap interval over works and a
     shuffle of work labels as the null. This is the share of lasting love that belongs to the SONG rather than the record; a perfect reader of the page
     could correlate with love at most at its square root. No pass rule: it is a measurement. Stated guess beforehand: 0.10 to 0.25.
 Controls reported: the same figure with the performer's own standing held (mean love of the performer's other hits); and for recordings that merely share a
     title but are different songs (should be about zero).
 Q2  (producer's directional prediction) within a work, the recording that sounds less like the hits of its own years (Spotify readings, the measure that passed
     the lock) is the one more loved now: sign test over pairs, predicted > 50%, pass at p < .05. Reported besides: the same for valence (-), danceability (-), acousticness, energy.

## Test 2. Is "concentrated sound" just "old slow ballad"? (two votes)
The locked-test measure `concentrated_spectrum`, unchanged, on all 3,472 recordings of the two stores.
 Q3  it stays positive, p < .01 pooled over stores, with ALL of these held at once: chart peak, five-year band, tempo band (Essentia bpm in five bands),
     and seven genre families. If it falls under +0.04 pooled, the finding was mostly era, tempo and genre.
 Q4  reported separately for love and for covers, and inside slow, middle and fast tempo thirds.
Nothing goes into the engine on this study.
