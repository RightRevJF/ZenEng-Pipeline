# Tension study (16 November 2026)

For the Doc "Tension research for Luthier v8: building and releasing tension" (https://claude.ai/artifact/HQvP9aJ1NUS4ApTWRm3wTS).

Data (not kept here): CoCoPops Billboard, github.com/Computational-Cognitive-Musicology-Lab/CoCoPops (CC BY-NC 4.0; derived counts only).
`git clone --depth 1 https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops.git /home/claude/data/cocopops/CoCoPops`

| Script | Writes | What |
| --- | --- | --- |
| parse_cocopops.py | cocopops_bars.json (not committed) | 214 songs with melody, 100 with four listeners' arousal and valence and the recording's RMS, as bars |
| tension_features.py | cocopops_features.json (not committed) | Lerdahl chord distance from the tonic and the last chord (checks against Table CO), the old 1-3 chord value, dissonance, melodic height, onsets, sung share, non-chord tones |
| ratings_test.py | ratings_results.json | within-song correlations with arousal; ridge models with per-feature memory, R^2 on held-out songs |
| section_test.py | section_results.json | readings by section role, at the approach to a chorus, and the listeners' split-half agreement |
| profile_test.py | profile_results.json | where each smoothed curve peaks on a normalised time axis |
| engine_songs.py | engine_songs_results.json | the same readings on songs 54 and 55 (lead-sheet MusicXML from songs/p64 and p65 out/) |

Run in order; each script reads the one before. Seeds fixed (20261116).
