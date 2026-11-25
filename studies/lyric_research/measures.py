"""Computable lyric measures for the lyric research (task 66).

Every measure works on words only: the text is lowercased, apostrophes are
dropped ("don't" -> "dont") and all other punctuation and line breaks are
removed, because the outcome corpus (Billboard year-end lyrics, 1965-2015) is
stored that way. Our own lyrics are scored through the same door, so the two
are comparable.

Nothing here stores lyric text. `features(text)` returns numbers only.
The stock-phrase measure needs a reference table of 4-gram -> number of
distinct artists; it is built from hashed 4-grams (no text kept) by
`build_stock_table` and lives outside the repo.

Sources for each measure are in reading.md (sections B, E, F, G).
"""
import re, math, zlib, hashlib, functools, collections

NORMS = "/home/claude/data/norms/concreteness.txt"   # Brysbaert et al. 2014

VOCABLES = set("""oh ooh ohh ooo ah ahh aah yeah yea ya yeh hey la na da doo dum
uh huh mm mmm hmm whoa woah wo ow ay ayy oo eh ha uhh woo yo""".split())

# Named emotions (fixed before any reading of the corpus; Kao & Jurafsky
# 2015: professional poems name fewer emotions).
EMOTION = set("""love loved loves loving lovin hate hated hates sad sadness happy
happiness joy joyful lonely loneliness alone fear afraid scared angry anger mad
cry crying cried tears pain hurt hurts hurting heartbreak heartache broken
sorrow sorry blue misery miserable glad excited jealous jealousy shame ashamed
proud pride hope hopeless despair desire passion feel feeling feelings felt
emotion emotions grief lust""".split())

# Stock "poetic" words that mark machine-written verse (Walsh et al. 2024)
# and greeting-card lyric. Kept separate from EMOTION.
POETIC_STOCK = set("""heart hearts soul souls embrace echo echoes whisper whispers
whispered dream dreams forever eternity eternal destiny tapestry symphony
journey shine shining glow glowing ignite spark sparks fire flame""".split())

ARCHAIC = set("""thee thou thy thine hath doth ere oft nigh yonder tis twas
whence wherefore art shalt wilt""".split())

YOU = set("you your yours yourself yourselves youre youll youve youd ya".split())
I_ = set("i me my mine myself im ive ill id".split())
WE = set("we us our ours ourselves were well weve wed".split())
# 'were', 'well', 'wed' are ambiguous once apostrophes are gone; they are
# counted only when spaCy tags them PRON (see features()).


def words(text):
    t = text.lower().replace("'", "").replace("’", "")
    return re.findall(r"[a-z]+", t)


@functools.lru_cache(None)
def _norms():
    d = {}
    with open(NORMS, encoding="utf-8") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            if p[1] == "0":
                d[p[0].lower()] = float(p[2])
    return d


@functools.lru_cache(None)
def _nlp():
    import spacy
    return spacy.load("en_core_web_md")


@functools.lru_cache(None)
def _cmu():
    import pronouncing
    pronouncing.init_cmu()
    return pronouncing


def _phones(w):
    p = _cmu().phones_for_word(w)
    return p[0].split() if p else None


def _onset(ph):
    return ph[0] if ph and not ph[0][-1].isdigit() else None


def _stressed_vowel(ph):
    if not ph:
        return None
    for x in ph:
        if x[-1] == "1":
            return x[:-1]
    for x in ph:
        if x[-1].isdigit():
            return x[:-1]
    return None


def _h(gram):
    return hashlib.blake2b(" ".join(gram).encode(), digest_size=8).hexdigest()


def grams(ws, n=4):
    ws = [w for w in ws if w not in VOCABLES]
    return [tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)]


def build_stock_table(songs):
    """songs: iterable of (artist_key, text). Returns {hash: {artists}} sizes
    as a dict hash -> Counter of artists (needed for leave-artist-out)."""
    tab = collections.defaultdict(set)
    for art, text in songs:
        for g in set(grams(words(text))):
            tab[_h(g)].add(art)
    return {k: frozenset(v) for k, v in tab.items() if len(v) >= 2}


def stock_rate(text, table, artist=None, k=5):
    """Share of a song's distinct 4-grams used by >= k OTHER artists."""
    gs = set(grams(words(text)))
    if not gs:
        return float("nan")
    hit = 0
    for g in gs:
        s = table.get(_h(g))
        if s:
            n = len(s) - (1 if artist in s else 0)
            hit += n >= k
    return hit / len(gs)


