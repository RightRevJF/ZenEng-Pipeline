# Run 07: data

26 November 2026, the 18:17 ET pass.

## Found and used tonight (the way through that run 06 named)
- **Lakh Pianoroll Dataset, LPD-5 cleansed** (Dong et al. 2018; Zenodo 5646574; CC BY 4.0): `lpd_5_cleansed.tar.gz` (555 MB) and `metadata.zip` (cleansed MSD ids, tempo). Downloaded to /home/claude/dl/lpd, outside the repo.
- **Gold-Caps LMD-matched** (Jonason, Casini & Sturm 2023; Zenodo 10178563; CC BY 4.0): `gold-caps_lmd-matched_general_v0.json`, which repeats the Million Song Dataset's artist, title, year and hotttnesss for 31,034 MSD tracks, covering all 21,425 cleansed ids. (millionsongdataset.com is not reachable from here.)
- **Hit Song Prediction** (Zangerle et al. 2019; Zenodo 3258042): `msd_bb_matches.csv` (Billboard Hot 100 peak and weeks for 5,832 MSD tracks), used only as a reported fame reading.
- **Discogs-VI 20240701** `main.zip` (Zenodo 13983028), reduced by the maintainer's `cliques_versions.py` unchanged; **Hooktheory.json.gz** (sha256 917b7cd5…8e0c), used only to exclude seen songs.

## Lessons about the Lakh data (notes side)
- The Lakh match is audio-based. One MIDI file is often the chosen file for several MSD tracks, sometimes up to 12 unrelated titles. Files carrying more than one clean title (8,607 tracks) were dropped; a file under one title and several artists was kept for each (the Skeptic's fix: those are a song and its covers).
- The cleansed set's downbeat vector marks only step 0; bars were taken as 96 steps (4/4, 24 per beat), as the set's own rules allow.
- No separate melody track: the melody is mixed into the five tracks.
- y_foreign's base rate on these songs is 39.7% (18% on single-song artists); power simulations assumed 20%.

## Spent tonight (now seen)
- 5,901 within-artist songs (predictions 9227e71, results 0908976).
- 3,436 single-song-artist songs (prediction 6165846, `cv_w_singletons`).
- Not yet joined: the 8,607 tracks on ambiguous files (they would need a rule for which song each file is).

## Still missing

| Idea | Missing file(s) |
|---|---|
| A powered confirmation of any notes measure at effects near 1 pp per SD | A chord corpus with artist and title several times Lakh's size. Chordonomicon (`chordonomicon_v2.csv`) stays blocked (Hugging Face storage host) and carries no names. |
| R03-I2 tonic resistance on whole songs | A written key per song (MIDI has none; key-finding adds a fitted step). |
| R03-I1 melody transport on whole songs | A separate melody line (Lakh mixes it into the tracks). |
| W01-J6c the MusicLab ceiling | The MusicLab per-song download and rating data (Salganik, Dodds & Watts 2006). |
| R02-breadth | `discogs_20240701_releases.xml.gz` (genres per release), from data.discogs.com (not reachable). |
