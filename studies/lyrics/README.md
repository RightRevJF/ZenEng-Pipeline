# Lyric craft (17 November 2026)

Doc: https://claude.ai/artifact/D5HXXMxiKS8RHJzhUjwi6o

- `lyrics_features.py`: lyric measures (repetition, variety, word frequency, pronouns, concreteness, story features, feeling per line,
  absolutes, rhyme, title count) for the CoCoPops Rolling Stone files with syllables (80) and Billboard transcriptions (214), one line
  rule for both (a gap of half a beat, a word held two beats, a new section). Writes `lyrics_rows.json` (derived numbers only).
- `lyrics_analyse.py`: greatest-list (Rolling Stone 500) against Hot 100 sample, 1958-1991, shuffled within decades. `lyrics_results.json`.
- `lyrics_our_songs.py`: songs 52 to 56. `lyrics_our_songs.json`.
Needs: pip install wordfreq vaderSentiment; Brysbaert concreteness norms at /home/claude/data/norms/concreteness.txt
(raw.githubusercontent.com/ArtsEngine/concreteness); spaCy en_core_web_sm; pronouncing. No lyric text is stored.
