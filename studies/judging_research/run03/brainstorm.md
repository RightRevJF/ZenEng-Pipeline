# Run 03 brainstorm (23 November 2026)

Three imaginers with fixed stances, then the Skeptic, then answers. Each was given card_1.md (Ollivier 2009), card_2.md (Devriendt & Lambiotte 2022), the Consensus scout's notes, run 02's first_principles.md and chair.md, and the maintainer's results on main (within-artist −0.042; fresh McGill −0.028; the spectral gap's renaming and split-half checks). Measure-side checks run by the imaginers used the notes only; no cover count, version or year was opened. Their scratch scripts are not in the repo.

# Round 1

## The Geometer, round 1

**Design rule for all three.** On graphs of 3 to 11 chords, curvature mostly measures size. In my check on 979 Hooktheory songs, mean edge κ had ρ −0.62 with distinct chords, and min p had −0.85. So each measure is compared with the same song's chords put in a different order. Shuffle the chord order within each clip, keeping the counts and clip lengths: 40 shuffles, seed 0, fixed in advance. The graph pools all of a song's clips. Each clip wraps back to its first chord, repeated chords are merged, and a chord is its root on the tonic plus its quality. No outcome was read.

**G1. Contraction beyond the vocabulary (Ollivier, Props. 20 and 29).**
*Mechanism:* positive κ means neighbouring chords lead to the same next chords. The walk then contracts, and the gap is at least κ, so the harmony offers routes that can stand in for each other. A loop is flat (κ = 0), which makes the bound empty.
*Measure:* κ̄_x is the traffic-weighted mean edge κ minus its shuffle mean. Settings fixed: laziness ½, undirected hop distance, exact linear program. First an audit: g_lazy ≥ κ_min must hold on every song, or the code is wrong.
*Check on 180 songs:* ρ −0.62 with ch_rep, +0.30 with chord count; split-half 0.60.
*Prediction (extrapolation: routes that stand in for each other give room to re-harmonise):* +0.04 SD per SD within artist. Repetition alone would carry only about +0.026 (0.62 × 0.042). With ch_rep held: +0.02.
*Kill:* raw ≤ +0.026, partial ≤ 0, or the halves split. Any of these means curvature is repetition renamed.

**G2. Out-and-back links (Devriendt–Lambiotte, Theorem 2 and cut nodes).**
*Mechanism:* a link whose spanning-tree probability c·ω equals 1 is a bridge. The song only ever makes that move out and back (a pendulum or a neighbour chord), and no other road joins the two chords. The end chord that still has other links is a cut node (p ≤ 0).
*Measure:* the share of distinct links with c·ω = 1, unit weights, no settings.
*Check on 1,223 songs:* non-zero in 28% of songs; ρ −0.04 with ch_rep and +0.06 with chord count; split-half 0.51. So this is a new axis, not size or repetition.
*Prediction (extrapolation: a bridge is a step nothing can replace; tree-like means negative curvature, a bottleneck):* −0.03.
*Kill:* weaker than −0.01, or the halves split.

