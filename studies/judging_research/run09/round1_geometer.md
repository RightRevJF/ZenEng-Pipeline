# Run 09, round 1: the Geometer

27 November 2026. Notes only. I opened no outcome and called no outcome loader. I read only `charts_run08.json` and `charts_run09.json`.

## The check that shaped the proposals

Card 1's signed areas are stable between two charts from the same source, at 0.73 to 0.81. Between chart writers they are not. When a Real Book or BiaB chart is compared with the iReal chart of the same title, they agree only 0.28 to 0.36. That holds for M1, M3, M5, my tension engine, its wrapped form and its ii-collapsed form (table B).

The signature shape vector does worse. I used the level-3 log-signature of (τ, u, h). It finds the same tune within one source (median rank 0.1%), but across sources its median rank is 32%. A plain four-number size and vocabulary vector does better, at 9%. So I withdraw shape heritability by signature.

**Why.** Lévy area is S^{12} − S^{21}, the difference of two large terms, and on an open path it depends on where the chart starts and ends. The unwrapped fifths path also jumps by 6 whenever a writer swaps a dominant for its tritone substitute. Terms that are sums of squares do not cancel, and they survive a change of writer (TQ 0.50).

## G09-1: Tension breathing, TQ (card 1, lead-lag)

1. **Mechanism.** By the lead-lag theorem, a path's lead-lag Lévy area is half its quadratic variation. For the tension channel, that is how often the harmony switches between tritone and rest.
2. **Recipe.** h = 1 if the chord's pitch-class set holds a tritone. TQ = ½ · mean over changes of (Δh)², computed as \|A(lead, lag)\| / n_chg.
3. **Data.** charts_run09 (unseen).
4. **Prediction.** +0.03 SD per SD. Holding IIV, +0.01 (a reading only).
   - What the mathematics says: only even-order terms survive a change of chart writer, so any song shape upstream of the chart should show in them.
   - **Extrapolation:** a song that lasts runs an engine of expectation and release, switching often.
5. **Kill.** +0.03 lies outside the 95% range.

## G09-2: Tritone resolution on the ii-collapsed path, TR (voice-leading geometry; quotient by ii insertion)

1. **Mechanism.** A dominant's tritone resolves by two contrary semitones. G7→C and D♭7→C share that tritone and that motion. Deleting every "ii" before its V gives a measure that adding or dropping ii-Vs cannot move. That is exactly what the obstacle says chart writers do.
2. **Recipe.** Delete each m7 that is followed by a d7 a fourth up, then merge repeats. TR = (d7 → root down a fifth or down a semitone) / changes.
3. **Data.** charts_run09: charts plus recordings.
4. **Prediction.** If the ii-V lead is the song's goal-directed resolution, +0.04. If it is chart-writer decoration, about 0 while IIV stays positive; this contrast is a lead, not counted. Non-jazz reading +0.02.
5. **Kill.** +0.04 lies outside the 95% range.

## G09-3: Tension engine, TE (card 1, Lévy area and the shuffle identity; estimate only)

1. **Mechanism.** By the shuffle identity, S^{uh} + S^{hu} reads only the endpoints, so the order of events is carried by the area alone.
   - Tension built on the sharp side and held while roots fall by fifths gives a positive area (ii–V–I gives +1).
   - A jump up to V from IV gives a negative one (−½).
2. **Recipe.** Path (u, h), with u the unwrapped fifths position (shortest step −5..+6). TE = A / n_chg on the open path.
3. **Data.** charts_run09.
4. **Prediction.** +0.02. This is an estimate only, since the cross-writer agreement is 0.28.
5. **Kill.** None (estimate).

## Checks

Recipes are frozen in `/home/claude/scripts/geometer/g09_measures.py` (TE, TR, ii_collapse, SIG, CH, base; unit tests reproduce card 1's Eq. 37–39 and time reversal) and in `g09_tq.py` (TQ). The checks are `g09_checks.py`, `g09_alt.py` and `g09_tq.py`, with outputs in `g09_*.json`. They took about 2.5 minutes of compute in total.

How to read the columns:
- **Stab** is over 3,796 run 08 pairs, grouped by normalised title plus artists, with identical chord lists skipped. Many pairs are near-duplicates (forum against playlist), so these values run above the chair's design-song figures (IIV here 0.916, against 0.772 in run 08).
- **Cross** compares a run 09 Real Book or BiaB chart with the first run 08 iReal chart of the same normalised title, for titles of two or more words (n = 2,475).
- **ρ** is pooled Spearman over run 08 charts, with run 09 in brackets.

**A. Proposals**

| | computable run 09 | Stab | Cross | ρ ch_rep | ρ V | ρ ln_chg | ρ IIV | ρ CH | Gate |
|---|---|---|---|---|---|---|---|---|---|
| TQ | 0.992 | 0.900 | 0.503 | −0.14 (−0.19) | 0.40 (0.20) | 0.11 (−0.10) | 0.57 (0.46) | −0.40 (−0.34) | passes |
| TR | 0.992 | 0.905 | 0.60 RB / 0.63 BiaB | −0.16 (−0.16) | 0.30 (0.10) | 0.02 (−0.16) | 0.48 (0.38; recordings 0.66) | −0.43 (−0.42) | passes |
| TE | 0.992 | 0.750 | 0.28 | 0.00 (0.04) | −0.09 (−0.13) | −0.06 (−0.08) | 0.06 (0.09) | −0.02 (−0.17) | passes; fails cross ≥ 0.5 |
| IIV (reference) | | 0.916 | 0.61 | | | | | | |

TQ against TR: ρ 0.74 (run 08), 0.56 (run 09).

**B. Card 1's areas, cross-writer (`g09_alt.py`)**

| Measure | Stab | Cross |
|---|---|---|
| TE | 0.75 | 0.28 |
| TE wrapped | 0.74 | 0.32 |
| M5 root–quality | 0.80 | 0.36 |
| M1 pitch-set fifths-plane | 0.81 | 0.36 |
| M3 arch (τ, u) | 0.75 | 0.29 |
| TE ii-collapsed | 0.73 | 0.29 |

M1 against chirality: ρ 0.48. SIG coordinates cross-writer: 0.14 to 0.39.

**C. Run 09 partition means (TR / IIV)**

| Partition | TR | IIV |
|---|---|---|
| Real Book | 0.28 | 0.09 |
| BiaB | 0.27 | 0.09 |
| weimar | 0.37 | 0.14 |
| jaah | 0.36 | 0.11 |
| isophonics | 0.05 | 0.003 |
| uspop2002 | 0.05 | 0.01 |
| rock-corpus | 0.03 | 0.003 |

Non-jazz TR is sparse, so its power will be low.
