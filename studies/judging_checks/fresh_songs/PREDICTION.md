# Chords that move, on fresh songs (the judging research's J6b): the rule, written before the outcome is joined

22 November 2026. The McGill Billboard chord charts are in the repo (`studies/harmony/billboard_sections.json`, 739 songs). Their cover counts have never been made: no McGill song has been joined to Discogs-VI. This file is committed before that join.

**The claim.** Songs whose chords repeat less within a section are covered more: −0.071 across artists and −0.042 within artists, both on the 2,360 Hooktheory songs where the finding was found. A finding is only known to be real when it shows on songs it was not found on.

**Seen before writing:** those two figures; the McGill charts' repetition readings from this morning's check (`studies/judging_checks/nights_1_2`), with no outcome. Nothing of any McGill song's covers.

**What is done** (`test.py`).
- **Covers:** each McGill song matched to a Discogs-VI group as the covers study matched Hooktheory songs: the cleaned title, and the McGill artist among the group's performing artists; covers = the group's other performing artists.
- **Fresh:** a McGill song is dropped if its Discogs-VI group is one that any Hooktheory song matched (all 3,080, not only the 2,360 with measures).
- **The measure, frozen this morning:** within-section chord repetition as `gap.py` reads it: the share of a section's chord 3-grams already heard earlier in that section; the first instance of each section letter; sections of at least four merged chords; weighted by bars. It is the nearest McGill allows to the covers study's measure, and it is not the same: whole charts by section, not Hooktheory clips; a different chord alphabet.
- **Model:** log(1 + covers) on repetition and the group's first year, both standardised, standard errors clustered by artist. No views (McGill has none). Chart peak is left out of the main model, because the notes may partly cause it; it is read as a sensitivity only.
- Power to see −0.05 is printed before the estimate.

**The rule.**
- **Holds on fresh songs:** −0.05 or stronger and the 95% range excludes zero.
- **Same direction, not settled:** negative, the range including zero. (The judging research put the power at 20 to 35 in 100, so this is the likeliest outcome even if the finding is true.)
- **Against:** positive. A positive figure whose range excludes zero would count as a failure to replicate.

**What I expect.** Negative, between −0.03 and −0.08, with a range that includes zero: same direction, not settled.

**Afterwards.** The McGill cover counts go to `studies/judging_data/` marked as a hold-out: the nightly research may be told the result of this one test, and must not explore on those counts, or they stop being fresh.
