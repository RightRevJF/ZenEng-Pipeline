"""Luthier v19, stage 6c (Module 27.100; fixes 852-855): four parts and a descant for a hymn tune written in hymn mode.

    python3 lib/luthier/hymn_parts.py songs/p63/spec53.json        # reads spec53.run.json (the pick), writes spec53.parts.json and spec53.parts.mid

852  FOUR PARTS, note against note under the tune (kept hymns: the lower voices carry as many notes a bar as the tune). At each note of the tune the alto, tenor
     and bass take tones of the bar's chord: every voice in its range, no voice above the one over it, no more than an octave between soprano and alto or alto and
     tenor, the chord's root and third both sounding, the bass on the root by preference, then the third, the fifth last. From note to note no two voices move
     in parallel fifths, octaves or unisons, and the whole setting is the one of least cost: the voices' moves in semitones, less a credit for each voice's kind of
     motion against the tune at the kept share for that voice (the Open Hymnal's alto, tenor and bass, by metre). Where the tune sings a tone outside the chord
     the lower voices may hold.
853  A DESCANT over the refrain (749.12): above the tune throughout, in its rhythm and words, tones of the chord, no parallel fifth, octave or unison with the tune
     or the bass, the nearest move preferred and motion against the tune credited; its summit sounds once, in the last quarter, where the tune itself is highest.
854  CHECKS: ranges, crossings, complete chords, parallels a hundred moves and each voice's motion against the kept, the descant above the tune and its summit.
855  The record: every voice on one timeline (749.13's first requirement); the pages are the session's.
Deterministic: there is no draw; the least-cost setting is found whole (a shortest path)."""
import json, sys, os, math, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ATLAS = os.path.join(HERE, "..", "..", "tables", "metre_atlas")
LAM, MOVE, BIAS = 3.0, 1.0, {"similar": 0.4, "contrary": 0.4, "oblique": -1.0}     # 852: fitted on song 53 until each voice's motion met the kept shares
RANGE = {"A": (55, 72), "T": (48, 67), "B": (40, 60)}; KEPT_KEY = {"A": "S1V2", "T": "S2V1", "B": "S2V2"}
def motion(ds, dv): return "oblique" if (ds == 0) != (dv == 0) else "static" if ds == 0 else "similar" if ds * dv > 0 else "contrary"
def perfect(a, b): return (a - b) % 12 in (0, 7)
def bad_parallel(x0, y0, x1, y1):
    """two voices (upper x, lower y) moving the same way from a perfect fifth, octave or unison to the same interval"""
    return x0 != x1 and y0 != y1 and (x1 - x0) * (y1 - y0) > 0 and (x0 - y0) % 12 == (x1 - y1) % 12 and (x0 - y0) % 12 in (0, 7)
