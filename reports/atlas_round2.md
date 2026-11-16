Round 2 extended the atlas with three more sources and was added to the atlas Doc (https://claude.ai/artifact/58vnmJPuJ8U9hyDLq47SVR). The tables are in tables/metre_atlas: lieder_mxl.json, ewld_mxl.json, symbtr_usul.json, with each table tagged by its licence.

## Sources added

- **OpenScore Lieder (CC0):** sung art songs with per-note lyrics in MusicXML, read for metre tables and English stress-to-beat alignment.
- **OpenEWLD (MIT):** public-domain lead sheets with chords, for popular-song tables in 4/4, 2/2, 3/4 and 6/8.
- **SymbTr (CC BY-NC-SA 4.0):** Turkish makam pieces with usul (rhythmic cycle) annotations and lyric syllables, for additive metres.

## Findings

- **Stress-to-beat in English holds across compound metres.** In hymns, art songs and lead sheets, stressed syllables fall on strong beats at 84 to 86% in 6/8, 82% in 9/8 and 84% in 12/8. English text-setting rules can carry into compound metres unchanged.
- **Additive groupings can be learned from the notes.** Scoring every arrangement of 2- and 3-pulse groups against where onsets fall recovered the traditional groupings from the music alone: aksak 2+2+2+3, türk aksağı 2+3, devr-i hindi 3+2+2, devr-i turan 2+2+3, curcuna 3+2+2+3. The engine can take additive metres as groupings and learn each grouping's onset weights.
- **Pitch readings carry across metres; rhythm readings do not.** The felt metre matters more than the notated one, and vocal tables must come from sung tunes.

## Licences

Lieder is CC0 and EWLD is MIT; both are usable without restriction. SymbTr is non-commercial (CC BY-NC-SA). The Essen tables through music21 are non-commercial too.
