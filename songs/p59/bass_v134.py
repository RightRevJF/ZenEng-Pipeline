"""v134 (song 48): v131's routine unchanged, used for the sung sections (the instrumentals' bass is written in build_p58.py). v131: song 47's bass: v130's routine (538 as adopted), with the scale read by the bar, so the second bridge's lifted bars (A major) take
their passing notes from A major. v130 (538 on v129's routine): song 46's bass. 538: on a section with four kicks a bar, the cells vary by pitch and articulation where the
rhythm cannot: each cell of the plan (A B A C A B D E) keeps its own figure of intervals and its own articulation (legato; short off-beats;
staccato; accented off-beats), the figures of B and D drawn apart from A's. Everything else as v129:
v129 (516, 517 on v128's Part 3): the bass written by rule from the chart, the kick and the vocal's rests (439; amends 233-235), and read (444-448).
  439  write_bass(rec): the record's bars (the chord at each half-bar), its kicks (drum note 36) and its lead (where the voice rests).
  445  each section's bass is a two-bar figure and its variants, laid out over eight bars as A B A C A B A D (C and D the fills of bars 4 and 8,
       or of a bar whose second half the voice leaves empty); never one bar repeated through.
  446  the bar's notes: the root on the first beat and at every change; the others drawn among the root, its octave, the fifth, the third,
       the seventh where the scale has it, and notes of passage, so that a bar holds 2 to 4 pitch classes and 38-73% of its notes are on the
       pitch class it began with.
  447  moves: repeats, steps, thirds, fourths and fifths drawn toward the pop-and-rock middle halves; an octave at most once a bar and never
       four octave moves running.
  448  a bass note on the kick (every kick the figure can take), notes between the kicks so that 35-59% of the bass's notes are on a kick;
       the bar's last note a step into the next bar's first in a quarter to a half of the bars whose first notes differ.
  440  the root at every change (the record's chords carry no inversions).
  444  each eight bars read with Window 144's measures() against the Lucerne quartiles for pop, rock, rock and roll, alternative and country
       (zeneng_v124_bass_between_the_chords.json); Window 118's bands are not used.
  449  nothing here takes a listener rating as its target: the bands are of what kept bass lines do.
A draw that breaks a test in some eight bars is drawn again (at most 60 times a section, from the section's own seed); what stands is read.
Usage: python3 bass_v129.py   (rebuilds the records of songs 40, 43 and 44 into records/, and writes records/bass_readings_v129.json)"""
import json, re, pickle, collections, random, os, sys
import numpy as np
H = "/home/claude/p59"; H55 = "/home/claude/p55"
TB = json.load(open(f"{H55}/tables/zeneng_v124_bass_between_the_chords.json"))
exec(re.search(r"^def measures\(.*?(?=^\S)", TB["code"], re.S | re.M).group(0))          # Window 144's reading of a bass
POPQ = TB["findings"]["quartiles and mean: pop, rock, rock and roll, alternative, country (198 patterns)"]
ALLQ = TB["findings"]["quartiles and mean: all patterns"]
NAME = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def root_pc(c):
    c = c.split("/")[0]; return (NAME[c[0]] + (1 if "#" in c[:2] else -1 if (len(c) > 1 and c[1] == "b") else 0)) % 12
def minor(c): c = c.split("/")[0]; return "m" in c[1:3] and "maj" not in c
def bass_pc(c):
    if "/" in c: return root_pc(c.split("/")[1])
    return root_pc(c)
BAR = 48
SONGS = {}
SCALE_AT = [None]                                                                          # v131: a function bar -> scale, or None
ARTS = ("legato", "short off-beats", "staccato", "accented off-beats")                    # 538
DENS = {"Verse": 5, "Pre": 6, "Chorus": 7, "Post": 7, "Bridge": 4, "Intro": 5, "Solo": 7, "Outro": 4, "Tag": 6}   # notes a bar by the section's place in the arc (9.12)
def scale_of(key):
    t, m = key; return {(t + x) % 12 for x in ((0, 2, 3, 5, 7, 8, 10) if m == "minor" else (0, 2, 4, 5, 7, 9, 11))}
