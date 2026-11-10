"""Dance Anyway, version 2 (lyric draft 5). The writer heard version 1 and kept its verses, pre-choruses and choruses; this script
  (1) maps the three changed lines onto their tunes (chorus line 6 onto chorus line 6's notes; verse 2 line 3 and pre-chorus 2 line 2
      onto verse 1's and pre-chorus 1's, as version 1 did),
  (2) searches a new bridge melody scored against a bridge's job (the engine's answer to finding 204): an eighth-note grid with no
      sixteenths, longer notes, a climb line by line that stops on B-flat 4 under the chorus's C5, line 3 returning line 1's figure a
      third higher, chord tones weighted on the beat (199), a contour unrelated to any verse or chorus unit; ranked on contrast,
      chord tones, memory against the chorus and surprise,
  (3) searches a synth answer riff (finding 205): a two-beat figure on beats 3-4 of each chorus line's second bar (where the voice
      holds), its own rhythm and contour, chord tones on the beat, unrelated to the vocal hook, nothing a semitone from the held note;
      also four times in the intro and in the outro.
Usage: PYTHONHASHSEED=0 python3 melody_v2_p36.py [N]"""
import sys, os, json, math, random, pickle, hashlib, collections, itertools, copy
import numpy as np
sys.argv = [sys.argv[0], "1", "main"] + sys.argv[1:]
sys.path[:0] = ["/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import melody_p36 as M
import lyric_v2 as L2
from measures import PPM, ic_profile, m_horizon
N = int(sys.argv[3]) if len(sys.argv) > 3 else 400
SEED = 20261110 + 362
HERE = "/home/claude/p36"; BAR = M.BAR
V1 = pickle.load(open(f"{HERE}/melody_main.pkl", "rb"))["alive"][0]
WORDS2 = dict(L2.SECTIONS)
LINES2 = {s: [M.syl(t) for _, t in WORDS2[s]] for s in M.SUNG}
CHANGED = [("Chorus 1", 5), ("Chorus 2", 5), ("Verse 2", 2), ("Pre 2", 1)]
SRC = {("Chorus 1", 5): ("Chorus 1", 5), ("Chorus 2", 5): ("Chorus 1", 5), ("Verse 2", 2): ("Verse 1", 2), ("Pre 2", 1): ("Pre 1", 1)}
def line_notes(c, sec, i): return [dict(n) for n in c["notes"] if n["line"] == f"{sec}:{i}"]

def mapped_lines():
    """the changed lines on their tunes, with the stress reading of draft 5."""
    out = {}
    for sec, i in CHANGED:
        ss, si = SRC[(sec, i)]
        src = line_notes(V1, ss, si); U0 = (M.BAR0[ss] + 2 * si) * BAR; U = (M.BAR0[sec] + 2 * i) * BAR
        prev_line = line_notes(V1, sec, i - 1); tmin = max(-12, prev_line[-1]["on"] + 12 - U)
        ns = M.align(src, M.LINES[ss][si], LINES2[sec][i], U0, U, tmin)
        assert ns is not None, (sec, i)
        for n in ns: n["sec"] = sec; n["line"] = f"{sec}:{i}"
        out[(sec, i)] = ns
    return out

# ---- the bridge ----
BR = "Bridge"; B0 = M.BAR0[BR] * BAR
MU_B = [62, 64, 66, 68]; LO_B, HI_B = 58, 70
EIGHTH = list(range(-12, 73, 6))
RT_LONG = [[v * (2.5 if d in (12, 18, 24) else 0.6 if d == 6 else 1.0) for d, v in enumerate(row)] for row in M.RT]
import inspect
_src = inspect.getsource(M.line_rhythm).replace("def line_rhythm(", "def line_rhythm_bridge(").replace(
    "tg = [(48, 0.55), (72, 0.25), (24, 0.12), (60, 0.08)]", "tg = [(72, 0.6), (60, 0.25), (48, 0.15)]")
assert "line_rhythm_bridge" in _src and "(72, 0.6)" in _src
exec(_src, M.__dict__)
def bridge_rhythm(sy, rng, tmin):
    """the bridge changes gear (204): an eighth-note grid, the class's rhythm table tilted toward quarters and longer, and the line's
    last stress late in its second bar so its words spread over both bars"""
    old, oldrt = M.GRID, M.RT; M.GRID = EIGHTH; M.RT = RT_LONG
    try: ons = M.line_rhythm_bridge(sy, rng, tmin)
    finally: M.GRID = old; M.RT = oldrt
    return ons
def chord_w_beat(p, n, ch):
    tones = M.CH[ch][1]
    if n["on"] % M.BEAT == 0: return 3.0 if p % 12 in tones else 0.35        # 199: chord tones on the beat
    return 1.3 if p % 12 in tones else 1.0
def bridge_walk(rng, ns, prev, mu, lo, hi, fixed=None):
    out = []; run = 1; last_iv = None
    on_set = {n["on"] for n in ns}
    for i, n in enumerate(ns): n["dur"] = ns[i + 1]["on"] - n["on"] if i + 1 < len(ns) else 24
    for i, n in enumerate(ns):
        if fixed and i in fixed: p = fixed[i]
        else:
            ch = M.chord_for(n, on_set)
            cats = list(M.CATS)
            if last_iv is not None and abs(last_iv) > 7: cats = [x for x in M.CATS if x[0] in ("step", "third")]
            p = None
            while cats and p is None:
                c = rng.choices(cats, [x[1] for x in cats])[0]; cands, ws = [], []
                for sz in c[2]:
                    for sg in ((0,) if sz == 0 else (-1, 1)):
                        q = prev + sg * sz if prev is not None else None
                        if q is None or not (lo <= q <= hi) or q % 12 not in M.SUNGPC or M.clash(q, ch): continue
                        if sz == 0 and run >= 3: continue
                        if fixed and (i + 1) in fixed and (abs(q - fixed[i + 1]) > 5 or abs(q - fixed[i + 1]) == 6): continue   # into the held B-flat
                        if last_iv is not None and abs(last_iv) > 7 and (sg > 0) == (last_iv > 0): continue
                        w = math.exp(-(q - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(q) * chord_w_beat(q, n, ch) * M.SIZE_W.get(sz, 1.0)
                        w *= 1.0 if sz == 0 else (0.42 if sg < 0 else 0.58)            # the bridge climbs: ascending moves favoured
                        cands.append(q); ws.append(w)
                if cands and sum(ws) > 0: p = rng.choices(cands, ws)[0]
                else: cats.remove(c)
            if p is None: return None
        run = run + 1 if p == prev else 1; last_iv = (p - prev) if prev is not None else None
        prev = p; out.append(p)
    return out
def bridge_candidate(rng, before_last_on, prev_p):
    lines = []; last_on = before_last_on; prev = prev_p
    for i in range(4):
        sy = LINES2[BR][i]; U = B0 + 2 * i * BAR; tmin = max(-12, last_on + 12 - U)
        if i == 2:                                                        # line 3 returns line 1's figure a third higher
            ns = M.align(lines[0], LINES2[BR][0], sy, B0, U, tmin)
            if ns is None: return None
            ps = [M.dshift(n["p"], 2) for n in ns]
            if max(ps) > HI_B or min(ps) < LO_B: return None
            for n, p in zip(ns, ps): n["p"] = p
            if abs(ns[0]["p"] - prev) > 9 or abs(ns[0]["p"] - prev) == 6: return None
        else:
            ons = bridge_rhythm(sy, rng, tmin)
            if ons is None: return None
            ns = [dict(on=U + t, p=None, syl=k, slur=False, stress=sy[k][1]) for k, t in enumerate(ons)]
            if i == 3 and rng.random() < 0.6:                              # the last word held as two notes, rising into the summit's key
                t = ons[-1]
                if t + 6 <= 72: ns.append(dict(on=U + t + 6, p=None, syl=len(sy) - 1, slur=True, stress=False))
            fixed = {len(ns) - 1: HI_B} if i == 3 else None
            ps = bridge_walk(rng, ns, prev, MU_B[i], LO_B, HI_B, fixed)
            if ps is None: return None
            for n, p in zip(ns, ps): n["p"] = p
        for n in ns: n["sec"] = BR; n["line"] = f"{BR}:{i}"
        lines.append(ns); last_on = ns[-1]["on"]; prev = ns[-1]["p"]
    return lines

def unit_of(notes, s, ln=2 * BAR): return M.unit(notes, s, ln)
def bridge_score(c_notes, bl):
    flat = [n for n in c_notes if n["sec"] == BR]; ps = [n["p"] for n in flat]
    # contrast: no unit of the bridge related to any verse or chorus unit; onsets a bar and gaps against verse 1's
    others = [(M.BAR0[s] + 2 * k) * BAR for s in ("Verse 1", "Chorus 1") for k in range(len(LINES2[s]))]
    rel_max = 0.0; related_any = False
    for i in range(4):
        u = unit_of(c_notes, B0 + 2 * i * BAR)
        for s0 in others:
            r = M.related(u, unit_of(c_notes, s0)); related_any |= r[0]; rel_max = max(rel_max, r[2])
    v = [n for n in c_notes if n["sec"] == "Verse 1"]
    rate_b = len(flat) / 8; rate_v = len(v) / 8
    contrast = (0.0 if related_any else 0.4) + 0.3 * (1 - max(0.0, rel_max)) + 0.3 * max(0.0, min(1.0, (rate_v - rate_b) / 2.0))
    on = {n["on"] for n in c_notes}
    ct = sum(1 for n in flat if n["p"] % 12 in M.CH[M.chord_for(n, on)][1]) / len(flat)
    H = [n for n in c_notes if n["sec"] == "Chorus 1"]
    mh, _, _ = m_horizon(M.quarters(H, H[0]["on"]), M.quarters(flat, flat[0]["on"]))
    tune = M.quarters(flat, flat[0]["on"]); bits = M.PPMM.bits(PPM.symbols(tune, M.TONIC)); ic, _ = ic_profile(bits, ps.index(max(ps)))
    climb = 1.0 if all(max(n["p"] for n in bl[i + 1]) >= max(n["p"] for n in bl[i]) for i in range(3)) else 0.0
    score = 0.30 * contrast + 0.25 * ct + 0.15 * min(1, mh) + 0.15 * ic + 0.15 * climb
    return score, dict(contrast=contrast, related_any=related_any, rel_max=rel_max, chord_tones=ct, memory=mh, IC=ic, climb=climb,
                       onsets_per_bar=rate_b, verse_onsets_per_bar=rate_v, range=(min(ps), max(ps)))

# ---- the riff ----
def riff_candidates(rng, n=3000):
    """two beats (24 twelfths) on beats 3-4: 3-6 onsets on sixteenths, at least one off the beat; pitches as scale steps from a chord
    tone; read later against each bar's chord."""
    out = []
    slots = list(range(0, 24, 3))
    for _ in range(n):
        k = rng.choice([3, 4, 4, 5, 5, 6])
        ons = sorted(rng.sample(slots, k))
        if ons[0] not in (0, 3, 6) or not any(t % 6 == 3 for t in ons) and not any(t % 12 == 6 for t in ons): continue
        steps = [0]
        for _ in range(k - 1):
            steps.append(steps[-1] + rng.choice([-3, -2, -1, 1, 2, 3, 4, -4, 0]))
        if max(steps) - min(steps) < 3 or max(steps) - min(steps) > 7: continue
        out.append((tuple(ons), tuple(steps)))
    return list(dict.fromkeys(out))
DEGS = sorted(p for p in range(48, 96) if p % 12 in M.SCALE)
def riff_pitches(steps, ch, base_lo=70):
    root = M.CH[ch][0]; start = min(p for p in DEGS if p >= base_lo and p % 12 == root)
    i0 = DEGS.index(start); return [DEGS[i0 + s] for s in steps]
def riff_rhythm_bits(ons, at=24):
    seq = [at + t for t in ons] + [at + 24]
    return float(np.mean([-math.log2(max(1e-9, M.RT[a % BAR][min(96, b - a)])) for a, b in zip(seq, seq[1:])]))

if __name__ == "__main__":
    rng = random.Random(SEED)
    mapped = mapped_lines()
    base = [dict(n) for n in V1["notes"] if n["sec"] != BR and (n["sec"], int(n["line"].split(":")[1])) not in mapped]
    for v in mapped.values(): base += v
    before = sorted([n for n in base if n["on"] < B0], key=lambda n: n["on"])[-1]
    deaths = collections.Counter(); alive = []
    for k in range(N):
        bl = bridge_candidate(rng, before["on"], before["p"])
        if bl is None: deaths["bridge: no build"] += 1; continue
        notes = sorted([dict(n) for n in base] + [dict(n) for l in bl for n in l], key=lambda n: n["on"]); M.finish(notes)
        c = dict(notes=notes, meta=dict(plans=V1["meta"]["plans"], shifts=V1["meta"]["shifts"],
                                        returns=[r for r in V1["meta"]["returns"] if r[0] != BR] + [(BR, 2, BR, 0, 2)]))
        old = M.LINES; M.LINES = LINES2
        try: cert, m = M.evaluate(c)
        finally: M.LINES = old
        if cert: deaths[cert[0]] += 1; continue
        if any(t["on"] % 6 for l in bl for t in l): deaths["bridge: a sixteenth"] += 1; continue
        sc, sd = bridge_score(notes, bl)
        if sd["related_any"]: deaths["bridge: related to a verse or chorus unit (204)"] += 1; continue
        c["meas"] = m; c["bridge"] = sd; c["bridge_score"] = sc; c["fp"] = M.fingerprint(c); alive.append(c)
    alive.sort(key=lambda c: (-c["bridge_score"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    print(f"bridge search: {N} built, {len(alive)} survivors, order {order}")
    for kk, vv in deaths.most_common(): print(f"   {vv:5d}  {kk}")
    best = alive[0]
    print("pick", best["fp"], round(best["bridge_score"], 3), {k: (round(v, 3) if isinstance(v, float) else v) for k, v in best["bridge"].items()}, "song pitch", best["meas"]["pitch_bits"], "composite", best["meas"]["composite"])
    # ---- the riff, against the pick ----
    notes = best["notes"]
    hook = M.unit(notes, M.BAR0["Chorus 1"] * BAR, 2 * BAR)
    slots_ = []
    for s in ("Chorus 1", "Chorus 2", "Last Chorus"):
        for i in range(8):
            b = M.BAR0[s] + 2 * i + 1; t0 = b * BAR + 24
            held = [n for n in notes if n["on"] < t0 + 24 and n["on"] + n["dur"] > t0]
            starts = [n for n in notes if t0 <= n["on"] < t0 + 24]
            slots_.append(dict(bar=b, ch=M.CHORD[b], t0=t0, held=[n["p"] for n in held], busy=len(starts)))
    rng2 = random.Random(SEED + 1)                 # the riff's own draw, apart from the bridge's
    cands = riff_candidates(rng2); rows = []
    for ons, steps in cands:
        rb = riff_rhythm_bits(ons)
        if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): continue
        bad = 0; ctb = 0; nb = 0
        for sl in slots_:
            ps = riff_pitches(steps, sl["ch"])
            for t, p in zip(ons, ps):
                if any(abs((p - h) % 12) in (1, 11) for h in sl["held"]): bad += 1
                if t % 12 == 0: nb += 1; ctb += p % 12 in M.CH[sl["ch"]][1]
        if bad: continue
        if min(min(riff_pitches(steps, sl["ch"])) for sl in slots_) < 67: continue      # above the voice's chorus lines
        r = M.unit([dict(on=t, p=p) for t, p in zip(ons, riff_pitches(steps, "Eb"))], 0, 24)
        rel_hook = M.related((r[0], r[1], r[2]), M.unit([dict(on=n["on"] - (M.BAR0["Chorus 1"] * BAR + 72), p=n["p"]) for n in notes if n["sec"] == "Chorus 1" and n["line"] == "Chorus 1:0"], 0, 24))
        sync = sum(1 for t in ons if t % 12) / len(ons)
        leap = max(abs(b - a) for a, b in zip(steps, steps[1:]))
        dif = [b2 - a for a, b2 in zip(steps, steps[1:])]
        turn = any((x > 0) != (y > 0) for x, y in zip([d for d in dif if d], [d for d in dif if d][1:]))
        score = (0.30 * (ctb / max(1, nb)) + 0.20 * min(1, sync / 0.5) + 0.15 * (1.0 if leap >= 3 else 0.4) + 0.15 * (0 if rel_hook[0] else 1)
                 + 0.10 * (1 if len(ons) in (4, 5) else 0) + 0.10 * turn - 0.10 * sum(1 for d in dif if d == 0) - 0.05 * abs(rb - 2.2))
        rows.append((score, ons, steps, rb, ctb / max(1, nb), sync, rel_hook[0]))
    rows.sort(key=lambda x: (-x[0], x[1], x[2]))
    riff = rows[0]
    print(f"riff: {len(cands)} drawn, {len(rows)} pass; pick onsets {riff[1]} steps {riff[2]} rhythm {riff[3]:.2f} bits, chord tones on the beat {riff[4]:.2f}, off the beat {riff[5]:.2f}, related to the hook: {riff[6]}")
    code = hashlib.sha1(open(__file__, "rb").read() + open(f"{HERE}/lyric_v2.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, N=N, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), from_v1=V1["fp"], cmd=f"PYTHONHASHSEED=0 python3 melody_v2_p36.py {N}")
    print("rerun:", rerun)
    pickle.dump(dict(pick=best, alive=alive[:20], deaths=deaths, built=N, survivors=len(alive), order=order, riff=riff, riff_slots=slots_, riff_rows=len(rows),
                     riff_drawn=len(cands), mapped={f"{k[0]}:{k[1]}": v for k, v in mapped.items()}, rerun=rerun, lines2=LINES2),
                open(f"{HERE}/melody_v2.pkl", "wb"))
