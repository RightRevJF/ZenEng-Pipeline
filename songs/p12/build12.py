"""Wood and Cloth (song 12), second edition: the record. The tune (melody_choice.json, D major, sounding pitch) harmonized in four parts by
song 53's beam search (harmonize12.py) three ways, then laid on one timeline from which every document (hymnal page, organ score,
lead sheet, MusicXML, demo) is written.

Harmonizations (the writer's 'as rich as possible within the rules', logged):
  HYMNAL   every stanza on the hymnal page: D Bm G A | Bm G E7 A | D F#7 Bm A | G Em7 A7 D  (two applied dominants a stanza, 749.23)
  STANZA4  choir alone: Bm D Em A | Bm Em E7 A | Bm F#7 Em A | Bm Gm6 A7 D  (darker; the hymn's one borrowed chord, G minor 6, under 'thorn')
  STANZA5  the organ's own, under the tune in unison: D Bm7 Em7 A | Bm7 G E7 A | D F#7 Bm A7 | G Em7 A7 D over a held D in the pedal

Timeline (twelfths of a quarter; bar n spans (n-1)*36 to n*36):
  bars 1-4    organ introduction: the last line in the hymnal harmony
  bars 5-52   stanzas 1-3, choir in four parts, the organ doubling them (stanzas 1-2 full; stanza 3 softer, manuals only)
  bars 53-68  stanza 4, choir alone, its own setting; the organ silent (stanza 3's last chord held, released as the choir breathes)
  bars 69-72  organ link back to full organ: starting on D (the choir's last chord), the hymn's figure rising over D, E, A in the pedal
  bars 73-88  stanza 5, everyone on the tune (men an octave lower), the sopranos' descant; the organ's own harmony; a held D in the
              pedal under the last line; broadening over the last two bars to a held chord"""
import json, collections, sys
import harmonize12 as HZ
sys.path[:0] = ["/home/claude/p63"]
import harm68
import lyric_p12 as L
H = "/home/claude/zeneng-pipeline/songs/p12"
BAR = 36
TUNE = json.load(open(f"{H}/melody_choice.json"))["tune"]
NOTES = []
for ln in TUNE:
    for j, n in enumerate(ln):
        NOTES.append(dict(n, melisma=bool(j and ln[j - 1]["slur"]), last=(j == len(ln) - 1)))
