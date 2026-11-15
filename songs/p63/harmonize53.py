"""Song 53 (Sung to Sleep): the carol pipeline's four-part setting (Module 11.19, v38), copied; two chords added for the verse-4 organ setting.
Module 11.19 (v38) four-part setting: beam search (width 8) over chord and voicing together,
costs from Table AL as the paper states them. Soprano = the chosen tune at reading pitch."""
import json, itertools, collections, math

TONIC = 2
CHORDS = {   # name: (root pc, chord pcs in order root, third, fifth[, seventh])
    "D": (2, [2, 6, 9]), "Em": (4, [4, 7, 11]), "F#m": (6, [6, 9, 1]), "G": (7, [7, 11, 2]),
    "A": (9, [9, 1, 4]), "Bm": (11, [11, 2, 6]), "A7": (9, [9, 1, 4, 7]), "E7": (4, [4, 8, 11, 2]),
    "Em7": (4, [4, 7, 11, 2]), "Bm7": (11, [11, 2, 6, 9]),
    "F#7": (6, [6, 10, 1, 4]), "C": (0, [0, 4, 7]),                       # song 53's verse-4 organ setting: V of vi, and the borrowed flat seven
}
DIATONIC_ALTS = ["D", "Em", "F#m", "G", "A", "Bm", "A7", "Em7", "Bm7"]
RANGE = {"A": (55, 69), "T": (48, 66), "B": (38, 60)}
MEDIAN_COMPASS = {"A": (58, 67), "T": (52, 62), "B": (43, 57)}     # Window 57
LEADING = 1   # C#

def motion_cost(a, b):
    d = abs(a - b)
    return 0.1 if d == 0 else 0.2 if d <= 2 else 0.9 if d <= 4 else 2.0 if d <= 7 else 5.0

def voicings(chord, s):
    root, pcs = CHORDS[chord]
    out = []
    for B in range(RANGE["B"][0], RANGE["B"][1] + 1):
        if B % 12 not in pcs: continue
        for T in range(max(B, RANGE["T"][0]), min(RANGE["T"][1], s) + 1):
            if T % 12 not in pcs or T - B > 19: continue
            for A in range(max(T, RANGE["A"][0]), min(RANGE["A"][1], s) + 1):
                if A % 12 not in pcs or A - T > 12 or s - A > 12: continue
                out.append((A, T, B))
    return out

SAME_FUNCTION = {("A", "A7"), ("A7", "A"), ("Em", "Em7"), ("Em7", "Em"), ("Bm", "Bm7"), ("Bm7", "Bm")}
def same(a, b): return a == b or (a, b) in SAME_FUNCTION

def vert_cost(chord, s, A, T, B, is_strong, bar_chord, phrase_end, final, first=False, summit=False):
    root, pcs = CHORDS[chord]
    c = 0.0
    if not same(chord, bar_chord):
        c += 3.5 if is_strong else 1.5
    present = [x % 12 for x in (s, A, T, B)]
    cnt = collections.Counter(present)
    third = pcs[1]; fifth = pcs[2]
    if root not in cnt: c += 5.0
    if third not in cnt: c += 5.0
    if fifth not in cnt: c += 0.5
    if len(pcs) == 4 and pcs[3] not in cnt: c += 1.0
    if cnt[third] >= 2 and len(pcs) == 3: c += 1.6                    # doubled third
    if cnt[LEADING] >= 2: c += 6.0                                    # doubled leading tone
    if len(pcs) == 4 and cnt[pcs[3]] >= 2: c += 4.0                   # doubled seventh
    inv = pcs.index(B % 12)
    if inv == 2: c += 2.2                                              # second inversion
    if inv == 3: c += 1.5
    if s - A > 9: c += 1.0                                             # alto more than a sixth below
    for v, x in (("A", A), ("T", T), ("B", B)):
        lo, hi = MEDIAN_COMPASS[v]
        if x < lo: c += 0.4 * (lo - x)
        if x > hi: c += 0.4 * (x - hi)
    if phrase_end and s % 12 in CHORDS[bar_chord][1] and (not same(chord, bar_chord) or inv != 0): c += 50.0
    if (first or final) and inv != 0: c += 3.0                          # open and close in root position
    if chord == "F#m": c += 0.6                                           # iii sparingly, as hymnals use it
    if summit and inv != 0: c += 1.5                                      # the summit on a root-position chord      # phrase end: bar's chord, root position
    if final and cnt[root] < 2: c += 1.0
    return c

