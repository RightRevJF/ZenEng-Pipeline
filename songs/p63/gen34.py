"""Sung to Sleep (song 53): the hymn tune, drawn by a 3/4 sketch of Luthier's method with kept tables from the Essen folk-song collection
(tables/essen_34.json: 1,601 tunes in 3/4). Written in D major ("D-space") and transposed by the engraving: verses 1-3 and their refrains
up a semitone to E-flat, verse 4 and the final refrain up three to F.

The hymn form sets the rhythm's frame (Common Meter, iambic): every stressed syllable on a downbeat; a line's first syllable a pickup on
beat 3 (the refrain's 'Hush now' lines open on the downbeat: 'Hush' 'now' 'the' on beats 1-2-3); an 8-syllable line ends on a held half,
a 6-syllable line on a dotted half held into the next bar. Inside that frame each bar holding a stressed and an unstressed syllable is
drawn from the kept 3/4 bars: half and quarter (0, 24), quarter and half (0, 12), or the stressed syllable on two quarters under a slur
(0, 12, 24), by their kept shares.
Pitch: each next note drawn from the kept 3/4 interval shares, chord tones weighted on downbeats, in the compass C#4-D5 (D-space).
Designs (the writer's, logged): the refrain's 'Hush now' line low and still (D4-F#4); line 3 climbs, each downbeat at or above the one
before, to D5 on 'world' (held, a half note), the tune's only D5; line 4: the second 'sleeping' a step above the first, 'here' home on D4. Verse line 2 ends
on the half cadence (a tone of A); verse line 4 and the refrain end on D.
Gates: no leap past a fifth; 'here' reached by a fourth at most; no run of four in a line (749.2), no note of no length (749.1), the designs. Judge: charge against the kept quartiles on the pitch
readings and rhythm variety; the readings set by the hymn form (notes a bar, gap classes, onsets on the beat) printed, not charged.
Pick: least charge (within 0.05), then nearest the medians. Run: python3 gen34.py 3000"""
import json, random, sys, collections, hashlib
import numpy as np
import lyric_p63 as L
H = "/home/claude/p63"
T = json.load(open(f"{H}/tables/essen_34.json"))
BAR, BEAT = 36, 12
SCALE = {2, 4, 6, 7, 9, 11, 1}
CH = {"D": {2, 6, 9}, "G": {7, 11, 2}, "A": {9, 1, 4}, "A7": {9, 1, 4, 7}, "Bm": {11, 2, 6}, "Em": {4, 7, 11}, "Em7": {4, 7, 11, 2}, "F#m": {6, 9, 1}}
VERSE_CH = ["D", "G", "D", "A", "Bm", "G", "Em", "A", "D", "Bm", "G", "Em", "G", "A", "D", "D"]
REFRAIN_CH = ["D", "D", "G", "D", "Bm", "G", "A", "A", "G", "D", "Bm", "Em7", "G", "A7", "D", "D"]
LOW, HIGH = 61, 74
IV = {int(k): v for k, v in T["intervals"].items()}; IVT = sum(IV.values())
BARS = {tuple(k): v for k, v in T["bar_rhythms"]}
SHARE = {"half-quarter": BARS[(0, 24)], "quarter-half": BARS.get((0, 12), 1), "slur": 0.25 * BARS[(0, 12, 24)]}          # a hymn slurs sparingly: the kept (0, 12, 24) bar mostly carries three syllables
Q = T["readings_quartiles"]
FORM_SET = ("notes a bar", "gaps of a sixteenth", "gaps of an eighth", "gaps of a quarter or more", "onsets on the beat", "onsets on the bar's first beat")
def ivp(d): return (IV.get(max(-12, min(12, d)), 0) + 0.5) / IVT
def runs_ok(ps): return all(not (ps[k] == ps[k + 1] == ps[k + 2] == ps[k + 3]) for k in range(len(ps) - 3))
def rhythm_line(rng, li, refrain):
    """notes of one line: (on, dur, syl_index, stressed, slur_continues), on relative to the section's bar 0"""
    n = L.SHAPE[li]; b0 = 4 * li; out = []
    if refrain and li in (0, 1):                                        # 'Hush now, the ...': beats 1-2-3, then pairs
        out += [(b0 * BAR, 12, 0, True, False), (b0 * BAR + 12, 12, 1, False, False), (b0 * BAR + 24, 12, 2, False, False)]
        k, bar = 3, b0 + 1
    else:
        out.append((b0 * BAR - 12, 12, 0, False, False)); k, bar = 1, b0
    slurred = False
    while k < n - 1:
        kind = rng.choices(list(SHARE), weights=list(SHARE.values()))[0]
        if kind == "slur" and slurred: kind = "half-quarter"                # at most one slur a line
        if refrain and li == 2 and k == 5: kind = "half-quarter"          # 'world' held: the summit on a half note
        slurred = slurred or kind == "slur"
        t = bar * BAR
        if kind == "half-quarter": out += [(t, 24, k, True, False), (t + 24, 12, k + 1, False, False)]
        elif kind == "quarter-half": out += [(t, 12, k, True, False), (t + 12, 24, k + 1, False, False)]
        else: out += [(t, 12, k, True, True), (t + 12, 12, k, True, False), (t + 24, 12, k + 1, False, False)]
        k += 2; bar += 1
    hold = 60 if n == 6 else (36 if (refrain and li == 0) else 24)
    out.append((bar * BAR, hold, n - 1, True, False))
    return out
