# Luthier list for v45 (since v44)

21 November 2026. Luthier v44 (957 and the verse-closer trial) is reviewed (`lib/luthier/REVIEW_stage29.md`) and merged into main at 3aa9cd2. Every kept table, every record, song 60's v44 record, `soundness.json` and the two new studies reproduce byte for byte, and so do the neighbour figures up to one block that reads an old ceiling (749.145). Both checks pass. Song 58's notes are unchanged, so it has no new edition. Next finding 749.153; next fix 958. (749.146 and 749.147 were added on 21 November from song 61, and 749.148 to 749.152 from song 12's second and third editions: a running tab while the maintainer is offline.)

## In short

957 holds. 749.140 was chance and 749.141 is not a fault; both are closed. Read for how long a weak word is held, kept songs agree: song 58's "the" sits at their 75th.

On the decision asked: build (a). The fall in song 54's builds' words' fit (0.028) does not reach its chosen tune (0.275 to 0.272). Song 58's chosen tune fits its words better (0.307 to 0.357). The three chosen tunes are sound with no lean at all. Form (b) gives song 54 no one-bar line, since its candidates are 8 or 9 syllables, and would fail the first check. The fifth check moves to the chosen tune, written now.

Two things follow: a hold-out the lever acts on (song 49, by a rule written now), and the second carrier of rhythm scaling, bars with nothing sung, for song 58.

## Items

### 749.142 Build the verse sung closer ("apart"), with the words' check on the chosen tune
**Problem.** Rhythm scaling is the engine's one lean. The trial form moves it into the kept quartiles in two songs of three but missed a check on the builds' middle words' fit in song 54.
**Evidence.** `studies/review29_verse_closer`: the three songs run in full under `LUTHIER_VERSE_CLOSER=apart`.
- Chosen tunes' words' fit, as built against the form: 0.341 against 0.347 (song 55); 0.275 against 0.272 (song 54); 0.307 against 0.357 (song 58).
- Chosen tunes' rhythm scaling: 0.688, 0.646, 0.550.
- `soundness.py` on them: sound, no lean, 10 checks outside the middle half (12 as built).
- Form (b) on 40 quick tunes: song 54 takes no one-bar line, rhythm scaling 0.601, under the kept 25th; it would pass the first check in one song only.

**Fix.** Turn the form on as built in the trial (one-bar verse lines of 6 to 8 syllables, shortest first, none side by side, an even count, nearest the kept middle of notes a bar, the guard on verse over chorus). Replace the fifth check, the builds' middle words' fit, with the check below, written before the build.
**Check.**
- Rhythm scaling of the builds inside the kept quartiles in two of songs 55, 54 and 58.
- No chosen tune's words' fit more than 0.02 under the tune chosen without the form, in each song.
- At least 7 in 10 as many builds live; the soundness rule and the pool standard hold; the guard holds.
- The chosen tunes keep the floor and the ceiling.
- Song 49 (749.143) read, not fitted to.

### 749.143 A hold-out the verse lever can act on: song 49
**Problem.** Song 59, the hold-out, has no verse line of 6 to 8 syllables, so the lever cannot be held out on it.
**Evidence.** Window 201: song 59 unchanged by every form.
**Fix.** A second hold-out, chosen by a rule written now: the most recent song in 4/4 not yet run by Luthier v8, with at least four verse lines of 6 to 8 syllables. That is song 49, "The World Is Asking" (`songs/p59`, words by Jason Bryant). Make `songs/p59/lyric49.json` from `lyric_locked.md` with no change of words; take tempo, genre and voice from its intake. Never fit to it. Its verse lines mostly run 8 syllables, as song 54's do, so it tests the case the words' check worries about.
**Check.** The lyric file's words match the locked lyric line for line. Song 49 is run under the engine with and without the form and reported, and no trial in the window reads it before the rule is fixed.

### 749.144 Song 58: the second carrier, bars with nothing sung
**Problem.** Even with the form, song 58's chosen tune stays under the kept 10th of rhythm scaling (0.550 against 0.574), and its builds under the 25th.
**Evidence.** Window 201: song 58's builds 0.555 to 0.592, its bars unsung 0.084 to 0.114 against kept quartiles 0.12, 0.19, 0.28. Its room file says its lyric leaves little room. The rhythm-memory study found bars with nothing sung carry rhythm scaling (+0.58) as well as slow change in busyness (+0.68).
**Fix.** Rule first: plan a bar with nothing sung where the lyric's room file shows a section end that can take one (after a verse's fourth line, before a chorus). Add only as many as bring the song's bars unsung to the kept 25th. Try it against the pool standard and the length limits.
**Check.** Song 58's builds' rhythm scaling at or over the kept 25th; bars unsung inside the kept quartiles; the song within the kept lengths; the soundness rule and the pool standard hold; songs 49 and 59 read only.

