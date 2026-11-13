"""The Ratios Hold (song 48): the song record from melody_final.pkl (the pick of record) and the 438 chart. Symphonic prog in five
movements, E major, q = 92, 174 bars (the form, A; the arrangement, A). The engine draws the sung sections on a 4/4 grid; the record gives
the instrumentals their meters and lays every section end to end in record time (a twelfth of a beat; 4/4 = 48, 7/8 = 42, 5/4 = 60).
  I    Overture (24): sixteen bars of 7/8, the pattern theme on the Moog over Hammond, pick bass and drums; eight of 4/4, the clean guitar
       foreshadowing the hook's figure over a Mellotron swell.
  II   The letter: the verses bass-led (the routine) under clean guitar arpeggios and a light kit; the choruses open into Mellotron choir and
       Hammond, the full kit, three-part harmony on the hook.
  III  The study (48): sixteen bars of 7/8 (the theme, Moog then guitar), eight of 5/4 (the guitar's long line), eight of 7/8 (Moog and guitar
       a bar each), eight of 4/4 on the acoustic guitar alone, eight of 4/4 building, the theme in octaves on Moog and guitar.
  IV   The window closes (10): eight bars of piano alone, then two bars of silence. The bridge: piano and voice; bass and drums back on the
       last pair.
  V    The last chorus: church organ at the summit, Mellotron choir, the full kit with ride, three-part harmony on every line; the tag the
       hook twice with harmony; the coda (24) the theme in quarters on the Moog over the church organ, ending on the organ's E chord.
The bass of the sung sections is written by the routine (bass_v134.py) on the engine's grid; the instrumentals' bass by the figures here."""
import pickle, sys, random, collections
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p58"]
import melody_v134_p58 as P
import bass_v134 as BV
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p58/melody_final.pkl", "rb")); c = F["pick"]
EB = 48; NB = P.NBARS; QB = 92
assert list(P.CHORD2) == list(F["run"]["chords2"]), "the chart drawn on import differs from the run's"
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"remember": ["re", "mem", "ber"], "never": ["nev", "er"], "letters": ["let", "ters"], "heartbeat": ["heart", "beat"], "stumble,": ["stum", "ble,"],
        "stumble": ["stum", "ble"], "music": ["mu", "sic"], "only": ["on", "ly"], "faces": ["fac", "es"], "every": ["ev", "ery"], "ratios": ["ra", "ti", "os"],
        "Something": ["Some", "thing"], "singing": ["sing", "ing"], "chisel": ["chis", "el"], "shavings": ["shav", "ings"], "forty": ["for", "ty"],
        "heartbeats,": ["heart", "beats,"], "carried": ["car", "ried"], "workbench": ["work", "bench"], "letter": ["let", "ter"], "before": ["be", "fore"],
        "ever": ["ev", "er"], "doesn't": ["does", "n't"], "reading,": ["read", "ing,"], "remembering": ["re", "mem", "ber", "ing"], "Whoever": ["Who", "ev", "er"],
        "instrument": ["in", "stru", "ment"], "ready": ["rea", "dy"], "cannot": ["can", "not"], "Singer": ["Sing", "er"], "believe": ["be", "lieve"],
        "into": ["in", "to"], "Dear": ["Dear"], "never,": ["nev", "er,"], "spruce": ["spruce"], "inside": ["in", "side"], "watched": ["watched"]}
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
METERS = {"Overture": ["7/8"] * 16 + ["4/4"] * 8, "Study": ["7/8"] * 16 + ["5/4"] * 8 + ["7/8"] * 8 + ["4/4"] * 16}
LEN = {"4/4": 48, "7/8": 42, "5/4": 60}
MOV = {"Overture": "I. Overture", "Verse 1": "II. The Letter", "Chorus 1": "II. The Letter", "Verse 2": "II. The Letter", "Chorus 2": "II. The Letter",
       "Study": "III. The Study", "Window": "IV. The Window Closes", "Bridge": "IV. The Window Closes", "Last Chorus": "V. Last Chorus", "Tag": "V. Last Chorus", "Coda": "V. Last Chorus"}
