# Run 07: the brainstorm

26 November 2026, the 18:17 ET pass. Three imaginers (the Geometer, the Listener, the Inventor) proposed; the Skeptic critiqued; each answered. Every proposal is in `ideas.json` as R07-G1… R07-I3.

**The data this pass changed everything they could use.** Whole songs, for the first time at scale: the Lakh Pianoroll Dataset's cleansed songs (MIDI, 4/4, five tracks), named by the Million Song Dataset metadata. The imaginers saw only the notes side: bar chroma (12-vectors per bar) and half-bar triad chords. No outcome was opened by anyone in this file.

**A correction made after round 1 (the orchestrator, on the notes alone).** The Inventor noticed that many MSD tracks share one MIDI file. A count showed it is worse than duplicates: one file is the chosen match for up to 12 unrelated songs (the Lakh match is audio-based). `common.lakh_songs()` now keeps a track only if its file belongs to one song (artist and clean title) and counts a file once within a song. That leaves **5,373 within-artist songs by 1,573 artists** (from 11,177). The imaginers' checks were run on the larger sample before the fix; the chair re-ran the gates on the clean set.

---

## Round 1: proposals

### The Geometer

**G1. The statue is a tree (card 1, the Gromov four-point condition).** If a song's bars form nested families (section, then variant, then bar), its bar space is nearly a tree metric, the grouping shape a musician can rebuild. *Measure Ht:* non-empty bar chroma, L2-normalised; bars identical to 3 decimals merged (at least 4 types); Euclidean d; per quadruple fp = ½(max − median) of the three pair sums; Ht = mean fp over 20,000 random quadruples of distinct types (all if fewer), divided by the mean pairwise d. Low = tree-like. *Mathematics:* fp ≡ 0 exactly for tree metrics (Buneman); a re-voicing that moves every distance by ≤ ε moves each fp by ≤ 2ε, so the 2|2 splits survive any change smaller than their gaps. A song that lasts is one whose skeleton survives re-voicing (bold extrapolation). *Prediction:* −0.6 pp of y_foreign per SD (−0.4 with ch_rep held). *Kill:* β ≥ 0. *Checks:* split-half 0.70, residual 0.59; two different MIDI files 0.34; largest overlap ch_rep −0.39; CV of distances −0.63 (report beside it).

**G2. … walked in a ring (card 2, sliding-window persistence).** A song that comes back through its sections in a fixed order traces a closed curve of 8-bar windows. *Measure R:* 8-bar windows, step 1, each pitch class centred over the window, L2-normalised, de-duplicated; score = longest H1 bar (Rips, F₁₁) / √3; R = score − mean over 20 shuffles of whole 4-bar blocks. *Mathematics:* bottleneck stability makes persistence a certified radius; Theorem 6.8 ties the score to one harmonic at the window period. *Prediction:* +0.5. *Kill:* β ≤ 0. *Kinship:* R05-M was killed on clips; R subtracts the loop part and needs a whole song. *Checks:* split-half 0.28, residual 0.27; overlaps ≤ 0.11; median R −0.004 (songs are on average no more ring-like than their own shuffled blocks).

**G3. Jason's S = 1 + g/π on whole songs.** g = 1 − |λ₂| of the row-normalised chord-move matrix (half-bar triads, runs collapsed, last joined to first); S ranks as g. By Cheeger (proved for reversible chains only, so a guide), small g means a bottleneck: two harmonic rooms or a strict cycle. *Prediction:* −0.5 (−0.3 with ch_rep). *Kill:* β ≥ 0. *Checks:* split-half 0.53 (clips gave 0.17), residual 0.44, two files 0.29, largest overlap ch_rep −0.35; 1.6% of songs have g = 0.

### The Listener

**L1. Tree-shaped memory of the phrases (card 1).** A player stores a song as a tree of phrases; a cover keeps the branches and redoes the leaves. *Measure H4m:* L2 bar chroma of sounding bars; every run of 4 consecutive bars as one 48-vector ÷ √4; exact duplicates dropped; Euclidean; 4,000 quadruples; H4m = 2 × mean fp ÷ mean pairwise d; CV of distances as a control. *Prediction:* −0.6. *Kill:* β ≥ 0. *Checks:* split-half 0.615, residual 0.56; largest overlap ln_chg −0.28; 95% of songs more tree-like than their own shuffled bars; correlates 0.84 with a 4-bar-block shuffle, so it reads the tree of phrases, not section order.

