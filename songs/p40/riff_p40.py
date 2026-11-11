"""Nothing Else on Earth (song 40): the instrumental figure (209, 235) against the shortlist pick: the riff, the fills, the riff break.
  The riff: a one-bar electric-guitar figure, its rhythm from the class's rhythm table (RT), chord tones on the beats, a contour of its own,
  unrelated by 27.31's test to every sung line's opening bar (235). It is placed on each chord of the riff progression (D C G D; over C the
  scale is D mixolydian, C natural), low (from D3). It plays all eight intro bars (the guitar alone in bars 1-4, the band from bar 5: the
  writer's riff-led A at Q5) and the outro's first three bars; the outro's last bar is one hit, left to ring.
  The fills (235, 272): where the voice is silent 2 beats or more, a fill in 70% of gaps (rate counted on gaps of 2.75 beats or more), as
  song 38's v2.
  The riff break (Solo kind): 8 bars over D C G D twice: the riff, its answer a step up, a walked line, the riff again, last note a chord tone.
  No countermelody (Q18 A: not chosen).
Usage: PYTHONHASHSEED=0 python3 riff_p40.py      (seeds: the melody's + 1 for the figure, + 2 for the solo, + 3 for fills)"""
import sys, math, random, pickle, hashlib, collections
import numpy as np
sys.argv = [sys.argv[0], "1", "main"]; sys.path[:0] = ["/home/claude/p40"]
import melody_p40 as P
M = P.M; BAR, BEAT = P.BAR, P.BEAT
D = pickle.load(open("/home/claude/p40/melody_main.pkl", "rb")); pick = D["pick"]; notes = pick["notes"]
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
SEED = D["rerun"]["seed"] + 1
DEGS = sorted(p for p in range(40, 100) if p % 12 in M.SCALE)
MIXO = (M.SCALE - {1}) | {0}                                                         # over C: D mixolydian (C natural)
def pitches(steps, ch, base_lo=64):
    dg = DEGS if ch != "C" else sorted(p for p in range(40, 100) if p % 12 in MIXO)
    root = M.CH[ch][0]; start = min(p for p in dg if p >= base_lo and p % 12 == root)
    i0 = dg.index(start); return [dg[i0 + s] for s in steps]
def draw(rng):
    t = rng.choice([0, 0, 6]); ons = [t]
    while True:
        ds = [d for d in range(6, 25, 6) if t + d < BAR]
        if not ds: break
        d = rng.choices(ds, [M.RT[t % BAR][d] for d in ds])[0]
        if t + d >= BAR - 6 or (len(ons) >= 4 and rng.random() < 0.22): break
        t += d; ons.append(t)
    if not 4 <= len(ons) <= 7: return None
    steps = [0]
    for _ in range(len(ons) - 1): steps.append(steps[-1] + rng.choice([-3, -2, -1, 1, 2, 3, 4, -4, 0]))
    if not 3 <= max(steps) - min(steps) <= 7: return None
    return tuple(ons), tuple(steps)
def rbits(ons, span=BAR):
    seq = list(ons) + [span]
    return float(np.mean([-math.log2(max(1e-9, M.RT[a % BAR][min(96, b - a)])) for a, b in zip(seq, seq[1:])]))
I0, O0 = P.BAR0["Intro"], P.BAR0["Outro"]
RIFF_LO = 50                                                                          # D3: the riff sits low, under the voice's row
SLOTS = [dict(where="intro", at=b * BAR, end=(b + 1) * BAR) for b in range(I0, I0 + 8)] + \
        [dict(where="outro", at=b * BAR, end=(b + 1) * BAR) for b in range(O0, O0 + 3)]
def place(ons, steps, sl):
    ch = M.chord_at(sl["at"]); ps = pitches(steps, ch, RIFF_LO)
    return [(sl["at"] + t, p) for t, p in zip(ons, ps) if sl["at"] + t < sl["end"]]
def held_at(t): return [n["p"] for n in notes if n["on"] <= t < n["on"] + n["dur"]]
LINE_UNITS = []
for ln in dict.fromkeys(n["line"] for n in notes):
    ns = [n for n in notes if n["line"] == ln]; s, i = ln.split(":"); U = P.line_start(s, int(i))
    LINE_UNITS.append((ln, M.unit(notes, U, BAR), M.unit(notes, U - BEAT, BAR)))
