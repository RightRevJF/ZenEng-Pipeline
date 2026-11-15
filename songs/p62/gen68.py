"""The Room Next Door (song 52): a compound-metre (6/8) melody sketch in Luthier's manner, since Luthier's tables are 4/4 only.
Grid: twelfths of a quarter; an eighth 6, a 6/8 bar 36, a dotted-quarter beat 18. Kept tables: the Essen folk-song collection's 922 tunes in
6/8 (tables/essen_meter_tables.json, by tables_68.py). What carries over from Luthier, and what replaces it:
  - 653/680 (a drawn line from a kept line, whole): a line's rhythm is a kept two-bar window with its syllable count, drawn by its frequency
    and by 731's stress rule restated for 6/8 (stressed syllables on the two beats of the bar, 0 and 18; unstressed between).
  - 731 (pickups): leading unstressed syllables before the first stress, up to two, sung as eighths before the bar line.
  - 288/314 (registers): the verse low, the chorus above it, the bridge's first lines low; the designs pinned.
  - 650 (the per-note reading): each next pitch drawn from the kept 6/8 interval shares, chord tones weighted on the beats.
  - Repeats: verses 2-4 sing verse 1's tunes fitted to their syllables (Luthier's 'again'); chorus 2 copies chorus 1; the final chorus copies
    its first two lines, draws the line over the borrowed B-flat, refits the fourth and sings the designed hooks.
  - 730/715 (the judge): many builds, each read on the kept 6/8 quartiles; the pick the least charge, then the nearest the medians.
  - Added from songs 50 and 51 (746, 749.1, 749.2): no line holds one pitch four times running; no note of no length; no two onsets alike.
Usage: python3 gen68.py N seed"""
import json, random, sys, collections, math
import numpy as np
H = "/home/claude/p62"
T = json.load(open(f"{H}/tables/essen_meter_tables.json"))["6/8"]
SY = json.load(open(f"{H}/syllables.json"))
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p62.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
BAR, BEAT, E8 = 36, 18, 6
SCALE = {2, 4, 6, 7, 9, 11, 1}
CHT = {"Dadd9": {2, 6, 9, 4}, "Gmaj7": {7, 11, 2, 6}, "Dadd9/F#": {2, 6, 9, 4}, "Asus4": {9, 2, 4}, "D/F#": {2, 6, 9}, "Em9": {4, 7, 11, 2, 6},
       "Bm7": {11, 2, 6, 9}, "A": {9, 1, 4}, "Gadd9": {7, 11, 2, 9}, "F#m7": {6, 9, 1, 4}, "Cadd9": {0, 4, 7, 2}, "G/B": {7, 11, 2},
       "A7sus4": {9, 2, 4, 7}, "Bbmaj7": {10, 2, 5, 9}}
V_ = ["Dadd9", "Gmaj7", "D/F#", "Em9", "Bm7", "Gmaj7", "Em9", "Asus4"]
C_ = ["Gmaj7", "D/F#", "Em9", "Bm7", "Gmaj7", "A", "Bm7", "Gadd9", "Em9", "Asus4"]
SECCH = {"Intro": ["Dadd9", "Gmaj7", "Dadd9/F#", "Asus4"], "Verse 1": V_, "Chorus 1": C_, "Verse 2": V_, "Chorus 2": C_,
         "Interlude": ["Bm7", "Gmaj7", "Dadd9/F#", "Asus4"], "Verse 3": V_, "Bridge": ["Bm7", "F#m7", "Gmaj7", "D/F#", "Em9", "Cadd9", "G/B", "A7sus4"],
         "Verse 4": V_, "Last Chorus": ["Gmaj7", "D/F#", "Em9", "Bm7", "Gmaj7", "Bbmaj7", "Bm7", "Gadd9", "Em9", "Asus4", "Gmaj7", "Dadd9"],
         "Outro": ["Gmaj7", "D/F#", "Em9", "Dadd9"]}
