"""Score-only tension features per bar for CoCoPops songs (parse_cocopops.py -> cocopops_bars.json), and the per-bar ratings.
Harmony: Lerdahl's chord distance (Tonal Pitch Space, 2001), delta = i + j + k, from the tonic (the 'hierarchical' reading at its shallowest)
and from the previous chord (the sequential reading); the engine's old 1-to-3 chord value (Table CO); chord dissonance (tones beyond the
triad). Melody: pitch height, highest note, onsets per second, share of the bar sung, share of sung time on non-chord tones.
Approximations: a chord's region is the home key when its triad is diatonic (minor keys admit the raised 7th in V and vii), otherwise the
nearest major-key collection on the circle of fifths that holds the triad; j between regions is the chromatic fifths distance."""
import json, re, numpy as np
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc_of(name):
    p = PC[name[0].upper()]
    for c in name[1:]:
        if c in "#": p += 1
        elif c in "-b": p -= 1
    return p % 12
QUAL = {"maj": [0, 4, 7], "min": [0, 3, 7], "dim": [0, 3, 6], "aug": [0, 4, 8], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10],
        "dim7": [0, 3, 6, 9], "hdim7": [0, 3, 6, 10], "minmaj7": [0, 3, 7, 11], "maj6": [0, 4, 7, 9], "min6": [0, 3, 7, 9], "9": [0, 4, 7, 10, 2],
        "maj9": [0, 4, 7, 11, 2], "min9": [0, 3, 7, 10, 2], "11": [0, 4, 7, 10, 2, 5], "min11": [0, 3, 7, 10, 2, 5], "13": [0, 4, 7, 10, 2, 9],
        "maj13": [0, 4, 7, 11, 2, 9], "min13": [0, 3, 7, 10, 2, 9], "sus4": [0, 5, 7], "sus2": [0, 2, 7], "7sus4": [0, 5, 7, 10], "1": [0], "5": [0, 7]}
def parse_harte(h):
    if not h or h in ("N", "X", ".") or h.startswith("="): return None
    h = h.split("/")[0]
    if ":" in h: r, q = h.split(":", 1)
    else: r, q = h, "maj"
    q = re.sub(r"\(.*\)", "", q) or "maj"
    try: root = pc_of(r)
    except (KeyError, IndexError): return None
    iv = QUAL.get(q)
    if iv is None:
        iv = QUAL["min"] if q.startswith("min") else QUAL["maj"]
    pcs = [(root + x) % 12 for x in iv]
    third = next((x for x in iv if x in (3, 4)), None); fifth = next((x for x in iv if x in (6, 7, 8)), 7)
    triad = [root] + ([(root + third) % 12] if third is not None else [(root + iv[1]) % 12] if len(iv) > 1 else []) + [(root + fifth) % 12]
    extra = len(set(pcs) - set(triad)) + (1 if q in ("dim", "aug", "dim7", "hdim7") else 0) + (1 if "sus" in q else 0)
    return dict(root=root, pcs=sorted(set(pcs)), triad=sorted(set(triad)), fifth=(root + fifth) % 12, diss=extra, q=q)
MAJ = [0, 2, 4, 5, 7, 9, 11]
def coll(tonic_major): return {(tonic_major + x) % 12 for x in MAJ}
def key_info(key):
    if not key: return None
    minor = key[0].islower(); t = pc_of(key)
    return dict(tonic=t, minor=minor, rel=(t + 3) % 12 if minor else t)   # rel = the major collection's tonic
def region(ch, K):
    home = coll(K["rel"])
    allow = set(home)
    if K["minor"]: allow |= {(K["tonic"] + 11) % 12} if ch["root"] in ((K["tonic"] + 7) % 12, (K["tonic"] + 11) % 12) else set()
    if set(ch["triad"]) <= allow: return 0, allow
    best = None
    for s in range(1, 7):
        for sg in (1, -1):
            r = (K["rel"] + 7 * s * sg) % 12; c = coll(r)
            if set(ch["triad"]) <= c: return s, c
    return 6, set(range(12))
FIFTHS = [5, 0, 7, 2, 9, 4, 11]   # diatonic circle F C G D A E B, in C
def j_steps(r1, r2, collection, rel):
    rel_pos = [(x + rel) % 12 for x in FIFTHS]
    if r1 in rel_pos and r2 in rel_pos:
        a, b = rel_pos.index(r1), rel_pos.index(r2); d = abs(a - b); return min(d, 7 - d)
    d = ((r2 - r1) * 7) % 12; return min(d, 12 - d)
def space(ch, collection):
    return [{ch["root"]}, {ch["root"], ch["fifth"]}, set(ch["triad"]), set(collection)]
def delta(x, y, K):
    ix, cx = region(x, K); iy, cy = region(y, K)
    i = abs(ix - iy) if ix == 0 or iy == 0 else min(abs(ix - iy), 6)
    j = j_steps(x["root"], y["root"], cy, K["rel"])
    X, Y = space(x, cx), space(y, cy)
    k = sum(len(Yl - Xl) for Xl, Yl in zip(X, Y))
    return i + j + k
