"""The Small Things (song 50): the song record from melody_final.pkl (the pick of record) and the 438 chart. Gentle acoustic folk, D major,
q = 88 swung (the swing only in the playing; the record straight), 96 bars, all 4/4 (the sound, A; the swing, A; the form, C).
  Intro (4): the fingerpicked guitar alone; the piano hints at the hook ('I think God likes the small things') in bars 3-4, softly.
  Verse 1: the guitar picking (Travis: the thumb on the root and fifth, the fingers between); the bass enters halfway (bar 13).
  Chorus 1: the guitar picking fuller, the piano in soft half-note chords, the bass, brushes on the rim; harmony on the hook.
  Verse 2: the guitar picking, the bass, the piano's high answers between the lines.
  Chorus 2: as the first, brushes on the snare.
  Bridge (8): the guitar alone, low; a beat of silence (the whole band out) before 'and the holy showed up clear' (the bridge, A).
  Last Chorus: the guitar, the piano, the bass, brushes on the snare; harmony on every line; the last line slows (in the playing).
  Outro (4): the guitar picking, the piano's last echo of the hook; the last D held.
The sung sections' bass is written by the routine (bass_v134.py) on the engine's grid."""
import pickle, sys, random, collections
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p60"]
import io as _io, contextlib as _cl
with _cl.redirect_stdout(_io.StringIO()): import melody_l7_p60 as P
import bass_v134 as BV
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p60/melody_final.pkl", "rb")); c = F["pick"]
EB = 48; NB = P.NBARS; QB = 88
assert list(P.CHORD2) == list(F["run"]["chords2"]), "the chart drawn on import differs from the run's"
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"afternoon": ["af", "ter", "noon"], "rolling": ["roll", "ing"], "itself": ["it", "self"], "across": ["a", "cross"], "Sammie": ["Sam", "mie"],
        "again": ["a", "gain"], "sliding": ["slid", "ing"], "bumblebee": ["bum", "ble", "bee"], "bouncing": ["bounc", "ing"], "Maggie": ["Mag", "gie"],
        "doesn't": ["does", "n't"], "even": ["e", "ven"], "somebody's": ["some", "bod", "y's"], "watching": ["watch", "ing"], "laughing": ["laugh", "ing"],
        "flying": ["fly", "ing"], "trying": ["try", "ing"], "moral": ["mor", "al"], "story": ["sto", "ry"], "lesson": ["les", "son"], "doing": ["do", "ing"],
        "sideways": ["side", "ways"], "remember": ["re", "mem", "ber"], "after": ["af", "ter"], "always": ["al", "ways"], "Nobody": ["No", "bod", "y"],
        "nobody": ["no", "bod", "y"], "Tuesday": ["Tues", "day"], "holy": ["ho", "ly"], "There's": ["There's"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",.;:?")
        if n <= 1: out.append((w, False)); continue
        parts = HFIX.get(w) or HFIX.get(core) or _PY.inserted(core).split("-")
        tail = "" if w in HFIX else w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1))
    assert len(out) == len(sy), (text, out, sy)
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
# ---- the record's bars: meters for the instrumentals ----
METERS = {}
LEN = {"4/4": 48, "7/8": 42, "5/4": 60}
MOV = {nm_: nm_ for nm_, _, _ in P.FORM}
def sp_(c_): return c_                                                                  # D major: no slash chords
H2 = [sp_(c_) for c_ in P.CHORD2]
bars = []; t = 0; RS = []                                                                # RS[b]: the record start of engine bar b
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k; met = METERS.get(nm, ["4/4"] * nb)[k]; L = LEN[met]
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, b=b, meter=met, start=t, len=L, chord=H2[2 * b], chord2=H2[2 * b + 1] if met == "4/4" else H2[2 * b],
                         roman=M.ROMAN[H2[2 * b].split("/")[0]], qbpm=QB, key="D major", movement=MOV[nm], stop=False))
        RS.append(t); t += L