def related_any(fig):
    u = M.unit(fig, 0, BAR); best = None
    for ln, a, b in LINE_UNITS:
        for x in (a, b):
            r = M.related(u, x)
            if r[0]: return True, ln
    return False, None

def solo(rng, rons, rsteps):
    b0 = P.BAR0["Riff break"]; out = []
    for k, sh in ((0, 0), (1, 2)):
        for t, p in zip(rons, pitches(tuple(s + sh for s in rsteps), M.chord_at((b0 + k) * BAR), 69)): out.append([(b0 + k) * BAR + t, p])
    t = (b0 + 2) * BAR; prev = out[-1][1]; run = 1; last_iv = None
    P.AIM = P.Aim(pick["meta"]["targets"]["C"], "C")
    while t < (b0 + 6) * BAR:
        pos = t % BAR; ds = [d for d in (6, 12, 18, 24) if t + d <= (b0 + 6) * BAR]
        d = rng.choices(ds, [M.RT[pos][d] * {6: 1.4, 12: 1.4, 18: 1.0, 24: 0.9}[d] for d in ds])[0]
        n = dict(on=t); ch = M.chord_at(t)
        mu = 74 + 5 * math.sin(math.pi * (t - (b0 + 2) * BAR) / (4 * BAR))
        p = P.next_pitch(rng, prev, run, n, ch, mu, 66, 84, last_iv)
        if p is None: return None
        run = run + 1 if p == prev else 1; last_iv = p - prev; prev = p; out.append([t, p]); t += d
    for k in (6, 7):
        for tt, p in zip(rons, pitches(rsteps, M.chord_at((b0 + k) * BAR), max(62, out[-1][1] - 6))): out.append([(b0 + k) * BAR + tt, p])
    for j in range(1, len(out)):                                                       # no leap past an octave between the solo's parts
        while out[j][1] - out[j - 1][1] > 12: out[j][1] -= 12
        while out[j - 1][1] - out[j][1] > 12: out[j][1] += 12
    ch = M.chord_at(out[-1][0]); out[-1][1] = min((p for p in range(66, 85) if p % 12 in M.CH[ch][1]), key=lambda p: abs(p - out[-1][1]))
    ev = []
    for j, (t, p) in enumerate(out):
        nxt = out[j + 1][0] if j + 1 < len(out) else (b0 + 8) * BAR
        ev.append(dict(on=t, dur=max(6, nxt - t), p=p))
    return ev
def solo_ok(ev):
    nb = ct = tr = 0
    for e in ev:
        ch = M.chord_at(e["on"])
        if e["on"] % BEAT == 0:
            nb += 1; ct += e["p"] % 12 in M.CH[ch][1]; tr += (e["p"] - M.CH[ch][0]) % 12 == 6
    ons = [e["on"] for e in ev] + [(P.BAR0["Riff break"] + 8) * BAR]
    rb = float(np.mean([-math.log2(max(1e-9, M.RT[a % BAR][min(96, b - a)])) for a, b in zip(ons, ons[1:])]))
    mx = max(abs(b["p"] - a["p"]) for a, b in zip(ev, ev[1:]))
    return dict(ct=ct / nb, tritones=tr, rbits=rb, max_leap=mx, ok=ct / nb >= 0.6 and tr == 0 and M.RBAND["p05"] <= rb <= M.RBAND["p95"] and mx <= 12)

def gaps():
    """the voice's silences of 2 beats or more inside the sung sections (none from 'Turn it off.' on)."""
    out = []; tag_on = min(n["on"] for n in notes if n["line"] == "Last Chorus:8")
    for a, b in zip(notes, notes[1:]):
        stop = a["on"] + a["dur"]; g = b["on"] - stop
        if g >= 2 * BEAT and b["on"] <= tag_on and a["sec"] == b["sec"] or (g >= 2 * BEAT and a["sec"] != b["sec"] and b["on"] <= tag_on and (b["on"] - stop) <= 8 * BEAT):
            out.append(dict(stop=stop, ret=b["on"], beats=g / BEAT, after=a["line"]))
    return out
