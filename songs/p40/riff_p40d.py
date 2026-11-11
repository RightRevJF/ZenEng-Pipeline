"""Nothing Else on Earth, made for real: the mandolin riff (the writer's Q27 A), the electric guitar's chorus fills and the riff break's
solo, against the final melody (melody_final_d.pkl).
  The riff: driving picked eighths. A melody line on top (4-7 onsets on the eighth grid, its rhythm from the class's rhythm table, chord
  tones on the beats, a contour with a turn, D mixolydian over C), and on every eighth an open string beneath it, D4 and A4 in turn: the
  drone. Placed on each chord of D C G D, the top from G4 up. It must be unrelated by 27.31's test to every sung line's opening bar.
  Where: the intro's eight bars (alone for four), verse bars 1-8 (the riff's changes), the riff break's first and last two bars under
  the solo, the outro's first three bars.
  The fills (235/272): electric guitar, in the voice's gaps inside the band's sections only (choruses, last chorus); the verses keep
  the mandolin.
  The solo: electric guitar, 8 bars over D C G D twice: the riff's top line, its answer a step up, a walked line, the riff again.
Usage: PYTHONHASHSEED=0 python3 riff_p40d.py"""
import sys, math, random, pickle, hashlib, collections
import numpy as np
sys.argv = [sys.argv[0], "1", "design"]; sys.path[:0] = ["/home/claude/p40"]
import melody_p40d as P
import riff_p40 as RV0
M = P.M; BAR, BEAT = P.BAR, P.BEAT
F = pickle.load(open("/home/claude/p40/melody_final_d.pkl", "rb")); pick = F["pick"]; notes = pick["notes"]
for _p in ("V", "C"): P.KNOBS[_p].update(F["run"]["knobs"][_p])
RV0.notes[:] = notes; RV0.pick = pick; RV0.P = P
SEED = F["run"]["rerun"]["seed"] + 11
MIXO = (M.SCALE - {1}) | {0}
TOP_LO = 67
def pitches(steps, ch, base_lo=TOP_LO):
    dg = sorted(p for p in range(40, 100) if p % 12 in (MIXO if ch == "C" else M.SCALE))
    root = M.CH[ch][0]; start = min(p for p in dg if p >= base_lo and p % 12 == root); i0 = dg.index(start)
    return [dg[i0 + s] for s in steps]
def draw(rng):
    t = rng.choice([0, 0, 6]); ons = [t]
    while True:
        ds = [d for d in (6, 12, 18, 24) if t + d < BAR]
        if not ds: break
        d = rng.choices(ds, [M.RT[t % BAR][d] for d in ds])[0]
        if t + d >= BAR - 6 or (len(ons) >= 4 and rng.random() < 0.22): break
        t += d; ons.append(t)
    if not 4 <= len(ons) <= 7: return None
    steps = [0]
    for _ in range(len(ons) - 1): steps.append(steps[-1] + rng.choice([-3, -2, -1, 1, 2, 3, 4, -4, 0]))
    if not 3 <= max(steps) - min(steps) <= 7: return None
    return tuple(ons), tuple(steps)
B0 = P.BAR0
RIFF_BARS = [("intro", b) for b in range(B0["Intro"], B0["Intro"] + 8)] + [("verse 1", b) for b in range(B0["Verse 1"], B0["Verse 1"] + 8)] + \
            [("verse 2", b) for b in range(B0["Verse 2"], B0["Verse 2"] + 8)] + [("riff break", b) for b in (B0["Riff break"], B0["Riff break"] + 1, B0["Riff break"] + 6, B0["Riff break"] + 7)] + \
            [("outro", b) for b in range(B0["Outro"], B0["Outro"] + 3)]
def place(ons, steps, b):
    """the riff in one bar: the top line on its onsets, an open string (D4, A4 in turn) on every eighth."""
    ch = P.CHORD[b]; ps = pitches(steps, ch); top = dict(zip(ons, ps)); out = []
    for k, t in enumerate(range(0, BAR, 6)):
        dr = 62 if k % 2 == 0 else 69
        out.append(dict(on=b * BAR + t, dur=6, p=sorted({dr} | ({top[t]} if t in top else set())), top=top.get(t)))
    return out