def sp_(c_): return c_.replace("/Ab", "/G#").replace("/Db", "/C#").replace("/Eb", "/D#")      # the slash bass spelled in E major (sharps)
H2 = [sp_(c_) for c_ in P.CHORD2]
bars = []; t = 0; RS = []                                                                # RS[b]: the record start of engine bar b
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k; met = METERS.get(nm, ["4/4"] * nb)[k]; L = LEN[met]
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, b=b, meter=met, start=t, len=L, chord=H2[2 * b], chord2=H2[2 * b + 1] if met == "4/4" else H2[2 * b],
                         roman=M.ROMAN[H2[2 * b].split("/")[0]], qbpm=QB, key="E major", movement=MOV[nm], stop=(nm == "Window" and k >= 8)))
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
# ---- three-part harmony: on the hook everywhere, on every line of the last chorus (the arrangement, A) ----
harm_hi, harm_lo = [], []
for n in lead:
    if not ((n["role"] == "hook") or n["sec"] == "Last Chorus"): continue
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
STEP = {"E": 0, "F#m": 1, "G#m": 2, "A": 3, "B": 4, "C#m": 5}
THEME = [76, 71, 69, 68, 64, 66, 68]                                                     # the pattern theme over E: E5 B4 A4 G#4 E4 F#4 G#4 (2+2+3)
def theme_on(ch, var=0):
    """the theme moved by scale steps to the chord's root (D: a whole step down, the flat seventh); var 1 reversed."""
    th = THEME[::-1] if var == 1 else THEME
    ch = ch.split("/")[0]
    if ch == "D": q = [x - 2 for x in th]
    else:
        k = STEP[ch]; q = [P.sstep(x, k) for x in th]
    while max(q) > 78: q = [x - 12 for x in q]
    while min(q) < 60: q = [x + 12 for x in q]
    return q
def kit_7_8(st, vel, full=True):
    for e in (0, 24): ev("drums", st + e, 3, DR["kick"], vel)
    for e in (12, 30): ev("drums", st + e, 3, DR["snare"], vel - 4)
    for e in range(0, 42, 6): ev("drums", st + e, 3, DR["hat"] if full else DR["ride"], vel - 26 + (8 if e in (0, 12, 24) else 0))
def kit_5_4(st, vel):
    for e in (0, 24, 42): ev("drums", st + e, 3, DR["kick"], vel)
    for e in (12, 36, 54): ev("drums", st + e, 3, DR["snare"], vel - 4)
    for e in range(0, 60, 6): ev("drums", st + e, 3, DR["hat"], vel - 26 + (8 if e % 12 == 0 else 0))
def kit_4_4(st, vel, style="full"):
    if style == "light":
        ev("drums", st, 3, DR["kick"], vel - 10); ev("drums", st + 30, 3, DR["kick"], vel - 18)
        for e in (12, 36): ev("drums", st + e, 3, DR["rim"], vel - 12)
        for e in range(0, 48, 6): ev("drums", st + e, 3, DR["hat"], vel - 34 + (6 if e % 12 == 0 else 0))
    elif style == "half":
        ev("drums", st, 3, DR["kick"], vel); ev("drums", st + 24, 3, DR["snare"], vel - 4)
        for e in range(0, 48, 12): ev("drums", st + e, 3, DR["ride"], vel - 24)
    else:
        for e in (0, 18, 24): ev("drums", st + e, 3, DR["kick"], vel - (10 if e == 18 else 0))
        for e in (12, 36): ev("drums", st + e, 3, DR["snare"], vel - 2)
        for e in range(0, 48, 6): ev("drums", st + e, 3, DR["ride"] if style == "ride" else DR["hat"], vel - 26 + (8 if e % 12 == 0 else 0))
def bass_fig(st, L, ch, vel):
    """the instrumentals' bass: the root in eighths, the 2+2+3 groups accented, the fifth on the third group's middle eighth."""
    bp_ = BV.bass_pc(ch); r = 28 + (bp_ - 28) % 12; f5 = 28 + (CH[ch][0] + 7 - 28) % 12
    for e in range(0, L, 6):
        acc = e in (0, 12, 24) if L == 42 else e % 12 == 0
        p = f5 if (L == 42 and e == 30) or (L != 42 and e % 24 == 18) else r
        ev("bass", st + e, 5, p, vel + (10 if acc else 0), "pick")
