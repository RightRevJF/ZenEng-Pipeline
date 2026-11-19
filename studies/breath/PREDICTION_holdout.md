# Breath, held out: written before any breath reading was computed on these songs (18 November 2026)

Songs: Hooktheory clips (melody in beats, aligned to the recording's beat times), 4/4 throughout, 64 beats or more; the longest clip of each song.
Joined by title and artist to the Billboard Hot 100 record (utdata/rwd-billboard-data, hot-100-current.csv; peak). Songs whose title is in CoCoPops or
BiMMuDa are left out, so none was seen in discovery. Groups as in discovery: peaked in the top 10 against peaked below no. 20.

Readings exactly as in discovery (breath_spectrum.py readings(); the breath is an onset gap of 1.5 beats or more; dominant period 3 to 32 beats;
locked = within 0.6 beats of 4, 8 or 16), with seconds a beat from the aligned beat times (median).

H1 (the lead, 749.65). Breath locked to 1, 2 or 4 bars is more common in top-10 songs than in songs that peaked below 20: odds ratio 1.5 or more,
one-sided Fisher p under 0.05. Anything less: the lead does not hold, and 749.65 says so.
H2 (first pass). The four-bar unit lasts longer in top-10 songs than in below-20 songs: AUC 0.55 or more, one-sided p under 0.05.
H3. The commonest dominant breath among top-10 songs is every two bars (8 beats).
Secondary, stated now: the same tests on clips of 32 beats or more (more songs, shorter clips; period read from 3 to 16 beats, locked to 4, 8 or 16).
Clips are sections, not whole songs, so a null here could be the clip; a pass would be on songs never seen.
