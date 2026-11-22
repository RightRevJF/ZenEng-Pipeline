# Run 02 debate (22 November 2026)

Three agents with fixed stances, given the four cards, week 01's chair.md and report.md, and week 01's first_principles.md.

# Round 1

## Round 1: The Geometer

**What I give up.** Shape templates, S near 1, the seven tune shapes and the learned regions map all failed on unseen songs. Card 2 adds a warning: even where musicians choose every tune, the melody adds only about 3%. No more shapes of the tune.

**A new shape: the chord graph.** Card 4 turns a piece into a network. Build it from chords alone. Points are chords named relative to the key. Arrows count moves to a *different* chord, with repeats dropped. The matrix of those moves acts on a Hilbert space; its eigenvalues show how the song travels.

**Measure: spectral gap, g = 1 − |λ₂|**, where λ₂ is the second-largest eigenvalue by size. Nothing is fitted.
- A I–V–vi–IV loop scores 0 however often it repeats. A pure cycle never forgets where it started.
- A two-chord rocking vamp also scores 0.
- One number catches both of Card 4's plain-network marks: little branching, much back-and-forth.
- Chords that can leave a place by more than one road usually score above 0.

On a graph, positive Ollivier–Ricci curvature sets a floor under the spectral gap, so g is Jason's non-Euclidean idea taken literally. It is only an analogy to S = 1 + g/π. S stays retired as a judge.

**Why it might separate great from good.** In Card 1, covers mostly stay inside the original's genre (73% for jazz). A cross-genre cover goes against that pull and usually re-harmonises; several roads through the chords give the arranger room. Card 3's exposure effect should matter least for musicians, who have heard nearly everything. In Card 4's preprint, popularity leans toward simpler networks, so g may split audiences from musicians.

**Test (prediction written now).** Use the 944 Hooktheory songs up to 2005; keep the 407 from 2006–2012 unseen. Hold year, distinct chords, length, within-section repetition, and Card 4's E and R. Prediction: in both artist halves, g predicts cross-genre cover breadth at +0.05 or more, and better than it predicts raw cover count.

**I am wrong if:**
- g correlates above 0.8 with repetition (the old finding renamed);
- the pooled effect is under +0.03, or the halves differ in sign;
- the sign flips on the unseen songs;
- breadth is predicted no better than raw count.

