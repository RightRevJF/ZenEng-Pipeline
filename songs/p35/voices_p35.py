"""The First Wood -- the inner voices, written after the tune and the bass (137: the bass is written with the melody and before the
inner voices). Alto G3-C5, tenor C3-G4; each chord complete where it can be (V7 may drop its fifth); the leading tone and the
seventh never doubled; the seventh falls by step; no parallel fifths or octaves between any two voices; no crossing; spacing within
an octave above the tenor; the least motion. The inner voices hold when the chord holds (a passing note in the tune moves alone)."""
import pickle, sys, itertools, collections
sys.path[:0] = ["/home/claude/p35"]
import melody_p35 as M
R = pickle.load(open("/home/claude/p35/melody_result.pkl", "rb")); PICK = R["alive"][0]
NOTES = PICK["notes"]; HARM = PICK["harm"]
ALO, AHI, TLO, THI = 55, 72, 48, 67
LT, SEV = 4, 10                          # E, the leading tone; B-flat, V7's seventh

def chords_merged():
    out = []
    for h in HARM:
        if out and (out[-1]["chord"], out[-1]["bass"]) == (h["chord"], h["bass"]): out[-1]["end"] = h["end"]
        else: out.append(dict(h))
    return out
SL = chords_merged()
RELAXED = []

def sop_at(t):
    n = M.sounding(NOTES, t); return n["p"] if n else None

def options(h, relax=False):
    s = sop_at(h["on"]); b = h["bass"]; ch = h["chord"]; tones = M.tones_of(ch)
    out = []
    for a in range(ALO, AHI + 1):
        if a % 12 not in tones: continue
        for t in range(TLO, THI + 1):
            if t % 12 not in tones: continue
            if s is not None and not (t <= a <= s): continue
            if not (b <= t): continue
            if s is not None and s - a > 12: continue
            if a - t > 12: continue
            pcs = [x % 12 for x in (s, a, t, b) if x is not None]
            need = set(tones) - ({7} if ch == "V7" else set())          # V7 may drop its fifth
            if ch == "I64": need = {0, 5, 9}
            if relax: need = {M.root_of(ch), (M.root_of(ch) + (4 if ch in ("I", "IV", "V", "V7", "I64") else 3)) % 12}   # root and third
            if not need <= set(pcs): continue
            if pcs.count(LT) > 1 and ch != "iii": continue
            if ch == "V7" and pcs.count(SEV) > 1: continue
            if ch == "I64" and pcs.count(0) < 2: continue
            out.append((a, t))
    return out

def parallels(prev, cur):
    """parallel fifths or octaves between any two voices, prev and cur as (s, a, t, b)."""
    for i, j in itertools.combinations(range(4), 2):
        if None in (prev[i], prev[j], cur[i], cur[j]): continue
        i0, i1 = (prev[i] - prev[j]) % 12, (cur[i] - cur[j]) % 12
        if i0 == i1 and i1 in (0, 7) and prev[i] != cur[i] and prev[j] != cur[j] and (cur[i] - prev[i] > 0) == (cur[j] - prev[j] > 0): return True
    return False

def solve():
    best = [{} for _ in SL]
    for o in options(SL[0]): best[0][o] = (abs(o[0] - 65) * 0.1 + abs(o[1] - 57) * 0.1, None)
    for k in range(1, len(SL)):
        h0, h1 = SL[k - 1], SL[k]
        s0, s1 = sop_at(h0["on"]), sop_at(h1["on"])
        opts = options(h1)
        if not opts: opts = options(h1, relax=True); RELAXED.append(k)
        for o in opts:
            top = None
            for po, (sc, _) in best[k - 1].items():
                prev = (s0, po[0], po[1], h0["bass"]); cur = (s1, o[0], o[1], h1["bass"])
                if parallels(prev, cur): continue
                v = sc + abs(o[0] - po[0]) + abs(o[1] - po[1])
                if abs(o[0] - po[0]) > 7 or abs(o[1] - po[1]) > 7: v += 6
                if h0["chord"] == "V7":                                   # the seventh falls by step
                    for x0, x1 in ((po[0], o[0]), (po[1], o[1])):
                        if x0 % 12 == SEV and not (1 <= x0 - x1 <= 2): v += 8
                if top is None or v < top[0]: top = (v, po)
            if top: best[k][o] = top
        if not best[k]: raise SystemExit(f"no voicing at slot {k} {h1}")
    o = min(best[-1], key=lambda x: best[-1][x][0]); path = [o]
    for k in range(len(SL) - 1, 0, -1):
        o = best[k][o][1]; path.append(o)
    path.reverse()
    return [dict(h, alto=a, tenor=t) for h, (a, t) in zip(SL, path)]

if __name__ == "__main__":
    V = solve()
    allv = [(sop_at(v["on"]), v["alto"], v["tenor"], v["bass"]) for v in V]
    bad = sum(1 for a, b in zip(allv, allv[1:]) if parallels(a, b))
    inv = sum(1 for v in V if v["bass"] % 12 != M.root_of(v["chord"])) / len(V)
    pickle.dump(dict(voices=V, fp=PICK["fp"], relaxed=RELAXED), open("/home/claude/p35/voices.pkl", "wb"))
    print(f"relaxed (root and third only): {RELAXED}")
    print(f"{len(V)} chords; parallels {bad}; inverted {inv:.2f}; alto {min(v['alto'] for v in V)}-{max(v['alto'] for v in V)}, tenor {min(v['tenor'] for v in V)}-{max(v['tenor'] for v in V)}")
