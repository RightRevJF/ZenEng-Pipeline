"""Wood and Cloth (song 12), SECOND EDITION: the hymn tune, drawn by song 53's hymn-mode sketch (749.11) adapted to a trochaic 87 87.
D major, 3/4; quarter = 12 ticks, bar = 36; every line starts on a downbeat (trochaic: stressed syllables on downbeats).

The writer's designs (logged in intake.py):
  key D major, compass D4-E5; 'cloth' (stanzas 1 and 5, line 4 syllable 3) on E5, the tune's only E5, reached by step from D5;
  the form A B A C: line 3 repeats line 1 exactly (pitch and rhythm), so the Easter half of every pair is heard as an echo;
  the score rich within the rules (749.23): an applied dominant in every stanza where line 2 turns to its half cadence (E7, V of V)
  and under line 3 (F#7, V of vi), so line 1's tune is harmonized D Bm G A and line 3's D F#7 Bm A: the tune is drawn to fit both
  (bar 2's notes F#, C# or E only; bar 3's downbeat B or D).
Rhythm (the concern list: one rhythm in every bar; heavy monosyllables need even notes):
  line 2 bars 1 and 3 and line 4 bar 1 are two even dotted quarters (the figure under 'one stone', 'stone rolled', 'star laid'),
  the tune's one recurring figure; line 4 bar 2 holds 'cloth' on a half note; the other bars are drawn from the Open Hymnal's 3/4
  hymn bars as song 53's second edition draws them (half-quarter; two slurred quarters and a quarter; dotted quarter, eighth slurred,
  and quarter; with slurred eighths on the weak syllable), quarter-half left out (it lengthens the weak syllable in every stanza).
  An 8-syllable line ends with its 7th syllable on a half and the 8th on a quarter; a 7-syllable line holds its 7th a dotted half.
Cadences: line 2 a half cadence (a tone of A over A); line 4 C#5 to D5 on 'end' (the leading tone rising, concern 9).
Judge: charged against the 3/4 hymn quartiles (46 hymns), as song 53; pick least charge (within 0.05), then nearest the medians.
Run: python3 gen12.py 3000"""
import json, random, sys, collections, hashlib
import numpy as np
sys.path[:0] = ["/home/claude/atlas"]
import atlas_build as AB
H = "/home/claude/zeneng-pipeline/songs/p12"
T = json.load(open("/home/claude/p63/tables/essen_34.json"))
HYM = json.load(open("/home/claude/atlas/tables/hymns.json"))["by_metre"]["3/4"]
Q = HYM["readings_quartiles"]
BAR = 36
SCALE = {2, 4, 6, 7, 9, 11, 1}
CH = {"D": {2, 6, 9}, "G": {7, 11, 2}, "A": {9, 1, 4}, "A7": {9, 1, 4, 7}, "Bm": {11, 2, 6}, "Em": {4, 7, 11}, "Em7": {4, 7, 11, 2},
      "E7": {4, 8, 11, 2}, "F#7": {6, 10, 1, 4}, "F#m": {6, 9, 1}}
CHORDS = {0: ["D", "Bm", "G", "A"], 1: ["Bm", "G", "E7", "A"], 2: ["D", "F#7", "Bm", "A"], 3: ["G", "Em7", "A7", "D"]}
L1_ALSO = ["D", "F#7", "Bm", "A"]            # line 1's tune must also fit line 3's chords
LOW, HIGH = 62, 74
IV = {int(k): v for k, v in T["intervals"].items()}; IVT = sum(IV.values())
def ivp(d): return (IV.get(max(-12, min(12, d)), 0) + 0.5) / IVT
EVEN = [(0, 18, 0, False), (18, 18, 1, False)]
PATTERNS = {
    "half-quarter": ([(0, 24, 0, False), (24, 12, 1, False)], 372),
    "quarters slurred-quarter": ([(0, 12, 0, True), (12, 12, 0, False), (24, 12, 1, False)], 0.4 * 264),
    "dotted quarter-eighth slurred-quarter": ([(0, 18, 0, True), (18, 6, 0, False), (24, 12, 1, False)], 62),
    "dotted quarter-eighth slurred-eighths slurred": ([(0, 18, 0, True), (18, 6, 0, False), (24, 6, 1, True), (30, 6, 1, False)], 27),
    "half-eighths slurred": ([(0, 24, 0, False), (24, 6, 1, True), (30, 6, 1, False)], 22),
    "quarters slurred-eighths slurred": ([(0, 12, 0, True), (12, 12, 0, False), (24, 6, 1, True), (30, 6, 1, False)], 16)}