**Limits.** Untested; needs Discogs genre tags (Card 1's check). With 944 songs, a pass is only a lead.

## Round 1: The Listener

**What card 3 does to my side.** Card 3 played 40 unknown excerpts to 15 people, 28 times each. Liking rose at every complexity level and never turned down; familiarity was the biggest driver. I accept the consequence: much of the love half of G records how often people heard a song, which the notes cannot see. Limits: 15 listeners, four weeks, no control group, complexity rated from recordings, not notes. Two results still matter. Which piece it was mattered strongly within each level. And simpler pieces were rated far more "dull" even as liking rose. Dullness is the first sign of wearing out, and card 3 stopped before wear-out could show.

**So preference has two jobs.** Memory: a song must be easy to carry, or no one learns it. Surprise: it must keep giving after the hundredth hearing. Musicians have heard almost everything, so in their choices exposure matters less and the song more.

Card 2 supports memory: on TheSession, tunes with lower pitch-class entropy and note density spread faster among players beyond prestige. But melody adds only about 3 points of R², and the effect curves (in the supplement) were not seen. The covers study supports surprise: songs whose chords repeat less within a section draw more covers in two sources, not more views.

**Proposal: plain tune, moving harmony.**
1. **Covers.** Discogs-VI's 2,360 songs, covers within five years of release. Hold views, year, and the original performer's covers of other songs (card 1's fame loop). Prediction: melodic pitch-class entropy and chord repetition both negative, beta −0.03 or stronger; songs low on both pick out the top tenth by early covers with AUC 0.6 or better. **Wrong if** entropy is positive pooled, artist halves disagree in sign, or AUC is under 0.6.
2. **Love against exposure** (card 3's own test). Hold Hot 100 weeks and peak. Prediction: looping songs lose more love as exposure rises; the weeks-by-repetition interaction on love is −0.05 or stronger in both halves. **Wrong if** it is under 0.03 in size or the halves split. Then card 3 wins: love mostly records exposure, and a notes judge should aim at covers alone, as last week's first-principles review proposed.

**Honest ceiling.** Notes explained 1.5 to 4% of covers, and same-artist tests found nothing, so a pass would be small. Card 4 adds little: in pop and rock every popularity r was under 0.07.

## Round 1: The Skeptic

My question for every idea: would it pick out lasting love and covers on songs it has never seen, or would it only pick up fame, exposure and era?

**Card 1 is a warning about the outcome itself.** The top 100 artists (0.1%) take 41% of all covers, and covering mostly stays inside a genre. So a raw cover count partly measures how famous the original performer is. The card's test is sound because it holds that fame fixed (the performer's covers on other songs). But note what it really is: the predictor is chord repetition, the replicated "chords that move" finding, with a new outcome (cross-genre breadth). Breadth will also track the raw count and the performer's reach, and we do not yet know whether Discogs-VI even carries genre tags.

**Card 2 is honest about size.** In the cleanest setting there is, musicians choosing tunes to learn, melody adds about 3 points of explained variance. Prestige from recordings adds 16. There is no control for a tune's age, recordings are both cause and effect, and β measures how fast a tune spreads, not lasting love. The proposed test runs five melody measures on hits. Five shape runs on about 3,100 songs already found nothing in the tune, and note density was already tested (−0.036, p = .08). That is five more chances to find something by luck. Low prior.

**Card 3 is the skeptic's paper, but it is small.** Fifteen listeners and no control group, yet the exposure effect is large (ω² about 0.20) and complexity has none. For the *love* half, I expect exposure and the recording's sound (which has now passed on two stores) to swamp the notes. The card's test has a flaw: weeks on the chart are partly *caused* by liking, so they are not exposure handed out at random. Its third leg is still worth running: does chord repetition still predict covers with chart weeks and peak held?

**Card 4 has no outcome that counts.** Spotify popularity, in Pop and Rock, |r| under 0.07, from fan-made MIDI. Its chord-entropy test is well built to separate itself from repetition. But it is fitted on the 944-song set where all seven chord measures failed, and 407 fresh songs give little power to detect an effect of 0.05.

**Size, honestly:** the best note finding is β −0.071, and the notes add 1.5% on Discogs-VI. Same-artist tests found nothing. Every corpus is hits only.

**My best bet:** last run's idea 1, early covers, with card 1's fame control and card 3's chart controls added to the same model. It tests the only finding that has already held twice, on the half of the yardstick that survives losing the recording, against the strongest confounds named. To count as replicated, it must keep the same sign in both artist halves, survive the fame control, and then hold on fresh McGill songs.

# Round 2

## Round 2: The Geometer

**Concessions to the Skeptic.** My test sat on the 944-song set, where seven chord measures failed; 407 unseen songs give little power; and I omitted Card 1's fame control. All fair. I am moving the test.

**Revised test.** g becomes one added term in the Skeptic's early-covers model, on the 2,360 Discogs-VI songs the covers study already scored.
- **Outcomes:** covers within five years of release, and cross-genre breadth if Discogs-VI has genre tags.
- **Held:** the performer's covers of other songs, Hot 100 weeks and peak, views, year, distinct chords, length, within-section repetition, and Card 4's E and R.
- **Then:** fresh McGill songs, with g frozen.

**Renaming check.** Before joining any outcome, report how strongly g correlates with repetition and with E. Stop if either correlation is above 0.8. g also counts as renamed if adding it leaves the covers R² unchanged at two decimals.

**Power.** For an effect of 0.05 on 2,360 songs, the chance of detecting it is about two in three pooled, and under half within each artist half. So a pass means pooled +0.05 at p < .05, with both halves the same sign.

**Defence.** g describes the harmony, not the tune, and the harmony is the only place a note signal has held. It also sees something a repetition count cannot: whether the loop has any way out.

**To the Listener.** g is the harmony half of "plain tune, moving harmony". After five failed tune runs, I doubt the plain-tune half.

## Round 2: The Listener

**To the Skeptic: two concessions.** Chart weeks are partly caused by liking, so my love-by-exposure interaction cannot tell wear-out from songs that charted long because they were loved. Card 3 assigned exposure at random; no table we hold does. I demote that leg to an exploratory reading. And melodic entropy is another try at the tune, where five runs on about 3,100 songs found nothing; note density already gave −0.036 (p = .08). Its prior is low.

**What I keep.** One melody term, pitch-class entropy, stated in advance, and none of card 2's other four. It tests memory where it should show most: musicians choosing what to learn. If it fails among hits, I will say the memory side is not visible on the page there.

**To the Geometer.** A chord graph that "forgets where it started" keeps its next chord hard to call after many hearings. That is my surprise half in other words. But g on a 6-to-10-chord graph is coarse and moves with length and chord count. It would also be built on the 944-song set where all seven chord measures failed. It belongs beside repetition in one frozen model.

**Revised proposal.** One model: the Skeptic's early covers, with card 1's fame control and card 3's chart controls. Terms: chord repetition (the main test), pitch-class entropy and g. Each fails if pooled size is under 0.03 or the artist halves split, and a pass must hold on fresh McGill songs.

## Round 2: The Skeptic

**The Listener's first leg is my best bet, with one addition.** It counts early covers only, holds views and year, and holds the original performer's covers of other songs. Those are the right controls. My objection is to melodic entropy. The tune has failed five times on unseen songs, so entropy should be a secondary term with its own pass rule, and chord repetition should stay the main claim. The −0.03 threshold is generous, so state up front how many terms are tested.

**The Listener's second leg (love against exposure)** asks the better question. An interaction is less exposed to reverse causation than a plain effect is. But chart weeks still depend on liking, and the chart rules changed over the decades. Add era bands and the Spotify sound readings as controls, and run a power check first: an interaction of 0.05 on about 900 songs may not be detectable. If it is null, I accept the Listener's own conclusion: aim the notes judge at covers.

**The Geometer's spectral gap** is new in kind. That is its strength and its risk. Before it counts, three things are needed:
- **Freeze the rules:** say beforehand how a chord with no next chord is handled.
- **Rule out form:** a song with separate verse and chorus loops joined by one move scores a small gap. So g may be measuring how a song is split into sections, not how it branches. Hold the section count.
- **Add the fame controls:** hold the original performer's other covers, and use early covers.

Also, "correlates above 0.8" is too loose a test for "renamed". What matters is what g adds once repetition, E and R are held.

**My best bet is the same:** chord repetition against early covers, with fame and chart controls, then fresh McGill songs. The Geometer's g and the Listener's entropy can be tested alongside it, each held to its own pass rule.
