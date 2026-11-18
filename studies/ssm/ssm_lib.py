"""A song as a picture of itself: the self-similarity matrix of its bars (melody and chords), from CoCoPops Humdrum files or a Luthier record.
Each bar becomes a set of melody events (place in the bar to a sixteenth, pitch class above the tonic) and a set of chords (Roman numerals).
Two bars' likeness: 0.7 x the Jaccard overlap of their melody events + 0.3 x that of their chords (chords alone where neither bar is sung)."""
import re, os, json
import numpy as np
LET = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
def kern_pitch(tok):
    m = re.search(r"([a-gA-G])\1*", tok)
    if not m or "r" in tok.replace("#", ""): return None
    s = m.group(0); base = LET[s[0].lower()]; octv = 4 + (len(s) - 1) if s[0].islower() else 3 - (len(s) - 1)
    acc = tok.count("#") - tok.count("-"); return 12 * (octv + 1) + base + acc
def kern_dur(tok):
    m = re.match(r"\[?(\d+)(\.*)", tok)
    if not m: return None
    d = 4.0 / int(m.group(1)) if int(m.group(1)) else 8.0; dots = len(m.group(2)); return d * (2 - 0.5 ** dots)   # quarter notes
def tonic_pc(tok):
    m = re.match(r"\*([A-Ga-g])([#-]?):", tok)
    if not m: return None
    return (LET[m.group(1).lower()] + (1 if m.group(2) == "#" else -1 if m.group(2) == "-" else 0)) % 12
def read_hum(path):
    L = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8", errors="ignore") if l.strip() and not l.startswith("!!")]
    head = next(r for r in L if r[0].startswith("**")); kern = head.index("**kern"); harm = head.index("**harm") if "**harm" in head else None
    meta = {m.group(1): m.group(2) for m in (re.match(r"!!!([^:]+):\s*(.*)", l) for l in open(path, encoding="utf-8", errors="ignore")) if m}
    t = 0.0; tb = None; bars = []; cur = None; tonic = None; started = False
    for r in L[L.index(head) + 1:]:
        if len(r) <= kern: continue
        a = r[kern]
        if a.startswith("*"):
            for x in r:
                m = re.match(r"\*tb(\d+)", x)
                if m: tb = int(m.group(1))
                tp = tonic_pc(x)
                if tp is not None and tonic is None: tonic = tp
            continue
        if a.startswith("!"): continue
        if a.startswith("="):
            cur = dict(t0=t, mel=[], ch=set()); bars.append(cur); started = True; continue
        if not started: cur = dict(t0=t, mel=[], ch=set()); bars.append(cur); started = True
        if harm is not None and r[harm] not in (".", "") and not r[harm].startswith(("*", "!", "=")):
            c = re.sub(r"^\d+\.*", "", r[harm]).strip()
            if c and c not in ("r", "N"): cur["ch"].add(c)
        if tb:                                                                                # timebase grid: every row the same length, tokens carry no duration
            if a not in (".", "") and "r" not in a and kern_pitch(a) is not None and not a.startswith("]") and "_" not in a: cur["mel"].append((t, kern_pitch(a)))
            t += 4.0 / tb
        else:
            if a in (".", ""): continue
            d = kern_dur(a); p = kern_pitch(a)
            if p is not None and "]" not in a and "_" not in a: cur["mel"].append((t, p))
            if d: t += d
    for i, b in enumerate(bars): b["len"] = (bars[i + 1]["t0"] if i + 1 < len(bars) else t) - b["t0"]
    bars = [b for b in bars if b["len"] > 0.01]
    return dict(title=meta.get("OTL", os.path.basename(path)), artist=meta.get("COC", ""), peak=meta.get("BillboardPeak"), rs_rank=meta.get("Rolling Stone List Rank"), tonic=tonic or 0, bars=bars)
def read_record(path):
    R = json.load(open(path)); B = R["bar"]; ton = R["key"]["tonic_midi"] % 12; s0 = {}; t = 0
    for n, k, nb in R["form"]: s0[n] = t; t += nb
    bars = [dict(t0=i * B, len=B, mel=[], ch=set()) for i in range(t)]
    for n in R["melody"]["notes"]:
        i = n["on"] // B
        if 0 <= i < t and n.get("text"): bars[i]["mel"].append((n["on"] / 12.0, n["midi"]))
    for n, rn in R.get("roman", {}).items():
        if n in s0:
            for j, b in enumerate(rn):
                if s0[n] + j < t: bars[s0[n] + j]["ch"] |= set(b.split() if isinstance(b, str) else b)
    for b in bars: b["t0"] /= 12.0; b["len"] /= 12.0
    return dict(title=R["title"], artist="Luthier", peak=None, rs_rank=None, tonic=ton, bars=bars)
def bar_sets(song):
    out = []
    for b in song["bars"]:
        mel = {(int(round((t - b["t0"]) / b["len"] * 16)) % 16, (p - song["tonic"]) % 12) for t, p in b["mel"]}; out.append((mel, b["ch"]))
    return out
def ssm(song):
    S = bar_sets(song); n = len(S); M = np.zeros((n, n))
    J = lambda a, b: len(a & b) / len(a | b) if (a or b) else 1.0
    for i in range(n):
        for j in range(n):
            (ma, ca), (mb, cb) = S[i], S[j]
            M[i, j] = 0.7 * J(ma, mb) + 0.3 * J(ca, cb) if (ma and mb) else (J(ca, cb) if not (ma or mb) else 0.3 * J(ca, cb))
    return M
