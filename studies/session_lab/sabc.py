import re, numpy as np
BASE = dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11); ORDER_S = "FCGDAEB"; MODES = dict(maj=0, ion=0, mix=1, dor=2, min=3, aeo=3, phr=4, loc=5, lyd=-1)
def keysig(mode):
    m = re.match(r"([A-G])([#b]?)\s*([A-Za-z]*)", mode or "C"); t = m.group(1); acc = m.group(2); md = (m.group(3) or "maj").lower()[:3]; fifths = dict(C=0, G=1, D=2, A=3, E=4, B=5, F=-1)[t] + (7 if acc == "#" else -7 if acc == "b" else 0) - MODES.get(md, 0)
    ks = {}
    if fifths > 0:
        for c in ORDER_S[:fifths]: ks[c] = 1
    elif fifths < 0:
        for c in ORDER_S[::-1][:-fifths]: ks[c] = -1
    return ks, (BASE[t] + (1 if acc == "#" else -1 if acc == "b" else 0)) % 12, md
TOK = re.compile(r'"[^"]*"|![^!]*!|\{[^}]*\}|\[[12]|\|+|:\||\|:|::|\[([^\]]*)\]|(\^\^|\^|__|_|=)?([A-Ga-gz])([,\']*)(\d*)(/*)(\d*)|[<>]|\(\d|.', re.S)
def parse(abc, mode):
    """-> (bars: list of lists of (pitch midi or None, duration in eighths)), tonic pc, mode family"""
    ks, tonic, md = keysig(mode); bars = [[]]; local = {}; pend = None
    for m in TOK.finditer(abc.replace("\r", "")):
        s = m.group(0)
        if s[0] == "|" or s in (":|", "|:", "::") or s.startswith("[1") or s.startswith("[2"):
            if "|" in s or ":" in s:
                if bars[-1]: bars.append([])
                local = {}
            continue
        inner = m.group(1)
        if inner is not None:
            mm = re.match(r"(\^\^|\^|__|_|=)?([A-Ga-gz])([,\']*)(\d*)(/*)(\d*)", inner)
            if not mm: continue
            acc, L, octs, n1, sl, n2 = mm.groups()
        elif m.group(3): acc, L, octs, n1, sl, n2 = m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7)
        elif s in "<>":
            pend = s; continue
        else: continue
        d = float(n1) if n1 else 1.0
        if sl: d /= (float(n2) if n2 else 2.0 ** len(sl))
        if L == "z": p = None
        else:
            U = L.upper(); key = (U, L.islower(), octs)
            if acc: local[key] = dict([("^", 1), ("^^", 2), ("_", -1), ("__", -2), ("=", 0)])[acc]
            a = local.get(key, ks.get(U, 0)); p = 60 + BASE[U] + a + (12 if L.islower() else 0) + 12 * octs.count("'") - 12 * octs.count(",")
        if pend and bars[-1]:
            q, dq = bars[-1][-1]; bars[-1][-1] = (q, dq * (1.5 if pend == ">" else 0.5)); d *= (0.5 if pend == ">" else 1.5); pend = None
        bars[-1].append((p, d))
    return [b for b in bars if b], tonic, md
