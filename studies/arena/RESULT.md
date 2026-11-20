# The arena: six researchers, one lock (19 Nov 2026). Study only; nothing built.
Six agents explored the open half of the artists (README.md gives them the goal, the data, and everything that had failed) and handed back 18 candidates,
16 distinct. Each was run once, unchanged, on the locked half. Rule in LOCK_RULE.md, written before the locked half was read. Full table in lock_results.json.

PASS (predicted sign everywhere, pooled p < .0031):
- concentrated_spectrum (sound): +0.248 on 271 whole recordings, +0.090 on 1,453 previews. Energy gathered in a few low and low-middle bands, the rest left comparatively empty.
- concentrated_and_loose (sound): +0.151, +0.098 (carried by the concentration; see tempo below).
- sound_unlike_its_years (sound): +0.091, +0.093. Distance, in any direction, from the typical hit of its own three years.
- spotify_unlike_its_years (Spotify's readings, 9,195 hits): +0.062. The same idea on a second measurer.
- sparse_onsets (sound): -0.035, -0.093. Fewer sound events per second.
- title_word_rarity / title_specificity (9,195 titles): +0.044 each (one finding). Its author warns it may partly be a matching artefact: a generic title is easier to mismatch.
Control, not a finding about music: hits_still_to_come +0.195 (years the performer went on charting; almost all through "still loved").

FAIL:
- tempo not locked to one value, handed back by three researchers independently: +0.017 on whole recordings, -0.066 on previews. Three agents agreeing on the open half was not evidence.
- Written arrangement from MIDI: spare_arrangement +0.038; low_register_weight +0.075 (p .047), right sign, short of the bar.
- Every candidate on the written tune: long_short_contrast, top_note_isolation (sign reversed), phrase_top_plateau, onbeat_rhythm_surprise. lyric_vocab_concreteness +0.069 (p .0046), short of the bar.
The researchers also reported about 700 further measures on the written tune tried and dropped on the open half (scarcity, localised surprise, memory density, layer dependence, form, phrasing, syncopation, singability, multifractal and other physics).

Reading: what passes is all in the recording. A lasting hit sounds sparse and concentrated rather than dense and bright, and unlike the other hits of its years. Nothing on the written tune passes.

# The two tests the brainstorm voted for (19 Nov 2026). Study only; nothing built.
Rules in votes/PREDICTION.md, written first.
## Same song, different hit recordings
745 works with two or more Hot 100 recordings by different performers (1,713 recordings). Intraclass correlation of lasting love across recordings of the same work:
-0.090 (95% -0.152 to -0.031; label shuffle 95th +0.049). With the performer's standing held -0.101. Versions within three years of each other: -0.058 (220 works).
Control, same title but different songs: +0.013. For scale, same performer, different songs: +0.364. Guess beforehand was +0.10 to +0.25; wrong.
Reading: how loved one recording is now says nothing about how loved another recording of the same song is; if anything one version takes the love and the others lose it.
Lasting love, as Spotify measures it, belongs to the record and the performer, not to the song. (It does not say the song adds nothing to whether SOME version lasts; this design cannot see that.)
Within a work (about 1,250 pairs): the earlier recording is the more loved in 67% of pairs; the more acoustic in 59%; the lower-energy in 56%.
The producer's prediction (the version less like its years is the more loved) FAILS: 48.5%. Valence 48.7%, danceability 49.6%.
## Is "concentrated sound" just "old slow ballad"?
`concentrated_spectrum`, unchanged, 3,472 recordings. With chart peak, five-year bands, tempo bands and seven genre families all held: +0.135 pooled (whole recordings +0.240, previews +0.115; p 1e-15). PASS.
With Spotify acousticness, energy and valence held as well: +0.110. Love +0.099, covers +0.113. Inside tempo thirds: slow +0.147, middle +0.103, fast +0.158.
By era: 1958-69 +0.135, 1970-79 +0.111, 1980-89 +0.193, 1990-2005 +0.049 (not significant; previews only).
Reading: not an artefact of era, tempo or genre, and not confined to ballads. It weakens after 1990.
