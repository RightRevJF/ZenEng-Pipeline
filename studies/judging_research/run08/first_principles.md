# Run 08: first principles

27 November 2026. Recommendations only; nothing is dropped without Jason.

## 1. Bedrock
**Facts.**
- Six counted tests (power 0.21 to 0.69): three killed, three passed.
- **Killed:**
  - chord repetition on fresh songs (−0.003 against −0.04);
  - key travel (−0.031 against +0.05);
  - the timeline slope (0.91 against 1.10).
- **Passed:**
  - the ii-V share within composer (+0.073, SE 0.018);
  - chord-space heritability (+0.051, p .0002);
  - the ii-V share on 2,707 unseen singletons, written after seeing results (+0.057, SE 0.019).
- Pure copying is rejected (sublinear). The urn leaves at most 48% of late-cover spread for anything about a song.
- Holding early covers, IIV says nothing about late covers (+0.006, SE 0.032).
- The ii-V signal sits in jazz genres: +0.087 there, against +0.021 elsewhere. Heritability halves after 1950.
- All 8,640 matched ChoCo songs are now seen.

**Assumptions.** A chart stands for the song (chart writers agree only 0.31 to 0.67); artist sets mean the same in jazz as in pop; the composer effect absorbs fame.

## 2. Question every requirement
- **Yardstick.** Love has gone unused since run 02. In jazz, recording standards is the convention. Flag: standardise covers within genre.
- **Notes only.** Keep it. But iReal charts are written by the players whose recordings make the outcome. iiv_source (power 0.06) could not separate the two.
- **Charted tunes.** A tune gets a chart because players play it: selection on the outcome.
- **Composer match.** Sound (8,003 of 8,640 writer matches; writer-only readings agree), but not within performer, and singletons hold no composer.
- **Measures.** The gates do not check for chart-writer leakage. Flag: a cross-source gate of at least 0.5.
- **Rulings.**
  - The power floor and range kill worked: kills fired 2.6 to 6.4 SE out.
  - No K was consistent, and an assumed composer share (0.3) set the counted list. Flag both.
- **"Test everything tonight."** It spent every matched song. Flag: hold back a confirmation batch.

## 3. Delete (recommended)
- **ch_rep as a predictor.** Killed at −0.04. Its range still holds main's −0.026, so keep it as a control.
- **TRAV5 and E (key travel).** Killed.
- **β > 1 (momentum hiding fitness).** Killed. Keep β = 0.91 as a fact.
- **econ.** An estimate, with the opposite sign in all four readings.
- **Tonic resistance.** Against its prediction a fourth time.
- **T.** At power 0.79, +0.05 is excluded.
- **p_min, loop period, burstiness.** Power under 0.05; spend no unseen songs.

## 4. Simplify
**The idea, reduced.** One number per song, the ii-V share of changes averaged over its charts, against log artist sets, genre and decade held.

**Honestly:** the lead is about songs as jazz players use them, not shown for songs in general.
- Most of it sits in jazz genres.
- IIV itself marks Medium Swing (+0.73 SD over Pop).
- On the Wikifonia subset, neither the Wikifonia nor the iReal reading reproduced the effect.

**Two stories fit.** Players choose tunes whose changes are good to improvise on (a song property), or iReal writers add ii-Vs to tunes they already record. Heritability may be the same finding, reached without a measure.

## 5. Speed the loop
**Written first; not run.**

**Songs (unseen):**
- the 13,225 iReal and Wikifonia charts that matched nothing in run 08 (42,002, less 6,095 stop-artist, 392 short and 22,290 matched);
- ChoCo's unparsed Real Book, Band-in-a-Box, JAAH, Isophonics, uspop2002, rock corpus and Chordify partitions (artist fields still to be checked).

(Hooktheory, Lakh or McGill re-measured would be seen or held-out.)

**Match.** Frozen before any join:
- the title equals that of exactly one Discogs-VI clique, with at least two words;
- exclude the 8,640 design cliques, the Hooktheory, fresh and Lakh sets, and Billboard/McGill;
- count the yield before reading any outcome.

**Rule.** The iiv_singletons model (OLS, HC1; w_chr, ch_rep, V, ln_chg, ln_bars, genre, decade; halves; Poisson second model), one counted test at α .05.

**Prediction.** +0.05 SD per SD, shrunk from +0.057 for winner's curse.

**Kill.** +0.05 lies outside the 95% range.

**Run it only at fake-outcome power 0.5 or more.** That needs about 1,500 matched songs.

**Frozen interpretive reading.** Non-jazz genres alone, predicted at +0.04. If the range excludes +0.04, label the finding "jazz repertoire". It counts only at power 0.2, which needs about 2,200 non-jazz songs.

## 6. The obstacle and the way through
**Obstacle.** The only chord corpus big enough for power is written and chosen by the community whose recordings are the outcome.

**Way through (speculation).**
- Read harmony upstream of covering: first-edition sheet music, copyright lead sheets, or chord recognition on the original recording.
- Then test IIV on late covers, holding early ones.
- Interim answer for Jason: one lead from the notes, probably the jazz ear's, not yet a judge of greatness.

**Addendum by the orchestrator (after this review, same pass).** The yield of section 5's title-only match was counted before any outcome was read (`experiments/posthoc08.title_only_rows()`, clique titles and ids only): **542 songs** (387 outside the jazz genres). Fake-outcome power at +0.05 is **0.04** (0.01 for the non-jazz reading at +0.04), far under the 0.5 asked. So it was **not run**, and these 542 songs stay unseen. The way to a powered confirmation is more chord charts with names from outside the iReal community (section 6), not this remainder.