### 749.145 One neighbour block reads the ceiling from a study, not the table
**Problem.** `neighbour.py`'s 749.134 block takes the ceiling from `studies/commonest_pitch/result.json`. The engine takes it from `tables/kept_commonest_pitch.json`. When 957 remade the table, the block's source lagged.
**Evidence.** Rerun, `neighbour_v44.json` matches byte for byte up to that block, where the committed file reads a chorus ceiling of 0.474 and the rerun 0.479. The headline figures are above it and match.
**Fix.** Read the ceiling from the kept table, as the engine does, and rerun `neighbour.py`.
**Check.** A rerun of `neighbour.py` matches the committed file byte for byte.

## Added from song 61 (running tab)

Song 61, "This Side of the Door" (`songs/p71`), was written under v44 as merged (main 3b83673), as built and with the verse sung closer; the two records are the same byte for byte. Its test report holds the readings.

### 749.146 The verse lever's range misses most verse lines
**Problem.** The verse sung closer (749.142) acts only on verse lines of 6 to 8 syllables. Song 61's verse lines run 8 to 11 syllables (8.6 at the middle), so no line is a candidate; song 59's run under 6. In two songs of the last three the lever does nothing.
**Evidence.** `songs/p71/lyric61.song.json` is the same under `LUTHIER_VERSE_CLOSER=apart` as without it. The engine gives a 9-syllable line two bars, as it does a 6-syllable one; song 61 runs 264 seconds, past the kept 75th, with bars unsung 0.06 (kept 0.12 to 0.28).
**Fix.** Rule first: read the kept share of verse lines in one bar by syllable count up to 11, and let the lever take any verse line whose length kept songs put in one bar at least as often as they do 8-syllable lines; keep the guard on verse over chorus and the words' check on the chosen tune.
**Check.** The lever acts on songs 61 and 54; the checks of 749.142 hold; songs 49 and 59 read only.

### 749.147 A short line in a long slot puts its length on its weak words
**Problem.** A line of four syllables given two bars spends the bars on its unstressed words. The words' fit does not see it.
**Evidence.** Song 61, "Three, and then two" (verse 3 and the last chorus): "three" a quarter of a beat, "and" two and a quarter beats, "then" three and a quarter. The chosen tune's words' fit was 0.363 and passed. Fixed by hand in the second edition ("three" a beat and a half on the downbeat, "and then" quick, "two" on the next downbeat; `songs/p71/hand61.py`), the fit rises to 0.404.
**Fix.** Rule first: read, in kept songs, where the length of a short line (five syllables or fewer) in a slot of two bars or more falls, stressed or not. If Luthier's builds put it on weak syllables more than kept songs do, either give such lines one bar or make the fit count held length by stress within a line.
**Check.** No chosen tune holds a weak syllable of a short line longer than its stressed ones, unless kept songs do so as often; the words' fit does not fall.

## Added from song 12, second edition (running tab)