FORM = [(s, len(SECCH[s])) for s in ("Intro", "Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Interlude", "Verse 3", "Bridge", "Verse 4", "Last Chorus", "Outro")]
BAR0 = {}; CHORD = []; b = 0
for s, nb in FORM: BAR0[s] = b; CHORD += SECCH[s]; b += nb
NBARS = b; assert NBARS == 84
SUNG = [s for s, _ in L.SECTIONS]
WORDS = dict(L.SECTIONS)
def line_start(sec, i): return (BAR0[sec] + 2 * i) * BAR
def chord_at(t): return CHORD[max(0, min(NBARS - 1, t // BAR))]
# ---- the designs ----
DOOR = [(6, 69, 6), (12, 71, 6), (18, 74, 18), (36, 71, 6), (42, 69, 6), (54, 69, 18)]          # 'there's a DOOR in the WALL': D5 on 'door', held; 'wall' open on A4 over Asus4
HOME = [(6, 69, 6), (12, 71, 6), (18, 71, 18), (36, 69, 6), (42, 66, 6), (54, 62, 54)]          # the second time: 'door' B4 over Gmaj7, 'wall' home on D4 over Dadd9, held into the outro
THERE = [(0, 62, 6), (6, 66, 6), (12, 69, 6), (18, 71, 12), (30, 69, 3), (33, 67, 3), (36, 67, 6), (42, 66, 6), (48, 64, 3), (51, 64, 3), (54, 64, 18)]   # 'and you were THERE ... GONE': B4, 'gone' held on E4 over A7sus4
DSPEC = {("Chorus 1", 4): DOOR, ("Chorus 2", 4): DOOR, ("Last Chorus", 4): DOOR, ("Last Chorus", 5): HOME, ("Bridge", 3): THERE}
REG = {"Verse": (64, 57, 69), "Chorus": (68, 62, 73), "Bridge": (62, 57, 66)}                  # centre, floor, cap (alto; D5 only in the designs)
def reg_of(sec, i):
    if sec.startswith("Verse"): return REG["Verse"]
    if sec == "Bridge": return REG["Bridge"] if i < 3 else (66, 59, 71)
    return REG["Chorus"]
WIN = {int(k): [(tuple(p), c) for p, c in v] for k, v in T["two_bar_windows"].items()}
IV = {int(k): v for k, v in T["intervals"].items()}; IVT = sum(IV.values())
Q = T["readings_quartiles"]
def ivp(d): return (IV.get(max(-12, min(12, d)), 0) + 0.5) / IVT
# ---- rhythm: a kept window for the line's syllables ----
def rhythm(rng, sy, min_start=-12):
    n = len(sy); lead = 0
    for x in sy:
        if x[1]: break
        lead += 1
    out = []
    for p in sorted({0, min(2, lead), min(1, lead)}):
        m = n - p
        for w, c in WIN.get(m, []):
            if w[-1] > 60 or w[0] != 0 and p > 0: continue
            ons = [-6 * (p - j) for j in range(p)] + list(w)
            if ons[0] < min_start: continue
            sc = 0.0
            for (t, (s_, st)) in zip(ons, sy):
                beat = t >= 0 and t % BEAT == 0
                sc += (1.5 if beat else -1.2 if t % 12 == 0 and t % BEAT else -0.4) if st else (-0.8 if beat and t % BAR == 0 else 0.0)
            if sy[-1][1] and ons[-1] % BEAT: sc -= 1.0
            out.append((ons, math.log(c + 1) + 1.4 * sc))
    if not out: return None
    top = sorted(out, key=lambda x: -x[1])[:12]; ws = [math.exp(s - top[0][1]) for _, s in top]
    return rng.choices([o for o, _ in top], ws)[0]
# ---- pitches ----
def pitches(rng, ons, U, sec, i, prev, end_rule=None, avoid=None):
    mu, lo, hi = reg_of(sec, i); ps = []
    for k, t in enumerate(ons):
        ch = CHT[chord_at(U + t)]; cands = [p for p in range(lo, hi + 1) if p % 12 in SCALE and (avoid is None or not avoid(U + t, p))]
        ws = []
        for p in cands:
            w = ivp(p - prev) if prev is not None else math.exp(-abs(p - mu) / 3)
            on_beat = (U + t) % BEAT == 0
            w *= (2.6 if p % 12 in ch else 0.3) if on_beat else (1.3 if p % 12 in ch else 0.8)
            w *= math.exp(-((p - mu) ** 2) / 50)
            if len(ps) >= 2 and ps[-1] == ps[-2] == p: w = 0.0                              # 749.2: no line holds one pitch four times (three here)
            if k == len(ons) - 1 and end_rule and not end_rule(p, ch): w *= 0.05
            ws.append(w)
        if sum(ws) <= 0: return None
        p = rng.choices(cands, ws)[0]; ps.append(p); prev = p
    return ps
def refit(rng, src, sy, U, sec, i, min_start=-12):
    """Luthier's 'again': the source line's onsets and pitches fitted to new syllables; a held note split, or a short one merged; a pickup
    that would collide with the line before dropped first."""
    keep = [(t, p) for t, p in src if t >= min_start] or src[-1:]
    on = [t for t, p in keep]; ps = [p for t, p in keep]; n = len(sy)
    while len(on) < n:
        gaps = [((on[j + 1] if j + 1 < len(on) else 66) - on[j], j) for j in range(len(on))]
        g, j = max(gaps)
        if g < 6: return None
        h = on[j] + (g // 2 // 3) * 3
        if h <= on[j]: return None
        nxt_p = ps[j + 1] if j + 1 < len(ps) else ps[j]
        step = [q for q in (ps[j] + 1, ps[j] - 1, ps[j] + 2, ps[j] - 2) if q % 12 in SCALE]
        q = min(step, key=lambda q_: abs(q_ - nxt_p)) if (rng.random() < 0.6 or (j > 0 and ps[j - 1] == ps[j])) else ps[j]
        on.insert(j + 1, h); ps.insert(j + 1, q)
    while len(on) > n:
        gaps = [(on[j + 1] - on[j], j) for j in range(1, len(on) - 1)]
        if not gaps: return None
        g, j = min(gaps); del on[j]; del ps[j]
    out = []
    for k, (t, p) in enumerate(zip(on, ps)):
        ch = CHT[chord_at(U + t)]
        if (U + t) % BEAT == 0 and p % 12 not in ch:                                         # a beat note moves a step to the chord
            q = min((p + d for d in (-1, 1, -2, 2) if (p + d) % 12 in SCALE and (p + d) % 12 in ch), key=lambda q_: abs(q_ - p), default=p); p = q
        mu, lo, hi = reg_of(sec, i)
        while p > hi: p -= 12 if p - 12 >= lo else 1
        while p < lo: p += 1
        while p % 12 not in SCALE: p -= 1
        out.append((t, p))
    return out
def lines_last_rel(lines, sec, i):
    """the earliest a line may begin, relative to its slot: the previous line's last onset plus an eighth and a breath (an eighth)"""
    keys = [(s, j) for s in SUNG for j in range(len(SY[s]))]; k = keys.index((sec, i))
    if k == 0: return -12
    ps, pj = keys[k - 1]
    if (ps, pj) not in lines: return 0
    last = line_start(ps, pj) + lines[(ps, pj)][-1][0]
    return max(-12, last + 12 - line_start(sec, i))
def runs_ok(ps): return all(not (ps[k] == ps[k + 1] == ps[k + 2] == ps[k + 3]) for k in range(len(ps) - 3))
def build(rng):
    lines = {}; prev = None
    plan_v = rng.choice(["ABCD", "ABAC", "ABCB"]); plan_b = rng.choice(["ABCX", "ABAX"])
    for sec in SUNG:
        for i, sy in enumerate(SY[sec]):
            U = line_start(sec, i); key = (sec, i)
            if key in DSPEC:
                lines[key] = [(t, p) for t, p, d in DSPEC[key]]; prev = lines[key][-1][1]; continue
            if sec == "Chorus 2" or (sec == "Last Chorus" and i in (0, 1)):
                lines[key] = list(lines[("Chorus 1", i)]); prev = lines[key][-1][1]; continue
            src = None
            if sec in ("Verse 2", "Verse 3", "Verse 4"): src = lines[("Verse 1", i)]
            if sec == "Last Chorus" and i == 3: src = lines[("Chorus 1", 3)]
            if sec == "Verse 1" and plan_v[i] != "ABCD"[i]: src = lines[("Verse 1", "ABCD".index(plan_v[i]))]
            if sec == "Bridge" and i == 2 and plan_b == "ABAX": src = lines[("Bridge", 0)]
            if src is not None:
                r = refit(rng, src, sy, U, sec, i, lines_last_rel(lines, sec, i))
                if r is None or not runs_ok([p for t, p in r]) or r[0][0] < lines_last_rel(lines, sec, i): return None, ("refit", key)
                lines[key] = r; prev = r[-1][1]; continue
            ms = (lines_last_rel(lines, sec, i) if (sec, i) != (SUNG[0], 0) else -12)
            ons = rhythm(rng, sy, ms)
            if ons is None: return None, ("rhythm", key)
            if i == 0 and prev is not None: pass
            end_rule = None
            if sec == "Verse 1" and i == 3: end_rule = lambda p, ch: p % 12 != 2                  # the verse ends off the tonic
            avoid = (lambda t, p: p % 12 in (6, 1, 11)) if (sec == "Last Chorus" and i == 2) else None   # over B-flat: no F#, C# or B
            ps = None
            for _ in range(20):
                ps = pitches(rng, ons, U, sec, i, prev, end_rule, avoid)
                if ps and runs_ok(ps): break
                ps = None
            if ps is None: return None, ("pitch", key)
            lines[key] = list(zip(ons, ps)); prev = ps[-1]
    notes = []
    keys = [(s, i) for s in SUNG for i in range(len(SY[s]))]
    flat = []
    for (s, i) in keys:
        U = line_start(s, i)
        for k, (t, p) in enumerate(lines[(s, i)]): flat.append(dict(on=U + t, p=p, sec=s, line=i, syl=k, stress=SY[s][i][k][1], text=SY[s][i][k][0]))
    flat.sort(key=lambda n: n["on"])
    for j, n in enumerate(flat):
        nx = flat[j + 1]["on"] if j + 1 < len(flat) else n["on"] + 72
        last = j + 1 == len(flat) or flat[j + 1]["line"] != n["line"] or flat[j + 1]["sec"] != n["sec"]
        key = (n["sec"], n["line"]); dd = dict((t, d) for t, p, d in DSPEC[key]) if key in DSPEC else None
        if dd is not None: n["dur"] = dd[n["on"] - line_start(*key)]
        elif last: n["dur"] = max(3, min(nx - n["on"] - 6, 24))
        else: n["dur"] = nx - n["on"]
    for j in range(len(flat) - 1):
        if flat[j]["on"] + flat[j]["dur"] > flat[j + 1]["on"]: flat[j]["dur"] = flat[j + 1]["on"] - flat[j]["on"]
    return dict(notes=flat, plans=dict(verse=plan_v, bridge=plan_b)), None
def readings(notes):
    p = [n["p"] for n in notes]; iv = np.diff(p)
    bars = collections.defaultdict(list)
    for n in notes: bars[n["on"] // BAR].append(n["on"] % BAR)
    pats = [tuple(v) for v in bars.values()]
    best = run = 1
    for a, b in zip(p, p[1:]): run = run + 1 if a == b else 1; best = max(best, run)
    gaps = np.diff([n["on"] for n in notes])
    return {"repeated notes": float(np.mean(iv == 0)), "moves by step": float(np.mean((abs(iv) >= 1) & (abs(iv) <= 2))), "moves by leap": float(np.mean(abs(iv) >= 5)),
            "turns of direction": sum(1 for a, b in zip(iv, iv[1:]) if a * b < 0) / max(1, int(np.sum(iv != 0)) - 1), "range": int(max(p) - min(p)),
            "distinct pitches": len(set(p)), "longest run of one pitch": best, "distinct rhythms over bars": len(set(pats)) / len(pats), "notes a bar": len(notes) / len(pats),
            "onsets on the beat": float(np.mean([n["on"] % BEAT == 0 for n in notes])), "onsets on the bar's first beat": float(np.mean([n["on"] % BAR == 0 for n in notes])),
            "gaps of a sixteenth": float(np.mean(gaps == 3)), "gaps of an eighth": float(np.mean(gaps == 6)), "gaps of a quarter or more": float(np.mean(gaps >= 12))}
LYRIC_SET = ("notes a bar", "gaps of a sixteenth", "gaps of an eighth", "gaps of a quarter or more", "range", "distinct pitches")   # set by the lyric's density and the designs: printed, not charged
def charge(r):
    c = 0.0; d = 0.0
    for k, (a, m, z) in Q.items():
        sp = max(z - a, 1e-6); d += abs(r[k] - m) / sp
        if k in LYRIC_SET: continue
        if r[k] < a: c += (a - r[k]) / sp
        if r[k] > z: c += (r[k] - z) / sp
    return c, d
def gates(c):
    ns = c["notes"]; f = []
    if any(n["dur"] <= 0 for n in ns): f.append("749.1: a note of no length")
    by = collections.defaultdict(list)
    for n in ns: by[(n["sec"], n["line"])].append(n)
    if any(len({n["on"] for n in v}) < len(v) for v in by.values()): f.append("749.1: two onsets alike")
    if any(not runs_ok([n["p"] for n in v]) for v in by.values()): f.append("749.2: a run of four")
    if max(n["p"] for n in ns) != 74 or any(n["p"] >= 74 and not ((n["sec"], n["line"]) in DSPEC and DSPEC[(n["sec"], n["line"])] in (DOOR,)) for n in ns): f.append("design: D5 only on 'door'")
    v = sorted(n["p"] for n in ns if n["sec"] == "Verse 1"); h = sorted(n["p"] for n in ns if n["sec"] == "Chorus 1" and n["line"] < 4)
    if h[len(h) // 2] < v[len(v) // 2] + 2: f.append("design: the chorus above the verse")
    if any(n["p"] > 66 for n in ns if n["sec"] == "Bridge" and n["line"] < 3): f.append("design: the bridge's first lines low")
    st = [n for n in ns if n["stress"] and (n["sec"], n["line"]) not in DSPEC]
    fr = [n for n in st if n["sec"] in ("Verse 1", "Chorus 1", "Bridge")]
    if (st and np.mean([n["on"] % BEAT == 0 for n in st]) < 0.4) or (fr and np.mean([n["on"] % BEAT == 0 for n in fr]) < 0.55): f.append("731: stressed syllables on the beat too few")
    return f
if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000; SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20261113 + 452
    rng = random.Random(SEED); made = 0; deaths = collections.Counter(); alive = []
    for k in range(N):
        c, err = build(rng); made += 1
        if err: deaths[err[0] + " " + err[1][0]] += 1; continue
        f = gates(c)
        if f: deaths[f[0]] += 1; continue
        r = readings(c["notes"]); ch, dist = charge(r); c.update(readings=r, charge=ch, distance=dist, n=k); alive.append(c)
    least = min(c["charge"] for c in alive); near = [c for c in alive if c["charge"] <= least + 0.05]
    pick = min(near, key=lambda c: c["distance"])
    import hashlib
    for c in alive: c["fp"] = hashlib.sha1(json.dumps([(n["on"], n["p"]) for n in c["notes"]]).encode()).hexdigest()[:12]
    print(f"built {made}, survivors {len(alive)}; deaths {dict(deaths.most_common())}")
    print("pick", pick["fp"], "charge", round(pick["charge"], 3), "distance", round(pick["distance"], 2), "plans", pick["plans"])
    for k, v in pick["readings"].items():
        a, m, z = Q[k]; print(f"  {k}: {round(v, 3)} (kept {round(a, 3)}, {round(m, 3)}, {round(z, 3)}){' *' if not (a <= v <= z) else ''}{' (lyric)' if k in LYRIC_SET else ''}")
    json.dump(dict(pick=pick, made=made, survivors=len(alive), deaths=dict(deaths), seed=SEED, alive=[dict(fp=c["fp"], charge=c["charge"], distance=c["distance"]) for c in alive],
                   median_build={k: float(np.median([c["readings"][k] for c in alive])) for k in Q}, form=FORM, chords=CHORD, bar0=BAR0), open(f"{H}/melody_final.json", "w"), default=float)