REC_END = t
def rt(on):
    """an engine time (4/4 grid) in record time, by the engine bar it falls in."""
    b = max(0, min(NB - 1, on // EB)); return RS[b] + (on - b * EB) * bars[b]["len"] // EB if bars[b]["meter"] != "4/4" else RS[b] + on - b * EB
SEC0 = {nm: RS[P.BAR0[nm]] for nm, _, _ in P.FORM}
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); tx, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=rt(n["on"]), on_engine=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=tx, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice"))
CH = {sp_(k_): v_ for k_, v_ in M.CH.items()}
def tones(ch): return CH[ch][1]
def up_to(p, pcs, k=1):
    q = p
    for _ in range(k):
        q += 1
        while q % 12 not in pcs: q += 1
    return q
def down_to(p, pcs, k=1):
    q = p
    for _ in range(k):
        q -= 1
        while q % 12 not in pcs: q -= 1
    return q
def chord_at_rec(t_):
    b_ = next(x for x in reversed(bars) if x["start"] <= t_)
    return b_["chord2"] if (b_["meter"] == "4/4" and t_ - b_["start"] >= 24) else b_["chord"]
# ---- three-part harmony: on the hook everywhere, on every line of the last chorus ----
harm_hi, harm_lo = [], []
for n in lead:
    if not ((n["role"] in ("hook", "tag")) or n["sec"] == "Last Chorus"): continue
    ch = chord_at_rec(n["on"]); ct = tones(ch); sc = M.SCALE
    hi_ = next((q for q in range(n["midi"] + 3, n["midi"] + 6) if q % 12 in ct), up_to(n["midi"], sc, 2))
    lo_ = next((q for q in range(n["midi"] - 3, n["midi"] - 6, -1) if q % 12 in ct), down_to(n["midi"], sc, 2))
    harm_hi.append(dict(n, midi=hi_, singer="harmony high")); harm_lo.append(dict(n, midi=lo_, singer="harmony low"))
# ---- the band ----
parts = collections.defaultdict(list)
def ev(part, on, dur, p, vel, art="", **kw): parts[part].append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=int(vel), art=art, **kw))
DR = dict(kick=36, snare=38, rim=37, hat=42, ohat=46, ride=51, crash=49, tom_hi=48, tom_mid=45, tom_lo=41)
def voicing(ch, lo=55, n=4):
    out, p = [], lo
    while len(out) < n:
        if p % 12 in tones(ch): out.append(p)
        p += 1
    return out
def travis(st, L, ch, vel, lo=40):
    """the fingerpicked guitar: the thumb on the root (beats 1, 3) and the fifth (2, 4), the fingers on the chord's upper notes between."""
    r = lo + (BV.bass_pc(ch) - lo) % 12; f5 = r + 7 if r + 7 <= 52 else r - 5; up = voicing(ch, 55, 3)
    for e, p in ((0, r), (6, up[1]), (12, f5), (18, up[2]), (24, r), (30, up[0]), (36, f5), (42, up[1])):
        if e < L: ev("guitar", st + e, 6 if e % 12 else 12, p, vel + (6 if e % 12 == 0 else -4))
def strum(st, L, ch, vel, eighths=False):
    vc = voicing(ch, 43, 6)
    for e in range(0, L, 6 if eighths else 12): ev("guitar", st + e, 6 if eighths else 12, vc, vel + (8 if e % 24 == 0 else 0) - (6 if e % 12 else 0))
def brush(st, vel, style="rim"):
    ev("drums", st, 3, DR["kick"], vel - 14); ev("drums", st + 24, 3, DR["kick"], vel - 20)
    for e in (12, 36): ev("drums", st + e, 3, DR["rim"] if style == "rim" else DR["snare"], vel - (16 if style == "rim" else 8))
    for e in range(0, 48, 12 if style == "rim" else 6): ev("drums", st + e, 3, DR["ride"], vel - 30 + (6 if e % 12 == 0 else 0))
def sticks(st, vel):
    for e in (0, 18, 24): ev("drums", st + e, 3, DR["kick"], vel - (10 if e == 18 else 0))
    for e in (12, 36): ev("drums", st + e, 3, DR["snare"], vel - 2)
    for e in range(0, 48, 6): ev("drums", st + e, 3, DR["ride"], vel - 26 + (8 if e % 12 == 0 else 0))
