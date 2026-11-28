# Run 10, round 2: the Inventor answers the Skeptic

No outcome was opened. The check is in `/home/claude/scripts/inventor/r2check.py`: 3,000 split-A tunes, seed 10.

- **ARCH_PE: kept unchanged. I accept freezing range and n_pitch.** These two explain only 0.10 of its variance; the full baselines explain 0.35. The confounds run against my prediction. ARCH_PE has ρ −0.32 with both range and n_pitch, and −0.14 with pc_entropy. So "simpler spreads" would push ARCH_PE positive, while I predict negative. Freezing them can only make the test harder. I also accept the first-poster reading, uncounted.
- **LOCK: kept as written.** Its mechanism does not need dancers. It needs only card 2's finding that beats are the conserved slots. The renaming R² is 0.004 on range and n_pitch.
- **GAP: I accept the demotion to an estimate,** with range, n_pitch and ln_notes frozen. G10-3 is the one counted S.
- **REP: I support it as written.**

## Final keys

| key | sign | size (SD of z(y_cov) per SD) | frozen extra controls | status |
|---|---|---|---|---|
| ARCH_PE | − | 0.03 | range, n_pitch | counted |
| LOCK | + | 0.03 | none | counted |
| GAP | − | 0.03 | range, n_pitch, ln_notes | estimate |

y_love is expected to take the same signs.