def chart(rec):
    """the chord of each half-bar (the record's chords2 if it has them, else the bar's chord twice)."""
    if rec.get("chords2"): return list(rec["chords2"])
    return [h for b in rec["bars"] for h in (b["chord"], b["chord"])]
def kicks(rec):
    K = collections.defaultdict(set)
    for d in rec["drums"]:
        if 36 in d["p"]: K[d["on"] // BAR].add(d["on"] % BAR)
    return K
def voice_rest(rec):
    """a half-bar the voice leaves without an onset."""
    on = collections.Counter(n["on"] // 24 for n in rec["lead"]); return lambda h: on[h] == 0
def lowr(pc, lo): return lo + (pc - lo) % 12
def section_bars(rec):
    out = collections.OrderedDict()
    for b, x in enumerate(rec["bars"]): out.setdefault(x["sec"], []).append(b)
    return out
def draw_cell(rng, kk, dens):
    """a bar's rhythm: the kicks it can take, beat 1, notes between toward the section's density, on the eighth grid (sixteenths rare)."""
    cell = {0} | {k for k in kk if k % 6 == 0}
    grid = [t for t in range(0, BAR, 6) if t not in cell]
    want = max(len(cell), min(8, int(round(dens + rng.choice((-1, 0, 0, 1))))))
    while len(cell) < want and grid:
        w = [3.0 if t % 12 == 6 else 1.5 for t in grid]; t = rng.choices(grid, w)[0]; cell.add(t); grid.remove(t)
    return sorted(cell)
def vary(rng, cell, fill=False):
    c = set(cell); free = [t for t in range(6, BAR, 6) if t not in c]
    if fill:                                                                                 # the fill: one or two more notes in beats 3 and 4
        f = [t for t in free if t >= 24]
        for t in rng.sample(f, min(len(f), rng.choice((1, 2)))): c.add(t)
    else:
        if len(c) > 3 and rng.random() < 0.5: c.discard(rng.choice([t for t in c if t not in (0, 24)] or [max(c)]))
        if free: c.add(rng.choice(free))
    return sorted(c)
def write_section(rng, rec, bars, H2, K, rest, lo, scale0, kind):
    kk0 = K.get(bars[0], set()) | (K.get(bars[1], set()) if len(bars) > 1 else set())
    dens = max(DENS.get(kind, 6), len([k for k in kk0 if k % 6 == 0]) / 0.52)          # 448: no more than about half the notes on a kick
    A = draw_cell(rng, kk0, dens); B = vary(rng, A); C = vary(rng, B, fill=True)
    if B == A: B = vary(rng, A)
    D = vary(rng, vary(rng, A))                                                              # 517: a third cell in the second four bars
    for _ in range(6):
        if D not in (A, B): break
        D = vary(rng, D)
    E = vary(rng, D, fill=True)
    plan = [A, B, A, C, A, B, D, E]                                                          # 517: A B A C A B D E
    LET = "ABACABDE"
    four = sum(1 for b in bars if {0, 12, 24, 36} <= K.get(b, set())) * 2 >= len(bars)        # 538: a section with four kicks a bar
    art = {}; Wl = {}
    if four:
        a0 = rng.choice(ARTS); art = {"A": a0}
        for l_ in "BCDE": art[l_] = rng.choice([x for x in ARTS if x != a0] if l_ in "BD" else ARTS)
        for l_ in "ABCDE": Wl[l_] = dict(rep=rng.uniform(0.9, 1.4), fifth=rng.uniform(0.5, 1.0), oct=rng.uniform(0.1, 0.3), third=rng.uniform(0.2, 0.5), sev=rng.uniform(0.1, 0.35), pas=rng.uniform(0.2, 0.5))
    W = dict(rep=rng.uniform(0.9, 1.4), fifth=rng.uniform(0.5, 1.0), oct=rng.uniform(0.1, 0.3), third=rng.uniform(0.2, 0.5), sev=rng.uniform(0.1, 0.35), pas=rng.uniform(0.2, 0.5))
    fig = {}                                                                                 # the figure: an interval for each place of cell A, kept for the A bars
    ev = []; prev = None; oct_run = 0
    for j, b in enumerate(bars):
        cell = list(plan[j % 8])
        if rest(2 * b + 1) and j % 8 not in (3, 7) and rng.random() < 0.35: cell = vary(rng, cell, fill=True)   # the voice rests: a fill
        for k in K.get(b, ()):                                                               # a kick the figure lacks, taken where it is on the grid
            if k % 6 == 0 and k not in cell and len(cell) < 8: cell = sorted(set(cell) | {k})
        chs = [H2[2 * b], H2[2 * b + 1]]
        if chs[1] != chs[0] and 24 not in cell: cell = sorted(set(cell) | {24})              # 440: a note at the change
        nxt_root = lowr(bass_pc(H2[2 * b + 2]), lo) if 2 * b + 2 < len(H2) else None
        scale = SCALE_AT[0](b) if SCALE_AT[0] else scale0
        oct_bar = 0
        for i, t in enumerate(cell):
            ch = chs[t // 24]; r = lowr(bass_pc(ch), lo); change = t == 0 or (t == 24 and chs[1] != chs[0])
            last = i == len(cell) - 1
            if change: p = r                                                                 # 440: the root at the bar line and at the change
            elif last and nxt_root is not None and nxt_root % 12 != r % 12 and rng.random() < 0.45:   # 448: a step into the next bar
                st = [nxt_root + d for d in (-2, -1, 1, 2) if (nxt_root + d) % 12 in scale]
                st = [x for x in st if lo - 2 <= x <= lo + 19] or [nxt_root - 2]
                p = min(st, key=lambda x: (abs(x - (prev if prev is not None else r)), x))
            else:
                key_ = (j % 8 in (0, 2, 4, 6), i)
                if four: key_ = (LET[j % 8], i)                                              # 538: each cell its own figure, kept
                if four and key_ in fig and rng.random() < 0.9: iv = fig[key_]
                elif key_ in fig and key_[0] and not four and rng.random() < 0.8: iv = fig[key_]
                else:
                    third = 3 if minor(ch) else 4; sev = 10 if (r + 10) % 12 in scale else None
                    W_ = Wl.get(LET[j % 8], W) if four else W
                    if four and LET[j % 8] in "BD" and ("A", i) in fig:                         # 538: B and D drawn apart from A's figure
                        W_ = dict(W_); W_["rep"] *= 0.5 if fig[("A", i)] == 0 else 1.0
                    opts = [(0, W_["rep"]), (7, W_["fifth"]), (-5, W_["fifth"] * 0.5), (third, W_["third"])]
                    if oct_bar == 0 and oct_run < 2: opts.append((12, W_["oct"]))
                    if sev is not None: opts.append((sev - 12, W_["sev"]))
                    pas = [d for d in (2, -1, -2, 5) if (r + d) % 12 in scale and (r + d) % 12 not in ((r + 7) % 12, (r + third) % 12)]
                    if pas: opts.append((rng.choice(pas), W_["pas"]))
                    if four and LET[j % 8] in "BD" and ("A", i) in fig and len(opts) > 1:
                        opts = [(x, w) for x, w in opts if x != fig[("A", i)]] or opts
                    iv = rng.choices([x for x, _ in opts], [w for _, w in opts])[0]
                    if key_[0]: fig[key_] = iv
                p = r + iv
                while p > lo + 19: p -= 12
                while p < lo - 5: p += 12
            if prev is not None and abs(p - prev) == 12: oct_bar += 1; oct_run += 1
            elif prev is not None: oct_run = 0
            nx_t = cell[i + 1] if i + 1 < len(cell) else BAR
            dur_ = max(3, nx_t - t - 1); vel_ = 100 if t == 0 else 94 if t % 12 == 0 else 88; a_ = art.get(LET[j % 8]) if four else None
            if a_ == "short off-beats" and t % 12: dur_ = 3
            elif a_ == "staccato": dur_ = max(3, (nx_t - t) // 2)
            elif a_ == "accented off-beats": vel_ = 104 if t % 12 else 86
            ev.append(dict(on=b * BAR + t, dur=dur_, p=[p], vel=vel_, art="bass" + (f":{LET[j % 8]}:{a_}" if a_ else "")))
            prev = p
    return ev
def read_window(B, K, b0, nb):
    """Window 144's measures on bars b0 .. b0+nb of the bass B (events) and kicks K."""
    bb = sorted(((e["on"] - b0 * BAR) / 12, e["dur"] / 12, min(e["p"])) for e in B if b0 * BAR <= e["on"] < (b0 + nb) * BAR)
    mono = []
    for x in bb:
        if mono and abs(mono[-1][0] - x[0]) < 1e-6:
            if x[2] < mono[-1][2]: mono[-1] = x
            continue
        mono.append(x)
    kk = [((b - b0) * BAR + k) / 12 for b in range(b0, b0 + nb) for k in sorted(K.get(b, ()))]
    m = measures(mono, kk, nb) if len(mono) >= 8 else None
    if m:                                                                                    # 516: 448's share read on the bars that have a kick
        kb_ = {b - b0 for b in range(b0, b0 + nb) if K.get(b)}; ks_ = {int(round(x * 12)) for x in kk}
        on_k = [int(round(x[0] * 12)) for x in mono if int(x[0] // 4) in kb_]
        m[0]["bass_with_kick_kicked_bars"] = float(np.mean([t in ks_ for t in on_k])) if on_k else float("nan")
    return (m[0] if m else None), mono
def cells538(B, b0, nb):
    """538: the eight bars' distinct bar rhythms, rhythm and figure, and rhythm, figure and articulation."""
    bars = collections.defaultdict(list)
    for e in B:
        if b0 * BAR <= e["on"] < (b0 + nb) * BAR: bars[e["on"] // BAR].append((e["on"] % BAR, min(e["p"]), e["dur"]))
    r = {b: tuple(o for o, _, _ in v) for b, v in bars.items()}; f = {b: tuple((o, y - v[0][1]) for o, y, _ in v) for b, v in bars.items()}
    a = {b: tuple((o, y - v[0][1], d) for o, y, d in v) for b, v in bars.items()}
    ra = {b: tuple((o, d) for o, _, d in v) for b, v in bars.items()}
    return dict(rhythms=len(set(r.values())), rhythm_and_articulation=len(set(ra.values())), rhythm_and_figure=len(set(f.values())), rhythm_figure_articulation=len(set(a.values())))
def alt_octaves(mono):
    iv = [abs(b[2] - a[2]) for a, b in zip(mono, mono[1:])]; run = best = 0
    for x in iv: run = run + 1 if x == 12 else 0; best = max(best, run)
    return best >= 4
def root_at_changes(B, H2, nbars):
    """440: of the changes (a half-bar whose chord differs from the one before), the share with a bass note on the root there."""
    at = {e["on"]: min(e["p"]) for e in B}; ok = n = 0
    for h in range(len(H2)):
        if h and H2[h] == H2[h - 1]: continue
        t = h * 24
        if t // BAR >= nbars: break
        n += 1; ok += t in at and at[t] % 12 == bass_pc(H2[h])
    return ok / max(1, n), n
def tests(m, mono):
    if m is None: return None
    T = {"445 two or more bar rhythms": m["distinct_bar_rhythms"] >= 2, "445 the bar before repeated in under half": m["bar_rhythm_same_as_last"] < 0.5,
         "446 2-4 pitch classes a bar": 2.0 <= m["pitch_classes_per_bar"] <= 4.0, "446 38-73% on the bar's first note": 0.38 <= m.get("on_the_bars_first_note", -1) <= 0.73,
         "447 repeats 20-61%": 0.20 <= m["iv_repeat"] <= 0.61, "447 steps 9-32%": 0.09 <= m["iv_step"] <= 0.32, "447 octaves under 29%": m["iv_octave"] < 0.29,
         "447 no alternating octaves": not alt_octaves(mono), "448 a note on 70% of kicks": m.get("kick_with_bass", 1.0) >= 0.70,
         "448 35-59% of notes on a kick (bars with a kick, 516)": (0.35 <= m["bass_with_kick_kicked_bars"] <= 0.59) if np.isfinite(m.get("bass_with_kick_kicked_bars", np.nan)) else None}
    s = m.get("into_the_bar_by_step_of_changes")
    T["448 a step into the next bar in 25-50% of changes"] = (0.25 <= s <= 0.50) if (s is not None and np.isfinite(s)) else None
    return T
def windows_of(rec):
    """each section's eight-bar windows (a shorter section read whole)."""
    out = []
    for sec, bs in section_bars(rec).items():
        for k in range(0, len(bs), 8):
            w = bs[k:k + 8]
            if len(w) >= 4: out.append((sec, w[0], len(w)))
    return out
def write_bass(rec, lo, key, song):
    H2 = chart(rec); K = kicks(rec); rest = voice_rest(rec); scale = scale_of(key); B = []; tries = {}
    for sec, bs in section_bars(rec).items():
        kind = rec["bars"][bs[0]]["kind"]; rng = random.Random(f"439 bass {song} {sec} v131"); best = None
        for it in range(60):
            ev = write_section(rng, rec, bs, H2, K, rest, lo, scale, kind)
            bad = 0
            for k in range(0, len(bs), 8):
                w = bs[k:k + 8]
                if len(w) < 4: continue
                m, mono = read_window(ev, K, w[0], len(w)); t = tests(m, mono)
                bad += sum(1 for v in (t or {}).values() if v is False) if t else 1
            if best is None or bad < best[0]: best = (bad, ev, it + 1)
            if bad == 0: break
        tries[sec] = (best[2], best[0]); B += best[1]
    return sorted(B, key=lambda e: e["on"]), tries
def read_song(rec, B):
    K = kicks(rec); rows = []
    for sec, b0, nb in windows_of(rec):
        m, mono = read_window(B, K, b0, nb)
        if m is None: rows.append(dict(sec=sec, bar=b0, bars=nb, note="under eight notes")); continue
        rows.append(dict(sec=sec, bar=b0, bars=nb, m={k: round(v, 3) for k, v in m.items() if np.isfinite(v)}, tests=tests(m, mono), cells538=cells538(B, b0, nb),
                         four=sum(1 for b in range(b0, b0 + nb) if {0, 12, 24, 36} <= K.get(b, set())) * 2 >= nb))
    return rows
def summary(rows):
    ms = ("notes_per_bar", "pitch_classes_per_bar", "on_the_bars_first_note", "iv_repeat", "iv_step", "iv_octave", "bar_rhythm_same_as_last", "distinct_bar_rhythms",
          "kick_with_bass", "bass_with_kick", "bass_with_kick_kicked_bars", "into_the_bar_by_step_of_changes", "bars_one_pitch_class", "on_sixteenth")
    R = [r for r in rows if "m" in r]; out = {}
    for m in ms:
        v = [r["m"][m] for r in R if m in r["m"]]
        if v: out[m] = dict(median=round(float(np.median(v)), 3), pop_rock_quartiles=POPQ[m][:3] if m in POPQ else None, all_quartiles=ALLQ[m][:3] if m in ALLQ else None)
    tp = collections.defaultdict(lambda: [0, 0])
    for r in R:
        for k, v in (r["tests"] or {}).items():
            if v is None: continue
            tp[k][0] += bool(v); tp[k][1] += 1
    out["tests: windows passing, of windows read"] = {k: v for k, v in tp.items()}
    out["windows read"] = len(R); out["windows under eight notes"] = len(rows) - len(R)
    return out
if __name__ == "__main__":
    print("bass_v130: write_bass is called by build_p56.py; the readings by readings_v130.py")
