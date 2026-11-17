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

- `words_results.json` and `words_more_results.json`: every figure in this report. `sung_syllables.json` is not committed; the parser rebuilds it.""" + md[b:]
if "Data: [CoCoPops]" not in md: md = md.replace("Data: CoCoPops, CC BY", "Data: [CoCoPops](https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops), CC BY", 1)
md = re.sub(r"(?m)^### (\*\*)?(Sources read:|Checks for the port:|Measured:)(\*\*)?$", r"\2", md)
open("words.md", "w").write(md); print("ok", md.count("data:image"))
