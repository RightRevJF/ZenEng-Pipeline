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
_syllables_v48 = syllables
def syllables(line):
    return _song26(_syllables_v48(line))
def install(*mods):
    lyricsearch.syllables = syllables; popsearch.syllables = syllables
    for m in mods: m.syllables = syllables
