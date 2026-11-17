"""Post-clean fixes for words.md (Part 23): the chart picture, paragraphs split at page breaks, the vowel table, the files list."""
import re, base64, sys
PNG = sys.argv[1]
md = open("words.md").read()
png = base64.b64encode(open(PNG, "rb").read()).decode()
pat = re.compile(r"<!-- Start of picture text -->.*?<!-- End of picture text -->\n\n(studies/words/words_test\.py on [^\n]*)\n", re.S)
assert len(pat.findall(md)) == 1
md = pat.sub(lambda m: f"![Songs 54 and 55 put weak syllables on beat 1 two to three times as often as hits do](data:image/png;base64,{png})\n\n*Source: {m.group(1)}*\n", md)
md = md.replace("on [CoCoPops](https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops) Billboard", "on CoCoPops Billboard", 1)
# rejoin text split across pages: a block starting lower-case continues the block before it
lines = md.split("\n"); out = []
for l in lines:
    if l and l[0].islower() and len(out) >= 2 and out[-1] == "" and out[-2] and not out[-2].startswith(("|", "!", "#")) and not re.search(r"[.:;!?)*]$", out[-2].rstrip()):
        out.pop(); out[-1] = out[-1] + " " + l
    else: out.append(l)
md = "\n".join(out)
a = md.index("|Notes|Men:|"); b = md.index("\n\nHeight alone", a)
md = md[:a] + """| Notes | Men: open | Men: close | Men: reduced | Women: open | Women: close | Women: reduced |
|---|---|---|---|---|---|---|
| All sung notes | 48% | 30% | 22% | 49% | 32% | 19% |
| Top tenth of the song's range | 50% | 32% | 18% | 52% | 34% | 14% |
| At or above E4 (men) / C5 (women) | 49% | 32% | 19% | 51% | 39% | 10% |
| Held a beat or more | 59% | 30% | 11% | 56% | 36% | 9% |
| Held and in the top tenth | 61% | 32% | 7% | 55% | 38% | 8% |""" + md[b:]
md = re.sub(r"` ([.:,;)])", r"`\1", md)
a = md.index("- `parse_words.py`:"); b = md.index("\n\nData:", a)
md = md[:a] + """- `parse_words.py`: every sung syllable of CoCoPops Billboard and the Rolling Stone 200 files with stress, with its note, place in the bar, length, section and line start.

- `words_test.py`: the measures in this report, for the corpora and for songs 54 and 55.

- `words_more.py`: the follow-ups from the further reading (stress and metre as contours, voiced endings and length).

- `pop20c_test.py`: the same measures by period on the Pop20c corpus, 1900 to 1999.

- `pop20c_rhythm.py`: melodic rhythm by period, with the post-2000 songs.

- `bimmuda_words.py`: the word measures on BiMMuDa, 1950 to 2022, words attached by exact count.

- `mxl_words.py`, `score_words.py`, `pdmx_words.py` and `openewld_words.py`: the measures on scores with words attached (PDMX, OpenEWLD).

- `words_results.json`, `words_more_results.json`, `pop20c_results.json`, `pop20c_rhythm_results.json`, `bimmuda_words_results.json`, `pdmx_words_results.json` and `openewld_words_results.json`: every figure in this report. `sung_syllables.json` is not committed; the parser rebuilds it.""" + md[b:]
if "Data: [CoCoPops]" not in md: md = md.replace("Data: CoCoPops, CC BY", "Data: [CoCoPops](https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops), CC BY", 1)
md = re.sub(r"(?m)^### (\*\*)?(Sources read:|Checks for the port:|Measured:)(\*\*)?$", r"\2", md)
md = re.sub(r"(?m)^### (In the repo, `studies/words/`:)$", r"\1", md)
md = md.replace("(Proto 2013)", "([Proto 2013](https://hispadoc.es/descarga/articulo/4147297.pdf))")
md = re.sub(r"(\d{4})\u2013 (\d{4})", lambda m: m.group(1) + "\u2013" + m.group(2), md)
md = re.sub(r"\n\n### (inside the word, not a lengthening rule\.)", lambda m: " " + m.group(1), md)
# a table split across a page: the second half's broken header and wrapped cells
i = md.find("|1980–1999 (17)|10%|")
if i > 0:
    j = md.find("\n", i); k = md.find("\n\nThe anticipation peaks", j)
    md = md[:j] + "\n|2000–2019 (11)|11%|42%|13%|26%|6.1|\n|Song 54|13%|41%|13%|21%|4.2|\n|Song 55|12%|40%|15%|38%|4.4|" + md[k:] if "|Period|Notes on|" in md[j:k] else md
md = re.sub(r"\n\n### (anticipation of the last stress is new\.)", lambda m: " " + m.group(1), md)
md = md.replace("### What it shows:", "What it shows:")
a = md.find("|Corpus, style")
if a > 0:
    b = md.find("\n\nWhat it shows:", a)
    md = md[:a] + """| Corpus, style and metre (songs) | Weak syllables on beat 1 | Function words on beat 1 | Stresses on beat 1 | Stress lower than its word | Opposed across words | Voiced / voiceless ending long | Held top notes: open / reduced |
|---|---|---|---|---|---|---|---|
| PDMX popular, 4/4 (483) | 6.2% | 7.3% | 22% | 25% | 27% | 55% / 38% | 57% / 12% |
| PDMX hymns and sacred, 4/4 (223) | 9.7% | 12.5% | 36% | 28% | 17% | 47% / 37% | 51% / 19% |
| PDMX hymns and sacred, 3/4 (60) | 15.6% | 19.5% | 57% | 33% | 18% | 59% / 52% | 57% / 19% |
| PDMX folk, 4/4 (185) | 9.1% | 11.1% | 31% | 22% | 20% | 52% / 37% | 55% / 16% |
| PDMX folk, 3/4 (42) | 16.9% | 18.3% | 53% | 36% | 22% | 49% / 42% | 55% / 14% |
| PDMX other classical, 4/4 (2,590) | 9.3% | 10.5% | 36% | 28% | 18% | 50% / 41% | 54% / 18% |
| PDMX other classical, 3/4 (553) | 11.0% | 13.3% | 61% | 30% | 8% | 57% / 50% | 53% / 19% |
| OpenEWLD standards before 1930, 4/4 (98) | 9.7% | 12.1% | 43% | 33% | 17% | 49% / 44% | 48% / 17% |
| OpenEWLD standards 1930 on, 4/4 (66) | 7.2% | 9.3% | 42% | 36% | 12% | 59% / 44% | 47% / 20% |""" + md[b:]
open("words.md", "w").write(md); print("ok", md.count("data:image"))
