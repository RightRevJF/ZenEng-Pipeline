# Setting words (Luthier v8 research)

`parse_words.py` reads every sung syllable of CoCoPops Billboard (214 songs; lyrics in **silbe) and the 80 Rolling Stone 200 files that
carry **stress (CC BY-NC 4.0; derived counts only) into `sung_syllables.json` (ignored). `words_test.py` measures, for 4/4 songs:
stress against the beat, one-syllable function words on beat 1, the stressed syllable's pitch and length against the rest of its word,
local pitch peaks by stress, the line's last stress (place, length, pitch, rhyme), and vowel classes on high and held notes by singer sex
(SingerSex.txt); and the same for the lead sheets of songs 54 and 55. Stress for Billboard from the CMU dictionary (`pip install
pronouncing`), one-syllable function words unstressed as in Luthier's Window 25. Writes `words_results.json`. `words_more.py` adds the follow-ups from the further reading (stress and metre as contours by domain; voiced endings and vowel length against note length), written to `words_more_results.json`. `pop20c_test.py` runs the same measures by period on the Pop20c corpus (VanderStel and Temperley; clone github.com/vanderstel/pop-corpus into /home/claude/data/pop20c), written to `pop20c_results.json`.
Report: Doc "Setting words for Luthier v8: stress, vowels and high notes".
