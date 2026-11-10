"""Engraving helpers for 'The First Wood': 3/4, a twelfths-of-a-beat grid (a bar is 36), F major (flats)."""
import collections, re
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {3: "16", 6: "8", 9: "8.", 12: "4", 18: "4.", 24: "2", 36: "2."}
def split(pos, n):
    out = []
    while n > 0:
        if pos == 0 and n >= 36: L = 36
        elif pos in (0, 12) and n >= 24: L = 24
        elif pos in (0, 12) and n >= 18 and n < 24 and (pos + 18) % 12 in (0, 6): L = 18
        elif pos % 12 == 0 and n >= 12: L = 12
        elif pos % 6 == 0 and n >= 6: L = 6 if not (n >= 9 and pos % 12 == 0) else 9
        else: L = 3
        L = min(L, 36 - pos)
        while L not in DUR: L -= 3
        out.append((pos, L)); pos += L; n -= L
    return out

def stream(items, start, end, tokfn, mm=True):
    """items: dicts with on (absolute twelfths), dur. Bars measured from 'start' (a bar line); returns tokens per bar."""
    items = sorted(items, key=lambda x: x["on"]); cur = start; seq = []
    for it in items:
        assert it["on"] >= cur, ("overlap", it["on"], cur)
        if it["on"] > cur: seq.append((None, cur, it["on"] - cur))
        seq.append((it, it["on"], it["dur"])); cur = it["on"] + it["dur"]
    if cur < end: seq.append((None, cur, end - cur))
    nb = (end - start + 35) // 36
    bybar = [[] for _ in range(nb)]
    for it, s, d in seq:
        first = True
        while d > 0:
            rel = s - start; bi = rel // 36; m = min(d, 36 - rel % 36)
            sp = split(rel % 36, m)
            for k, (pos, L) in enumerate(sp):
                if it is None: tok = ("R2." if (L == 36 and mm) else "r" + DUR[L])
                else: tok = tokfn(it, L, not (k == len(sp) - 1 and m == d), first)
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar
def esc(t): return t.replace('"', '\\"')
CHNAME = {"I": ("f", ""), "ii": ("g", ":m"), "iii": ("a", ":m"), "IV": ("bes", ""), "V": ("c", ""), "V7": ("c", ":7"), "vi": ("d", ":m"), "vii": ("e", ":dim"), "I64": ("f", "")}
CHTEXT = {"I": "F", "ii": "Gm", "iii": "Am", "IV": "B♭", "V": "C", "V7": "C7", "vi": "Dm", "vii": "E°", "I64": "F"}
def chord_tok(ch, bass, L):
    r, q = CHNAME[ch]; t = f"{r}{DUR[L]}{q}"
    root = {"I": 5, "ii": 7, "iii": 9, "IV": 10, "V": 0, "V7": 0, "vi": 2, "vii": 4, "I64": 5}[ch]
    if bass % 12 != root: t += "/" + SP[bass % 12]
    return t
def chord_text(ch, bass):
    root = {"I": 5, "ii": 7, "iii": 9, "IV": 10, "V": 0, "V7": 0, "vi": 2, "vii": 4, "I64": 5}[ch]
    N = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 10: "B♭"}
    return CHTEXT[ch] + ("" if bass % 12 == root else "/" + N[bass % 12])