**G3. The obtuse statue (card 2's circumcentre).**
*Mechanism:* using the resistances ω as squared lengths, the chord graph becomes an exact simplex in R^(n−1). This is Jason's song in a Hilbert space. The curvatures p are the barycentric coordinates of the simplex's circumcentre. If min p < 0, the circumcentre lies outside the simplex, beyond one chord: the statue is obtuse and leans on a hub.
*Measure:* mean p is exactly 1/n, so use min p, compared with its shuffle mean (pmin_x).
*Check:* |ρ| ≤ 0.2 with chord count, ch_rep and chord surprise. But split-half is only 0.37, and ρ is −0.45 with G2.
*Prediction (extrapolation: a hub chord means plain harmony centred on home, which fits chord surprise −0.042):* the more obtuse, the more covers, −0.02 per SD of pmin_x.
*Kill:* ≥ 0. With an SE of about 0.016, power is low. Treat it as a lead: one term, judged at .025.

**Order of testing.** Freeze each rule before any outcome is read. Test it first on Hooktheory, within artist, holding chord count n, links and first year. The McGill hold-out stays untouched until a measure has passed there.

*Notes from the Geometer's checks:* the lazy spectral gap on pooled Hooktheory graphs had ρ −0.67 with chord count, against +0.02 for the non-lazy g on McGill, so the repo's results for g may not carry over to Hooktheory unchanged. Time-reversal asymmetry of Ollivier curvature (forward walk against reversed walk) was also tried: zero in 49% of songs, split-half 0.20, dropped.

## The Listener, round 1

When a musician learns a song by ear, they are building a map of where each chord can go next. When they re-arrange it, they swap one chord for another that does the same job. Ollivier curvature measures exactly that kind of interchangeability.

**L1. Substitutable chords (Ollivier κ, Prop. 20).**
*Mechanism:* κ(x,y) > 0 means that after hearing chord x or chord y, the listener expects much the same next chord. By Prop. 20, the listener's sense of where they are shrinks by a factor of (1−κ) with each chord. So x and y work as stand-ins for each other (ii and IV both lead to V), and a coverer can swap one for the other without breaking the song.
*Measure:* kbar, the move-weighted mean of lazy κ over observed chord changes. Fixed in advance: laziness α = ½; distance = shortest path on the undirected chord graph; chord = root relative to the key plus its quality; repeats merged; each clip wrapped back to its first chord; clips pooled per song. Residualise on the ranks of distinct chords and edges.
*Checked tonight on 2,893 songs (measures only):* raw kbar tracks size and surprise (chord count −0.57, chord surprise −0.47). After residualising: repetition +0.04, chord surprise −0.07, lazy g +0.26. Between two different clips of the same song, residual kbar agrees at 0.26. g ≥ min κ held for every song, as Prop. 29 requires.
*Prediction (extrapolation):* **+0.03** SD of log(1+covers) per SD, within artist, with repetition held. Musicians cover songs whose chords have stand-ins.
*Killed if:* below +0.015, or the two artist halves disagree in sign, or adding chord surprise takes away more than half of it.

**L2. No detour (resistance, Devriendt–Lambiotte Thm 2).**
*Mechanism:* a link with c·ω = 1 is in every spanning tree, so it is the only road between two parts of the harmony. A coverer cannot re-route it. Songs that put a lot of their movement on such roads leave less room to re-arrange.
*Measure:* the share of symmetrised move traffic on bridges (self-loops dropped, graph as in L1).
*Checked tonight:* |ρ| ≤ 0.04 with chord count, repetition and surprise; clip-to-clip agreement 0.19; 67% of songs score exactly 0, so test it as bridged against not bridged.
*Prediction:* **−0.025** within artist.
*Killed if:* ≥ 0, or the halves disagree in sign. The opposite reading is that a bridge is the one move listeners remember, so a positive result would favour memory over room to re-arrange.

**L3. Inverted curvature–repetition ordering.**
*Mechanism:* a musician needs a song that is learnable (it converges, L1) but not yet used up (low ch_rep). Exposure wears out a loop; it does not wear out a grammar.
*Measure:* none new. Add kbar × ch_rep (both standardised) to L1's model.
*Prediction:* the interaction is **negative, about −0.02**.
*Killed if:* ≥ 0. Low power: exploration, not a test.

*Facts from the Listener's checks (measures only):* on Hooktheory, lazy g has a median of 0.33 and tracks chord count at −0.69. Only 24% of songs have min κ > 0. Clip-to-clip agreement after residualising: kbar 0.26, bridge share 0.19, lazy g 0.12.

## The Inventor, round 1

**I1. The melody as a contraction of the harmony (Ollivier, melody and chords together).**
*Mechanism:* take Ollivier's κ = 1 − W1(m_x,m_y)/d(x,y), let m_x be the melody notes heard over chord x and d the transport distance between the two chords' tones. Positive κ means the tune moves less than the chords under it: a tune that keeps fitting when the chords are swapped.
*Measure:* κ_mel. For each chord change x→y (merged; clip wrapped), W1 between the duration-weighted melody pitch classes over x and over y, divided by W1 between x's and y's chord tones (uniform), both on the 12-semitone circle. Average over changes, weighted by count; skip d = 0. Fixed: the circle metric, duration weights, the wrap rule.
*Checked tonight (no outcome):* 2,765 songs computable. Median −0.80 (10th–90th −1.99 to +0.03). ρ +0.15 with ch_rep, −0.20 with distinct chords. Clip-to-clip ρ 0.19 (different sections, so a floor).
*Prediction (extrapolation, after Prop. 20's contraction):* +0.03 within artist, holding ch_rep and distinct chords.
*Kill:* below +0.01, halves split in sign, or ρ above 0.7 with chord-tone share (already failed).

**I2. Tonic resistance: is home the electrical hub? (Devriendt–Lambiotte; commute-time theorem).**
*Mechanism:* make the chord graph a circuit, with move counts as conductances. Low resistance from every chord to the tonic means many parallel routes home; an arranger can take detours without getting lost.
*Measure:* H = Σ_x π_x ω(x,T) / Σ_y π_y Σ_x π_x ω(x,y), T the busiest chord on the key tonic. H below 1: home more central than the average chord.
*Checked tonight:* 2,612 songs; median 1.66 (the denominator carried an extra ½; ranks unchanged); ρ −0.43 with distinct chords, +0.14 with ch_rep; clip-to-clip 0.25.
*Prediction (extrapolation):* −0.03 within artist, holding distinct chords and ch_rep. Home closer, more covers, in line with "plainer chords, more covers".
*Kill:* weaker than −0.01, or ρ above 0.6 with chord surprise (checked before any outcome).

**I3. The cover done on the computer (perturbation bound W1(π,π′) ≤ ε/κ).**
*Mechanism:* a cover swaps chords for close substitutes; a walk that contracts keeps its centre of gravity when that happens.
*Measure:* R: for every single-chord substitution that keeps two of three tones within the key (I↔vi, I↔iii, IV↔ii, V↔iii), the W1 shift in the stationary chord-tone distribution divided by the W1 size of the swap; mean over substitutions. Table fixed in advance. Not yet computed.
*Prediction (bold):* −0.03 (more robust, more covers), holding g and ch_rep.
*Kill:* ≥ 0, or ρ above 0.7 with g.

# Round 2

## The Skeptic, round 2

**Rules for every test.** Hold artist fixed effect, first year, clips per song, distinct chords, edges and ch_rep. More clips means more edges and fewer bridges. Clip count probably also tracks fame, because users transcribe more sections of famous songs. So clip count can push covers directly. At a reliability of 0.2 to 0.6, a true effect of +0.03 shows up as about +0.015 to +0.023, which is near the SE of about 0.016. Freeze the rules and correct for the number of tests run.

**About the gap on Hooktheory.** The lazy gap tracks chord count at −0.67 to −0.69, while McGill's non-lazy g tracks it at +0.03. So on pooled Hooktheory graphs, lazy g mostly measures size. McGill's renaming check and its 0.58 split-half do not carry over. Testing "g" on Hooktheory needs the non-lazy version or a version residualised on size, with its stability checked again. Otherwise it is a new and untested measure. I3, which holds g fixed, and L1's "+0.26 with lazy g" inherit this problem.

**G1.** After the shuffle, curvature still correlates −0.62 with ch_rep, so it is mostly "chords that move" renamed. The partial with ch_rep held (+0.02) is the only new claim, and it cannot be detected at this power. Merge it with L1.

**L1.** The same κ̄, residualised on size instead of the shuffle. That leaves ρ +0.04 with ch_rep but −0.07 with chord surprise, and clip-to-clip agreement of only 0.26. Adding chord surprise could wipe it out. It is the best candidate as one merged test: residualise on size, hold ch_rep and surprise, and keep L1's kill rule.

**G2/L2.** The same bridge measure, and really a new axis (|ρ| ≤ 0.06 with size, repetition and surprise). But the score is zero in 67–72% of songs, so test bridged against not bridged as one merged test. Agreement is 0.19 to 0.51. Clips per song is the key confound to hold. It runs fast.

**G3.** Split-half 0.37, ρ with G2 −0.45, and the raw score tracks size at −0.85. Its prediction leans on chord surprise. Lowest power of the three.

**L3.** An interaction between two noisy measures, each at a reliability of about 0.26, has no realistic power. Exploration with nothing that could kill it.

**I1.** Not really Ollivier's κ: d is not a graph distance, and the median is −0.80. The ratio blows up when d is small. Agreement 0.19. Tune measures have failed five runs, and chord-tone share has already failed. Check ρ with chord-tone share before reading any outcome.

**I2.** "Home is central" is plain harmony, so probably chord surprise renamed. It also tracks size at −0.43 and overlaps G3. Its own gate (ρ with surprise) can run tonight, but not the outcome test.

**I3.** Not computed, no reliability check. The substitution table is arbitrary, and the measure holds a g that only measures size on Hooktheory.

**Verdicts.** G1: DROP (merge into L1). L1: RUN TONIGHT (merged κ̄, ch_rep and surprise held). G2 and L2: RUN TONIGHT (one merged bridge test, clips held). G3: LATER. L3: DROP. I1: LATER (gate on chord-tone share first). I2: LATER (only its surprise check tonight). I3: LATER (needs computing and a stability check).

## The Geometer, answer

**G1: withdrawn.** It goes into L1's merged test: κ̄ residualised on size, with ch_rep and chord surprise held, under L1's kill rule. My one new claim, a partial of +0.02, cannot be seen at this power.

**G2: merged with L2, run tonight.** The test is bridged against not bridged, holding clips per song, distinct chords, edges, ch_rep, first year and artist. Prediction: −0.03 per SD of the indicator, about −0.065 SD of log(1+covers) for a bridged song. Killed if weaker than −0.01, or if the artist halves split.

**G3: later.** The barycentric reading stays a description, not a test.

**The gap g on Hooktheory.** g is not tested on Hooktheory until it passes two gates, each run without outcomes: (1) compute g on each clip by McGill's rule, unchanged (not lazy, not pooled), then average over clips weighted by chord count; it passes if |ρ| with distinct chords is under 0.3 and split-half is at least 0.5 (across clips, for songs with two or more). (2) If it fails, residualise on n and edges with a linear rule fixed in advance, and check stability again. If both fail, g stays out of every Hooktheory model, I3's included.

## The Listener, answer

**L3: withdrawn.** It multiplies two measures that each repeat at only about 0.26 between clips, so it has no power and nothing could kill it.

**L1: kept, merged with G1.** I drop my "+0.26 with lazy g" line, because lazy g mostly measures song size on Hooktheory. Revised measure: kbar residualised on the ranks of distinct chords, edges and clips per song, with ch_rep and chord surprise held. Kbar barely tracks clips per song (ρ −0.08). With a reliability of 0.26, a true +0.03 would show as about +0.015. Revised prediction: **+0.015 to +0.02**. Kill rule, made fairer: dead if the estimate is ≤ 0, or the halves disagree in sign, or chord surprise takes away more than half of it. It passes only at p < .025.

**L2: merged with G2, as one indicator: does the song have any bridge?** The indicator is the same under both definitions. Checked tonight, measures only: 33% of songs have a bridge, and the share rises with clips per song (29%, 34%, 41% for one, two, three or more clips). That is the opposite of the Skeptic's guess that more clips mean fewer bridges, but it confirms clips per song is a confounder. Hold it. Prediction **−0.025**; dead if ≥ 0 or the halves disagree in sign.

## The Inventor, answer

I accept the verdicts. Both gates below were run tonight on notes only, with no outcome read.

**I2: gate passes.** Over 2,612 songs, the Spearman correlation of H with chord surprise is −0.14. With distinct chords held, the partial is +0.11, so the sign flips. Either way it is far below my 0.6 kill line, so H is not chord surprise renamed. It still tracks size (−0.43). It stays LATER, with the Skeptic's full set of controls, clips per song included. I concede the overlap with G3: run whichever of the two is more stable, not both.

**I1: revised, still LATER.** Against chord-tone share, ρ is −0.28 (−0.27 with chord count held), under the 0.7 gate. The Skeptic is right that this is not true Ollivier κ and that the ratio is fragile when the chord move is small. I would replace it with the difference W1(melody) − W1(chord tones), which drops the division. Its clip-to-clip agreement of 0.19 makes it weak. It goes only after a stability recheck.

**I3: withdrawn.** It was never computed and it leaned on a gap that, on Hooktheory, mostly measures size.

## Where the four agreed and split
- **Agreed:** on tiny chord graphs curvature mostly measures size, so every curvature measure must be compared against size (shuffle or residual) and must hold clips per song. The bridge indicator (G2 = L2) is a new axis and runs tonight. G1 folds into L1. L3 and I3 are withdrawn.
- **Split:** the Geometer wants size removed by shuffling the song's own chords (keeps the vocabulary, destroys the order); the Listener by residualising on ranks of size. The Geometer's shuffled curvature still tracks repetition (−0.62), the Listener's residual does not (+0.04), so the two are different measures. On the gap g, the Geometer would rescue it with McGill's per-clip rule; the Skeptic thinks pooled lazy g on Hooktheory is just size.