def trans_cost(prev, cur, s0, s1, holds):
    (c0, A0, T0, B0), (c1, A1, T1, B1) = prev, cur
    c = motion_cost(A0, A1) + motion_cost(T0, T1)
    for a, b in ((A0, A1), (T0, T1), (B0, B1)):
        if abs(a - b) == 6: c += 3.0                                    # no tritone leaps
    tune_moves = s1 != s0
    nh = dict(holds)
    for v, a, b in (("A", A0, A1), ("T", T0, T1)):
        nh[v] = holds[v] + 1 if a == b else 0
        if a == b and tune_moves and nh[v] > 2: c += 0.8
    ds = s1 - s0
    for a, b in ((A0, A1), (T0, T1), (B0, B1)):
        if ds and (b - a) and (ds > 0) != (b - a > 0): c -= 0.3       # contrary motion earns
    db = abs(B1 - B0)
    if db in (1, 2): c -= 0.45                                         # bass step earns
    elif db > 7: c += 4.0
    elif db == 0: c += 0.2
    elif db <= 4: c += 0.4
    else: c += 0.6
    # parallel fifths / octaves between any pair
    v0 = [s0, A0, T0, B0]; v1 = [s1, A1, T1, B1]
    for i, j in itertools.combinations(range(4), 2):
        i0 = (v0[i] - v0[j]) % 12; i1 = (v1[i] - v1[j]) % 12
        if i0 == i1 and i0 in (0, 7) and v0[i] != v1[i] and v0[j] != v1[j]:
            c += 8.0
    # voice overlap with the previous chord
    if A1 > s0 or T1 > A0 or B1 > T0 or A1 < T0 or T1 < B0: c += 4.0
    # tendency tones
    _, p0 = CHORDS[c0]
    for a, b in ((A0, A1), (T0, T1), (B0, B1)):
        if c0 in ("A7", "E7") and a % 12 == p0[3] and not (0 < a - b <= 2) and c1 != c0: c += 2.0   # 7th falls
        if a % 12 == LEADING and c1 in ("D", "Bm") and c0 != c1 and b % 12 not in (2, 1): c += 1.0
        if c0 == "E7" and a % 12 == 8 and c1 != c0 and b % 12 != 9: c += 2.0                       # G# rises
    return c, nh

def harmonize(notes, beam_width=8):
    """notes: list of dict(s, dur, strong, bar_chord, phrase_end, final, passing_ok)"""
    beams = [(0.0, [], None, {"A": 0, "T": 0})]
    for k, n in enumerate(notes):
        s = n["s"]
        cands = []
        chords = [n["bar_chord"]] + [c for c in DIATONIC_ALTS if c != n["bar_chord"]]
        for ch in chords:
            pcs = CHORDS[ch][1]
            if s % 12 not in pcs and not n["passing_ok"]: continue
            for (A, T, B) in voicings(ch, s):
                vc = vert_cost(ch, s, A, T, B, n["strong"], n["bar_chord"], n["phrase_end"], n["final"],
                               first=(k == 0), summit=n.get("summit", False))
                if s % 12 not in pcs: vc += 0.5
                cands.append((ch, A, T, B, vc))
        nb = []
        for cost, path, prev, holds in beams:
            for ch, A, T, B, vc in cands:
                if prev is None:
                    tc, nh = 0.0, holds
                else:
                    tc, nh = trans_cost(prev, (ch, A, T, B), notes[k - 1]["s"], s, holds)
                    if n.get("melisma") and ch != prev[0]: tc += 6.0              # hold the chord under a melisma
                    if n.get("melisma") and (abs(A - prev[1]) > 2 or abs(T - prev[2]) > 2 or B != prev[3]): tc += 3.0
                nb.append((cost + vc + tc, path + [(ch, A, T, B)], (ch, A, T, B), nh))
        nb.sort(key=lambda x: x[0])
        # keep the best path per distinct final verticality, then the top beam_width
        seen, beams = set(), []
        for x in nb:
            if x[2] in seen: continue
            seen.add(x[2]); beams.append(x)
            if len(beams) == beam_width: break
    return beams[0]