HYMNAL = ["D", "Bm", "G", "A", "Bm", "G", "E7", "A", "D", "F#7", "Bm", "A", "G", "Em7", "A7", "D"]
STANZA4 = ["Bm", "D", "Em", "A", "Bm", "Em", "E7", "A", "Bm", "F#7", "Em", "A", "Bm", "Gm6", "A7", "D"]
STANZA5 = ["D", "Bm7", "Em7", "A", "Bm7", "G", "E7", "A", "D", "F#7", "Bm", "A7", "G", "Em7", "A7", "D"]
def hz_input(notes, chs, lock_bars=()):
    out = []; downs = {}
    for k, n in enumerate(notes):
        if n["on"] % BAR == 0: downs[n["line"]] = k
    for k, n in enumerate(notes):
        out.append(dict(s=n["p"], dur=n["dur"], strong=n["on"] % BAR == 0, bar_chord=chs[n["on"] // BAR], phrase_end=downs[n["line"]] == k,
                        final=k == len(notes) - 1, melisma=n["melisma"], summit=(n["p"] == 76),
                        passing_ok=(n["dur"] <= 12 and n["on"] % BAR != 0), lock=n["on"] % BAR == 0 or (lock_bars and n["on"] // BAR in lock_bars)))
    return out
def harmonize(chs, lock_bars=()):
    cost, path, _, _ = HZ.harmonize(hz_input(NOTES, chs, lock_bars), 8)
    for k, n in enumerate(NOTES):
        if n["melisma"]: path[k] = tuple(path[k - 1])
    return [list(x) for x in path], cost
import itertools
def pars(path, k):
    v0 = [NOTES[k - 1]["p"]] + path[k - 1][1:]; v1 = [NOTES[k]["p"]] + path[k][1:]; out = []
    for i, j in itertools.combinations(range(4), 2):
        i0 = (v0[i] - v0[j]) % 12; i1 = (v1[i] - v1[j]) % 12
        if i0 == i1 and i0 in (0, 7) and v0[i] != v1[i] and v0[j] != v1[j]: out.append((i, j))
    return out
def fix_parallels(path):
    """a parallel fifth or octave left by the hold under a melisma: the lower voice of the pair, at the later chord, moves to another
    tone of its chord within a fourth of where it was, keeping the voices in order and making no new parallel either side"""
    fixes = []
    for k in range(1, len(path)):
        for i, j in pars(path, k):
            v = j; ch = path[k][0]; cur = path[k][v]
            for q in sorted((q for q in range(cur - 5, cur + 6) if q % 12 in HZ.CHORDS[ch][1] and q != cur), key=lambda q: abs(q - cur)):
                trial = [list(x) for x in path]; trial[k][v] = q
                vs = [NOTES[k]["p"]] + trial[k][1:]
                if not all(vs[a] > vs[a + 1] for a in range(3)): continue
                if pars(trial, k) or (k + 1 < len(path) and pars(trial, k + 1)): continue
                fixes.append((k, v, cur, q)); path[k][v] = q; break
    return fixes
PATH_H, COST_H = harmonize(HYMNAL)
PATH_4, COST_4 = harmonize(STANZA4, lock_bars=(13, 14))          # G minor 6 held through its bar, then A7
PATH_5, COST_5 = harmonize(STANZA5)
# stanza 4, bars 14-15 (the writer's G minor 6, then A7): the search's bass went B-flat to C-sharp, an augmented second. Set by hand: the bass
# holds G under G minor 6 and steps to A; the tenor's B-flat falls to A; the third of A7 arrives in the tune on beat 3 ("his").
def _set(path, bar, vs):
    ks = [k for k, x in enumerate(NOTES) if x["on"] // BAR == bar - 1]
    for k, v in zip(ks, vs): path[k] = list(v)
_set(PATH_4, 14, [("Gm6", 67, 58, 43), ("Gm6", 67, 58, 43)]); _set(PATH_4, 15, [("A7", 67, 57, 45), ("A7", 64, 57, 45)])
HAND = ["stanza 4 bars 14-15 voiced by hand: bass G2 G2 A2 A2 (was G2 B-flat2 C-sharp3, an augmented second), tenor B-flat3 to A3"]
FIXES = {n: fix_parallels(p) for n, p in (("hymnal", PATH_H), ("stanza4", PATH_4), ("stanza5", PATH_5))}
SCALE_D = {2, 4, 6, 7, 9, 11, 1}
def passing(notes, path, rate=0.10):
    """song 53's passing notes: where an inner voice (alto, then tenor, then the bass on longer notes) moves a third inside a line,
    the second half of its note takes the scale tone between, unless that makes parallels, crosses a voice or sits under a melisma"""
    segs = [[(0, n["dur"], *path[k][1:])] for k, n in enumerate(notes)]; cands = []
    for k in range(len(notes) - 1):
        n, m = notes[k], notes[k + 1]
        if n["line"] != m["line"] or n["dur"] not in (12, 24) or n["slur"] or n["melisma"]: continue
        (c0, A0, T0, B0), (c1, A1, T1, B1) = path[k], path[k + 1]
        for vi, (x0, x1) in enumerate(((A0, A1), (T0, T1), (B0, B1))):
            if abs(x1 - x0) not in (3, 4) or (vi == 2 and n["dur"] == 12): continue
            mid = [q for q in range(min(x0, x1) + 1, max(x0, x1)) if q % 12 in (SCALE_D | set(HZ.CHORDS[c0][1]) & set(HZ.CHORDS[c1][1]) or SCALE_D)]
            mid = [q for q in mid if q % 12 in SCALE_D or q % 12 in HZ.CHORDS[c1][1]]
            if len(mid) != 1: continue
            q = mid[0]; v0 = [n["p"], A0, T0, B0]; v1 = [m["p"], A1, T1, B1]; vm = list(v0); vm[vi + 1] = q
            ok = all(vm[i] >= vm[i + 1] for i in range(3))
            for i in range(4):
                for j in range(i + 1, 4):
                    if i == vi + 1 or j == vi + 1:
                        im, i1 = abs(vm[i] - vm[j]) % 12, abs(v1[i] - v1[j]) % 12
                        if im == i1 and im in (0, 7) and vm[i] != v1[i] and vm[j] != v1[j]: ok = False
            if ok: cands.append((k, vi, q, n["dur"])); break
    want = int(round(rate * 3 * len(notes) / 2))
    for k, vi, q, d in ([c for c in cands if c[3] == 12][:want] + [c for c in cands if c[3] == 24]):
        A, T, B = segs[k][0][2:]; v = [A, T, B]; v2 = list(v); v2[vi] = q
        segs[k] = [(0, d // 2, *v), (d // 2, d // 2, *v2)]
    return segs
SEG_H, SEG_4 = passing(NOTES, PATH_H), passing(NOTES, PATH_4)
# the descant (stanza 5): above the tune a third to a sixth, chord tones of the organ's chord on strong and long notes; G5 over 'cloth'
def descant():
    """stanza 5's descant, one line by least cost over the whole stanza: B4 to G5, always at least a minor third over the tune; chord tones
    of the organ's chord on downbeats and long notes, scale tones between by step; thirds, sixths and tenths over the tune cheap, fifths
    and octaves dear and never in parallel; steps and holds cheap, leaps over a fourth dear; G5 (the top) only over 'wood and cloth',
    the third above 'cloth'; it ends on F#5, the third of the last chord."""
    ch = [set(HZ.CHORDS[c][1]) for c, *_ in PATH_5]; INT = {3: 0.0, 4: 0.0, 8: 0.3, 9: 0.3, 0: 2.5, 7: 1.8, 5: 1.0}
    cl = next(k for k, n in enumerate(NOTES) if n["p"] == 76)
    cands = []
    for k, n in enumerate(NOTES):
        strong = n["on"] % BAR == 0 or n["dur"] >= 24
        pcs = ch[k] if strong else (SCALE_D | ch[k])
        cs = []
        for p in range(71, 80):
            if p % 12 not in pcs or p - n["p"] < 3 or (p - n["p"]) % 12 not in INT: continue
            if p == 79 and n["on"] // BAR not in (12, 13): continue
            c = INT[(p - n["p"]) % 12] + (0 if p % 12 in ch[k] else 0.6)
            if k == cl and p != 79: continue
            if k == len(NOTES) - 1 and p != 78: continue
            cs.append((p, c))
        cands.append(cs)
    best = [{p: (c, None) for p, c in cands[0]}]
    for k in range(1, len(NOTES)):
        row = {}
        for p, c in cands[k]:
            opts = []
            for q, (bc, _) in best[-1].items():
                m = abs(p - q); t = 0.25 * m + (2.0 if m > 5 else 0) + (-0.1 if m == 0 else 0)
                if NOTES[k - 1]["melisma"] or NOTES[k]["melisma"]: t += 0 if m <= 2 else 3.0
                i0, i1 = (q - NOTES[k - 1]["p"]) % 12, (p - NOTES[k]["p"]) % 12
                if i0 == i1 and i0 in (0, 7) and p != q: t += 20.0
                ds, dd = NOTES[k]["p"] - NOTES[k - 1]["p"], p - q
                if ds and dd and (ds > 0) != (dd > 0): t -= 0.3
                opts.append((bc + t + c, q))
            if opts: row[p] = min(opts)
        best.append(row)
    p = min(best[-1], key=lambda q: best[-1][q][0]); out = [p]
    for k in range(len(NOTES) - 1, 0, -1): p = best[k][p][1]; out.append(p)
    return out[::-1]
DESC = descant()
assert DESC[next(k for k, n in enumerate(NOTES) if n["p"] == 76)] == 79
# ---- the timeline ----
INTRO, ST = 0, {1: 4 * BAR, 2: 20 * BAR, 3: 36 * BAR, 4: 52 * BAR, 5: 72 * BAR}
LINK = 68 * BAR; END = 88 * BAR
V = collections.defaultdict(list)
def put(voice, on, dur, p, **kw): V[voice].append(dict(on=on, dur=dur, p=p, **kw))
def choir(off, path, segl, stanza):
    for k, n in enumerate(NOTES):
        put("S", n["on"] + off, n["dur"], n["p"], slur=n["slur"], melisma=n["melisma"], stanza=stanza)
        for o, d, A, T, B in segl[k]:
            put("A", n["on"] + off + o, d, A, stanza=stanza); put("T", n["on"] + off + o, d, T, stanza=stanza); put("B", n["on"] + off + o, d, B, stanza=stanza)
def organ_double(off, path, segl, pedal=True, t0=0, t1=16 * BAR):
    for k, n in enumerate(NOTES):
        if not (t0 <= n["on"] < t1): continue
        for o, d, A, T, B in segl[k]:
            on = n["on"] + off + o
            put("org_rh", on, d, sorted({n["p"], A}) if o == 0 else [A] if False else sorted({n["p"], A}))
            if pedal: put("org_lh", on, d, T); put("org_ped", on, d, B)
            else: put("org_lh", on, d, sorted({T, B}))
# introduction: the last line, hymnal harmony, full
organ_double(INTRO - 12 * BAR, PATH_H, SEG_H, True, 12 * BAR, 16 * BAR)
for s in (1, 2, 3):
    choir(ST[s], PATH_H, SEG_H, s)
    organ_double(ST[s], PATH_H, SEG_H, pedal=(s != 3))
choir(ST[4], PATH_4, SEG_4, 4)
# link, bars 69-72 (third edition): it starts on D, the chord the choir ends stanza 4 on, so the organ meets the choir where it is;
# the right hand rises in the hymn's figure (dotted quarter, slurred eighth, quarter) over a held lower note; pedal D, E, A, A
LINK_TOP = [(66, 67, 69), (67, 69, 71), (69, 71, 73), (73, 74, 76)]
LINK_LOW = [62, 64, 64, 67]
LINK_LH = [[54, 57], [55, 59], [55, 61], [57, 61]]
LINK_PED = [50, 40, 45, 45]
LINK_CH = ["D", "Em7", "A7", "A7"]
for i in range(4):
    t = LINK + i * BAR; a, b_, c = LINK_TOP[i]
    put("org_rh", t, 18, sorted({LINK_LOW[i], a})); put("org_rh", t + 18, 6, sorted({LINK_LOW[i], b_})); put("org_rh", t + 24, 12, sorted({LINK_LOW[i], c}))
    put("org_lh", t, 36, LINK_LH[i]); put("org_ped", t, 36, LINK_PED[i])
# stanza 5: all on the tune; descant; the organ's own harmony
for k, n in enumerate(NOTES):
    on = n["on"] + ST[5]
    put("S", on, n["dur"], n["p"], slur=n["slur"], melisma=n["melisma"], stanza=5, unison=True)
    put("T", on, n["dur"], n["p"] - 12, stanza=5, unison=True, slur=n["slur"], melisma=n["melisma"])
    put("Desc", on, n["dur"], DESC[k], slur=n["slur"], melisma=n["melisma"], stanza=5)
    ch, A, T, B = PATH_5[k]
    # the left hand stays above the men's unison line: the tenor an octave up where it fits under the alto, else left out
    fill = [q for q in range(A + 3, n["p"] - 2) if q % 12 in HZ.CHORDS[ch][1]]          # full organ: a chord tone between alto and tune
    put("org_rh", on, n["dur"], sorted({n["p"], A} | ({fill[len(fill) // 2]} if fill and not n["melisma"] else set())))
    t2 = T if T >= 57 else T + 12
    if t2 < A: put("org_lh", on, n["dur"], t2)
    if n["on"] < 12 * BAR: put("org_ped", on, n["dur"], B)
put("org_ped", ST[5] + 12 * BAR, 4 * BAR, 38)                     # the held D under the last line
for v in V.values(): v.sort(key=lambda e: (e["on"], -e["dur"]))
def merge_holds(ev, organ):
    out = []
    for e in ev:
        if out and out[-1]["p"] == e["p"] and out[-1]["on"] + out[-1]["dur"] == e["on"] and (organ or e.get("hold_ok")): out[-1]["dur"] += e["dur"]
        else: out.append(dict(e))
    return out
S_on = {e["on"]: e for e in V["S"]}
for voice in ("A", "T", "B"):
    for e in V[voice]:
        s = S_on.get(e["on"]); e["hold_ok"] = bool(s and s.get("melisma"))
    V[voice] = merge_holds(V[voice], False)
for voice in ("org_rh", "org_lh", "org_ped"): V[voice] = merge_holds(V[voice], True)
REC = dict(title=L.TITLE, edition=L.EDITION, voices=dict(V), stanza_offsets=ST, intro=INTRO, link=LINK, end=END, bars=88, qpm=100,
           key="D major", meter="3/4", chords=dict(hymnal=HYMNAL, stanza4=STANZA4, stanza5=STANZA5),
           paths=dict(hymnal=PATH_H, stanza4=PATH_4, stanza5=PATH_5), costs=dict(hymnal=COST_H, stanza4=COST_4, stanza5=COST_5),
           segments=dict(hymnal=SEG_H, stanza4=SEG_4), parallel_fixes=FIXES, hand=HAND, descant=DESC, tune=NOTES, build=json.load(open(f"{H}/melody_choice.json"))["n"])
json.dump(REC, open(f"{H}/song_record.json", "w"), default=list)
if __name__ == "__main__":
    N = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']; nm = lambda p: N[p % 12] + str(p // 12 - 1)
    print("parallel fixes", FIXES); print("costs", {k: round(v, 1) for k, v in REC["costs"].items()})
    for k, v in V.items():
        ps = [q for e in v for q in (e["p"] if isinstance(e["p"], list) else [e["p"]])]; print(f"{k:8} {len(v):4} events  {nm(min(ps))}-{nm(max(ps))}")
    for name, path in (("hymnal", PATH_H), ("stanza4", PATH_4), ("stanza5", PATH_5)):
        print(name, " ".join(f"{c}" for c, *_ in path)); print("   stats", HZ.stats([dict(s=n["p"]) for n in NOTES], [tuple(p) for p in path]))
    print("descant", " ".join(nm(p) for p in DESC))
