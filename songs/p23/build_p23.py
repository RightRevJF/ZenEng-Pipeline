"""Build the song record for 'What Holds' from the frozen melody ranking (#1): one male voice. Times in eighths at q = 104; each bar
carries metre, tempo, key and chord. The instrumental line (Module 27.21): the riff, on an overdriven guitar, in the intro, the riff
break after chorus 1, and the outro -- written from the title cell's first four notes ('what HOLDS is the'), each phrase's chord changes
anticipated by an eighth (the push ahead of the beat, Q tempo/feel A). 27.21 ships no ostinato kind; the run repeats the phrase (a riff
repeats) -- a finding."""
import pickle, sys
sys.path[:0] = ["/home/claude/p23"]
import melody_p23 as M, lyric as L
R = pickle.load(open("/home/claude/p23/melody_result.pkl", "rb"))
c = R["alive"][0]
KEY = {s: ("E minor" if s in ("Intro", "Verse 1", "Riff", "Verse 2", "Outro") else "G major") for s, *_ in M.FORM}
QB = 104
bars = [dict(sec=b["sec"], meter=b["meter"], chord=b["chord"], start=b["start"], len=b["len"], qbpm=QB, key=KEY[b["sec"]],
             build=b["sec"] == "Bridge", instrumental=b["sec"] in ("Intro", "Riff", "Outro")) for b in M.BARS]
def bar_at(e): return next(b for b in bars if b["start"] <= e < b["start"] + b["len"])
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        ln = M.SECS[s][li]
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=ln["role"], meter="4/4", singer="him"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = sum(b["len"] * 60 / QB / 2 for b in bars)
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, met))
# ---- Module 27.21: the riff ----
INSTR = dict(name="riff guitar", program=30, lo=40, hi=76, clef="treble_8", label="riff guitar (overdriven) -- sounds an octave below the written notes")
h0 = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
S = sorted(p for p in range(INSTR["lo"], INSTR["hi"] + 1) if p % 12 in M.EM)
def deg(p): return S.index(min(S, key=lambda q: abs(q - p)))
MOTIF = dict(steps=[deg(b["midi"]) - deg(a["midi"]) for a, b in zip(h0[:4], h0[1:4])], durs=[n["dur"] for n in h0[:4]],
             source=" ".join(n["syl"][0] for n in h0[:4]) + " (the title cell's first four notes)")
ROOTP = {"Em": 40, "C": 48, "D": 50, "G": 43, "Am": 45}       # the riff's low roots (E2, C3, D3)
def phrase(st, chords, pickup_ok, final=False):
    """one four-bar phrase: bar 1 the motif (its first note the push into the bar, its held note the chord's root an octave up),
    then the low root in eighths; bars 2-4 the root chugged, each change anticipated on the 'and' of 4 and tied across the bar"""
    out = []
    held = ROOTP[chords[0]] + 12                               # E3: the motif's long note
    d = deg(held); m = [S[d - MOTIF["steps"][0]], held]
    for stp in MOTIF["steps"][1:]: d += stp; m.append(S[d])
    du = MOTIF["durs"]
    if pickup_ok: out.append(dict(on=st - 1, dur=1, midi=m[0], src="motif:pickup"))
    pos = st
    for p, dd in zip(m[1:], du[1:]):
        out.append(dict(on=pos, dur=dd, midi=p, src="motif")); pos += dd
    while pos < st + 7: out.append(dict(on=pos, dur=1, midi=ROOTP[chords[0]], src="chug")); pos += 1
    for k in range(1, 4):
        b0 = st + 8 * k; ch = chords[k]; r = ROOTP[ch]
        if final and k == 3:
            out.append(dict(on=b0 - 1, dur=1 + 8, midi=r, src="push+final")); return out
        out.append(dict(on=b0 - 1, dur=3, midi=r, src="push"))          # the change an eighth early, tied over the bar line
        for e in range(2, 6): out.append(dict(on=b0 + e, dur=1, midi=r + (7 if (k == 3 and e == 4) else 0), src="chug"))
        out.append(dict(on=b0 + 6, dur=1, midi=r + (12 if k < 3 else 4), src="lick"))
    return out
