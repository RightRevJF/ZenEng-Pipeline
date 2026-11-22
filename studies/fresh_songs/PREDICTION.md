# Chords that move, on songs never used before (J6b): the rule, written before any cover count is joined

22 November 2026, by the songwriting session while the maintainer is offline. Written before any Discogs-VI file is on this machine and before any chord measure is computed on these songs.

**The claim under test.** Songs whose chords repeat less within a section are covered more. Across artists: −0.124 on SHS100K (780 songs) and −0.071 on Discogs-VI (2,360 songs). Within each artist's own songs: −0.042 (p .009, 1,681 songs; `studies/judging_checks/within_artist`). Every one of those songs is a Hooktheory transcription, and the measure was chosen on them. No test has used songs the finding was not found on.

**Revised 22 November 2026, 12:35, before any Discogs-VI file is on this machine and before any chord measure is computed:** the songs and the measure now follow the frozen rules of the judging research's own check on these charts (night two, "The one check"), on the 739 McGill charts committed at `studies/harmony/billboard_sections.json`, so that the measure matches the one already checked against the spectral gap; and a song is fresh only if it is in no part of Hooktheory, not only outside the covers study's matches. Nothing else changes.

**Seen before writing:** the figures above; that the McGill Billboard chord annotations (890 songs charting 1958 to 1991, in ChoCo at `/home/claude/data/choco`, partition `billboard`) are on this machine; that their index gives each song's chart date, peak rank and weeks on the chart; that Discogs-VI is reachable on Zenodo. Nothing of any covers figure on these songs; no chord measure computed on them.

**The songs.** The 739 McGill Billboard charts in `studies/harmony/billboard_sections.json`, less any song whose normalised artist and title (as `studies/covers/covers_match_discogs.py` normalises them) appear anywhere in Hooktheory, and less any song that matches a Discogs-VI version group already matched to a Hooktheory song (`studies/judging_checks/within_artist/discogs_versions_matched.json`). Those left are fresh.

**The measure.** `ch_rep` as the covers study defines it (`studies/surprise/surprise_hooktheory.py`): within a section, the share of chord 3-grams already heard earlier in that section. Read with the research check's frozen rules: the chord token is the chart's Roman numeral with its quality, plus a "7" where the chart flags a seventh; no-chord marks are dropped; a chord repeating the one before is merged into it (bar lines ignored); the first instance of each distinct section letter only, sections of at least 4 merged chords; averaged over those sections weighted by bar count. The code and the measures are committed before Discogs-VI is joined.

**The outcome.** Covers as in the covers study's Discogs-VI leg: the distinct performing artists in a song's version group, minus one, matched by its matcher unchanged; log(1 + covers).

**The model.** Everything standardised as in the covers study, so the figure is on the scale of −0.071. Robust standard errors (HC1).
- Primary: covers on `ch_rep`, with controls for the year the song first charted and the number of merged chords in the sections read. Night two's first-principles review argued that chart weeks and peak are partly caused by the notes and belong in a sensitivity check, not the main model; I follow it.
- Sensitivity, deciding nothing: with log weeks on the Hot 100 (the McGill index) and peak rank added. Views are not used: no YouTube data is fetched for this test, and in the Discogs-VI leg covers and views were unrelated once the year was held (r 0.00).
- The power to see −0.04 is computed and printed before the estimate.

**The rule.**
- **Holds on fresh songs:** −0.04 or stronger, p under .05.
- **Does not travel:** weaker than −0.02, or the other sign.
- **Unsettled:** anything between, or strong enough but not significant.
- If fewer than 300 fresh songs match a version group, the test is reported as too small and decides nothing.

**Also reported, deciding nothing:**
- The same model with each artist held (fixed effects), on artists with two or more fresh songs.
- `ch_rep` against weeks on the Hot 100 instead of covers (the writer's other yardstick, the longevity of love), with the year held.
- Songs that charted in the top 40 only.

**What I expect.** About −0.04 to −0.06: a little weaker than across artists on Hooktheory, because the measure was chosen there, and because McGill's sections and chord spelling differ from Hooktheory's. I hold this loosely.

**What it cannot say.**
- Every song is still a chart song, and every song is from 1958 to 1991.
- McGill annotates whole songs, and Hooktheory mostly sections, so the measure is read on more music here.
- A result on covers does not show that the notes cause covers.
