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
def install(*mods):
    lyricsearch.syllables = syllables; popsearch.syllables = syllables
    for m in mods: m.syllables = syllables
