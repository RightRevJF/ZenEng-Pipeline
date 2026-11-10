"""Windows Down: the instrumental hook (209) and the guitar solo, searched against the pick.
The hook: a one-bar lead-guitar figure, its rhythm drawn from the class's rhythm table (RT), chord tones on the beats, a contour of its
own, not related to the vocal hook by 27.31's test. It sounds in the intro (eight times), in the holds after chorus lines where two
beats or more are free (never over a sung onset), and in the outro (seven times). Gated as a lead (164): the class's rhythm band, chord
tones on the beats, no semitone against a held sung note, above the voice (from A4), no tritone or flat ninth against a root.
The solo (16 bars over the chorus chords): the hook stated, answered, then developed by the same walk the voice uses, in the guitar's
register, gated as a lead (the rhythm band, chord tones on the beats, no tritone against a root on a beat), its last note the tonic.
No corpus on file separates instrumental figures from the voice, so 209 has no kept figure behind it.
Usage: PYTHONHASHSEED=0 python3 riff_p37.py      (seeds: the melody's + 1 for the hook, + 2 for the solo)"""
import sys, math, random, pickle, hashlib, collections
import numpy as np
sys.argv = [sys.argv[0], "1", "main"]; sys.path[:0] = ["/home/claude/p37"]
import melody_p37 as P
M = P.M; BAR, BEAT = P.BAR, P.BEAT
D = pickle.load(open("/home/claude/p37/melody_main.pkl", "rb")); pick = D["alive"][0]; notes = pick["notes"]
SEED = D["rerun"]["seed"] + 1
DEGS = sorted(p for p in range(48, 100) if p % 12 in M.SCALE)
def pitches(steps, ch, base_lo=69):
    root = M.CH[ch][0]; start = min(p for p in DEGS if p >= base_lo and p % 12 == root)
    i0 = DEGS.index(start); return [DEGS[i0 + s] for s in steps]
def draw(rng):
    t = rng.choice([0, 0, 6]); ons = [t]
    while True:
        ds = [d for d in range(3, 25, 3) if t + d < BAR]
        if not ds: break
        ws = [M.RT[t % BAR][d] for d in ds]
        d = rng.choices(ds, ws)[0]
        if t + d >= BAR - 3 or (len(ons) >= 4 and rng.random() < 0.22): break
        t += d; ons.append(t)
    if not 4 <= len(ons) <= 7: return None
    steps = [0]
    for _ in range(len(ons) - 1): steps.append(steps[-1] + rng.choice([-3, -2, -1, 1, 2, 3, 4, -4, 0]))
    if not 3 <= max(steps) - min(steps) <= 7: return None
    return tuple(ons), tuple(steps)
def rbits(ons):
    seq = list(ons) + [BAR]
    return float(np.mean([-math.log2(max(1e-9, M.RT[a % BAR][min(96, b - a)])) for a, b in zip(seq, seq[1:])]))
SLOTS = [dict(where="intro", at=b * BAR, end=(b + 1) * BAR) for b in range(P.BAR0["Intro"], P.BAR0["Intro"] + 8)]
for s in ("Chorus 1", "Chorus 2", "Last Chorus"):
    for i in range(8):
        ln = [n for n in notes if n["line"] == f"{s}:{i}"]; nx = [n for n in notes if n["on"] > ln[-1]["on"]]
        a = ln[-1]["on"]; b = nx[0]["on"] if nx else P.BAR0["Outro"] * BAR
        if s == "Last Chorus" and i == 7: continue                       # the last line runs into the outro, which plays the hook
        at = (a + BEAT) // BEAT * BEAT
        if b - at >= BEAT * 2: SLOTS.append(dict(where=f"{s} {i + 1}", at=at, end=min(b - 6, at + BAR)))
SLOTS += [dict(where="outro", at=b * BAR, end=(b + 1) * BAR) for b in range(P.BAR0["Outro"], P.BAR0["Outro"] + 7)]
def place(ons, steps, sl):
    ch = M.chord_at(sl["at"]); ps = pitches(steps, ch)
    return [(sl["at"] + t, p) for t, p in zip(ons, ps) if sl["at"] + t < sl["end"]]
def held_at(t): return [n["p"] for n in notes if n["on"] <= t < n["on"] + n["dur"]]
_c1 = [n for n in notes if n["sec"] == "Chorus 1"]; _h = P.line_start("Chorus 1", 0)
HOOK_UNITS = [M.unit(_c1, _h - BEAT, BAR), M.unit(_c1, _h, BAR), M.unit(_c1, _h + BAR, BAR)]

def solo(rng, rons, rsteps):
    """16 bars over the chorus chords: bars 1-2 the hook and its answer an octave's worth higher; bars 3-14 a walked line (mostly eighths and
    quarters from the rhythm table, the walk's chord term); bars 15-16 the hook again, landing on A."""
    b0 = P.BAR0["Solo"]; out = []
    for k, sh in ((0, 0), (1, 2)):
        for t, p in zip(rons, pitches(tuple(s + sh for s in rsteps), M.chord_at((b0 + k) * BAR))): out.append([(b0 + k) * BAR + t, p])
    t = (b0 + 2) * BAR; prev = out[-1][1]; run = 1; last_iv = None
    P.AIM = P.Aim(P.draw_targets(random.Random(1)) if False else pick["meta"]["targets"])
    while t < (b0 + 14) * BAR:
        pos = t % BAR; ds = [d for d in (3, 6, 9, 12, 18, 24) if t + d <= (b0 + 14) * BAR]
        d = rng.choices(ds, [M.RT[pos][d] * {3: 0.3, 6: 1.3, 9: 0.6, 12: 1.6, 18: 1.2, 24: 1.0}[d] for d in ds])[0]   # a singing line, not a shred
        n = dict(on=t); ch = M.chord_at(t)
        mu = 72 + 4 * math.sin(math.pi * (t - (b0 + 2) * BAR) / (12 * BAR))       # the line rises to the middle of the solo and comes back
        p = P.next_pitch(rng, prev, run, n, ch, mu, 64, 81, last_iv)
        if p is None: return None
        run = run + 1 if p == prev else 1; last_iv = p - prev; prev = p; out.append([t, p]); t += d
    for k in (14, 15):
        for tt, p in zip(rons, pitches(rsteps, M.chord_at((b0 + k) * BAR))): out.append([(b0 + k) * BAR + tt, p])
    out[-1][1] = min((p for p in range(64, 82) if p % 12 == M.TONIC), key=lambda p: abs(p - out[-1][1]))
    ev = []
    for j, (t, p) in enumerate(out):
        nxt = out[j + 1][0] if j + 1 < len(out) else (b0 + 16) * BAR
        ev.append(dict(on=t, dur=max(3, nxt - t), p=p))
    return ev
