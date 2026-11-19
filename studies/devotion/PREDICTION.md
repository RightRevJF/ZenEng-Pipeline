# Devotion: the songs people return to — rules written 19 Nov 2026 before measuring

Human preference read from behaviour one step closer to the person: last.fm counts of LISTENERS (how many people played a song at all: breadth) and
PLAYS (how many times in total). Devotion = plays per listener (log plays - log listeners), with log listeners and release year held, so it is not
just fame. A song with high devotion is one its listeners come back to.
Data: Voetter et al., HSP-S (7,736 Million Song Dataset tracks, half Hot 100 hits and half never charted, Essentia numbers from previews) and
HSP-L (73,482 tracks, AcousticBrainz numbers from whole recordings). HSP-S is measured first; HSP-L is the replication, same rules, nothing refitted.

 D1  `concentrated_spectrum` (the six readings that passed the lock, equal weights, unchanged) against devotion: > 0, p < .01.
 D2  Essentia's mood classifiers: sad > 0 and happy < 0 against devotion, p < .01 each (from the finding that lasting hits are less cheerful).
 D3  a ridge reader over the sound means, fitted on half the tracks and judged on the other half, against devotion: > 0, p < .001. Reported: its size against
     the same reader built for breadth, i.e. whether sound says more about who comes back than about how many came.
Reported, no pass rule: the single readings that separate devotion from breadth with the same sign in both halves; hits and non-hits apart.
Nothing goes into the engine on this study.

## Amendment after HSP-S, before HSP-L was read
HSP-S: D1 FAILED as stated (-0.036): across all genres, devoted listening on last.fm goes with dense, loud genres. With Essentia's own genre classes held it is +0.050.
For HSP-L the genre-held reading is therefore the primary one for D1 and D2 (declared now, after seeing HSP-S, before reading HSP-L); the unheld reading is reported beside it.
D1 on HSP-L, genre held: > 0, p < .01. D2: happy < 0, p < .01 (sad dropped: it showed nothing). D3 as before.