for x in bars:
    sec, kind, st, k, nb, L, met = x["sec"], x["kind"], x["start"], x["k"], x["n"], x["len"], x["meter"]
    ch, ch2 = x["chord"], x["chord2"]
    if sec == "Overture":
        if met == "7/8":
            th = theme_on(ch, 0)
            for j, p in enumerate(th): ev("moog", st + 6 * j, 6 if j < 6 else 6, p, 84 + (8 if j in (0, 2, 4) else 0))
            ev("hammond", st, L, voicing(ch, 55), 70); bass_fig(st, L, ch, 74); kit_7_8(st, 92)
            if k == 0: ev("drums", st, 6, DR["crash"], 100)
        else:
            j8 = k - 16
            ev("strings", st, L, voicing(ch, 52, 5), 52 + 4 * j8)
            if j8 % 2 == 0:                                                                # the hook's figure, foreshadowed on the clean guitar
                for (tt, p, d) in P.HOOK[3]: ev("guitar", st + tt - 24, d if d else 24, p, 72)
            ev("hammond", st, L, voicing(ch, 55), 56); bass_fig(st, L, ch, 62)
            if j8 >= 4: kit_4_4(st, 70, "light")
    elif sec in ("Verse 1", "Verse 2"):
        for h, cc in enumerate((ch, ch2)):                                                # clean guitar arpeggios, eighths
            vc = voicing(cc, 59, 4)
            for j, e in enumerate(range(0, 24, 6)): ev("guitar", st + 24 * h + e, 6, vc[(0, 2, 1, 3)[j]], 58 + (6 if sec == "Verse 2" else 0))
        kit_4_4(st, 72 if sec == "Verse 2" else 64, "light")
    elif kind == "Chorus" or sec == "Tag":
        last = sec == "Last Chorus" or sec == "Tag"
        for h, cc in enumerate((ch, ch2)):
            ev("organ" if last else "hammond", st + 24 * h, 24, voicing(cc, 52 if last else 55, 5 if last else 4), 78 if last else 64)
            ev("choir", st + 24 * h, 24, voicing(cc, 60, 3), 72 if last else 52)
            if last: ev("hammond", st + 24 * h, 24, voicing(cc, 55, 4), 70); ev("strings", st + 24 * h, 24, voicing(cc, 64, 3), 64)
            for e in ((0, 6, 12, 18) if last else (0, 12)): ev("guitar", st + 24 * h + e, 5 if last else 10, [p for p in voicing(cc, 52, 3)], 76 if last else 60)
        kit_4_4(st, 100 if last else 86, "ride" if last else "full")
        if k == 0: ev("drums", st, 6, DR["crash"], 104 if last else 96)
    elif sec == "Study":
        if met == "7/8" and k < 16:
            inst = "moog" if k < 8 else "guitar"; th = theme_on(ch, k % 2)
            for j, p in enumerate(th): ev(inst, st + 6 * j, 6, p, 82 + (8 if j in (0, 2, 4) else 0))
            ev("hammond", st, L, voicing(ch, 55), 60); bass_fig(st, L, ch, 70); kit_7_8(st, 84)
        elif met == "5/4":                                                                 # the guitar's long line: the theme and three notes more
            th = theme_on(ch, 0); line = th + [P.sstep(th[-1], 1), P.sstep(th[-1], 2), P.sstep(th[-1], 1)]
            for j, p in enumerate(line): ev("guitar", st + 6 * j, 6, p, 82 + (8 if j % 2 == 0 else 0))
            ev("strings", st, L, voicing(ch, 52, 5), 54); bass_fig(st, L, ch, 70); kit_5_4(st, 84)
        elif met == "7/8":                                                                 # the exchange: Moog and guitar a bar each
            inst = "moog" if k % 2 == 0 else "guitar"; th = theme_on(ch, (k // 2) % 2)
            for j, p in enumerate(th): ev(inst, st + 6 * j, 6, p, 88)
            ev("hammond", st, L, voicing(ch, 55), 64); bass_fig(st, L, ch, 72); kit_7_8(st, 88)
        elif k < 40:                                                                       # the acoustic guitar alone
            for h, cc in enumerate((ch, ch2)):
                vc = voicing(cc, 52, 5)
                for j, e in enumerate(range(0, 24, 3)): ev("acoustic", st + 24 * h + e, 3, vc[(0, 2, 4, 3, 1, 3, 2, 4)[j]], 56)
        else:                                                                              # the build: the theme in octaves, 4/4 (seven eighths and a rest)
            th = theme_on(ch, 0); g = k - 40
            for j, p in enumerate(th): ev("moog", st + 6 * j, 6, p, 70 + 4 * g); ev("guitar", st + 6 * j, 6, p - 12, 66 + 4 * g)
            ev("hammond", st, L, voicing(ch, 55), 60 + 3 * g); bass_fig(st, L, ch, 66 + 3 * g); kit_4_4(st, 74 + 3 * g)
            if g == 7: [ev("drums", st + e, 3, DR[tm], 90) for e, tm in ((24, "tom_hi"), (30, "tom_hi"), (36, "tom_mid"), (42, "tom_lo"))]
    elif sec == "Window":
        if k < 8:                                                                          # piano alone, softer each bar
            for h, cc in enumerate((ch, ch2)):
                vc = voicing(cc, 48, 5)
                for j, e in enumerate(range(0, 24, 6)): ev("piano", st + 24 * h + e, 12, vc[(0, 2, 4, 3)[j]], 60 - 3 * k)
        # bars 8-9: silence
    elif sec == "Bridge":
        for h, cc in enumerate((ch, ch2)):
            vc = voicing(cc, 48, 5); ev("piano", st + 24 * h, 24, vc[:1] + vc[2:], 50 + (10 if k >= 8 else 0) + 2 * k)
        if k >= 8:
            kit_4_4(st, 70 + 4 * (k - 8), "light" if k < 10 else "full")
            if k == 11: [ev("drums", st + e, 3, DR[tm], 92) for e, tm in ((24, "tom_hi"), (30, "tom_hi"), (36, "tom_mid"), (42, "tom_lo"))]
    elif sec == "Coda":                                                                    # the theme in quarters, a statement each two bars
        if k < 22:
            if k % 2 == 0:
                th = theme_on(ch, 0)
                for j, p in enumerate(th): ev("moog", st + 12 * j, 12, p, 70)
            ev("organ", st, L, voicing(ch, 48, 4), 58); ev("strings", st, L, voicing(ch, 52, 5), 50); bass_fig(st, L, ch, 64); kit_4_4(st, 74, "half")
        elif k == 22:
            ev("organ", st, 2 * L, voicing("E", 52, 5) + [76], 72); ev("strings", st, 2 * L, voicing("E", 52, 5), 56)
            ev("bass", st, 2 * L, 28, 70); ev("drums", st, 6, DR["crash"], 96); ev("drums", st, 3, DR["kick"], 90)
# ---- the sung sections' bass: the routine on the engine's grid ----
ebars = [dict(sec=nm, kind=kind, k=k, n=nb, chord=H2[2 * (P.BAR0[nm] + k)], start=(P.BAR0[nm] + k) * EB, len=EB) for nm, kind, nb in P.FORM for k in range(nb)]
edrums = [dict(e, on=e["on"] - SEC0[bars[_b]["sec"]] + P.BAR0[bars[_b]["sec"]] * EB) for e in parts["drums"] for _b in [next(i_ for i_ in range(NB - 1, -1, -1) if bars[i_]["start"] <= e["on"])] if bars[_b]["sec"] in P.SUNG]
erec = dict(bars=ebars, chords2=list(P.CHORD2), drums=edrums, lead=[dict(n, on=n["on_engine"]) for n in lead])
BV.SCALE_AT[0] = None
BB, tries = BV.write_bass(erec, 33, (4, "major"), "48")
def bass_on(sec, k):
    return sec in ("Verse 1", "Verse 2", "Chorus 1", "Chorus 2", "Last Chorus", "Tag") or (sec == "Bridge" and k >= 8)
for e in BB:
    b = e["on"] // EB; x = bars[b]
    if x["sec"] in P.SUNG and bass_on(x["sec"], x["k"]): parts["bass"].append(dict(e, on=rt(e["on"])))
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"] and out[-1]["art"] == e["art"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); continue
        out.append(e)
    return out
PARTS = {k: tidy(v) for k, v in parts.items()}
plan = []
for nm, kind, nb in P.FORM:
    mets = METERS.get(nm, ["4/4"] * nb); plan.append((nm, nb, SEC0[nm], mets, MOV[nm]))
secs = sum(x["len"] for x in bars) / 12 * 60 / QB
rec = dict(title="The Ratios Hold", nbars=NB, bars=bars, chords2=H2, plan=plan, lead=lead, harm_hi=harm_hi, harm_lo=harm_lo, parts=PARTS, slot="twelfth of a beat",
           qbpm=QB, feel=P.FEEL, seconds=secs, tw_sec=60 / QB / 12, end=REC_END, meters=METERS, movements=MOV,
           fp=c["fp"], order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"],
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, judge={k: c["judge"][k] for k in ("combined", "content", "order")},
           plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"], kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()},
           rerun=F["run"]["rerun"], text=TEXT, registers=c["meta"]["registers"], carriers=c["meta"]["carriers"],
           design=dict(gates=P.DESIGN_GATES, hook=P.HOOK, bridge=P.LIFTL, slots={s: P.slots_of(s) for s in P.SUNG}), chart438=F["run"]["rerun"].get("chart438"),
           bass_written_by="bass_v134.py write_bass (the sung sections, on the engine's grid); the instrumentals by build_p58.py's figures", bass_tries=tries)
pickle.dump(rec, open("/home/claude/p58/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{secs % 60:04.1f});", len(lead), "sung;", {k: len(v) for k, v in PARTS.items()}, "harmony", len(harm_hi), "bass tries", tries)
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t_ + ("-" if h else "") for t_, h in ws))
