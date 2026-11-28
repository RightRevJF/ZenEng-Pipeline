# Run 11: first principles

28 November 2026. Nothing is dropped without Jason.

## 1. Bedrock
**Facts.**
- K = 5, α .01; 9,588 seen songs; outcome: a version by another artist (22%).
- **REP passed:** −0.029 within artist (SE 0.011, p .0076); halves −0.010 (p .50) and −0.046; size held, −0.026 (p .073).
- **Killed:** GAP (+0.001), TIE (−0.010), TYP11 (+0.002), ANT (−0.004).
- **Estimates:** SLG −0.010, core_ic +0.002 (both would have died); LOCKP failed its gate.
- **After seeing, single-song artists:** −0.025 (p .12), unsettled; +0.040 with size held. The folk replication flips likewise.
- Run 10's corpus is withdrawn; its figures count for nothing.

**Assumptions.** A clip stands for the song; within-artist removes fame; a new measure on seen songs tests fairly.

## 2. Question every requirement
- **Yardstick.** Love is still unused. On main the chord finding sat mostly in songs the artist was already covering; REP lacks that split. Flag.
- **Notes only.** On main the recording's sound passed on a second store (+0.08 to +0.2); notes give about 0.03. Keep it; know the ceiling.
- **Hits only.** A strength: the transcribed recording predates its covers, so they cannot wear the notes.
- **Seen songs re-spent.** Dozens of measures since run 04; K counts one pass only. Flag: a project-wide count.
- **The 0.20 gate.** Clip 1 against clip 2 is usually verse against chorus, so it rewards "the same everywhere", not "real". GAP passed by 0.0004. Flag.
- **Power floor.** Fake outcomes had no artist share, so their SEs ran about a third above the real ones. At real SEs power was about 0.5 to 0.8, not 0.13 to 0.39 (my rough arithmetic). Kills are firmer than stated; but K would have been 7 (α .0071), and **REP's p .0076 would not pass**. Fix: give fake outcomes an artist share.
- **Kill wording.** "Killed" means "smaller than predicted".
- **REP** is mostly pitch-class count (ρ 0.88).

## 3. Delete (recommended)
- **GAP, and Jason's S = 1 + g/π.** Jason's own formula had two fair tests on allowed data: as a scaling exponent (main's shape study) and as the spectral gap here. Popular tunes do sit near the critical point, as he said; how near did not tell songs apart. Worth trying; as a judge, done.
- **ROOMS, SETTLE, Cheeger, CUT_AB, S_gap, pe_h0, IRR, ARCH:** noise or wrong sign.
- **TIE/HB:** every reading negative.
- **TYP11, ANT:** near zero.
- **SLG:** wrong sign throughout.
- **core_ic:** carries pc_entropy.
- **LOCKP, BIP:** unstable.
- **Geometry left:** a true theorem and a vocabulary. The stable part of every pitch-graph number is size. Recommend closing the line.

## 4. Simplify
How few pitch classes a melody spends its time on, among one artist's songs: about one point of uptake per standard step, on 22% (my conversion). Plainest twin: the count of pitch classes (−0.021, p .031).

## 5. Speed the loop
**Prediction, first.** On melodies never joined to an outcome, within artist: REP **−0.02** (shrunk for winner's curse). Killed if −0.02 lies outside the 95% range. Reading: size held, −0.02; if only bare survives, it is size.

**Data.** Lakh "lmd_matched" (CC BY 4.0), files with a melody or vocal track, fetched by the maintainer. Exclude the Hooktheory rows, main's shape sets and McGill. Count the yield first: power 0.5 at −0.02 needs about 11,000 within-artist songs (my scaling); fewer, wait or pool. POP909 is too small.

**On data at hand: none can run without re-spending.** No clip has an outcome, and the file has no section labels (I checked), so no within-song test exists. About 763 Hooktheory melodies lie outside both row sets (my count; history unchecked), but across artists, at power about 0.1, where REP flips with size. Free now: rerun power with an artist share.

## 6. The obstacle and the way through
**Obstacle.** One small lead, on seen songs, passing only at K = 5, inseparable from size across artists; every allowed named melody spent.

**Way through (speculation).** New named melodies, within artist, under mended power. Or skip covers: a sing-back test of learnability.

## 7. For Jason: pitch-class entropy
Fold notes to letter names; add the time on each. Entropy (bits) says how spread that time is: 0 is one note, 3.58 all twelve evenly. Two to the bits is the "effective number of notes."

- *Mary Had a Little Lamb*, 16 beats: E 6, D 6, G 3, C 1 → **1.76 bits**, about 3.4 notes.
- *Twinkle, Twinkle*, 16 beats: C 4, G 4, A, F, E, D 2 each → **2.50 bits**, about 5.7.

Why it might matter (speculation): each extra note is one more thing to learn by ear, so a narrow tune is sung back sooner and travels further. Twinkle is loved too: a lean, not a rule.

## Addendum (after Jason's word, 28 November 2026): the formula's last attempt
Jason asked that his formula be dropped only after one more, novel attempt. Every earlier test read S as an exponent or swapped g for a spectral gap; this one measured **g as a coupling**: how the melody line and the bass line move together over whole Lakh songs (detrended cross-correlation at one, two and four bars), S = 1 + g/π. Rule first (344be9b): contrary motion (g below 0) goes with covers, −0.03. Result +0.017 (SE 0.017): **killed**, halves and logit the wrong way. On the notes alone the formula's identity did not hold either: π(S − 1) of the melody is unrelated to the measured coupling (Spearman 0.006). By Jason's rule, S = 1 + g/π is now eliminated from consideration as a judge of songs. What it leaves: popular melodies do sit near S = 1, as he said; nearness does not grade them.
