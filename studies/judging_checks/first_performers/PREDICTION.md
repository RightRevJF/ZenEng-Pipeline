# Chord repetition against covers, among first performers and by other artists only (R04-2): the rule, written first

26 November 2026. Seen before writing: `within_artist/RESULT.md` (−0.042, p .009, within artists; and, read beside it and deciding nothing, the same model on other artists' versions only), and the count from R02-3's mend: of the songs the covers study measured, the Hooktheory artist is not among the clique's first performers in about a quarter (703 of 2,769). Nothing has been run with the first-performer flag joined to any measure.

**Question.** 749.157 held chord repetition against covers within each artist's songs. But a quarter of those "artist's songs" are the artist's cover of someone else's song, and their cover counts are the song's, not theirs. Does the finding hold where the artist is the song's first performer, counting only other artists' versions?

**Rows.** As `within_artist/test.py` builds them, with one filter: the Hooktheory artist is among the performers of the clique's earliest dated versions (R02-3's rule). Artists with two such songs or more.

**Outcome.** Versions by other artists only (`others`: sets of performers that do not include the artist), log(1 + count). The model, the controls (first year, log views) and the standardising are `within_artist/test.py`'s, unchanged.

**The one test.** Chord repetition, within artist. By the rule of 749.157, unchanged: **holds** if −0.04 or stronger, p < .05, and the same sign in both halves of the artists (the same hash); **belongs to performers** if weaker than −0.02; **unsettled** otherwise.

**Power (the floor ruled today).** Reckoned from the test's standard error against −0.04 before the estimate is printed. If it is under 0.2 the test is reported as an estimate and passes or kills nothing.

**Read beside it, deciding nothing:** the same on all covers (the old outcome) among first performers; the same on other artists' versions with no filter (already read, repeated for the table); and among the songs where the artist is *not* the first performer.

**What I expect.** Fewer rows (about three quarters), so a wider error; the estimate between −0.03 and −0.05; "unsettled" more likely than "holds" for want of power, not for a change of sign. If the effect is much weaker among first performers and strong among the covers-of-covers, the finding was partly about which songs artists choose to cover, and that would be worth knowing.
