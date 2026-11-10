"""Swallowed Up -- the solo, searched over the frozen riff (ZenEng v78, 9-M.10a: in a song whose voice is harsh throughout the search
writes only the pitched leads). Sixteen bars at q = 200 over riff D, i-bVII-bVI-V (B5 A5 G5 F#5, two bars a chord, twice).
  The lead: B natural minor, with b2 (C) and b5 (F) as inflections (9-M.4) and A# over F#5 (the leading tone); sounding F#3-B5.
  Eight two-bar phrases by a cell plan, A A' B A'' | C C' D E: the motif, its answers moved to the chord, a climb that gets denser,
  the summit in phrase 7, and phrase 8 a cadence onto A# or F# over F#5, resolving to B at the slowdown.
  Gates: range; leaps of an octave at most; the bar downbeats on chord tones in at least 40% of bars (fix 134's floor, read on the
  lead); the declared design clause THE SUMMIT ONCE (fix 133: a clause binds when the design declares it), in phrase 7.
  9-M.10b: the tritone filter, the consonance and spectral gates do not read this class's material; realness prints OUT OF
  CALIBRATION (no metal corpus on file) and ranks nothing. The composite ranks the survivors on IC, CMP and the memory horizon.
  The rerun record names the seed, N, the code's hash, the library versions and PYTHONHASHSEED (fix 145)."""
import sys, os, json, pickle, random, hashlib, collections, platform
import numpy as np
sys.path[:0] = ["/home/claude/p34", "/home/claude/carol", "/home/claude/pop"]
from measures import cmp_score, m_horizon, PPM, ic_profile, feature_vec, intervals
import riffs_p34 as R
TCAL = 11
PPMM = pickle.load(open("/home/claude/pop/pop_ppm.pkl", "rb"))
CAL = json.load(open("/home/claude/pop/pop_calibration.json")); MU, SD = np.array(CAL["mu"]), np.array(CAL["sd"]); ZREF = np.array(CAL["Z"]); REAL_KNN = CAL["real_knn"]
B0 = R.SEC_FIRST["Solo"]
CHORDS = [0, 0, 10, 10, 8, 8, 7, 7] * 2                    # offsets from B: B A G F#
CT = {0: {11, 2, 6}, 10: {9, 1, 4}, 8: {7, 11, 2}, 7: {6, 10, 1}}      # chord tones (the third the guitars omit, carried by the lead)
SCALE = {11, 1, 2, 4, 6, 7, 9}
LO, HI = 59, 83
CEIL = 76                                                  # the plan lowers the ceiling outside phrase 7 (fix 143's way: met by construction)
RHY = {"q": [4, 4, 4, 4], "e": [2] * 8, "ee4": [2, 2, 4, 2, 2, 4], "run": [1, 1, 1, 1, 2, 2, 4, 4], "shred": [1] * 16,
       "long": [6, 2, 4, 4], "hold": [8, 4, 4], "end": [4, 12], "trip": [2, 1, 1, 2, 1, 1, 4, 4]}
PLAN = ["A", "A'", "B", "A''", "C", "C'", "D", "E"]
DENS = {"A": ["ee4", "long", "e"], "B": ["e", "ee4", "trip"], "C": ["run", "trip", "e"], "D": ["shred", "run"], "E": ["hold", "end"]}

def pcs(b): return CT[CHORDS[b]]
def allowed(b):
    s = set(SCALE)
    if CHORDS[b] == 7: s = (s - {9}) | {10}                  # A# over F#5
    return s
def near(p, pcset, lo=LO, hi=HI):
    c = [q for q in range(lo, hi + 1) if q % 12 in pcset]
    return min(c, key=lambda q: (abs(q - p), q))

def phrase(rng, kind, start_p, bars, motif=None):
    """two bars of (slot, dur, pitch) relative to the phrase."""
    out = []
    if motif is not None and kind.startswith(("A", "C")) and kind not in ("A", "C"):
        # an answer: the motif's rhythm and contour moved to this chord, its last bar varied
        shift = None
        for s, d, p in motif:
            b = bars[0] + s // 16
            q = p + (shift if shift is not None else 0)
            if shift is None:                                  # the octave nearest the last note (no leap at the join)
                tgt = near(p, pcs(b)); shift = tgt - p
                shift = min((shift + 12 * k for k in (-1, 0, 1)), key=lambda x: abs(p + x - start_p)); q = p + shift
            if q % 12 not in allowed(b): q = near(q, allowed(b))
            if s >= 16 and rng.random() < 0.5: q = near(q + rng.choice([-2, -1, 1, 2, 3]), allowed(b))
            out.append((s, d, q))
        while max(q for _, _, q in out) > CEIL: out = [(s, d, q - 12) for s, d, q in out]       # an answer too high moves down an octave
        while min(q for _, _, q in out) < LO: out = [(s, d, q + 12) for s, d, q in out]
        return out
    fam = kind[0]; pos = 0; p = start_p
    for half in range(2):
        rh = RHY[rng.choice(DENS[fam])] if not (fam == "E" and half == 1) else RHY["end"]
        b = bars[half]
        for k, d in enumerate(rh):
            s = half * 16 + sum(rh[:k])
            strong = s % 8 == 0
            if fam == "E" and half == 1 and k == len(rh) - 1:
                q = near(p, {10, 6}); out.append((s, d, q)); continue
            step = rng.choices([-4, -3, -2, -1, 1, 2, 3, 4, 5, 7, -5, -7], [2, 3, 8, 6, 6, 8, 3, 2, 1, .5, 1, .5])[0]
            if fam in ("C", "D"): step = abs(step) if rng.random() < 0.62 else step
            q = p + step
            hi = HI if fam == "D" else CEIL
            if fam == "D" and k >= len(rh) - 4 and half == 0: q = max(q, p + 1)      # the climb into the summit
            if q > hi or q < LO: q = p - step
            pool = pcs(b) if strong and rng.random() < 0.85 else allowed(b)
            if not strong and rng.random() < 0.06: pool = pool | {0, 5}          # b2, b5 inflections
            q = near(q, pool, LO, hi)
            if len(out) >= 2 and q == out[-1][2] == out[-2][2]:                 # the monotony floor, built into the fill (v77)
                q = near(q + rng.choice([-2, 2, 3, -3]), pool, LO, hi)
            out.append((s, d, q)); p = q
    return out

