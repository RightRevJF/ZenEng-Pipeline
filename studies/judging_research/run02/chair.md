# Run 02: the chair's ranking

22 November 2026. Research only: nothing here goes into the Luthier engine. The yardstick is unchanged: a song still loved after many years, plus covers by other artists. Song 59 and its folders were not read.

Run 02 brought four cards: Ortega 2021 on who gets covered (card 1), McBride and Leroi 2026 on which Irish tunes players keep learning (card 2), Madison and Schiölde 2017 on liking that grows with hearing (card 3), and Di Marco and colleagues 2026 on note-transition networks (card 4). None of the four measures greatness from the notes against lasting love or covers. Cards 1 and 3 are about the outcome and its confounds; card 2 is the nearest thing to the covers half, but its notes add only about 3 points of explained variance; card 4 gives a new way to describe chords but no outcome that counts. So the ranking below is mostly about testing the one note finding that has held twice (chords that move within a section predict covers) against confounds that were named more sharply this run.

## 1. Early covers with the fame and chart controls in one frozen model (BUILDS ON week 01 idea 1 / J6a and the covers study's Discogs-VI replication)

**Idea.** Count only covers made within five years of a song's first release. Then test whether chords that move within a section still predict those covers once we also hold the original performer's fame (their covers on other songs) and how long and how high the song charted.

**Cards that support it.** Card 1 (the top 0.1% of artists take 41% of all covers, so the performer's cover fame has to be held). Card 3 (exposure makes liking, so chart exposure has to be held; its third leg is exactly this). Card 2 indirectly (even in musicians' own choices, prestige from recordings outweighs the notes, so a note effect has to survive prestige controls). All three debaters ended on this model in round 2.

**Prediction, written now, before any test.** Within-section chord repetition has a standardised effect of −0.05 or stronger on log(1 + early covers), pooled p < .05, with the same sign in both artist halves (artists split by name), holding: log views, first year, duration, number of Hooktheory clips, first performer or not, the original performer's Discogs-VI covers on their *other* songs (log), Hot 100 weeks and peak (0 and 101 for songs that did not chart, with a did-not-chart flag), and era bands. Then, frozen, on the McGill Billboard songs not in the 2,360 set, the sign is negative.

