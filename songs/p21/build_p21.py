"""Build the song record for 'Make Do' from the frozen melody ranking (#1). Times in eighths, 4/4 at q = 72, each bar carrying metre,
tempo, key (G major) and chord. The INSTRUMENTAL LINES (Module 27.21, v64): the intro, the break and the outro -- instrumental form
items of four bars or more -- each take a line of their own, written from the hook's cell and floored, played by the clean guitar
(the writer's Q5 A: 'the break a clean guitar line'), notated as a cue voice on the lead sheet."""
import pickle, sys, random
sys.path[:0] = ["/home/claude/p21"]
import melody_p21 as M, lyric as L
R = pickle.load(open("/home/claude/p21/melody_result.pkl", "rb"))
c = R["alive"][0]
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        ln = M.SECS[s][li]
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=ln["role"], meter="4/4", falsetto=False))
lead.sort(key=lambda n: n["on"])
bars = [dict(sec=b["sec"], meter="4/4", chord=b["chord"], start=b["start"], len=8, qbpm=72, key="G major",
             build=False, instrumental=b["sec"] in ("Intro", "Break", "Outro")) for b in M.BARS]
TOT = M.TOTAL; EIGHTH_SEC = {"4/4": 60 / 72 / 2}; secs = TOT * EIGHTH_SEC["4/4"]
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, met))
# ---- Module 27.21: the instrumental line ----
INSTR = dict(name="clean guitar", program=27, lo=52, hi=84, clef="treble_8", label="cue: clean guitar — written under the staff's 8vb clef: sounds an octave lower")
SC = sorted(p for p in range(INSTR["lo"], INSTR["hi"] + 1) if p % 12 in M.GSET)
def deg(p): return SC.index(p)
h = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 3]                  # the title cell
MOTIF_P = [deg(min(SC, key=lambda q: abs(q - n["midi"]))) for n in h[:4]]
MOTIF = dict(steps=[b - a for a, b in zip(MOTIF_P, MOTIF_P[1:])], ratios=[n["dur"] / h[0]["dur"] for n in h[:4]],
             source=" ".join(n["syl"][0] for n in h[:4]))
SEQ_PLAIN = ["repeat", "tonal", "inverted", "varied", "tonal", "repeat"]
def chord_tones(ch): return M.CH[ch]
def bar_at(e): return next(b for b in bars if b["start"] <= e < b["start"] + 8)
def transform(kind, steps):
    if kind == "inverted": return [-s for s in steps]
    if kind == "varied": return steps[:-1] + [steps[-1] + (1 if steps[-1] <= 0 else -1)]
    return list(steps)