FIXED = {(1, 0): EVEN, (1, 2): EVEN, (3, 0): EVEN, (3, 1): PATTERNS["half-quarter"][0]}
def rhythm_line(rng, li):
    n = [8, 7, 8, 7][li]; b0 = 4 * li; out = []; slurs = 0; kinds = []
    for b in range(3):
        if (li, b) in FIXED: pat = FIXED[(li, b)]; kinds.append("fixed")
        else:
            names = [p for p in PATTERNS if not (slurs >= 2 and any(x[3] for x in PATTERNS[p][0]))]
            k = rng.choices(names, weights=[PATTERNS[p][1] for p in names])[0]; pat = PATTERNS[k][0]; kinds.append(k)
        slurs += sum(1 for x in pat if x[3])
        for off, d, which, sl in pat: out.append(((b0 + b) * BAR + off, d, 2 * b + which, which == 0, sl))
    if n == 8: out += [((b0 + 3) * BAR, 24, 6, True, False), ((b0 + 3) * BAR + 24, 12, 7, False, False)]
    else: out.append(((b0 + 3) * BAR, 36, 6, True, False))
    return out
def ok_pc(p, ch, li, b, strong):
    pc = p % 12
    if pc not in SCALE and not (pc == 8 and ch == "E7"): return False
    if pc == 1 and ch not in ("A", "A7", "F#7", "F#m") and strong: return False
    if li == 0 and b == 1 and pc not in {6, 1, 4}: return False                 # fits Bm (line 1) and F#7 (line 3)
    if li == 0 and strong and b == 2 and pc not in {11, 2}: return False       # fits G and Bm
    if li == 0 and strong and pc not in CH[L1_ALSO[b]]: return False
    return True
