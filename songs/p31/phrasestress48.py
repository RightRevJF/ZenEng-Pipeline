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
_syllables_v48 = syllables
def syllables(line):
    return _song31(_song27(_song26(_syllables_v48(line))))
def install(*mods):
    lyricsearch.syllables = syllables; popsearch.syllables = syllables
    for m in mods: m.syllables = syllables
