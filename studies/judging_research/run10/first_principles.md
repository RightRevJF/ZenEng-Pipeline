# Run 10: first principles

27 November 2026. Recommendations only; nothing is dropped without Jason.

## 1. Bedrock
**Facts.**
- TheSession.org, 23,089 tunes, melody only, never joined (A 14,511; C 4,261; H 4,317 sealed). K = 9 frozen, eight run.
- **REP** (pitch-class entropy): −0.083 on A, −0.062 on C (−0.082 with all baselines). The one counted finding; love agrees.
- Passed A, unconfirmed: irr_skel (C −0.011, about zero with entropy held); core_ic (C −0.051 at power 0.14, an estimate).
- Killed: S_gap, pe_h0, slg. Unsettled: cut_ab, ARCH_PE.
- **Seen lead, GAP** (full-melody spectral gap): −0.065 on A, −0.067 on C (rule written after A); −0.052 with all baselines; −0.066 with entropy held, so not REP. cheeger, the same graph's bottleneck: −0.065 on A.

**Assumptions.** The first setting stands for the tune; members' recordings are covers; a tunebook is love (maybe a bookmark; only 10+ listed); first-posting year is age (it is site age); notes come before popularity.

## 2. Question every requirement
- **Yardstick here.** No original artist: recordings are session players choosing a trad tune, tunebooks musicians choosing to learn it. Both are uptake by players, not lasting love.
- **Greatness or learnability?** Probably learnability (extrapolation): for REP, love (intent to learn) beats recordings. Worse, card 2 finds rare pitches mutate most and substitutions are small steps, so a much-played tune's posted setting is worn toward fewer pitch classes and fewer leaps, lowering entropy and GAP alike. The arrow may run from popularity to notes. Flag, unproven.
- **Notes only.** Cleaner than charts, but the transcriber now leaks; the first-poster effect (username is in tunes.csv) is missing. Flag: add it.
- **Measures.** The beat-skeleton premise failed: S_gap died while full GAP held; off-beat surf_ic matched core_ic.
- **Cap of eight.** It pushed LOCK onto seen A for nothing: K already counted nine. Flag: waive it then.
- **Power floor, splits, R09-5.** C gave power 0.14 to 0.28 for −0.03; R09-5's 0.5 for confirmations was not adopted, and 4,300 tunes cannot reach it for −0.03 at α .05/3. Flag: test fewer on H. Its stability gate worked.

## 3. Delete (recommended)
- **S_gap:** −0.005, Poisson wrong sign; pitch classes fold away the registers.
- **pe_h0:** +0.016; positive only with entropy held.
- **slg:** wrong sign; the raw link is repetition and length.
- **TSG:** wrong sign on A and C.
- **irr_skel:** zero on C with entropy held; spend no H.
- **ARCH_PE:** gone with baselines held.
- **h0_max:** nothing.
- **The skeleton premise**, for outcomes.

Kept as readings: cut_ab (strict AABB +0.062), cheeger.

## 4. Simplify
Two numbers: how few pitch classes a tune uses (REP), and how rarely, for its range, it crosses between its low and high rooms (GAP). GAP, cheeger and cut_ab are one idea (Cheeger's inequality ties gap to bottleneck; the cut is by register in 88% of tunes): stay in a room, cross rarely, cross at the part break. Plainest twin (speculation): the share of moves crossing the median pitch.

## 5. Speed the loop
Written first, for sealed H next pass: K = 3, α = .05/3, run-10 rules. Power from `harness10.py power` before any join (brackets: my scaling).

| Test | Measure; extras | Predicted | Power | Killed if outside the range |
|---|---|---|---|---|
| GAP | GAP; range, n_pitch, ln_notes | −0.05 | (~0.75) | −0.05 (estimate weaker than about −0.02) |
| core_ic | core_ic; pc_entropy | −0.035 | (~0.35) | −0.035 (estimate near zero or positive) |
| LOCK | LOCK; none | +0.03 | (~0.3) | +0.03 (estimate near zero or negative) |

Under R09-5's 0.5, only GAP counts. GAP readings: all baselines (−0.04), n_bars added, named-composer tunes only (−0.05), cheeger, cross-median share, first poster. LOCK still runs first on A as frozen. If GAP's all-baselines reading is near zero, it is range renamed; if named-composer GAP and REP vanish, wear wins.

## 6. The obstacle and the way through
**Obstacle.** Every surviving lead (few pitch classes, a typical melody, staying in one register) is what transmission keeps and wear produces, so the posted notes may be downstream of being played.

**Way through (speculation).** Use notes fixed before a tune spread: named-composer tunes, and time (refetch the dump; do today's notes predict tunebooks and recordings added after 27 November 2026, holding today's counts?). Surviving both, they judge uptake, not yet greatness.

## 7. For Jason: what GAP means
Dots are pitches, lines are moves, thicker when repeated. The gap is how fast a walker on that map forgets where it started: two clusters joined by a thin line, slow (small gap); everything joined, fast.

Worked example (my computation, no outcomes; 16 notes, equal range):
- `D E F# E D E F# E | G A B A G A B A` (low room, high room, one doorway each way): g = 0.21, S = 1.07.
- The rooms visited twice each: g = 0.29.
- `D G E A F# B E A D G F# B E A F# G` (leaping across every move): g = 0.51, S = 1.16.

Small-gap tunes, for their range, have more recording artists: A part low, B part high, few jumps between.
