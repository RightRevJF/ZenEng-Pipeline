# The learned space — predictions written 19 Nov 2026 before anything was fitted

Two graded sets, as before: set 1 (1,102 songs, the first run) and set 2 (634 songs, the lyrics-melody set). Yardstick G.
The space is learned WITHOUT grades, from songs in neither set (Hooktheory songs off the yardstick; lyrics-melody songs
not matched). Points are windows of 8 notes. Because set 2 has no bar lines, the cross-set space uses four coordinates
per note (scale degree on the circle of fifths, height, log time to next note), not six.

 L1 codebook   k-means, 64 regions; a song is the share of its windows in each region
 L2 code       a 16-number bottleneck (autoencoder); a song is the mean and spread of its windows' codes and its
               mean step length through the code space
 L3 words in   as L1, on lyrics-melody songs only, with the syllable's weight as a fifth coordinate

A ridge reader is fitted to G on one group and judged on another it never saw. The score is the partial Spearman of its
reading with G on the unseen group, holding year and note count (and source in set 1).

 T1  L1, fitted on set 1, judged on set 2          > 0
 T2  L2, fitted on set 1, judged on set 2          > 0
 T3  L3, five-fold within set 2 (out-of-fold)      > 0
Pass: > 0 with p < .0125, and for T1 and T2 the reverse direction (fitted on set 2, judged on set 1) also > 0.
Also reported, no pass rule: L3 against its notes-only twin on the same songs (do the words add anything);
and each reading against love and covers apart. Nothing goes into the engine on this study.
