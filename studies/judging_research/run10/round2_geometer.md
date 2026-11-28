# Run 10, round 2: the Geometer answers the Skeptic

No outcome was opened. The power figures below come from fake outcomes (`common10.power`, 100 draws, α = .05/9) on all 14,511 split-A rows, with the frozen control in the model. Script: `/home/claude/scripts/geometer/power_r2.py`.

- **G10-1 pe_h0: kept.** I accept dropping the 1/p kill: the two versions correlate 0.87, so they are one test, and pe_h0_inv stays as a reading only. Simplicity points the other way here (pc_entropy +0.25 against a predicted +), but I freeze pc_entropy anyway so the result is clean if REP passes. Power with it frozen: 0.72.
- **G10-2 irr_skel: kept.** n_pc is frozen as you ask. Power 0.77.
- **G10-3 S_gap: kept, and counted as the only S.** n_pc is frozen. Power 0.64. pc_entropy goes in as an uncounted reading.
- **First-poster fixed effect:** accepted as an uncounted reading. All three measures use only on-beat notes, which are the ones transcribers agree on most (card 2).
- **No measure was revised.** `measure(t)` is unchanged, and all four keys are finite for all 14,511 tunes.

## Final (to freeze)

| Key | Predicted sign and size on y_cov (SD per SD) | Frozen extra control | Fake power |
|---|---|---|---|
| pe_h0 | **+0.03** (y_love +) | pc_entropy | 0.72 |
| irr_skel | **−0.03** (y_love −) | n_pc | 0.77 |
| S_gap | **−0.03** (y_love −) | n_pc | 0.64 |

pe_h0_inv is a reading only and is not counted.
