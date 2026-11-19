# Strengthening the four gates

A day of pre-registered tests on what makes music last produced four findings that held on unseen songs. Each is small. Your job is to make ONE of them stronger,
honestly: a better measure of the same thing, tested on a half of the data you never see. The owner (Jason Bryant) wants a purely mathematical standard,
with no human ears, that his song-writing engine can be held to.

## The four findings
1. THE PAGE GATE. Where there is no recording and the forgotten are included, plainer and more predictable tunes are the ones kept.
   23,205 Irish session tunes (kept in players' tunebooks, commercially recorded): a ridge reader over plain page measures scores +0.14 on unseen tunes
   (pentatonic share +0.12, low surprise -0.07, repeated bars, time on the tonic, low pitch and interval variety, few leaps).
   10,360 hymn tunes (number of hymnals printing them; only the opening 15-20 scale degrees known): plainness +0.04, low surprise -0.06.
   Within one artist's work, charted songs are plainer than uncharted ones (+0.07 Lakh MIDI, +0.04 Hooktheory).
   Among songs that are already hits it ranks nothing (covers or lasting love): a gate, not a grade.
2. THE SHELL. Among Hot 100 hits, the recordings still loved and covered decades later lie FAR from the typical hit of their own years, in any direction.
   Distance from the era's centre in the era's own covariance (a Mahalanobis radius over ~54 Essentia sound means): +0.144 on unseen recordings;
   nearness to the centre of the great recordings is NEGATIVE (-0.11): the great do not cluster. Spotify's ten readings: +0.05.
3. THE SOUND. The same lasting hits have a spectrum concentrated in a few low and low-middle bands with the rest left open (`concentrated_spectrum`, +0.12 to +0.25
   on whole recordings), fewer sound events per second, lower Spotify valence (-0.07 with other things held). Robust to era, tempo, genre; about half of it survives
   holding pitch salience, onset rate, high-frequency content and zero-crossing rate.
4. DEVOTION. On last.fm (64,507 tracks, all genres) the sound predicts plays per listener (who comes back) better than listeners (how many came):
   a ridge reader over 53 sound means scores +0.22 genre held; fewer events per second, less danceable, fewer chord changes, darker, less happy.
   Concentrated spectrum does NOT predict devotion.

## What failed (do not hand these back)
Everything on the written tune AMONG HITS; melodic curvature, loops, 1/f scaling exponent as a grade; chord-tone measures; verse-to-chorus surprise drop;
tempo locked to one value; a "plain tune x far recording" interaction; nearness to a cloud of great songs.

## Reading for ideas
/home/claude/reports/Human preference and lasting music.md (an 11,000-word literature report written today: read the parts on your gate, its "computable list",
and its "most promising next tests") and the researchers' notes in /home/claude/research_notes/Human preference and lasting music/.
The day's study write-ups: /home/claude/rightrevjf/zeneng-pipeline/studies/*/RESULT.md.

## Data (the OPEN half only; the other half is locked and you must not open /home/claude/arena2_locked or /home/claude/arena_locked)
`import sys; sys.path.insert(0, '/home/claude/arena2'); import arena2`
- `arena2.session()` -> 11,640 tunes, each a dict: tune_id (also the submission order: early = famous, always held), name, type, mode, meter, tonic_pc, mode_family,
  bars = list of bars, each a list of (midi pitch or None for a rest, duration in quarter-note beats), n (notes), n_settings (how many variant settings players have
  submitted), tunebooks, recordings, Gs (the yardstick: mean rank of tunebooks and recordings, ranked over all tunes), abc (raw).
  Other settings of each tune are in /home/claude/corpus/thesession/json/tunes.json (parse with /home/claude/zeneng/corpus/v39/sabc.py) if you want variants.
- `arena2.hymns()` -> 5,257 hymn tunes: incipit (scale degrees 1-7; U and D shift the octave up or down for what follows; parentheses mark ornamental notes),
  meter, tuneKey, minor, length, n (hymnals), y = log(1+n), composers, born.
- `arena2.gate()` -> 8,364 songs: source ('lakh' whole songs with a guessed voice track, or 'hooktheory' hand-transcribed sections), artist, title, charted (bool),
  notes = list of (onset in beats, midi pitch).
- `arena2.sound()` -> 1,748 recordings x Essentia numbers (two stores: mcgill_whole_recordings, msd_previews) with year, peak, G, love, cover_rank.
- `arena2.hot100()` -> 8,829 hits with Spotify's readings, title, performer, spotify_genre, year, peak, G, love, cover_rank.
- Devotion data: /tmp/claude-0/hspd/hsp-l_acousticbrainz.parquet (73k tracks, columns lowlevel.*, rhythm.*, tonal.*, highlevel.*, uuid, lastfm_listener_count,
  lastfm_playcount) and hsp-l_uuid_year.csv; devotion = log(plays/listeners) with log listeners, year and Essentia genre classes held. The split there is
  int(md5(uuid),16) % 2: use only half 0. /home/claude/zeneng/corpus/v41/devotion.py shows how it was read and scored.
- Scoring helpers that hold the right things: arena2.score_session, score_hymns, score_gate, score_sound.

## The rules
- Explore the open half freely; split it yourself to check you are not fooling yourself. Many tries make lucky hits.
- Hand back exactly ONE strengthened measure for your gate (plus, if you like, one runner-up), as `/home/claude/arena2/candidates/<your_name>.py` defining
  `CANDIDATES = [dict(name=..., kind=..., fn=..., sign=+1 or -1, why="one sentence", baseline="what it should beat and that baseline's open-half score")]`.
  kind and fn signature: "session": fn(list of tune dicts) -> array; "hymn": fn(dataframe) -> array; "gate": fn(list of song dicts) -> array;
  "sound": fn(dataframe) -> array; "hot100": fn(dataframe) -> array; "devotion": fn(dataframe with the parquet's columns) -> array.
  The function gets the WHOLE collection it is scored on (so it may standardise within it or compute era statistics from it) but never the outcome columns:
  it must not read Gs, tunebooks, recordings, n_settings, n, y, charted, G, love, cover_rank, peak, play or listener counts of the rows it is scoring.
  Anything fitted (weights, a model, a codebook) must be fitted at import time on the OPEN half only, deterministically, in under three minutes.
- Plain arithmetic on the data. Nothing needing a human judgment.
- Reply with: what you built and why (plain words), its open-half score against the baseline, how you checked it, what you tried that did not help,
  what the literature report suggested that you could not test for want of data, and your honest odds that it beats the baseline on the locked half.
