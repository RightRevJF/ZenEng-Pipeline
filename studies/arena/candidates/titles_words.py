"""titles_words: IDENTITY (title distinctiveness) and lyric vocabulary. Plain arithmetic on text only.
Fixed-path inputs: the full Hot 100 title list (no yardstick), Brysbaert concreteness norms, two public year-end-hit lyric files."""
import re, json, glob, collections
import numpy as np, pandas as pd

_BB = "/home/claude/zeneng/corpus/billboard_songs.csv"
_BRYS = "/home/claude/corpus/lex/concreteness/Concreteness_ratings_Brysbaert_et_al_BRM.txt"
_KS = "/home/claude/zeneng/corpus/big_lyrics.jsonl"
_WK = "/home/claude/corpus/lyrics/walkerkq/billboard_lyrics_1964-2015.csv"
_STOP = set("a an the of to in on for and or but with at by from my your you i me we it is be so that this do don't".split())
_C = {}

def _norm(t):
    t = str(t).lower(); t = re.sub(r"\(.*?\)|\[.*?\]", " ", t); t = t.replace("&", " and ")
    return re.findall(r"[a-z0-9']+", t)
def _key(t): return " ".join(_norm(t)).replace("'", "")
def _ak(s): return re.sub(r"[^a-z]", "", re.split(r" feat| with | and | & |,", str(s).lower())[0])
def _content(toks):
    return [w.replace("'", "") for w in toks if w not in _STOP] or [w.replace("'", "") for w in toks]

def _titles():
    if "wdf" not in _C:
        bb = pd.read_csv(_BB); k = bb.title.map(_key); wdf = collections.Counter()
        for x in k.drop_duplicates(): wdf.update(set(x.split()))
        _C["wdf"] = wdf; _C["nt"] = k.nunique()
    return _C["wdf"], _C["nt"]
def _conc():
    if "conc" not in _C:
        br = pd.read_csv(_BRYS, sep="\t"); _C["conc"] = dict(zip(br.Word.astype(str), br["Conc.M"]))
    return _C["conc"]
def _lyrics():
    if "lyr" not in _C:
        L = {}
        for l in open(_KS):
            d = json.loads(l)
            if d["src"] != "billboard": continue
            L.setdefault((_key(d["title"]), _ak(d["artist"])), " ".join(d["lines"]))
        w = pd.read_csv(_WK, encoding="latin-1")
        for t, a, ly in zip(w.Song, w.Artist, w.Lyrics):
            if isinstance(ly, str) and len(ly.split()) > 40: L.setdefault((_key(t), _ak(a)), ly)
        _C["lyr"] = L
    return _C["lyr"]

def title_word_rarity(df):
    """Mean over the title's content words of -log(share of all distinct Hot 100 titles containing that word). High = rare words."""
    wdf, nt = _titles(); out = []
    for t in df["title"]:
        c = _content(_norm(t))
        out.append(-np.mean([np.log(wdf.get(w, 1) / nt) for w in c]) if c else np.nan)
    return np.array(out, float)

def title_specificity(df):
    """Rank-average of title-word rarity and Brysbaert concreteness of the title's content words (missing concreteness -> middle)."""
    from scipy.stats import rankdata
    r = title_word_rarity(df); cn = _conc(); c = []
    for t in df["title"]:
        v = [cn[w] for w in _content(_norm(t)) if w in cn]; c.append(np.mean(v) if v else np.nan)
    c = np.array(c, float)
    def rk(x):
        o = np.full(len(x), 0.5); ok = np.isfinite(x)
        if ok.sum() > 1: o[ok] = (rankdata(x[ok]) - 0.5) / ok.sum()
        return o
    out = rk(r) + 0.5 * rk(c); out[~np.isfinite(r)] = np.nan
    return out

def lyric_vocab_concreteness(df):
    """Mean Brysbaert concreteness of the DISTINCT content words in the lyric (lyrics joined by title+artist; NaN where no lyric)."""
    L = _lyrics(); cn = _conc(); out = []
    for t, a in zip(df["title"], df["performer"]):
        ly = L.get((_key(t), _ak(a)))
        if ly is None: out.append(np.nan); continue
        w = re.findall(r"[a-z']+", ly.lower())
        if len(w) < 40: out.append(np.nan); continue
        v = [cn[x] for x in set(w) if x in cn and x not in _STOP]
        out.append(np.mean(v) if v else np.nan)
    return np.array(out, float)

CANDIDATES = [
    dict(name="title_word_rarity", kind="hot100", fn=title_word_rarity, sign=+1,
         why="Titles built from words few other Hot 100 titles use (distinctive identity) mark the hits still loved later."),
    dict(name="title_specificity", kind="hot100", fn=title_specificity, sign=+1,
         why="Rare AND concrete title words (a thing, a place, a name) rather than generic love/you/heart abstractions."),
    dict(name="lyric_vocab_concreteness", kind="hot100", fn=lyric_vocab_concreteness, sign=+1,
         why="Lyrics whose vocabulary is concrete (things you can see and touch) outlast lyrics made of abstractions."),
]