def draw_line(rng, rh, li, prev, rule):
    ps = []
    for j, (on, d, k, st, sl) in enumerate(rh):
        b = (on // BAR) % 4; ch = CHORDS[li][b]; ct = CH[ch]; strong = on % BAR == 0
        if j in rule.get("pin", {}): ps.append(rule["pin"][j]); continue
        lo, hi = rule.get("lo", LOW), rule.get("hi", HIGH)
        cands = [p for p in range(lo, hi + 1) if ok_pc(p, ch, li, b, strong)]
        if strong: cands = [p for p in cands if p % 12 in ct]
        if j == len(rh) - 1 and "end" in rule: cands = [p for p in cands if p % 12 in rule["end"]]
        if not cands: return None
        ref = ps[-1] if ps else prev
        w = [ivp(p - ref) * ((6.0 if p % 12 in ct else 0.05) if strong else (1.5 if p % 12 in ct else 1.0)) for p in cands]
        if j and rh[j - 1][4]:
            keep = [(x, p) for x, p in zip(w, cands) if 1 <= abs(p - ref) <= 2]
            if not keep: return None
            w, cands = [x for x, _ in keep], [p for _, p in keep]
        if j and not strong and not rh[j - 1][4] and (p := None) is None:
            # a weak-beat non-chord tone must be approached and left by step: approach checked here, departure below
            keep = [(x, q) for x, q in zip(w, cands) if q % 12 in ct or 1 <= abs(q - ref) <= 2]
            if not keep: return None
            w, cands = [x for x, _ in keep], [q for _, q in keep]
        ps.append(rng.choices(cands, weights=w)[0])
    for j in range(1, len(ps) - 1):
        on = rh[j][0]; b = (on // BAR) % 4; ch = CHORDS[li][b]
        if on % BAR and ps[j] % 12 not in CH[ch] and not (1 <= abs(ps[j + 1] - ps[j]) <= 2): return None
    if any(abs(b2 - a) > 7 for a, b2 in zip(ps, ps[1:])): return None
    if any(ps[k] == ps[k + 1] == ps[k + 2] == ps[k + 3] for k in range(len(ps) - 3)): return None
    return ps
def build(rng):
    lines = []; prev = 66
    for li in range(4):
        if li == 2:
            lines.append([dict(n, on=n["on"] + 8 * BAR, line=2) for n in lines[0]]); prev = lines[0][-1]["p"]; continue
        rh = rhythm_line(rng, li); rule = {}
        if li == 0: rule = {"lo": 62, "hi": 74}
        if li == 1: rule = {"lo": 62, "hi": 74, "end": {9, 1, 4}}
        if li == 3:
            cl = next(j for j, x in enumerate(rh) if x[2] == 2); an = next(j for j, x in enumerate(rh) if x[2] == 1)
            th = next(j for j, x in enumerate(rh) if x[2] == 5 and x[0] % BAR == 0) if any(x[2] == 5 and x[0] % BAR == 0 for x in rh) else \
                 next(j for j, x in enumerate(rh) if x[2] == 5)
            rule = {"lo": 66, "hi": 76, "pin": {an: 74, cl: 76, len(rh) - 2: 73, len(rh) - 1: 74}}
        ps = None
        for _ in range(40):
            ps = draw_line(rng, rh, li, prev, rule)
            if ps is None: continue
            if li in (0, 1) and max(ps) > 74: ps = None; continue
            if li == 3 and sum(p == 76 for p in ps) != 1: ps = None; continue
            if li == 0 and ps[0] % 12 != 2: ps = None; continue                      # the hymn opens on the tonic
            break
        if ps is None: return None, f"line {li + 1}"
        lines.append([dict(on=on, dur=d, syl=k, stress=st, slur=sl, p=p, line=li) for (on, d, k, st, sl), p in zip(rh, ps)])
        prev = ps[-1]
    t = [n for ln in lines for n in ln]
    if max(n["p"] for n in t if n["line"] != 3) >= 76: return None, "summit"
    return lines, None
def flat(lines): return [n for ln in lines for n in ln]
def readings(lines):
    return AB.readings([[n["on"] + 12, n["dur"], n["p"]] for n in flat(lines)], BAR, [0, 12, 24], 12)
def charge(r):
    c = d = 0.0
    for k, (a, m, z) in Q.items():
        sp = max(z - a, 1e-6); d += abs(r[k] - m) / sp
        if r[k] < a: c += (a - r[k]) / sp
        if r[k] > z: c += (r[k] - z) / sp
    return c, d
if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000; SEED = 20261113 + 400 + 12
    rng = random.Random(SEED); alive = []; deaths = collections.Counter()
    for k in range(N):
        t, err = build(rng)
        if err: deaths[err] += 1; continue
        r = readings(t); c, d = charge(r)
        fp = hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in flat(t)]).encode()).hexdigest()[:12]
        alive.append(dict(tune=t, readings=r, charge=c, distance=d, n=k, fp=fp))
    least = min(a["charge"] for a in alive); near = [a for a in alive if a["charge"] <= least + 0.05]
    pick = min(near, key=lambda a: a["distance"])
    print(f"built {N}, survivors {len(alive)} ({100*len(alive)/N:.1f}%); deaths {dict(deaths.most_common())}")
    print("pick", pick["fp"], "charge", round(pick["charge"], 3), "distance", round(pick["distance"], 2))
    for k, v in pick["readings"].items():
        a, m, z = Q[k]; print(f"  {k}: {round(v, 3)} (kept {round(a, 3)}, {round(m, 3)}, {round(z, 3)}){' *' if not (a <= v <= z) else ''}")
    med = {k: float(np.median([a["readings"][k] for a in alive])) for k in Q}
    alive.sort(key=lambda a: (a["charge"], a["distance"]))
    json.dump(dict(pick=pick, shortlist=alive[:12], built=N, survivors=len(alive), deaths=dict(deaths), seed=SEED, median_build=med, chords=CHORDS),
              open(f"{H}/melody_final.json", "w"), default=float)
