# Run 10, round 2: the Skeptic

No outcome opened. Check: `/home/claude/scripts/skeptic/xcheck.py` (1,500 split-A tunes).

**General.** Year, type, meter and mode are fixed effects. The live confounds are simplicity (McBride & Leroi), length and form, and the first poster's notation of weak beats. Where a measure leans on n_pc or pc_entropy in simplicity's direction, freeze that baseline. tunes.csv has `username`: run a first-poster fixed effect as an uncounted reading for surface measures. y_love (10+ tunebooks only) has power below 0.6.

**Duplicates.** Inventor GAP and Listener g: rho 0.97, both mostly range (R² 0.65). Geometer S_gap (skeleton pitch classes) is distinct (|rho| < 0.3, R² 0.15). **Count G10-3 as the one S**, n_pc frozen (rho −0.22). R10-I3 and L3's g become estimates with range, n_pitch and ln_notes frozen.

**Each proposal.**
- **G10-1 pe_h0 (+).** Clean (R² 0.14); simplicity pushes the other way (pc_entropy +0.25). Drop the "1/p opposite sign" kill: rho 0.87 makes it one test.
- **G10-2 irr_skel (−).** Clean (R² 0.07), but n_pc +0.13 aligns with "simpler spreads": freeze n_pc.
- **L1 SLG (+).** Partly repetition and length (bar_rep +0.34, ln_notes +0.32). Count only with both frozen.
- **L2 TSG (−).** Mostly minus surf_ic (rho −0.76), and off-beat surprisal is where transcribers differ (card 2). **Count core_ic (−) instead**, pc_entropy frozen (n_pc +0.27, simplicity's direction): card 2's typicality test. TSG becomes an estimate.
- **L3 CUT_AB (+).** Reads form: rho −0.21 with written bars, −0.16 with ln_notes; "second half" differs between two- and three-part tunes. Freeze n_bars and ln_notes; report strict-AABB reels and jigs separately.
- **R10-I1 ARCH_PE (−).** Renamed by range, n_pitch and step_share (R² 0.35); rho 0.42 with GAP; written-out ornaments add short bars. Freeze range and n_pitch; add the poster reading.
- **R10-I2 LOCK (+).** Cleanest (R² 0.01). Weakest mechanism: rarely danced to. Count as written.

**Proposed K = 9:** pe_h0, irr_skel, S_gap, SLG, core_ic, CUT_AB, ARCH_PE, LOCK, REP. Each must clear the 0.2 power floor with its frozen controls in.

**REP (replication baseline, counted, written first).** z(pc_entropy), McBride & Leroi's own measure, on y_love and y_cov. Predicted **−0.03** (simpler spreads); density (notes per bar) negative as companion. Stability 0.83 (n_pc 0.70).
- REP unsettled at power 0.2 or more: the known effect is invisible on this design, and every null above means little.
- REP passes: any measure correlated with pc_entropy must beat it with pc_entropy frozen.
