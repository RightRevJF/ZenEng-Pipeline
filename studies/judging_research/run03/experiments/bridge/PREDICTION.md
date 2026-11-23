# Does the chord graph have a bridge? Prediction, frozen before any outcome is joined

Run 03, 23 November 2026, written by the chair. Nothing on the outcome side has been opened: no cover count, version, release, `first_year` or `discogs_versions_matched.json`. Figures marked "chair" come from a check on the notes only: 2,672 songs with at least 3 chords, before the first-year filter.

**Claim (G2 = L2; Devriendt & Lambiotte 2022, Theorem 2).** A link with conductance × effective resistance = 1 lies in every spanning tree. It is a bridge: nothing else connects its two sides. The extrapolation: a coverer cannot re-route that move, so within an artist's own songs, a song with a bridge is covered less.

## Rows
The data are in `studies/judging_data/` and are read only.
- **A song** is a YouTube video id that is a key of `hooktheory_covers_discogs.json`.
- **Its clips** are the clips in `hooktheory_clips.json.gz` with that `video` whose id is also a `k` in both `hooktheory_surprise.json.gz` and `hooktheory_rhythm.json.gz`.
- **Keep a song** if it has at least one such clip, a truthy `first_year`, and at least 3 distinct chords pooled.
- **Artist** = the `artist` of the song's first clip in surprise-file order (the covers study's `cs[0]`). Keep only artists with two or more songs.
- **Data-pack measures** (the 17 in `FE` of `studies/covers/study_covers_discogs.py`) are clip values averaged with weights `n_mel`.

## Measure
- **Chord token:** `((root_pitch_class − tonic) % 12)*9 + qual(root_position_intervals)`, with `qual` as in `studies/surprise/surprise_hooktheory.py`. Tonic = the clip's `keys[0].tonic_pitch_class` (0 if there are no keys). Chords are sorted by onset, and a chord equal to the one before is merged.
- **Moves:** in each clip's merged sequence s, every s[i]→s[i+1], plus the wrap s[−1]→s[0] when the two differ. All of the song's clips are pooled: M[a,b] = number of moves from a to b.
- **No dead ends.** Each clip is a closed walk, so every chord has a way out. Assert out-degree ≥ 1 for every node.
- **Graph:** undirected, unit weights, with a link {a,b} wherever M[a,b] + M[b,a] > 0 and a ≠ b.
- **B** = 1 if any link has cω = 1, else 0.
  - c = 1; Q is the Laplacian; Q† = `numpy.linalg.pinv(Q)`.
  - ω_ab = Q†_aa + Q†_bb − 2Q†_ab.
  - Tolerance: 1e-8.
- **Weights do not matter:** by Theorem 2, a link is a bridge under any positive weights.
- **Disconnected graphs** (110 songs; chair): the pseudoinverse handles each piece on its own. These songs are kept.

## Audit first (no outcome)
1. **Checks that the code is right.** Fix the code before going on if either fails.
   - B from resistance must equal B from `networkx.bridges` on every song (chair: 2,764 of 2,764).
   - Foster's theorem must hold: the sum of cω over links = n − number of pieces, within 1e-8.
2. **Print these:**
   - the share of songs with a bridge (chair: 30.5%; by clips per song: 25% with 1, 34% with 2, 40% with 3 or more);
   - Spearman ρ of B with distinct chords, distinct links, clips per song, merged moves, `kbar` (from `experiments/curvature`) and all 17 data-pack measures (chair: the largest |ρ| is 0.18, with distinct chords).
3. **Stop rule.** Join no outcome, and record the test as "stopped", if either:
   - the share with a bridge falls outside 0.15–0.60; or
   - |ρ| > 0.7 with anything listed in step 2.

## Outcome
**Primary:** log(1 + `covers`), all years.

**Secondary, deciding nothing:** covers within 5 years, and covers more than 10 years after `first_year`.
- Source: `discogs_versions_matched.json`, read as in the maintainer's `within_artist/test.py`.
- Count only versions by other artists: those whose performing artists, after `norm()`, do not include the song's artist slug after `norm()`.
- Within 5 years: year ≤ first_year + 5. After 10: year > first_year + 10. Undated versions are dropped.

## Model
Copy `within()` from `studies/judging_checks/within_artist/test.py` (on `origin/main`):
- standardise y and every column over the rows;
- demean all of them within artist;
- fit OLS with no constant;
- cluster the SE by artist, with statsmodels' small-sample correction.

If statsmodels is missing, use CR1 instead: G/(G−1) · (N−1)/(N−K) · (X′X)⁻¹ ΣX_g′u_g u_g′X_g (X′X)⁻¹, with normal p-values.

**Columns:**
- B;
- `first_year`;
- log(clips per song);
- distinct links;
- `ch_rep`;
- dummies for distinct chords = 4, …, 11 and 12+ (3 is the reference).

**Artist halves:** `int(hashlib.md5(artist.encode()).hexdigest(), 16) % 2`. Fit the same model in each half, with the set of artists fixed on the full rows before splitting.

## Prediction
**β = −0.025** SD of y per SD of B. The SD of B is 0.46, so this is about −0.054 SD for a song with a bridge against one without.

## Power
The script prints the SE and the power before it prints β:

power = Φ(0.025/SE − 2.2414) + Φ(−0.025/SE − 2.2414)

The chair's estimate, scaled from the within-artist SE (0.016 on 1,681 songs) by B's leftover variance after the controls: SE ≈ 0.015, power ≈ 0.29.

## Rules
Tonight counts two tests (this one and `experiments/curvature`), so each needs **p < .025**.
- **Pass:** β < 0, p < .025, and β < 0 in both halves.
- **Kill:** pooled β > −0.01.
- **Unsettled:** anything else. If the halves split, the test cannot pass, but the split does not kill it: each half has power of only about 0.15.
- **Opposite sign** (β > 0, p < .025): reported as "the bridge is the move people remember". It is not a pass; it needs its own rule first.
- **Threshold stays fixed:** if either test is stopped, the other still needs p < .025.

## Reported, deciding nothing
- The secondary outcomes.
- The main model without the disconnected songs.
- The share of move traffic carried on bridges, in place of B.
- Number of songs and artists, and the share with a bridge, in each half.

## What it cannot say
- **Low power:** a null does not clear bridges.
- **Not causal:** a pass would not show that bridges cause fewer covers. An artist's songs still differ in era and singles.
- **What the graph leaves out:** it sees one step only. It ignores direction, rhythm and melody.
- **Clips:** the result depends on which sections users transcribed. Clips per song is held, but not which sections they were.
- **Scope:** hits only. The McGill hold-out is untouched.
