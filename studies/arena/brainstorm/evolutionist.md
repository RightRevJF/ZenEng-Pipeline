# The evolutionist's contribution: fitness, luck, and the conserved core

## 1. Diagnosis

Three things went wrong, and none of them is "music is not mathematics".

First, the yardstick fuses two different kinds of selection. "Still loved" is mostly selection on a RECORDING (one performance, one sound: the body). "Covered" is selection on the SONG (the tune and chords that pass from artist to artist: the gene). The page was tested against a blend dominated by the body, so of course only sound measures held. The page should be tested against reproduction alone.

Second, luck. Salganik, Dodds and Watts ran the same songs in parallel artificial worlds and found that the best rarely flopped and the worst rarely won, but everything in between landed almost anywhere, because early listeners steer later ones (cumulative advantage: the rich get richer). If the musical share of the yardstick is, say, a quarter of its variance, and a page measure is itself noisy (the three transcription sources disagree), then the highest correlation any perfect measure could show is roughly sqrt(reliability of yardstick x reliability of measure), perhaps 0.3 to 0.4. A 0.25 may be most of what is there. Nobody has measured this ceiling yet; until it is measured, "small" is not a finding.

Third, restricted range and the wrong object. Every test song already passed the first-hearing filter (it charted), so first-hearing traits are used up. And the "page" tested is one transcription of one version. The gene of a song is not its original lead sheet. It is whatever stays the same across all its versions. Nobody has measured that.

## 2. Ideas, most promising first

### Idea 1. The song's breeding value (luck subtracted by replication)

Plain words. A cover is the same song rerun in a different world: another artist, another year, another sound. Quantitative genetics estimates an animal's "breeding value" from how its offspring do across many different mothers and farms. Do the same: estimate how much a song lifts whichever recording carries it. Luck in the original's history cannot fake this, because each cover is a fresh draw.

Mathematics. For every version v of work w by performer a in year t, let y_v = 1 if that version charted (later: its popularity). Fit a mixed logistic model
  logit P(y_v = 1) = b0 + b1 * s(a,t) + b2 * peak(w) + u_w,   u_w ~ Normal(0, sigma_u^2)
where s(a,t) = the performer's number of OTHER chart entries in the five years before t (their pulling power) and peak(w) = the original's peak chart position (so that mere fame of the original is removed). The fitted u_w is the song's breeding value. Drop the original version from the fit so the song is graded only by its descendants. A model-free version: O_w = number of distinct non-original performers who charted with w; E_w = sum over its cover versions of the base chart rate for a performer of that strength in that year; score = log((O_w + 1)/(E_w + 1)). "Heritability of success" = sigma_u^2 / (sigma_u^2 + sigma_performer^2 + pi^2/3); that single number says how much of a recording's fate is the song.

Data. Cover lists joined to the Hot 100 histories: we have both. Popularity of non-charting covers would need a Spotify track dump (several sit on GitHub and Zenodo; check).

Proved wrong if. sigma_u^2 is indistinguishable from zero after controlling peak(w), meaning songs carry nothing from one recording to the next; or page features correlate with u_w no better than they did with the old yardstick (below 0.05 on hold-out).

Odds. 60% that u_w is real and sizeable; 35% that page features predict it clearly better than the old yardstick.

### Idea 2. The no-recording control: folk tunes and hymn tunes

Plain words. In a tradition with no definitive recording, the page is all there is to select on. If the page carries greatness anywhere, it must show there. The Irish session tradition and the hymnal tradition both offer critic-free fitness counts and real variants. Hymn tunes add a gift: one tune is sung to many different texts, so a tune's spread is fitness with the words swapped out, which is exactly the owner's "without words" claim.

