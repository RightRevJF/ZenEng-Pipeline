"""Build the song record for 'The Seam' from the frozen melody ranking (#1): a duet. Times in eighths at q = 80; each bar carries metre
(4/4, or 7/8 as 2+2+3 in the instrumental), tempo, key and chord. HER verses (E minor), HIS verses (F minor), the CHORUS hers with
HIS harmony a third (or a sixth) below on chord tones, HIS ending. The instrumental lines (Module 27.21): intro, interlude,
instrumental (48 bars of 7/8, a build by thirds) and outro, on the synth lead (Q12 A), notated as a cue voice."""
import pickle, sys, random
sys.path[:0] = ["/home/claude/p22"]
import melody_p22 as M, lyric as L
R = pickle.load(open("/home/claude/p22/melody_result.pkl", "rb"))
c = R["alive"][0]
KEY = {"Intro": "E minor", "Verse 1": "E minor", "Verse 3": "E minor", "Verse 2": "F minor", "Verse 4": "F minor", "Chorus 1": "C major",
       "Chorus 2": "C major", "Chorus 3": "C major", "Interlude": "C major", "Instrumental": "F minor", "Ending": "F minor", "Outro": "F minor"}
SCALE = {"E minor": M.EM, "F minor": M.FM, "C major": M.CM}
bars = [dict(sec=b["sec"], meter=b["meter"], chord=b["chord"], start=b["start"], len=b["len"], qbpm=80, key=KEY[b["sec"]],
             build=b["sec"] == "Instrumental", instrumental=b["sec"] in ("Intro", "Interlude", "Instrumental", "Outro")) for b in M.BARS]
def bar_at(e): return next(b for b in bars if b["start"] <= e < b["start"] + b["len"])
lead = []
for s in M.SINGS:
    who = L.SINGER[s]
    for o, d, p, x, li in c[s]:
        ln = M.SECS[s][li]
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=ln["role"], meter="4/4", singer="her" if who in ("her", "both") else "him"))
lead.sort(key=lambda n: n["on"])
# his harmony in the choruses: a third below her, a chord tone on the strong beats (else a sixth), inside his row
CMS = sorted(p for p in range(40, 80) if p % 12 in M.CM)
harm = []
for n in lead:
    if not n["sec"].startswith("Chorus"): continue
    b = bar_at(n["on"]); ch = M.CH[b["chord"]]; top = 69 if n["sec"] == "Chorus 3" and n["line"] == 3 else 67
    strong = (n["on"] - b["start"]) % 4 == 0
    i = CMS.index(n["midi"]) if n["midi"] in CMS else None
    third = CMS[i - 2] if i is not None else n["midi"] - 3
    p = third
    if (strong or n["dur"] >= 3) and third % 12 not in ch:
        opts = [q for q in range(n["midi"] - 9, n["midi"] - 2) if q % 12 in ch and 52 <= q <= top and n["midi"] - q in (3, 4, 8, 9)]
        if opts: p = min(opts, key=lambda q: abs((n["midi"] - q) - 4) if (n["midi"] - q) in (3, 4) else 10 + abs((n["midi"] - q) - 8))
    while p > top: p -= 12
    while p < 52: p += 12
    harm.append(dict(on=n["on"], dur=n["dur"], midi=p, syl=n["syl"], sec=n["sec"], line=n["line"], singer="him"))
TOT = M.TOTAL; secs = sum(b["len"] * 60 / 80 / 2 for b in bars)
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, met))
# ---- Module 27.21: the instrumental lines, on the synth lead ----
INSTR = dict(name="synth lead", program=81, lo=48, hi=84, clef="treble", label="cue: synth lead -- treble clef, sounds as written")
h0 = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
def degs(sc): return sorted(p for p in range(INSTR["lo"], INSTR["hi"] + 1) if p % 12 in sc)
def step_of(sc, a, b):
    s_ = degs(sc); return s_.index(min(s_, key=lambda q: abs(q - b))) - s_.index(min(s_, key=lambda q: abs(q - a)))
MOTIF = dict(steps=[step_of(M.CM, a["midi"], b["midi"]) for a, b in zip(h0[:4], h0[1:4])], durs=[n["dur"] for n in h0[:4]],
             source=" ".join(n["syl"][0] for n in h0[:4]) + " (the title cell's first four notes)")