def harmonise(tune, chord_of, CH, kept, shift=0):
    """tune: [(on, dur, pitch)]; chord_of(i) -> chord name; CH: name -> pitch classes (root first). Returns [(A, T, B)] and the cost."""
    lam, mv = LAM, MOVE; states = []
    for i, (on, d, s) in enumerate(tune):
        pcs = CH[chord_of(i)]; root, third = pcs[0], pcs[1]; v = []
        for b in range(RANGE["B"][0], RANGE["B"][1] + 1):
            if b % 12 not in pcs: continue
            cb = 0.0 if b % 12 == root else 2.5 if b % 12 == third else 5.0
            for t in range(max(RANGE["T"][0], b + 1), RANGE["T"][1] + 1):
                if t % 12 not in pcs: continue
                for a in range(max(RANGE["A"][0], t + 1), min(RANGE["A"][1], s - 1) + 1):
                    if a % 12 not in pcs or a - t > 12 or s - a > 12: continue
                    have = {a % 12, t % 12, b % 12} | ({s % 12} if s % 12 in pcs else set())
                    if root not in have or third not in have: continue
                    c = cb + (0.0 if len(have) == len(set(pcs)) else 1.0) + (1.5 if [x % 12 for x in (s, a, t, b)].count(third) > 1 else 0.0) + 0.05 * abs(a - 62) + 0.05 * abs(t - 57)
                    v.append((a, t, b, c))
        v.sort(key=lambda x: x[3]); states.append(v[:160])
    INF = 1e18; best = [dict() for _ in tune]
    for j, st in enumerate(states[0]): best[0][j] = (st[3], None)
    for i in range(1, len(tune)):
        ds = tune[i][2] - tune[i - 1][2]; s0, s1 = tune[i - 1][2], tune[i][2]; hold_ok = tune[i][2] % 12 not in CH[chord_of(i)] or chord_of(i) == chord_of(i - 1)
        for j, (a1, t1, b1, c1) in enumerate(states[i]):
            bj = (INF, None)
            for k, (a0, t0, b0, _) in enumerate(states[i - 1]):
                if k not in best[i - 1]: continue
                if bad_parallel(s0, a0, s1, a1) or bad_parallel(s0, t0, s1, t1) or bad_parallel(s0, b0, s1, b1) or bad_parallel(a0, t0, a1, t1) or bad_parallel(a0, b0, a1, b1) or bad_parallel(t0, b0, t1, b1): continue
                if a1 > s0 or t1 > a0 or b1 > t0 or a0 > s1 or t0 > a1 or b0 > t1: continue                    # no overlap
                c = best[i - 1][k][0] + c1 + mv * (abs(a1 - a0) + abs(t1 - t0) + 0.6 * abs(b1 - b0)) + (3.0 if abs(a1 - a0) > 5 else 0.0) + (3.0 if abs(t1 - t0) > 5 else 0.0) + (2.0 if abs(b1 - b0) > 7 else 0.0)
                for name, d_ in (("A", a1 - a0), ("T", t1 - t0), ("B", b1 - b0)):
                    m = motion(ds, d_)
                    if m != "static": c -= lam * (math.log(max(0.02, kept[KEPT_KEY[name]][m]) * 3.0) + BIAS[m])                # the kept share of that kind of motion for that voice
                if c < bj[0]: bj = (c, k)
            if bj[1] is not None: best[i][j] = bj
        if not best[i]: raise RuntimeError(f"no setting at note {i}")
    j = min(best[-1], key=lambda x: best[-1][x][0]); cost = best[-1][j][0]; out = []
    for i in range(len(tune) - 1, -1, -1): out.append(states[i][j][:3]); j = best[i][j][1]
    return out[::-1], cost
def descant(tune, parts, chord_of, CH, top_limit=81):
    """853: tune and parts for the passage; returns the descant's pitches"""
    n = len(tune); q0 = int(n * 0.75); peak_i = max(range(q0, n), key=lambda i: (tune[i][2], tune[i][1], -i))                 # the tune's highest (then longest) note of the last quarter
    top = max(p for p in range(tune[peak_i][2] + 3, top_limit + 1) if p % 12 in CH[chord_of(peak_i)])
    states = []
    for i, (on, d, s) in enumerate(tune):
        pcs = CH[chord_of(i)]; cap = top if i == peak_i else top - 1
        v = [p for p in range(s + 3, min(cap, s + 12) + 1) if p % 12 in pcs] if i != peak_i else [top]
        if not v: v = [p for p in range(s + 1, cap + 1) if p % 12 in pcs][:3]
        states.append(v)
    INF = 1e18; best = [dict() for _ in tune]
    for p in states[0]: best[0][p] = (0.02 * abs(p - (tune[0][2] + 7)), None)
    for i in range(1, n):
        s0, s1 = tune[i - 1][2], tune[i][2]; b0, b1 = parts[i - 1][2], parts[i][2]; ds = s1 - s0
        for p1 in states[i]:
            bj = (INF, None)
            for p0 in best[i - 1]:
                if bad_parallel(p0, s0, p1, s1) or bad_parallel(p0, b0, p1, b1): continue
                dv = p1 - p0; m = motion(ds, dv); c = best[i - 1][p0][0] + abs(dv) + (4.0 if abs(dv) > 5 else 0.0) + {"contrary": -1.5, "oblique": -1.0, "static": 0.0, "similar": 0.5}[m] + 0.02 * abs(p1 - (s1 + 7))
                if c < bj[0]: bj = (c, p0)
            if bj[1] is not None: best[i][p1] = bj
        if not best[i]: raise RuntimeError(f"no descant at note {i}")
    p = min(best[-1], key=lambda x: best[-1][x][0]); out = []
    for i in range(n - 1, -1, -1): out.append(p); p = best[i][p][1]
    return out[::-1], peak_i, top
