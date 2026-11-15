"""A reader for the Open Hymnal Project's ABC files (github.com/mzealey/openhymnal, public domain): four voices interleaved line by line
([V: S1V1] soprano, [V: S1V2] alto, [V: S2V1] tenor, [V: S2V2] bass), each soprano line followed by its stanzas' w: lines.
Returns, per hymn: metre, key, the four voices as notes (onset and length in twelfths of a quarter, MIDI pitch) and, for the soprano, each
stanza's syllables aligned to its notes (ABC rules: one syllable a note; '_' holds the last syllable over a note; '*' skips a note; a note
tied from the one before takes no syllable)."""
import re, glob, collections
KEYS = {"C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6, "C#": 7, "F": -1, "Bb": -2, "Eb": -3, "Ab": -4, "Db": -5, "Gb": -6, "Cb": -7}
MINOR = {"Am": "C", "Em": "G", "Bm": "D", "F#m": "A", "C#m": "E", "G#m": "B", "Dm": "F", "Gm": "Bb", "Cm": "Eb", "Fm": "Ab", "Bbm": "Db", "Ebm": "Gb"}
SHARPS, FLATS = "FCGDAEB", "BEADGCF"
BASE = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}
def keysig(k):
    k = k.strip().split()[0] if k.strip() else "C"
    k = MINOR.get(k, k)
    if k.endswith("maj") or k.endswith("Maj"): k = k[:-3]
    if k.endswith("min") or k.endswith("m"): k = MINOR.get(k if k.endswith("m") else k[:-3] + "m", "C")
    n = KEYS.get(k, 0); acc = {}
    for i in range(abs(n)): acc[(SHARPS if n > 0 else FLATS)[i]] = 1 if n > 0 else -1
    return acc
def frac(s, default):
    if s == "": return default
    if s.startswith("/"):
        s2 = s[1:]; return default / (int(s2) if s2 else 2) if not s2.startswith("/") else default / 4
    if "/" in s:
        a, b = s.split("/", 1); return default * int(a) / (int(b) if b else 2)
    return default * int(s)
