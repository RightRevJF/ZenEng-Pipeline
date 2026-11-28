# Card 2: McBride & Fitch, "Contrasting statistical patterns in melodic and molecular evolution reveal distinctive constraints in a culturally evolving system"

## 1. Citation and copy read
McBride, J. M. & Fitch, W. T. (Univ. of Vienna). arXiv:2607.12673.
- **Read:** https://arxiv.org/html/2607.12673 in full, over five WebFetch passes: the body, the supplement §1–8 and the bibliography (about 109 refs).
- **Metadata:** the v1 abs page gives 14 Jul 2026, q-bio.PE plus cs.SD and physics.soc-ph. One of two abs fetches showed no header.
- **Not reached:** the figure images (so no per-position values), and the code and data (github jomimc/TheSessionEvo, zenodo 21356647).
- **Caveats:** WebFetch summarises, so all numbers are as it reported them. It also noted some internal inconsistencies in the paper: part length "8 or 4" vs "8 or 16" bars, and 328 vs 242 Savage pairs.

## 2. Claim and data
**Claim.** Once variants are aligned with rhythm taken into account, melodic variation differs from protein evolution in four ways:
- Rare pitches mutate most.
- Substitutions are mostly small steps.
- Conservation follows metrical strength.
- Covariance comes in bands one bar apart, produced by repetition.

The authors put this down to memory, motor and social biases. They propose a ***stable melodic skeleton*** on strong beats that carries the tune's identity.

**TheSession, used directly.**
- **Source:** the TheSession-data GitHub dump (no date given): 54,075 settings in 22,702 families. Families are the site's own tune pages; 1,874 have more than 5 settings.
- **Dropped:** settings that failed parsing (1,972); grace notes, chords or multiple voices (4,642, dropped rather than cleaned); unmatched repeats (6,001); music21 failures (590). Also waltzes, tunes that change meter, and user-composed tunes. That leaves **41,050** settings in 4/4, 6/8, 2/4, 9/8 and 12/8.
- **Parts:** pickups removed; any bar of the wrong length, or a bar count that is not a multiple of 8, excludes the tune. Tunes are cut into 8-bar parts, merged into 16-bar parts when pitch identity is at least 80% (98% correct on 126 hand-checked variants).
- **Pitch:** transposed to tonic C and reduced to pitch class.
- **Pairs:** an all-vs-all MMseqs2 search found about 4 million hits (e < 0.001). Requiring the same meter and bar count and PID > 50% leaves **51,680 part pairs**. (My reading: some pairs may cross family labels.)

**Other corpora.** Meertens (18,618 songs) is used only for testing family identification. Bronson ballads and Japanese folk songs come in through Savage et al.'s alignments. **No Essen.**

## 3. Is the measure from the notes?
**Yes.**
- MIDI pitch and duration are placed on a grid whose step is the smallest common duration unit; each note fills d/G cells.
- Two parts with the same meter and length are compared cell by cell, with no gaps. Splitting or merging notes therefore costs nothing.
- No audio, listener or popularity data enters.

## 4. Effect sizes and how they were checked
**Central construction:** Dayhoff/BLOSUM log-odds substitution matrices.
- **Log-odds:** S(c,c′) = log[p̂(c,c′)/(p̂(c)p̂(c′))], computed for each mode (12×12).
- **Mutability:** μ(c) = substitutions of c ÷ occurrences of c.
- **Positional conservation:** the substitution rate at each eighth-note slot in the bar.
- **Covariance:** covariance of a Boolean match matrix, split into a repetition part and the rest.
- **Weighting:** each part gets weight q^−0.5 (q = its share of all pairs), to stop tunes with many settings dominating.
- **Not used:** phylogenies, gamma site rates or mutation spectra.

**Results.**
- **Mutability vs prevalence:** r = −0.95 for pitch, against r = 0.30 (p = 0.2) for amino acids. Bronson r = −0.81 (n = 9); Japanese r = −0.84 (n = 8). Tonic and dominant are the most stable notes. The pattern holds in every mode except minor.
- **Interval size:** substitution rate tracks the interval distribution, r = 0.98 (n = 13). Log-odds fall by about 20% per semitone (r = −0.82).
- **Meter:** substitution rate against an expert metrical hierarchy (source not stated) gives r = 0.71, p = 4.8×10⁻⁷, across 5 meters. Downbeats are the most conserved positions and bar ends the least, in every meter and dance type.
- **Covariance:** the periodicity is reproduced by repetition alone.
- **Key-finding:** a Krumhansl–Schmuckler variant using profiles built from TheSession itself is 76% accurate overall, and about 65% from the first 10 eighth notes (chance 12.5%). The 10 most-conserved notes beat the 10 least-conserved by about 34 points. Pitch-class entropy is 3.05 bits overall and 2.75 within a key and mode.
- **Pitch-only alignment fails:** only 13% of Savage's pairs have a unique best alignment.

**Checks.**
- Replications within each mode and meter; bootstrap CIs on one figure.
- Sensitivity analyses are mentioned but not shown.
- **No null model, no held-out test** (the key profiles are trained and tested on the same corpus), and no correction for multiple tests. Most correlations span only 8–13 categories.

