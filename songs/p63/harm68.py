"""Harmony vocals written as lines (proposed fix 749.9, tried on song 52).

Before: each harmony note was the nearest chord tone a third or fourth above (or below) the lead's note, in the lead's rhythm: a shadow.
Now two parts with different jobs:
  - High: sings the words with the lead, in its rhythm, a third to a sixth above. Chosen as one line by the least cost over the whole
    phrase (dynamic programming): small moves and held notes are cheap; motion against the lead or holding while the lead moves is cheaper
    than moving with it; parallel fifths and octaves with the lead, a tritone against it, and a non-chord tone on a stressed or long note
    are ruled out or costly. Thirds are the home interval, sixths next, fourths and fifths occasional.
  - Low: sings "ooh" in long notes under the lead, a third to a sixth below its lowest note in each beat, one note a beat at most and held
    while it fits, chord tones only, never a second, seventh or tritone against a lead note of an eighth or longer.
Readings (both versions): at each pair of the lead's onsets inside the harmony, how the part moves against the lead (similar, contrary,
oblique), parallel fifths and octaves, the intervals used, and the part's own notes and moves."""
import collections
BAR, BEAT = 36, 18
SCALE = {2, 4, 6, 7, 9, 11, 1}
def _ic(h, l): return abs(h - l) % 12
NODE_HI = {3: 0.0, 4: 0.0, 8: 0.4, 9: 0.4, 5: 1.2, 7: 1.6}            # interval above the lead: cost (tritone ruled out)
W = dict(move=0.3, hold=0.15, contrary=0.9)
def _trans(hp, lp, h, l, linked=True):
    m = abs(h - hp); c = W['move'] * m + (2.0 if m > 4 else 0) + (6.0 if m > 7 else 0)
    if m == 0: c -= W['hold']
    if not linked: return 0.5 * c
    dl, dh = l - lp, h - hp
    if dl and dh and (dl > 0) == (dh > 0):
        c += 0.7
        if _ic(h, l) in (0, 7) and _ic(hp, lp) == _ic(h, l): c += 25.0          # parallel fifths or octaves
    elif dl and dh: c -= W['contrary']                                                        # contrary
    elif dl and not dh: c -= 0.3                                                    # oblique
    return c
def high(lead_span, tones_at, lo=57, hi=79):
    """lead_span: lead notes in order (dicts with on, dur, midi, stress, line, sec); one DP over the span (line joins relaxed)."""
    cands = []
    for n in lead_span:
        ct = tones_at(n["on"]); strong = n["stress"] or n["dur"] >= 12 or n["on"] % BEAT == 0
        pcs = ct if (strong or ct - SCALE) else (SCALE | ct)
        cs = [(p, NODE_HI[_ic(p, n["midi"])] + (0 if p % 12 in ct else 0.8)) for p in range(n["midi"] + 3, n["midi"] + 10)
              if lo <= p <= hi and p % 12 in pcs and _ic(p, n["midi"]) in NODE_HI]
        if not cs: cs = [(min((p for p in range(n["midi"] + 3, n["midi"] + 10) if p % 12 in ct), default=n["midi"] + 4), 5.0)]
        cands.append(cs)
    best = [{p: (c, None) for p, c in cands[0]}]
    for k in range(1, len(lead_span)):
        a, b = lead_span[k - 1], lead_span[k]; linked = (a["sec"], a["line"]) == (b["sec"], b["line"])
        row = {}
        for p, c in cands[k]:
            row[p] = min(((best[-1][q][0] + _trans(q, a["midi"], p, b["midi"], linked) + c, q) for q in best[-1]), key=lambda x: x[0])
        best.append(row)
    p = min(best[-1], key=lambda q: best[-1][q][0]); out = [p]
    for k in range(len(lead_span) - 1, 0, -1): p = best[k][p][1]; out.append(p)
    return out[::-1]