rng = random.Random(2101)
def write_line(sec, center=66, peak_top=None):
    bs = [b for b in bars if b["sec"] == sec]; nph = len(bs) // 4; out = []; kinds = []
    peak_ph = max(1, (nph + 1) // 2) if nph > 1 else 0               # one phrase past the middle takes the top
    prev = None
    for ph in range(nph):
        kind = SEQ_PLAIN[ph % len(SEQ_PLAIN)]; kinds.append(kind)
        st = bs[4 * ph]["start"]; ch0 = bs[4 * ph]["chord"]
        cen = center + (2 if kind == "tonal" else 0) + (4 if ph == peak_ph and nph > 1 else 0)
        start = min([p for p in SC if p % 12 in chord_tones(ch0)], key=lambda q: abs(q - cen))
        d0 = deg(start); pos = st
        for k, stp in enumerate([0] + transform(kind, MOTIF["steps"])):      # the motif, a quarter a unit
            d0 += stp; p = SC[max(0, min(len(SC) - 1, d0))]
            out.append(dict(on=pos, dur=2, midi=p, sec=sec, src="motif:" + kind)); pos += 2
        prev = out[-1]["midi"]; end = st + 32
        while pos < end:                                                   # the fills: chord tones on strong beats, steps between
            b = bar_at(pos); rel = pos - b["start"]; last = end - pos <= 4
            dur = 4 if last else 2
            if rel % 4 == 0 or last:
                cands = [p for p in SC if p % 12 in chord_tones(b["chord"]) and abs(deg(p) - deg(prev)) <= 3]
                if ph == peak_ph and nph > 1 and pos == st + 16 and peak_top: cands = [max(p for p in SC if p <= peak_top and p % 12 in chord_tones(b["chord"]))]
                p = min(cands, key=lambda q: abs(q - cen) + 0.5 * abs(q - prev)) if cands else prev
            else:
                nb = bar_at(pos + 2) if pos + 2 < TOT else b
                tgt = [p for p in SC if p % 12 in chord_tones(nb["chord"])]
                t = min(tgt, key=lambda q: abs(q - prev) if q != prev else 99)
                p = SC[deg(prev) + (1 if t > prev else -1)]
            out.append(dict(on=pos, dur=min(dur, end - pos), midi=p, sec=sec, src="fill")); prev = p; pos += dur
    return out, kinds
gtr, kinds_by = [], {}
for sec, cen, top in (("Intro", 64, None), ("Break", 66, 76), ("Outro", 64, None)):
    ln_, kd = write_line(sec, cen, top); gtr += ln_; kinds_by[sec] = kd
og = [n for n in gtr if n["sec"] == "Outro"]; og[-1]["midi"] = min([p for p in SC if p % 12 == 7], key=lambda q: abs(q - og[-1]["midi"]))
# the floor (27.21), row by row -- the rule, not a band (no corpus of instrumental lines was measured)
def floor(sec):
    ns = [n for n in gtr if n["sec"] == sec]; bs = [b for b in bars if b["sec"] == sec]; st0 = bs[0]["start"]; L_ = 8 * len(bs)
    strong = [n for n in ns if (n["on"] - bar_at(n["on"])["start"]) % 4 == 0]
    ct = sum(1 for n in strong if n["midi"] % 12 in chord_tones(bar_at(n["on"])["chord"])) / max(1, len(strong))
    phr = [len({n["midi"] for n in ns if st0 + 32 * k <= n["on"] < st0 + 32 * (k + 1)}) for k in range(len(bs) // 4)]
    pk = max(ns, key=lambda n: n["midi"]); place = (pk["on"] - st0) / L_
    rows = dict(chord_tones_on_strong=(round(ct, 2), ct >= 0.8), distinct_pitches_a_phrase=(min(phr), min(phr) >= 3),
                peak_place=(round(place, 2), place > 1 / 3 if len(bs) > 4 else True),
                range=([min(n["midi"] for n in ns), max(n["midi"] for n in ns)], all(INSTR["lo"] <= n["midi"] <= INSTR["hi"] for n in ns)))
    return rows
FLOOR = {s: floor(s) for s in ("Intro", "Break", "Outro")}
gtr.sort(key=lambda n: n["on"])
vocal_spans = [(n["on"], n["on"] + n["dur"]) for n in lead]
def clash(n): return any(a < n["on"] + n["dur"] and n["on"] < b for a, b in vocal_spans)
kept = []
for n in gtr:                                                              # the cue steps aside where a sung pickup reaches into its bars
    if not clash(n): kept.append(n); continue
    nxt = min((a for a, b in vocal_spans if a > n["on"]), default=None)
    if nxt is not None and not any(a <= n["on"] < b for a, b in vocal_spans) and nxt - n["on"] >= 1: kept.append(dict(n, dur=nxt - n["on"]))
STEPPED = sum(1 for a in gtr if a not in kept); gtr = kept
assert all(a["on"] + a["dur"] <= b["on"] for a, b in zip(gtr, gtr[1:]))
rec = dict(title=L.TITLE, meter="4/4", nbars=len(bars), bars=bars, plan=plan, lead=lead, gtr=gtr, instrument=INSTR, motif=MOTIF, line_kinds=kinds_by,
           gtr_floor=FLOOR, gtr_stepped=STEPPED, total_eighths=TOT, seconds=secs,
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, fp=c["fp"], order_fp=R["order_fp"],
           survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()), by_construction=R["by_construction"],
           eighth_sec=EIGHTH_SEC, qbpm={"4/4": 72}, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p21/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{secs%60:04.1f});", len(lead), "sung notes;", len(gtr), "cue notes (stepped aside", STEPPED, "); fp", rec["fp"])
print("motif from the title cell:", MOTIF); print("phrases:", kinds_by)
for s, f in FLOOR.items(): print(" floor", s, f)
for s, nb, b0, met in plan: print(f"  {s:10s} bars {b0+1:3d}-{b0+nb:3d}")
