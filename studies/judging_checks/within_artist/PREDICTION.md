# Chords that move, within each artist's own songs (the judging research's R02-1): the rule, written before the outcome is joined

22 November 2026, written while the Discogs-VI download is still running and before any cover count is on this machine. The notes file (Hooktheory, Sheet Sage) is here; the cover counts and the views are not yet joined to anything.

**The claim under test.** Songs whose chords repeat less within a section are covered more: −0.124 on SHS100K (780 songs), −0.071 on Discogs-VI (2,360 songs) (`studies/covers/covers_study_report.md`). Both compare different artists' songs. The judging research (run 02, R02-1) points out that the performer's fame, voice, era and genre travel with the harmony, and that no test has held the performer still.

**Seen before writing:** the two figures above and the committed `covers_discogs_results.json`; the judging research's own prediction for this test; nothing of any within-artist result.

**Step 0, reproduction.** `studies/covers/study_covers_discogs.py`, unchanged, on the data fetched again today. Its chord-repetition term must come out near −0.071 (I accept −0.05 to −0.09: views are fetched two weeks later and some videos will be gone). If it does not, the rows are not the same and nothing below is read.

**The test** (`test.py`). On those same rows, artists with two or more songs. log(1 + covers) on within-section chord repetition (`ch_rep`), with a fixed effect for each artist, first year and log views. Everything standardised as in the covers study, so the figure is on the scale of −0.071. Standard errors clustered by artist. Artists split in two by the parity of an md5 of the artist's name. The power to see −0.04 is computed and printed before the estimate is.

**The rule (the judging research's, adopted unchanged).**
- **Holds:** −0.04 or stronger, pooled p < .05, the same sign in both halves.
- **Belongs to performers, eras or genres:** weaker than −0.02. J1's change to the engine's structure draw is then withdrawn.
- **Unsettled:** in between, or strong enough but not significant, or the halves split. Reported and left.

**Also reported, deciding nothing:** the same model on covers made within five years of the first release and on covers made more than ten years after; the full control set of the covers study with the artist held; the same test for the other sixteen note measures (seventeen tests: about one would pass at .05 by chance).

**What I expect.** The between-artist figure is partly the artist's, so I expect it to shrink: about −0.03 to −0.04, with the halves agreeing in sign and the pooled p near .05. That is the unsettled band. I hold this loosely: I have no evidence either way, and I was wrong twice yesterday on this project's readings.

**What it cannot say.** The songs are all hits with a Hooktheory transcription. An artist's own songs still differ in era and in which were singles. A within-artist effect is not proof that the notes cause covers; a null within artists does not prove they do not, if power is low.
