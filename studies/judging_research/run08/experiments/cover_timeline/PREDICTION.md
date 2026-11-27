# cover_timeline: momentum or fitness? (R08-L2 merged with R08-G3; card 2). Frozen before any outcome is joined

Run 08, 27 November 2026, by the chair. Card 2 (Evans & Giometto, neutral copying models; counter-evidence). Ideas R08-L2 (the Listener) and R08-G3 (the Geometer, merged in as its gamma readings). This is an **outcome-side** test: it asks whether early covers predict late covers with slope 1 (pure rich-get-richer) or more (hidden fitness). No outcome has been opened by the chair or by any brainstorm agent: no version timeline, year or count has been read. Status: **COUNTED** (one of K = 5), on an assumed outcome scale (see Power).

## Counts (frozen; `models08.timeline_counts`)
For each song (clique): t0 = its first year (`common.load_outcomes`: the clique's earliest dated release); years = each artist set's earliest year (`common.load_timelines`, None dropped).
- **K10** = number of artist sets with earliest year ≤ t0 + 9 (the original included).
- **L** = number of artist sets with earliest year in t0 + 10 … t0 + 29.
- Second model: K15 = sets ≤ t0 + 14; L15 = sets in t0 + 15 … t0 + 34.

## Songs
The run 08 design (5,907 within-composer songs). Drop songs with no first year or no dated set. **Primary: 1950 ≤ t0 ≤ 1994** (pre-1950 Discogs years are often reissues, the Skeptic; t0 + 29 ≤ 2023). All years (t0 ≤ 1994) reported. Second model: 1950 ≤ t0 ≤ 1989.

## Model
**Poisson QMLE: log E[L] = composer FE + 5-year t0 bins + β · log(K10 + 1)** (`models08.poisson_fe`: composer effects concentrated out; composers whose songs have no late set carry no information and drop; cluster-robust SE by composer). β is tested against 1: z = (β − 1)/SE.
- Neutral reading (linear preferential attachment with a shared aging curve, card 2 (a)): **β = 1**. Fitness (content or fame): β > 1. Saturation: β < 1.
- Halves: `common.halves(composer)`, the same model in each half.
- Second model: the same with K15 and L15 (1950 ≤ t0 ≤ 1989).

## Prediction
**β = 1.10** (the Listener; unchanged through round 3).

## Rules (K = 5, α = .01, two-sided)
- **Pass:** p(β = 1) < .01, β > 1, β > 1 in both halves, second-model β > 1. A pass says late covers grow faster than early covers predict under neutral copying: heterogeneous fitness (it does not say the fitness is in the notes).
- **Kill (range kill):** 1.10 outside β ± 1.96 SE. If 1 is inside the range and 1.10 is not, the neutral reading stands for the late phase.
- **Unsettled:** anything else.

## Power (printed again by test.py before β)
The outcome scale is unknown before the outcome is opened, so power comes from a fake urn on the real design (`power_run08.timeline_sim`, 200 draws, α = .01; assumptions: half the design songs fall in the primary window; composer effect N(0, 0.5); K10 − 1 Poisson-gamma (shape 0.8); L Poisson-gamma (shape 1) with mean ∝ (K10 + 1)^β; three scales of mean (K10 − 1, L)):

| Scenario | mean K10 − 1, mean L | power at α = .01 (β = 1.10) | with both halves | kill fires if 1.10 true | kill fires if β = 1 | SE |
|---|---|---|---|---|---|---|
| low | 1.5, 3 | 0.17 | 0.17 | 10% | 41% | 0.063 |
| **middle (the frozen assumption)** | 3, 6 | **0.25** | 0.25 | 8% | 55% | 0.051 |
| high | 4, 10 | 0.305 | 0.305 | 6% | 62% | 0.047 |

The count status is set by the middle scenario (power 0.25 ≥ 0.2), written before any outcome. test.py also prints, before β, a power on the real K10 with fake L (reported only; it cannot change the status or K).

## Reported, deciding nothing
- All years (t0 ≤ 1994) and t0 bands 1900–49, 1950–69, 1970–94.
- **Card 2's urn ceiling** (`models08.urn_ceiling`, c0 = 1, 200 replicates, primary songs): within each 5-year cohort the observed total of late sets is dealt by a Polya urn with weights K10 + c0 (drawn exactly as Dirichlet-multinomial); ceiling = (observed − urn) / observed residual variance of log(L + 1) after cohort and K10 dummies. The most any song attribute, notes included, could explain beyond copying momentum.
- **Gamma readings (R08-G3; the Listener's IIV second reading):** the primary model plus genre dummies plus z(measure) and its frozen extra columns, one measure at a time: TRAV5, econ, T_rep, IIV, ch_rep. The Geometer's bet: γ_T = +0.03. Deciding nothing.

## What it cannot say
Dating error (reissues, missing years) biases β toward 0 and toward 1 alike; Discogs coverage grows over time, which the cohort bins absorb only on average. A β > 1 can come from fame or publishers, not notes. β = 1 does not clear the notes: content may act through K10 itself (card 2 (d)).