def solo_ok(ev):
    nb = ct = tr = 0
    for e in ev:
        ch = M.chord_at(e["on"])
        if e["on"] % BEAT == 0:
            nb += 1; ct += e["p"] % 12 in M.CH[ch][1]; tr += (e["p"] - M.CH[ch][0]) % 12 == 6
    ons = [e["on"] for e in ev] + [(P.BAR0["Solo"] + 16) * BAR]
    rb = float(np.mean([-math.log2(max(1e-9, M.RT[a % BAR][min(96, b - a)])) for a, b in zip(ons, ons[1:])]))
    mx = max(abs(b["p"] - a["p"]) for a, b in zip(ev, ev[1:]))
    return dict(ct=ct / nb, tritones=tr, rbits=rb, max_leap=mx, ok=ct / nb >= 0.6 and tr == 0 and M.RBAND["p05"] <= rb <= M.RBAND["p95"] and mx <= 12)

if __name__ == "__main__":
    rng = random.Random(SEED); drawn = set(); deaths = collections.Counter(); rows = []
    for _ in range(4000):
        r = draw(rng)
        if r is None or r in drawn: continue
        drawn.add(r); ons, steps = r; rb = rbits(ons)
        if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): deaths["rhythm band (164 via 163)"] += 1; continue
        semi = tri = 0; nb = ctb = 0; low = 99
        for sl in SLOTS:
            for t, p in place(ons, steps, sl):
                ch = M.chord_at(t); low = min(low, p)
                if any(abs((p - h) % 12) in (1, 11) for h in held_at(t)): semi += 1
                if t % BEAT == 0:
                    nb += 1; ctb += p % 12 in M.CH[ch][1]
                    if (p - M.CH[ch][0]) % 12 == 6: tri += 1
                if (p - M.CH[ch][0]) % 12 == 1: tri += 1
        if semi: deaths["a semitone against a held sung note"] += 1; continue
        if tri: deaths["a tritone or flat ninth against the root"] += 1; continue
        if low < 69: deaths["below A4 (the voice's top is F#4)"] += 1; continue
        ct = ctb / max(1, nb)
        if ct < 0.6: deaths["chord tones on the beats under 0.6"] += 1; continue
        fig = [dict(on=t, p=p) for t, p in zip(ons, pitches(steps, "A"))]
        rels = [M.related(M.unit(fig, 0, BAR), u) for u in HOOK_UNITS]; rel = max(rels, key=lambda x: (x[0], x[1] + x[2]))
        if rel[0]: deaths["related to the vocal hook (27.31)"] += 1; continue
        dif = [b - a for a, b in zip(steps, steps[1:])]; nz = [d for d in dif if d]
        if not any((x > 0) != (y > 0) for x, y in zip(nz, nz[1:])): deaths["no contour of its own (no turn)"] += 1; continue
        sync = sum(1 for t in ons if t % BEAT) / len(ons)
        score = 0.35 * ct + 0.2 * min(1, sync / 0.5) + 0.15 * (1 if max(abs(d) for d in dif) >= 3 else 0.4) + 0.1 * (len(ons) in (4, 5, 6)) \
                - 0.1 * sum(1 for d in dif if d == 0) - 0.05 * abs(rb - 2.2) + 0.1 * (pitches(steps, "A")[-1] % 12 in M.CH["A"][1])
        rows.append(dict(score=round(score, 4), ons=ons, steps=steps, rbits=rb, ct=ct, sync=sync, related=rel))
    rows.sort(key=lambda x: (-x["score"], x["ons"], x["steps"])); best = rows[0]
    print(f"instrumental hook: {len(drawn)} distinct drawn, {len(rows)} pass; slots {len(SLOTS)}")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("pick", best)
    rng2 = random.Random(SEED + 1); sdeaths = 0
    for k in range(500):
        ev = solo(rng2, best["ons"], best["steps"])
        if ev is None: sdeaths += 1; continue
        chk = solo_ok(ev)
        if chk["ok"]: break
        sdeaths += 1
    print(f"solo: draw {k + 1} passed ({sdeaths} failed before it):", {a: (round(b, 3) if isinstance(b, float) else b) for a, b in chk.items()}, len(ev), "notes")
    pickle.dump(dict(pick=best, rows=rows[:20], deaths=deaths, drawn=len(drawn), passed=len(rows), slots=SLOTS, seed=SEED, solo=ev, solo_check=chk,
                     solo_draws=k + 1, code_sha=hashlib.sha1(open(__file__, "rb").read()).hexdigest()[:12]), open("/home/claude/p37/riff_p37.pkl", "wb"))