riff, kinds_by = [], {}
for sec in ("Intro", "Riff", "Outro"):
    bs = [b for b in bars if b["sec"] == sec]; nph = len(bs) // 4; kinds_by[sec] = []
    for ph in range(nph):
        st = bs[4 * ph]["start"]; chords = [b["chord"] for b in bs[4 * ph:4 * ph + 4]]
        pk = not (sec == "Intro" and ph == 0)
        riff += phrase(st, chords, pk, final=(sec == "Outro" and ph == nph - 1)); kinds_by[sec].append("repeat")
riff.sort(key=lambda n: n["on"])
for a, b in zip(riff, riff[1:]):                                    # a tie never runs into the next note
    if a["on"] + a["dur"] > b["on"]: a["dur"] = b["on"] - a["on"]
def strong_pos(e): b = bar_at(e); return (e - b["start"]) in (0, 4)
def sounding(n, e): return n["on"] <= e < n["on"] + n["dur"]
def floor(sec):
    ns = [n for n in riff if bar_at(max(0, n["on"]))["sec"] == sec or (n["src"].startswith("motif:pickup") and bar_at(n["on"] + 1)["sec"] == sec)]
    bs = [b for b in bars if b["sec"] == sec]
    pts = [b["start"] + x for b in bs for x in (0, 4)]
    hits = [(e, next((n for n in ns if sounding(n, e)), None)) for e in pts]
    hits = [(e, n) for e, n in hits if n]
    ct = sum(1 for e, n in hits if n["midi"] % 12 in M.CH[bar_at(e)["chord"]]) / max(1, len(hits))
    phs = [(bs[4 * k]["start"], bs[4 * k + 3]["start"] + 8) for k in range(len(bs) // 4)]
    phr = [len({n["midi"] for n in ns if a <= n["on"] < z}) for a, z in phs]
    span = [max(n["midi"] for n in ns if a <= n["on"] < z) - min(n["midi"] for n in ns if a <= n["on"] < z) for a, z in phs]
    rep = [sum(1 for x, y in zip(q, q[1:]) if x["midi"] == y["midi"]) / max(1, len(q) - 1) for q in [[n for n in ns if a <= n["on"] < z] for a, z in phs]]
    push = sum(1 for n in ns if n["src"].startswith("push")) / max(1, sum(1 for b in bs if (b["start"] - bs[0]["start"]) // 8 % 4 != 0))
    return dict(chord_tones_on_strong=(round(ct, 2), ct >= 0.8), distinct_pitches_a_phrase=(min(phr), min(phr) >= 3),
                span_a_phrase=(min(span), min(span) >= 7), repeated_note_share=(round(max(rep), 2), True),
                changes_anticipated=(round(push, 2), push >= 0.99),
                range=([min(n["midi"] for n in ns), max(n["midi"] for n in ns)], all(INSTR["lo"] <= n["midi"] <= INSTR["hi"] for n in ns)))
FLOOR = {s: floor(s) for s in ("Intro", "Riff", "Outro")}
voc = [(n["on"], n["on"] + n["dur"]) for n in lead]
assert not any(a < n["on"] + n["dur"] and n["on"] < b for n in riff for a, b in voc), "the riff overlaps the voice"
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], riff=riff, instrument=INSTR, motif=MOTIF, line_kinds=kinds_by,
           riff_floor=FLOOR, total_eighths=TOT, seconds=secs, singers=dict(him=M.HIM), singer_by_sec=L.SINGER,
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, fp=c["fp"], order_fp=R["order_fp"],
           survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()), by_construction=R["by_construction"],
           qbpm={"4/4": QB}, eighth_sec={"4/4": 60 / QB / 2}, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p23/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{secs%60:04.1f});", len(lead), "sung;", len(riff), "riff notes; fp", rec["fp"])
print("motif:", MOTIF)
for s, f in FLOOR.items(): print(" floor", s, f)
