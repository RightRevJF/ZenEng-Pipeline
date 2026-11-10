"""Engraving helpers for 'Swallowed Up': sixteenth grid, 4/4, a tempo change at the slowdown. Spelled from B minor (sharps), with
the b2 (C) and the b5 (F) as naturals; A# over F#."""
import collections, sys, re
sys.path[:0] = ["/home/claude/p34", "/home/claude/carol"]
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"}
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "16", 2: "8", 3: "8.", 4: "4", 6: "4.", 8: "2", 12: "2.", 16: "1"}
def split(pos, n):
    """a bar of sixteen: nothing crosses a beat unless it starts on one and is a half, a dotted half or a whole from a strong beat."""
    out = []
    while n > 0:
        if pos == 0 and n >= 16: L = 16
        elif pos == 0 and n >= 12: L = 12
        elif pos in (0, 8) and n >= 8: L = 8
        elif pos % 8 == 0 and n >= 6: L = 6
        elif pos % 4 == 0 and n >= 4: L = 4
        else:
            room = min(n, 4 - pos % 4)
            if pos % 4 == 0 and room >= 3 and n >= 3: L = 3
            elif pos % 2 == 0 and room >= 2: L = 2
            else: L = 1
        out.append((pos, L)); pos += L; n -= L
    return out

def stream(items, nbars, tokfn, rest="r", mmrest=True, extra=None):
    """items: dicts with abs16 (bar*16+slot), dur (sixteenths) and whatever tokfn needs. Returns tokens per bar (list of lists).
    tokfn(item, L, tie, first) -> token string."""
    items = sorted(items, key=lambda x: x["abs16"]); cur = 0; seq = []; TOT = nbars * 16
    for it in items:
        assert it["abs16"] >= cur, ("overlap", it["abs16"], cur)
        if it["abs16"] > cur: seq.append((None, cur, it["abs16"] - cur))
        seq.append((it, it["abs16"], it["dur"])); cur = it["abs16"] + it["dur"]
    if cur < TOT: seq.append((None, cur, TOT - cur))
    bybar = [[] for _ in range(nbars)]
    for it, s, d in seq:
        first = True
        while d > 0:
            bi = s // 16; m = min(d, 16 - s % 16)
            sp = split(s % 16, m)
            for k, (pos, L) in enumerate(sp):
                if it is None: tok = ("R1" if (L == 16 and mmrest) else rest + DUR[L])
                else:
                    tie = not (k == len(sp) - 1 and m == d)
                    tok = tokfn(it, L, tie, first)
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar

def esc(t): return t.replace('"', '\\"')
