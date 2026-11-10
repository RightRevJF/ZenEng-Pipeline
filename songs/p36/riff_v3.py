"""Dance Anyway, version 3: the instrumental hook (fix 209), searched against the v3 pick.
A one-bar figure for the synth: its rhythm drawn from the class's rhythm table (RT), chord tones on the beats, a contour of its own,
not related to the vocal hook by 27.31's test. It sounds in the intro (four times), in the holds and rests after chorus lines where a
beat or more is free (never over a sung onset), and in the outro. Gated as a lead (164): the class's rhythm band, chord tones on the
beats, no semitone against a held sung note, above the voice, no tritone against a chord's root on a beat. No corpus on file separates
instrumental figures from the voice, so the rule has no kept figure behind it.
Usage: PYTHONHASHSEED=0 python3 riff_v3.py     (the draw's seed is the melody's seed + 1)"""
import sys, math, random, pickle, hashlib, collections
import numpy as np
sys.argv = [sys.argv[0], "1", "main"]
sys.path[:0] = ["/home/claude/p36"]
import melody_v3_p36 as V
M = V.M; BAR, BEAT = V.BAR, V.BEAT
D = pickle.load(open("/home/claude/p36/melody_v3_main.pkl", "rb")); pick = D["alive"][0]; notes = pick["notes"]
SEED = D["rerun"]["seed"] + 1
DEGS = sorted(p for p in range(48, 96) if p % 12 in M.SCALE)
def pitches(steps, ch, base_lo=70):
    root = M.CH[ch][0]
    if root not in M.SCALE: root = next(t for t in sorted(M.CH[ch][1]) if t in M.SCALE and (t - M.CH[ch][0]) % 12 == 7)   # a borrowed chord: from its fifth
    start = min(p for p in DEGS if p >= base_lo and p % 12 == root)
    i0 = DEGS.index(start); return [DEGS[i0 + s] for s in steps]
def draw(rng):
    """onsets: a walk over the class's rhythm table from beat 1 (or its 'and'), sixteenths allowed, inside one bar."""
    t = rng.choice([0, 0, 6]); ons = [t]
    while True:
        ds = [d for d in range(3, 25, 3) if t + d < BAR]
        if not ds: break
        ws = [M.RT[t % BAR][d] for d in ds]
        if sum(ws) <= 0: break
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

# where it sounds: the intro, the holds after chorus lines (a beat or more free), the outro
SLOTS = [dict(where="intro", at=b * BAR, end=(b + 1) * BAR) for b in range(V.BAR0["Intro"], V.BAR0["Intro"] + 4)]
for s in ("Chorus 1", "Chorus 2", "Last Chorus"):
    for i in range(8):
        ln = [n for n in notes if n["line"] == f"{s}:{i}"]; nx = [n for n in notes if n["on"] > ln[-1]["on"]]
        a = ln[-1]["on"]; b = nx[0]["on"] if nx else V.BAR0["Outro"] * BAR
        at = (a + BEAT) // BEAT * BEAT                       # a beat of the hold first: the sung word is heard alone
        if b - at >= BEAT * 2: SLOTS.append(dict(where=f"{s} {i + 1}", at=at, end=min(b - 6, at + BAR)))
SLOTS += [dict(where="outro", at=b * BAR, end=(b + 1) * BAR) for b in range(V.BAR0["Outro"], V.BAR0["Outro"] + 3)]
def place(ons, steps, sl):
    ch = M.chord_at(sl["at"]); ps = pitches(steps, ch)
    return [(sl["at"] + t, p) for t, p in zip(ons, ps) if sl["at"] + t < sl["end"]]
def held_at(t):
    return [n["p"] for n in notes if n["on"] <= t < n["on"] + n["dur"]]
_c1 = [n for n in notes if n["sec"] == "Chorus 1"]; _h = V.line_start("Chorus 1", 0)
HOOK_UNITS = [M.unit(_c1, _h - BEAT, BAR), M.unit(_c1, _h, BAR), M.unit(_c1, _h + BAR, BAR)]   # the hook's bars, with and without its pickup
if __name__ == "__main__":
    rng = random.Random(SEED); drawn = set(); deaths = collections.Counter(); rows = []
    for _ in range(4000):
        r = draw(rng)
        if r is None or r in drawn: continue
        drawn.add(r); ons, steps = r
        rb = rbits(ons)
        if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): deaths["rhythm band (164 via 163)"] += 1; continue
        bad = semi = tri = 0; nb = ctb = 0; low = 99
        for sl in SLOTS:
            for t, p in place(ons, steps, sl):
                ch = M.chord_at(t); low = min(low, p)
                if any(abs((p - h) % 12) in (1, 11) for h in held_at(t)): semi += 1
                if t % BEAT == 0:
                    nb += 1; ctb += p % 12 in M.CH[ch][1]
                    if (p - M.CH[ch][0]) % 12 == 6: tri += 1
                if (p - M.CH[ch][0]) % 12 == 1: tri += 1                  # a flat ninth over the root, anywhere
        if semi: deaths["a semitone against a held sung note"] += 1; continue
        if tri: deaths["a tritone against the root on a beat"] += 1; continue
        if low < 67: deaths["below the voice's chorus (G4)"] += 1; continue
        ct = ctb / max(1, nb)
        if ct < 0.6: deaths["chord tones on the beats under 0.6"] += 1; continue
        fig = [dict(on=t, p=p) for t, p in zip(ons, pitches(steps, "Eb"))]
        rels = [M.related(M.unit(fig, 0, BAR), u) for u in HOOK_UNITS]; rel = max(rels, key=lambda r: (r[0], r[1] + r[2]))
        if rel[0]: deaths["related to the vocal hook (27.31)"] += 1; continue
        dif = [b - a for a, b in zip(steps, steps[1:])]; nz = [d for d in dif if d]
        turn = any((x > 0) != (y > 0) for x, y in zip(nz, nz[1:]))
        if not turn: deaths["no contour of its own (no turn)"] += 1; continue
        sync = sum(1 for t in ons if t % BEAT) / len(ons)
        score = 0.35 * ct + 0.2 * min(1, sync / 0.5) + 0.15 * (1 if max(abs(d) for d in dif) >= 3 else 0.4) + 0.1 * (len(ons) in (4, 5, 6)) \
                - 0.1 * sum(1 for d in dif if d == 0) - 0.05 * abs(rb - 2.2) + 0.1 * (pitches(steps, "Eb")[-1] % 12 in M.CH["Eb"][1])
        rows.append(dict(score=round(score, 4), ons=ons, steps=steps, rbits=rb, ct=ct, sync=sync, related=rel))
    rows.sort(key=lambda x: (-x["score"], x["ons"], x["steps"]))
    best = rows[0]
    print(f"instrumental hook: {len(drawn)} distinct drawn, {len(rows)} pass; slots {len(SLOTS)}")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("pick", best)
    print("slots:", [(s["where"], (s["end"] - s["at"]) // 12) for s in SLOTS])
    pickle.dump(dict(pick=best, rows=rows[:20], deaths=deaths, drawn=len(drawn), passed=len(rows), slots=SLOTS, seed=SEED,
                     code_sha=hashlib.sha1(open(__file__, "rb").read()).hexdigest()[:12]), open("/home/claude/p36/riff_v3.pkl", "wb"))