**L2. The phrase a guitarist must learn: loop period P\* (card 2's window-equals-period rule).** You learn a song by learning one cycle; a 2-bar vamp gives little to carry over, a whole 4- to 16-bar sentence that returns is worth covering. *Measure:* L1 bar chroma of sounding bars; D(ℓ) = mean ‖x_{t+ℓ} − x_t‖²; P\* = argmin over ℓ = 2…16 (ties to the smaller); ln P\*; needs ≥ 34 bars. *Prediction:* +0.6. *Kill:* β ≤ 0. *Checks:* split-half 0.454, residual 0.417; largest overlap ln_chg −0.275; powers of two are 86% of P\*.

**L3. Front-loaded exposure.** A musician learns from the part heard most, the opening; new material late is a cost. *Measure Nfr:* bar triad labels; share of 4-bar label sequences ending after the first third that never occurred within the first third. *Prediction:* −0.5 with ch_rep held. *Kill:* β ≥ 0. *Checks:* split-half 0.485, residual 0.24 (narrow); overlap ch_rep −0.63 (the weakest gates).

*Stopped by the Listener on the notes:* first-minute novelty (residual 0.19), time to first return (0.15), bar of the first chorus (0.088), card 2's κ loop span (a shuffle gives exactly 4: lag-1 autocorrelation renamed), return depth (R05-M renamed).

### The Inventor

**I1. Phylogenetic form (card 1, Buneman).** A tree on m phrases needs 2m − 3 lengths, a general metric m(m−1)/2: a tree-like form is a compressible genome another musician can rebuild. *Measure Hm:* non-overlapping 4-bar phrases (48-vectors, L2), Euclidean, mean fp over all 4-subsets (6,000 sampled), ÷ mean pairwise d; cv beside it. *Prediction (extrapolation):* −0.7. *Kill:* β ≥ 0. *Checks:* split-half 0.307, residual 0.256; overlap ch_rep −0.23, cv −0.64; the theorem-normalised form H is cv renamed (−0.93), so Hm is primary.

**I2. Campfire fidelity F (channel coding).** Songs pass through musicians who reduce them to plain triads; what lives in voicing colour is lost. *Measure:* mean over sounding bars of the best triad template's share of the bar's L1 chroma. *Prediction:* +0.5. *Kill:* β ≤ 0 (risk: rich-chorded jazz standards are covered a lot). *Checks:* split-half 0.897, residual 0.81; largest overlap ln_chg −0.35; fame proxies |ρ| ≤ 0.08.

**I3. Kac burstiness B (Poincaré recurrence).** Kac fixes each chord's mean return time; all free information is in the spread. Clockwork returns mean a loop; clustered returns mean sectional harmony. *Measure:* gaps of each chord with ≥ 3 occurrences, ÷ its mean gap, pooled (n ≥ 6); B = (σ − 1)/(σ + 1). *Prediction:* +0.5 holding ch_rep and V. *Kill:* β ≤ 0. *Checks:* split-half 0.626, residual 0.386; overlap V +0.59, ln_chg +0.47; only 7.8% of songs burstier than chance.

---
## Round 2: the Skeptic

All correlations Spearman, within artist (artist-demeaned ranks), on the 5,373 clean songs. No outcome opened.

**Merge G1, L1 and I1 into one: L1's H4m.** The three hyperbolicities correlate only 0.32 to 0.44 with each other within artist. Ht (G1) mostly reads voicing, not form (−0.56 with its CV of distances, −0.41 with F, +0.33 with per-bar pitch-class entropy). Hm (I1) mostly reads its CV (−0.64; only 59% of its variance left once CV is held). **H4m** correlates −0.20 with its CV and −0.03 with ch_rep, largest overlap V −0.28, 96% of its variance left once CV is held; dropping quadruples whose windows overlap in time gives ρ 0.98 with H4m, so it is not reading the song as a path; split-half 0.52. The model must hold cv_w and ch_rep beside it (cv_w correlates +0.54 with ch_rep: the CV of distances is the repetition axis in chroma space). Frozen form: sliding 4-bar windows (48-vectors ÷ 2), exact duplicates dropped, 4,000 quadruples seeded by md5(tid), 2·mean fp ÷ mean pairwise d. Kill if β ≥ 0.

**G2 (ring R).** A cousin of R05-M (killed). Median −0.004 and split-half 0.28: mostly noise around its own shuffles. Report only.

**G3 (spectral gap g).** This is R02-gap: parked, never tested, not failed; the whole song fixes its clip-stability failure (0.53). Overlaps ch_rep −0.27, cv_w −0.36. Hold ch_rep and V. It can run.

**L2 (P\*).** Overlaps clean (≤ 0.25), but 86% are powers of two: really four categories; report a categorical version too. P\* in bars depends on whether the arranger wrote it in half or double time: hold ln tempo (LPD midi_info; ρ +0.09).

**L3 (Nfr).** Chord repetition renamed and inverted (ch_rep −0.54, cv −0.50). Withdraw it or report it as a reading of ch_rep.

**I2 (F).** Close to the inverse of per-bar pitch-class entropy (−0.82), +0.21 with tempo: the measure most likely to read MIDI arranger style (pads, doublings). Two-file agreement 0.84 cannot clear that (duplicate Lakh files are often edits of one transcription). Report only, unless a voicing-free version exists.

**I3 (B).** Mostly vocabulary and length (V +0.48, ln_chg +0.40, ln_bars +0.27). Hold all three; secondary at most.

**Fame, era, genre.** Every measure has |ρ| ≤ 0.07 within artist with hotttnesss, the Billboard flag, year, year-known and the number of files. Artist fixed effects absorb genre and dance loops (MSD artist terms are artist-level).

**Design issues for the battery.**
1. *The ambiguous-file filter selects on the outcome.* 583 files that carry one title under several artists (1,533 tracks) are dropped: Fast Car (Tracy Chapman / David Usher), Baker Street, When a Man Loves a Woman. These are covers that are themselves in MSD. Own files by title, not by song: give the file to each artist with that title.
2. *Some artists are covering other people's songs.* 61 karaoke, orchestra or panpipe artists account for 228 songs (Panpipes alone 43). For these, y_foreign comes from the original performer. Drop a frozen name list; run the maintainer's first-performer rule as a sensitivity.
3. *Year* is a precision control, not a first-year control: 41% unknown; album year, so reissues count. Use min over tracks. Never use Discogs first_year (it exists only for matched songs).
4. *Billboard and hotttnesss:* report with them held; do not hold in the primary (partly downstream of the outcome).
5. *The run 06 ch_rep prediction (+1.0) is the wrong size for MIDI chords.* MIDI ch_rep correlates only 0.32 with Hooktheory's, yet its split-half is 0.75 and two-file agreement 0.78: a different construct, not a noisy copy. Through the shared part alone, expect +0.3 to +0.5. Keep +1.0 as written, but state that β between 0 and 1 neither passes nor kills. Power at SE 0.5: 0.52 if +1.0, 0.12 if +0.4 (at .05).
6. *Power for the battery is low:* 0.17 to 0.27 at .05 for 0.5 to 0.7, and 0.06 to 0.12 at .05/9. Count ch_rep as primary and H4m as the one secondary; report the rest as estimates; require the same sign in both halves.

Checks (notes only): `skeptic_r07_checks.py`, `skeptic_r07_an.py`, `skeptic_r07_two.py` (two-file agreement 0.62 to 0.84 on 174 songs), `skeptic_r07_amb.py`, `skeptic_r07_h4far.py` (in /home/claude/scripts, outside the repo).

## Round 2: the answers

**The Geometer.** G1 merged into H4m; Ht withdrawn (it correlated −0.63 with its CV on my sample too). H4m is nearly my reported column Hw (split-half 0.59, CV −0.26), so the card 1 grounding moves over unchanged: a cover that moves each distance by ε moves each fp by at most 2ε, so a tree-like song's 2|2 splits survive re-arranging. Prediction −0.5 pp per SD with cv_w and ch_rep held; kill β ≥ 0. **G2 withdrawn** as a test (report only). **G3 runs as R02-gap**, holding ch_rep and V: −0.3 pp per SD; kill β ≥ 0. I back the Skeptic's issue 1 (give each file to every artist under that title). Caveat: my numbers came from the list before cleaning.

**The Listener.** L1 (H4m) accepted in the Skeptic's frozen form (÷2 is my ÷√4), with cv_w and ch_rep held; −0.6, kill β ≥ 0, same sign in both halves; the one secondary, with ch_rep primary. **L2 revised and reported only:** ln P\* with ln tempo held, +0.6, wrong if β ≤ 0; a categorical form (2, 8, 16 bars against 4; "other" pooled), predicted order 2 < 4 < 8 ≤ 16; and a variant in seconds, P\* × 4 × 60 / tempo, which half- or double-time writing cannot move. **L3 withdrawn** (ch_rep inverted).

**The Inventor.** I1 withdrawn, merged into H4m; the tree-genome reading carries over (extrapolation): −0.5 with cv_w and ch_rep held; kill β ≥ 0; real songs are more tree-like than their own shuffled bars in 98.5% of songs. **I2 report only:** F likely reads the arranger; a voicing-free version (which pitch classes are present, unweighted) is untested and not forked tonight. **I3 secondary at most, reported as an estimate,** holding V, ln_chg and ln_bars (residual split-half 0.386): +0.3; kill β ≤ 0. I support the Skeptic's design fixes.

## Where they agreed and split
- **Agreed:** one tree-likeness measure (H4m, the Listener's form) is the pass's mathematics; it must sit beside the CV of distances and chord repetition. Files belong to a title, not to one artist. Fame columns are reported, not held.
- **Split:** how many tests to count. The Skeptic wants two counted (ch_rep and H4m) and the rest as estimates; Jason's standing rule says every testable idea is tested and counted. The chair rules.
