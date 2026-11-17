# Setting words (Luthier v8 research)

`parse_words.py` reads every sung syllable of CoCoPops Billboard (214 songs; lyrics in **silbe) and the 80 Rolling Stone 200 files that
carry **stress (CC BY-NC 4.0; derived counts only) into `sung_syllables.json` (ignored). `words_test.py` measures, for 4/4 songs:
stress against the beat, one-syllable function words on beat 1, the stressed syllable's pitch and length against the rest of its word,
local pitch peaks by stress, the line's last stress (place, length, pitch, rhyme), and vowel classes on high and held notes by singer sex
(SingerSex.txt); and the same for the lead sheets of songs 54 and 55. Stress for Billboard from the CMU dictionary (`pip install
pronouncing`), one-syllable function words unstressed as in Luthier's Window 25. Writes `words_results.json`. `words_more.py` adds the follow-ups from the further reading (stress and metre as contours by domain; voiced endings and vowel length against note length), written to `words_more_results.json`. `pop20c_test.py` runs the same measures by period on the Pop20c corpus (VanderStel and Temperley; clone github.com/vanderstel/pop-corpus into /home/claude/data/pop20c), written to `pop20c_results.json`. `pop20c_rhythm.py` measures melodic rhythm by period, including the 20 post-2000 transcriptions (note lists made by the corpus's own Perl script), written to `pop20c_rhythm_results.json`. `bimmuda_words.py` runs the word measures on BiMMuDa (Hamilton and Pearce, 1950-2022; clone github.com/madelinehamilton/BiMMuDa into /home/claude/data/bimmuda), attaching words only where a section's note count equals a stanza's syllable count and line ends fall on long notes; lyrics are read, never stored. Written to `bimmuda_words_results.json`.
Report: Doc "Setting words for Luthier v8: stress, vowels and high notes".

Scores with words attached: `mxl_words.py` reads MusicXML lyrics (first part with lyrics, voice 1, pickups right-aligned);
`score_words.py` holds the measures (English only, 4/4 and 3/4). `pdmx_words.py` runs them on PDMX (Long et al., Zenodo record
15571083, CC BY 4.0: fetch PDMX.csv and mxl.tar.gz into /home/claude/data/pdmx, then `python3 pdmx_words.py --extract`, then run);
`openewld_words.py` on OpenEWLD (clone github.com/00sapo/OpenEWLD into /home/claude/data/openewld). Results in
`pdmx_words_results.json` and `openewld_words_results.json`.
