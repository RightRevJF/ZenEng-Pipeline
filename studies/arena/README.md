# The greatness arena

Goal (Jason Bryant's): a purely mathematical measure, no human ears, that tells GREAT songs from merely good hits.
Yardstick G: a song is great if it is (a) still loved long after release (Spotify popularity in 2021, ranked against Hot 100
songs released within 3 years) and (b) covered by many artists (SecondHandSongs versions, ranked within era). G = mean of the two.
All songs are US Hot 100 hits of 2005 or earlier. "Good vs great AMONG HITS" is the question. Critics are deliberately left out.

## Data you may use (the OPEN half: artists whose name-hash is 0)
`import sys; sys.path.insert(0, '/home/claude/arena'); import arena`
- `arena.tunes()` -> ~1,500 songs, each a dict: set (1, 2, 3 = three transcription sources; analyse each separately, they differ in habits),
  title, artist, year, peak (chart peak), G, G_rank (G ranked 0-1 within its set), love, cover_rank,
  clips = list of clips, each a list of (onset in quarter-note beats, midi pitch) of the sung tune.
  set 1: Hooktheory/CoCoPops/BiMMuDa transcriptions (often a verse or chorus clip, not the whole song); where source == "HT",
         `hooktheory` holds the raw annotations per clip: melody, harmony (chords with root_pitch_class, root_position_intervals), keys, meters.
  set 2: whole songs from karaoke-style MIDI; also `syllables` (one per note) and `durations` (beats). No bar lines.
  set 3: whole songs from Lakh MIDI; the voice track was GUESSED by a rule, so it is noisy. `midi_path` gives the full multi-track MIDI
         (pretty_midi is installed) if you want bass, drums, other instruments, i.e. the ARRANGEMENT.
- `arena.sound()` -> ~1,700 recordings with 127 Essentia/AcousticBrainz sound numbers (lowlevel/rhythm/tonal means and variances),
  store = mcgill_whole_recordings (few, good) or msd_previews (many, 60-second 22 kHz previews); columns year, peak, G, love, cover_rank.
- `arena.hot100()` -> ~9,000 hits: title, performer, year, peak, weeks, spotify_genre, Spotify's 11 audio readings, G, love, cover_rank.
- `arena.partial(values, target, controls)` and `arena.score_tunes(fn)` for partial rank correlations (always hold year and, for tunes, note count;
  for sound/hot100 hold year and peak).
Other raw corpora are under /home/claude/corpus and /home/claude/corpus_new if you need them (unlabelled songs are fine to learn from).

## The lock
The other half of the artists is locked away. You never see it. Whatever you propose is run there ONCE by the coordinator, unchanged.
So explore the open half as freely as you like, but hand back only what you would bet on. Do NOT look in /home/claude/arena_locked.

## What has already been tested and FAILED on unseen songs (do not hand these back)
On the written tune (3,100+ songs): amount of repetition/return, varied return, curvature of the melodic path, persistence (Hurst), dimensionality,
topological loops, DFA scaling exponent of pitch or rhythm and its nearness to 1 (1/f), pace, range, span, step size, leaps, repeated notes,
long notes, mean surprise under a learned predictor, k-means "phrase region" histograms with a ridge reader (passed two sets, failed the third),
an autoencoder code of 8-note windows, newness vs the previous ten years, similarity to the following ten years, mood (valence/danceability)
as predicted from the written tune. On tune-against-chords (Hooktheory, 944 songs): chord-tone share, resolved non-chord tones, notes held across
chord changes, on-beat dissonance, colour tones, chords outside the key, contrary motion to the bass. Same-artist comparisons of all the above: nothing.
Word stress against the tune's accents: leaned positive on 128 well-aligned songs, nothing on 634 loosely aligned ones; unsettled.

## What HAS held (small): the SOUND of the recording
A ridge reader over the 127 sound numbers, fitted on McGill, frozen, scored +0.08 on 2,919 unseen previews (+0.12 with genre and decade held).
Named parts that repeated: more energy in the low band (spectral_energyband_low.mean), spectrum skewed to the low bands (barkbands_skewness.mean)
and peaked (barkbands_kurtosis.mean). About +0.2 on whole recordings, +0.07 on previews. Spotify valence (-0.09) and danceability (-0.08) on 18,000
songs, though danceability did not repeat with a second measurer.

## What to hand back
Write `/home/claude/arena/candidates/<your_name>.py` containing at most THREE candidates, and nothing that needs a human judgment or an AI's opinion
of a song: plain arithmetic on the data only. Each candidate is a function plus a line in a list:
    CANDIDATES = [dict(name="...", kind="tune" | "sound" | "hot100", fn=function, sign=+1 or -1, why="one sentence")]
- kind "tune": fn(song dict) -> float.   - kind "sound" or "hot100": fn(dataframe) -> array of floats, one per row (use only columns that exist).
Functions must be self-contained (imports inside the file), deterministic, and take under a second per song.
A candidate that fits something (a model, a codebook) must fit it inside the file on the open half or on unlabelled songs only.
Then reply with: your three candidates, what each scored on the open half per set, what else you tried that failed, and your honest odds for each.