L3 = RS[P.BAR0["Bridge"] + 6]                                                          # the bridge's last line: a beat of silence before it (the bridge, A)
for x in bars:
    sec, kind, st, k, nb, L = x["sec"], x["kind"], x["start"], x["k"], x["n"], x["len"]
    ch, ch2 = x["chord"], x["chord2"]
    if sec == "Intro":
        travis(st, 24, ch, 60); travis(st + 24, 24, ch2, 60)
        if k == 2:                                                                          # the hook hinted on the piano, an octave up
            for (tt, p, d) in P.HOOK[6]: ev("piano", st + tt, min(d, 2 * L - tt), p + 12, 50)
    elif sec in ("Verse 1", "Verse 2"):
        travis(st, 24, ch, 56 if sec == "Verse 1" else 60); travis(st + 24, 24, ch2, 56 if sec == "Verse 1" else 60)
        if sec == "Verse 2" and k % 2 == 1: ev("piano", st + 36, 12, voicing(ch2, 74, 1), 44)   # the piano's answer at the line's end
    elif kind == "Chorus":
        last = sec == "Last Chorus"
        for h, cc in enumerate((ch, ch2)):
            travis(st + 24 * h, 24, cc, 66 if last else 62)
            ev("piano", st + 24 * h, 24, voicing(cc, 50, 4), 58 if last else (54 if sec == "Chorus 2" else 50))
        if sec == "Chorus 1": brush(st, 58, "rim")
        if sec == "Chorus 2": brush(st, 68, "snare")
        if last: brush(st, 74, "snare")
    elif sec == "Bridge":
        if k == 6: travis(st + 12, 12, ch, 50); travis(st + 24, 24, ch2, 52)                # the beat of silence, then the guitar again
        else: travis(st, 24, ch, 50); travis(st + 24, 24, ch2, 50)
    elif sec == "Outro":
        if k < 3:
            travis(st, 24, ch, 56 - 4 * k); travis(st + 24, 24, ch2, 54 - 4 * k)
            if k == 1:
                for (tt, p, d) in P.HOOK[7]: ev("piano", st + tt, min(d, 2 * L - tt), p + 12, 46)
        else: ev("guitar", st, L, voicing("D", 50, 5), 58); ev("piano", st, L, voicing("D", 62, 3), 44); ev("bass", st, L, 38, 56)
for n in lead:                                                                            # nothing sounds in the bridge's beat of silence
    if n["on"] < L3 < n["on"] + n["dur"]: n["dur"] = L3 - n["on"]
# ---- the sung sections' bass: the routine on the engine's grid ----
ebars = [dict(sec=nm, kind=kind, k=k, n=nb, chord=H2[2 * (P.BAR0[nm] + k)], start=(P.BAR0[nm] + k) * EB, len=EB) for nm, kind, nb in P.FORM for k in range(nb)]
edrums = [dict(e, on=e["on"] - SEC0[bars[_b]["sec"]] + P.BAR0[bars[_b]["sec"]] * EB) for e in parts["drums"] for _b in [next(i_ for i_ in range(NB - 1, -1, -1) if bars[i_]["start"] <= e["on"])] if bars[_b]["sec"] in P.SUNG]
erec = dict(bars=ebars, chords2=list(P.CHORD2), drums=edrums, lead=[dict(n, on=n["on_engine"]) for n in lead])
BV.SCALE_AT[0] = None
BB, tries = BV.write_bass(erec, 38, (2, "major"), "50")
def bass_on(sec, k):
    return (sec == "Verse 1" and k >= 8) or sec in ("Verse 2", "Chorus 1", "Chorus 2", "Last Chorus")   # the bass in halfway through verse 1; out of the bridge
for e in BB:
    b = e["on"] // EB; x = bars[b]
    if x["sec"] in P.SUNG and bass_on(x["sec"], x["k"]): parts["bass"].append(dict(e, on=rt(e["on"])))
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"] and out[-1]["art"] == e["art"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); continue
        out.append(e)
    return out
for e in parts["bass"]: e["p"] = [q + 12 if q < 28 else q for q in e["p"]]                 # the acoustic bass's low E (E1) is its floor
PARTS = {k: tidy(v) for k, v in parts.items()}
plan = []
for nm, kind, nb in P.FORM:
    mets = METERS.get(nm, ["4/4"] * nb); plan.append((nm, nb, SEC0[nm], mets, MOV[nm]))
secs = sum(x["len"] for x in bars) / 12 * 60 / QB
rec = dict(title="The Small Things", nbars=NB, bars=bars, chords2=H2, plan=plan, lead=lead, harm_hi=harm_hi, harm_lo=harm_lo, parts=PARTS, slot="twelfth of a beat",
           qbpm=QB, feel=P.FEEL, seconds=secs, tw_sec=60 / QB / 12, end=REC_END, meters=METERS, movements=MOV,
           fp=c["fp"], order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"],
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, judge={k: c["judge"][k] for k in ("combined", "content", "order")},
           plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"], kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()},
           rerun=F["run"]["rerun"], text=TEXT, registers=c["meta"]["registers"], carriers=c["meta"]["carriers"],
           design=dict(gates=P.DESIGN_GATES, hook=P.HOOK, bridge=P.LIFTL, bridge_low=P.BRIDGE_LOW, slots={s: P.slots_of(s) for s in P.SUNG}), chart438=F["run"]["rerun"].get("chart438"),
           bass_written_by="bass_v134.py write_bass (the sung sections, on the engine's grid); the intro and outro have none", bass_tries=tries)
pickle.dump(rec, open("/home/claude/p60/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{secs % 60:04.1f});", len(lead), "sung;", {k: len(v) for k, v in PARTS.items()}, "harmony", len(harm_hi), "bass tries", tries)
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t_ + ("-" if h else "") for t_, h in ws))