def generate(rng):
    notes = []; motif = None; p = rng.choice([66, 71, 74])
    for ph, kind in enumerate(PLAN):
        bars = [2 * ph, 2 * ph + 1]
        src = motif if kind in ("A'", "A''") else (cmot if kind == "C'" else None)
        ns = phrase(rng, kind, p, bars, src)
        if kind == "A": motif = ns
        if kind == "C": cmot = ns
        notes += [(32 * ph + s, d, q) for s, d, q in ns]; p = ns[-1][2]
    return notes

def evaluate(ns):
    ps = [p for _, _, p in ns]
    if min(ps) < LO or max(ps) > HI: return ("range", (min(ps), max(ps))), None
    iv = [b - a for a, b in zip(ps, ps[1:])]
    if max(abs(x) for x in iv) > 12: return ("leap", max(abs(x) for x in iv)), None
    run = 1
    for a, b in zip(ps, ps[1:]):
        run = run + 1 if a == b else 1
        if run > 3: return ("monotony", a), None
    for ph in range(8):
        if len({p for s, d, p in ns if s // 32 == ph}) < 4 and ph != 7: return ("monotony: fewer than four pitches in a phrase", ph + 1), None
    down = [n for n in ns if n[0] % 16 == 0]
    ctshare = sum(1 for s, d, p in down if p % 12 in pcs(s // 16)) / max(1, len(down))
    if ctshare < 0.40: return ("chord-tone floor (134)", round(ctshare, 2)), None
    top = max(ps); at = [s for s, d, p in ns if p == top]
    if len(at) != 1 or not (6 * 32 <= at[0] < 7 * 32): return ("design clause: the summit once, in phrase 7 (133)", (len(at), at[0] // 32 + 1)), None
    if ps[-1] % 12 not in (10, 6): return ("cadence onto A# or F#", ps[-1] % 12), None
    m = [(s / 4.0, d / 4.0, p) for s, d, p in ns]
    cmp_, _ = cmp_score(m, 4, TCAL)
    hook = [x for x in m if x[0] < 16]; rest = [x for x in m if x[0] >= 16]
    mh, _, _ = m_horizon(hook, rest)
    bits = PPMM.bits(PPM.symbols(m, TCAL))
    ic, _ = ic_profile(bits, ps.index(top))
    fv = (feature_vec(m, TCAL, 4) - MU) / SD
    dist = np.sort(np.sqrt(((ZREF - fv) ** 2).sum(1)))[:10].mean()
    real = sum(1 for x in REAL_KNN if x >= dist) / len(REAL_KNN)
    comp = 0.35 * ic + 0.35 * min(1.0, cmp_ / 0.6) + 0.30 * min(1.0, mh)
    return None, dict(composite=round(comp, 4), IC=round(ic, 3), CMP=round(cmp_, 3), M_horizon=round(mh, 3), realness_out_of_calibration=round(real, 3),
                      chord_tone_downbeats=round(ctshare, 2), top=top, top_bar=at[0] // 16 + 1, n=len(ns), lo=min(ps))

def fp(ns): return hashlib.sha1(json.dumps(ns).encode()).hexdigest()[:12]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    SEED = 20261110 + 34
    rng = random.Random(SEED); made, deaths, alive, tries = 0, collections.Counter(), [], 0
    while made < N and tries < N * 40:
        tries += 1; ns = generate(rng); made += 1
        err, m = evaluate(ns)
        if err: deaths[err[0]] += 1; continue
        alive.append(dict(notes=ns, meas=m, fp=fp(ns)))
    alive.sort(key=lambda c: (-c["meas"]["composite"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    print(f"built {made}, survivors {len(alive)} ({100 * len(alive) / made:.1f}%), order frozen {order}")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    for c in alive[:6]: print(c["fp"], c["meas"])
    code = hashlib.sha1(open(__file__, "rb").read() + open("/home/claude/p34/riffs_p34.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, N=N, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(), numpy=np.__version__,
                 riffs_sha=pickle.load(open("/home/claude/p34/riffs_frozen.pkl", "rb"))["sha"],
                 cmd=f"PYTHONHASHSEED={os.environ.get('PYTHONHASHSEED')} python3 solo_p34.py {N}")
    print("rerun:", rerun)
    pickle.dump(dict(alive=alive[:40], top20=[c["fp"] for c in alive[:20]], deaths=deaths, made=made, survivors=len(alive), order_fp=order, rerun=rerun),
                open("/home/claude/p34/solo_result.pkl", "wb"))
