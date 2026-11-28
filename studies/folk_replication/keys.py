"""Title keys for the folk replication's match (PREDICTION.md, "The match"). The same functions on both sides."""
import re, unicodedata
TYPE_WORDS = ["double jig", "single jig", "slip jig", "hop jig", "quick step", "set dance", "highland fling", "long dance",
              "reel", "jig", "hornpipe", "strathspey", "march", "quickstep", "air", "polka", "waltz", "clog", "schottische",
              "slide", "fling", "lament", "song"]
TRAD = re.compile(r"\b(trad|traditional|anon|public domain|unknown)", re.I)

def fold(s):
    s = (s or "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue").replace("ß", "ss")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def key(s):
    return re.sub(r"[^a-z0-9]", "", fold(s).lower().replace("&", "and"))

def clean(title):
    t = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", title or "")
    t = t.split(" -- ")[0]
    t = t.strip().rstrip(".").strip()
    return t

def words(s):
    return re.findall(r"[a-z0-9']+", fold(s).lower().replace("&", "and"))

def strip_type(ws):
    """take trailing tune-type words off a word list"""
    changed = True
    while changed and ws:
        changed = False
        for tw in TYPE_WORDS:
            t = tw.split()
            if len(ws) > len(t) and ws[-len(t):] == t: ws = ws[:-len(t)]; changed = True; break
    return ws

def exact_key(title):
    return key(clean(title))

def loose_key(title):
    ws = strip_type(words(clean(title)))
    if ws and ws[0] in ("the", "a", "an") and len(ws) > 1: ws = ws[1:]
    return key(" ".join(ws))

def usable(title):
    """two words or more once trailing tune-type words are off (articles count)"""
    return len(strip_type(words(clean(title)))) >= 2
