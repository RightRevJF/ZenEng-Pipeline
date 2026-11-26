# Run 06: first principles

26 November 2026. Recommendations; nothing is dropped without Jason.

## 1. Bedrock
**Facts.**
- Six frozen tests, none passed. Killed: melody range (+0.69 against −0.7) and diatonicity (−0.29 against +0.5). Unsettled: chirality CH (−0.30), chord repetition on fresh songs (+1.32, p .20, both halves and the logit positive), the arrow A on fresh songs (+0.09) and tonic resistance (−0.25).
- One walk's Hodge gradient is the unit current from first chord to last; card 2's directional part is likewise one start-to-end path. A clip's flow is its boundary plus loops, and the loops mostly count distinct chords.
- The fresh outcomes are close to independent: only 10 of 312 matched fresh songs share a Discogs group with a seen song. Fresh uptake is 17% (seen 24%). On fresh songs y_foreign is nearly y (222 of 238).
- Chord repetition is positive on every reading of "taken up at all": +1.19 (in Discogs-VI, seen), +1.00 (y_foreign, seen), +1.32 (fresh). It is negative on "how many" (−0.042 within artist). A has faded: +0.84 seen, +0.09 fresh, −1.75 across single-song artists.
- |CH| is as large as signed CH (−0.31): any lean may be how much a song turns, not which way.
- My notes-only check: a fresh song's ch_rep correlates 0.20 with its artist's seen mean, which explains under 2% of the tested column. So the fresh slope is truly within artist.

**Assumptions.** y_foreign records musicians choosing; a clip stands for the song; artist and fresh effects absorb why the pack left songs out.

## 2. Question every requirement
- **Yardstick.** No test since run 02 has used love. Flag it in every RESULT.
- **Notes only.** Keep; CH ignores chord quality.
- **Hits only.** Fresh songs are mostly chords-only clips of lesser songs.
- **The .05/N rule at power 0.02.** Five blind tests cut chirality's bar from .05 to .00833 (power 0.35 to 0.15). Their kills fire half the time on noise and a quarter to a third when true (odds moved about 1.5); both killed predictions lie inside their own 95% ranges. Flag for Jason: count only tests with fake-outcome power of 0.2 or more (run 04's proposal) and report the rest as estimates.
- **Engine (origin/main).** loop_less (960, 749.159) is a setting, off; 749.178 failed; the loop gate with a chance (749.185) waits with song 63 sealed. 749.178 lets 960 become the default only "after the fresh-songs question settles which way covers lean". Tonight did not settle it, at this size cannot, and the margins disagree. Flag: judge 749.185 on matching the kept rate alone, citing covers for neither side.

## 3. Delete (recommended)
- **Melody range:** killed on fresh songs; never past .05 on seen songs; opposite signs on the two margins. Keep as a control.
- **Diatonicity:** killed; with run 05's fifths path, the pair is closed.
- **Tonic resistance:** unsettled a third time, never close; fresh stability 0.182. Retire.
- **Stopped on the notes tonight:** Hodge gradient share and downhill H (clip boundaries); λ, P, D, β₁ (distinct chords); holes (residual stability 0.18); A\* and σ (A renamed); heat engine (0.06); melodic holonomy (0.152); one-song circularity (start and end); March's symmetric fields (dimension claims fail).
- **Carried:** run 05's deletions.

## 4. Simplify
Chord repetition: one measure, one outcome, within artist, both margins. Loops are taken up more often; songs that move are taken up by more people. CH stays a reported column, unsigned beside signed.

## 5. Speed the loop
**No seventh test tonight.** No within-artist outcome is unspent; the fresh songs are now seen. Pooling the two ch_rep estimates is description, not a test (+1.06, SE 0.44, p .017). A new measure on fresh songs has power near 0.02. Re-fitting the fresh model is a forking path that the check says would change little.

**Prediction for the next independent batch, written now:** ch_rep within artist on y_foreign, **+1.0 pp per SD**, one counted test at .05, kill if β ≤ 0, run only with fake-outcome power of 0.5 or more. From tonight's SE (1.04 on 1,295 songs), that needs about 5,400 fresh within-artist songs; 0.8 power needs about 11,000.

## 6. The obstacle and the way through
**Obstacle.** Effects are about 1 pp per SD on a 22% outcome, and all of Hooktheory's within-artist songs give an SE of 0.4 to 0.5. The measures have outrun the outcomes.

**Way through (speculation).** Pause new measures. Look for a large chords-only corpus with artist and title (Chordonomicon; size, licence and fields unverified), matched to Discogs-VI by the maintainer's rule; ch_rep needs chords only. Pin the file in DATA.md. If the mathematics continues, the one honest family left is the loop part paired with a fixed form on a fixed space, as CH does on the circle of fifths, tested only once outcomes exist to spend.
