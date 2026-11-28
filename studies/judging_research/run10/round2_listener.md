# Run 10, round 2: the Listener answers the Skeptic

**L1 SLG: kept, and I accept both frozen controls.** With bar_rep and ln_notes held, a pass means the tune's own grammar matters beyond plain repetition.

**L2: revised.** I accept the Skeptic's point: TSG mostly reads surf_ic (rho −0.76), and off-beat notes are where transcribers differ. **core_ic (−) is counted** with pc_entropy frozen. TSG becomes an estimate. A pass on core_ic says "typical skeleton spreads", which is card 2's typicality reading, not "balance".

**L3 CUT_AB: kept, and I accept n_bars and ln_notes frozen.** Note that n_bars is a `baseline()` key but is not in `BASE`. I add an `aabb` flag for a separate, uncounted report on strict AABB reels and jigs: 16 written bars that expand to 32. That subset is about 12% of tunes, so it has low power. The three-part mismatch is real but it dilutes the effect rather than reversing it. Whatever the halves are, a high CUT_AB still means "register marks the part".

**g / S: estimate only.** I agree with counting G10-3 as the one S.

**REP: agreed.** Since core_ic leans on pc_entropy, it must beat REP with pc_entropy frozen.

## Final keys (`measure(t)` in /home/claude/scripts/listener/measures_listener.py; `FINAL` dict)
| key | status | sign | size (SD of z(y) per SD) | frozen extra controls |
|---|---|---|---|---|
| slg | counted | + | +0.03 (y_cov; y_love +) | bar_rep, ln_notes |
| core_ic | counted | − | −0.03 (y_cov; y_love −) | pc_entropy |
| cut_ab | counted | + | +0.03 (y_cov; y_love +) | n_bars, ln_notes |
| tsg | estimate | − | — | pc_entropy |
| gap (S) | estimate | − | — | range, n_pitch, ln_notes |
| aabb | subset flag for cut_ab report | | | |