**Test that could fail.**
- Data: Discogs-VI (Zenodo, CC BY-SA 4.0; version groups with each release's year) joined to the 2,360 Hooktheory songs of the covers study, both re-fetched because neither is committed; a public Hot 100 weekly archive for weeks and peak. Fresh leg: `studies/harmony/billboard_sections.json` (739 McGill charts, committed) joined to Discogs-VI, dropping songs already in the 2,360.
- Fails if the pooled effect is weaker than −0.03, or the halves split in sign, or the effect is present only on covers made after year five (then it travels through fame), or it vanishes when the performer-fame term is added (then Ortega's fame loop explains it). A pass on Discogs-VI that is reversed in sign on fresh McGill songs is a fail of the "fresh" claim.
- Power, honestly: a true effect of −0.05 on 2,360 songs is detected about 68% of the time pooled and about 41% within each half. The all-covers effect was −0.071, which would be detected about 93% of the time, but early covers are fewer and noisier, so expect less. The fresh McGill leg (perhaps 400 to 500 songs after matching) has roughly 20 to 35% power: a null there settles nothing.
- Multiple testing: one primary term (chord repetition). The debate wanted two secondary terms carried in the same model, each with its own pass rule: the Geometer's spectral gap g (idea 3) and the Listener's melodic pitch-class entropy. That is three terms. The primary is judged at .05; each secondary at .025 (Bonferroni over the two).
- Weakness: the 2,360 songs are where the finding was found, so this asks *when and through what* the effect works, not *whether* it exists. Only the McGill leg is fresh.

**What Jason or the maintainer must decide.** Whether to re-fetch Discogs-VI and the Hooktheory notes. Where the Hot 100 weeks come from (the shape studies used a Hot 100 table that is not committed). Whether early covers become the covers half of the yardstick for notes-only work. Whether the two secondary terms ride along (cost: two more chances of a lucky pass, handled by the .025 rule).

## 2. Cross-style cover breadth as the outcome (BUILDS ON week 01 first_principles.md, section 6; card 1's within-genre baseline is NEW THIS RUN)

**Idea.** Count how many different genres a song has been covered in, early covers only, not counting the original's own genre. A song covered in jazz, country and punk has shown that its notes carry it without the original singer and sound, and card 1 shows that crossing a genre goes against the strongest force in covering, so each such cover is a more selective vote than a raw count.

**Cards that support it.** Card 1 (73% of jazz covers stay in jazz; crossing genres is the exception, and fame is concentrated, so breadth must be judged against the original's genre and the performer's fame). Card 2's second reading and the Geometer's round 1 both proposed breadth as the outcome. Card 3 weakly (exposure should matter least to musicians from another genre).

**Prediction, written now.** Holding log(1 + early covers), first year, the original's genre, and the performer's covers on other songs, within-section chord repetition has a partial Spearman of −0.05 or stronger with breadth, pooled p < .05, same sign in both artist halves; and its effect on breadth is larger in size than its effect on the raw early-cover count in the same model family.

**Test that could fail.**
- Data: Discogs-VI release records with Discogs genre (and style) tags, on the same 2,360 songs. **Step 0, a feasibility check that costs no outcome:** does the Discogs-VI release dump carry genre tags? If not, the Discogs API or the monthly Discogs data dump (CC0) can supply them by release id. **Step 0b (card 1's prerequisite):** most early covers share the original's genre. If they do not, Ortega's pattern does not carry to Discogs, and breadth does not mean "against the pull" here.
- Fails if the pooled partial is weaker than −0.03, the halves split, the effect on breadth is no larger than on raw count, or the effect disappears with performer fame held.
- Power: lower than idea 1. With a median of 6 covers in all, early covers will often span one or two genres, so the outcome is coarse and full of ties. Treat it as a lead even if it passes.
- Multiple testing: one term. Run after idea 1, on the same songs, so it is not independent evidence; it asks whether the note signal is sharper on a better outcome.

**What Jason or the maintainer must decide.** Whether breadth is acceptable as part of the covers half (it moves the yardstick, and so needs Jason's agreement, as week 01's first-principles note said). Genre or style as the unit (Discogs has 15 genres and about 500 styles; styles are finer but noisier). Whether to fetch genre tags from the Discogs dump.

## 3. The spectral gap of the chord graph, as a secondary term only (NEW THIS RUN, from card 4 via the Geometer)

**Idea.** Turn each song's chords into a map of moves from one chord to the next, and measure how quickly a walk on that map forgets where it began (g = 1 − |λ2|): a pure loop or a two-chord rocking vamp scores 0, harmony with more than one road out of a chord scores higher. It is a property of the harmony that a repetition count cannot see in principle, but it may be repetition, chord count or song form under another name.

**Cards that support it.** Card 4 (chord networks, its reciprocity and branching marks; in its preprint, popularity leans faintly to simpler networks in pop and rock, |r| under 0.07). Card 1 only by argument (re-harmonising across genres needs harmonic room). The Listener read it as the "surprise" half of plain tune, moving harmony. The Skeptic set three conditions: frozen rules, form held, fame held.

**Prediction, written now.** Rides in idea 1's model with repetition, distinct chords, length in chords and section count held: g has a standardised effect of +0.05 or more on early covers, pooled p < .025, same sign in both halves. Its effect on views is smaller than its effect on covers.

**Test that could fail.** Same data as idea 1. Fails if pooled under +0.03, halves split, p ≥ .025, or the covers R² is unchanged at two decimals when g is added (the Geometer's own renaming rule). Before that: the renaming check below, which needs no outcome. Power is the same as idea 1's secondary terms (under half within each artist half for an effect of 0.05).

**After the check (run after this section was written; see the end).** g is not repetition, chord count or section count under another name, so it keeps its place, but only as a secondary term. Nothing about its link to any outcome is known yet.

**What must be decided.** Whether g is worth a term at all, given that its stability within a song is still untested. Whether it is built per song (as here) or per section.

## Not ranked, and why

- **Card 2's five melody measures as their own test.** Five shape runs on about 3,100 songs found nothing in the tune on unseen songs, and note density was already tested (−0.036, p = .08). One of them, pitch-class entropy, is allowed to ride in idea 1 as a secondary term with its own rule; the other four are not tested.
- **Card 3's love-by-exposure interaction.** Chart weeks are partly caused by liking, so the interaction cannot tell wear-out from songs that charted long because they were loved; the Listener demoted it himself. Power for an interaction of 0.05 on about 900 songs is low. Kept as an exploratory reading if idea 1's data are fetched anyway.
- **Card 4's E and R on the 944-song chord set as their own test.** That set is where all seven chord measures failed, and the 407 fresh songs have little power. E, R and distinct chords enter idea 1 and idea 3 as controls instead.
- **Card 4's melody-network version.** Not recommended by the card itself.
- **Week 01 idea 2 (plain vocabulary, varied path, on McGill).** Folded into idea 1's fresh leg; the interaction and voice-leading terms would add more chances of a lucky pass to a leg that already has 20 to 35% power.
- **Week 01 idea 3 (measure the ceiling with MusicLab).** Still standing and unchanged. No card this run bears on it, so it is carried over rather than re-ranked.
- **Network measures of artists (card 1's PageRank and betweenness).** Not from the notes; used only as the fame control in ideas 1 and 2.

## The one check: is g just repetition, chord count or form under another name?

**Question.** Before g is allowed into any outcome model, does it measure something different from within-section chord repetition, and does it simply follow the number of distinct chords or the number of sections (the Skeptic's form worry)? No outcome is used; chart peak and every other outcome were removed from the data before anything was computed.

**Data.** The 739 McGill Billboard chord charts committed at origin/main:studies/harmony/billboard_sections.json (Roman numerals on the tonic, bar by bar, every section as performed). Read only; scratch copy and script in the session scratchpad, not the repo.

**Frozen rules (set before running).**
- *Chord token.* The chart's Roman numeral with its quality (major, minor, diminished, augmented, sus, power chord), plus a "7" mark where the chart flags a seventh or extension. This copies the covers study's chord token (root on the tonic with quality, sevenths distinguished) as closely as McGill allows; McGill does not separate dominant from major sevenths. "No chord" marks (N, X, pauses) are dropped, not treated as chords, because Hooktheory has none.
- *Merging.* A chord that repeats the one before it is merged into it (bar lines ignored), as in the covers study's chord sequence.
- *Within-section repetition (copied from studies/surprise/surprise_hooktheory.py, the source of the covers study's `ch_rep`).* For a section's merged chord sequence, the share of its chord 3-grams already heard earlier in the same section. Hooktheory clips are one transcription per section type and must have at least 4 chords, so here: the first instance of each distinct section letter (A, B, A' counts as its own), sections with at least 4 merged chords only, averaged over sections weighted by bar count (the covers study weighted by melody notes, which McGill lacks).
- *The chord graph and g.* All sections in performed order, joined into one merged sequence (section boundaries ignored, as card 4 and the Geometer specify). Nodes are distinct tokens; an arrow counts each move to a different chord; rows are normalised. **A chord with no next chord:** the song is treated as a cycle, so the last chord moves to the first (merged if they are the same). This guarantees that every chord has a way out and that the graph is one connected piece. g = 1 − |λ2|, where λ2 is the eigenvalue with the second-largest size (complex eigenvalues allowed). Songs with fewer than 2 distinct chords or fewer than 4 merged chords are dropped.
- *Also computed.* Number of distinct chords; number of section instances; number of distinct section letters; length in merged chords; E (mean over chords of the entropy of where each chord goes next, divided by log2 of the number of other chords); R (weighted reciprocity: the share of move traffic that goes A to B and B to A, summing the smaller of each pair).
- *Statistics.* Spearman correlations; a partial Spearman of g with repetition holding distinct chords and length (on ranks); the share of songs with g below 0.01. Sensitivity, stated in advance: repetition computed over every section instance rather than the first of each letter.

**Prediction (written before running).**
1. g is not repetition renamed: Spearman of g with repetition is negative and between −0.2 and −0.6; with E, positive and below +0.8. The Geometer's stop rule (either above 0.8 in size) is not triggered.
2. The form worry is not the main story: |rho| of g with the number of distinct section letters is under 0.3, and with section instances under 0.3.
3. Chord count: |rho| of g with distinct chords is under 0.5.
4. A floor: at least 10% of songs have g below 0.01 (pure cycles, vamps, and graphs that alternate in two groups), which would make g lumpy at zero.

**Result (721 of 739 songs kept; 18 had too few chords).** Three of the four predictions held; the fourth failed narrowly.

| Reading | Predicted | Found | Verdict |
|---|---|---|---|
| g against within-section repetition | −0.2 to −0.6 | −0.26 (p < 10⁻¹²); −0.25 with distinct chords and length held; halves by artist −0.19 and −0.33 | held |
| g against repetition over every section instance (sensitivity) | (same) | −0.35 | held |
| g against E (branching) | positive, under +0.8 | +0.47; +0.54 with distinct chords and length held | held |
| g against distinct section letters / section instances | size under 0.3 | +0.07 / −0.08 | held |
| g against distinct chords | size under 0.5 | +0.02 (halves −0.04, +0.09) | held |
| Share of songs with g below 0.01 | at least 10% | 8.7% (15% below 0.05) | failed, narrowly |

Other readings: g against R (back-and-forth) +0.05; against length in chords −0.10. The median g is 0.19 (middle half 0.09 to 0.30). Ranked together, repetition, E, R, distinct chords, length and both section counts explain 33% of the variation in g's ranks. The songs near zero are mostly the small ones: 31% of songs with 2 to 4 distinct chords have g below 0.01, against 1% of songs with 12 or more. The script deleted chart peak and date from each song as soon as it loaded the file. No outcome was looked at.

**Honest reading.** On McGill charts, g is not chords-that-move renamed. It shares only about 7% of its rank variation with within-section repetition, and it does not follow the number of chords or the number of sections. So the Skeptic's form worry, put the way he put it (hold the section count), is not what g measures. g is closest to E, card 4's branching measure (+0.47), which is what it should be, but it is not E either. So it passes the Geometer's own stop rule and is allowed into idea 1's model as a secondary term. Four limits:
- Being different is not the same as meaning something. Two thirds of g's variation is unexplained by everything measured here. That could be real harmonic structure or plain noise: on a graph of 6 to 10 chords, one unusual move can shift λ2 a lot. A cheap next check, still with no outcome, is whether g on a song's first half agrees with g on its second half. I did not run it, because the brief allowed one check.
- The failed fourth prediction cuts both ways. Fewer songs sit exactly at zero than I expected, so g is less lumpy overall. But in three- and four-chord songs it is often zero for structural reasons (pure cycles, and moves that alternate between two groups of chords). So distinct chords must stay in the model even though the overall correlation is near zero.
- The check holds the *number* of sections. It does not directly test the Skeptic's mechanism (verse and chorus loops joined by one move). That would need a graph built per section, compared with the whole-song graph.
- This was McGill, with whole songs as performed. Idea 1's main corpus is Hooktheory, whose clips are one transcription per section type, so g there would be built from fewer, shorter sequences and may behave differently. The rules above must be reused unchanged, with that difference stated beforehand.

Script and output (scratch only, not in the repo): `/tmp/claude-0/-home-claude-zeneng-pipeline/a6ee0ee0-c7ac-5962-9610-7b3a105bbd73/scratchpad/chair/gap_check.py` and `gap_check_out.txt` beside it.