def checks(tune, parts, kept, desc=None, d_from=0, peak=None, top=None):
    S = [x[2] for x in tune]; V = {"A": [x[0] for x in parts], "T": [x[1] for x in parts], "B": [x[2] for x in parts]}; out = {}
    out["ranges (lowest, highest)"] = {k: [min(v), max(v)] for k, v in V.items()}; out["every voice in its range"] = all(RANGE[k][0] <= min(v) and max(v) <= RANGE[k][1] for k, v in V.items())
    out["crossings"] = sum(not (s > a > t > b) for s, a, t, b in zip(S, V["A"], V["T"], V["B"])); pairs = [("S", "A"), ("S", "T"), ("S", "B"), ("A", "T"), ("A", "B"), ("T", "B")]; W = dict(V, S=S); par = 0; moves = 0
    for x, y in pairs:
        for i in range(1, len(S)):
            if W[x][i] != W[x][i - 1] or W[y][i] != W[y][i - 1]: moves += 1
            par += bad_parallel(W[x][i - 1], W[y][i - 1], W[x][i], W[y][i])
    out["parallel fifths, octaves, unisons a hundred moves (kept 0.7 to 0.9)"] = round(100 * par / max(1, moves), 2)
    for k in ("A", "T", "B"):
        c = collections.Counter(motion(S[i] - S[i - 1], V[k][i] - V[k][i - 1]) for i in range(1, len(S))); n = sum(v for m, v in c.items() if m != "static") or 1
        out[f"{k}: similar / contrary / oblique against the tune, written; kept"] = [[round(c[m] / n, 2) for m in ("similar", "contrary", "oblique")], [round(kept[KEPT_KEY[k]][m], 2) for m in ("similar", "contrary", "oblique")]]
        out[f"{k}: moves by step or less, share"] = round(sum(abs(V[k][i] - V[k][i - 1]) <= 2 for i in range(1, len(S))) / (len(S) - 1), 2)
    out["bass on the root, share"] = None
    if desc is not None:
        T2 = S[d_from:]; B2 = V["B"][d_from:]; out["descant above the tune throughout"] = all(d > s for d, s in zip(desc, T2)); out["descant: lowest, highest"] = [min(desc), max(desc)]
        out["descant's summit sounds once, in the last quarter"] = desc.count(max(desc)) == 1 and desc.index(max(desc)) >= int(len(desc) * 0.75)
        out["descant: parallels with the tune or the bass"] = sum(bad_parallel(desc[i - 1], T2[i - 1], desc[i], T2[i]) or bad_parallel(desc[i - 1], B2[i - 1], desc[i], B2[i]) for i in range(1, len(desc)))
        c = collections.Counter(motion(T2[i] - T2[i - 1], desc[i] - desc[i - 1]) for i in range(1, len(desc))); n = sum(c.values())
        out["descant: with / against / one holds / both hold, share"] = [round(c[m] / n, 2) for m in ("similar", "contrary", "oblique", "static")]
    return out