def fill(rng, g):
    """235: 4-6 notes, 2-3 beats (2.75 at most in a long gap), from 0.5 or 0.75 beats after the voice stops, before it returns.
    272: a gap under 2.75 beats takes a fill of a beat and a half, from half a beat after the voice stops, ending as it returns."""
    if g["beats"] < 2.75:
        start = g["stop"] + 6
        if g["ret"] - start < 18: return None
        L_ = 18; k = rng.choice([4, 5, 6])
    else:
        start = g["stop"] + rng.choice([6, 9]); room = g["ret"] - start - 3
        mx = min(36 if g["beats"] < 8 else 33, room)
        if mx < 24: return None
        L_ = rng.choice([x for x in (24, 27, 30, 33, 36) if x <= mx]); k = rng.choice([4, 5, 6])
    if L_ // k < 3: return None
    cuts = sorted(rng.sample(range(1, L_ // 3), k - 1)); ons = [0] + [c * 3 for c in cuts]
    if any(b - a < 3 for a, b in zip(ons, ons[1:])): return None
    ln = [n for n in notes if n["line"] == g["after"]]; mu = float(np.median([n["p"] for n in ln])) + 12
    P.AIM = P.Aim(pick["meta"]["targets"]["C"], "C"); prev = int(round(mu)); prev = min(DEGS, key=lambda d: abs(d - prev)); out = []; run = 1; li = None
    for j, t in enumerate(ons):
        n = dict(on=start + t); ch = M.chord_at(start + t)
        p = P.next_pitch(rng, prev if out else None, run, n, ch, mu, 60, 84, li)
        if p is None: return None
        run = run + 1 if out and p == prev else 1; li = (p - prev) if out else None; prev = p; out.append(dict(on=start + t, p=p))
    last = out[-1]; ch = M.chord_at(last["on"])
    if last["p"] % 12 not in M.CH[ch][1]:
        opts = [last["p"] + d for d in (-1, 1, -2, 2) if (last["p"] + d) % 12 in M.CH[ch][1]]
        if not opts: return None
        last["p"] = opts[0]
    for j, e in enumerate(out): e["dur"] = (out[j + 1]["on"] if j + 1 < len(out) else start + L_) - e["on"]
    if any(abs((e["p"] - h) % 12) in (1, 11) for e in out for h in held_at(e["on"])): return None
    fu = M.unit([dict(on=e["on"] - start, p=e["p"]) for e in out], 0, BAR)                    # never the phrase before it
    lu = M.unit([dict(on=n["on"] - ln[0]["on"], p=n["p"] + 12) for n in ln], 0, BAR)
    if M.related(fu, lu)[0]: return None
    return out

def counter(rng):
    """the last chorus's organ line, bars 1-16, above the voice (C#5 to A5)."""
    b0 = P.BAR0["Last Chorus"]; out = []; t = b0 * BAR; prev = 76
    vs = [n for n in notes if n["sec"] == "Last Chorus" and n["line"] != "Last Chorus:8"]
    def voice_holds(t):
        return any(n["on"] < t < n["on"] + n["dur"] and n["dur"] >= BEAT for n in vs) or not any(n["on"] <= t < n["on"] + n["dur"] for n in vs)
    while t < (b0 + 16) * BAR:
        ch = M.chord_at(t); tones = sorted(p for p in range(73, 82) if p % 12 in M.CH[ch][1])
        if voice_holds(t):
            d = rng.choice([12, 12, 6, 18]) if t % BEAT == 0 else 6
            opts = [p for p in range(72, 82) if p % 12 in M.SCALE and abs(p - prev) <= 4 and (t % BEAT or p % 12 in M.CH[ch][1])
                    and not any(abs((p - h) % 12) in (1, 11) for h in held_at(t))]
            p = rng.choice(opts) if opts else min(tones, key=lambda q: abs(q - prev))
        else:
            d = BAR - t % BAR; ok_ = [q for q in tones if not any(abs((q - h) % 12) in (1, 11) for x in (0, 12, 24, 36) if x < d for h in held_at(t + x))] or tones
            p = min(ok_, key=lambda q: abs(q - prev))
        d = min(d, (t // BAR + 1) * BAR - t) if not voice_holds(t) else min(d, (b0 + 16) * BAR - t)
        out.append(dict(on=t, dur=d, p=p)); prev = p; t += d
    tog = [e for e in out if any(n["on"] == e["on"] for n in vs)]
    uni = sum(1 for e in tog if any(n["on"] == e["on"] and (e["p"] - n["p"]) % 12 == 0 for n in vs))
    tri = sum(1 for e in out if (e["p"] - M.CH[M.chord_at(e["on"])][0]) % 12 == 6)
    semi = sum(1 for e in out for h in held_at(e["on"]) if abs((e["p"] - h) % 12) in (1, 11))
    return out, dict(together=len(tog), unison_or_octave=uni, share=uni / max(1, len(tog)), tritones=tri, semitones=semi)

if __name__ == "__main__":
    rng = random.Random(SEED); drawn = set(); deaths = collections.Counter(); rows = []
    for _ in range(6000):
        r = draw(rng)
        if r is None or r in drawn: continue
        drawn.add(r); ons, steps = r; rb = rbits(ons)
        if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): deaths["rhythm band (164 via 163)"] += 1; continue
        tri = nb = ctb = 0
        for sl in SLOTS:
            for t, p in place(ons, steps, sl):
                ch = M.chord_at(t)
                if t % BEAT == 0:
                    nb += 1; ctb += p % 12 in M.CH[ch][1]
                    if (p - M.CH[ch][0]) % 12 == 6: tri += 1
                if (p - M.CH[ch][0]) % 12 == 1: tri += 1
        if tri: deaths["a tritone or flat ninth against the root"] += 1; continue
        ct = ctb / max(1, nb)
        if ct < 0.6: deaths["chord tones on the beats under 0.6"] += 1; continue
        fig = [dict(on=t, p=p) for t, p in zip(ons, pitches(steps, "D", RIFF_LO))]
        rel, ln = related_any(fig)
        if rel: deaths["related to a sung line (235, 27.31)"] += 1; continue
        dif = [b - a for a, b in zip(steps, steps[1:])]; nz = [d for d in dif if d]
        if not any((x > 0) != (y > 0) for x, y in zip(nz, nz[1:])): deaths["no contour of its own (no turn)"] += 1; continue
        sync = sum(1 for t in ons if t % BEAT) / len(ons)
        score = 0.35 * ct + 0.2 * min(1, sync / 0.5) + 0.15 * (1 if max(abs(d) for d in dif) >= 3 else 0.4) + 0.1 * (len(ons) in (4, 5, 6)) \
                - 0.1 * sum(1 for d in dif if d == 0) - 0.05 * abs(rb - 2.2) + 0.1 * (pitches(steps, "D", RIFF_LO)[-1] % 12 in M.CH["D"][1])
        rows.append(dict(score=round(score, 4), ons=ons, steps=steps, rbits=rb, ct=ct, sync=sync))
    rows.sort(key=lambda x: (-x["score"], x["ons"], x["steps"])); best = rows[0]
    print(f"intro tune: {len(drawn)} distinct drawn, {len(rows)} pass")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("pick", best)
    rng2 = random.Random(SEED + 1); sdeaths = 0
    for ks in range(800):
        ev = solo(rng2, best["ons"], best["steps"])
        if ev is None: sdeaths += 1; continue
        chk = solo_ok(ev)
        if chk["ok"]: break
        sdeaths += 1
    print(f"solo: draw {ks + 1} passed ({sdeaths} failed before it):", {a: (round(b, 3) if isinstance(b, float) else b) for a, b in chk.items()}, len(ev), "notes")
    rng3 = random.Random(SEED + 2); G = gaps(); fills = []; fstats = collections.Counter()
    for g in G:
        if rng3.random() >= 0.70: fstats["gap left open (30%)" + ("" if g["beats"] >= 2.75 else " (short gap)")] += 1; continue
        f = None
        for _ in range(200):
            f = fill(rng3, g)
            if f: break
        el = "" if g["beats"] >= 2.75 else " (short gap)"
        if f: fills.append(dict(gap=g, notes=f)); fstats["filled" + el] += 1
        else: fstats["no fill fits" + el] += 1
    print(f"fills: {len(G)} gaps of 2+ beats;", dict(fstats))
    cm, cchk = [], dict(chosen=False, note="Q18 A: no countermelody")
    pickle.dump(dict(pick=best, rows=rows[:20], deaths=deaths, drawn=len(drawn), passed=len(rows), slots=SLOTS, seed=SEED, solo=ev, solo_check=chk,
                     solo_draws=ks + 1, gaps=G, fills=fills, fill_stats=dict(fstats), counter=cm, counter_check=cchk,
                     code_sha=hashlib.sha1(open(__file__, "rb").read()).hexdigest()[:12]), open("/home/claude/p40/riff_p40.pkl", "wb"))