TOK = re.compile(r"(\[[A-Za-z]:[^\]]*\])|(!.*?!)|(\"[^\"]*\")|(\{[^}]*\})|(\(\d)|(\[[^\]]+\][\d/]*-?)|([_^=]*[A-Ga-gz][,']*[\d/]*-?)|(\|\]|\|\||\|:|:\||\||\]|::)|([()])|(\s+)|(.)")
def parse_voice(s, unit, ks, state):
    """notes from one line of a voice: list of dict(on, dur, p or None for rest, tie_from_prev)"""
    out = []; t = state["t"]; bar_acc = state["acc"]; tied = state["tied"]
    for m in TOK.finditer(s):
        g = m.group(0)
        if m.group(1) or m.group(2) or m.group(3) or m.group(4) or m.group(5) or m.group(10) or m.group(9) or m.group(11): continue
        if m.group(8):
            bar_acc = {}
            if state.get("first_bar") is None and t > 0: state["first_bar"] = t
            continue
        if m.group(6):                                              # a chord: take its top note, length from after the bracket
            inner = re.match(r"\[([^\]]+)\]([\d/]*)(-?)", g); notes = re.findall(r"[_^=]*[A-Ga-g][,']*[\d/]*", inner.group(1))
            g = (notes[-1] if notes else "z") ; g = re.sub(r"[\d/]+$", "", g) + (inner.group(2) or re.search(r"[\d/]*$", notes[-1]).group(0) if notes else "") + inner.group(3)
        mm = re.match(r"([_^=]*)([A-Ga-gz])([,']*)([\d/]*)(-?)", g)
        if not mm: continue
        acc, L, octs, ln, tie = mm.groups()
        d = int(round(frac(ln, unit) ))
        if L == "z": out.append(dict(on=t, dur=d, p=None, tied=False)); t += d; tied = False; continue
        p = BASE[L.upper()] + (12 if L.islower() else 0) + 12 * octs.count("'") - 12 * octs.count(",")
        if acc:
            a = acc.count("^") - acc.count("_"); bar_acc[(L.upper(), p // 12)] = a
        a = bar_acc.get((L.upper(), p // 12), ks.get(L.upper(), 0))
        out.append(dict(on=t, dur=d, p=p + a, tied=tied)); t += d; tied = bool(tie)
    state.update(t=t, acc=bar_acc, tied=tied)
    return out
def lyric_tokens(w):
    w = re.sub(r"^\s*\d+\.\s*~?", "", w.strip())
    toks = []; buf = ""
    i = 0
    for part in re.findall(r"[^\s\-_*|]+-?|_|\*|\||-", w.replace("~", " ")):
        if part == "|": continue
        toks.append(part)
    return toks
def parse(path):
    txt = open(path, errors="ignore").read()
    head = lambda f: (re.search(rf"\n{f}:\s*([^\n%]*)", "\n" + txt) or [None, ""])[1].strip()
    metre = head("M"); unitf = head("L") or "1/8"; a, b = unitf.split("/"); unit = 48 * int(a) / int(b)
    ks = keysig(head("K"))
    voices = collections.defaultdict(list); states = collections.defaultdict(lambda: dict(t=0, acc={}, tied=False)); lyr = collections.defaultdict(list)
    cur = None; last_sop_notes = None; wcount = 0
    body = txt.split("\nK:", 1)[1].split("\n", 1)[1] if "\nK:" in txt else ""
    for line in body.split("\n"):
        line = line.split("%")[0].rstrip() if not line.startswith("w:") else line
        if not line.strip(): continue
        mv = re.match(r"\[V:\s*(\S+?)\]\s*(.*)", line)
        if mv:
            cur, rest = mv.group(1), mv.group(2)
            ns = parse_voice(rest, unit, ks, states[cur]); voices[cur] += ns
            if cur == "S1V1": last_sop_notes = ns; wcount = 0
            continue
        if line.startswith("w:") and cur == "S1V1" and last_sop_notes is not None:
            wcount += 1; k = wcount                                  # the n-th w: line under a soprano line is stanza n
            lyr[k].append((last_sop_notes, lyric_tokens(line[2:])))
    # align each stanza's syllables to the soprano's notes
    stanzas = {}
    for k, chunks in lyr.items():
        al = []
        for notes, toks in chunks:
            sing = [n for n in notes if n["p"] is not None]; ti = 0
            for n in sing:
                if n["tied"]: continue
                if ti >= len(toks): break
                tk = toks[ti]
                if tk == "_": ti += 1; continue
                if tk == "*": ti += 1; continue
                al.append(dict(on=n["on"], dur=n["dur"], p=n["p"], syl=tk.rstrip("-"), joins=tk.endswith("-") or (ti + 1 < len(toks) and toks[ti + 1] == "-")))
                ti += 1
                while ti < len(toks) and toks[ti] == "-": ti += 1
        stanzas[k] = al
    BARLEN = {"4/4": 48, "3/4": 36, "6/4": 72, "3/2": 72, "6/8": 36, "2/4": 24, "2/2": 48, "8/4": 96, "9/8": 54, "C": 48, "C|": 48}
    bl = BARLEN.get(metre); fb = states["S1V1"].get("first_bar")
    shift = (bl - fb) if (bl and fb and fb < bl) else 0                      # a pickup: bar lines fall on multiples of the bar
    for v in voices.values():
        for n in v: n["on"] += shift
    for al in stanzas.values():
        for x in al: x["on"] += shift
    return dict(path=path, metre=metre, unit=unit, barlen=bl, pickup=shift, voices={k: [n for n in v] for k, v in voices.items()}, stanzas=stanzas)
def all_hymns():
    return sorted(glob.glob("/home/claude/atlas/src/openhymnal/Complete/*/*.abc"))
if __name__ == "__main__":
    h = parse([f for f in all_hymns() if "Eventide" in f][0])
    print(h["metre"], {k: len(v) for k, v in h["voices"].items()})
    print([(x["syl"], x["on"], x["p"]) for x in h["stanzas"][1][:14]])
    print(len(h["stanzas"]), [len(v) for v in h["stanzas"].values()])