def stats(notes, path):
    roots = firsts = seconds = 0; dbl = collections.Counter(); bassm = collections.Counter()
    am = collections.Counter(); tm = collections.Counter(); changes = 0; par = 0
    for k, (ch, A, T, B) in enumerate(path):
        pcs = CHORDS[ch][1]; inv = pcs.index(B % 12)
        roots += inv == 0; firsts += inv == 1; seconds += inv == 2
        cnt = collections.Counter(x % 12 for x in (notes[k]["s"], A, T, B))
        if len(pcs) == 3:
            for role, pc in zip(("root", "third", "fifth"), pcs):
                if cnt[pc] >= 2: dbl[role] += 1
        if k:
            pc_, A0, T0, B0 = path[k - 1]
            if ch != pc_: changes += 1
            d = abs(B - B0); bassm["stay" if d == 0 else "step" if d <= 2 else "third" if d <= 4 else "4th/5th" if d <= 7 else "wide"] += 1
            for cnt_, a, b in ((am, A0, A), (tm, T0, T)):
                dd = abs(a - b); cnt_["hold" if dd == 0 else "step" if dd <= 2 else "leap"] += 1
            v0 = [notes[k - 1]["s"], A0, T0, B0]; v1 = [notes[k]["s"], A, T, B]
            for i, j in itertools.combinations(range(4), 2):
                i0 = (v0[i] - v0[j]) % 12; i1 = (v1[i] - v1[j]) % 12
                if i0 == i1 and i0 in (0, 7) and v0[i] != v1[i] and v0[j] != v1[j]: par += 1
    n = len(path); nm = n - 1
    norm = lambda c: {k: round(v / sum(c.values()), 3) for k, v in c.items()}
    return {"root_position": round(roots / n, 3), "first_inversion": round(firsts / n, 3),
            "second_inversion": round(seconds / n, 3), "doubling": dict(dbl),
            "bass_motion": norm(bassm), "alto": norm(am), "tenor": norm(tm),
            "chord_change_per_note": round(changes / nm, 3), "parallels": par}

if __name__ == "__main__":
    rec = json.load(open("melody_record.json"))
    STANZA_CH = ["D", "G", "D", "A", "D", "Bm", "E7", "A", "Bm", "G", "Em", "A", "D", "G", "A", "D"]
    bar_ch = STANZA_CH + rec["refrain_chords"]
    mel = [tuple(x) for x in rec["stanza"]] + [tuple(x) for x in rec["refrain"]]
    notes = []
    # phrase ends: the last note of each 4-bar line
    # the cadence of each line is its last downbeat (feminine endings put a weak syllable after it)
    last_down = {}
    for k, (on, du, p, syl) in enumerate(mel):
        if abs(on % 3) < 1e-6: last_down[int(on // 12)] = k
    for k, (on, du, p, syl) in enumerate(mel):
        bar = int(on // 3)
        line_end = (k == len(mel) - 1) or (int(mel[k + 1][0] // 12) != int(on // 12))
        notes.append(dict(s=p, dur=du, strong=abs(on % 3) < 1e-6, bar_chord=bar_ch[bar],
                          phrase_end=(last_down[int(on // 12)] == k), final=k == len(mel) - 1,
                          melisma=syl is None, summit=(p == max(x[2] for x in mel) and abs(on % 3) < 1e-6),
                          passing_ok=(du <= 0.5 or syl is None) and not line_end))
    cost, path, _, _ = harmonize(notes, 8)
    st = stats(notes, path)
    print("total cost", round(cost, 2)); print(json.dumps(st, indent=1))
    json.dump({"notes": notes, "path": path, "stats": st, "cost": cost, "mel": mel},
              open("setting.json", "w"), indent=1)