if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); run = json.load(open(sys.argv[1].replace(".json", "") + ".run.json")); ns = run["pick"]["notes"]; m = spec["metre"]
    T = json.load(open(os.path.join(ATLAS, m.replace("/", "-") + "_sung.json"))); kept = json.load(open(os.path.join(ATLAS, "hymns.json")))["by_metre"][m]["harmony"]; BAR = T["bar"]
    chords = [c for sec in spec["tune"] for c in sec["chords"]]; CH = {}
    for name, pcs in spec["chords"].items():                                                 # root first: the chord's name gives its root
        r = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[name[0]] + (1 if name[1:2] == "#" else -1 if name[1:2] == "b" else 0); third = next(p for p in pcs if (p - r) % 12 in (3, 4)); CH[name] = [r % 12, third] + [p for p in pcs if p not in (r % 12, third)]
    tune = [(n["on"], n["dur"], n["p"]) for n in ns]; chord_of = lambda i: chords[min(len(chords) - 1, max(0, tune[i][0]) // BAR)]
    parts, cost = harmonise(tune, chord_of, CH, kept); r0 = next(i for i, n in enumerate(ns) if n["sec"] == spec["tune"][-1]["name"])
    desc, peak, top = descant(tune[r0:], parts[r0:], lambda i: chord_of(i + r0), CH); ck = checks(tune, parts, kept, desc, r0, peak, top)
    ck["bass on the root, share"] = round(sum(parts[i][2] % 12 == CH[chord_of(i)][0] for i in range(len(tune))) / len(tune), 2)
    ck["chords complete (root, third and fifth sounding), share"] = round(sum(len({tune[i][2] % 12, *[p % 12 for p in parts[i]]} & set(CH[chord_of(i)][:3])) == 3 for i in range(len(tune))) / len(tune), 2)
    rec = dict(title=spec.get("title"), metre=m, pick=run["pick"]["fp"], bar=BAR, cost=round(cost, 2), checks=ck,
               voices={"S": [dict(on=o, dur=d, p=p) for o, d, p in tune], "A": [dict(on=o, dur=d, p=parts[i][0]) for i, (o, d, p) in enumerate(tune)], "T": [dict(on=o, dur=d, p=parts[i][1]) for i, (o, d, p) in enumerate(tune)],
                       "B": [dict(on=o, dur=d, p=parts[i][2]) for i, (o, d, p) in enumerate(tune)], "Desc": [dict(on=tune[r0 + i][0], dur=tune[r0 + i][1], p=p) for i, p in enumerate(desc)]},
               chords=[chord_of(i) for i in range(len(tune))], descant=dict(over=spec["tune"][-1]["name"], summit=top, at_note=peak, of=len(desc)))
    out = sys.argv[1].replace(".json", "") + ".parts.json"; json.dump(rec, open(out, "w"), indent=1)
    import mido
    mid = mido.MidiFile(ticks_per_beat=480); meta = mido.MidiTrack(); mid.tracks.append(meta); num, den = (int(x) for x in m.split("/")); meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(spec.get("bpm", 84)))); meta.append(mido.MetaMessage("time_signature", numerator=num, denominator=den))
    for ch_, (name, prog) in enumerate((("S", 52), ("A", 52), ("T", 52), ("B", 52), ("Desc", 53))):
        tr = mido.MidiTrack(); mid.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name)); tr.append(mido.Message("program_change", program=prog, channel=ch_)); msgs = []
        for e in rec["voices"][name]: msgs += [((e["on"] + BAR) * 40, 1, e["p"]), ((e["on"] + BAR + e["dur"]) * 40 - 1, 0, e["p"])]
        last = 0
        for t, k, p in sorted(msgs): tr.append(mido.Message("note_on" if k else "note_off", note=p, velocity=76 if k else 0, channel=ch_, time=max(0, t - last))); last = max(last, t)
    mid.save(out.replace(".json", ".mid"))
    print(f"{rec['title']}: four parts over {len(tune)} notes, cost {rec['cost']}; descant over the {rec['descant']['over']}, summit {top} at note {peak + 1} of {len(desc)}")
    for k, v in ck.items(): print("  ", k + ":", v)
