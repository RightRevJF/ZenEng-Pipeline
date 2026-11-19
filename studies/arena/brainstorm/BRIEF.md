# Brainstorm brief: what, in mathematics, makes a song GREAT rather than merely good?

## The owner's conviction
Jason Bryant (pastor, physicist of scaling and criticality, songwriter) is convinced music is mathematics and that greatness must be quantifiable with no
human ears in the loop. His hunch: plot a song in some space so that its greatness shows as shape, the way one statue is beautiful and another humdrum.
He says music can move people without words, so the answer should not depend on lyrics, though words may amplify it. He wants this explored on faith that an
answer exists, and he wants IDEAS now, not more of the same analysis.

## The yardstick he chose
Great = still loved long after release AND covered by many other artists. Critics deliberately left out. All test songs so far are US Hot 100 hits up to 2005,
so the question has been "good hit versus great hit".

## What a day of testing found (about 40 pre-stated tests, then six agents with a locked hold-out)
FAILED on unseen songs, all on the written tune and chords (melody as onset/pitch lists, lead-sheet chords), on 1,500-4,000 songs:
repetition and varied repetition; melodic curvature; persistence; dimensionality; topological loops; 1/f scaling (songs DO sit near the critical point, S about 0.9,
but nearness does not grade them); pace, range, leaps, long notes; mean and localised surprise under n-gram models; learned phrase codebooks and autoencoders
(one passed two sets and died on a third); newness against the prior decade and influence on the next; chord-tone share, tension and resolution, contrary motion;
mood predicted from the notes; scarcity (the single high note: reversed if anything); memory density; mutual information between pitch, rhythm and harmony;
song form and section contrast; syncopation and phrasing; singability; multifractal and avalanche statistics; robustness of a tune under perturbation.
Same-artist comparisons of all of it: nothing. Word stress against melodic accent: leaned positive on 128 well-aligned songs, never properly tested.
HELD on unseen songs, all small (rank correlations 0.05-0.25), all in the RECORDING not the page:
- concentrated spectrum: energy gathered in a few low and low-middle bands with the rest left open; sparse rather than a dense bright wall (+0.25 whole recordings).
- fewer sound events per second.
- the recording sounds UNLIKE other hits of its own years, in any direction (+0.09); the same measure on the written tune scores zero.
- less cheerful sound (Spotify valence -0.09).
- distinctive title words (+0.04).
- (career, not music: performers who kept charting are still loved, +0.2.)
The artist explains only about 15% of the yardstick; most of the variation is between songs by the same artist.

## Data that exists here (so an idea can be tested quickly)
Tunes as note lists for ~3,100 graded hits (three transcription sources); Hooktheory melody+chords for ~900 graded and ~20,000 ungraded songs; full multi-track MIDI
arrangements for ~1,400 graded songs (Lakh clean, ~17,000 ungraded); 127 Essentia sound numbers for ~3,500 graded recordings (no raw audio); Spotify's 11 readings,
titles, genres, chart histories for ~18,000 graded hits; cover-version lists (SecondHandSongs, ~10,000 works, each version's performer and title); lyrics for a few thousand;
hymn tunes, folk tunes, jazz standards and classical scores ungraded. No raw audio. Internet access is limited to GitHub and Zenodo for new datasets.

## What is wanted from you
Think. Do not run analyses. Read nothing but this brief unless you need to check a fact. Bring your own field's deepest ideas to bear and be bold: new framings of the
question, new representations of a song, new objects to measure, new yardsticks or sharper versions of this one, reasons the failures happened and what they imply,
experiments nobody here has thought of. An idea may need data we do not have; say so and say where it might be found.
Write your contribution to the file you are told, in this form:
1. Your diagnosis in a short paragraph: why did everything on the page fail, and what does that tell us?
2. Five to seven ideas, most promising first. For each: a name; the idea in plain words (three or four sentences); the mathematics precisely enough that a programmer
   could compute it; what data it needs and whether we have it; what result would prove it WRONG; your honest odds it holds.
3. One wild idea you would not defend in public but cannot put down.
Plain language. No jargon without a one-line gloss. No flattery of the owner's hunch and no dismissal of it either: take it seriously and say what would make it true.