def tonic_chord(K):
    t = K["tonic"]; return parse_harte(f"{'CDEFGAB'[0]}:maj") and dict(root=t, pcs=sorted({t, (t + (3 if K['minor'] else 4)) % 12, (t + 7) % 12}),
        triad=sorted({t, (t + (3 if K['minor'] else 4)) % 12, (t + 7) % 12}), fifth=(t + 7) % 12, diss=0, q="min" if K["minor"] else "maj")
OLD = {0: 0, 7: 3, 11: 3, 5: 2, 2: 2, 9: 1, 4: 1, 3: 1, 8: 2, 10: 2}
def old_value(ch, K):
    return OLD.get((ch["root"] - K["tonic"]) % 12, 2)
def features(song):
    bars = song["bars"]; out = []; prev = None; last_key = None
    ts = [b["t"] for b in bars]
    for n, b in enumerate(bars):
        K = key_info(b["key"] or last_key); last_key = b["key"] or last_key
        # bar length in seconds
        nxt = next((bars[m]["t"] for m in range(n + 1, len(bars)) if bars[m]["t"] is not None), None)
        sec = (nxt - b["t"]) if (b["t"] is not None and nxt is not None and nxt > b["t"]) else None
        f = dict(bar=b["bar"], label=b["label"], t=b["t"], sec=sec)
        chs = []
        for c in b["chords"]:
            ch = parse_harte(c["harte"])
            if ch and K: chs.append((ch, c["q"] or 1.0))
        if K and chs:
            T = tonic_chord(K); w = sum(q for _, q in chs)
            f["tps_tonic"] = sum(delta(T, ch, K) * q for ch, q in chs) / w
            seq = []
            for ch, q in chs:
                if prev is not None: seq.append((delta(prev, ch, K), q))
                prev = ch
            f["tps_seq"] = (sum(d * q for d, q in seq) / sum(q for _, q in seq)) if seq else None
            f["old"] = sum(old_value(ch, K) * q for ch, q in chs) / w
            f["diss"] = sum(ch["diss"] * q for ch, q in chs) / w
            f["tonic_bar"] = int(any((ch["root"] - K["tonic"]) % 12 == 0 and ch["q"] in ("maj", "min", "maj7", "min7", "maj6", "min6") for ch, _ in chs))
            f["dom_bar"] = int(any((ch["root"] - K["tonic"]) % 12 == 7 for ch, _ in chs))
            f["chords_n"] = len(b["chords"])
        # melody, aligned to the bar's chords by quarter position
        pos = 0.0; sung = []; cpos = []; acc = 0.0
        for ch, q in chs: cpos.append((acc, acc + q, ch)); acc += q
        nct = 0.0; tot = 0.0; ons = 0
        for nt in b["notes"]:
            if nt["p"] is not None:
                sung.append((nt["p"], nt["q"])); ons += int(nt["on"])
                c = next((c for a, z, c in cpos if a <= pos < z), cpos[-1][2] if cpos else None)
                if c is not None:
                    tot += nt["q"]; nct += nt["q"] * (nt["p"] % 12 not in c["pcs"])
            pos += nt["q"]
        qbar = sum(nt["q"] for nt in b["notes"]) or (b["meter"][0] * 4 / b["meter"][1] if b["meter"] else 4.0)
        if sung:
            w = sum(q for _, q in sung)
            f["pitch"] = sum(p * q for p, q in sung) / w if w else float(np.mean([p for p, _ in sung]))
            f["pmax"] = max(p for p, _ in sung)
            f["sung"] = min(1.0, w / max(qbar, 1e-6))
        else:
            f["sung"] = 0.0
        f["onsets"] = ons
        f["onset_rate"] = (ons / sec) if sec else None
        f["nct"] = (nct / tot) if tot else None
        ar = [np.mean(x) for x in b["ar"] if x]; va = [np.mean(x) for x in b["va"] if x]
        f["arousal"] = float(np.mean(ar)) if ar else None
        f["valence"] = float(np.mean(va)) if va else None
        f["rms"] = float(np.mean(b["rms"])) if b["rms"] else None
        out.append(f)
    return out
if __name__ == "__main__":
    S = json.load(open("cocopops_bars.json"))
    F = {k: dict(varms=s["varms"], bars=features(s)) for k, s in S.items()}
    json.dump(F, open("cocopops_features.json", "w"))
    # checks: Table CO distances from I in C major
    K = key_info("C"); T = tonic_chord(K)
    for h in ["G:maj", "F:maj", "A:min", "E:min", "D:min", "B:dim", "A#:maj", "D:maj", "G#:maj", "E:maj"]:
        print(h, delta(T, parse_harte(h), K), end="; ")
    print()
    import collections
    n = sum(len(s["bars"]) for s in F.values()); r = sum(1 for s in F.values() for b in s["bars"] if b.get("arousal") is not None)
    print(n, "bars;", r, "rated bars;", sum(1 for s in F.values() for b in s["bars"] if b.get("tps_tonic") is not None), "with chords")
