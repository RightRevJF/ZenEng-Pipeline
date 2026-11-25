"""Copied unchanged from the maintainer's studies/lyric_lines/linefeat.py (luthier-v8-stage1 at add5ae8), so both tests read lines the same way.
Line-level measures of a lyric (PREDICTION.md). features(stanzas) takes a list of stanzas, each a list of lines; returns numbers only."""
import re, sys, os, functools, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lyric_research"))
from measures import EMOTION, YOU, I_, VOCABLES, words
import pronouncing

@functools.lru_cache(None)
def phones(w):
    p = pronouncing.phones_for_word(w)
    if not p and w.endswith("in"): p = pronouncing.phones_for_word(w + "g")
    return tuple(p[0].split()) if p else None

def tail(ph):
    """(last stressed vowel, sounds after it)"""
    idx = [i for i, x in enumerate(ph) if x[-1] in "12"] or [i for i, x in enumerate(ph) if x[-1].isdigit()]
    if not idx: return None
    i = idx[-1]; return ph[i][:-1], tuple(re.sub(r"\d", "", x) for x in ph[i + 1:])

def rhyme(a, b):
    """0 none, 1 slant, 2 perfect; None if a word is unknown. The same word is no rhyme."""
    if a == b: return 0
    pa, pb = phones(a), phones(b)
    if pa is None or pb is None: return None
    ta, tb = tail(pa), tail(pb)
    if ta is None or tb is None: return None
    if ta == tb: return 2
    if ta[0] == tb[0] or (ta[1] and ta[1] == tb[1]): return 1
    return 0

def endword(line):
    ws = [w for w in words(line) if w not in VOCABLES]; return ws[-1] if ws else None

def rhymed(ends, i, span=4):
    """best rhyme of line i's end with an end within span lines either side (None if its word is unknown)"""
    if ends[i] is None or phones(ends[i]) is None: return None
    best = 0
    for j in range(max(0, i - span), min(len(ends), i + span + 1)):
        if j != i and ends[j]:
            r = rhyme(ends[i], ends[j]); best = max(best, r or 0)
    return best

def syl(line):
    n = 0
    for w in words(line):
        p = phones(w); n += sum(x[-1].isdigit() for x in p) if p else max(1, len(re.findall(r"[aeiouy]+", w)))
    return n

def features(stanzas):
    stanzas = [[l for l in s if words(l)] for s in stanzas]; stanzas = [s for s in stanzas if s]; lines = [l for s in stanzas for l in s]
    ws = [w for l in lines for w in words(l) if w not in VOCABLES]; n = len(ws)
    if n < 50 or len(lines) < 8: return None
    key = [" ".join(words(l)) for l in lines]; seen = set(); first = []
    for k in key: first.append(k not in seen); seen.add(k)
    ends = [endword(l) for l in lines]; rr = [rhymed(ends, i) for i in range(len(lines))]
    cand = [r for r, f in zip(rr, first) if f and r is not None]; hit = [r for r in cand if r > 0]
    rate = lambda s, W: sum(w in s for w in W) / max(1, len(W))
    lw = [[w for w in words(l) if w not in VOCABLES] for l in lines]; FY = EMOTION | YOU
    last, rest = [], []; i = 0
    for s in stanzas:
        for k in range(len(s)): (last if k == len(s) - 1 else rest).extend(lw[i]); i += 1
    half = len(lines) // 2; A = [w for x in lw[:half] for w in x]; B = [w for x in lw[half:] for w in x]; sy = np.array([syl(l) for l in lines], float)
    return dict(n_words=n, n_lines=len(lines), stanzas=len(stanzas),
                rhyme_rate=len(hit) / len(cand) if len(cand) >= 6 else None, perfect_share=sum(r == 2 for r in hit) / len(hit) if len(hit) >= 4 else None,
                iyou_rate=100 * (rate(I_, ws) + rate(YOU, ws)), i_rate=100 * rate(I_, ws), you_lines=float(np.mean([any(w in YOU for w in x) for x in lw])),
                end_weight=(rate(FY, last) - rate(FY, rest)) if len(stanzas) >= 2 and last and rest else None, feel_late=rate(EMOTION, B) - rate(EMOTION, A),
                emo_rate=100 * rate(EMOTION, ws), line_cv=float(sy.std() / sy.mean()), syl_line=float(sy.mean()), repeat_share=1 - sum(first) / len(lines))
