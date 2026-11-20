# Physicist's contribution: past the single exponent

## 1. Diagnosis

Everything on the page failed for a reason physics predicts. A critical exponent is a *universal* quantity: by construction it is blind to the details of the system and is shared by every member of a class. Finding S near 1 in all hits says they belong to one universality class (the class "tunes people can follow"); it cannot rank the members, any more than the exponent 0.326 ranks one magnet above another. What distinguishes members of one class is always *non-universal*: the amplitudes, the size of the corrections to scaling, the position along the critical surface, the symmetry that gets broken and how, and above all the *response* to being pushed. Nearly all forty tests measured one-song, equal-time, scalar summaries of the page, which are the universal-ish quantities. The yardstick, by contrast, is a response function: "covered by many" means "perturbed many times and still itself"; "still loved" means "slow relaxation". A response cannot be read off a single equilibrium snapshot unless a fluctuation-dissipation relation holds, and music is far from equilibrium (it has an arrow of time). Two further points. (a) Range restriction: every song tested is already a hit, so we are sampling a thin shell around the critical surface and the control variables that got songs there have had their variance cut off. (b) The yardstick itself is the outcome of a rich-get-richer branching process (a cover begets covers), and near the critical point of such a process most of the outcome variance is amplified chance. Rank correlations of 0.05 to 0.25 may be close to the ceiling for raw cover counts; the hidden "fitness" underneath is the thing worth predicting (Idea 3).

### What "sparse, concentrated spectrum; unlike its neighbours" means in my language

- **Sparse, concentrated spectrum = condensation, a low participation ratio.** Energy sits in a few modes and the rest are unoccupied, like a condensate or a low-temperature state, where a "dense bright wall" is the high-temperature, maximum-entropy state (all modes equally filled, nothing distinguishable). The standard measure is the participation ratio PR = (sum_k E_k)^2 / sum_k E_k^2, the effective number of occupied modes. Low PR also means a large *null space*: many directions in which something can be added without touching what is already there. That is room for a cover artist. In information-geometry terms the song is "sloppy" (gloss: a few combinations of its parameters are rigidly fixed, and most can be changed freely without changing what it is). I read the finding as: **a great song fixes few things hard and leaves many things free.**
- **Unlike its neighbours = a separate basin of attraction.** In an associative memory holding many patterns, a pattern is recalled reliably when its overlap ("crosstalk") with the other stored patterns is small. A recording unlike the other hits of its years has a wide basin in collective memory: a fragment of it cannot be mistaken for anything else. That the same measure on the written tune scores zero says the basin is defined in the space of *sound*, and that the tune-level descriptors used so far do not carry the coordinates memory actually uses.
- **Fewer events per second** is the same statement in time: low occupancy, room left.
- Caution I would want checked before building on this: sparse recordings are also older recordings (pre loudness-war), and older songs have had longer to gather covers. The finding must survive within a release-year band.

Putting the two together gives my central conjecture, a candidate for the "extremised quantity":

> **A lasting song maximises the volume of performances that are still recognisably it.** Equivalently, it has the largest *symmetry group* (set of transformations that leave its identity unchanged) at fixed distinctness from other songs.

Write Omega_s = log volume of {performances x : a listener identifies x as song s}. Greatness is large Omega_s together with a large margin Delta_s from other songs. Free-energy form: F_s = -Delta_s - T * Omega_s, low F lasts. The conserved quantities are the few stiff coordinates every cover keeps; by the logic of Noether's theorem, each freedom the song grants a performer corresponds to something that does not matter to its identity, and the fewer things that matter, the more ways it can live.

---

## 2. Ideas, most promising first

### Idea 1. The stiff-sloppy spectrum of a song (identity geometry measured on real covers)