Mathematics. Session tunes: fitness F = log(1 + number of players' tunebooks containing the tune), residualised on tune type (reel, jig...) and date added. Hymn tunes: F = residual of log(1 + number of hymnals printing the tune) and of log(1 + number of DISTINCT texts set to it), regressed on year composed and metre class (common metre has more texts available, so it must be controlled). Run the whole failed page battery against F with a locked hold-out. Variants ("settings") of the same session tune supply real mutations for Ideas 3 and 4.

Data. thesession.org publishes a data dump on GitHub (adactio/TheSession-data, tunes in ABC with multiple settings and tunebook counts; verify). Hymn tunes are here ungraded; hymnal and text counts are on Hymnary.org, which may need a request. The Meertens Dutch tune families (annotated variants) are a third source.

Proved wrong if. The page battery scores zero here too. That would be serious evidence against greatness living on the page at all. If it scores well here and zero on hits, the hit failures were the recording drowning the song.

Odds. 55% that at least three page measures hold on folk or hymn fitness at 0.15 or better.

### Idea 3. The conserved core (measure the gene, not one specimen)

Plain words. Biologists find what matters in a gene by lining up many species and seeing which positions never change. Line up many versions of one song and see which notes every performer keeps. Then measure the old features on the conserved notes only, and measure the SHAPE of conservation itself. My guess: great songs have a small rigid core and a large free periphery; humdrum songs are either rigid everywhere (nothing to do with them) or soft everywhere (nothing to recognise).

Mathematics. For a work with versions 1..K, transpose to a common key, scale to common length, align each to the original by dynamic time warping on (pitch class, beat position). For original note i, conservation c_i = fraction of versions with a matching pitch class within a quarter beat of the aligned position. Then (a) core-weighted features: any earlier feature f recomputed as sum(c_i * f_i)/sum(c_i); (b) core shape: bimodality of {c_i} (Sarle's coefficient = (skew^2 + 1)/kurtosis), core fraction = share of notes with c_i > 0.9, and core compactness = longest run of such notes divided by their count. (c) To reach all 3,100 tunes, train a predictor c_i ~ g(metric strength, duration, contour peak or trough, chord tone, number of repeats of the containing figure, position in phrase) on multi-version songs and apply it everywhere.

Data. Lakh MIDI contains many independent arrangements of the same song (use now). Our three transcription sources are a second set of "copies". Session settings are a third. For true covers, the Da-TACOS cover dataset (about 15,000 cover performances with pre-computed chroma, i.e. pitch-class energy over time; hosted via GitHub/Zenodo, verify) allows the same alignment on chroma frames.

Proved wrong if. Conservation is uniform noise (versions agree at chance on which notes to keep), or core shape does not separate graded songs on hold-out.

Odds. 80% that conservation is strongly non-uniform and predictable; 30% that core shape grades greatness.

### Idea 4. Reach across the cover network, with prolific coverers discounted

Plain words. Raw cover count rewards fame. What marks a standard is being covered by UNLIKE artists: country, jazz, punk, choirs, other languages. The network of who covers what reveals artist communities without any genre labels, and lets us discount performers who cover everything (karaoke bands, string tributes).

Mathematics. Build the two-sided network performers x works. (a) Find performer communities by modularity clustering of the performer-performer projection. Participation of work w: P_w = 1 - sum_c (k_wc/k_w)^2, with k_wc its covers from community c. Because P rises with count, use rarefaction (an ecologist's trick): expected number of communities in a random draw of n = 10 covers. (b) Selectivity weighting, by the fitness-complexity iteration from economics: F_w(n) = sum_a M_aw * Q_a(n-1); Q_a(n) = 1 / sum_w M_aw / F_w(n-1); normalise each round. A cover by a choosy performer counts more. (c) Null model: shuffle the network keeping every performer's and every work's cover count; score = observed reach minus shuffled mean, in shuffled standard deviations. (d) Words-off reach, available today: share of a work's versions whose title differs from the original's (translations, new lyrics) and share by instrumental performers. A tune that survives losing its words is the owner's claim in a single number.

Data. SecondHandSongs lists: have. If version dates exist, add late-cover share (covers by artists who debuted 20+ years after release).

Proved wrong if. Rarefied reach is just cover count again (correlation above 0.9 after rarefaction), or page features predict it no better than raw count.

Odds. 70% that it is a distinct, sharper yardstick; 30% that the page predicts it at 0.15 or better.

### Idea 5. Transmissible surprise (what survives the telephone game)

Plain words. Mean surprise failed, and artificial perturbation failed, because neither asks what a human copier does. In sung telephone-game experiments (Anglada-Tort and colleagues, 2023) tunes drift toward small intervals, simple rhythms and arch shapes. A tune that sits AT that resting point is banal; one far from it is forgotten. The fit tune is mostly resting-point material plus one or two odd features that survive copying anyway. Measure surprise only where it is copy-proof.

Mathematics. Learner L = a melody model trained on folk and hymn tunes (survivors of oral copying). One generation: corrupt each note with probability e (deletion, or interval shrunk toward a step), then replace the corrupted stretch by L's most probable filling given context. Run R = 200 chains of G = 10 generations. For each figure g in the tune (every 3 to 7 note window): survival s_g = fraction of chains in which g is intact at generation G; distinctiveness d_g = -log2 P(g) under a hit-corpus model. Score T = max over g of s_g * d_g, and T_sum = sum over non-overlapping g. Also report drift D = mean edit distance to the original at generation G; the prediction is that graded songs have ordinary D but high T.

Data. Have everything; the copying-error model can be tuned on session settings or Lakh duplicates (real variants).

Proved wrong if. T does no better than mean surprise on hold-out (near zero).

Odds. 25%.

### Idea 6. Degeneracy: how many different bodies fit the same song

Plain words. Every held result says the loved thing leaves ROOM: sparse spectrum, fewer events. In biology, many gene sequences fold to one shape, and such "many-to-one" traits are both sturdy and easy to evolve. A song many arrangers can dress differently, while staying itself, invites covers. Jazz standards are exactly tunes that tolerate re-harmonising.

Mathematics. Train a chord model on Hooktheory: hidden chord states, melody notes as emissions. For melody m, harmonic degeneracy H_w = entropy per bar of the distribution over chord sequences given m (computed exactly by the forward-backward algorithm). Tempo and metre tolerance: change in melody-model likelihood when durations are requantised to 3/4 or swung, or tempo-scaled by 0.5 and 2. Empirical check: across Lakh arrangements of one song, entropy of chord choice per bar, and variance of tempo and instrumentation.

Data. Have.

Proved wrong if. H_w is unrelated to cover reach (Idea 4) and to breeding value (Idea 1) on hold-out; or relates only through pace.

Odds. 30%.

### Idea 7. Measure the ceiling first

Plain words. Before another feature is tried, find how much of the yardstick is song at all. Three cheap estimates, each a number.

Mathematics. (a) Split-world: for hits that charted in the US and in other countries, correlate residual longevity (weeks charted given peak) between countries; that correlation bounds the song-plus-recording share. (b) Heritability from Idea 1. (c) Citation-style fitness: if cover dates exist, fit each work's cumulative covers to the Wang-Song-Barabasi curve c(t) = m * (exp(lambda_w * Phi((ln t - mu_w)/sigma_w)) - 1), where Phi is the normal cumulative curve; lambda_w is fitness with rich-get-richer growth divided out. Ceiling for any feature = sqrt(song share x feature reliability), feature reliability being its agreement across the three transcription sources.

Data. US charts have; foreign charts exist on GitHub in several collections (check); cover dates uncertain.

Proved wrong if. Not falsifiable as such; it is a calibration. But if the ceiling comes out near 0.25, the search is largely finished and the sound findings are the answer.

Odds. 90% it yields a usable number; my guess for the ceiling is 0.3 to 0.45.

## 3. The wild idea

Greatness cannot be seen in a single specimen at all. The owner's statue is not the song; it is the CLOUD of all its versions plotted in feature space. A great song's cloud is a star: a point-like centre (the conserved core, identical everywhere) with long arms in every direction (tempo, harmony, timbre, language). A humdrum song's cloud is a small blob. Compute it as the ratio of spread in free dimensions to spread in core dimensions: the eigenvalue spectrum of the covariance of version features, with greatness = a few near-zero eigenvalues beside many large ones. The bolder half: this shape is predictable from the page before any cover exists, by Ideas 3c and 6, as the song's capacity to be many things while remaining one. If so, a great song is not a finished object but a precisely specified invitation, and the mathematics of greatness is the mathematics of what is fixed against what is left open.
