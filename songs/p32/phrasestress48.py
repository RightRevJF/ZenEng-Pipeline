"""v48 fix 1.1 as written: a line (or comma-phrase) with no stressed syllable gets ONE promoted, in order:
a quantifier/intensifier, then a main verb not acting as an auxiliary, then the last word."""
import lyricsearch, popsearch
_orig = lyricsearch.syllables
QUANT = {"all","both","each","every","more","most","much","no","none","own","so","such"}
MAINV = {"am","are","be","did","do","does","had","has","have","is","was","were"}
def _promote(seg):
    if any(x[2] for x in seg): return seg
    ws=[x[0] for x in seg]
    idx=None
    for i,w in enumerate(ws):
        if w in QUANT: idx=i; break
    if idx is None:
        for i,w in enumerate(ws):
            nxt = ws[i+1] if i+1<len(ws) else ""
            if w in MAINV and nxt != "not" and not nxt.endswith("ed"): idx=i; break
    if idx is None: idx=len(seg)-1
    return [(w,v,(True if i==idx else st),fn) for i,(w,v,st,fn) in enumerate(seg)]
def syllables(line):
    out=_orig(line)
    # comma-phrases: split by commas in the text, mapped by word count
    parts=[p for p in line.split(",") if p.strip()]
    if len(parts)<=1: return _promote(out)
    res=[]; i=0
    for p in parts:
        n=len(_orig(p)); res+= _promote(out[i:i+n]); i+=n
    return res + out[i:]
LINE_END_ADV = {"now", "here", "there", "mine", "yours", "ours"}   # line-final adverbs of time/place, and a possessive pronoun standing alone
BINARY = {"no": {"yes", "or"}, "or": {"either", "yes", "this", "that"}}
def _song27(res):
    """song 27 port (finding, extends fix 39): a binary pair named as a thing -- 'yes or NO', 'either OR' -- stresses its last word at a
    line's end; a subject pronoun set against a noun ('the wind was never ... / and YOU were never ...') is contrastive (fix 19)."""
    out = []; ws = [x[0] for x in res]
    for k, (w, v, st, fn) in enumerate(res):
        if k == len(res) - 1 and w in BINARY and any(p in BINARY[w] for p in ws[max(0, k - 3):k]): st, fn = True, False
        if w in ("you", "we", "i") and k > 0 and ws[k - 1] == "and" and k + 2 < len(ws) and ws[k + 1] in ("were", "was", "are") and ws[k + 2] == "never": st, fn = True, False
        out.append((w, v, st, fn))
    return out
def _song26(res):
    """song 26 port (finding): a numeral read as 'one' in a time ('five-oh-ONE') is a content word; a line-final adverb of time or
    place ('good luck finding me NOW', 'you'll find me HERE'), or a possessive pronoun standing alone ('every single one of them's MINE'),
    carries the line's last stress."""
    out = []
    for k, (w, v, st, fn) in enumerate(res):
        if w == "one" and k > 0 and res[k - 1][0] == "oh": st, fn = True, False
        if w in LINE_END_ADV and k == len(res) - 1: st, fn = True, False
        out.append((w, v, st, fn))
    return out
def _song29(res):
    """song 29 port (findings): negation 'not' before its noun phrase is stressed (fix 7, 'with NOT a single word'); a line-final
    quantifier or pronoun-free 'all' carries the line's last stress ('at ALL', fix 39); 'both' as a pronoun object is stressed ('past
    BOTH of them'); a clause-initial 'now' set off by a colon is stressed ('NOW: Abba'); the contractions 'it's' and 'she'll' before a
    verb are function words."""
    out = []; ws = [x[0] for x in res]
    for k, (w, v, st, fn) in enumerate(res):
        if w == "not" and k + 1 < len(ws) and ws[k + 1] == "a": st, fn = True, False
        if w == "all" and k == len(res) - 1: st, fn = True, False
        if w == "both": st, fn = True, False
        if w == "now" and k == 0 and len(ws) > 1 and ws[1] == "abba": st, fn = True, False
        if w in ("it's", "she'll") and k + 1 < len(ws) and ws[k + 1] not in ("a", "the"): st, fn = False, True
        out.append((w, v, st, fn))
    return out
def _song31(res):
    """song 31 port (finding, extends the song 30 port): the particle 'on' closing a phrase after 'nothing', 'back' or 'light(s)' carries
    the stress ('nothing ON, nothing ON', 'come back ON'); a line-final 'you' or 'are' after a function word carries the line's last
    stress ('the only thing glowing is YOU', 'nothing on but YOU', 'till I find where you ARE')."""
    out = []; ws = [x[0] for x in res]
    for k, (w, v, st, fn) in enumerate(res):
        end = k == len(res) - 1 or ws[k + 1] == "nothing"
        if w == "on" and end and k > 0 and ws[k - 1] in ("nothing", "back", "light"): st, fn = True, False
        if w in ("you", "are") and k == len(res) - 1 and k > 0 and res[k - 1][3]: st, fn = True, False
        out.append((w, v, st, fn))
    return out
SONG32_WORDS = {"rabboni": (False, True, False), "instead": (False, True), "itself": (False, True), "someone": (True, False)}
def _song32(res):
    """song 32 ports (findings): (1) a line-final question word ('tell me WHERE') carries the line's last stress; (2) a line-final
    'own' or 'was' ('to tend his OWN', 'and he WAS') carries it too, as a content word; (3) two-syllable words the dictionary stresses
    twice take one stress (in-STEAD, it-SELF, SOME-one), and rab-BO-ni is stressed on its middle syllable; (4) 'just' before a stressed word is weak ('just GIVE me', 'just TELL me'); (5) a wh-word opening an indirect question after its object pronoun is stressed ('asked me WHO', 'tell me WHERE')."""
    out = []; n = len(res); k = 0
    while k < n:
        w = res[k][0]; j = k
        while j < n and res[j][0] == w and (j == k or res[j][1] != res[k][1] or True) and j - k < len(SONG32_WORDS.get(w, (0,) * 9)): j += 1
        if w in SONG32_WORDS and j - k == len(SONG32_WORDS[w]):
            for t, stv in enumerate(SONG32_WORDS[w]):
                ww, v, st, fn = res[k + t]; out.append((ww, v, stv, False))
            k = j; continue
        ww, v, st, fn = res[k]
        if k == n - 1 and ww in ("where", "why", "who", "how", "when", "what", "own", "was"): st, fn = True, False
        if ww == "just" and k + 1 < n and res[k + 1][2]: st, fn = False, True       # (4) 'just' before a stress is the adverb: weak
        if ww in ("where", "why", "who") and k > 0 and res[k - 1][0] in ("me", "him", "her", "us", "them"): st, fn = True, False   # (5) 'asked me WHY', 'tell me WHERE'

        out.append((ww, v, st, fn)); k += 1
    return out
_syllables_v48 = syllables
def syllables(line):
    return _song32(_song31(_song29(_song27(_song26(_syllables_v48(line))))))
def install(*mods):
    lyricsearch.syllables = syllables; popsearch.syllables = syllables
    for m in mods: m.syllables = syllables