if __name__ == "__main__":
    rng = random.Random(SEED); drawn = set(); deaths = collections.Counter(); rows = []
    for _ in range(6000):
        r = draw(rng)
        if r is None or r in drawn: continue
        drawn.add(r); ons, steps = r; rb = RV0.rbits(ons)
        if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): deaths["rhythm band (164 via 163)"] += 1; continue
        tri = nb = ctb = 0
        for b in sorted({b for _, b in RIFF_BARS}):
            ch = P.CHORD[b]
            for t, p in zip(ons, pitches(steps, ch)):
                if t % BEAT == 0:
                    nb += 1; ctb += p % 12 in M.CH[ch][1]
                    if (p - M.CH[ch][0]) % 12 == 6: tri += 1
                if (p - M.CH[ch][0]) % 12 == 1: tri += 1
        if tri: deaths["a tritone or flat ninth against the root"] += 1; continue
        ct = ctb / max(1, nb)
        if ct < 0.6: deaths["chord tones on the beats under 0.6"] += 1; continue
        fig = [dict(on=t, p=p) for t, p in zip(ons, pitches(steps, "D"))]
        if RV0.related_any(fig)[0]: deaths["related to a sung line (235, 27.31)"] += 1; continue
        dif = [b - a for a, b in zip(steps, steps[1:])]; nz = [d for d in dif if d]
        if not any((x > 0) != (y > 0) for x, y in zip(nz, nz[1:])): deaths["no contour of its own (no turn)"] += 1; continue
        sync = sum(1 for t in ons if t % BEAT) / len(ons)
        score = 0.35 * ct + 0.2 * min(1, sync / 0.5) + 0.15 * (1 if max(abs(d) for d in dif) >= 3 else 0.4) + 0.1 * (len(ons) in (5, 6)) \
                - 0.1 * sum(1 for d in dif if d == 0) - 0.05 * abs(rb - 2.2) + 0.1 * (pitches(steps, "D")[-1] % 12 in M.CH["D"][1])
        rows.append(dict(score=round(score, 4), ons=ons, steps=steps, rbits=rb, ct=ct, sync=sync))
    rows.sort(key=lambda x: (-x["score"], x["ons"], x["steps"])); best = rows[0]
    print(f"mandolin riff: {len(drawn)} distinct drawn, {len(rows)} pass"); [print(f"   {v:5d}  {k}") for k, v in deaths.most_common()]
    print("pick", best, "top line over D:", pitches(best["steps"], "D"))
    mand = [e for where, b in RIFF_BARS for e in place(best["ons"], best["steps"], b)]
    for e, (where, b) in zip(mand, [(w, b) for w, b in RIFF_BARS for _ in range(8)]): e["where"] = where
    # the solo (electric guitar): song 38's method, its first two and last two bars the riff's top line an octave up
    RV0.P.BAR0 = dict(P.BAR0)
    rng2 = random.Random(SEED + 1); sd = 0
    for ks in range(800):
        ev = RV0.solo(rng2, best["ons"], best["steps"])
        if ev is None: sd += 1; continue
        chk = RV0.solo_ok(ev)
        if chk["ok"]: break
        sd += 1
    print(f"solo: draw {ks + 1} passed:", {a: (round(b, 3) if isinstance(b, float) else b) for a, b in chk.items()}, len(ev), "notes")
    # fills: only in the band's sections
    BAND = ("Chorus 1", "Chorus 2", "Last Chorus")
    rng3 = random.Random(SEED + 2); G = [g for g in RV0.gaps() if g["after"].split(":")[0] in BAND]; fills = []; fstats = collections.Counter()
    for g in G:
        el = "" if g["beats"] >= 2.75 else " (short gap)"
        if rng3.random() >= 0.70: fstats["gap left open (30%)" + el] += 1; continue
        f = None
        for _ in range(200):
            f = RV0.fill(rng3, g)
            if f: break
        if f: fills.append(dict(gap=g, notes=f)); fstats["filled" + el] += 1
        else: fstats["no fill fits" + el] += 1
    print(f"fills: {len(G)} gaps in the choruses;", dict(fstats))
    pickle.dump(dict(pick=best, rows=rows[:20], deaths=deaths, drawn=len(drawn), passed=len(rows), bars=RIFF_BARS, mandolin=mand, seed=SEED, solo=ev, solo_check=chk,
                     gaps=G, fills=fills, fill_stats=dict(fstats), code_sha=hashlib.sha1(open(__file__, "rb").read()).hexdigest()[:12]),
                open("/home/claude/p40/riff_p40d.pkl", "wb"))
