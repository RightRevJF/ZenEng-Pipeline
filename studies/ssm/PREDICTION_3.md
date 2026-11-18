# Predictions for the two ideas taken from the other AI's proposal, written before measuring (18 November 2026, 18:15)

The moments study (listeners' timestamped moments, with the words) cannot run here today: its raw timestamps are no longer on this machine and
there is no YouTube key in this session. These two tests run now on the songs already used: CoCoPops (194 Rolling Stone, 214 Billboard with peak
and weeks) and BiMMuDa (290 year-end top-five songs held out from CoCoPops). Melody alone; notes in order; inter-onset intervals in quarters.

S. Scaling (the classic form of "the same order at every scale"): the DFA exponent alpha of the pitch series and of the inter-onset series
(windows of 4 notes up to a quarter of the song). Alpha near 1 is 1/f. The reading is closeness to 1: minus |alpha - 1|.
K. Compression (the "edge of chaos"): the melody as tokens (pitch above the tonic, interval to the next onset), compressed with LZMA; the ratio of
compressed to raw size, lower = more compressible.

S1. Rolling Stone songs sit closer to 1/f than Billboard sample songs, pitch or rhythm (AUC over 0.55).
S2. Inside Billboard, closeness to 1/f relates to peak or weeks past rho 0.15.
S3. Inside BiMMuDa, closeness to 1/f relates to year-end position (one-sided p under 0.05).
K1. A sweet spot: in Billboard, the middle third by compression has a better median peak than both outer thirds, and a quadratic fit of peak rank on
compression rank bends downward (negative square term, p under 0.05).
K2. Rolling Stone songs are more compressible than Billboard songs (AUC over 0.55 for 1 - ratio), as the sameness reading suggested (0.65).
K3. Inside BiMMuDa, the same sweet spot as K1 against year-end position.
What I expect: K2 holds (it repeats the sameness result); S1-S3, K1 and K3 fail, as the related readings did today.
