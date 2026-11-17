# Melody by genre (Luthier v8 research)

`genre_test.py` measures sung scale degrees in CoCoPops Billboard (214 songs with melody; CC BY-NC 4.0, derived counts only) by family
(hand tagging by artist: soul/R&B, country, others), section and decade: five-note-scale fit, flat 3 and flat 7, the chord under flat 3
and where it goes, the notes v7's fix 200 and tri() would forbid, non-chord tones in verses and choruses; and the same for the lead sheets
of songs 54 and 55. Needs `../tension/cocopops_bars.json` (run `../tension/parse_cocopops.py` first). Writes `genre_results.json`
(committed) and `genre_per_song.json` (ignored). Report: Doc "Melody by genre for Luthier v8: scales, blue notes and the divorce".