base = MOTIF["durs"][0]; RATIO = [d / base for d in MOTIF["durs"]]
SEQ_PLAIN = ["repeat", "tonal", "inverted", "varied", "tonal", "repeat"]
def transform(kind, steps):
    if kind == "inverted": return [-s for s in steps]
    if kind == "varied": return steps[:-1] + [steps[-1] + (1 if steps[-1] <= 0 else -1)]
    return list(steps)
rng = random.Random(2201)
def strong_pos(b, pos):
    rel = pos - b["start"]; return rel in M.METER[b["meter"]]["beats"]
def write_line(sec, center, build=False):
    bs = [b for b in bars if b["sec"] == sec]; nph = len(bs) // 4; out = []; kinds = []
    sc = SCALE[bs[0]["key"]]; S = degs(sc)
    peak_ph = max(1, (nph + 1) // 2) if nph > 1 else 0
    prev = None
    for ph in range(nph):
        if build:
            third = (3 * ph) // nph; kind = ["augmented", "tonal", "diminished"][third]
            fill = [4, 2, 1][third]; mult = [2.0, 1.0, 0.5][third]
            cen = center + 2 * ph; ceiling = min(INSTR["hi"], center + 6 + 2 * ph)
        else:
            kind = SEQ_PLAIN[ph % len(SEQ_PLAIN)]; fill = 2; mult = 1.0
            cen = center + (2 if kind == "tonal" else 0) + (4 if ph == peak_ph and nph > 1 else 0); ceiling = cen + 7
        kinds.append(kind)
        st = bs[4 * ph]["start"]; end = bs[4 * ph + 3]["start"] + bs[4 * ph + 3]["len"]
        ch0 = M.CH[bs[4 * ph]["chord"]]
        start = min([p for p in S if p % 12 in ch0 and p <= ceiling], key=lambda q: abs(q - cen))
        d0 = S.index(start); pos = st
        stps = [0] + transform("repeat" if build and kind != "tonal" else kind, MOTIF["steps"])
        if build and kind == "tonal": d0 = min(len(S) - 1, d0 + 2)
        for k, stp in enumerate(stps):
            d0 = max(0, min(len(S) - 1, d0 + stp)); p = S[d0]
            while p > ceiling: d0 -= 7; p = S[d0]
            du = max(1, int(round(base * RATIO[k] * mult)))
            if pos + du > end: break
            out.append(dict(on=pos, dur=du, midi=p, sec=sec, src="motif:" + kind)); pos += du
        prev = out[-1]["midi"]; dirn = 1
        while pos < end:
            b = bar_at(pos); last = end - pos <= max(fill, 2) * 2 and not build
            du = min(4 if last else fill, end - pos, b["start"] + b["len"] - pos) if not build else min(fill, end - pos)
            floor_ = ceiling - (12 if build else 9)
            if build:                                                  # runs: a direction kept, turned at the ceiling and the floor
                i = S.index(prev)
                nx = S[max(0, min(len(S) - 1, i + dirn))]
                if nx > ceiling or nx < floor_: dirn = -dirn
                if strong_pos(b, pos):
                    cands = [p for p in S if p % 12 in M.CH[b["chord"]] and floor_ <= p <= ceiling and 0 < (p - prev) * dirn <= 5]
                    if ph == nph - 1 and pos >= end - 7: cands = [max(p for p in S if p % 12 in M.CH[b["chord"]] and p <= ceiling)]
                    if not cands:                                          # the direction cannot reach a chord tone: the nearest one, and turn
                        cands = [p for p in S if p % 12 in M.CH[b["chord"]] and floor_ - 3 <= p <= ceiling and p != prev] or [prev]; dirn = -dirn
                    p = min(cands, key=lambda q: abs(q - prev))
                else:
                    p = S[max(0, min(len(S) - 1, i + dirn))]
                if rng.random() < 0.12: dirn = -dirn
            elif strong_pos(b, pos) or last:
                cands = [p for p in S if p % 12 in M.CH[b["chord"]] and abs(S.index(p) - S.index(prev)) <= 3 and p <= ceiling]
                arc = cen + 4.0 * __import__("math").sin(__import__("math").pi * (pos - st) / max(1, end - st))   # an arch through the phrase
                p = min(cands, key=lambda q: abs(q - arc) + 0.4 * abs(q - prev)) if cands else prev
            else:
                nb = bar_at(min(TOT - 1, pos + du)); tgt = [q for q in S if q % 12 in M.CH[nb["chord"]] and q != prev]
                t_ = min(tgt, key=lambda q: abs(q - prev)); p = S[min(len(S) - 1, max(0, S.index(prev) + (1 if t_ > prev else -1)))]
                if p > ceiling: p = S[S.index(prev) - 1]
            out.append(dict(on=pos, dur=du, midi=p, sec=sec, src="fill")); prev = p; pos += du
    return out, kinds
syn, kinds_by = [], {}
for sec, cen, bld in (("Intro", 64, False), ("Interlude", 67, False), ("Instrumental", 62, True), ("Outro", 62, False)):
    ln_, kd = write_line(sec, cen, bld); syn += ln_; kinds_by[sec] = kd
og = [n for n in syn if n["sec"] == "Outro"]; og[-1]["midi"] = min([p for p in degs(M.FM) + [57, 69] if p % 12 == 9], key=lambda q: abs(q - og[-1]["midi"]))
def floor(sec):
    ns = [n for n in syn if n["sec"] == sec]; bs = [b for b in bars if b["sec"] == sec]; st0 = bs[0]["start"]; L_ = sum(b["len"] for b in bs)
    strong = [n for n in ns if strong_pos(bar_at(n["on"]), n["on"])]
    ct = sum(1 for n in strong if n["midi"] % 12 in M.CH[bar_at(n["on"])["chord"]]) / max(1, len(strong))
    phs = [(bs[4 * k]["start"], bs[4 * k + 3]["start"] + bs[4 * k + 3]["len"]) for k in range(len(bs) // 4)]
    phr = [len({n["midi"] for n in ns if a <= n["on"] < z}) for a, z in phs]
    dens = [round(sum(1 for n in ns if a <= n["on"] < z) / 4, 2) for a, z in phs]
    pk = max(ns, key=lambda n: (n["midi"], n["on"])); place = (pk["on"] - st0) / L_
    build = bs[0]["build"]
    rows = dict(chord_tones_on_strong=(round(ct, 2), ct >= 0.8), distinct_pitches_a_phrase=(min(phr), min(phr) >= 3),
                peak_place=(round(place, 2), (0.67 <= place <= 1.0) if build else (place > 1 / 3 if len(phs) > 1 else True)),
                density_rising=(dens, all(b_ >= a_ for a_, b_ in zip(dens, dens[1:])) and dens[-1] > dens[0]) if build else (dens, True),
                range=([min(n["midi"] for n in ns), max(n["midi"] for n in ns)], all(INSTR["lo"] <= n["midi"] <= INSTR["hi"] for n in ns)))
    return rows
FLOOR = {s: floor(s) for s in ("Intro", "Interlude", "Instrumental", "Outro")}
syn.sort(key=lambda n: n["on"])
voc = [(n["on"], n["on"] + n["dur"]) for n in lead]
def clash(n): return any(a < n["on"] + n["dur"] and n["on"] < b for a, b in voc)
kept = []
for n in syn:
    if not clash(n): kept.append(n); continue
    nxt = min((a for a, b in voc if a > n["on"]), default=None)
    if nxt is not None and not any(a <= n["on"] < b for a, b in voc) and nxt - n["on"] >= 1: kept.append(dict(n, dur=nxt - n["on"]))
STEPPED = sum(1 for a in syn if a not in kept); syn = kept
assert all(a["on"] + a["dur"] <= b["on"] for a, b in zip(syn, syn[1:]))
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=harm, gtr=syn, instrument=INSTR, motif=MOTIF, line_kinds=kinds_by,
           gtr_floor=FLOOR, gtr_stepped=STEPPED, total_eighths=TOT, seconds=secs, singers=dict(her=M.HER, him=M.HIM), singer_by_sec=L.SINGER,
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, fp=c["fp"], order_fp=R["order_fp"],
           survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()), by_construction=R["by_construction"],
           qbpm={"4/4": 80, "7/8": 80}, eighth_sec={"4/4": 60 / 80 / 2, "7/8": 60 / 80 / 2}, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p22/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{secs%60:04.1f});", len(lead), "sung;", len(harm), "harmony;", len(syn), "cue (stepped", STEPPED, "); fp", rec["fp"])
print("motif:", MOTIF); print("phrases:", kinds_by)
for s, f in FLOOR.items(): print(" floor", s, f)
print("harmony intervals:", sorted({n["midi"] - h["midi"] for n, h in zip([x for x in lead if x["sec"].startswith("Chorus")], harm)}))
print("his harmony range:", min(h["midi"] for h in harm), max(h["midi"] for h in harm))