Song 12, "Wood and Cloth" (`songs/p12`), a five-stanza 87 87 Christmas hymn in 3/4 for congregation, choir and organ, rewritten on 21 November by the sketch path (song 53's hymn-mode tools, adapted to a trochaic metre), since Luthier does not yet write 3/4 or hymns. These are for when hymn mode is ported. Its test report holds the readings.

### 749.148 The song-wide peak band does not fit a hymn whose last stanza carries the descant
**Problem.** 749.17 puts the song's high point at 0.65 to 0.85 of the song as performed. A strophic hymn with a last-stanza descant and full organ peaks in its last stanza by design.
**Evidence.** Song 12 peaks at bars 85 and 86 of 88 (the descant's G5 over "cloth," full organ), 0.97 of the song. Its release before the peak is stanza 4, choir alone (bars 53 to 68, 0.60 to 0.77), and the organ's return at bar 69 (0.78) is the fresh re-entry 749.19 asks for, late. The shape is the standard one for a hymn with a final-verse descant (Willcocks, "O Come, All Ye Faithful," Carols for Choirs 1, 1961).
**Fix.** Rule first: read the high point's place in hymns with a last-verse descant or reharmonization; give hymn mode its own band, or exempt a final stanza that is marked as the climax.
**Check.** Song 12 reads inside the hymn band; songs 52 and 53 still read inside theirs.

### 749.149 The hymn judge does not read a line's shape or where the tune sits
**Problem.** The charge against the 3/4 hymn quartiles reads intervals, steps, range and rhythms, but not where in the range each line sits or whether it rises and falls.
**Evidence.** Song 12's least-charge pick (2c26d99ebe1c, charge 0.406) kept line 1 inside D4 to F#4. In an A B A C form, line 3 repeats it, so half the hymn sat in a third; the tie at the same charge (build 1060) climbs D4 to D5 and was chosen by ear. 2,630 of 3,000 builds survived (87.7%): the gates decide too little.
**Fix.** Rule first: read, in the kept hymns, each line's median pitch and its highest note's place in the line, and charge against their quartiles; in a form with a repeated line, read the repeated line twice.
**Check.** Song 12's judge picks a tune whose line 1 reaches the octave or within a step of it; songs 52 and 53's picks unchanged or better on the new reading.

### 749.150 The four-part search lets an augmented second and low thirds through
**Problem.** Song 53's beam search (the four-part setting) has no cost for an augmented second in a voice and none for close intervals low down (Module 9.14: no third below F3, no second below C4). A slurred melisma copies the chord under it, which can leave parallel octaves.
**Evidence.** Song 12's stanza 4 bass went G2, B-flat2, C-sharp3 (fixed by hand). Its first harmonization put a third below F3 in 90 samples of 6 ticks and a second below C4 in 20; with two costs added (`songs/p12/harmonize12.py`) the choir has none and only the men's unison tune against the organ bass remains (23). The melisma hold left one parallel octave, soprano and tenor, E to F-sharp in bar 10, removed by a pass after the search.
**Fix.** In the setting module: cost an augmented second in any voice; cost the two low intervals; check parallels across a melisma inside the search, not after.
**Check.** Song 12's three settings and song 53's rerun with no augmented second, no low interval in the choir and no parallels, with no hand edits.

### 749.151 The room check cannot read a strophic hymn
**Problem.** `lyric_room.py` lays a lyric out on the 4/4 engine, so it cannot run on a 3/4 hymn.
**Evidence.** Song 12's locked lyric: not run. Its room is in the holds at every line end and a stanza for choir alone, which the check does not count.
**Fix.** With hymn mode: lay a hymn out on its metre's line template, count line-end holds and unaccompanied stanzas as room, and read against kept hymns.
**Check.** Song 12's and song 53's lyrics read; songs 58 and 61 unchanged.

### 749.152 A rhythm shared by every stanza must be read for how long each weak syllable is held
**Problem.** In a strophic hymn one rhythm carries every stanza. The mouth test and the column test read where stresses fall, not how long each syllable is held, so a rhythm chosen for one stanza's words can hold weak syllables long in the others.
**Evidence.** Song 12's second edition gave bars 5, 7 and 13 two even dotted quarters, for "one stone," "stone rolled" and "star laid." Across the five stanzas the figure helped 3 of 15 word pairs and held the weak syllable as long as the strong one in 12 ("a-gainst," "be-neath," "the," "a," "to," "and"); an outside reviewer caught it. The third edition makes those bars a dotted quarter, a slurred passing eighth and a quarter; no weak syllable in any stanza is now as long as the strong one before it (`songs/p12/consistency12.py`).
**Fix.** With hymn mode: for every bar of a strophic tune, read each stanza's syllables against the note lengths; a weak syllable held as long as or longer than the stressed one before it dies unless kept hymns do so as often at that place; a pair of heavy words in one stanza does not license an even bar for all.
**Check.** Song 12's second-edition rhythm dies at bars 5, 7 and 13; its third edition and song 53's tune live.

## Closed

749.139 (957), 749.140 (chance; per build), 749.141 (not a fault; the held reading agrees, `studies/review29_verse_closer/held_weak_top.py`). 749.138 becomes 749.142 and 749.144.

## Carried

749.125 (song 60 as a practice song), 749.127 (the "seen before writing" line: kept), 749.109, 749.116, 749.103, 749.101, 749.61.