def chord_at(chs, t): return chs[max(0, t) // BAR]
def draw_line(rng, rh, chs, prev, rule):
    ps = []
    for j, (on, d, k, st, sl) in enumerate(rh):
        ct = CH[chord_at(chs, on)]; strong = on % BAR == 0
        lo, hi = rule.get("lo", LOW), rule.get("hi", HIGH - 1)
        if "pin" in rule and j in rule["pin"]: ps.append(rule["pin"][j]); continue
        cands = [p for p in range(lo, hi + 1) if p % 12 in SCALE and (p % 12 != 1 or chord_at(chs, on) in ("A", "A7"))]
        if j == len(rh) - 1 and "end" in rule: cands = [p for p in cands if p % 12 in rule["end"]]
        if strong and "rise" in rule and ps and j < min(rule.get("pin", {len(rh): 0})):
            last_down = max((ps[i] for i, x in enumerate(rh[:j]) if x[0] % BAR == 0), default=lo)
            cands = [p for p in cands if p >= last_down]
        if not cands: return None
        ref = ps[-1] if ps else prev
        w = [ivp(p - ref) * (6.0 if p % 12 in ct else 0.05) if strong else ivp(p - ref) * (1.5 if p % 12 in ct else 1.0) for p in cands]
        if j and rh[j - 1][4]:                                              # the slur's second note: a step from the first
            keep = [(x, p) for x, p in zip(w, cands) if 1 <= abs(p - ref) <= 2]
            if not keep: return None
            w, cands = [x for x, _ in keep], [p for _, p in keep]
        ps.append(rng.choices(cands, weights=w)[0])
    if any(abs(b - a) > 7 for a, b in zip(ps, ps[1:])): return None              # no leap past a fifth in a congregational tune
    return ps if runs_ok(ps) else None
def build(rng):
    tune = {}
    for sec, chs in (("verse", VERSE_CH), ("refrain", REFRAIN_CH)):
        prev = 66 if sec == "verse" else 62; lines = []
        for li in range(4):
            rh = rhythm_line(rng, li, sec == "refrain"); rule = {}
            if sec == "verse":
                rule = {"lo": 61, "hi": 71}
                if li == 1: rule["end"] = {9, 1, 4}
                if li == 3: rule["end"] = {2}
            else:
                if li == 0: rule = {"lo": 62, "hi": 66}
                if li == 1: rule = {"lo": 62, "hi": 69, "end": {9, 1, 4}}
                if li == 2:
                    wd = next(j for j, x in enumerate(rh) if x[2] == 5 and x[0] % BAR == 0)          # 'world' (syllable 5), on its downbeat
                    rule = {"lo": 64, "hi": 74, "rise": True, "pin": {wd: 74}}
                if li == 3:
                    rule = {"lo": 62, "hi": 71, "end": {2}}
            ps = None
            for _ in range(30):
                ps = draw_line(rng, rh, chs, prev, rule)
                if ps is None: continue
                if sec == "refrain" and li == 2 and sum(p == 74 for p in ps) != 1: ps = None; continue
                if sec == "refrain" and li == 3:
                    d1 = next(p for p, x in zip(ps, rh) if x[2] == 1); d2 = next(p for p, x in zip(ps, rh) if x[2] == 3)
                    if not (1 <= d2 - d1 <= 2 and d2 % 12 in CH["A7"] and d1 % 12 in CH["G"]) or ps[-1] != 62 or ps[-2] - ps[-1] > 5: ps = None; continue          # 'here' reached by a fourth at most
                if sec == "verse" and max(ps) >= 74: ps = None; continue
                break
            if ps is None: return None, f"{sec} {li}"
            lines.append([dict(on=on, dur=d, syl=k, stress=st, slur=sl, p=p, line=li) for (on, d, k, st, sl), p in zip(rh, ps)])
            prev = ps[-1]
        tune[sec] = lines
    return tune, None
def flat(tune): return [n for sec in ("verse", "refrain") for ln in tune[sec] for n in ln]
def readings(tune):
    out = []
    for i, sec in enumerate(("verse", "refrain")):
        for ln in tune[sec]:
            for n in ln: out.append((n["on"] + i * 16 * BAR, n["p"]))
    p = [x[1] for x in out]; iv = np.diff(p)
    bars = collections.defaultdict(list)
    for on, q in out: bars[on // BAR].append(on % BAR)
    pats = [tuple(v) for v in bars.values()]
    best = run = 1
    for a, b in zip(p, p[1:]): run = run + 1 if a == b else 1; best = max(best, run)
    gaps = np.diff([x[0] for x in out])
    return {"repeated notes": float(np.mean(iv == 0)), "moves by step": float(np.mean((abs(iv) >= 1) & (abs(iv) <= 2))), "moves by leap": float(np.mean(abs(iv) >= 5)),
            "turns of direction": sum(1 for a, b in zip(iv, iv[1:]) if a * b < 0) / max(1, int(np.sum(iv != 0)) - 1), "range": int(max(p) - min(p)),
            "distinct pitches": len(set(p)), "longest run of one pitch": best, "distinct rhythms over bars": len(set(pats)) / len(pats), "notes a bar": len(out) / len(pats),
            "onsets on the beat": float(np.mean([on % BEAT == 0 for on, _ in out])), "onsets on the bar's first beat": float(np.mean([on % BAR == 0 for on, _ in out])),
            "gaps of a sixteenth": float(np.mean(gaps == 3)), "gaps of an eighth": float(np.mean(gaps == 6)), "gaps of a quarter or more": float(np.mean(gaps >= 12))}
def charge(r):
    c = d = 0.0
    for k, (a, m, z) in Q.items():
        sp = max(z - a, 1e-6); d += abs(r[k] - m) / sp
        if k in FORM_SET: continue
        if r[k] < a: c += (a - r[k]) / sp
        if r[k] > z: c += (r[k] - z) / sp
    return c, d
if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000; SEED = 20261115 + 453
    rng = random.Random(SEED); alive = []; deaths = collections.Counter()
    for k in range(N):
        t, err = build(rng)
        if err: deaths[err] += 1; continue
        r = readings(t); c, d = charge(r)
        fp = hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in flat(t)]).encode()).hexdigest()[:12]
        alive.append(dict(tune=t, readings=r, charge=c, distance=d, n=k, fp=fp))
    least = min(a["charge"] for a in alive); near = [a for a in alive if a["charge"] <= least + 0.05]
    pick = min(near, key=lambda a: a["distance"])
    print(f"built {N}, survivors {len(alive)}; deaths {dict(deaths.most_common())}")
    print("pick", pick["fp"], "charge", round(pick["charge"], 3), "distance", round(pick["distance"], 2))
    for k, v in pick["readings"].items():
        a, m, z = Q[k]; print(f"  {k}: {round(v, 3)} (kept {round(a, 3)}, {round(m, 3)}, {round(z, 3)}){' *' if not (a <= v <= z) else ''}{' (form)' if k in FORM_SET else ''}")
    med = {k: float(np.median([a["readings"][k] for a in alive])) for k in Q}
    json.dump(dict(pick=pick, built=N, survivors=len(alive), deaths=dict(deaths), seed=SEED, median_build=med, verse_chords=VERSE_CH, refrain_chords=REFRAIN_CH), open(f"{H}/melody_final.json", "w"), default=float)