**Plain words.** Stop measuring songs and measure the *cloud of versions* of each song. Across covers, some features barely move (stiff: these are the song) and others range freely (sloppy: these are the performer's). The conjecture is that great songs are extreme: a small, very rigid core and an unusually wide free shell. The earlier "robustness under perturbation" test asked one scalar question (how robust); this asks for the shape (robust in which directions, free in which).

**Mathematics.** For work s with versions v = 1..n_s, compute a feature vector x_{s,v} in R^d (tempo, key, chroma/HPCP statistics, onset density, MFCC statistics, melodic-contour descriptors). Let B = pooled between-work covariance and W_s = within-work covariance of work s (shrink towards the pooled within-covariance W-bar, since n_s is small: W_s' = (1-a) W_s + a W-bar). Whiten by the pooled within-covariance and take eigenvalues lambda_1 >= ... >= lambda_d of W-bar^{-1/2} W_s' W-bar^{-1/2}. Three numbers per work:
- free volume Omega_s = (1/2) sum_i log lambda_i (log volume of the version cloud relative to a typical work);
- anisotropy A_s = variance of log lambda_i (how hierarchical: few stiff, many free);
- stiff-core rank k_s = number of lambda_i below 1/4.
Then the predictive step, which is what removes the circularity: learn from covered works which directions are typically stiff (the eigenvectors of W-bar with smallest eigenvalue: call the span "identity space" P) and which are free (Q). For *any* single recording or MIDI arrangement, compute its distinctness in identity space, Delta_s = distance from x_s to its k nearest neighbours of the same years measured only in P, and its "occupancy" in Q. Prediction: yardstick rises with Delta_s in P and is indifferent to distance in Q. This would also explain why "unlike its neighbours" was weak (+0.09): it mixed stiff and free directions.

**Data.** Needs feature vectors for many versions of the same work. Not in hand. Da-TACOS (MTG, on GitHub and Zenodo; I believe about 15,000 performances of 3,000 works drawn from SecondHandSongs, with pre-extracted chroma, HPCP, MFCC, key, tempo and onset features, no audio needed; verify before relying on it) is exactly this. A weaker in-house proxy: Lakh has several independent MIDI transcriptions of many songs, and there are three transcription sources for tunes; transcriber disagreement is a perturbation ensemble too. For the predictive step, the 3,500 Essentia recordings.

**Wrong if.** Version clouds of much-covered and little-covered works have the same shape once the number of versions is matched (subsample to equal n); or distance in P predicts no better than distance in Q or in the full space.

**Odds.** 30% that P-distance beats raw distinctness on hold-out; 20% that anisotropy itself grades songs.

### Idea 2. Condensate fraction of the arrangement (carry the one solid finding from sound to symbols)

**Plain words.** The strongest held result is spectral concentration in the recording, where we have only 127 summary numbers. The 1,400 graded multi-track MIDI arrangements let the same physical idea be computed exactly, with no audio: how many independent "modes" does the arrangement occupy in pitch and time, and how much is left empty. If it holds there, greatness is a property of the *arrangement* (written, quantifiable, earless), sitting between the page that failed and the sound that worked.

**Mathematics.** Build the piano-roll matrix M (rows = 88 pitches or 24 quarter-octave bands, columns = time frames of a sixteenth note, entries = summed velocity x sounding).
- Register participation ratio: E_k = sum_t M_kt^2, PR_f = (sum E_k)^2 / sum E_k^2.
- Temporal occupancy: fraction of (band, frame) cells that are non-zero, and events per second.
- Condensate fraction: singular values sigma_i of M (after removing the column mean), c_1 = sigma_1^2 / sum sigma_i^2, and effective rank R = exp(-sum p_i log p_i) with p_i = sigma_i^2 / sum sigma_j^2. Low R means the arrangement is a few modes repeated.
- Spectral gap: the widest empty interval (in semitones, time-averaged) between the bass voice and the next voice up; and the gap ratio sigma_1/sigma_2.
- Null-space room: 1 - (occupied band-time cells) / (cells within the song's own range).
Compute all within release-year bands and within genre.

**Data.** Have it: Lakh clean MIDI, ~1,400 graded. Then check against the Essentia spectral numbers for the same songs.

**Wrong if.** No arrangement-level sparsity measure reaches even +0.08 on the hold-out within year bands, or the audio finding itself vanishes within year bands (then it was an era effect).

**Odds.** 30% it transfers to MIDI; 60% the audio effect shrinks noticeably but does not vanish under year control.

### Idea 3. Look for criticality in the response, and replace the yardstick with a fitness

**Plain words.** The critical dynamics that separates lasting from fading songs may be in how the world responds, which is a time series we already hold: weekly chart histories and dated covers. In the theory of self-exciting processes, a burst that grew by word of mouth near the critical point rises slowly and decays slowly and symmetrically; a burst that was pushed from outside spikes and collapses. Separately, raw cover counts are inflated by rich-get-richer; dividing that out gives each song an intrinsic fitness, a cleaner target for every other idea.

**Mathematics.**
(a) Chart shape. For each hit, take rank-derived activity a(t) (e.g. 101 - rank, or a points scale) around its peak time t_c. Fit the rise a ~ (t_c - t)^(-p_up) and the decay a ~ (t - t_c)^(-p_down). The Crane-Sornette classification for an epidemic process with memory kernel ~ t^-(1+theta): pushed and subcritical, decay exponent 1 + theta (fast, no precursor); pushed and critical, 1 - theta; self-grown and critical, 1 - 2 theta with a matching rise. Simple statistics do nearly as well: fraction of chart life before the peak (precursor fraction), weeks to peak, and the asymmetry (area before peak)/(area after).
(b) Cover kinetics. Fit each work's cover times to a Hawkes process (gloss: each event raises the rate of later events): rate(t) = mu_s + sum_{t_i < t} n_s * phi(t - t_i), phi a normalised power-law kernel. The branching ratio n_s (average number of covers triggered per cover) is the distance from criticality: n_s near 1 means the song sustains itself. Also the long-time exponent of the cover rate, rate ~ t^-gamma: small gamma means ageing without forgetting.
(c) Fitness. Model rate_s(t) = eta_s * (k_s(t) + 1) * A(t - t_s), with k_s the covers so far and A a common ageing curve estimated from all works (Bianconi-Barabasi fitness model). Estimate eta_s by maximum likelihood. Use eta_s, not the count, as the yardstick for all musical tests.

**Data.** Have it: chart histories for ~18,000 hits, SecondHandSongs version lists (need the year of each version; if the lists lack years, that is the gap).

**Wrong if.** Chart shape in the first chart run does not predict later covers and present-day love beyond peak position and weeks on chart; or musical features correlate no better with eta_s than with raw counts.

**Odds.** 40% that precursor fraction or decay exponent predicts the yardstick at 0.1 or better beyond peak rank; 35% that switching to eta_s raises the existing small correlations. Plainly: (a) is not a property of the notes. It is a no-ears early readout of greatness and a better target, which may be worth more than another feature.

### Idea 4. Identity under coarse-graining: which of a song's features are "relevant"

**Plain words.** Renormalisation asks what survives when you blur. Blur every tune from notes to beats to bars to phrases and ask, at each level of blur, whether the song can still be told apart from twenty thousand others from a short excerpt. Features that keep distinguishing songs as you blur are "relevant" (they grow under the flow); those that wash out are "irrelevant". The conjecture: a merely good hit is distinguished only by fine detail, while a great one is still itself as a four-bar skeleton, so its identity sits in relevant directions. This differs from the failed 1/f test, which asked whether the *statistics* look alike across scales; this asks whether the *identity* survives.

**Mathematics.** Coarse-graining map C_b: partition time into blocks of b beats (b = 1/2, 1, 2, 4, 8, 16); replace each block by (duration-weighted mean scale degree, first-note scale degree, onset count, chord root if available), transposition- and tempo-normalised. For an excerpt of L blocks, define a similarity kernel between coarse-grained excerpts (e.g. exp(-beta * alignment distance)). Identity information of song s at blur b and length L:
I_s(b, L) = log N + E_x [ log p(s | C_b x) ], p(s | y) = sum over excerpts of s of K(y, .) / sum over all N songs' excerpts of K(y, .),
with x ranging over excerpts of s held out from the reference set (use other sections, or another transcription source, as reference). Per song: the blur half-life b*_s (the b at which I_s falls to half its b = 1/2 value at fixed L = 8), and the minimal cue length L*_s (smallest L with p(s|x) > 1/2: "name that tune in L notes"). Ensemble version: at each b compute the between-song covariance Sigma_b of block descriptors; directions whose share of variance grows with b are the relevant operators; score each song by its squared projection on them.

**Data.** Have it: ~3,100 graded tunes plus ~20,000 Hooktheory melodies as the confusion set.

**Wrong if.** b*_s and L*_s are flat across the yardstick within year and source bands. Given that tune-level distinctness already scored zero, this is a real risk; the coarse-graining axis is the only new element.

**Odds.** 12%.

### Idea 5. The arrow of time: entropy production and who leads whom

**Plain words.** Equal-time coupling between pitch, rhythm and harmony was tested and failed. A system out of equilibrium is characterised by something that test cannot see: net circulation, the difference between the piece forwards and backwards, and which field moves first. A chord loop that goes round one way and never the other is a probability current. Great songs may drive harder (more directed motion per note) or may have a characteristic order of leadership, e.g. harmony changes announced by rhythm.

**Mathematics.** Joint state z_t = (scale degree, position in bar, chord function) or any pair. Estimate transition counts with smoothing; stationary p(z) and transitions p(z -> z').
- Entropy production per step (gloss: how distinguishable the song is from itself played backwards): sigma = sum_{z,z'} p(z) p(z -> z') log [ p(z) p(z -> z') / ( p(z') p(z' -> z) ) ]. Zero if reversible.
- Cycle currents: J(z, z') = p(z) p(z->z') - p(z') p(z'->z); total circulation = (1/2) sum |J|; and the share of sigma carried by the single strongest cycle (one dominant loop versus diffuse drift).
- Leadership: transfer entropy T_{X->Y} = I(Y_{t+1}; X_t | Y_t) for each ordered pair of fields (pitch, rhythm, harmony; with MIDI add bass, drums, loudness from velocity), and the antisymmetric part T_{X->Y} - T_{Y->X}.
- Cross-scale version: the same sigma computed on the coarse-grained sequences of Idea 4; an irreversibility spectrum sigma(b). A song with an arrow at every scale (notes, phrases, sections) has a direction, not merely a groove.
Compare each against a time-shuffled-within-bar surrogate to remove the trivial part.

**Data.** Have it: tunes, Hooktheory melody+chords, MIDI arrangements.

**Wrong if.** sigma, the dominant-cycle share and the transfer-entropy asymmetries are all flat on hold-out.

**Odds.** 10%. It is the one family of page measurements the forty tests did not touch, which is the case for trying it, no stronger.

### Idea 6. Order parameter, its fluctuations, and finite-size scaling (non-universal amplitudes)

**Plain words.** If the exponent is universal, measure what is not. A key is a broken symmetry (all twelve transpositions were equivalent until the song chose one), and the degree of that ordering, how much it wobbles, and where it slips are song-specific. Likewise the ratio of the song's correlation length to its own length: a finite system at criticality has correlations spanning the whole of it, and a song that is "one thought" from first bar to last should show that, while a song assembled from parts should show a shorter length.

**Mathematics.**
- Tonal order parameter: in a sliding window w with pitch-class weights h_w(c), c = 0..11, take the discrete Fourier coefficients f_k(w) = sum_c h_w(c) exp(-2 pi i k c / 12) / sum_c h_w(c). |f_5| measures diatonic order, arg f_5 the key. Per song: mean order m = <|f_5|>, susceptibility chi = N_w * Var(|f_5|), Binder cumulant U = 1 - <|f_5|^4> / (3 <|f_5|^2>^2) (a scale-free shape number for the fluctuations), and the count and position of phase slips (jumps of arg f_5 beyond a threshold: modulations, borrowed chords). Same construction for metre with onset positions in the bar in place of pitch classes.
- Amplitudes and corrections: fit the fluctuation function F(n) = A n^alpha (1 + B n^-omega); keep A and B, discard alpha.
- Finite-size ratio: xi_s / L_s, where xi_s is the block size at which F(n) departs from its power law (or the lag at which the autocorrelation of the coarse-grained contour first loses significance) and L_s the song length.

**Data.** Have it.

**Wrong if.** None of m, chi, U, slip placement, A, B, xi/L grades songs on hold-out. Tension-resolution and multifractal tests already covered nearby ground and failed.

**Odds.** 7%.

---

## 3. The wild idea

**The grade is the coupling g, and g lives in the residual field: recording minus page.** In S = 1 + g/pi, read the "1" as the page (everyone's tune sits at criticality, which is why it grades nothing) and g as the coupling between the written song and the field of deviations a performer lays over it: the microtiming (each note's onset minus its notated time), the pitch drift of the voice against the notated pitch, the loudness curve. That deviation field delta(t) is where every surviving result was found (all in the recording, none on the page). Conjecture: (i) in great recordings delta(t) is itself long-range correlated, with its own exponent near 1, and (ii) it is *coupled to the structure of the page*: deviations grow and shrink with the phrase and section hierarchy, so the cross-spectrum between delta(t) and the page's own structural signal s(t) (metrical weight, phrase position, harmonic rhythm) follows a power law, |S_{delta,s}(f)| ~ f^-beta, with coherence high at the low frequencies (sections) and falling at the high (notes). Define g operationally as pi * (S_delta - 1) or as the low-frequency coherence between delta and s. A great song would then be one whose page *invites* this coupling in any performer, which is why it survives covering: each cover re-establishes g with a different delta. The sparse spectrum is the precondition: deviations are only audible, and only free, where the texture leaves room.

Data: needs note-level alignment of recordings to scores, which we lack (no raw audio). Possible sources: DALI (vocal notes aligned to audio, annotations on Zenodo/GitHub; audio must be fetched separately), unquantised performance MIDI within Lakh (microtiming and velocity survive in some files; detectable by onset times off the grid), and jazz-solo transcription sets with measured onsets. A first cheap look: split the Lakh files into quantised and performed, and in the performed ones compute the scaling of the microtiming series and its coherence with metrical weight. I would not defend this in public because g so defined mixes the song with the performance, and the yardstick rewards the song. But it is the only reading I can find under which the owner's formula, the page's failure and the recording's success are all the same fact.
