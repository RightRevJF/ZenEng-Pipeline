# Shorter lines, or the chorus? Sung transcriptions against WASABI: prediction

26 November 2026, the songwriting session. Written and committed before any sung transcription is set beside WASABI or beside a cover count.

**Seen before writing:** Design B (`studies/covers_lines`): within a writer, shorter lines went with more covering artists (−0.029 a SD in two independent joins), but not once repeated lines were held (−0.010, p .28), and the two measures correlate (r −0.24). The worry, from the line test: WASABI's lyrics are fans' typing, and famous songs may be typed out in full (every chorus) where lesser songs get "chorus x2", so repetition and short lines could be a typing habit. Of the sung sets I have looked only at their formats: BiMMuDa's lyric files (367 Billboard top-five singles, 1950 to 2022, transcribed by hand from the recordings with stanza breaks; 4 files hold any repeat shorthand) and its metadata.

## Data
- **Sung:** BiMMuDa's lyric files (`/home/claude/data/bimmuda`), one per song, read with the same `linefeat.py` as Design B (stanzas at blank lines).
- **Typed:** the same song in WASABI (the committed `studies/covers_lines/data/wasabi_english_meta.csv.gz` to match; the raw lyrics streamed once for the matched ids only), matched by normalised artist and title, the longest WASABI lyric kept.
- **Covers:** Discogs-VI cliques (main.zip, streamed once), the clique whose title matches and among whose versions' artists the BiMMuDa artist appears (the round-one rule); outcome log of distinct recording artists. Unmatched songs are left out of the covers questions.
- No lyric text is stored; numbers only.

## Questions and rules
1. **Is repetition a typing habit?** For songs in both: WASABI's `repeat_share` less BiMMuDa's. **Named** if the mean excess is at least 0.05 **and** the excess goes up with log recording artists (Spearman, p < 0.05, one-sided). If named, Design B's repetition and short-line passes are read as partly typing. If not, they are read as the songs' own.
2. **Do the two sources agree?** Spearman between WASABI and BiMMuDa for `repeat_share` and for `syl_line`. Described, no mark.
3. **Shorter lines on their own, in sung lyrics.** Across songs (too few per artist for within-writer): OLS of log recording artists on `syl_line` (standardised) with log word count, year, and BiMMuDa's own `repeat_share`. Predicted negative. **Before it is run**, its power is reckoned from fake outcomes (the observed log artists shuffled, an effect of −0.029 a SD planted, 1,000 draws). Under the power floor of 0.2 (R06-5) the coefficient is reported as an estimate and counts for nothing; at or over it, it counts if negative at p < 0.05 one-sided.
4. **Described:** in sung lyrics, Spearman between `syl_line` and `repeat_share` (WASABI's was −0.24).

## What I expect
Question 1 not named: hand transcriptions and fans' typing should both write the chorus out for famous songs, so the excess should be small and flat. Question 3 underpowered, so only an estimate. Question 4 near −0.24, which would say that short lines and returning lines are one trait of the songs themselves (choruses are short-lined and come back), and the drafting note would be about choruses, not line length.
