"""944 (Window 196): a song's shape from its own words. What a lyric's words and form say about its tune, by the link found in the kept 4/4 songs as a body
(studies/words_to_shape: bars on a figure already sung, bars on a rhythm already sung and range are predicted from the words on songs held out; how a tune moves is not).
The table tables/kept_words_to_shape.json is made by make_kept_words_to_shape.py. No one kept song is a model for any Luthier song."""
import os, re, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); TABLE = os.path.join(HERE, "..", "..", "tables", "kept_words_to_shape.json")
PRED = ["syllables in the song (log)", "syllables a line", "unevenness of the lines", "syllables a word", "different words over all words", "lines said again word for word", "words in a three-word run already sung", "kinds of section", "share of syllables in a chorus", "has a bridge", "minor", "year"]
def features(lines, kinds, chorus_share, bridge, minor, year):
    """lines: [(words of the line, syllables in the line)] in the order sung"""
    w = [re.sub(r"[^a-z']", "", a.lower()) for ws, _ in lines for a in ws]; w = [a for a in w if a]; L = [float(n) for _, n in lines]; tot = sum(L); mean = tot / len(L); sd = math.sqrt(sum((x - mean) ** 2 for x in L) / len(L))
    seen = set(); rep = 0
    for ws, _ in lines:
        x = " ".join(ws)
        if x and x in seen: rep += 1
        seen.add(x)
    tri = [tuple(w[i:i + 3]) for i in range(len(w) - 2)]; st = set(); t3 = 0
    for x in tri:
        if x in st: t3 += 1
        st.add(x)
    return [math.log(max(tot, 1)), mean, sd / mean, tot / max(len(w), 1), len(set(w)) / max(len(w), 1), rep / max(len(lines), 1), t3 / max(len(tri), 1), float(kinds), float(chorus_share), float(bridge), float(minor), float(year)]
def kept_lines(k):
    """946 (749.128): a kept song's words tied to its notes, so its lines are read as a Luthier lyric's are. k: a song from kept_corpus.kept_songs().
    Each word takes as many notes as it has syllables sung; a melisma's further notes carry no word (kept_corpus writes them as a word of no letters);
    a line's words are the words that begin in it; a line's syllables are its notes that carry a syllable. -> [(words, syllables)] in the order sung"""
    out = {}; i = 0
    for w, n in k["words"]:
        ln = k["lines"][i]; o = out.setdefault(ln, [[], 0]); x = re.sub(r"[^a-z']", "", w.lower())
        if x: o[0].append(x); o[1] += n
        i += n
    return [(ws, n) for ln, (ws, n) in sorted(out.items()) if n]
def from_sung(sung, minor=False, year=None):
    """sung: the spec's sections as sung, [name, kind, [[(word, stressed) for each syllable] for each line]]"""
    T = json.load(open(TABLE)); lines = []; kinds = set(); cho = 0; tot = 0; br = False
    for name, kind, ls in sung:
        kinds.add(kind.lower()); br = br or kind.lower() == "bridge"
        for ln in ls:
            ws = []
            for txt, _ in ln:
                if not ws or ws[-1] != txt: ws.append(txt)                                     # a word is written once for each of its syllables
            lines.append((ws, len(ln))); tot += len(ln); cho += len(ln) * (kind.lower() == "chorus")
    x = features(lines, len(kinds), cho / max(tot, 1), br, minor, T["year_held_at"] if year is None else year); out = {}
    for c, m in T["readings"].items():
        v = m["intercept"] + sum(m["coef"][i] * (x[i] - T["mean"][i]) / T["sd"][i] for i in range(len(x))); out[c] = max(m["kept_10th"], min(m["kept_90th"], v))      # held inside the kept 10th to 90th
    return out, dict(zip(PRED, [round(v, 4) for v in x]))