def low(lead_span, tones_at, lo=55, hi=69):
    """'ooh' under the lead: segments at the beats inside each line; one DP per line; equal neighbours merged into held notes."""
    lines = collections.OrderedDict()
    for n in lead_span: lines.setdefault((n["sec"], n["line"]), []).append(n)
    out = []
    for key, ln in lines.items():
        t0, t1 = ln[0]["on"], ln[-1]["on"] + ln[-1]["dur"]
        cuts = [t0] + [t for t in range((t0 // BEAT + 1) * BEAT, t1, BEAT)] + [t1]
        if len(cuts) > 2 and cuts[1] - cuts[0] < 12: cuts = cuts[1:]                 # a pickup: the 'ooh' starts on the beat
        segs = []
        for a, b in zip(cuts, cuts[1:]):
            snd = [n for n in ln if n["on"] < b and n["on"] + n["dur"] > a]
            if snd: segs.append((a, b, snd))
        cands = []
        for a, b, snd in segs:
            ct = tones_at(a); top = min(n["midi"] for n in snd); cs = []
            for p in range(max(lo, top - 9), min(hi, top - 3) + 1):
                if p % 12 not in ct: continue
                bad = sum(1 for n in snd if n["dur"] >= 6 and _ic(n["midi"], p) in (1, 2, 6, 10, 11))
                cs.append((p, 6.0 * bad + (0 if _ic(top, p) in (3, 4, 8, 9) else 0.8)))
            if not cs: cs = [(max(lo, top - 4), 6.0)]
            cands.append(cs)
        best = [{p: (c, None) for p, c in cands[0]}]
        for k in range(1, len(segs)):
            la, lb = segs[k - 1][2][-1]["midi"], segs[k][2][0]["midi"]; row = {}
            for p, c in cands[k]:
                row[p] = min(((best[-1][q][0] + _trans(q, la, p, lb) - (0.8 if q == p else 0) + c, q) for q in best[-1]), key=lambda x: x[0])
            best.append(row)
        p = min(best[-1], key=lambda q: best[-1][q][0]); ps = [p]
        for k in range(len(segs) - 1, 0, -1): p = best[k][p][1]; ps.append(p)
        ps = ps[::-1]
        for (a, b, snd), p in zip(segs, ps):
            if out and out[-1]["key"] == key and out[-1]["midi"] == p and out[-1]["on"] + out[-1]["dur"] == a: out[-1]["dur"] = b - out[-1]["on"]
            else: out.append(dict(on=a, dur=b - a, midi=p, key=key, sec=key[0], line=key[1], text="ooh"))
    return out
def sounding(part, t):
    for n in part:
        if n["on"] <= t < n["on"] + n["dur"]: return n["midi"]
    return None
def readings(lead_span, part):
    pairs = []; sim = con = obl = par = 0; ics = collections.Counter()
    for a, b in zip(lead_span, lead_span[1:]):
        if (a["sec"], a["line"]) != (b["sec"], b["line"]): continue
        ha, hb = sounding(part, a["on"]), sounding(part, b["on"])
        if ha is None or hb is None: continue
        dl, dh = b["midi"] - a["midi"], hb - ha
        if not dl and not dh: continue
        if dl and dh and (dl > 0) == (dh > 0):
            sim += 1
            if _ic(hb, b["midi"]) in (0, 7) and _ic(ha, a["midi"]) == _ic(hb, b["midi"]): par += 1
        elif dl and dh: con += 1
        else: obl += 1
    for n in lead_span:
        h = sounding(part, n["on"])
        if h is not None: ics[abs(h - n["midi"])] += 1
    tot = max(1, sim + con + obl); ps = [n["midi"] for n in part]
    moves = [abs(b - a) for a, b in zip(ps, ps[1:])]
    return {"moves with the lead (similar)": sim / tot, "against it (contrary)": con / tot, "holding while it moves, or the reverse (oblique)": obl / tot,
            "parallel fifths or octaves": par, "distinct distances from the lead": len(ics), "farthest from the lead (semitones)": max(ics) if ics else 0,
            "notes": len(part), "held notes (a dotted quarter or longer)": sum(1 for n in part if n["dur"] >= 18), "mean move (semitones)": (sum(moves) / len(moves)) if moves else 0.0}