def mattr(ws, w=50):
    if len(ws) < w:
        return len(set(ws)) / max(1, len(ws))
    c = collections.Counter(ws[:w]); tot = len(c)
    for i in range(w, len(ws)):
        c[ws[i]] += 1
        c[ws[i - w]] -= 1
        if c[ws[i - w]] == 0:
            del c[ws[i - w]]
        tot += len(c)
    return tot / (len(ws) - w + 1) / w


def features(text, stock_table=None, artist=None):
    from wordfreq import zipf_frequency
    ws = words(text)
    n = len(ws)
    out = {"n_words": n}
    if n < 30:
        return out
    per100 = 100.0 / n
    doc = _nlp()(" ".join(ws))
    norms = _norms()
    content = [t for t in doc if t.pos_ in ("NOUN", "VERB", "ADJ", "ADV")
               and t.text not in VOCABLES]
    nouns = [t for t in doc if t.pos_ == "NOUN" and t.text not in VOCABLES]
    nc = [norms[t.lemma_] for t in nouns if t.lemma_ in norms]
    out["conc_noun"] = sum(nc) / len(nc) if nc else float("nan")
    out["image_noun_rate"] = sum(1 for t in nouns if norms.get(t.lemma_, 0) >= 4.0) * per100
    out["emo_rate"] = sum(1 for w in ws if w in EMOTION) * per100
    out["poetic_stock_rate"] = sum(1 for w in ws if w in POETIC_STOCK) * per100
    out["archaic_rate"] = sum(1 for w in ws if w in ARCHAIC) * per100
    nv = sum(1 for t in content if t.pos_ == "VERB")
    out["verb_share"] = nv / len(content) if content else float("nan")
    out["adj_share"] = (sum(1 for t in content if t.pos_ == "ADJ") / len(content)) if content else float("nan")
    amb = {"were", "well", "wed"}
    out["you_rate"] = sum(1 for w in ws if w in YOU) * per100
    out["i_rate"] = sum(1 for w in ws if w in I_) * per100
    out["we_rate"] = sum(1 for t in doc if t.text in WE and (t.text not in amb or t.pos_ == "PRON")) * per100
    g = grams(ws)
    out["repetition"] = 1 - len(set(g)) / len(g) if g else float("nan")
    out["mattr"] = mattr([w for w in ws if w not in VOCABLES])
    out["compress"] = len(zlib.compress(" ".join(ws).encode(), 9)) / len(" ".join(ws))
    cw = [t.text for t in content]
    zs = [zipf_frequency(w, "en") for w in cw]
    out["zipf_content"] = sum(zs) / len(zs) if zs else float("nan")
    # sound devices: pairs of content words within 3 tokens of each other
    idx = [(t.i, t.text) for t in content]
    al = asn = 0
    for a in range(len(idx)):
        pa = _phones(idx[a][1])
        for b in range(a + 1, len(idx)):
            if idx[b][0] - idx[a][0] > 3:
                break
            if idx[b][1] == idx[a][1]:
                continue
            pb = _phones(idx[b][1])
            if pa and pb:
                oa, ob = _onset(pa), _onset(pb)
                if oa and oa == ob:
                    al += 1
                va, vb = _stressed_vowel(pa), _stressed_vowel(pb)
                if va and va == vb:
                    asn += 1
    out["allit_rate"] = al * per100
    out["asson_rate"] = asn * per100
    # semantic distance between neighbouring distinct content words
    vec = [t for t in content if t.has_vector and t.vector_norm > 0]
    ds = []
    for a in range(len(vec) - 1):
        if vec[a].lemma_ != vec[a + 1].lemma_:
            ds.append(1 - vec[a].similarity(vec[a + 1]))
    out["sem_dist"] = sum(ds) / len(ds) if ds else float("nan")
    if stock_table is not None:
        out["stock_rate"] = stock_rate(text, stock_table, artist)
    return out


MEASURES = ["conc_noun", "image_noun_rate", "emo_rate", "poetic_stock_rate",
            "archaic_rate", "verb_share", "adj_share", "you_rate", "i_rate",
            "we_rate", "repetition", "mattr", "compress", "zipf_content",
            "allit_rate", "asson_rate", "sem_dist", "stock_rate"]
