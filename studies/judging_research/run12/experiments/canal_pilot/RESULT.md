# canal_pilot: result (notes-only pilot, rank 9)

**Status: PILOT.** No outcome is read; there is no K slot. Three of four predictions held; **P3 is false**.

## The predictions, written first
- **P1:** Spearman(CANAL, −|ΔH1|) > +0.20 and Spearman(CANAL, −|ΔREP_L|) > +0.20.
- **P2:** Spearman(CANAL, −|ΔPI3c|) positive and smaller than both P1 values.
- **P3:** |Spearman(CANAL, −|ΔROUGH_X|)| < 0.15 (voicing belongs to the arranger).
- **P4:** |Spearman(CANAL, mean PCE_ALL)| < 0.30 (CANAL is not simplicity renamed). This is a check of the recipe: the Inventor had seen +0.19.

## What came out (result.json)
- 159 non-duplicate pairs. CANAL median 0.988 (10th to 90th percentile 0.930 to 0.998). 86% of pairs are in the same key.

| Measure | ρ(CANAL, −\|Δ\|) | n |
|---|---|---|
| H1 | +0.52 | 135 |
| E5_L | +0.50 | 159 |
| REP_L | +0.41 | 159 |
| ROUGH_X | +0.34 | 159 |
| PI3c | +0.30 | 135 |
| NPB | +0.23 | 159 |

- ρ(CANAL, mean PCE_ALL) = +0.19.
- **P1 true** (0.52, 0.41). **P2 true** (0.30, below both). **P3 false** (0.34, not under 0.15). **P4 true** (0.19).

## How firm
Descriptive. 159 pairs give each ρ a standard error of roughly 0.08. P4 was a recipe check, not a fresh prediction. Disclosure carried from PREDICTION.md: an earlier invocation wrote a result.json before the predictions existed; it was deleted unread, and only the pair count (159) was seen.

## What it can and cannot say
When two arrangers agree on pitch content, they also agree on the melody's spread, which supports two-file stability as a gate. P3's failure means they also agree on voicing roughness; the likeliest reason is that well-canalised pairs share a source arrangement, so pair agreement may overstate the song's own invariance. It says nothing about covers or uptake.

Credit: Lakh MIDI / LPD (CC BY 4.0).