## 5. Lasting love and covers: what cuts against the stance
The paper never analyses tunebook counts, recordings, survival or quality.

**Against "greatness readable from the notes":**
1. **What is conserved is the typical.** Common pitches, tonic and dominant, strong beats and small steps persist. These are properties of the whole system, not of individual tunes. *My extrapolation:* a feature of the notes that "predicts" success may be measuring typicality, not greatness.
2. **Transmission is partly social.** The authors explain skeleton stability partly by ensemble conformity: wrong pitches on strong beats are audible in a session. Their Prediction 1 expects more stability in ensemble traditions than in solo ones, which puts that cause outside the notes.
3. **Identity is not quality.** The skeleton tells you which tune it is. Nothing in the paper links how conserved a tune is to how much it is loved.
4. **Representation choices drive the results.** Pitch-only alignment largely fails, and grid alignment has to drop ornaments, waltzes and irregular tunes.
5. **Settings counts had to be down-weighted.** *My extrapolation:* the settings count tracks popularity, so variability and popularity are entangled by construction.

**For the stance:**
- Variation is far from random and is shaped by cognition.
- The authors suggest stability is kept by selection on learnability and memorability, which are properties of the notes.
- Their Prediction 4 is that listeners recognise a tune from its skeleton.

The notes plausibly carry what makes a tune transmissible. The step from there to "loved" is untested.

## 6. Methods and measures for this pass (TheSession, melody only)
**Setup (nothing fitted):**
- Parse the ABC. Strip grace notes and decorations rather than dropping the tune. Remove pickups.
- Transpose to the annotated tonic and reduce to pitch class.
- Quantise to an eighth-note grid (sixteenths if needed), with each cell holding the sounding pitch.
- Cut into 8-bar parts.
- Compare settings of a tune only when they have the same meter and bar count, cell by cell.

**M1. Tune variability.** The mean of 1 − PID over pairs of settings, where PID is the share of matching cells (so it is weighted by duration).
- **Could rename:** the settings count and note density.
- **Control:** use a fixed number of randomly drawn pairs per tune (only tunes with at least 3 settings). Report its correlation with the settings count first.
- **Stability:** split the settings into random halves and correlate the two half-estimates.

**M2. Core (skeleton).** Per grid slot, consensus = the share of settings with the modal pitch class there. Core = slots with consensus ≥ 0.8. A version with nothing chosen at all: the pitch classes on main beats (beats 1 and 3 in 4/4, 1 and 2 in 6/8).
- **First check:** reproduce the paper's gradient (downbeats most stable, bar ends least; bars 3 and 7 the most variable).
- **Stability:** two-setting agreement on core vs off-core cells.

**M3. Features on the core.** Compute distinct pitch classes, interval entropy, range, contour turns and repetition on the core sequence only.
- **Test 1:** is the between-settings ICC higher than for the same feature on the full surface?
- **Test 2:** does the core version predict tunebook counts or distinct artists better, holding type, mode and settings count fixed?
- A feature that is unstable across settings cannot diagnose *the tune*.

**M4. Typicality vs distinctiveness.** Use leave-one-out pitch-class backgrounds for each mode × type.
- **Typicality:** the mean log-probability of the core pitches.
- **Distinctiveness:** the share of rare pitch classes on core cells.
- **Could rename:** the tonic and dominant share.
- **Skeptic's test:** do outcomes track typicality rather than distinctiveness?

**M5. Repetition index.** The share of cells in bars 5–8 that equal the cells 4 bars earlier, plus a one-bar-lag version.
- **Could rename:** compression or n-gram repetition.
- **Stability:** compare the index across settings.

**M6. Variation profile.** Among the mismatched cells between settings, the share that are steps rather than leaps, and the share on weak rather than strong slots. This gives the kind of variation (ornamental or structural) rather than the amount.

**M7. Tonal clarity.** Run Krumhansl–Schmuckler with the published profiles on the first 10 eighth notes and on the core. Record whether it matches the annotated key, and whether two settings get the same result.

**Caveat (mine).** Settings are user transcriptions, often copied from recordings or from each other. Some of the variation is transcription noise.

## 7. Leads
1. Savage, Passmore, Chiba, Currie, Suzuki, Atkinson (2022). "Sequence alignment of folk song melodies reveals cross-cultural regularities of musical evolution." *Current Biology*, doi:10.1016/j.cub.2022.01.039. The mutability and substitution findings re-tested here.
2. Janssen, Burgoyne, Honing (2017). "Predicting variation of folk songs." *Frontiers in Psychology*, doi:10.3389/fpsyg.2017.00621. Predicts phrase stability from note features; relevant to defining a "core".
3. Street, Eerola, Kendal (2022). "The role of population size in folk tune complexity." *Humanities and Social Sciences Communications*, doi:10.1057/s41599-022-01139-y. Demographic confounds on complexity.
4. Youngblood (2019). "Conformity bias in the cultural transmission of music sampling traditions." *Royal Society Open Science*, doi:10.1098/rsos.191149; arXiv:1906.11928. Social copying drives spread.
5. Anglada-Tort et al. (2023). "Large-scale iterated singing experiments reveal oral transmission mechanisms underlying music evolution." *Current Biology*, doi:10.1016/j.cub.2023.02.070. Which structures survive transmission.
